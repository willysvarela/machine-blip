---
name: machine-blip
description: Play a short synthesized droid-style "machine blip" chatter. Use when the user asks to hear the blip, test it, play the variations, or change how it sounds.
---

# Machine blip

Plays a droid-style chatter. Every play synthesizes a new random phrase: 3–6 syllables (chirps,
short "dee"s, trills, warbles) ending in an impressed, falling "fiu fiu" (45%), a rising "wheep"
(35%) or an inquisitive "dwoo" (20%).

## Play it

```bash
bash scripts/blip.sh
```

Run it from this skill's directory. It is non-blocking and exits 0 even if audio fails.

## Change the sound

`scripts/make_blip.py [out.wav] [--seed N]` is a stdlib-only synthesizer. The syllable functions
(`chirp`, `dee`, `trill`, `wobble`, `wheep`, `dwoo`, `fiu_fiu`) and the weights in the phrase
builder at the bottom shape the voice. `--seed` reproduces a phrase. After editing, play it to
let the user hear the result. Without Python, `blip.sh` falls back to a system sound.

## Requirements

`python3` plus a player: `afplay` (macOS), or `pw-play`, `paplay` or `aplay` (Linux).
