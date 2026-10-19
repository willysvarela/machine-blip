# Machine Blip

A Claude Code plugin that plays a short sound every time Claude finishes a turn, so you can look
away and still hear when it's done.

Every blip is synthesized on the spot, so no two sound the same. Pick a style:

- **droid** (default): a few chirps, trills and warbles that end in an impressed **"fiu fiu"**, a
  happy rising **"wheep!"** or a curious **"dwoo?"**. Nothing to download; a tiny Python script using
  only the standard library makes it.
- **smooth**: a soft kalimba motif of 2–4 notes that rises, settles or arcs. The notes are
  physically modelled kalimba plucks from [earshot](https://github.com/Leonxlnx/earshot)'s sound bank.

## Install

### As a Claude Code plugin (plays automatically)

```bash
claude plugin marketplace add willysvarela/machine-blip
claude plugin install machine-blip@machine-blip
```

Or inside a session: `/plugin install machine-blip --marketplace willysvarela/machine-blip`.

This installs the skill and a `Stop` hook that plays the blip whenever Claude finishes responding.
Start a new session (or run `/reload-plugins`) and you will hear it at the end of the next reply.

### As a standalone skill (on demand)

```bash
npx skills add willysvarela/machine-blip
```

This installs only the skill, so it plays when you ask ("play the blip", "make it sound sadder").
To also play it automatically, add a `Stop` hook to `~/.claude/settings.json` that runs
`bash /path/to/skills/machine-blip/scripts/blip.sh`.

## Switch style

Ask Claude ("switch the blip to smooth") or run:

```bash
bash skills/machine-blip/scripts/blip.sh --style smooth   # or: droid
```

The choice is saved in `~/.config/machine-blip/style` (the `MACHINE_BLIP_STYLE` env var overrides
it). The first switch to smooth fetches a pinned copy of earshot plus a numpy/scipy virtualenv into
`~/.cache/machine-blip` (~230 MB; only earshot's sound bank is used, so no torch and no models). If
the smooth style can't render, the droid blip plays instead.

## Requirements

- `python3`
- macOS (`afplay`, built in) or Linux with `pw-play`, `paplay` or `aplay`
- smooth style only: `git` and network access for the one-time setup

## Customize

Ask Claude: "make the blip calmer", "more trills", "only end with fiu fiu", "slower kalimba". Or edit
`skills/machine-blip/scripts/make_blip.py` (droid) yourself: each syllable is a small function, and the
weights at the bottom decide how often each one appears. `make_smooth.py` does the same for the
smooth motif's shapes, voices and timing.

## Turn it off

`claude plugin disable machine-blip@machine-blip`

## License

MIT
