#!/bin/bash
# Install what the "smooth" style needs: a pinned clone of earshot (https://github.com/Leonxlnx/earshot) and a
# venv with numpy + scipy. Only earshot's sound bank is used, so no torch, no models.
set -e
home="${MACHINE_BLIP_HOME:-$HOME/.cache/machine-blip}"
rev=925ebe56a1b755e5d354ab642bb8f344440cfa9c
py="$(command -v python3)" || { echo "machine-blip: python3 is required" >&2; exit 1; }

mkdir -p "$home"
if [ "$(git -C "$home/earshot" rev-parse HEAD 2>/dev/null)" != "$rev" ]; then
  echo "machine-blip: fetching earshot @ ${rev:0:7} into $home/earshot"
  rm -rf "$home/earshot"
  git init -q "$home/earshot"
  git -C "$home/earshot" fetch -q --depth 1 https://github.com/Leonxlnx/earshot.git "$rev"
  git -C "$home/earshot" checkout -q FETCH_HEAD
fi
if ! "$home/venv/bin/python" -c "import numpy, scipy" 2>/dev/null; then
  echo "machine-blip: creating $home/venv (numpy, scipy)"
  "$py" -m venv "$home/venv"
  "$home/venv/bin/python" -m pip install -q --disable-pip-version-check "numpy>=1.26" "scipy>=1.11"
fi
PYTHONPATH="$home/earshot" "$home/venv/bin/python" "$(dirname "$0")/make_smooth.py" "$home/check.wav" --seed 1
rm -f "$home/check.wav"
echo "machine-blip: smooth style ready"
