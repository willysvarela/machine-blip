#!/bin/bash
# Play a freshly generated blip without blocking the caller.
#   blip.sh                  play in the current style (droid or smooth)
#   blip.sh --style          print the current style
#   blip.sh --style NAME     switch to droid or smooth (smooth installs earshot on first use), then play it
# MACHINE_BLIP_STYLE overrides the saved style. Falls back to droid, then to a system sound, if generation fails.
# Always exits 0 when playing so it is safe in hooks.
dir="$(cd "$(dirname "$0")" && pwd)"
home="${MACHINE_BLIP_HOME:-$HOME/.cache/machine-blip}"
conf="${XDG_CONFIG_HOME:-$HOME/.config}/machine-blip/style"

if [ "$1" = "--style" ]; then
  case "$2" in
    "") cat "$conf" 2>/dev/null || echo droid; exit 0 ;;
    droid) ;;
    smooth) bash "$dir/setup_smooth.sh" || exit 1 ;;
    *) echo "machine-blip: unknown style '$2' (droid or smooth)" >&2; exit 1 ;;
  esac
  mkdir -p "$(dirname "$conf")" && echo "$2" > "$conf"
  echo "machine-blip: style set to $2"
fi
style="${MACHINE_BLIP_STYLE:-$(cat "$conf" 2>/dev/null)}"

play() {
  if command -v afplay >/dev/null 2>&1; then afplay "$1"
  elif command -v pw-play >/dev/null 2>&1; then pw-play "$1"
  elif command -v paplay >/dev/null 2>&1; then paplay "$1"
  elif command -v aplay >/dev/null 2>&1; then aplay -q "$1"
  fi
} >/dev/null 2>&1

smooth() {
  [ "$style" = smooth ] && PYTHONPATH="$home/earshot" "$home/venv/bin/python" "$dir/make_smooth.py" "$1"
}

py="$(command -v python3)"
base="$(mktemp "${TMPDIR:-/tmp}/machine-blip.XXXXXX")" && rm -f "$base"
tmp="$base.wav"
(
  if smooth "$tmp" 2>/dev/null || { [ -n "$py" ] && "$py" "$dir/make_blip.py" "$tmp" 2>/dev/null; }; then
    play "$tmp"
  else
    for f in /System/Library/Sounds/Pop.aiff /usr/share/sounds/freedesktop/stereo/complete.oga; do
      [ -f "$f" ] && { play "$f"; break; }
    done
  fi
  rm -f "$tmp"
) </dev/null >/dev/null 2>&1 &
exit 0
