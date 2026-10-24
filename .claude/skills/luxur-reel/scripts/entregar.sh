#!/bin/bash
# entregar.sh DIR NOMBRE — render + master + copia Instagram, ajustando la calidad hasta que entren.
#
# Dos límites mandan sobre el crf: GitHub rechaza archivos de más de 100 MiB y por el chat no pasan
# más de 30 MB. Un reel de 50 s entra en crf 17; uno de 100 s no, así que el master baja de crf
# hasta caber en vez de fallar el push.
set -euo pipefail
DIR="${1:?uso: entregar.sh DIR NOMBRE}"
NAME="${2:?uso: entregar.sh DIR NOMBRE}"
SP=/tmp/claude-0/-home-user-sarier/08997238-b1ce-5d5f-8d4f-63bf23144449/scratchpad
export HYPERFRAMES_NO_TELEMETRY=1

MAX_MASTER=$((100 * 1024 * 1024))
MAX_IG=$((30 * 1024 * 1024))
V="libx264 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart"

cd "$SP/$DIR"
rm -rf renders
hyperframes render 2>&1 | tail -2
cd renders
RAW=$(ls -t *.mp4 | head -1)

for CRF in 17 19 20 21 22 23; do
  ffmpeg -nostdin -y -v error -i "$RAW" -c:v $V -crf $CRF -c:a aac -b:a 192k "$NAME-final.mp4"
  S=$(stat -c%s "$NAME-final.mp4")
  echo "master crf $CRF -> $((S / 1048576)) MiB"
  [ "$S" -lt "$MAX_MASTER" ] && break
done

for R in 3000 2600 2150 1800; do
  ffmpeg -nostdin -y -v error -i "$RAW" -c:v $V -crf 24 -maxrate ${R}k -bufsize $((R * 2))k \
    -c:a aac -b:a 128k "$NAME-final-instagram.mp4"
  S=$(stat -c%s "$NAME-final-instagram.mp4")
  echo "instagram ${R}k -> $((S / 1048576)) MiB"
  [ "$S" -lt "$MAX_IG" ] && break
done

rm -f "$RAW"
ffmpeg -nostdin -y -v error -i "$NAME-final.mp4" \
  -vf "select='not(mod(n,100))',scale=270:480,tile=8x3" -frames:v 1 final-sheet.jpg
ls -la
echo "ENTREGA LISTA $DIR"
