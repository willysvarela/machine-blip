---
name: machine-blip
description: Play a short synthesized "machine blip" (droid-style chatter or a smooth kalimba motif). Use when the user asks to hear the blip, test it, play the variations, switch between the droid and smooth styles, or change how it sounds.
---

# Machine blip

Two styles, each synthesizing a new random phrase on every play:

- **droid** (default): 3–6 syllables (chirps, short "dee"s, trills, warbles) ending in an impressed,
  falling "fiu fiu" (45%), a rising "wheep" (35%) or an inquisitive "dwoo" (20%).
- **smooth**: a soft 2–4 note kalimba motif on a pentatonic scale that rises to the octave (45%),
  settles down onto the tonic (35%) or arcs up and back (20%). The notes are physically modelled
  kalimba plucks from [earshot](https://github.com/Leonxlnx/earshot)'s sound bank.

## Play it

```bash
bash scripts/blip.sh
```

Run it from this skill's directory. It is non-blocking and exits 0 even if audio fails.

## Switch style

```bash
bash scripts/blip.sh --style smooth   # or: droid
bash scripts/blip.sh --style          # print the current style
```

The choice is saved in `~/.config/machine-blip/style` and applies to the Stop hook too
(`MACHINE_BLIP_STYLE` overrides it). The first switch to smooth runs `scripts/setup_smooth.sh`,
which clones a pinned earshot and a numpy/scipy venv into `~/.cache/machine-blip` (~230 MB, needs
network and `git`; no torch or models). If smooth can't render, the droid blip plays instead.

## Change the sound

`scripts/make_blip.py [out.wav] [--seed N]` is the stdlib-only droid synthesizer. The syllable
functions (`chirp`, `dee`, `trill`, `wobble`, `wheep`, `dwoo`, `fiu_fiu`) and the weights in the
phrase builder at the bottom shape the voice.

`scripts/make_smooth.py [out.wav] [--seed N]` builds the smooth motif: the shapes (`rise`, `fall`,
`arc`), their weights, the kalimba voice (`pluck/kalimba`, `pluck/kalimba_soft`,
`pluck/kalimba_ring`), the root note, note spacing and ring time. Run it with
`PYTHONPATH=~/.cache/machine-blip/earshot ~/.cache/machine-blip/venv/bin/python`.

`--seed` reproduces a phrase. After editing, play it to let the user hear the result. Without
Python, `blip.sh` falls back to a system sound.

## Requirements

`python3` plus a player: `afplay` (macOS), or `pw-play`, `paplay` or `aplay` (Linux). Smooth also
needs `git` and network access once, for the setup.
