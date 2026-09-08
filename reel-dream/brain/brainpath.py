import math
def bumpy(pts, k=0.62, close=True):
    d = f"M{pts[0][0]} {pts[0][1]}"
    seq = pts[1:] + ([pts[0]] if close else [])
    prev = pts[0]
    for x, y in seq:
        c = math.hypot(x - prev[0], y - prev[1]); r = round(c * k, 1)
        d += f" A{r} {r} 0 0 1 {x} {y}"; prev = (x, y)
    return d + (" Z" if close else "")
# side view, front to the left · cerebrum with lobe bumps
CEREBRUM = bumpy([(330,262),(352,182),(418,118),(505,84),(600,80),(685,104),(748,156),(772,228),(748,300),(690,345),
                  (600,362),(505,366),(422,350),(360,318)])
CEREBELLUM = bumpy([(690,360),(742,350),(778,384),(756,428),(702,434),(668,402)], k=0.7)
STEM = "M604 366 C598 398 604 428 618 452 M652 370 C656 402 646 430 636 452"
FISSURE = "M372 306 C440 272 510 292 580 270 C610 262 636 250 660 234"   # lateral (sylvian) fissure
GYRI = ["M400 190 C425 215 455 170 480 200", "M520 130 C548 160 582 118 612 148", "M655 190 C680 220 705 178 730 208",
        "M430 228 C458 254 490 212 518 238", "M560 312 C588 338 620 300 648 326", "M690 266 C712 292 738 256 752 286"]
if __name__ == "__main__":
    W = 'stroke="#1D1D1F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="520" viewBox="0 0 1080 520"><rect width="1080" height="520" fill="#F5F5F7"/>'
    svg += f'<path d="{CEREBRUM}" {W}/><path d="{CEREBELLUM}" {W}/><path d="{STEM}" {W}/><path d="{FISSURE}" {W}/>'
    svg += "".join(f'<path d="{g}" {W}/>' for g in GYRI) + "</svg>"
    open("brain.svg", "w").write(svg)
