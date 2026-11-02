"""
Procedural 2.5D render engine for faceless "3D explainer" YouTube Shorts.

Everything is rendered from math (numpy + OpenCV), no external footage:
  * Underwater pool environment with true perspective floor/surface, animated
    caustics, god rays, depth fog and floating particles.
  * "Clay 3D" characters built from height-field tubes (front-surface height of
    swept spheres) that are lit with normals -> reads as soft 3D CGI.
  * Glossy organ / blob shading from signed-distance fields.
  * Caption + HUD rendering with PIL.

Frame format: float32 RGB in [0, 1], shape (H, W, 3).
"""
import math
import functools
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS = 30

FONT_DIR = "/usr/share/fonts/opentype/inter/"
FONT_BLACK = FONT_DIR + "InterDisplay-Black.otf"
FONT_XBOLD = FONT_DIR + "InterDisplay-ExtraBold.otf"
FONT_BOLD = FONT_DIR + "InterDisplay-Bold.otf"
FONT_SEMI = FONT_DIR + "InterDisplay-SemiBold.otf"

PY, PX = np.mgrid[0:H, 0:W].astype(np.float32)
PY4, PX4 = PY[::4, ::4].copy(), PX[::4, ::4].copy()


# --------------------------------------------------------------------------
# small math helpers
# --------------------------------------------------------------------------
def C(r, g, b):
    return np.array([r, g, b], np.float32)


def clamp01(x):
    return np.clip(x, 0.0, 1.0)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def sstep(e0, e1, x):
    """scalar smoothstep"""
    t = min(max((x - e0) / (e1 - e0), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def lin(e0, e1, x):
    return min(max((x - e0) / (e1 - e0), 0.0), 1.0)


def ease_out_back(t, s=1.70158):
    t = min(max(t, 0.0), 1.0) - 1.0
    return t * t * ((s + 1) * t + s) + 1.0


def ease_out_cubic(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def smax(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.maximum(a, b) + h * h * k * 0.25


def smin(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def hash2(a, b):
    v = np.sin(a * 12.9898 + b * 78.233) * 43758.5453
    return v - np.floor(v)


def up4(a):
    """upsample a quarter-res map to full res"""
    return cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)


# --------------------------------------------------------------------------
# compositing
# --------------------------------------------------------------------------
def blit(dst, rgb, a, x0, y0, mode="over"):
    """Composite rgb (h,w,3) with alpha a (h,w) into dst at integer x0,y0."""
    h, w = a.shape
    X0, Y0 = max(x0, 0), max(y0, 0)
    X1, Y1 = min(x0 + w, dst.shape[1]), min(y0 + h, dst.shape[0])
    if X1 <= X0 or Y1 <= Y0:
        return
    sx0, sy0 = X0 - x0, Y0 - y0
    sa = a[sy0:sy0 + (Y1 - Y0), sx0:sx0 + (X1 - X0)][..., None]
    if rgb.ndim == 1:
        sr = rgb[None, None, :]
    else:
        sr = rgb[sy0:sy0 + (Y1 - Y0), sx0:sx0 + (X1 - X0)]
    reg = dst[Y0:Y1, X0:X1]
    if mode == "over":
        dst[Y0:Y1, X0:X1] = reg * (1.0 - sa) + sr * sa
    elif mode == "add":
        dst[Y0:Y1, X0:X1] = reg + sr * sa
    elif mode == "mul":
        dst[Y0:Y1, X0:X1] = reg * (1.0 - sa + sr * sa)


def blit_rgba(dst, rgba, cx, cy, scale=1.0, opacity=1.0, mode="over"):
    """Blit a float RGBA (h,w,4) image centred at (cx,cy) with scale."""
    if opacity <= 0.002:
        return
    img = rgba
    if abs(scale - 1.0) > 1e-3:
        nw = max(1, int(round(img.shape[1] * scale)))
        nh = max(1, int(round(img.shape[0] * scale)))
        img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA)
    h, w = img.shape[:2]
    blit(dst, img[..., :3], img[..., 3] * opacity, int(round(cx - w / 2)), int(round(cy - h / 2)), mode)


def pil_to_rgba(im):
    return np.asarray(im, dtype=np.float32) / 255.0


# --------------------------------------------------------------------------
# caustics
# --------------------------------------------------------------------------
def caustic(u, v, t, iters=4):
    """Classic iterative water-caustic pattern. Returns ~[0,1] bright web."""
    px = u - 250.0
    py = v - 250.0
    ix = px.copy()
    iy = py.copy()
    c = np.ones_like(u)
    inten = 0.005
    for n in range(iters):
        tt = t * (1.0 - (3.5 / (n + 1)))
        nx = px + np.cos(tt - ix) + np.sin(tt + iy)
        ny = py + np.sin(tt - iy) + np.cos(tt + ix)
        ix, iy = nx, ny
        sa = np.sin(ix + tt)
        ca = np.cos(iy + tt)
        sa = np.where(np.abs(sa) < 1e-4, 1e-4, sa)
        ca = np.where(np.abs(ca) < 1e-4, 1e-4, ca)
        a = px / (sa / inten)
        b = py / (ca / inten)
        c += 1.0 / np.sqrt(a * a + b * b + 1e-9)
    c /= iters
    c = 1.17 - np.power(c, 1.4)
    return np.clip(np.power(np.abs(c), 8.0), 0, 2.5).astype(np.float32)


def caustic_field(u, v, t, iters=4):
    """smooth pre-power field; apply sharpen_caustic() after upsampling for crisp lines"""
    px = u - 250.0
    py = v - 250.0
    ix = px.copy()
    iy = py.copy()
    c = np.ones_like(u)
    inten = 0.005
    for n in range(iters):
        tt = t * (1.0 - (3.5 / (n + 1)))
        nx = px + np.cos(tt - ix) + np.sin(tt + iy)
        ny = py + np.sin(tt - iy) + np.cos(tt + ix)
        ix, iy = nx, ny
        sa = np.sin(ix + tt)
        ca = np.cos(iy + tt)
        sa = np.where(np.abs(sa) < 1e-4, 1e-4, sa)
        ca = np.where(np.abs(ca) < 1e-4, 1e-4, ca)
        a = px / (sa / inten)
        b = py / (ca / inten)
        c += 1.0 / np.sqrt(a * a + b * b + 1e-9)
    c /= iters
    return (1.17 - np.power(c, 1.4)).astype(np.float32)


def sharpen_caustic(f, p=8.0):
    return np.clip(np.power(np.abs(f), p), 0, 2.5)


# --------------------------------------------------------------------------
# underwater pool environment
# --------------------------------------------------------------------------
WATER_TOP = C(0.10, 0.52, 0.66)
WATER_BOT = C(0.02, 0.22, 0.36)


class Underwater:
    """Perspective pool: camera looks horizontally down the lane."""

    def __init__(self, seed=3, n_particles=170):
        rng = np.random.default_rng(seed)
        self.p = rng.uniform([-4.0, 0.05, 0.0], [4.0, 2.2, 14.0], size=(n_particles, 3)).astype(np.float32)
        self.ph = rng.uniform(0, 6.283, n_particles).astype(np.float32)
        self.f = 1000.0

    def water_color(self, yh, tint=1.0):
        g = clamp01(PY / H)[..., None]
        col = WATER_TOP * (1 - g) + WATER_BOT * g
        return col * tint

    def fog_at_y(self, y):
        g = min(max(y / H, 0), 1)
        return WATER_TOP * (1 - g) + WATER_BOT * g

    def render(self, t, cam):
        """cam: dict(yh horizon px, hc cam height above floor m, hs surface above cam m,
        x lateral m, z forward m, lane_x m)"""
        f = self.f
        yh = float(cam.get("yh", 820.0))
        hc = cam.get("hc", 1.1)
        hs = cam.get("hs", 0.9)
        cx = cam.get("x", 0.0)
        cz = cam.get("z", 0.0)
        lane_x = cam.get("lane_x", -1.0)
        img = self.water_color(yh)
        yi = int(min(max(yh, 0), H))

        # ---------------- floor (rows below horizon) -----------------
        r0 = max(0, yi - 2)
        if r0 < H:
            py = PY[r0:]
            pxx = PX[r0:]
            fogc = img[r0:]
            dy = py - yh
            z = f * hc / np.maximum(dy, 0.5)
            xw = (pxx - W * 0.5) * z / f + cx
            zw = z + cz
            tile = 0.25
            fx = z / f
            fz = z * z / (f * hc)
            gx = xw / tile
            gz = zw / tile
            dxl = np.abs(gx - np.round(gx)) * tile
            dzl = np.abs(gz - np.round(gz)) * tile
            gw = 0.006
            lx = (1 - smoothstep(gw - fx, gw + fx, dxl)) * (1 - smoothstep(0.012, 0.05, fx))
            lz = (1 - smoothstep(gw - fz, gw + fz, dzl)) * (1 - smoothstep(0.012, 0.05, fz))
            grout = np.maximum(lx, lz)
            shade = 1.0 + hash2(np.floor(gx), np.floor(gz)) * 0.10 - 0.05 + grout * 0.18
            if "lane_z" in cam:
                lane = 1 - smoothstep(0.11 - fz, 0.11 + fz, np.abs(zw - cam["lane_z"]))
            else:
                lane = 1 - smoothstep(0.11 - fx, 0.11 + fx, np.abs(xw - lane_x))
            # caustics: smooth field at 1/4 res, sharpen at full res
            h4 = (H - r0 + 3) // 4
            zz4 = z[::4, ::4]
            cf4 = caustic_field(xw[::4, ::4] * 7.0, zw[::4, ::4] * 7.0, t * 0.9 + 23.0)
            cf = cv2.resize(cf4, (W, H - r0), interpolation=cv2.INTER_CUBIC)
            caus = sharpen_caustic(cf, 9.0) * np.exp(-z * 0.16) * (1 - smoothstep(0.004, 0.02, fz))
            lum = shade * (0.52 + 1.45 * caus)
            tilec = C(0.58, 0.88, 0.95)
            lanec = C(0.03, 0.09, 0.26)
            floor = (tilec * (1 - lane)[..., None] + lanec * lane[..., None]) * lum[..., None]
            absorb = np.exp(-z[..., None] * C(0.26, 0.05, 0.03))
            ff = (1 - np.exp(-z * 0.12))[..., None]
            floor = floor * absorb * (1 - ff) + fogc * ff
            fm = clamp01(dy + 0.5)[..., None]
            img[r0:] = fogc * (1 - fm) + floor * fm
            self._floor_caus = (r0, caus)

        # ---------------- surface (rows above horizon) -----------------
        r1 = min(H, yi + 2)
        if r1 > 0:
            py = PY[:r1]
            pxx = PX[:r1]
            fogc = img[:r1]
            du = yh - py
            zs = f * hs / np.maximum(du, 0.5)
            xs = (pxx - W * 0.5) * zs / f + cx
            zsw = zs + cz
            rf4 = caustic_field(xs[::4, ::4] * 4.5, zsw[::4, ::4] * 4.5, t * 1.3 + 7.0)
            rf = cv2.resize(rf4, (W, r1), interpolation=cv2.INTER_CUBIC)
            rip = sharpen_caustic(rf, 5.0) * np.exp(-zs * 0.10)
            top = smoothstep(yh - 120, -150, py)
            surf = C(0.40, 0.80, 0.92) * (0.50 + 0.75 * top[..., None]) + C(0.80, 1.0, 1.0) * (rip[..., None] * (0.35 + 0.5 * top[..., None]))
            sf = (1 - np.exp(-zs * 0.17))[..., None]
            surf = surf * (1 - sf) + fogc * sf
            sm = clamp01(du + 0.5)[..., None]
            img[:r1] = fogc * (1 - sm) + surf * sm

        # ---------------- god rays (quarter res) -----------------
        sx = W * 0.5 + 260 * math.sin(t * 0.13) + cam.get("ray_x", 0.0)
        sy = -900.0
        ang = np.arctan2(PX4 - sx, PY4 - sy)
        r = (np.sin(ang * 41 + t * 0.6) + np.sin(ang * 67 - t * 0.45 + 1.3) + np.sin(ang * 103 + t * 0.8 + 2.1)) / 3.0
        rays = clamp01(r * 0.5 + 0.25) ** 3 * np.exp(-PY4 / 1100.0)
        rays = up4(rays.astype(np.float32))
        img += C(0.55, 0.88, 1.0) * (rays[..., None] * 0.22 * cam.get("rays", 1.0))
        return img

    def project(self, x, y, z, cam):
        """world (x lateral, y height above floor, z forward) -> screen px, scale px/m"""
        f = self.f
        yh = cam.get("yh", 820.0)
        hc = cam.get("hc", 1.1)
        zr = z - cam.get("z", 0.0)
        s = f / max(zr, 0.05)
        return W * 0.5 + (x - cam.get("x", 0.0)) * s, yh - (y - hc) * s, s

    def particles(self, img, t, cam, amount=1.0):
        f = self.f
        yh = cam.get("yh", 820.0)
        hc = cam.get("hc", 1.1)
        cx = cam.get("x", 0.0)
        cz = cam.get("z", 0.0)
        p = self.p
        zr = np.mod(p[:, 2] - cz, 14.0) + 0.35
        xr = np.mod(p[:, 0] - cx + 4.0 + 0.06 * np.sin(t * 0.3 + self.ph), 8.0) - 4.0
        yr = np.mod(p[:, 1] + 0.02 * t, 2.2) - hc
        sx = W * 0.5 + xr * f / zr
        sy = yh - yr * f / zr
        rad = 0.0045 * f / zr
        bri = np.exp(-zr * 0.18) * amount
        layer = np.zeros((H, W), np.uint8)
        for i in range(len(p)):
            if -20 < sx[i] < W + 20 and -20 < sy[i] < H + 20:
                v = int(min(255, 200 * bri[i]))
                if v < 6:
                    continue
                cv2.circle(layer, (int(sx[i] * 16), int(sy[i] * 16)), max(1, int(rad[i] * 16)), v, -1, cv2.LINE_AA, 4)
        lay = cv2.GaussianBlur(layer, (0, 0), 1.2).astype(np.float32) / 255.0
        img += C(0.75, 0.95, 1.0) * lay[..., None] * 0.9


# --------------------------------------------------------------------------
# bubbles
# --------------------------------------------------------------------------
_bubble_cache = {}


def bubble_sprite(r):
    r = max(2, int(round(r)))
    if r in _bubble_cache:
        return _bubble_cache[r]
    s = r * 2 + 6
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    d = np.sqrt((xx - s / 2) ** 2 + (yy - s / 2) ** 2) / r
    ring = np.exp(-((d - 0.92) ** 2) / 0.012) * 0.85
    fill = (d < 1).astype(np.float32) * 0.10
    hl = np.exp(-(((xx - s / 2 + r * 0.38) ** 2 + (yy - s / 2 + r * 0.38) ** 2) / (r * r * 0.05))) * 0.9
    a = clamp01(ring + fill + hl)
    a = cv2.GaussianBlur(a, (0, 0), 0.6)
    rgba = np.zeros((s, s, 4), np.float32)
    rgba[..., :3] = C(0.85, 0.97, 1.0)
    rgba[..., 3] = a
    _bubble_cache[r] = rgba
    return rgba


class Bubbles:
    def __init__(self, seed=7):
        self.rng = np.random.default_rng(seed)
        self.items = []  # (t0, x0, y0, r, wob)

    def emit_burst(self, t0, x, y, n, spread=12, rmin=4, rmax=14):
        for _ in range(n):
            self.items.append((t0 + self.rng.uniform(0, 0.5), x + self.rng.uniform(-spread, spread),
                               y + self.rng.uniform(-spread, spread), self.rng.uniform(rmin, rmax),
                               self.rng.uniform(0, 6.28)))

    def draw(self, img, t, speed=260.0, dx=0.0, dy=0.0):
        for (t0, x0, y0, r, wob) in self.items:
            age = t - t0
            if age < 0 or age > 4.5:
                continue
            y = y0 - speed * age * (0.6 + r / 30) + dy
            x = x0 + 10 * math.sin(age * 6 + wob) + dx
            if y < -40:
                continue
            spr = bubble_sprite(r * (1 + 0.15 * age))
            blit_rgba(img, spr, x, y, 1.0, min(1.0, age * 6) * (1 - lin(3.5, 4.5, age)), mode="add")


# --------------------------------------------------------------------------
# height-field tube characters
# --------------------------------------------------------------------------
def tube_h(u, v, a, b, ra, rb):
    """front-surface height of a tapered swept sphere from a to b (local units).
    Inside: sqrt(r^2-q^2)  Outside: -(q-r)"""
    bax, bay = b[0] - a[0], b[1] - a[1]
    pax, pay = u - a[0], v - a[1]
    L2 = bax * bax + bay * bay
    if L2 < 1e-9:
        t = 0.0
    else:
        t = np.clip((pax * bax + pay * bay) / L2, 0.0, 1.0)
    dx = pax - bax * t
    dy = pay - bay * t
    q2 = dx * dx + dy * dy
    r = ra + (rb - ra) * t
    ins = r * r - q2
    return np.where(ins > 0, np.sqrt(np.maximum(ins, 0.0)), r - np.sqrt(q2))


def shade_normals(Hpx, clipg=6.0):
    gy, gx = np.gradient(Hpx)
    g2 = gx * gx + gy * gy
    m = np.minimum(1.0, clipg / np.sqrt(g2 + 1e-6))
    gx = gx * m
    gy = gy * m
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    return -gx * inv, -gy * inv, inv


LIGHT_TOP = np.array([0.18, -0.80, 0.57], np.float32)
LIGHT_TOP /= np.linalg.norm(LIGHT_TOP)


def light_shade(nx, ny, nz, base, spec_i=0.3, spec_p=30.0, L=LIGHT_TOP, key=C(1, 1, 1), fill=C(0.12, 0.35, 0.42),
                rim=C(0.3, 0.6, 0.7), keymod=None, wrap=0.3, amb=0.18):
    ndl = nx * L[0] + ny * L[1] + nz * L[2]
    diff = clamp01((ndl + wrap) / (1 + wrap))
    if keymod is not None:
        diff = diff * keymod
    hx, hy, hz = L[0], L[1], L[2] + 1.0
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    ndh = clamp01((nx * hx + ny * hy + nz * hz) / hn)
    spec = ndh ** spec_p * spec_i
    if keymod is not None:
        spec = spec * (0.4 + 0.6 * keymod)
    fl = clamp01(ny * 0.8 + nz * 0.35)
    rimv = (1 - nz) ** 2.5
    if base.ndim == 1:
        base = base[None, None, :]
    col = base * (diff[..., None] * key + amb + fl[..., None] * fill) + spec[..., None] * key + rimv[..., None] * rim
    return col


KEY_UW = C(1.25, 1.2, 1.1)


class Swimmer:
    """Side view swimmer, local units = cm, x forward, y down. Pelvis at origin."""

    MATS = {
        "skin": (C(1.0, 0.66, 0.50), 0.25, 22.0),
        "trunks": (C(0.10, 0.13, 0.33), 0.30, 40.0),
        "cap": (C(0.98, 0.28, 0.08), 0.55, 60.0),
        "goggle": (C(0.04, 0.06, 0.09), 1.1, 90.0),
    }

    def __init__(self, cap=C(0.98, 0.28, 0.08), trunks=C(0.10, 0.13, 0.33)):
        self.cap = cap
        self.trunks = trunks

    def pose(self, t, kick=1.0, limp=0.0, stroke=0.0):
        ph = 2 * math.pi * 1.45 * t
        prims_near, prims_far = [], []
        tb = 0.0
        # legs
        def leg(phase, near):
            th1 = math.pi + (0.17 * math.sin(phase) * kick) + limp * 0.10
            bend = (0.08 + 0.26 * (0.5 + 0.5 * math.sin(phase + 1.3))) * kick + limp * 0.45
            hj = (-6.0, 2.0 + (0 if near else -1.5))
            k = (hj[0] + 44 * math.cos(th1), hj[1] + 44 * math.sin(th1))
            th2 = th1 + bend
            a = (k[0] + 42 * math.cos(th2), k[1] + 42 * math.sin(th2))
            th3 = th2 - 0.10 - 0.2 * limp
            ft = (a[0] + 21 * math.cos(th3), a[1] + 21 * math.sin(th3))
            L = prims_near if near else prims_far
            L.append((hj, k, 9.6, 6.6, "skin", 0.0))
            L.append((k, a, 6.2, 3.9, "skin", 0.0))
            L.append((a, ft, 3.6, 2.0, "skin", 0.0))
            if near:
                L.append(((hj[0] - 1, hj[1]), (hj[0] + 13 * math.cos(th1), hj[1] + 13 * math.sin(th1)), 10.25, 9.75, "trunks", 0.0))
        leg(ph + math.pi, False)
        leg(ph, True)

        # torso
        P = prims_near
        P.append(((-13.0, -1.0), (6.0, -0.5), 16.3, 15.3, "trunks", 0.0))
        P.append(((2.0, 0.0), (24.0, -1.5), 14.0, 13.6, "skin", 0.0))
        P.append(((24.0, -1.5), (45.0, -3.0), 14.0, 15.6, "skin", 0.0))
        S = (49.0, -6.0)
        P.append((S, S, 10.5, 10.5, "skin", 0.0))
        P.append(((51.0, -2.0), (60.0, 0.5 + 2 * limp), 7.2, 6.6, "skin", 0.0))
        hc = (71.5, 3.0 + 5 * limp)
        P.append((hc, hc, 12.6, 12.6, "head", 0.0))
        P.append(((hc[0] + 8.2, hc[1] + 10.0), (hc[0] + 8.2, hc[1] + 10.0), 2.5, 2.5, "skin", 0.0))
        gpos = (hc[0] + 8.6, hc[1] + 4.4)
        P.append((gpos, gpos, 3.0, 3.0, "goggle", 7.6))
        self._head = hc
        self._mouth = (hc[0] + 6.0, hc[1] + 11.0)

        # arms (streamline, or limp floating)
        def arm(near):
            dy0 = 0.0 if near else 1.8
            a1 = -0.06 + limp * (0.50 if near else 0.38)
            e = (S[0] + 30 * math.cos(a1), S[1] + dy0 + 30 * math.sin(a1))
            a2 = a1 + 0.05 + limp * 0.30
            w = (e[0] + 27 * math.cos(a2), e[1] + 27 * math.sin(a2))
            a3 = a2 + 0.04 + limp * 0.22
            hd = (w[0] + 17 * math.cos(a3), w[1] + 17 * math.sin(a3))
            L = prims_near if near else prims_far
            L.append(((S[0], S[1] + dy0), e, 5.6, 4.6, "skin", 0.0 if near else -2.0))
            L.append((e, w, 4.4, 3.3, "skin", 0.0))
            L.append((w, hd, 3.2, 2.2, "skin", 0.0))
        arm(False)
        arm(True)
        return prims_near, prims_far

    def render(self, img, t, sx, sy, scale, angle=0.0, kick=1.0, limp=0.0, dist=2.0, fog=None,
               caus_amp=1.0, desat=0.0, bright=1.0):
        """Draw swimmer centred on pelvis at screen (sx,sy) with px/cm scale."""
        near, far = self.pose(t, kick, limp)
        ca, sa = math.cos(angle), math.sin(angle)
        # bbox
        ext = np.array([[-125, -45], [140, -45], [140, 50], [-125, 50]], np.float32)
        pts = np.stack([sx + scale * (ca * ext[:, 0] - sa * ext[:, 1]), sy + scale * (sa * ext[:, 0] + ca * ext[:, 1])], 1)
        x0 = int(max(0, pts[:, 0].min() - 4))
        x1 = int(min(W, pts[:, 0].max() + 4))
        y0 = int(max(0, pts[:, 1].min() - 4))
        y1 = int(min(H, pts[:, 1].max() + 4))
        if x1 - x0 < 4 or y1 - y0 < 4:
            return
        gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dx = (gx - sx) / scale
        dy = (gy - sy) / scale
        u = ca * dx + sa * dy
        v = -sa * dx + ca * dy

        # caustic light on body
        cb = caustic_field(gx[::3, ::3] * 0.022 + 3.0, gy[::3, ::3] * 0.022, t * 1.1 + 5.0)
        cb = sharpen_caustic(cv2.resize(cb, (x1 - x0, y1 - y0), interpolation=cv2.INTER_CUBIC), 6.0)
        keymod = (0.62 + 1.25 * cb * caus_amp) * bright
        fogc = fog if fog is not None else C(0.05, 0.35, 0.5)

        for layer, prims, dim in (("far", far, 0.58), ("near", near, 1.0)):
            Hh = np.full(u.shape, -1e4, np.float32)
            mat = np.zeros(u.shape, np.int16)
            names = []
            for i, (a, b, ra, rb, m, zoff) in enumerate(prims):
                # prim bbox in local -> restrict
                h = tube_h(u, v, a, b, ra, rb)
                if zoff != 0.0:
                    h = np.where(h > 0, h + zoff, h)
                k = 3.0 if m in ("skin", "trunks", "head") else 0.3
                better = h > Hh
                mat = np.where(better, i, mat)
                Hh = smax(Hh, h, k) if k > 0.5 else np.maximum(Hh, h)
                names.append(m)
            Hpx = Hh * scale
            alpha = clamp01(0.5 + Hpx)
            if alpha.max() <= 0:
                continue
            nx, ny, nz = shade_normals(np.maximum(Hpx, -2.0))
            col = np.zeros(u.shape + (3,), np.float32)
            hc = self._head
            for i, m in enumerate(names):
                sel = mat == i
                if not sel.any():
                    continue
                if m == "head":
                    # cap / strap / skin split
                    du = u - hc[0]
                    dv = v - hc[1]
                    capm = (du * 0.75 - dv * 0.66) > -2.5
                    strap = np.abs((du - 7.8) * 0.24 - (dv - 4.0) * (-0.97)) < 0.9
                    for sub, (bc, si, sp) in ((capm & ~strap, (self.cap, 0.55, 60.0)),
                                              (~capm & ~strap, self.MATS["skin"]),
                                              (strap, (C(0.05, 0.05, 0.07), 0.3, 30.0))):
                        s2 = sel & sub
                        if s2.any():
                            c = light_shade(nx[s2], ny[s2], nz[s2], bc[None, :], si, sp, keymod=keymod[s2], key=KEY_UW, amb=0.14)
                            col[s2] = c.reshape(-1, 3)
                    continue
                bc, si, sp = self.MATS[m]
                if m == "trunks":
                    bc = self.trunks
                c = light_shade(nx[sel], ny[sel], nz[sel], bc[None, :], si, sp, keymod=keymod[sel], key=KEY_UW, amb=0.14)
                col[sel] = c.reshape(-1, 3)
            col *= dim
            # underwater absorption + fog
            col = col * np.exp(-dist * C(0.16, 0.035, 0.02)) * 1.12
            ff = 1 - math.exp(-dist * 0.115)
            col = col * (1 - ff) + fogc * ff
            if desat > 0:
                lum = (col @ C(0.3, 0.55, 0.15))[..., None]
                col = col * (1 - desat) + lum * desat
            blit(img, col, alpha, x0, y0)
        # mouth position for bubbles (screen)
        mx, my = self._mouth
        self.mouth_screen = (sx + scale * (ca * mx - sa * my), sy + scale * (sa * mx + ca * my))


# --------------------------------------------------------------------------
# SDF blob shading (organs)
# --------------------------------------------------------------------------
def sd_circle(x, y, cx, cy, r):
    return np.sqrt((x - cx) ** 2 + (y - cy) ** 2) - r


def sd_ellipse_approx(x, y, cx, cy, rx, ry, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    dx, dy = x - cx, y - cy
    u = (c * dx + s * dy) / rx
    v = (-s * dx + c * dy) / ry
    k = np.sqrt(u * u + v * v)
    return (k - 1.0) * min(rx, ry)


def sd_capsule(x, y, ax, ay, bx, by, ra, rb=None):
    if rb is None:
        rb = ra
    bax, bay = bx - ax, by - ay
    L2 = bax * bax + bay * bay
    t = np.clip(((x - ax) * bax + (y - ay) * bay) / max(L2, 1e-9), 0, 1)
    dx = x - ax - bax * t
    dy = y - ay - bay * t
    return np.sqrt(dx * dx + dy * dy) - (ra + (rb - ra) * t)


def bevel_height(d, R):
    s = np.clip(-d, 0, R)
    hin = np.sqrt(np.maximum(R * R - (R - s) ** 2, 0))
    return np.where(d < 0, hin, -d)


def shade_blob(d, R, base, spec_i=0.5, spec_p=40.0, bump=None, L=None, sss=0.0, rim=C(0.6, 0.5, 0.6), fill=C(0.15, 0.1, 0.2),
               amb=0.16, wrap=0.4, key=C(1, 1, 1)):
    Hh = bevel_height(d, R)
    if bump is not None:
        Hh = Hh + bump * clamp01(-d / (R * 0.6))
    nx, ny, nz = shade_normals(np.maximum(Hh, -2.0), clipg=8.0)
    if L is None:
        L = np.array([-0.35, -0.6, 0.72], np.float32)
        L /= np.linalg.norm(L)
    col = light_shade(nx, ny, nz, base, spec_i, spec_p, L=L, key=key, fill=fill, rim=rim, wrap=wrap, amb=amb)
    if sss > 0:
        col += base[None, None, :] * (sss * clamp01(1 - nz))[..., None]
    alpha = clamp01(0.5 - d)
    return col, alpha, (nx, ny, nz)


# --------------------------------------------------------------------------
# glossy sphere sprites (molecules, cells highlights)
# --------------------------------------------------------------------------
@functools.lru_cache(maxsize=256)
def sphere_sprite(r, col):
    r = max(2, int(r))
    s = 2 * r + 4
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    d = sd_circle(xx, yy, s / 2, s / 2, r)
    base = np.array(col, np.float32)
    c, a, _ = shade_blob(d, r, base, spec_i=0.8, spec_p=50.0, rim=base * 0.5 + 0.2, fill=base * 0.2, amb=0.25)
    rgba = np.concatenate([c, a[..., None]], -1).astype(np.float32)
    return rgba


def glow_dot(img, x, y, r, col, strength=1.0):
    s = int(r * 3)
    if s < 2:
        return
    yy, xx = np.mgrid[-s:s + 1, -s:s + 1].astype(np.float32)
    g = np.exp(-(xx * xx + yy * yy) / (2 * (r * 0.8) ** 2)) * strength
    blit(img, np.asarray(col, np.float32), g, int(x) - s, int(y) - s, mode="add")


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------
@functools.lru_cache(maxsize=64)
def font(path, size):
    return ImageFont.truetype(path, size)


def text_rgba(text, size=90, fill=(255, 255, 255), stroke=10, stroke_fill=(0, 0, 0), path=FONT_BLACK, shadow=True,
              spacing=0, colors=None, glow=None):
    """Render a single line; `colors` optional list of per-word fill colours."""
    fnt = font(path, size)
    words = text.split(" ")
    space = fnt.getlength(" ") + spacing
    widths = [fnt.getlength(w) for w in words]
    tw = int(sum(widths) + space * (len(words) - 1)) + 2 * stroke + 40
    asc, desc = fnt.getmetrics()
    th = asc + desc + 2 * stroke + 40
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    x = 20 + stroke
    for i, w in enumerate(words):
        fc = colors[i] if colors is not None else fill
        dr.text((x, 20 + stroke), w, font=fnt, fill=tuple(fc) + (255,), stroke_width=stroke, stroke_fill=tuple(stroke_fill) + (255,))
        x += widths[i] + space
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        a = im.split()[3].filter(ImageFilter.GaussianBlur(10))
        sh.putalpha(a.point(lambda v: int(v * 0.65)))
        sh = Image.composite(sh, sh, sh)
        base = Image.new("RGBA", im.size, (0, 0, 0, 0))
        base.alpha_composite(sh, (0, 8))
        base.alpha_composite(im)
        im = base
    if glow is not None:
        g = Image.new("RGBA", im.size, tuple(glow) + (0,))
        a = im.split()[3].filter(ImageFilter.GaussianBlur(18))
        g.putalpha(a.point(lambda v: int(v * 0.8)))
        base = Image.new("RGBA", im.size, (0, 0, 0, 0))
        base.alpha_composite(g)
        base.alpha_composite(im)
        im = base
    return pil_to_rgba(im)


def label_rgba(text, size=40, fg=(255, 255, 255), bg=(10, 20, 30), alpha=200, pad=(22, 12), radius=18, path=FONT_XBOLD,
               border=None):
    fnt = font(path, size)
    tw = int(fnt.getlength(text))
    asc, desc = fnt.getmetrics()
    w = tw + 2 * pad[0]
    h = asc + desc + 2 * pad[1]
    S = 2
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, w * S - 1, h * S - 1], radius=radius * S, fill=tuple(bg) + (alpha,),
                         outline=(tuple(border) + (255,)) if border else None, width=3 * S if border else 0)
    im = im.resize((w, h), Image.LANCZOS)
    dr = ImageDraw.Draw(im)
    dr.text((pad[0], pad[1]), text, font=fnt, fill=tuple(fg) + (255,))
    return pil_to_rgba(im)


# --------------------------------------------------------------------------
# post
# --------------------------------------------------------------------------
_vig = None


def vignette_map():
    global _vig
    if _vig is None:
        d = np.sqrt(((PX - W / 2) / (W * 0.62)) ** 2 + ((PY - H / 2) / (H * 0.60)) ** 2)
        _vig = (1 - 0.55 * smoothstep(0.55, 1.25, d)).astype(np.float32)
    return _vig


def post(img, t, bloom=0.35, grain=0.018, vig=1.0, tunnel=0.0, desat=0.0, exposure=1.0, seed=0):
    img = img * exposure
    if desat > 0:
        lum = (img @ C(0.3, 0.55, 0.15))[..., None]
        img = img * (1 - desat) + lum * desat
    if bloom > 0:
        small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        br = np.maximum(small - 0.72, 0)
        br = cv2.GaussianBlur(br, (0, 0), 9)
        img = img + up4(br) * bloom * 2.2
    if vig > 0:
        v = vignette_map()
        img = img * (1 - vig + vig * v[..., None])
    if tunnel > 0:
        d = np.sqrt(((PX - W / 2) / (W * 0.5)) ** 2 + ((PY - H * 0.47) / (H * 0.5)) ** 2)
        rr = 1.35 * (1 - tunnel)
        m = smoothstep(rr * 0.35, rr + 0.05, d)
        img = img * (1 - m[..., None])
    if grain > 0:
        rng = np.random.default_rng(int(t * 1000) + seed)
        n = rng.standard_normal((H // 2, W // 2)).astype(np.float32)
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_LINEAR)
        img = img + n[..., None] * grain
    return img


def tonemap(img):
    # linear up to 0.8, soft shoulder above (keeps designed colours, no clipping)
    x = np.maximum(img, 0)
    y = np.where(x < 0.8, x, 0.8 + 0.2 * (1 - np.exp(-(x - 0.8) / 0.2)))
    return (y * 255 + 0.5).astype(np.uint8)
