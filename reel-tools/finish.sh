#!/bin/bash
# finish.sh DIR NAME — render + master (crf17) + instagram copy + contact sheets
set -e
SP=/tmp/claude-0/-home-user-sarier/08997238-b1ce-5d5f-8d4f-63bf23144449/scratchpad
export HYPERFRAMES_NO_TELEMETRY=1
cd "$SP/$1"; rm -rf renders
node /home/user/heygen-com/hyperframes/packages/cli/bin/hyperframes.mjs render 2>&1 | tail -2
cd renders; RAW=$(ls -t *.mp4 | head -1)
ffmpeg -nostdin -y -v error -i "$RAW" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 192k "$2-final.mp4"
ffmpeg -nostdin -y -v error -i "$RAW" -c:v libx264 -preset slow -crf 24 -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 160k "$2-final-instagram.mp4"
rm -f "$RAW"
ffmpeg -nostdin -y -v error -i "$2-final.mp4" -vf "select='not(mod(n,100))',scale=270:480,tile=8x3" -frames:v 1 final-sheet.jpg
ls -la; echo "FINISH DONE $1"
