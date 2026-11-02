"""
Sound design + mix for Ep01.
  * voiceover (ElevenLabs, Viraj - Dramatic TV Narration)
  * ElevenLabs SFX: underwater ambience, hyperventilation, whooshes, heartbeat, power-down
  * synthesized score (D minor suspense): drone, pads, curiosity plucks, pulse, risers, impacts
  * synthesized accents: alarm beeps, bubbles, UI pops, error buzz
  * sidechain ducking of music under VO, soft limiting, 2-pass loudnorm to -14 LUFS / -1 dBTP
output: ../out/mix.wav
"""
import os
import json
import subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
OUT = os.path.join(ROOT, "out")
SR = 48000
DUR = 61.45
N = int(DUR * SR) + SR
rng = np.random.default_rng(42)


def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(A, name), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def db(x):
    return 10 ** (x / 20)


def rms(x):
    return float(np.sqrt(np.mean(x ** 2) + 1e-12))


def norm_peak(x, p=0.9):
    return x * (p / (np.max(np.abs(x)) + 1e-9))


def fades(x, fi=0.01, fo=0.05):
    x = x.copy()
    a = int(fi * SR)
    b = int(fo * SR)
    if a > 0:
        x[:a] *= np.linspace(0, 1, a)[:, None]
    if b > 0 and b < len(x):
        x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


def place(buf, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(clip))
    buf[i:j] += clip[:j - i] * gain


def lp(x, fc, order=2):
    sos = butter(order, fc, "low", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def hp(x, fc, order=2):
    sos = butter(order, fc, "high", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def bp(x, f1, f2, order=2):
    sos = butter(order, [f1, f2], "band", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def stereo(m, width=0.0):
    if m.ndim == 2:
        return m
    return np.stack([m, m], 1)


def resample_speed(x, speed):
    n = int(len(x) / speed)
    idx = np.linspace(0, len(x) - 1, n)
    return np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in range(2)], 1).astype(np.float32)


_ir = None


def reverb(x, wet=0.3, length=2.4, damp=2.8):
    global _ir
    if _ir is None:
        n = int(length * SR)
        t = np.arange(n) / SR
        e = np.exp(-t * damp)
        irL = rng.standard_normal(n) * e
        irR = rng.standard_normal(n) * e
        irL = lp(irL[:, None], 6000)[:, 0]
        irR = lp(irR[:, None], 6000)[:, 0]
        irL[: int(0.012 * SR)] = 0
        irR[: int(0.017 * SR)] = 0
        _ir = np.stack([irL, irR], 1) / np.sqrt(np.sum(irL ** 2))
    y = np.stack([fftconvolve(x[:, c], _ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet * 0.6


# --------------------------------------------------------------------------
# synth primitives
# --------------------------------------------------------------------------
def note_freq(n):
    names = {"C": -9, "C#": -8, "Db": -8, "D": -7, "D#": -6, "Eb": -6, "E": -5, "F": -4, "F#": -3, "Gb": -3, "G": -2,
             "G#": -1, "Ab": -1, "A": 0, "A#": 1, "Bb": 1, "B": 2}
    name, octv = n[:-1], int(n[-1])
    return 440.0 * 2 ** ((names[name] + (octv - 4) * 12) / 12)


def saw_tone(freq, dur, harm=10, roll=1.7, detune=0.0025, voices=3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for v in range(voices):
        f = freq * (1 + detune * (v - (voices - 1) / 2))
        ph = rng.uniform(0, 2 * np.pi, harm)
        for k in range(1, harm + 1):
            if f * k > 9000:
                break
            out += np.sin(2 * np.pi * f * k * t + ph[k - 1]) / k ** roll
    return out / voices


def pad(notes, dur, attack=1.5, release=1.5, bright=1.7, lfo=0.13):
    n = int(dur * SR)
    t = np.arange(n) / SR
    m = np.zeros(n)
    for nt in notes:
        m += saw_tone(note_freq(nt), dur, harm=9, roll=bright)
    env = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release)
    env = np.clip(env, 0, 1) * (0.85 + 0.15 * np.sin(2 * np.pi * lfo * t))
    m = m * env / max(len(notes), 1)
    L = m * (1 + 0.06 * np.sin(2 * np.pi * 0.21 * t))
    R = m * (1 - 0.06 * np.sin(2 * np.pi * 0.21 * t))
    return np.stack([L, R], 1)


def pluck(freq, dur=0.9, decay=5.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 9)
         + 0.15 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 14))
    s *= np.exp(-t * decay) * np.minimum(1, t / 0.004)
    return stereo(s)


def sub_boom(dur=1.6, f0=72, f1=34, amp=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 2.6) * np.minimum(1, t / 0.003)
    click = rng.standard_normal(n) * np.exp(-t * 60) * 0.25
    click = lp(click[:, None], 2500)[:, 0]
    return stereo((s + click) * amp)


def riser(dur=2.0, f0=300, f1=4000):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    seg = int(0.05 * SR)
    for i in range(0, n, seg):
        u = i / n
        fc = f0 * (f1 / f0) ** u
        chunk = noise[max(0, i - 2048): i + seg]
        y = bp(chunk[:, None], fc * 0.7, min(fc * 1.4, 20000))[:, 0]
        out[i:i + seg] = y[-min(seg, n - i):]
    tone = np.sin(2 * np.pi * np.cumsum(220 * (2 ** (t / dur * 1.5))) / SR) * 0.25
    env = (t / dur) ** 2.2
    return stereo((out * 0.8 + tone) * env)


def beep(freq, dur=0.16):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * freq * t)) * 0.35 + np.sin(2 * np.pi * freq * t) * 0.65
    s *= np.minimum(1, t / 0.005) * np.minimum(1, (dur - t) / 0.02)
    return stereo(lp(s[:, None], 3500)[:, 0])


def bloop(f=420, dur=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    fr = f * (1 + 2.2 * t / dur)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 28) * np.minimum(1, t / 0.002)
    return stereo(s)


def ui_pop(f=1400):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t * (1 - 0.3 * t / 0.09)) * np.exp(-t * 45)
    s += rng.standard_normal(n) * np.exp(-t * 120) * 0.15
    return stereo(s)


def buzz(dur=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 116 * t)) * 0.5
    s *= np.minimum(1, t / 0.005) * np.minimum(1, (dur - t) / 0.04)
    return stereo(lp(s[:, None], 1800)[:, 0])


def env_curve(points):
    """piecewise linear gain automation from [(t, g), ...]"""
    t = np.arange(N) / SR
    ts = [p[0] for p in points]
    gs = [p[1] for p in points]
    return np.interp(t, ts, gs)[:, None]


# --------------------------------------------------------------------------
def build():
    vo = load("voiceover.mp3")
    vo = hp(vo, 70)
    VO = np.zeros((N, 2))
    place(VO, vo, 0.0)
    vo_rms = rms(vo)

    # ------------------------------------------------------------- score
    MUS = np.zeros((N, 2))
    # drone D2 + A2 across the whole piece
    dr = pad(["D2", "A2", "D3"], DUR + 0.5, attack=0.4, release=2.0, bright=2.1, lfo=0.09)
    place(MUS, dr, 0.0, 1.0)
    # minor 7 pad in the explainer section
    place(MUS, pad(["D3", "F3", "A3", "C4"], 25.6, attack=2.0, release=1.5, bright=2.0), 5.0, 0.55)
    # tense cluster on the brain / alarm build
    place(MUS, pad(["D4", "Eb4", "A4"], 8.4, attack=3.0, release=0.6, bright=2.2), 22.0, 0.25)
    # sad pad after blackout
    place(MUS, pad(["D3", "A3", "E4", "F4"], 10.2, attack=2.5, release=2.5, bright=2.2), 44.7, 0.6)
    # resolution at the end: Bbmaj7 -> F
    place(MUS, pad(["Bb2", "D3", "F3", "A3"], 4.2, attack=1.0, release=1.2, bright=2.0), 54.2, 0.6)
    place(MUS, pad(["F2", "C3", "F3", "A3", "C4"], 4.0, attack=1.2, release=1.6, bright=2.0), 57.6, 0.6)

    # curiosity plucks, 92 bpm 8ths over Dm - Bb - F - C (5.2 - 30.0)
    eighth = 60 / 92 / 2
    chords = [["D4", "F4", "A4", "C5"], ["Bb3", "D4", "F4", "A4"], ["F4", "A4", "C5", "E5"], ["C4", "E4", "G4", "Bb4"]]
    pat = [0, 2, 1, 3, 2, 1, 3, 2]
    PL = np.zeros((N, 2))
    t = 5.25
    k = 0
    while t < 29.9:
        ch = chords[(k // 16) % 4]
        nt = ch[pat[k % 8]]
        vel = 0.55 + 0.45 * (k % 2 == 0)
        place(PL, pluck(note_freq(nt), 0.8, 6.5), t, vel)
        if k % 8 == 0:
            place(PL, pluck(note_freq(ch[0]) / 2, 1.2, 3.0), t, 0.7)
        t += eighth
        k += 1
    PL = reverb(lp(PL, 4200), wet=0.35)
    MUS += PL * 0.5

    # heartbeat-like pulse 30.3 - 40.0 (low double thump, 76 bpm)
    t = 30.4
    while t < 40.0:
        place(MUS, sub_boom(0.5, 70, 45, 0.30), t)
        place(MUS, sub_boom(0.45, 65, 42, 0.18), t + 0.22)
        t += 60 / 76
    # risers + impacts
    place(MUS, riser(2.3, 250, 5000), 27.0, 0.3)
    place(MUS, riser(1.6, 200, 3000), 47.95, 0.35)
    place(MUS, sub_boom(2.2, 80, 30, 1.0), 0.0)
    for tt, a in ((49.55, 0.9), (49.95, 0.8), (50.38, 1.1)):
        place(MUS, sub_boom(1.8, 85, 32, a), tt)
    MUS = reverb(MUS, wet=0.22)

    # section automation for the score (silence at the blackout)
    mus_auto = env_curve([(0, 1.0), (5.0, 1.0), (5.4, 0.75), (22.3, 0.75), (29.3, 1.0), (30.3, 0.85), (40.0, 0.9),
                          (43.55, 1.0), (43.75, 0.0), (44.7, 0.0), (45.6, 0.8), (54.2, 0.8), (54.6, 0.9), (60.6, 0.9), (61.45, 0.0), (62.5, 0.0)])
    MUS *= mus_auto
    # normalise music bed ~15 dB under the VO, then duck under speech
    MUS *= (vo_rms * db(-13.5)) / (rms(MUS[: int(DUR * SR)]) + 1e-9)
    venv = np.abs(VO).max(1)
    a_att = np.exp(-1 / (0.03 * SR))
    a_rel = np.exp(-1 / (0.35 * SR))
    e = np.zeros(N)
    acc = 0.0
    for i in range(0, N, 64):
        v = venv[i:i + 64].max()
        acc = a_att * acc + (1 - a_att) * v if v > acc else a_rel * acc + (1 - a_rel) * v
        e[i:i + 64] = acc
    e = np.clip(e / (np.percentile(e[e > 0], 95) + 1e-9), 0, 1)
    MUS *= (1 - 0.42 * e)[:, None]

    # ------------------------------------------------------------- SFX
    FX = np.zeros((N, 2))
    amb = load("sfx_underwater_amb.mp3")
    amb = amb * (db(-24) * vo_rms / rms(amb))
    # looped ambience with crossfades
    AMB = np.zeros((N, 2))
    L = len(amb)
    xf = int(1.0 * SR)
    pos = 0
    first = True
    while pos < N:
        seg = amb.copy()
        if not first:
            seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
        j = min(N, pos + L)
        AMB[pos:j] += seg[: j - pos]
        pos += L - xf
        first = False
    amb_auto = env_curve([(0, 1.0), (5.0, 1.0), (5.5, 0.0), (30.0, 0.0), (30.6, 1.0), (42.4, 1.0), (44.3, 0.7), (44.5, 0.0),
                          (44.8, 0.0), (45.8, 0.7), (54.1, 0.7), (54.5, 1.0), (61.0, 1.0), (61.45, 0.0), (62.5, 0.0)])
    AMB *= amb_auto
    # muffle during the blackout
    amb_lp = lp(AMB, 350, 4)
    mfx = env_curve([(0, 0), (41.8, 0), (44.2, 1), (44.6, 1), (44.8, 0), (62, 0)])
    AMB = AMB * (1 - mfx) + amb_lp * mfx * 1.4
    FX += AMB

    br = load("sfx_breathing.mp3")
    br = fades(br, 0.02, 0.15) * (db(-14) * vo_rms / rms(br))
    for tt in (5.35, 7.25, 9.05):
        place(FX, br if tt < 9 else fades(br[: int(1.0 * SR)], 0.01, 0.4), tt, 0.85)

    wh = load("sfx_whoosh.mp3")
    wh = fades(wh, 0.005, 0.1) * (db(-12) * vo_rms / rms(wh))
    for tt in (5.05, 14.1, 22.15, 30.1, 37.42, 54.15):
        place(FX, wh, tt, 0.9)

    hb = load("sfx_heartbeat.mp3")
    hb = fades(hb, 0.01, 0.2) * (db(-9) * vo_rms / rms(hb))
    place(FX, hb, 40.0, 0.8)
    place(FX, resample_speed(hb, 0.85), 41.95, 0.95)

    pdn = load("sfx_powerdown.mp3")
    pdn = fades(pdn, 0.005, 0.3) * (db(-7) * vo_rms / rms(pdn))
    place(FX, pdn, 43.62, 1.0)

    def lvl(clip, rel_db):
        return clip * (vo_rms * db(rel_db) / (rms(clip) + 1e-12))
    # alarm beeps on "BREATHE!"
    b1, b2 = lvl(beep(988, 0.15), -17), lvl(beep(740, 0.15), -17)
    for i in range(3):
        place(FX, b1, 29.3 + i * 0.32)
        place(FX, b2, 29.46 + i * 0.32)
    # error buzz on the red X
    place(FX, lvl(buzz(0.32), -19), 26.32)
    # UI pops
    for tt in (0.2, 5.7, 10.3, 11.6, 14.55, 16.6, 18.75, 19.7, 22.7, 24.3, 27.55, 30.45, 54.55, 57.85):
        place(FX, lvl(ui_pop(1500 if tt < 50 else 1100), -16), tt)
    # bubbles escaping
    for t0, n in ((44.95, 6), (46.2, 3)):
        for j in range(n):
            place(FX, lvl(bloop(rng.uniform(320, 620)), -15), t0 + rng.uniform(0, 0.45))

    # ------------------------------------------------------------- master
    mix = VO * 1.0 + MUS + FX
    mix = mix[: int(DUR * SR)]
    # gentle glue + soft clip
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.95
    mix = np.tanh(mix * 1.25) / np.tanh(1.25)
    os.makedirs(OUT, exist_ok=True)
    pre = os.path.join(OUT, "mix_pre.wav")
    import wave
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(pre, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    # 2-pass loudnorm to -14 LUFS, -1 dBTP
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = r.stderr[r.stderr.rfind("{"): r.stderr.rfind("}") + 1]
    m = json.loads(js)
    af = (f"loudnorm=I=-14:TP=-1.0:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    final = os.path.join(OUT, "mix.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", pre, "-af", af, "-ar", str(SR), final])
    print("measured:", m["input_i"], "LUFS ->", final)


if __name__ == "__main__":
    build()
