#!/usr/bin/env python3
"""Reanclaje suave: parte del DTW y pega una frontera a una pausa real de silencedetect
solo si el punto medio de la pausa cae a menos de TOL. Donde no hay pausa cerca, manda el DTW.
Evita el defecto de retime2.py aquí: con runs de habla muy cortos repartía frases entre ellos
y dejaba líneas de medio segundo."""
import json, re, subprocess

TOL = 0.45
frs = json.load(open("captions.dtw.json", encoding="utf-8"))
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", "audio16k.wav",
                      "-af", "silencedetect=noise=-33dB:d=0.25", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
pauses = list(zip(ss, se))

KEEP = 0.70   # una frase no puede perder más del 30% de lo que midió el DTW
MIN = 0.55    # ni bajar de esto en absoluto

orig = [f["end"] - f["start"] for f in frs]
snapped = 0
for i in range(len(frs) - 1):
    b = frs[i]["end"]
    best = min(pauses, key=lambda p: abs((p[0] + p[1]) / 2 - b))
    if abs((best[0] + best[1]) / 2 - b) > TOL:
        continue
    a, c = best[0] - frs[i]["start"], frs[i + 1]["end"] - best[1]
    if a < max(KEEP * orig[i], MIN) or c < max(KEEP * orig[i + 1], MIN):
        continue   # el ajuste dejaría la línea ilegible: manda el DTW
    frs[i]["end"], frs[i + 1]["start"] = round(best[0], 2), round(best[1], 2)
    snapped += 1

for f in frs:
    f["start"], f["end"] = round(f["start"], 2), round(f["end"], 2)
json.dump(frs, open("captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{snapped}/{len(frs) - 1} fronteras pegadas a una pausa real")
for f in frs:
    d = f["end"] - f["start"]
    print(f"{f['start']:6.2f}-{f['end']:6.2f} {d:4.1f}s {len(f['text'])/d:5.1f} car/s  {f['text'][:48]}")
