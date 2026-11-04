#!/usr/bin/env bash
# One-time setup: Python deps, fonts (Google Fonts / OFL), and the Mixkit SFX library (Mixkit Free License).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
pip install -q faster-whisper numpy
mkdir -p "$HERE/assets/fonts" "$HERE/assets/sfx_raw" "$HERE/assets/sfx"
F="$HERE/assets/fonts"
curl -sSL -o "$F/Anton-Regular.ttf"      https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf
curl -sSL -o "$F/BebasNeue-Regular.ttf"  https://raw.githubusercontent.com/google/fonts/main/ofl/bebasneue/BebasNeue-Regular.ttf
for w in Black ExtraBold; do
  curl -sSL -o "$F/Montserrat-$w.ttf" "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-$w.ttf"
done
while read -r name id; do
  [ -z "$name" ] && continue
  curl -sSL -o "$HERE/assets/sfx_raw/$name.mp3" "https://assets.mixkit.co/active_storage/sfx/$id/$id-preview.mp3"
done < "$HERE/sfx_list.txt"
python3 "$HERE/prep_sfx.py" "$HERE/assets/sfx_raw" "$HERE/assets/sfx"
echo "setup done"
