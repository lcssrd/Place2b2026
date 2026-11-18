# Bande-son de la vidéo : musique + effets, synthétisés sur une seule grille (120 BPM, do majeur).
import json, wave
import numpy as np

SR = 48000
DUR = 22.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def idx(t): return int(round(t * SR))

L = np.zeros(N); R = np.zeros(N)
def add(sig, t0, gain=1.0, pan=0.0, bus=None):
    """Ajoute un signal mono à t0 (s), pan -1..1 (loi à puissance constante)."""
    i0 = idx(t0)
    if i0 >= N: return
    sig = sig[: N - max(i0, 0)]
    if i0 < 0: sig = sig[-i0:]; i0 = 0
    a = (pan + 1) * np.pi / 4
    (bus or (L, R))[0][i0:i0 + len(sig)] += sig * gain * np.cos(a)
    (bus or (L, R))[1][i0:i0 + len(sig)] += sig * gain * np.sin(a)

def env(n, a=0.002, d=0.2, sus=0.0, curve=1.0):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) / d) * (1 - sus) + sus)
    return e ** curve

def lp1(x, fc):
    """Passe-bas 1 pôle (fc fixe ou tableau)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y

def lp(x, fc, order=2):
    for _ in range(order): x = lp1(x, fc)
    return x

def hp(x, fc): return x - lp1(x, fc)

def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    ph = (f * t + phase) % 1.0
    return 2 * ph - 1

def noise(n): return rng.standard_normal(n)

# ---------- Instruments ----------
def kick(gain=1.0):
    n = idx(0.42); t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.16)
    click = lp(noise(n), 3000, 1) * np.exp(-t / 0.004) * 0.25
    return np.tanh((body + click) * 1.6) * gain

def clap():
    n = idx(0.3); t = np.arange(n) / SR
    x = noise(n)
    x = hp(lp(x, 2600, 1), 900)
    e = np.zeros(n)
    for k, o in enumerate([0, 0.011, 0.022]):
        i = idx(o); e[i:] += np.exp(-(t[: n - i]) / (0.008 if k < 2 else 0.11))
    return x * e * 0.55

def hat(open_=False):
    n = idx(0.18 if open_ else 0.05); t = np.arange(n) / SR
    x = lp(hp(noise(n), 6500), 11000, 1)
    return x * np.exp(-t / (0.045 if open_ else 0.010)) * 0.32

def crash():
    n = idx(1.6); t = np.arange(n) / SR
    x = hp(noise(n), 4500)
    x = lp(x, 8500, 2)
    return x * np.exp(-t / 0.5) * 0.3

def bass_note(m, dur):
    n = idx(dur); t = np.arange(n) / SR
    f = mf(m)
    x = 0.6 * np.sin(2 * np.pi * f * t) + 0.4 * saw(f, n) * 0.5
    x = lp(x, 900, 1)
    return x * env(n, 0.004, dur * 0.6) * np.minimum(1, (n - np.arange(n)) / idx(0.01))

def stab(ms, dur=0.16, bright=2600, detune=0.11):
    n = idx(dur + 0.25); t = np.arange(n) / SR
    out = np.zeros(n)
    for m in ms:
        for d in (-detune, 0, detune):
            out += saw(mf(m + d), n, phase=rng.random())
    fenv = 500 + bright * np.exp(-t / 0.07)
    out = lp(out / (3 * len(ms)), fenv, 2)
    gate = np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.06))
    return out * env(n, 0.003, 0.25, 0.25) * gate

def pad(ms, dur, cutoff=1400):
    n = idx(dur); t = np.arange(n) / SR
    out = np.zeros(n)
    for m in ms:
        for d in (-0.08, 0.07):
            out += saw(mf(m + d), n, phase=rng.random())
    out = lp(out / (2 * len(ms)), cutoff, 2)
    a = np.minimum(1, t / 0.25); r = np.minimum(1, (dur - t) / 0.2)
    return out * a * np.clip(r, 0, 1)

def bell(m, dur=0.5, bright=1.0):
    n = idx(dur); t = np.arange(n) / SR
    f = mf(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * bright * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05) + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / 0.03)
    return x * env(n, 0.002, dur * 0.35)

def pluck(m, dur=0.35):
    n = idx(dur); t = np.arange(n) / SR
    x = saw(mf(m), n) * 0.5 + np.sin(2 * np.pi * mf(m) * t) * 0.6
    x = lp(x, 900 + 4000 * np.exp(-t / 0.04), 1)
    return x * env(n, 0.002, 0.11)

def whoosh(dur, up=True, f0=400, f1=5000):
    n = idx(dur); t = np.arange(n) / SR; k = t / dur
    fc = f0 + (f1 - f0) * (k ** 2 if up else (1 - k) ** 2)
    x = lp(noise(n), fc, 2) - lp(noise(n), fc * 0.3, 1) * 0.3
    e = (k ** 1.6 if up else (1 - k) ** 1.2) * np.minimum(1, (1 - k) * 30 if up else 1)
    return x * e * 0.5

def click():
    n = idx(0.06); t = np.arange(n) / SR
    x = hp(noise(n), 2500) * np.exp(-t / 0.0025) * 0.7 + np.sin(2 * np.pi * mf(91) * t) * np.exp(-t / 0.012) * 0.35
    return x

def pop(m, dur=0.16):
    n = idx(dur); t = np.arange(n) / SR
    f = mf(m) * (1 + 0.6 * np.exp(-t / 0.012))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.001, 0.045)

def thud(m=36):
    n = idx(0.5); t = np.arange(n) / SR
    f = mf(m) * (1 + 1.5 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(np.sin(ph) * np.exp(-t / 0.18) * 1.8) * 0.9

# ---------- Grille harmonique ----------
CH = {  # basse, voicing
    'C': (36, [60, 64, 67]), 'G': (43, [59, 62, 67]), 'Am': (45, [60, 64, 69]), 'F': (41, [60, 65, 69]),
}
PROG = [(0, 1, 'Am'), (1, 2, 'F'), (2, 3, 'G'), (3, 5, 'C'), (5, 7, 'G'), (7, 9, 'Am'), (9, 11, 'F'),
        (11, 13, 'C'), (13, 15, 'G'), (15, 17, 'Am'), (17, 19, 'F'), (19, 21, 'G'), (21, 22, 'C')]
def chord_at(t):
    for a, b, c in PROG:
        if a <= t < b: return c
    return 'C'
groove = lambda t: (3.0 <= t < 13.0) or (15.0 <= t < 21.0)

M = (np.zeros(N), np.zeros(N))    # harmonie (nappes, stabs, cloches)
DR = (np.zeros(N), np.zeros(N))   # batterie
BS = (np.zeros(N), np.zeros(N))   # basse
FX = (np.zeros(N), np.zeros(N))   # effets
VERB = (np.zeros(N), np.zeros(N)) # envoi réverbe
kicks = []

# Intro : nappe filtrée qui s'ouvre, coups de grosse caisse sur les impacts
for a, b, c in PROG[:3]:
    cut = 700 + 900 * a
    add(pad([m - 12 for m in CH[c][1]] + CH[c][1], b - a + 0.05, cut), a, 0.22, 0, M)
for tk in (0.0, 1.0, 2.0):
    add(kick(), tk, 0.9, 0, DR); kicks.append(tk)
for i in range(8):  # roulement de caisse claire 2.0 -> 2.94
    tt = 2.0 + i * 0.125
    add(clap(), tt, 0.10 + 0.05 * i, 0, DR)
add(whoosh(1.0, True, 300, 7000), 2.0, 0.55, 0, FX)

# Groove
for k in range(int(3.0 / BEAT), int(21.0 / BEAT)):
    tb = k * BEAT
    if not groove(tb): continue
    add(kick(), tb, 0.95, 0, DR); kicks.append(tb)
    beat_in_bar = int(round((tb - 3.0) / BEAT)) % 4
    if beat_in_bar in (1, 3): add(clap(), tb, 0.55, 0.05, DR); add(clap(), tb, 0.12, 0, VERB)
    add(hat(True), tb + 0.25, 0.55, 0.25, DR)
    for s16 in (0.125, 0.375):
        add(hat(False), tb + s16, 0.30, -0.3, DR)
    c = chord_at(tb)
    root = CH[c][0]
    add(bass_note(root + (12 if beat_in_bar == 3 else 0), 0.22), tb + 0.25, 0.55, 0, BS)
    add(bass_note(root, 0.12), tb, 0.30, 0, BS)
# Stabs syncopés (positions en doubles-croches dans la mesure)
for bar_t in np.arange(3.0, 21.0, 2.0):
    if not groove(bar_t): continue
    for s in (0, 3, 6, 10, 12, 14):
        tt = bar_t + s * 0.125
        c = chord_at(tt)
        st = stab(CH[c][1], 0.13 if s != 12 else 0.2)
        add(st, tt, 0.20, -0.35, M); add(st, tt + 0.012, 0.20, 0.35, M); add(st, tt, 0.05, 0, VERB)

# Break (scène « trajets ») : nappe de sol, charleston en doubles-croches, montée vers 15.0
add(pad([55, 59, 62, 67, 71], 2.05, 1500), 13.0, 0.26, 0, M)
for i in range(16):
    add(hat(False), 13.0 + i * 0.125, 0.22 + 0.01 * i, 0.2 * ((-1) ** i), DR)
add(whoosh(1.0, True, 300, 6500), 14.0, 0.45, 0, FX)
for i in range(8):
    add(clap(), 14.5 + i * 0.0625, 0.08 + 0.035 * i, 0, DR)
add(kick(), 13.0, 0.9, 0, DR); kicks.append(13.0)

# Mélodie (cloche) sur la fin : motif simple sur les accords
motif = {'C': [72, 76, 79, 76], 'G': [71, 74, 79, 74], 'Am': [72, 76, 81, 76], 'F': [72, 77, 81, 77]}
for bar_t in (11.0, 15.0, 17.0, 19.0):
    for j, s in enumerate((0, 3, 6, 8, 11, 14)):
        tt = bar_t + s * 0.125
        c = chord_at(tt); ns = motif[c]
        m = ns[j % 4]
        add(bell(m, 0.45), tt, 0.10, 0.15, M); add(bell(m, 0.45), tt, 0.05, 0, VERB)

# Final : accord de do plein + cymbale
add(kick(), 21.0, 1.0, 0, DR); kicks.append(21.0)
add(stab([48, 60, 64, 67, 72], 0.75, 3200), 21.0, 0.42, 0, M)
add(stab([48, 60, 64, 67, 72], 0.75, 3200), 21.0, 0.25, 0, VERB)
add(bass_note(36, 0.9), 21.0, 0.6, 0, BS)
add(bell(84, 1.0), 21.0, 0.12, 0, M)

# ---------- Effets (même tonalité, même grille) ----------
pent = [72, 74, 76, 79, 81, 84, 86, 88, 91, 93]
# accroche : impacts + souffles avant les cartes
for tk, m in ((0.0, 36), (1.0, 41), (2.0, 43)):
    add(thud(m), tk, 0.55, 0, FX)
for tk in (1.0, 2.0):
    add(whoosh(0.22, True, 600, 6000), tk - 0.22, 0.35, 0.3, FX)
add(whoosh(0.26, True, 500, 8000), 2.74, 0.5, 0, FX)   # balayage vers l'app
add(crash(), 3.0, 0.55, 0, FX); add(crash(), 15.0, 0.38, 0, FX); add(crash(), 17.0, 0.42, 0, FX); add(crash(), 21.0, 0.5, 0, FX)

man = json.load(open('data/manifest.json'))
pins = sorted(man['after']['pins'], key=lambda p: p['p'][0])
for i, p in enumerate(pins):  # épingles : pops en triples-croches, panoramique selon la position
    tt = 3.125 + i * 0.0625
    pan = (p['p'][0] / 1456) * 1.4 - 0.7
    add(pop(pent[i % len(pent)] - 12 + 12 * (i // 7)), tt, 0.22, pan, FX)
for i in range(8):  # points : petites cloches aiguës
    add(bell(pent[(i * 2) % len(pent)] + 12, 0.18, 0.4), 3.5 + i * 0.125, 0.05, 0.5 * ((-1) ** i), FX)
for tc in (3.42, 3.62, 8.95, 15.1):   # légendes
    add(whoosh(0.18, True, 900, 5000), tc - 0.08, 0.16, -0.5, FX)
add(whoosh(1.2, True, 250, 2500), 5.75, 0.22, 0.3, FX)   # caméra vers le bouton
add(click(), 7.5, 0.5, 0.25, FX); add(click(), 8.5, 0.5, 0.1, FX)
add(pop(79, 0.2), 7.5625, 0.25, 0, FX); add(pop(72, 0.2), 8.5625, 0.18, 0, FX)
# liaisons : arpège montant en doubles-croches (la mineur -> fa majeur)
arp = [69, 72, 76, 77, 81, 84, 88, 89, 93, 96, 100, 101, 105]
for i, m in enumerate(arp):
    tt = 8.875 + i * 0.125
    add(pluck(m - 12, 0.3), tt, 0.16 + 0.006 * i, 0.4 * np.sin(i), FX)
    add(pluck(m - 12, 0.3), tt, 0.05, 0, VERB)
# résultat : carillon de do majeur
for j, m in enumerate((84, 88, 91, 96)):
    add(bell(m, 0.7), 11.0 + j * 0.0625, 0.16, (j - 1.5) * 0.2, FX); add(bell(m, 0.7), 11.0 + j * 0.0625, 0.08, 0, VERB)
add(thud(36), 11.0, 0.35, 0, FX)
# scène trajets : barres, puis tampons
add(whoosh(0.3, True, 300, 3000), 13.25, 0.22, -0.2, FX); add(whoosh(0.3, True, 300, 3000), 13.5, 0.22, 0.2, FX)
add(thud(31), 13.75, 0.5, 0, FX); add(pop(55, 0.25), 13.75, 0.2, 0, FX)
for j, m in enumerate((86, 91)):
    add(bell(m, 0.6), 14.0 + j * 0.0625, 0.17, 0.1, FX); add(bell(m, 0.6), 14.0, 0.06, 0, VERB)
# parcours : petites touches, puis la colonne « prévu »
for i in range(6):
    add(bell(pent[i] + 12, 0.15, 0.3), 15.125 + i * 0.125, 0.045, 0.4 * ((-1) ** i), FX)
for i in range(4):
    add(pop(pent[i + 3], 0.18), 15.625 + i * 0.0625, 0.12, 0.2, FX)
# final
add(whoosh(0.22, True, 500, 8000), 16.72, 0.45, 0, FX)
add(pop(72, 0.3), 17.0, 0.35, 0, FX); add(pop(84, 0.25), 17.06, 0.2, 0, FX)
add(thud(36), 17.25, 0.25, 0, FX)
add(click(), 17.8, 0.3, 0, FX)

# ---------- Mixage ----------
# compression latérale sur la musique (pompe sous la grosse caisse), hors grosse caisse elle-même
duck = np.ones(N)
for tk in kicks:
    i0 = idx(tk); n = min(idx(0.3), N - i0)
    tt = np.arange(n) / SR
    duck[i0:i0 + n] = np.minimum(duck[i0:i0 + n], 1 - 0.45 * np.exp(-tt / 0.09))
def rms(b): return 20 * np.log10(np.sqrt(np.mean((b[0] + b[1]) ** 2) / 2) + 1e-12)
print('rms dB  drums %.1f  bass %.1f  harm %.1f  fx %.1f' % (rms(DR), rms(BS), rms(M), rms(FX)))
G_DR, G_BS, G_M = 0.5, 1.4, 2.3
mus = (DR[0] * G_DR + (BS[0] * G_BS + M[0] * G_M) * (0.55 + 0.45 * duck), DR[1] * G_DR + (BS[1] * G_BS + M[1] * G_M) * (0.55 + 0.45 * duck))

# réverbe : réponse impulsionnelle de bruit à décroissance exponentielle
ir_n = idx(0.9); ir_t = np.arange(ir_n) / SR
def conv(x, ir):
    n = len(x) + len(ir) - 1; nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(ir, nf), nf)[: len(x)]
irL = lp(noise(ir_n), 5000, 1) * np.exp(-ir_t / 0.28); irR = lp(noise(ir_n), 5000, 1) * np.exp(-ir_t / 0.28)
irL /= np.sqrt(np.sum(irL ** 2)); irR /= np.sqrt(np.sum(irR ** 2))
rv = (conv(VERB[0], irL) * 0.5, conv(VERB[1], irR) * 0.5)
fxv = (conv(FX[0] * 0.25, irL) * 0.5, conv(FX[1] * 0.25, irR) * 0.5)

out = np.stack([mus[0] + FX[0] * 0.85 + rv[0] + fxv[0], mus[1] + FX[1] * 0.85 + rv[1] + fxv[1]])
out = hp(out[0], 28), hp(out[1], 28)
out = np.stack(out)
# fondu final
fade = np.clip((DUR - t_all) / 0.35, 0, 1); out *= fade
fi = np.clip(t_all / 0.004, 0, 1); out *= fi
# limiteur doux
peak = np.max(np.abs(out)); out = out / peak * 1.25
out = np.tanh(out) / np.tanh(1.25) * 0.89
wav = (out.T * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(wav.tobytes())
print('mix rms drums %.1f bass %.1f harm %.1f fx %.1f' % (rms((DR[0]*G_DR, DR[1]*G_DR)), rms((BS[0]*G_BS, BS[1]*G_BS)), rms((M[0]*G_M, M[1]*G_M)), rms((FX[0]*.85, FX[1]*.85))))
print('ok', out.shape, 'rms dB', 20 * np.log10(np.sqrt(np.mean(out ** 2))))
