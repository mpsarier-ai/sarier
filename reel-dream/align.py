#!/usr/bin/env python3
"""Forced alignment of a known script to real audio, pure numpy.
Same idea as aeneas: TTS the text, MFCC both signals, DTW, map fragment boundaries."""
import wave, sys, json
import numpy as np

SR = 16000
WIN = int(0.025 * SR)   # 25 ms
HOP = int(0.020 * SR)   # 20 ms  -> 50 fps
NFFT = 512
NMEL = 26
NCEP = 13

def load(path):
    with wave.open(path, 'rb') as w:
        assert w.getframerate() == SR and w.getnchannels() == 1, path
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    return x

def hz2mel(f): return 2595 * np.log10(1 + f / 700.0)
def mel2hz(m): return 700 * (10 ** (m / 2595.0) - 1)

def mel_fb():
    pts = mel2hz(np.linspace(hz2mel(0), hz2mel(SR / 2), NMEL + 2))
    bins = np.floor((NFFT + 1) * pts / SR).astype(int)
    fb = np.zeros((NMEL, NFFT // 2 + 1))
    for m in range(1, NMEL + 1):
        a, b, c = bins[m - 1], bins[m], bins[m + 1]
        for k in range(a, b): fb[m - 1, k] = (k - a) / max(b - a, 1)
        for k in range(b, c): fb[m - 1, k] = (c - k) / max(c - b, 1)
    return fb

def dct_mat():
    n = np.arange(NMEL)
    return np.array([np.cos(np.pi * k * (2 * n + 1) / (2 * NMEL)) for k in range(NCEP)])

FB, DCT = mel_fb(), dct_mat()

def mfcc(x):
    x = np.append(x[0], x[1:] - 0.97 * x[:-1])          # pre-emphasis
    n = 1 + max(0, (len(x) - WIN) // HOP)
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n)[:, None]
    frames = x[idx] * np.hamming(WIN)
    pw = (np.abs(np.fft.rfft(frames, NFFT)) ** 2) / NFFT
    e = np.log(pw @ FB.T + 1e-10)
    c = e @ DCT.T
    # append log-energy and deltas
    le = np.log(pw.sum(1) + 1e-10)[:, None]
    f = np.hstack([c, le])
    d = np.gradient(f, axis=0)
    f = np.hstack([f, d])
    return (f - f.mean(0)) / (f.std(0) + 1e-8)          # CMVN

def dtw(A, B, band):
    """A: real (n x d), B: synth (m x d). Returns path as list of (i,j)."""
    n, m = len(A), len(B)
    INF = 1e18
    D = np.full((n + 1, m + 1), INF)
    D[0, 0] = 0.0
    slope = m / n
    # cosine-like distance via normalized vectors
    An = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-8)
    Bn = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-8)
    for i in range(1, n + 1):
        c = int(i * slope)
        lo, hi = max(1, c - band), min(m, c + band)
        cost = 1.0 - Bn[lo - 1:hi] @ An[i - 1]
        prev = D[i - 1]
        row = D[i]
        # diagonal & vertical (vectorized), then horizontal scan
        best = np.minimum(prev[lo - 1:hi], prev[lo:hi + 1])
        row[lo:hi + 1] = cost + best
        for j in range(lo, hi + 1):
            v = row[j - 1] + cost[j - lo]
            if v < row[j]: row[j] = v
    # backtrack
    i, j = n, m
    path = []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        a, b, c = D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]
        if a <= b and a <= c: i, j = i - 1, j - 1
        elif b <= c: i -= 1
        else: j -= 1
    path.reverse()
    return path

def main(real_wav, synth_wav, bounds_txt, script_txt, out_json):
    real, synth = load(real_wav), load(synth_wav)
    A, B = mfcc(real), mfcc(synth)
    print(f"frames real={len(A)} synth={len(B)}", file=sys.stderr)
    band = int(12.0 / 0.020)    # ±12 s
    path = dtw(A, B, band)
    # map each synth frame -> first real frame on the path
    s2r = {}
    for i, j in path:
        s2r.setdefault(j, i)
    bounds = [float(l) for l in open(bounds_txt).read().split()]
    lines = [l.rstrip('\n') for l in open(script_txt, encoding='utf-8') if l.strip()]
    assert len(lines) == len(bounds) - 1, (len(lines), len(bounds))
    def r_time(t_synth):
        j = min(int(t_synth / 0.020), len(B) - 1)
        while j not in s2r and j > 0: j -= 1
        return s2r.get(j, 0) * 0.020
    frags = []
    for k, text in enumerate(lines):
        st, en = r_time(bounds[k]), r_time(bounds[k + 1])
        frags.append({"i": k + 1, "start": round(st, 2), "end": round(en, 2), "text": text})
    # enforce monotonic, min duration
    for k in range(1, len(frags)):
        if frags[k]["start"] < frags[k - 1]["end"]:
            frags[k]["start"] = frags[k - 1]["end"]
    json.dump(frags, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for f in frags:
        print(f'{f["start"]:6.2f} → {f["end"]:6.2f}  {f["end"]-f["start"]:4.1f}s  {f["text"]}')

if __name__ == '__main__':
    main(*sys.argv[1:6])
