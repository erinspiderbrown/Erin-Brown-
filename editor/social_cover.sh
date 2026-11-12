#!/bin/bash
# Social upload copy with the cover thumbnail as the first 3 frames (0.1 s), so TikTok / Instagram
# pick it as the cover (neither upload API takes a custom cover image).
# usage: social_cover.sh <master.mp4> <thumb.jpg> <out.mp4> [video bitrate, e.g. 5000k; default crf 18]
# Audio is copied untouched and offset by 0.1 s to stay in sync.
# Phone-safe H.264 (owner's iPhone/Dropbox/TikTok couldn't play the 318 MB High@5.0 file): High@4.1,
# capped peaks, 2 s keyframes. Colour stays BT.601 as build.py writes it.
set -e
IN="$1"; TH="$2"; OUT="$3"; BR="${4:-}"
BR="${BR:-6000k}"; V="-crf 19 -maxrate $BR -bufsize $(( ${BR%k} * 2 ))k -profile:v high -level:v 4.1 -g 60 -colorspace bt470bg -color_range tv"
ffmpeg -v error -y -loop 1 -framerate 30 -t 0.1 -i "$TH" -i "$IN" -itsoffset 0.1 -i "$IN" \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[c];[1:v]format=yuv420p,setsar=1[m];[c][m]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow $V -r 30 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
