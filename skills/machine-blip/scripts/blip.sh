#!/bin/bash
# Play a freshly generated droid chatter without blocking the caller.
# Falls back to a system sound if generation fails. Always exits 0 so it is safe in hooks.
dir="$(cd "$(dirname "$0")" && pwd)"

play() {
  if command -v afplay >/dev/null 2>&1; then afplay "$1"
  elif command -v pw-play >/dev/null 2>&1; then pw-play "$1"
  elif command -v paplay >/dev/null 2>&1; then paplay "$1"
  elif command -v aplay >/dev/null 2>&1; then aplay -q "$1"
  fi
} >/dev/null 2>&1

py="$(command -v python3)"
base="$(mktemp "${TMPDIR:-/tmp}/machine-blip.XXXXXX")" && rm -f "$base"
tmp="$base.wav"
(
  if [ -n "$py" ] && "$py" "$dir/make_blip.py" "$tmp" 2>/dev/null; then
    play "$tmp"
  else
    for f in /System/Library/Sounds/Pop.aiff /usr/share/sounds/freedesktop/stereo/complete.oga; do
      [ -f "$f" ] && { play "$f"; break; }
    done
  fi
  rm -f "$tmp"
) </dev/null >/dev/null 2>&1 &
exit 0
