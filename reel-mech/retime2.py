#!/usr/bin/env python3
"""Auto re-anchor: speech runs from silencedetect; each fragment joins the run holding its DTW midpoint;
time inside a run is split by text length (+ micro-pause weight on punctuation)."""
import json, subprocess, re, sys
dtw = json.load(open("captions.dtw.json", encoding="utf-8"))
out = subprocess.run(["ffmpeg","-hide_banner","-i","audio16k.wav","-af","silencedetect=noise=-32dB:d=0.35","-f","null","-"],capture_output=True,text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
total = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","audio16k.wav"],capture_output=True,text=True).stdout)
runs=[]; cur=0.0
for a,b in zip(ss,se):
    if a-cur>0.25: runs.append([cur,a])
    cur=b
if total-cur>0.25: runs.append([cur,total])
def weight(t):
    w=len(t)
    if t.endswith((".","?","!",";")): w+=4
    elif t.endswith((",",":")): w+=2
    return w
assign={i:[] for i in range(len(runs))}
for f in dtw:
    mid=(f["start"]+f["end"])/2
    k=min(range(len(runs)), key=lambda i: 0 if runs[i][0]<=mid<=runs[i][1] else min(abs(mid-runs[i][0]),abs(mid-runs[i][1])))
    assign[k].append(f)
frags=[]
for k,(st,en) in enumerate(runs):
    fs=assign[k]
    if not fs: continue
    ws=[weight(f["text"]) for f in fs]; tot=sum(ws); t=st
    for f,w in zip(fs,ws):
        d=(en-st)*w/tot; frags.append({"i":f["i"],"start":round(t,2),"end":round(t+d,2),"text":f["text"]}); t+=d
frags.sort(key=lambda f:f["i"])
json.dump(frags,open("captions.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
old={f["i"]:f for f in dtw}
for f in frags: print(f'{f["i"]:2d} {f["start"]:6.2f}-{f["end"]:6.2f} Δ{f["start"]-old[f["i"]]["start"]:+.2f}  {f["text"][:46]}')
print("runs:",[(round(a,2),round(b,2)) for a,b in runs], file=sys.stderr)
