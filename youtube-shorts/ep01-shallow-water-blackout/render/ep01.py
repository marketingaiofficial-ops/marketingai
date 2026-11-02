"""
Episode 01 - "Shallow Water Blackout"
Scene timeline, anatomy renders, HUD, captions and the parallel render/encode.

usage:
  python3 ep01.py preview 2.0 10.5 27.0      # write preview JPGs for given times
  python3 ep01.py render [workers]           # full render -> ../out/video_noaudio.mp4
"""
import os
import sys
import json
import math
import time
import subprocess
import functools
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
WORDS = json.load(open(os.path.join(ROOT, "assets", "words.json")))["words"]
DUR = 61.45

# ==========================================================================
# shared colours / sprites
# ==========================================================================
O2_COL = (0.25, 0.78, 1.0)
CO2_C = (0.30, 0.30, 0.34)
CO2_O = (1.0, 0.62, 0.16)
RED = (1.0, 0.22, 0.2)

UW = Underwater(n_particles=260)
SWIM = Swimmer()
BUDDY = Swimmer(cap=C(1.0, 0.82, 0.08), trunks=C(0.05, 0.32, 0.26))


def draw_o2(img, x, y, ang, r=11, alpha=1.0):
    dx, dy = math.cos(ang) * r * 0.78, math.sin(ang) * r * 0.78
    spr = sphere_sprite(int(r), O2_COL)
    glow_dot(img, x, y, r * 1.6, C(*O2_COL) * 0.25 * alpha)
    blit_rgba(img, spr, x - dx, y - dy, opacity=alpha)
    blit_rgba(img, spr, x + dx, y + dy, opacity=alpha)


def draw_co2(img, x, y, ang, r=10, alpha=1.0):
    dx, dy = math.cos(ang) * r * 1.45, math.sin(ang) * r * 1.45
    so = sphere_sprite(int(r * 0.92), CO2_O)
    sc = sphere_sprite(int(r), CO2_C)
    glow_dot(img, x, y, r * 2.0, C(*CO2_O) * 0.18 * alpha)
    blit_rgba(img, so, x - dx, y - dy, opacity=alpha)
    blit_rgba(img, so, x + dx, y + dy, opacity=alpha)
    blit_rgba(img, sc, x, y, opacity=alpha)


def radial_bg(c_in, c_out, cx=540, cy=900, r=1150.0):
    d = np.sqrt((PX - cx) ** 2 + (PY - cy) ** 2) / r
    m = smoothstep(0, 1, d)[..., None]
    return (C(*c_in) * (1 - m) + C(*c_out) * m).astype(np.float32)


class Bokeh:
    def __init__(self, n=26, seed=11, col=(0.4, 0.8, 1.0)):
        rng = np.random.default_rng(seed)
        self.p = rng.uniform([0, 0, 18, 0], [W, H, 70, 6.28], size=(n, 4))
        self.col = C(*col)

    def draw(self, img, t, amt=0.10):
        for x, y, r, ph in self.p:
            yy = (y - t * 14 * (r / 40)) % (H + 200) - 100
            xx = x + 20 * math.sin(t * 0.3 + ph)
            glow_dot(img, xx, yy, r, self.col * amt * (0.6 + 0.4 * math.sin(t * 0.7 + ph)))


BOKEH_TEAL = Bokeh()
BOKEH_RED = Bokeh(seed=5, col=(1.0, 0.35, 0.3))


# ==========================================================================
# HUD + cards (PIL, 2x supersampled)
# ==========================================================================
def _rr(dr, box, r, **kw):
    dr.rounded_rectangle(box, radius=r, **kw)


def hud_panel(bars, width=960, title=None, alarm=None):
    """bars: list of dict(label, value 0..1, color(rgb255), text, marker (0..1) or None)."""
    S = 2
    row_h = 112
    top = 70 if title else 22
    h = top + row_h * len(bars) + 18
    im = Image.new("RGBA", (width * S, h * S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    _rr(dr, [0, 0, width * S - 1, h * S - 1], 34 * S, fill=(6, 14, 22, 175), outline=(120, 200, 230, 70), width=2 * S)
    if title:
        dr.text((34 * S, 18 * S), title, font=font(FONT_XBOLD, 30 * S), fill=(170, 220, 240, 255))
    bar_x0 = 205
    bar_x1 = width - (330 if alarm is not None else 170)
    for i, b in enumerate(bars):
        y = top + i * row_h
        col = tuple(int(c) for c in b["color"])
        # icon pill
        _rr(dr, [26 * S, (y + 20) * S, 180 * S, (y + 92) * S], 36 * S, fill=col + (255,))
        lf = font(FONT_BLACK, 40 * S)
        lw = dr.textlength(b["label"], font=lf)
        dr.text(((103 * S - lw / 2), (y + 30) * S), b["label"], font=lf, fill=(8, 14, 20, 255))
        # track
        _rr(dr, [bar_x0 * S, (y + 38) * S, bar_x1 * S, (y + 74) * S], 18 * S, fill=(30, 44, 56, 255))
        v = min(max(b["value"], 0.0), 1.0)
        fx1 = bar_x0 + (bar_x1 - bar_x0) * v
        if fx1 - bar_x0 > 36:
            _rr(dr, [bar_x0 * S, (y + 38) * S, int(fx1 * S), (y + 74) * S], 18 * S, fill=col + (255,))
            _rr(dr, [(bar_x0 + 8) * S, (y + 43) * S, int((fx1 - 8) * S), (y + 52) * S], 5 * S, fill=(255, 255, 255, 70))
        if b.get("marker") is not None:
            mx = bar_x0 + (bar_x1 - bar_x0) * b["marker"]
            for yy in range(y + 26, y + 88, 10):
                dr.line([mx * S, yy * S, mx * S, (yy + 5) * S], fill=(255, 90, 80, 255), width=4 * S)
            mf = font(FONT_BLACK, 20 * S)
            mt = b.get("marker_text", "ALARM")
            mw = dr.textlength(mt, font=mf)
            dr.text((mx * S - mw / 2, (y + 2) * S), mt, font=mf, fill=(255, 110, 100, 255))
        tf = font(FONT_BLACK, 44 * S)
        dr.text(((bar_x1 + 22) * S, (y + 30) * S), b["text"], font=tf, fill=(255, 255, 255, 255))
    if alarm is not None:
        # alarm light at right side spanning rows
        cx = width - 88
        cy = top + row_h * len(bars) / 2 - 6
        on = alarm.get("on", 0.0)
        base_col = (int(70 + 185 * on), int(80 - 40 * on), int(90 - 50 * on))
        dr.pieslice([(cx - 46) * S, (cy - 50) * S, (cx + 46) * S, (cy + 42) * S], 180, 360, fill=base_col + (255,))
        _rr(dr, [(cx - 56) * S, (cy - 4) * S, (cx + 56) * S, (cy + 16) * S], 6 * S, fill=(150, 160, 170, 255))
        if alarm.get("muted", False):
            dr.line([(cx - 52) * S, (cy - 56) * S, (cx + 52) * S, (cy + 24) * S], fill=(255, 70, 60, 255), width=8 * S)
        lt = alarm.get("text", "")
        if lt:
            lf2 = font(FONT_BLACK, 22 * S)
            lw2 = dr.textlength(lt, font=lf2)
            dr.text((cx * S - lw2 / 2, (cy + 26) * S), lt, font=lf2, fill=(255, 120, 110, 255) if alarm.get("muted") else (255, 255, 255, 255))
    im = im.resize((width, h), Image.LANCZOS)
    return pil_to_rgba(im)


def rule_card(n, line1, line2, width=980):
    S = 2
    h = 190
    im = Image.new("RGBA", (width * S, h * S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    _rr(dr, [0, 0, width * S - 1, h * S - 1], 40 * S, fill=(8, 14, 22, 215), outline=(255, 80, 70, 200), width=4 * S)
    cx, cy, r = 105, h // 2, 62
    dr.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=(232, 52, 48, 255))
    k = 26
    dr.line([(cx - k) * S, (cy - k) * S, (cx + k) * S, (cy + k) * S], fill=(255, 255, 255, 255), width=14 * S)
    dr.line([(cx - k) * S, (cy + k) * S, (cx + k) * S, (cy - k) * S], fill=(255, 255, 255, 255), width=14 * S)
    f1 = 58
    while font(FONT_BLACK, f1 * S).getlength(line1) > 745 * S:
        f1 -= 2
    dr.text((200 * S, (30 + (58 - f1) * 0.6) * S), line1, font=font(FONT_BLACK, f1 * S), fill=(255, 255, 255, 255))
    dr.text((202 * S, 108 * S), line2, font=font(FONT_BOLD, 40 * S), fill=(255, 200, 190, 255))
    im = im.resize((width, h), Image.LANCZOS)
    return pil_to_rgba(im)


@functools.lru_cache(maxsize=8)
def rule_cards():
    return (rule_card(1, "NEVER HYPERVENTILATE", "before going underwater"),
            rule_card(2, "NEVER HOLD YOUR BREATH", "alone - always have a spotter"))


@functools.lru_cache(maxsize=32)
def label(text, size=36, fg=(255, 255, 255), bg=(8, 16, 26), border=None):
    return label_rgba(text, size=size, fg=fg, bg=bg, alpha=200, border=border)


def pop(t, t0, dur=0.28):
    """scale/opacity helper for pop-in"""
    k = (t - t0) / dur
    if k <= 0:
        return 0.0, 0.0
    return ease_out_back(k, 2.2) if k < 1 else 1.0, min(1.0, k * 2.5)


def red_x(img, cx, cy, size, t, t0):
    """animated big red X (two strokes)"""
    if t < t0:
        return
    k1 = ease_out_cubic((t - t0) / 0.14)
    k2 = ease_out_cubic((t - t0 - 0.12) / 0.14)
    lay = np.zeros((H, W), np.uint8)
    s = size
    if k1 > 0:
        cv2.line(lay, (int(cx - s), int(cy - s)), (int(cx - s + 2 * s * k1), int(cy - s + 2 * s * k1)), 255, 26, cv2.LINE_AA)
    if k2 > 0:
        cv2.line(lay, (int(cx + s), int(cy - s)), (int(cx + s - 2 * s * k2), int(cy - s + 2 * s * k2)), 255, 26, cv2.LINE_AA)
    a = lay.astype(np.float32) / 255.0
    sh = cv2.GaussianBlur(a, (0, 0), 8)
    img *= (1 - sh[..., None] * 0.5)
    img[:] = img * (1 - a[..., None]) + C(*RED) * a[..., None]


# ==========================================================================
# precomputed anatomy layers (built lazily once per process)
# ==========================================================================
@functools.lru_cache(maxsize=1)
def anatomy_layers():
    L = {}
    # ---------------- background ----------------
    L["bg_teal"] = radial_bg((0.05, 0.14, 0.21), (0.008, 0.02, 0.045), cy=880)
    L["bg_red"] = radial_bg((0.22, 0.035, 0.045), (0.04, 0.005, 0.012), cy=900)
    L["bg_navy"] = radial_bg((0.06, 0.08, 0.16), (0.01, 0.012, 0.03), cy=800)

    # ---------------- hologram body (front) ----------------
    d = sd_ellipse_approx(PX, PY, 540, 330, 100, 124)
    d = smin(d, sd_capsule(PX, PY, 540, 430, 540, 585, 50), 40)
    d = smin(d, sd_capsule(PX, PY, 345, 690, 735, 690, 86), 70)
    d = smin(d, sd_capsule(PX, PY, 540, 760, 540, 1500, 200, 182), 90)
    d = smin(d, sd_capsule(PX, PY, 262, 730, 205, 1310, 58, 44), 25)
    d = smin(d, sd_capsule(PX, PY, 818, 730, 875, 1310, 58, 44), 25)
    edge = np.exp(-np.abs(d) / 5.0)
    inner = np.exp(-np.maximum(-d, 0) / 55.0) * (d < 0)
    holo = edge * 0.95 + inner * 0.32 + (d < 0) * 0.045
    # ribs hint
    for i in range(7):
        yy = 790 + i * 62
        rr = np.abs(np.sqrt(((PX - 540) / 1.55) ** 2 + (PY - yy + 120) ** 2) - 150)
        holo += np.exp(-rr / 3.0) * 0.10 * (np.abs(PX - 540) > 30) * (d < -20) * (np.abs(PX - 540) < 190)
    spine = np.exp(-np.abs(PX - 540) / 6.0) * (PY > 600) * (PY < 1400) * 0.10
    holo += spine
    holo *= 1 - smoothstep(1180, 1420, PY)
    L["holo"] = (holo[..., None] * C(0.35, 0.80, 1.0)).astype(np.float32)

    # ---------------- lungs / trachea / heart (front) ----------------
    x0, y0, x1, y1 = 250, 440, 830, 1240
    gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)

    def lung(xx, yy, left):
        dd = smin(sd_circle(xx, yy, 455, 772, 60), sd_circle(xx, yy, 430, 900, 116), 70)
        dd = smin(dd, sd_ellipse_approx(xx, yy, 424, 1032, 138, 118), 70)
        dd = smax(dd, xx - 516, 34)
        dd = smax(dd, yy - 1148, 44)
        return dd

    dR = lung(gx, gy, False)
    gxm = 1080 - gx
    dL = lung(gxm, gy, True)
    dL = smax(dL, -sd_circle(gx, gy, 600, 1060, 78), 34)

    def groove(xx, yy, ax, ay, bx, by, w=4.0, depth=7.0):
        dd = sd_capsule(xx, yy, ax, ay, bx, by, 0.0)
        return -depth * np.exp(-(dd * dd) / (2 * w * w))

    tex = 1.3 * (np.sin(gx * 0.33) * np.sin(gy * 0.29) + 0.6 * np.sin(gx * 0.19 + gy * 0.23))
    bR = tex + groove(gx, gy, 318, 905, 512, 878) + groove(gx, gy, 478, 778, 404, 960) + groove(gx, gy, 404, 960, 352, 1110)
    bL = tex + groove(gx, gy, 600, 792, 690, 960) + groove(gx, gy, 690, 960, 742, 1112)
    lung_col = C(0.95, 0.44, 0.50)
    Lgt = np.array([-0.35, -0.6, 0.72], np.float32)
    Lgt /= np.linalg.norm(Lgt)
    cR, aR, _ = shade_blob(dR, 95, lung_col, spec_i=0.42, spec_p=30, bump=bR, sss=0.22, rim=C(0.6, 0.35, 0.45), fill=C(0.25, 0.08, 0.12), L=Lgt)
    cL, aL, _ = shade_blob(dL, 95, lung_col, spec_i=0.42, spec_p=30, bump=bL, sss=0.22, rim=C(0.6, 0.35, 0.45), fill=C(0.25, 0.08, 0.12), L=Lgt)
    # heart (behind lungs)
    dH = smin(sd_ellipse_approx(gx, gy, 578, 1080, 78, 96, -0.6), sd_circle(gx, gy, 556, 1018, 46), 36)
    cH, aH, _ = shade_blob(dH, 55, C(0.52, 0.07, 0.10), spec_i=0.5, spec_p=40, sss=0.2, rim=C(0.6, 0.2, 0.25), fill=C(0.2, 0.03, 0.05), L=Lgt)
    # trachea + bronchi
    dT = sd_capsule(gx, gy, 540, 560, 540, 772, 22)
    dB1 = sd_capsule(gx, gy, 540, 770, 470, 828, 15, 13)
    dB2 = sd_capsule(gx, gy, 540, 770, 610, 828, 15, 13)
    dTr = smin(smin(dT, dB1, 10), dB2, 10)
    rings = 2.2 * np.sin(gy * 0.33) * (gy < 770)
    cT, aT, _ = shade_blob(dTr, 20, C(0.93, 0.78, 0.74), spec_i=0.5, spec_p=40, bump=rings, sss=0.15, L=Lgt)

    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.float32)

    def over(c, a):
        rgba[..., :3] = rgba[..., :3] * (1 - a[..., None]) + c * a[..., None]
        rgba[..., 3] = rgba[..., 3] * (1 - a) + a
    L["heart"] = (cH.astype(np.float32), aH.astype(np.float32))
    over(cR, aR)
    over(cL, aL)
    L["lungs"] = rgba.copy()
    tr = np.zeros_like(rgba)
    tr[..., :3] = cT
    tr[..., 3] = aT
    L["trachea"] = tr
    L["lung_box"] = (x0, y0)

    # ---------------- blood vessel ----------------
    yc, R = 900.0, 360.0
    dyv = (PY - yc) / R
    inside = np.abs(dyv) < 1
    hcyl = np.sqrt(np.maximum(1 - dyv * dyv, 0))
    plasma = C(0.55, 0.07, 0.07) * (0.35 + 0.65 * hcyl[..., None])
    wall = np.exp(-((np.abs(dyv) - 0.97) ** 2) / 0.0016)
    bgv = L["bg_red"].copy()
    m = smoothstep(1.0, 0.985, np.abs(dyv))[..., None]
    vess = bgv * (1 - m) + plasma * m
    vess += (wall[..., None] * C(0.95, 0.35, 0.38) * 0.75)
    L["vessel_bg"] = vess.astype(np.float32)
    # front wall glossy highlight + tissue streaks (overlay)
    spec = np.exp(-((dyv + 0.62) ** 2) / 0.004) * 0.22 + np.exp(-((dyv - 0.75) ** 2) / 0.01) * 0.06
    streak = (0.5 + 0.5 * np.sin(PX * 0.012 + np.sin(PY * 0.02) * 2)) * 0.05
    fw = np.zeros((H, W, 4), np.float32)
    fw[..., :3] = C(1.0, 0.75, 0.75)
    fw[..., 3] = (spec + streak * inside) * inside
    L["vessel_front"] = fw

    # ---------------- RBC sprites (several tilts) ----------------
    sprites = []
    for k in range(10):
        tilt = k / 9 * 1.15  # rad
        r = 90
        s = 2 * r + 12
        yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
        u = (xx - s / 2) / r
        v = (yy - s / 2) / (r * max(math.cos(tilt), 0.28))
        rho2 = u * u + v * v
        rho = np.sqrt(rho2)
        T = np.sqrt(np.maximum(1 - rho2, 0)) * (0.81 + 7.83 * rho2 - 4.39 * rho2 * rho2) / 2.6
        hgt = T * r * 0.42 * (0.6 + 0.4 * math.cos(tilt))
        dd = (rho - 1.0) * r * max(math.cos(tilt), 0.28)
        hgt = np.where(rho < 1, hgt, -dd)
        nx, ny, nz = shade_normals(np.maximum(hgt, -2.0), clipg=5.0)
        Ls = np.array([-0.4, -0.65, 0.65], np.float32)
        Ls /= np.linalg.norm(Ls)
        col = light_shade(nx, ny, nz, C(0.82, 0.10, 0.11), 0.55, 36.0, L=Ls, fill=C(0.25, 0.03, 0.04), rim=C(0.7, 0.2, 0.2),
                          amb=0.22, wrap=0.5)
        col += C(0.82, 0.10, 0.11) * (0.25 * clamp01(1 - nz))[..., None]
        a = clamp01(0.5 - dd)
        sprites.append(np.concatenate([col, a[..., None]], -1).astype(np.float32))
    L["rbc"] = sprites

    # ---------------- brain (side view) ----------------
    bx0, by0, bx1, by1 = 120, 420, 960, 1260
    gy, gx = np.mgrid[by0:by1, bx0:bx1].astype(np.float32)
    dC = sd_ellipse_approx(gx, gy, 520, 760, 318, 222)
    dC = smin(dC, sd_ellipse_approx(gx, gy, 700, 772, 188, 178), 80)
    dC = smin(dC, sd_ellipse_approx(gx, gy, 338, 800, 182, 168), 80)
    dC = smin(dC, sd_ellipse_approx(gx, gy, 585, 908, 178, 92, -0.12), 50)
    # gyri: two families of meandering warped stripes, blended
    ph1 = gx * 0.060 + 2.8 * np.sin(gy * 0.020 + 0.7) + 1.9 * np.sin(gx * 0.016 + gy * 0.025) + 1.1 * np.sin(gy * 0.051 + gx * 0.012)
    ph2 = gy * 0.058 + 2.6 * np.sin(gx * 0.022 + 1.3) + 1.7 * np.sin(gy * 0.017 - gx * 0.021 + 0.4) + 1.0 * np.sin(gx * 0.047)
    blend = 0.5 + 0.5 * np.sin(gx * 0.011 + gy * 0.009 + 1.0)
    g1 = (0.5 + 0.5 * np.cos(ph1)) ** 0.45
    g2 = (0.5 + 0.5 * np.cos(ph2)) ** 0.45
    gyri = 12 * (g1 * blend + g2 * (1 - blend))
    sylvian = sd_capsule(gx, gy, 430, 885, 700, 820, 0)
    central = sd_capsule(gx, gy, 600, 545, 520, 840, 0)
    gyri += -14 * np.exp(-(sylvian ** 2) / 120) - 8 * np.exp(-(central ** 2) / 70)
    cC, aC, nC = shade_blob(dC, 70, C(0.95, 0.63, 0.66), spec_i=0.38, spec_p=26, bump=gyri, sss=0.2,
                            rim=C(0.5, 0.4, 0.6), fill=C(0.2, 0.1, 0.18), L=Lgt)
    cav = clamp01(0.62 + 0.035 * gyri)[..., None]
    cC = cC * cav
    dCb = sd_ellipse_approx(gx, gy, 368, 985, 140, 86, 0.12)
    fol = 3.0 * np.sin(np.sqrt((gx - 380) ** 2 + (gy - 890) ** 2) * 0.36)
    cCb, aCb, _ = shade_blob(dCb, 50, C(0.86, 0.52, 0.58), spec_i=0.3, spec_p=24, bump=fol, sss=0.15, L=Lgt)
    cCb = cCb * clamp01(0.75 + 0.08 * fol)[..., None]
    dBs = smin(sd_capsule(gx, gy, 522, 930, 552, 1190, 40, 31), sd_circle(gx, gy, 530, 985, 50), 30)
    cBs, aBs, _ = shade_blob(dBs, 40, C(0.90, 0.60, 0.60), spec_i=0.35, spec_p=30, sss=0.15, L=Lgt)
    rgba = np.zeros((by1 - by0, bx1 - bx0, 4), np.float32)

    def over2(c, a):
        rgba[..., :3] = rgba[..., :3] * (1 - a[..., None]) + c * a[..., None]
        rgba[..., 3] = rgba[..., 3] * (1 - a) + a
    over2(cBs, aBs)
    over2(cCb, aCb)
    over2(cC, aC)
    L["brain"] = rgba
    L["brain_box"] = (bx0, by0)
    return L


def warp_rgba_into(img, rgba, x0, y0, scale=1.0, ax=None, ay=None, opacity=1.0):
    """scale an RGBA layer around anchor (screen coords) and composite"""
    h, w = rgba.shape[:2]
    if ax is None:
        ax, ay = x0 + w / 2, y0 + h / 2
    if abs(scale - 1) < 1e-4:
        blit(img, rgba[..., :3], rgba[..., 3] * opacity, x0, y0)
        return
    # destination box
    lx = ax - (ax - x0) * scale
    ly = ay - (ay - y0) * scale
    nw, nh = int(w * scale) + 2, int(h * scale) + 2
    M = np.float32([[scale, 0, lx - int(lx)], [0, scale, ly - int(ly)]])
    out = cv2.warpAffine(rgba, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    blit(img, out[..., :3], out[..., 3] * opacity, int(lx), int(ly))


# ==========================================================================
# scenes
# ==========================================================================
def floor_shadow(img, cam, wx, wy, wz, strength=1.0):
    """soft blob shadow on the pool floor under a swimmer at world (wx, wy, wz)"""
    fx, fy, s = UW.project(wx + 0.06, 0.0, wz, cam)
    f, hc = UW.f, cam.get("hc", 1.1)
    zr = wz - cam.get("z", 0.0)
    rx = 1.05 * s * (1 + 0.5 * wy)
    ry = f * hc * 0.20 / (zr * zr) * (1 + 0.8 * wy) + 6
    k = 0.55 * math.exp(-wy * 1.6) * strength
    x0, x1 = int(max(0, fx - 2 * rx)), int(min(W, fx + 2 * rx))
    y0, y1 = int(max(0, fy - 3 * ry)), int(min(H, fy + 3 * ry))
    if x1 <= x0 or y1 <= y0 or k < 0.01:
        return
    gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    m = np.exp(-(((gx - fx) / rx) ** 4) - ((gy - fy) / ry) ** 2) * k
    img[y0:y1, x0:x1] *= (1 - m[..., None] * C(0.75, 0.6, 0.55))


def swimmer_at(img, t, cam, wx, wy, wz, **kw):
    floor_shadow(img, cam, wx, wy, wz)
    sx, sy, s = UW.project(wx, wy, wz, cam)
    fog = UW.fog_at_y(sy)
    SWIM.render(img, t, sx, sy, s * 0.01, dist=wz - cam.get("z", 0.0), fog=fog, **kw)
    return sx, sy, s * 0.01


def head_screen(sx, sy, sc, angle=0.0):
    hx, hy = SWIM._head
    ca, sa = math.cos(angle), math.sin(angle)
    return sx + sc * (ca * hx - sa * hy), sy + sc * (sa * hx + ca * hy)


# --- S1 hook: 0 - 5.4 -------------------------------------------------------
def scene_hook(t):
    v = 1.05
    cam = dict(yh=720, hc=1.15, hs=0.85, x=v * t, z=0.0, lane_z=3.0)
    img = UW.render(t, cam)
    UW.particles(img, t, cam)
    zs = 2.95 - 0.10 * t
    sx, sy, sc = swimmer_at(img, t, cam, cam["x"] - 0.06, 0.62, zs, angle=0.02)
    # red target ring on the swimmer (hook)
    if 0.15 < t < 2.4:
        hx, hy = head_screen(sx, sy, sc, 0.02)
        k = ease_out_cubic((t - 0.15) / 0.45)
        fade = 1 - lin(2.0, 2.4, t)
        lay = np.zeros((H, W), np.uint8)
        rad = int(95 + 10 * math.sin(t * 6))
        cv2.ellipse(lay, (int(hx * 4), int(hy * 4)), (rad * 4, rad * 4), -90, 0, 360 * k, 255, 9, cv2.LINE_AA, 2)
        a = lay.astype(np.float32) / 255.0 * fade
        g = cv2.GaussianBlur(a, (0, 0), 6)
        img += C(1.0, 0.2, 0.15) * g[..., None] * 0.6
        img[:] = img * (1 - a[..., None]) + C(1.0, 0.18, 0.15) * a[..., None]
    # danger pulse on "black out"
    p = math.exp(-((t - 1.75) ** 2) / 0.08) * 0.55
    if p > 0.01:
        d = np.sqrt(((PX - 540) / 620) ** 2 + ((PY - 960) / 1050) ** 2)
        img *= (1 - (smoothstep(0.5, 1.2, d) * p)[..., None] * C(0.1, 0.75, 0.75))
    return img


# --- S2/S3 lungs: 5.2 - 14.5 -------------------------------------------------
def breath_phase(t):
    """lung inflation -1..1 and its derivative sign"""
    if t < 10.0:
        f = 1.75  # hyperventilating
        a = 1.0
    else:
        f = 0.55
        a = 0.6
    return a * math.sin(2 * math.pi * f * t), math.cos(2 * math.pi * f * t)


O2_PATHS = np.random.default_rng(21).uniform([0, 0, 0, 0], [1, 1, 1, 6.28], size=(46, 4))


def scene_lungs(t):
    L = anatomy_layers()
    tl = t - 5.2
    zoom = 1.0 + 0.012 * tl
    img = L["bg_teal"].copy()
    BOKEH_TEAL.draw(img, t)
    img += L["holo"] * (0.92 + 0.08 * math.sin(t * 9.0))
    b, db = breath_phase(t)
    s = 1.0 + 0.075 * b
    x0, y0 = L["lung_box"]
    cH, aH = L["heart"]
    blit(img, cH, aH * 0.85, x0, y0)
    warp_rgba_into(img, L["lungs"], x0, y0, s, 540, 760)
    tr = L["trachea"]
    blit(img, tr[..., :3], tr[..., 3], x0, y0)
    # air flow in the trachea
    for i in range(14):
        ph = (i / 14 + t * (1.6 if t < 10 else 0.6)) % 1.0
        yy = 470 + ph * 300 if db > 0 else 770 - ph * 300
        xx = 540 + 7 * math.sin(i * 2.1 + t * 3)
        glow_dot(img, xx, yy, 7, C(0.8, 0.95, 1.0) * 0.55)
    # breath "speed" chevrons at the mouth during hyperventilation
    if t < 10.0:
        k = (t * 1.75) % 1.0
        for j in range(3):
            yy = 395 - 30 * j - (k * 40 if db < 0 else -k * 40)
            a = 0.45 * (1 - j / 3)
            cv2.ellipse(img, (540, int(yy)), (40 - j * 6, 14), 0, 200, 340, (0.7 * a, 0.95 * a, 1.0 * a), 5, cv2.LINE_AA)
        lb = label("x4  BREATHING SPEED", 38, fg=(255, 220, 90), border=(255, 210, 60))
        sc_, op = pop(t, 5.7)
        blit_rgba(img, lb, 540, 175, sc_, op * (1 - lin(9.8, 10.2, t)))
    # O2 molecules flowing in (what he thinks)
    if t > 10.0:
        for i, (a1, a2, a3, ang) in enumerate(O2_PATHS):
            t0 = 10.0 + a1 * 3.4
            k = (t - t0) / 1.1
            if k < 0:
                continue
            k = min(k, 1.0)
            side = -1 if a2 < 0.5 else 1
            tx = 540 + side * (60 + a3 * 150)
            ty = 830 + (a2 % 0.5) * 2 * 320
            if k < 0.45:
                q = k / 0.45
                x = 540 + 6 * math.sin(i)
                y = 330 + q * 440
            else:
                q = ease_in_out((k - 0.45) / 0.55)
                x = 540 + (tx - 540) * q
                y = 770 + (ty - 770) * q
            x += 4 * math.sin(t * 3 + i)
            draw_o2(img, x, y, ang + t * 1.5, r=12, alpha=min(1.0, (t - t0) * 4))
        lb = label("O₂  OXYGEN", 44, fg=(120, 220, 255), border=(90, 200, 255))
        sc_, op = pop(t, 10.3)
        blit_rgba(img, lb, 540, 175, sc_, op)
        if t > 11.6:
            q = label("FILLING UP...?", 40, fg=(255, 255, 255))
            sc_, op = pop(t, 11.6)
            blit_rgba(img, q, 540, 262, sc_, op)
    return img


# --- S4/S5 blood vessel: 14.2 - 22.6 -------------------------------------
RBC = np.random.default_rng(4).uniform([0, -1, -1, 0, 0, 0], [1, 1, 1, 6.28, 1, 6.28], size=(30, 6))
CO2S = np.random.default_rng(9).uniform([0, -1, -1, 0, 0], [1, 1, 1, 6.28, 1], size=(34, 5))


def scene_vessel(t):
    L = anatomy_layers()
    tl = t - 14.2
    img = L["vessel_bg"].copy()
    yc, R = 900.0, 360.0
    sprites = L["rbc"]
    # cells sorted back-to-front by depth
    order = np.argsort(RBC[:, 2])
    flow = 230.0
    co2_out = sstep(18.6, 21.6, t)  # CO2 being flushed
    for idx in order:
        fx, fy, fz, rot, tilt, ph = RBC[idx]
        depth = 0.78 + 0.32 * (fz + 1) / 2
        x = (fx * (W + 400) + flow * depth * tl) % (W + 400) - 200
        y = yc + fy * (R - 110) * 0.9 + 18 * math.sin(t * 0.8 + ph)
        k = int(min(9, max(0, (0.5 + 0.5 * math.sin(t * 0.5 + ph * 3)) * 9 * tilt)))
        spr = sprites[k]
        ang = math.degrees(rot + t * 0.25 * (1 if ph > 3 else -1))
        sc = 0.62 * depth
        hh, ww = spr.shape[:2]
        M = cv2.getRotationMatrix2D((ww / 2, hh / 2), ang, sc)
        size = int(max(hh, ww) * sc) + 4
        M[0, 2] += size / 2 - ww / 2
        M[1, 2] += size / 2 - hh / 2
        out = cv2.warpAffine(spr, M, (size, size), flags=cv2.INTER_LINEAR)
        dim = 0.55 + 0.45 * (fz + 1) / 2
        blit(img, out[..., :3] * dim, out[..., 3], int(x - size / 2), int(y - size / 2))
        # O2 loaded on each cell (saturated)
        rr = 0.62 * 90 * sc * 0.55
        for j in range(4):
            a = rot + t * 0.25 + j * 1.5708 + 0.4
            draw_o2(img, x + rr * math.cos(a), y + rr * math.sin(a) * 0.7, a, r=int(7 * depth + 1), alpha=0.95 * dim)
    # CO2 molecules: in plasma, then flushed out through the top wall
    for i, (fx, fy, fz, ang, sp) in enumerate(CO2S):
        x = (fx * (W + 300) + 150 * tl) % (W + 300) - 150
        y = yc + fy * (R - 60) * 0.85 + 14 * math.sin(t + i)
        leave = clamp01((co2_out * 1.6 - (i / len(CO2S)) * 0.6))
        if leave > 0:
            y = y - leave * (y - (yc - R - 260 - sp * 300))
        alpha = 1.0 - lin(0.85, 1.0, leave)
        if alpha > 0.02:
            draw_co2(img, x, y, ang + t * 1.2, r=11, alpha=alpha)
    fw = L["vessel_front"]
    blit(img, fw[..., :3], fw[..., 3], 0, 0, mode="add")
    # HUD
    if t < 18.7:
        val = 0.97 + 0.01 * sstep(15.6, 17.6, t)
        pct = int(round(val * 100))
        hud = hud_panel([dict(label="O₂", value=val, color=(70, 200, 255), text=f"{pct}%")], title="BLOOD OXYGEN")
        sc_, op = pop(t, 14.55)
        blit_rgba(img, hud, 540, 210, sc_, op * (1 - lin(18.4, 18.7, t)))
        if t > 16.6:
            lb = label("BARELY CHANGES", 46, fg=(255, 220, 90), border=(255, 210, 60))
            sc_, op = pop(t, 16.6)
            blit_rgba(img, lb, 540, 395, sc_, op * (1 - lin(18.4, 18.7, t)))
    else:
        val = 0.95 - 0.58 * co2_out
        hud = hud_panel([dict(label="CO₂", value=val, color=(255, 165, 50), text=f"{int(val*100)}%")], title="CARBON DIOXIDE IN BLOOD")
        sc_, op = pop(t, 18.75)
        blit_rgba(img, hud, 540, 210, sc_, op)
        if t > 19.7:
            lb = label("FLUSHED OUT", 46, fg=(255, 180, 80), border=(255, 160, 60))
            sc_, op = pop(t, 19.7)
            blit_rgba(img, lb, 540, 395, sc_, op)
    return img


# --- S6 brain: 22.3 - 30.6 -------------------------------------------------
def wire(img, pts, col, width, alpha, pulse=None, pulse_col=None):
    lay = np.zeros((H, W), np.uint8)
    p = np.array(pts, np.int32).reshape(-1, 1, 2)
    cv2.polylines(lay, [p * 4], False, 255, width * 4, cv2.LINE_AA, 2)
    a = lay.astype(np.float32) / 255.0 * alpha
    g = cv2.GaussianBlur(a, (0, 0), 7)
    img += C(*col) * g[..., None] * 0.6
    img[:] = img * (1 - a[..., None]) + C(*col) * a[..., None]
    if pulse is not None:
        # glowing packets travelling along the path
        seg = np.array(pts, np.float32)
        dists = np.r_[0, np.cumsum(np.linalg.norm(np.diff(seg, axis=0), axis=1))]
        total = dists[-1]
        for k in pulse:
            dd = (k % 1.0) * total
            j = min(np.searchsorted(dists, dd) - 1, len(seg) - 2)
            j = max(j, 0)
            u = (dd - dists[j]) / max(dists[j + 1] - dists[j], 1e-6)
            x, y = seg[j] + (seg[j + 1] - seg[j]) * u
            glow_dot(img, x, y, 16, C(*pulse_col) * 1.2)
            glow_dot(img, x, y, 6, C(1, 1, 1) * 0.9)


def curve(p0, p1, p2, n=40):
    out = []
    for i in range(n + 1):
        u = i / n
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
        y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
        out.append((x, y))
    return out


def scene_brain(t):
    L = anatomy_layers()
    tl = t - 22.3
    img = L["bg_navy"].copy()
    BOKEH_TEAL.draw(img, t, 0.07)
    bx0, by0 = L["brain_box"]
    s = 1.0 + 0.008 * math.sin(t * 1.3) + 0.01 * tl / 8
    warp_rgba_into(img, L["brain"], bx0, by0, s, 540, 800)
    node = (548, 1112)
    alarm = sstep(28.6, 29.2, t)
    # O2 wire from the left, CO2 wire from the right
    o2_pts = curve((-20, 1230), (300, 1235), (node[0] - 24, node[1] + 8))
    co2_pts = curve((1100, 1230), (800, 1235), (node[0] + 24, node[1] + 8))
    o2_on = sstep(24.2, 24.6, t)
    o2_pulse = [((t - 24.2) * 0.9 + i / 3) for i in range(3)] if 24.2 < t < 27.0 else None
    wire(img, o2_pts, (0.25, 0.75, 1.0), 6, 0.35 + 0.65 * o2_on * (1 - 0.6 * sstep(26.3, 26.8, t)), o2_pulse, (0.3, 0.8, 1.0))
    co2_on = sstep(27.5, 27.9, t)
    co2_pulse = [((t - 27.5) * 1.1 + i / 4) for i in range(4)] if t > 27.5 else None
    wire(img, co2_pts, (1.0, 0.62, 0.16), 6, 0.35 + 0.65 * co2_on, co2_pulse, (1.0, 0.7, 0.2))
    # node
    base = C(0.2, 0.9, 0.8) * (1 - alarm) + C(1.0, 0.15, 0.12) * alarm
    flick = 1.0 if alarm < 0.5 else (0.65 + 0.35 * (math.sin(t * 22) > 0))
    glow_dot(img, node[0], node[1], 60, base * 0.7 * flick)
    glow_dot(img, node[0], node[1], 22, base * 1.6 * flick)
    glow_dot(img, node[0], node[1], 9, C(1, 1, 1))
    if alarm > 0:
        for k in range(3):
            ph = ((t - 28.6) * 1.4 + k / 3) % 1.0
            rr = 30 + ph * 230
            lay = np.zeros((H, W), np.uint8)
            cv2.circle(lay, (node[0] * 4, node[1] * 4), int(rr * 4), 255, 6 * 4, cv2.LINE_AA, 2)
            a = lay.astype(np.float32) / 255.0 * (1 - ph) * 0.8 * alarm
            img += C(1.0, 0.25, 0.2) * a[..., None]
    # labels
    lb = label("BREATHING ALARM", 36, fg=(255, 255, 255), border=(120, 220, 210) if alarm < 0.5 else (255, 80, 70))
    sc_, op = pop(t, 22.7)
    blit_rgba(img, lb, 780, 1060, sc_, op)
    if t > 24.2:
        lb = label("LOW O₂", 38, fg=(120, 220, 255), border=(90, 200, 255))
        sc_, op = pop(t, 24.3)
        blit_rgba(img, lb, 175, 1175, sc_, op)
        red_x(img, 175, 1175, 52, t, 26.3)
    if t > 27.5:
        lb = label("HIGH CO₂", 38, fg=(255, 190, 90), border=(255, 160, 60))
        sc_, op = pop(t, 27.55)
        blit_rgba(img, lb, 905, 1175, sc_, op)
    if t > 29.25:
        lb = label("BREATHE!", 64, fg=(255, 255, 255), bg=(200, 30, 30), border=(255, 140, 120))
        sc_, op = pop(t, 29.3, 0.22)
        blit_rgba(img, lb, 548, 300, sc_ * (1 + 0.04 * math.sin(t * 20)), op)
    # CO2 meter top-left rising during 27.5-29.3
    if t > 27.45:
        v = 0.25 + 0.6 * sstep(27.6, 29.1, t)
        hud = hud_panel([dict(label="CO₂", value=v, color=(255, 165, 50), text=f"{int(v*100)}%", marker=0.8)], width=900)
        sc_, op = pop(t, 27.5)
        blit_rgba(img, hud, 540, 455 if t < 29.25 else 455, sc_, op * (1 - lin(29.2, 29.4, t) * 0.0))
    return img


# --- S7 swim with HUD: 30.25 - 37.8 ----------------------------------------
def scene_swim_hud(t):
    v = 1.0
    cam = dict(yh=780, hc=1.15, hs=0.85, x=v * t, z=0.0, lane_z=2.75)
    img = UW.render(t, cam)
    UW.particles(img, t, cam)
    swimmer_at(img, t, cam, cam["x"] - 0.05, 0.6, 2.7, angle=0.02)
    o2 = 0.97 - 0.70 * sstep(31.0, 37.2, t)
    co2 = 0.12 + 0.28 * sstep(31.0, 37.4, t)
    oc = (70, 200, 255) if o2 > 0.6 else ((255, 210, 60) if o2 > 0.4 else (255, 70, 60))
    hud = hud_panel([dict(label="O₂", value=o2, color=oc, text=f"{int(o2*100)}%"),
                     dict(label="CO₂", value=co2, color=(255, 165, 50), text=f"{int(co2*100)}%", marker=0.8,
                          marker_text="ALARM")],
                    alarm=dict(on=0.0, muted=t > 36.4, text="SILENT" if t > 36.4 else "OFF"))
    sc_, op = pop(t, 30.45)
    blit_rgba(img, hud, 540, 300, sc_, op)
    return img


# --- S8 close-up + blackout: 37.55 - 44.6 -----------------------------------
def scene_close(t):
    v = 1.0
    cam = dict(yh=700, hc=1.2, hs=0.8, x=v * t, z=0.0, lane_z=2.2)
    img = UW.render(t, cam)
    UW.particles(img, t, cam)
    drain = sstep(40.0, 44.2, t)
    floor_shadow(img, cam, cam["x"] - 0.62, 0.66, 1.75)
    sx, sy, s = UW.project(cam["x"] - 0.62, 0.66, 1.75, cam)
    fog = UW.fog_at_y(sy)
    SWIM.render(img, t, sx, sy, s * 0.01, angle=0.03 + 0.05 * sstep(43.6, 44.5, t), dist=1.75, fog=fog,
                kick=1 - sstep(43.4, 44.3, t), limp=0.3 * sstep(43.6, 44.5, t), desat=0.4 * drain)
    return img


# --- S9/S10 limp sink + title: 44.6 - 54.6 ----------------------------------
SINK_BUB = Bubbles(seed=17)


def scene_sink(t):
    X9 = 45.0
    cam = dict(yh=640, hc=1.15, hs=0.9, x=X9, z=0.0, lane_z=3.3, rays=0.7)
    pz = 3.3 - 0.35 * sstep(48.4, 54.5, t)
    img = UW.render(t, cam)
    UW.particles(img, t, cam, 0.8)
    k = sstep(44.6, 51.5, t)
    wx = X9 - 0.25 + 0.38 * (1 - (1 - min(max((t - 44.6) / 6.0, 0), 1)) ** 2)
    wy = 0.62 - 0.38 * k
    ang = 0.05 + 0.2 * sstep(44.6, 48.0, t) - 0.18 * sstep(48.5, 51.8, t)
    limp = sstep(44.6, 46.0, t)
    floor_shadow(img, cam, wx, wy, pz, 1.2)
    sx, sy, s = UW.project(wx, wy, pz, cam)
    fog = UW.fog_at_y(sy)
    SWIM.render(img, t, sx, sy, s * 0.01, angle=ang, dist=pz, fog=fog, kick=0.0, limp=limp, desat=0.25, bright=0.9)
    if not SINK_BUB.items:
        pass
    # a few last bubbles escape from the mouth
    mx, my = SWIM.mouth_screen
    for (t0, n) in ((44.95, 6), (46.2, 3)):
        if t0 <= t < t0 + 4.0:
            rng = np.random.default_rng(int(t0 * 10))
            for j in range(n):
                tj = t0 + rng.uniform(0, 0.45)
                age = t - tj
                if age < 0:
                    continue
                r = rng.uniform(5, 13)
                y = my - 170 * age * (0.6 + r / 25)
                x = mx + rng.uniform(-10, 10) + 9 * math.sin(age * 6 + j)
                blit_rgba(img, bubble_sprite(r), x, y, 1.0, min(1, age * 6) * (1 - lin(3.0, 4.0, age)), mode="add")
    # title
    if t > 49.4:
        words = [("SHALLOW", 49.55), ("WATER", 49.95), ("BLACKOUT", 50.38)]
        for i, (w_, t0) in enumerate(words):
            if t < t0:
                continue
            k = (t - t0) / 0.22
            sc_ = 1.0 + 0.9 * (1 - ease_out_cubic(k))
            op = min(1.0, k * 3)
            col = (255, 214, 10) if w_ == "BLACKOUT" else (255, 255, 255)
            tr = title_word(w_, col)
            blit_rgba(img, tr, 540, 290 + i * 165, sc_, op)
            if k < 1.0:
                img += C(1, 1, 1) * (0.10 * (1 - k))
    return img


@functools.lru_cache(maxsize=8)
def title_word(w_, col):
    return text_rgba(w_, size=170, fill=col, stroke=12, path=FONT_BLACK, glow=(255, 180, 0) if col[2] < 100 else (80, 200, 255))


# --- S11 rules: 54.3 - 61.45 -------------------------------------------------
def scene_rules(t):
    v = 0.95
    cam = dict(yh=820, hc=1.15, hs=0.85, x=v * t, z=0.0, lane_z=3.4, rays=1.1)
    img = UW.render(t, cam)
    UW.particles(img, t, cam)
    # buddy higher & further, main swimmer near
    floor_shadow(img, cam, cam["x"] + 0.35, 1.45, 4.6)
    bx, by, bs = UW.project(cam["x"] + 0.35, 1.45, 4.6, cam)
    BUDDY.render(img, t + 0.37, bx, by, bs * 0.01, angle=-0.02, dist=4.6, fog=UW.fog_at_y(by))
    swimmer_at(img, t, cam, cam["x"] - 0.1, 0.62, 3.0, angle=0.0)
    c1, c2 = rule_cards()
    sc_, op = pop(t, 54.55, 0.3)
    blit_rgba(img, c1, 540, 330, sc_, op)
    sc_, op = pop(t, 57.85, 0.3)
    blit_rgba(img, c2, 540, 545, sc_, op)
    return img


# ==========================================================================
# timeline
# ==========================================================================
# (start, end, fn, transition_in_duration, zoom_through)
SEGMENTS = [
    (0.0, 5.42, scene_hook, 0.0, False),
    (5.22, 14.55, scene_lungs, 0.20, True),
    (14.25, 22.62, scene_vessel, 0.30, True),
    (22.32, 30.55, scene_brain, 0.28, False),
    (30.27, 37.82, scene_swim_hud, 0.26, False),
    (37.55, 44.62, scene_close, 0.25, False),
    (44.62, 54.6, scene_sink, 0.0, False),
    (54.3, 61.45, scene_rules, 0.30, False),
]


def scene_frame(t):
    act = [s for s in SEGMENTS if s[0] <= t < s[1]]
    if not act:
        act = [SEGMENTS[-1]]
    if len(act) == 1:
        img = act[0][2](t)
    else:
        a, b = act[0], act[1]
        dur = b[3]
        k = ease_in_out((t - b[0]) / max(dur, 1e-6))
        ia = a[2](t)
        ib = b[2](t)
        if b[4]:
            z = 1.0 + 0.25 * k
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
            ia = cv2.warpAffine(ia, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            z2 = 0.85 + 0.15 * k
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 / z2)
            ib = cv2.warpAffine(ib, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        img = ia * (1 - k) + ib * k
    return img


# ==========================================================================
# captions
# ==========================================================================
HL = {
    "cyan": (90, 215, 255),
    "amber": (255, 175, 50),
    "red": (255, 70, 60),
    "yellow": (255, 220, 40),
    "green": (110, 255, 140),
}
PHRASES = [
    (["black", "out"], "red"), (["no", "idea"], "yellow"), (["really", "fast"], "yellow"),
    (["oxygen"], "cyan"), (["carbon", "dioxide"], "amber"), (["rising"], "amber"),
    (["never", "goes", "off"], "red"), (["completely", "fine"], "green"), (["shuts", "down"], "red"),
    (["strongest", "swimmers"], "yellow"), (["problem"], "red"), (["without", "any", "warning"], "red"),
]
NO_CAPTION = [(49.4, 51.15), (54.3, 61.6)]


def clean(w):
    return w.replace("...", "").replace(",", "").replace(".", "").replace("…", "")


def build_chunks():
    ws = [dict(t=clean(w["text"]).upper(), raw=w["text"], s=w["start"], e=w["end"]) for w in WORDS if w["type"] == "word"]
    low = [clean(w["text"]).lower() for w in WORDS if w["type"] == "word"]
    cols = [None] * len(ws)
    for ph, cname in PHRASES:
        n = len(ph)
        for i in range(len(low) - n + 1):
            if low[i:i + n] == ph:
                for j in range(n):
                    cols[i + j] = HL[cname]
    pid = [None] * len(ws)
    plen = {}
    k = 0
    for ph, cname in PHRASES:
        n = len(ph)
        for i in range(len(low) - n + 1):
            if low[i:i + n] == ph:
                for j in range(n):
                    pid[i + j] = k
                plen[k] = (n, len(" ".join(ph)))
                k += 1
    chunks = []
    cur = []
    MAXC = 16
    for i, w in enumerate(ws):
        cur.append(i)
        txt = " ".join(ws[j]["t"] for j in cur)
        end_punct = any(p in w["raw"] for p in [".", ",", "..."])
        last = i + 1 >= len(ws)
        nxt_gap = (ws[i + 1]["s"] - w["e"]) if not last else 9
        brk = end_punct or nxt_gap > 0.3 or last or len(cur) >= 4
        if not brk:
            nt = ws[i + 1]["t"]
            same_phrase = pid[i] is not None and pid[i] == pid[i + 1]
            if same_phrase:
                brk = len(txt) + 1 + len(nt) > 24
            else:
                brk = len(txt) + 1 + len(nt) > MAXC
                p2 = pid[i + 1]
                if not brk and p2 is not None and plen[p2][0] > 1:
                    brk = len(txt) + 1 + plen[p2][1] > MAXC
        if brk:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    # merge tiny orphan chunks (e.g. a lone "THE") into the next/previous chunk
    merged = []
    i = 0
    while i < len(chunks):
        c = chunks[i]
        single = len(c) == 1 and len(ws[c[0]]["t"]) <= 4 and not any(p in ws[c[0]]["raw"] for p in [".", ","])
        if single and i + 1 < len(chunks):
            comb = c + chunks[i + 1]
            if len(" ".join(ws[j]["t"] for j in comb)) <= 24:
                merged.append(comb)
                i += 2
                continue
        merged.append(c)
        i += 1
    chunks = merged
    out = []
    for ci, c in enumerate(chunks):
        s = ws[c[0]]["s"] - 0.04
        e_last = ws[c[-1]]["e"]
        nxt = ws[chunks[ci + 1][0]]["s"] - 0.04 if ci + 1 < len(chunks) else e_last + 0.5
        e = nxt if nxt - e_last < 0.7 else e_last + 0.35
        text = " ".join(ws[j]["t"] for j in c)
        colors = [cols[j] if cols[j] else (255, 255, 255) for j in c]
        out.append(dict(s=s, e=e, text=text, colors=tuple(colors), idx=tuple(c)))
    return out, ws


CHUNKS, WLIST = build_chunks()
CAP_Y = 1395


@functools.lru_cache(maxsize=256)
def caption_img(text, colors):
    rgba = text_rgba(text, size=88, stroke=10, colors=list(colors))
    if rgba.shape[1] > 1000:
        f = 1000 / rgba.shape[1]
        rgba = cv2.resize(rgba, (int(rgba.shape[1] * f), int(rgba.shape[0] * f)), interpolation=cv2.INTER_AREA)
    return rgba


def draw_captions(img, t):
    for a, b in NO_CAPTION:
        if a <= t < b:
            return
    for c in CHUNKS:
        if c["s"] <= t < c["e"]:
            k = (t - c["s"]) / 0.13
            sc = 0.80 + 0.20 * ease_out_back(k, 2.0)
            op = min(1.0, k * 2.0 + 0.2)
            blit_rgba(img, caption_img(c["text"], c["colors"]), 540, CAP_Y, sc, op)
            return


# ==========================================================================
# full frame
# ==========================================================================
def frame(t):
    img = scene_frame(t)
    # grading per section
    desat = 0.0
    tunnel = 0.0
    expo = 1.0
    if 40.0 < t < 44.62:
        desat = 0.55 * sstep(40.0, 44.0, t)
        tunnel = 0.92 * sstep(42.2, 44.4, t) + 0.08 * sstep(44.3, 44.5, t)
        expo = 1.0 - 0.25 * sstep(42.5, 44.4, t)
        # heartbeat pulse brightness flicker
        hb = math.exp(-((((t - 40.2) % 1.05)) ** 2) / 0.004)
        expo *= 1 - 0.06 * hb
        if t > 43.7:
            k = (t - 43.7) / 0.8
            jitter = (math.sin(t * 90) > 0.2) * 0.25 * (1 - k)
            expo *= max(0.0, 1 - k) + jitter * 0.3
    if 44.62 <= t < 54.6:
        desat = 0.30
        expo = 0.88 * sstep(44.62, 45.4, t) if t < 45.4 else 0.88
    if 42.2 < t < 44.6:
        # vision blur
        b = sstep(42.6, 44.3, t)
        if b > 0.02:
            small = cv2.resize(img, (W // 6, H // 6), interpolation=cv2.INTER_AREA)
            bl = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
            img = img * (1 - b * 0.8) + bl * b * 0.8
    img = post(img, t, bloom=0.32, grain=0.016, vig=1.0, tunnel=tunnel, desat=desat, exposure=expo)
    if t > DUR - 0.25:
        img *= max(0.0, (DUR - t) / 0.25) * 0.3 + 0.7
    draw_captions(img, t)
    return tonemap(img)


# ==========================================================================
# render
# ==========================================================================
def render_segment(args):
    f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                          "-pix_fmt", "yuv420p", "-threads", "2", path], stdin=subprocess.PIPE)
    for i in range(f0, f1):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    p.wait()
    return path


def main_render(workers=4):
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    seg_dir = os.path.join(OUT, "segments")
    os.makedirs(seg_dir, exist_ok=True)
    n = int(round(DUR * FPS))
    nseg = 24
    bounds = np.linspace(0, n, nseg + 1).astype(int)
    jobs = [(int(bounds[i]), int(bounds[i + 1]), os.path.join(seg_dir, f"seg_{i:03d}.mp4")) for i in range(nseg)]
    t0 = time.time()
    with Pool(workers) as pool:
        for k, pth in enumerate(pool.imap_unordered(render_segment, jobs)):
            print(f"[{time.time()-t0:6.0f}s] done {k+1}/{nseg} {os.path.basename(pth)}", flush=True)
    lst = os.path.join(seg_dir, "list.txt")
    with open(lst, "w") as fh:
        for j in jobs:
            fh.write(f"file '{j[2]}'\n")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                           os.path.join(OUT, "video_noaudio.mp4")])
    print("total", time.time() - t0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if cmd == "preview":
        outdir = sys.argv[2]
        times = [float(x) for x in sys.argv[3:]]
        for tt in times:
            t0 = time.time()
            im = frame(tt)
            cv2.imwrite(os.path.join(outdir, f"f_{tt:05.2f}.jpg"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
            print(f"t={tt:.2f} {time.time()-t0:.2f}s", flush=True)
    elif cmd == "render":
        main_render(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
