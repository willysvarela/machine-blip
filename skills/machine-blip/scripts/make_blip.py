"""Synthesize a droid-style chatter WAV: a random phrase of whistle glides, chirps and trills.

Usage: make_blip.py [out.wav] [--seed N]   (no seed = new phrase every run)
"""
import math, random, struct, wave, sys, os

RATE = 44100
args = sys.argv[1:]
seed = None
if "--seed" in args:
    i = args.index("--seed")
    seed = int(args[i + 1])
    del args[i : i + 2]
out = args[0] if args else os.path.join(os.path.dirname(__file__), "blip.wav")
rng = random.Random(seed)

def whistle(f0, f1, dur, trill=0.0, trill_hz=0.0, vibrato=0.0, via=None, via_at=0.3):
    """Sine whistle, exponential glide f0->f1 (through `via` at `via_at` if given),
    optional trill (pitch flutter) and vibrato."""
    n = int(RATE * dur)
    phase, samples = 0.0, []
    for i in range(n):
        t = i / n
        if via is None:
            f = f0 * (f1 / f0) ** t
        elif t < via_at:
            f = f0 * (via / f0) ** (t / via_at)
        else:
            f = via * (f1 / via) ** ((t - via_at) / (1 - via_at))
        if trill:
            f *= 1 + trill * (1 if math.sin(2 * math.pi * trill_hz * i / RATE) >= 0 else -1)
        f *= 1 + vibrato * math.sin(2 * math.pi * 9 * i / RATE)
        phase += 2 * math.pi * f / RATE
        tone = math.sin(phase) + 0.08 * math.sin(3 * phase)
        env = min(1.0, i / 120) * min(1.0, (n - i) / 250)
        samples.append(tone * env)
    return samples

def gap():
    return [0.0] * int(RATE * rng.uniform(0.008, 0.025))

def pitch(lo=1400, hi=3400):
    return rng.uniform(lo, hi)

def chirp():  # bi / doo: quick glide up or down
    return whistle(pitch(), pitch(), rng.uniform(0.035, 0.06))

def dee():  # short near-flat note
    f = pitch(2200, 3500)
    return whistle(f, f * rng.uniform(0.95, 1.08), rng.uniform(0.025, 0.04))

def trill():  # brrrrt
    f = pitch(1500, 2600)
    return whistle(f, f * rng.uniform(0.85, 1.25), rng.uniform(0.09, 0.15),
                   trill=rng.uniform(0.12, 0.22), trill_hz=rng.uniform(22, 34))

def wobble():  # warbly mid glide
    return whistle(pitch(1500, 2500), pitch(1800, 3000), rng.uniform(0.07, 0.11), vibrato=rng.uniform(0.04, 0.08))

def wheep():  # happy rising finish
    return whistle(pitch(1300, 1900), pitch(3000, 3900), rng.uniform(0.13, 0.19), vibrato=0.03)

def dwoo():  # inquisitive falling finish
    return whistle(pitch(2800, 3500), pitch(1200, 1600), rng.uniform(0.12, 0.17), vibrato=0.025)

def fiu():  # one "fiu": quick flick up, long swoop down
    top = pitch(2900, 3700)
    return whistle(top * rng.uniform(0.6, 0.7), top * rng.uniform(0.38, 0.48), rng.uniform(0.17, 0.22),
                   via=top, via_at=rng.uniform(0.2, 0.3), vibrato=0.01)

def fiu_fiu():  # impressed "fiu fiu" finish
    return fiu() + [0.0] * int(RATE * rng.uniform(0.06, 0.1)) + fiu()

phrase = []
for _ in range(rng.randint(3, 6)):
    phrase.append(rng.choices([chirp, dee, trill, wobble], weights=[5, 3, 2, 2])[0])
if trill not in phrase and rng.random() < 0.6:
    phrase.insert(rng.randrange(1, len(phrase) + 1), trill)
phrase.append(rng.choices([fiu_fiu, wheep, dwoo], weights=[45, 35, 20])[0])

audio = []
for i, syllable in enumerate(phrase):
    if i:
        audio += gap()
    audio += syllable()

peak = max(abs(s) for s in audio)
audio = [s / peak * 0.45 for s in audio]

with wave.open(out, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(b"".join(struct.pack("<h", int(s * 32767)) for s in audio))
