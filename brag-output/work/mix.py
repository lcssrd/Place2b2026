# Bande-son v2 : extrait de « Happy Beats / Business Moves Vol. 12 » (Sascha Ende, CC BY 4.0)
# + bruitages Kenney (CC0), placés sur la grille de la musique (110 BPM, un temps = 0,5454 s).
import wave
import numpy as np

SR = 48000
DUR = 19.5
N = int(SR * DUR)
B = 0.5454
K = lambda n: n * B

def load(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    return x.reshape(-1, w.getnchannels()).T

music = load('music/excerpt.wav')[:, :N]
music = np.pad(music, ((0, 0), (0, N - music.shape[1])))
t = np.arange(N) / SR
music *= np.clip(t / 0.03, 0, 1) * np.clip((DUR - t) / 1.4, 0, 1) ** 1.5   # fondu de fin sur 1,4 s

fx = np.zeros((2, N))
def place(name, at, db, pan=0.0):
    s = load(f'sfx/{name}.wav')
    i = int(round(at * SR)); s = s[:, : max(0, N - i)]
    g = 10 ** (db / 20); a = (pan + 1) * np.pi / 4
    fx[0, i:i + s.shape[1]] += s[0] * g * np.cos(a) * np.sqrt(2)
    fx[1, i:i + s.shape[1]] += s[1] * g * np.sin(a) * np.sqrt(2)

# accroche : chaque ligne qui tombe
place('impactSoft_medium_001', K(0), -11, -0.2)
place('impactSoft_medium_002', K(1.5), -11, 0.2)
place('impactSoft_heavy_001', K(3), -13)
# balayage puis arrivée de l'app sur l'entrée de la basse
place('card-slide-1', 3.02, -17)
place('impactSoft_medium_003', K(6), -12)
for j, n in enumerate(('drop_001', 'drop_002', 'drop_003')):   # épingles (très discret)
    place(n, K(6) + 0.136 * (j + 1) * 2, -24, -0.5 + 0.5 * j)
place('rollover2', K(7), -22)                    # légende vue d'ensemble
# clic sur l'étudiant, la fiche glisse
place('click_003', K(13), -9, -0.3)
place('card-slide-1', K(13) + 0.02, -21, -0.3)
place('rollover2', K(14), -22, 0.4)              # légende « Un clic »
# survols : le trajet s'affiche, l'étiquette apparaît
for h in (K(18), K(22)):
    place('rollover2', h, -15, -0.3)
    place('bong_001', h + 0.3, -19, 0.2)
place('rollover2', K(19), -24, 0.4)              # légende « Chaque trajet »
# final
place('card-slide-1', 13.96, -17)
place('impactBell_heavy_000', K(26), -15)
place('click_002', K(28), -16)

out = music + fx
peak = np.max(np.abs(out))
if peak > 0.98: out *= 0.98 / peak
pcm = (out.T * 32767).astype(np.int16)
with wave.open('audio2.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
print('musique %.1f dB  effets %.1f dB  crête %.2f' % (rms(music), rms(fx), peak))
