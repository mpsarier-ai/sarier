#!/bin/bash
# snap.sh DIR t1,t2,... — snapshot frames with safe-zone guides and tile them into snapshots/sheet.jpg
set -e
SP=/tmp/claude-0/-home-user-sarier/08997238-b1ce-5d5f-8d4f-63bf23144449/scratchpad
cd "$SP/$1"; rm -rf snapshots
node /home/user/heygen-com/hyperframes/packages/cli/bin/hyperframes.mjs snapshot --at "$2" --no-end -o snapshots >/dev/null 2>&1
cd snapshots
for f in frame-*.png; do ffmpeg -nostdin -y -v error -i "$f" -vf "drawbox=0:0:1080:250:red@0.25:fill,drawbox=0:1600:1080:320:red@0.25:fill,drawbox=0:520:1080:2:yellow@1:fill,scale=300:533" "g-${f%.png}.jpg"; done
n=$(ls g-*.jpg | wc -l); cols=6; rows=$(( (n + cols - 1) / cols ))
ffmpeg -nostdin -y -v error -pattern_type glob -i "g-*.jpg" -vf "tile=${cols}x${rows}" sheet.jpg
echo "SNAP $1 $n frames"
