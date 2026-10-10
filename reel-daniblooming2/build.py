#!/usr/bin/env python3
"""daniblooming — reel 9:16: los beneficios del journaling.

Mismo design system que el reel 1 (mpsarier-ai/daniblooming) y los mismos componentes:
tarjeta de papel con hairline naranja, píldora de 99px, líneas punteadas, la flor de seis pétalos
y los blobs de color. Aquí sí rebota: back.out(1.7).

Lo que cambia es el encuadre. Este plano es al revés que el anterior: la mampara esmerilada deja
la franja de arriba muy clara (211-217) y la silla y el suelo dejan la de abajo oscura (65-92).
Así que los gráficos siguen arriba en tinta café, pero **los subtítulos van en papel**, no en tinta.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("daniblooming — beneficios del journaling", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="daniblooming")
S, E = R.S, R.E

PAPER, CREAM, CREAM_L = "#FFFAF3", "#F9E8D8", "#FDF3EA"
INK, INK_SOFT = "#3A2418", "#7A5C48"
ORANGE, PINK, ROSE = "#E97C41", "#E18C8F", "#E2B8BC"
GOLD, BLUE = "#B8AA2D", "#B9C8FF"
LINE = "rgba(233,124,65,0.30)"       # el hairline naranja de las tarjetas
LINE_SOFT = "rgba(233,124,65,0.22)"

SANS = "'Poppins', 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
SERIF = "'Alegreya', Georgia, 'Times New Roman', serif"

M = 72
BACK = "back.out(1.7)"               # el rebote del sistema
EASE = "power2.out"
WORDMARK, MONOGRAM = "brand/logo2.png", "brand/logo1.png"
WM_AR = 1596 / 824


# ---------------------------------------------------------------- piezas del sistema
def t(id_, s, x, y, size, fam=SANS, fill=INK, anchor="start", weight=400, style="normal",
      tr="0", op=1.0):
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" opacity="{op}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};font-style:{style};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def ed(id_, s, x, y, size, fill=INK, anchor="start", weight=800, op=1.0):
    """Voz editorial de la marca: Alegreya itálica. 800 para títulos y números, 500 para los sub."""
    return t(id_, s, x, y, size, SERIF, fill, anchor, weight, "italic", "-0.02em", op)


def ui(id_, s, x, y, size, fill=INK_SOFT, anchor="start", weight=300, op=1.0):
    return t(id_, s, x, y, size, SANS, fill, anchor, weight, "normal", "0", op)


def pill(cid, s, x, y, size=24, h=52, pad=28, fg=INK, grad="pg", caps=True):
    """Píldora de 99px con el degradé naranja→rosa del sistema.
    El sitio la escribe en blanco (2,8:1): a tamaño de reel no se lee, así que lleva la
    tinta café de la marca sobre el mismo degradé."""
    s = s.upper() if caps else s
    w = len(s) * size * (0.80 if caps else 0.60) + 2 * pad
    tr = "0.15em" if caps else "0"
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="url(#{grad})"/>'
            + t(f"{cid}t", s, x + w / 2, y + h / 2 + size * 0.36, size, SANS, fg, "middle", 500, "normal", tr)
            + '</g>'), w


def paper_card(cid, x, y, w, h, r=28, rot=0.0):
    """La tarjeta de la marca: papel translúcido, hairline naranja, esquinas redondeadas."""
    g = f' transform="rotate({rot} {x + w/2:.0f} {y + h/2:.0f})"' if rot else ""
    return (f'<g id="{cid}"{g}><rect id="{cid}r" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="url(#pc)" stroke="{LINE}" stroke-width="1.5"/>')


def dash(id_, d, color=ORANGE, w=2, pattern="12 12", op=0.45):
    return (f'<path id="{id_}" d="{d}" stroke="{color}" stroke-width="{w}" fill="none" '
            f'stroke-linecap="round" stroke-dasharray="{pattern}" opacity="{op}"/>')


def flower(cid, cx, cy, s=1.0, petal=ROSE, core=ORANGE, op=1.0):
    """La flor de seis pétalos del sistema (bloom-reset.html, .svg-flower): seis elipses
    rx7/ry13 giradas cada 60° y un centro naranja. Se copia, no se redibuja."""
    pet = "".join(f'<ellipse cx="0" cy="-13" rx="7" ry="13" fill="{petal}" transform="rotate({a})"/>'
                  for a in range(0, 360, 60))
    return (f'<g id="{cid}" opacity="{op}" transform="translate({cx},{cy}) scale({s})">'
            f'{pet}<circle cx="0" cy="0" r="6" fill="{core}"/></g>')


DEFS = f'''<defs>
    <linearGradient id="pg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{PINK}"/>
    </linearGradient>
    <linearGradient id="pc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PAPER}" stop-opacity="0.96"/>
      <stop offset="1" stop-color="{CREAM_L}" stop-opacity="0.94"/>
    </linearGradient>
  </defs>'''



# ================================================================= subtítulos
# Aquí el tercio bajo del plano es oscuro (65-92), así que los subtítulos van en papel.
R.card_frags = {1, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 20, 23}
R.punch = {2: "vida,", 3: "años", 8: "gigantes", 11: "levanto", 16: "empiezo", 17: "soltando",
           18: "dirección", 19: "escribí.", 21: "journaling?", 22: "claridad,", 24: "vamos,",
           25: "cabeza,", 26: "sacamos.", 27: "mano", 28: "digital.", 29: "perspectiva",
           30: "cabeza,", 31: "empezar,", 32: "sí,", 33: "priorizar", 34: "mundo",
           35: "tranquilidad.", 36: "beneficiosa.", 37: "Claridad,", 38: "regalo,",
           39: "allá", 40: "nudo", 41: "claras,", 42: "parados,", 43: "vamos,", 44: "regalo."}
R.rail()

# ================================================================= lavado de color (blobs)
R.scene("wash", 0.0, R.DUR, "transparent", f'''
  <defs>
    <radialGradient id="w1"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
    <radialGradient id="w2"><stop offset="0" stop-color="{PINK}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
    <radialGradient id="w3"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.14"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  </defs>
  <circle id="wb1" cx="70" cy="180" r="600" fill="url(#w1)"/>
  <circle id="wb2" cx="1020" cy="1500" r="560" fill="url(#w2)"/>
  <circle id="wb3" cx="980" cy="480" r="400" fill="url(#w3)"/>''')
for sel, dx, dy, dur in [("#wb1", 44, 32, 12), ("#wb2", -36, -44, 14), ("#wb3", -28, 50, 10)]:
    R.raw(f'  tl.to("{sel}", {{ x: {dx}, y: {dy}, duration: {dur}, ease: "sine.inOut", '
          f'yoyo: true, repeat: 8 }}, 0.00);')

# ================================================================= bug de marca
R.clip("bug", 0.40, 82.60, f'<image id="bugw" href="{WORDMARK}" x="{M}" y="196" '
       f'width="{44 * WM_AR:.0f}" height="44" opacity="0.88"/>', hold=True)
R.fade("#bug-in", 82.30, 0.0, 0.3)
R.hidden("#bug-in", 82.60)


# ================================================================= 1 · HOOK
R.card("hook", 0.0, 3.46, [
    ("a", "desde muy chiquita", 56, 0, 266, "center", "drop", 0.86, 0.10),
    ("b", "escribo", 170, 0, 352, "center", "scale", 1.0, 0.48)])
R.punch_cam(0.30)
R.clip("orn", 0.90, 3.46, flower("fl1", 168, 560, 2.0) + flower("fl2", 918, 300, 1.5, op=0.85))
R.pop("#fl1, #fl2", 1.05, 0.5, 0.18)
R.raw('  tl.to("#fl1", { y: -20, rotation: 9, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: 1 }, 1.30);')
R.raw('  tl.to("#fl2", { y: 16, rotation: -11, duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, 1.60);')

R.card("antes", 9.20, 11.56, [
    ("a", "un antes", 92, 0, 262, "center", "drop", 0.88, 9.28),
    ("b", "y un después", 118, 0, 390, "center", "scale", 1.0, 9.72)])
R.punch_cam(9.74, 1.04)


# ================================================================= 2 · ME PERMITE
ROWS = [("aterrizar ideas", 11.70), ("estar más clara", 13.40), ("desenredar nudos mentales", 15.60)]
rows_svg = []
for k, (txt, _) in enumerate(ROWS):
    ry = 326 + k * 96
    rows_svg.append(f'<g id="mp{k}"><rect x="170" y="{ry}" width="740" height="78" rx="22" '
                    f'fill="url(#pc)" stroke="{LINE}" stroke-width="1.5"/>'
                    + flower(f"mpf{k}", 214, ry + 39, 0.85)
                    + ed(f"mpt{k}", txt, 252, ry + 52, 44, INK, "start", 500) + '</g>')
R.clip("permite", 11.60, 18.14, DEFS + ed("mp-h", "me permite", 170, 282, 70, INK) + "".join(rows_svg))
R.hidden("#mp0, #mp1, #mp2", 11.60)
R.fromTo("#mp-h", "autoAlpha:0, y:20", "autoAlpha:1, y:0", 11.66, 0.45, BACK)
for k, (_, at) in enumerate(ROWS):
    R.show(f"#mp{k}", at)
    R.fromTo(f"#mp{k}", "autoAlpha:0, x:-28, scale:0.94, transformOrigin:'0% 50%'",
             "autoAlpha:1, x:0, scale:1", at, 0.45, BACK)

# gigante -> pequeña
R.clip("tam", 18.26, 21.00, DEFS + f'''
  <circle id="tg-b" cx="540" cy="424" r="168" stroke="{ORANGE}" stroke-width="3" fill="none"
     stroke-dasharray="16 14" opacity="0.65"/>
  <circle id="tg-s" cx="540" cy="424" r="38" fill="{ORANGE}"/>
  {ed("tg-l1", "gigantes", 540, 284, 50, INK, "middle", 500)}
  {ed("tg-l2", "pequeñas", 540, 638, 50, INK, "middle", 500)}''')
R.hidden("#tg-s, #tg-l2", 18.26)
R.fromTo("#tg-b", "scale:0.3, autoAlpha:0, transformOrigin:'540px 424px'",
         "scale:1, autoAlpha:1", 18.34, 0.5, BACK)
R.fromTo("#tg-l1", "autoAlpha:0, y:-12", "autoAlpha:1, y:0", 18.44, 0.35)
R.to("#tg-b", "scale:0.24, autoAlpha:0.25, transformOrigin:'540px 424px'", 19.50, 0.6, "power3.inOut")
R.show("#tg-s", 19.90)
R.pop("#tg-s", 19.90, 0.45)
R.show("#tg-l2", 20.02)
R.fromTo("#tg-l2", "autoAlpha:0, y:12", "autoAlpha:1, y:0", 20.02, 0.35)

# dos píldoras: por dónde empezar · cómo me siento
pa, _ = pill("sb0", "por dónde empezar", 0, 330, 28, 62)
pb, _ = pill("sb1", "cómo me siento", 0, 416, 28, 62)
for cid, s, y in [("sb0", "por dónde empezar", 330), ("sb1", "cómo me siento", 416)]:
    pass
sb0, w0 = pill("sb0", "por dónde empezar", 0, 330, 28, 62)
sb1, w1 = pill("sb1", "cómo me siento", 0, 416, 28, 62)
sb0 = sb0.replace('<rect x="0"', f'<rect x="{(1080 - w0) / 2:.0f}"').replace(
    f'x="{w0 / 2}"', f'x="{(1080 - w0) / 2 + w0 / 2:.0f}"')
sb1 = sb1.replace('<rect x="0"', f'<rect x="{(1080 - w1) / 2:.0f}"').replace(
    f'x="{w1 / 2}"', f'x="{(1080 - w1) / 2 + w1 / 2:.0f}"')
R.clip("saber", 21.36, 24.30, DEFS + sb0 + sb1)
R.hidden("#sb1", 21.36)
R.fromTo("#sb0", "autoAlpha:0, scale:0.72, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", 21.44, 0.45, BACK)
R.show("#sb1", 22.80)
R.fromTo("#sb1", "autoAlpha:0, scale:0.72, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", 22.80, 0.45, BACK)


# ================================================================= 3 · EL RITUAL
R.card("ritual", 26.90, 30.86, [
    ("a", "el journaling", 74, 0, 268, "center", "drop", 0.88, 26.98),
    ("b", "es mi momento", 112, 0, 384, "center", "scale", 1.0, 27.40)])
R.punch_cam(27.42, 1.035)

RIT = [("mi rutina", 30.96), ("mi ritual sagrado", 32.72), ("mi momento de presencia", 33.90)]
rit_svg = []
for k, (txt, _) in enumerate(RIT):
    p, w = pill(f"rp{k}", txt, 0, 272 + k * 92, 30, 66)
    x = (1080 - w) / 2
    p = p.replace('<rect x="0"', f'<rect x="{x:.0f}"').replace(f'x="{w / 2}"', f'x="{x + w / 2:.0f}"')
    rit_svg.append(p)
R.clip("rit", 30.90, 35.22, DEFS + "".join(rit_svg))
R.hidden("#rp0, #rp1, #rp2", 30.90)
for k, (_, at) in enumerate(RIT):
    R.show(f"#rp{k}", at)
    R.fromTo(f"#rp{k}", "autoAlpha:0, scale:0.7, y:16, transformOrigin:'50% 50%'",
             "autoAlpha:1, scale:1, y:0", at, 0.45, BACK)

# el nudo mental que se suelta y se vuelve una línea
KNOT = ("M300 400 C360 320, 430 470, 500 380 S610 300, 660 410 S560 520, 470 460 "
        "S330 500, 380 400 S520 330, 600 360 S720 430, 780 390")
R.clip("nudo", 35.26, 39.24, DEFS
       + f'<path id="nd-k" d="{KNOT}" stroke="{INK}" stroke-width="4" fill="none" '
         f'stroke-linecap="round" opacity="0.85"/>'
       + dash("nd-l", "M250 420 L844 420", ORANGE, 5, "16 14", 0.85)
       + flower("nd-f", 894, 420, 3.0))
R.hidden("#nd-l, #nd-f", 35.26)
R.draw("#nd-k", 1500, 35.34, 1.25, "power1.inOut")
R.fade("#nd-k", 37.30, 0.0, 0.45)
R.show("#nd-l", 37.52)
R.draw("#nd-l", 594, 37.52, 0.7)
R.pop("#nd-f", 38.28, 0.5)
R.raw('  tl.to("#nd-f", { rotation: 14, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1 }, 38.70);')


# ================================================================= 4 · LA PREGUNTA
# El silencio de 2,3 s antes de la pregunta es el único hueco grande del reel: entra la tarjeta ahí.
R.clip("preg", 42.30, 47.28, DEFS
       + ed("pq-a", "¿cuál es", 540, 300, 96, INK, "middle")
       + ed("pq-b", "la diferencia?", 540, 416, 96, INK, "middle")
       + dash("pq-d", "M300 464 L780 464", ORANGE, 3, "12 12", 0.5)
       + ed("pq-c", "entre una persona que hace journaling", 540, 540, 40, INK_SOFT, "middle", 500))
R.hidden("#pq-d, #pq-c", 42.30)
R.fromTo("#pq-a", "autoAlpha:0, y:24", "autoAlpha:1, y:0", 42.40, 0.5, BACK)
R.fromTo("#pq-b", "autoAlpha:0, y:24", "autoAlpha:1, y:0", 42.70, 0.5, BACK)
R.show("#pq-d", 43.20)
R.draw("#pq-d", 480, 43.20, 0.6)
R.show("#pq-c", 44.50)
R.fromTo("#pq-c", "autoAlpha:0, y:14", "autoAlpha:1, y:0", 44.50, 0.45, EASE)
R.punch_cam(42.42, 1.04)


# ================================================================= 5 · CLARIDAD · CERTEZA · LUCES
R.clip("tres", 52.40, 57.30, DEFS
       + ed("t3-a", "claridad", 170, 300, 112, INK)
       + ed("t3-b", "certeza", 300, 420, 86, INK, "start", 700)
       + ed("t3-c", "luces", 430, 522, 68, INK, "start", 700))
R.hidden("#t3-b, #t3-c", 52.40)
R.fromTo("#t3-a", "autoAlpha:0, x:-30, rotation:-2", "autoAlpha:1, x:0, rotation:0", 52.48, 0.5, BACK)
R.show("#t3-b", 53.95)
R.fromTo("#t3-b", "autoAlpha:0, x:-26, rotation:1.5", "autoAlpha:1, x:0, rotation:0", 53.95, 0.5, BACK)
R.show("#t3-c", 54.95)
R.fromTo("#t3-c", "autoAlpha:0, x:-22, rotation:-1.5", "autoAlpha:1, x:0, rotation:0", 54.95, 0.5, BACK)

# todo en la cabeza -> lo sacamos
scribs = "".join(f'<rect id="sc{k}" x="{266 + (k % 3) * 190}" y="{306 + (k // 3) * 56}" '
                 f'width="{[150, 118, 164, 132, 150, 104][k]}" height="7" rx="3.5" '
                 f'fill="{INK_SOFT}" opacity="0.55"/>' for k in range(6))
R.clip("saca", 57.44, 61.40, DEFS
       + f'<rect id="sa-c" x="226" y="256" width="628" height="214" rx="26" fill="url(#pc)" '
         f'stroke="{LINE}" stroke-width="1.5"/>' + scribs)
R.fromTo("#sa-c", "autoAlpha:0, scale:0.94, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", 57.52, 0.45, BACK)
R.raw('  tl.fromTo(gsap.utils.toArray("#saca rect[id^=sc]"), { autoAlpha: 0, x: -14 }, '
      '{ autoAlpha: 0.55, x: 0, duration: 0.3, ease: "power2.out", stagger: 0.09 }, 57.70);')
R.raw('  tl.to(gsap.utils.toArray("#saca rect[id^=sc]"), { y: 300, autoAlpha: 0, duration: 0.7, '
      'ease: "power2.in", stagger: 0.07 }, 59.80);')
R.to("#sa-c", "autoAlpha:0.35", 60.60, 0.5)


# ================================================================= 6 · A MANO vs DIGITAL
def vs_card(cid, x, label, strong):
    st = LINE if strong else "rgba(122,92,72,0.22)"
    op = "1" if strong else "0.72"
    g = (f'<g id="{cid}" opacity="{op}"><rect x="{x}" y="256" width="392" height="206" rx="26" '
         f'fill="url(#pc)" stroke="{st}" stroke-width="1.5"/>'
         + ed(f"{cid}t", label, x + 196, 384, 56, INK if strong else INK_SOFT, "middle", 800 if strong else 500))
    if strong:
        g += flower(f"{cid}f", x + 196, 310, 1.1)
    return g + '</g>'


R.clip("vs", 61.56, 75.90, DEFS
       + vs_card("vs-a", 94, "a mano", True)
       + vs_card("vs-b", 594, "digital", False))
R.hidden("#vs-b", 61.56)
R.fromTo("#vs-a", "autoAlpha:0, y:26, scale:0.94, transformOrigin:'50% 50%'",
         "autoAlpha:1, y:0, scale:1", 61.64, 0.5, BACK)
R.show("#vs-b", 64.20)
R.fromTo("#vs-b", "autoAlpha:0.72, y:26, scale:0.94, transformOrigin:'50% 50%'",
         "autoAlpha:0.72, y:0, scale:1", 64.20, 0.5, BACK)
# perspectiva: las dos fichas se abren en ángulo
R.to("#vs-a", "rotation:-3.5, transformOrigin:'50% 100%'", 68.00, 0.8, "power2.out")
R.to("#vs-b", "rotation:3.5, transformOrigin:'50% 100%'", 68.10, 0.8, "power2.out")

sy0, wy0 = pill("ys0", "qué sí", 230, 520, 30, 66)
yn = (f'<g id="ys1"><rect x="620" y="520" width="{wy0:.0f}" height="66" rx="33" fill="none" '
      f'stroke="{INK_SOFT}" stroke-width="2" opacity="0.6"/>'
      + t("ys1t", "QUÉ NO", 620 + wy0 / 2, 562, 30, SANS, INK_SOFT, "middle", 500, "normal", "0.15em") + '</g>')
R.clip("sino", 72.90, 75.90, DEFS + sy0 + yn)
R.hidden("#ys1", 72.90)
R.fromTo("#ys0", "autoAlpha:0, scale:0.7, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", 72.98, 0.42, BACK)
R.show("#ys1", 73.50)
R.fromTo("#ys1", "autoAlpha:0, scale:0.7, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", 73.50, 0.42, BACK)


# ================================================================= 7 · TRANQUILIDAD
R.clip("flor", 76.40, 82.30, DEFS
       + flower("tq0", 326, 392, 3.6) + flower("tq1", 540, 348, 4.4) + flower("tq2", 754, 392, 3.6))
R.hidden("#tq0, #tq1, #tq2", 76.40)
for k, at in enumerate([76.60, 77.50, 78.40]):
    R.show(f"#tq{k}", at)
    R.fromTo(f"#tq{k}", "autoAlpha:0, scale:0.2, rotation:-40, transformOrigin:'50% 50%'",
             "autoAlpha:1, scale:1, rotation:0", at, 0.7, BACK)
R.raw('  tl.to("#tq1", { y: -16, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 1 }, 79.40);')
R.raw('  tl.to("#tq0, #tq2", { y: 14, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: 1 }, 79.70);')


# ================================================================= 8 · EL JOURNAL
JX, JY, JW, JH = 84, 196, 912, 318
tp, tpw = pill("jo-tag", "en el link de mi bio", JX + 48, JY + 34)
R.clip("journal", 82.95, 92.60, DEFS
       + paper_card("jo-c", JX, JY, JW, JH, 28, -0.7) + "</g>"
       + tp
       + ed("jo-t", "Journal Claridad", JX + 48, JY + 156, 76, INK)
       + dash("jo-d", f"M{JX + 48} {JY + 188} L{JX + JW - 48} {JY + 188}", ORANGE, 2, "10 10", 0.40)
       + ed("jo-s", "una guía de preguntas para cada noche", JX + 48, JY + 250, 42, INK_SOFT, "start", 500),
       hold=True)
R.hidden("#jo-tag, #jo-t, #jo-d, #jo-s", 82.95)
R.fromTo("#jo-c", "autoAlpha:0, y:34, scale:0.96, transformOrigin:'50% 50%'",
         "autoAlpha:1, y:0, scale:1", 83.02, 0.55, BACK)
R.show("#jo-tag", 83.32)
R.fromTo("#jo-tag", "autoAlpha:0, scale:0.72, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1", 83.32, 0.45, BACK)
R.show("#jo-t", 83.62)
R.fromTo("#jo-t", "autoAlpha:0, y:22", "autoAlpha:1, y:0", 83.62, 0.5, BACK)
R.show("#jo-d", 84.10)
R.draw("#jo-d", JW - 96, 84.10, 0.5)
R.show("#jo-s", 84.70)
R.fromTo("#jo-s", "autoAlpha:0, y:16", "autoAlpha:1, y:0", 84.70, 0.45, EASE)
R.punch_cam(83.04, 1.04)
R.fade("#journal-in", 92.24, 0.0, 0.36)
R.hidden("#journal-in", 92.60)


# ================================================================= 9 · CIERRE sobre el plano
LW = 452
R.clip("fin", 96.20, R.DUR, DEFS
       + flower("fi-f", 540, 242, 2.3)
       + f'<image id="fi-w" href="{WORDMARK}" x="{(1080 - LW) / 2:.0f}" y="302" '
         f'width="{LW}" height="{LW / WM_AR:.0f}" opacity="0.92"/>'
       + ui("fi-h", "@daniblooming", 540, 596, 36, INK, "middle", 500), hold=True)
R.hidden("#fi-f, #fi-w, #fi-h", 96.20)
R.show("#fi-w", 96.30)
R.fromTo("#fi-w", "autoAlpha:0, y:20, scale:0.94", "autoAlpha:1, y:0, scale:1", 96.30, 0.6, BACK)
R.show("#fi-f", 96.60)
R.pop("#fi-f", 96.60, 0.5)
R.show("#fi-h", 96.90)
R.fromTo("#fi-h", "autoAlpha:0, y:12", "autoAlpha:1, y:0", 96.90, 0.45, EASE)
R.slow_push(96.25, 2.3, 1.045)
R.fadeout(0.45)


# ================================================================= estilos
R.extra_css = f'''
      /* El cuaderno crema cruza las bandas de 1392 y 1440; en 1500 el plano se mantiene oscuro
         en todo el video, así que ahí el papel se lee sin caja y sin sombra. Las dos frases
         más largas van partidas en el guion para que ninguna llegue a tres renglones. */
      .rail {{ top: 1500px; }}
      .rail .line {{ max-width: 880px; color: {PAPER}; text-shadow: none;
        font-weight: 500; font-size: 50px; line-height: 1.20; letter-spacing: 0.005em; }}
      .rail .w.hot.pill {{ padding: 0.04em 0.30em 0.10em; border-radius: 99px; }}
      /* Statements: Alegreya itálica sobre la mampara clara, en tinta café. */
      .card {{ height: 920px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-family: {SERIF}; font-style: italic; font-weight: 800; letter-spacing: -0.02em; }}
      #hook-a {{ font-family: {SANS}; font-style: normal; font-weight: 300;
        color: {INK_SOFT}; letter-spacing: 0; }}
      #antes-a, #ritual-a {{ font-weight: 500; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
