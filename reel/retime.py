#!/usr/bin/env python3
"""Re-anchor fragment timings to the measured audio pauses (silencedetect), distributing time
inside each speech run by text length (+ a small micro-pause weight for sentence punctuation).
Speech-rate across runs is ~16 chars/s, which is why this beats frame-level DTW drift here."""
import json, shutil

lines = [l.rstrip("\n") for l in open("guion.txt", encoding="utf-8") if l.strip()]
assert len(lines) == 35

# (run_start, run_end, fragment indices 1-based) — runs come from silencedetect -32dB/0.35s
RUNS = [
    (0.00,  2.16,  [1]),
    (2.94,  10.92, [2, 3, 4, 5]),
    (11.43, 28.41, [6, 7, 8, 9, 10, 11, 12, 13, 14]),
    (29.18, 31.39, [15]),
    (31.75, 44.65, [16, 17, 18, 19, 20, 21, 22]),
    (45.06, 50.76, [23, 24, 25]),
    (51.14, 52.95, [26]),
    (53.40, 55.07, [27]),
    (55.49, 68.09, [28, 29, 30, 31, 32, 33]),
    (68.53, 73.54, [34, 35]),
]

def weight(t):
    w = len(t)
    if t.endswith((".", "?", "!", '".')): w += 4     # sentence end: micro-pause
    elif t.endswith((",", ":")): w += 2
    return w

frags = []
for st, en, idx in RUNS:
    ws = [weight(lines[i - 1]) for i in idx]; tot = sum(ws)
    t = st
    for i, w in zip(idx, ws):
        d = (en - st) * w / tot
        frags.append({"i": i, "start": round(t, 2), "end": round(t + d, 2), "text": lines[i - 1]})
        t += d
frags.sort(key=lambda f: f["i"])
try: shutil.copy("captions.json", "captions.dtw.json")
except FileNotFoundError: pass
json.dump(frags, open("captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
old = {f["i"]: f for f in json.load(open("captions.dtw.json", encoding="utf-8"))} if True else {}
for f in frags:
    o = old.get(f["i"]); delta = (f["start"] - o["start"]) if o else 0
    print(f'{f["i"]:2d} {f["start"]:6.2f}-{f["end"]:6.2f}  Δinicio {delta:+.2f}  {f["text"][:48]}')
