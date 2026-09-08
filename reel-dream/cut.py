#!/usr/bin/env python3
"""Cut the pauses: speech runs from silencedetect (+pads) become the kept segments.
Writes cuts.json, captions.cut.json (remapped) and re-encodes the source into public/input-video.mp4."""
import json, subprocess, re, sys
PRE, POST, MINGAP = 0.07, 0.12, 0.10
out = subprocess.run(["ffmpeg","-hide_banner","-i","audio16k.wav","-af","silencedetect=noise=-28dB:d=0.22","-f","null","-"],capture_output=True,text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
total = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","orig.mov"],capture_output=True,text=True).stdout)
runs=[]; cur=0.0
for a,b in zip(ss,se):
    if a-cur>0.2: runs.append([cur,a])
    cur=b
if total-cur>0.2: runs.append([cur,total])
segs=[]
for a,b in runs:
    a=max(0.0,a-PRE); b=min(total,b+POST)
    if segs and a-segs[-1][1] < MINGAP: segs[-1][1]=b
    else: segs.append([a,b])
segs[-1][1]=min(total, segs[-1][1]+0.6)   # hold the closing statement
kept=sum(b-a for a,b in segs)
print(f"total {total:.2f}s → kept {kept:.2f}s (removed {total-kept:.2f}s in {len(segs)-1} cuts)", file=sys.stderr)
for a,b in segs: print(f"  keep {a:6.2f}-{b:6.2f}", file=sys.stderr)
def remap(t):
    off=0.0
    for a,b in segs:
        if t<a: return round(off,2)
        if t<=b: return round(off+(t-a),2)
        off+=b-a
    return round(off,2)
caps=json.load(open("captions.json",encoding="utf-8"))
new=[dict(f, start=remap(f["start"]), end=remap(f["end"])) for f in caps]
json.dump({"segments":segs,"total":round(kept,2)},open("cuts.json","w"),indent=1)
json.dump(new,open("captions.cut.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
# ffmpeg: trim each segment (video+audio), tiny audio fades to avoid clicks, concat
fc=[]
for k,(a,b) in enumerate(segs):
    fc.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{k}];"
              f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.012:.3f}:d=0.012[a{k}]")
fc.append("".join(f"[v{k}][a{k}]" for k in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=1[v][a]")
open("cut.filter","w").write(";".join(fc))
