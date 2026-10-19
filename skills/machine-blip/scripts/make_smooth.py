"""Synthesize a smooth kalimba motif WAV with earshot's sound bank (https://github.com/Leonxlnx/earshot).

Usage: make_smooth.py [out.wav] [--seed N]   (no seed = new motif every run)

Needs earshot importable (setup_smooth.sh clones it next to a numpy/scipy venv; no models, no network).
"""
import os, random, sys, tempfile, wave

import numpy as np
from earshot.forge import bank

SR = bank.SR
args = sys.argv[1:]
seed = None
if "--seed" in args:
    i = args.index("--seed")
    seed = int(args[i + 1])
    del args[i : i + 2]
out = args[0] if args else os.path.join(tempfile.gettempdir(), "machine-blip.wav")
rng = random.Random(seed)

PENTA = [0, 2, 4, 7, 9]  # major pentatonic: any two notes sound good together

def hz(semis):  # semitones above C5
    return 523.25 * 2 ** (semis / 12)

def scale(root, lo, hi):  # pentatonic degrees in [lo, hi] semitones above root
    return [root + 12 * o + s for o in range(-1, 3) for s in PENTA if lo <= 12 * o + s <= hi]

def rise(root):  # climb to the octave: "done!"
    return sorted(rng.sample(scale(root, 0, 9), rng.randint(1, 3))) + [root + 12]

def fall(root):  # gentle settle down onto the tonic
    return sorted(rng.sample(scale(root, 4, 12), rng.randint(1, 3)), reverse=True) + [root]

def arc(root):  # up and back: a little question
    top = rng.choice(scale(root, 7, 14))
    return [root, top, rng.choice(scale(root, 2, 7))]

voice = bank.get(rng.choice(["pluck/kalimba", "pluck/kalimba_soft", "pluck/kalimba_ring"]))
root = rng.choice([-5, -3, 0, 2])  # G4 A4 C5 D5
notes = rng.choices([rise, fall, arc], weights=[45, 35, 20])[0](root)

step = rng.uniform(0.09, 0.15)
ring = rng.uniform(0.9, 1.3)  # how long the last note rings before the fade
length = int(SR * (step * (len(notes) - 1) + ring))
mix = np.zeros((length, 2))
note_seed = rng.randrange(1 << 30)
for i, semis in enumerate(notes):
    x = bank.renderer(voice, note_seed + i)({"f0": hz(semis)})
    x = x[:, None].repeat(2, 1) if x.ndim == 1 else x
    x = x / np.abs(x).max() * (1.0 if i == len(notes) - 1 else rng.uniform(0.55, 0.8))
    start = int(SR * (step * i + rng.uniform(-0.006, 0.006))) if i else 0
    seg = x[: length - start]
    mix[start : start + len(seg)] += seg

fade = int(SR * 0.35)
mix[-fade:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fade)))[:, None]
mix *= 0.45 / np.abs(mix).max()

with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
