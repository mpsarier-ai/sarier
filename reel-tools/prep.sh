#!/bin/bash
# prep.sh DIR URL SHA — download + verify, align the script, cut pauses, encode, contact sheet
set -euo pipefail
SP=/tmp/claude-0/-home-user-sarier/08997238-b1ce-5d5f-8d4f-63bf23144449/scratchpad
DIR=$1; URL=$2; SHA=$3
cd "$SP/$DIR"
[ -f orig.mov ] || curl -sSL -o orig.mov "$URL"
echo "$SHA  orig.mov" | sha256sum -c
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 orig.mov | awk -F/ '{printf "%d", $1/$2}')
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -show_entries format=duration -of default=nw=1 orig.mov | tee probe.txt
echo "$FPS" > fps.txt
cp ../reel-dream/align.py ../reel-dream/retime2.py ../reel-dream/cut.py ../reel-dream/package.json ../reel-dream/hyperframes.json .
mkdir -p public tts tts16 brain; cp -r ../reel-dream/public/fonts ../reel-dream/public/vendor public/; cp ../reel-dream/brain/brainpath.py brain/
ffmpeg -nostdin -y -v error -i orig.mov -vn -ac 1 -ar 16000 audio16k.wav
i=0; while IFS= read -r line; do i=$((i+1)); n=$(printf "%02d" $i); espeak-ng -v es-419 -s 165 -w tts/$n.wav "$line" </dev/null >/dev/null 2>&1; ffmpeg -nostdin -y -v error -i tts/$n.wav -ac 1 -ar 16000 tts16/$n.wav; done < guion.txt
python3 - <<'PY'
import wave,glob
t=0.0; b=[0.0]; parts=[]
for p in sorted(glob.glob("tts16/*.wav")):
    w=wave.open(p); d=w.getnframes()/w.getframerate(); w.close(); t+=d; b.append(round(t,3)); parts.append(p)
open("bounds.txt","w").write("\n".join(str(x) for x in b))
open("concat.txt","w").write("".join(f"file '{p}'\n" for p in parts))
PY
ffmpeg -nostdin -y -v error -f concat -safe 0 -i concat.txt -c copy synth16k.wav
python3 align.py audio16k.wav synth16k.wav bounds.txt guion.txt captions.dtw.json > align.log 2>&1
python3 retime2.py > retime.log 2>&1
python3 cut.py > cut.log 2>&1
ffmpeg -nostdin -y -v error -i orig.mov -filter_complex_script cut.filter -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 16 -g $FPS -keyint_min $FPS -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -c:a aac -b:a 192k public/input-video.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 public/input-video.mp4 > cutdur.txt
ffmpeg -nostdin -y -v error -i public/input-video.mp4 -vf "select='not(mod(n,125))',scale=270:480,drawbox=0:0:270:63:red@0.35:fill,drawbox=0:150:270:1:yellow@1:fill,drawbox=0:160:270:1:yellow@1:fill,tile=6x2" -frames:v 1 contact.jpg
echo "PREP DONE $DIR fps=$FPS cut=$(cat cutdur.txt)"
