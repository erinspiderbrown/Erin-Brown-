#!/usr/bin/env bash
# One-time setup: Python deps, fonts (Google Fonts / OFL), and the Mixkit SFX library (Mixkit Free License).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
pip install -q faster-whisper numpy onnxruntime
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
# Real-ESRGAN general x4 v3 (BSD-3) for enhance.py: AI upscaling of low-res clips/photos, runs on CPU
mkdir -p "$HERE/assets/models"
curl -sSL -o /tmp/esr.zip https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/models/real_esrgan_general_x4v3/releases/v0.66.0/real_esrgan_general_x4v3-onnx-float.zip
unzip -o -j -q /tmp/esr.zip '*.onnx' '*.data' -d "$HERE/assets/models" && rm /tmp/esr.zip
echo "setup done"
