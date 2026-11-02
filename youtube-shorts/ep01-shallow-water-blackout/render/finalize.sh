#!/usr/bin/env bash
# Mux rendered video + mixed audio into the upload-ready Short.
set -euo pipefail
cd "$(dirname "$0")/../out"
ffmpeg -y -v error -i video_noaudio.mp4 -i mix.wav \
  -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset slow -crf 19 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -profile:v high -level 4.2 \
  -x264-params "keyint=60:min-keyint=30" \
  -af "volume=-0.6dB,alimiter=limit=0.82:attack=2:release=60:level=false" \
  -c:a aac -b:a 192k -ar 48000 \
  -shortest -movflags +faststart \
  -metadata title="Shallow Water Blackout" \
  ep01_shallow_water_blackout.mp4
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=nw=1 ep01_shallow_water_blackout.mp4
