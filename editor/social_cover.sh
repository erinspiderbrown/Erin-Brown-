#!/bin/bash
# Social upload copy with the cover thumbnail as the first 3 frames (0.1 s), so TikTok / Instagram
# pick it as the cover (neither upload API takes a custom cover image).
# usage: social_cover.sh <master.mp4> <thumb.jpg> <out.mp4> [video bitrate, e.g. 5000k; default crf 18]
# Audio is copied untouched and offset by 0.1 s to stay in sync.
set -e
IN="$1"; TH="$2"; OUT="$3"; BR="${4:-}"
if [ -n "$BR" ]; then V="-b:v $BR -maxrate $(( ${BR%k} * 13 / 10 ))k -bufsize $(( ${BR%k} * 2 ))k"; else V="-crf 18"; fi
ffmpeg -v error -y -loop 1 -framerate 30 -t 0.1 -i "$TH" -i "$IN" -itsoffset 0.1 -i "$IN" \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[c];[1:v]format=yuv420p,setsar=1[m];[c][m]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow $V -r 30 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
