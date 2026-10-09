#!/usr/bin/env python3
"""daniblooming — reel 9:16 sobre el video original: tres cosas que cambiaron desde que escribe.

El sistema visual es el de daniblooming (mpsarier-ai/daniblooming): papel cálido, tinta café,
naranja como única tinta de acción, Alegreya itálica para lo editorial y Poppins ligera para la
interfaz. Los componentes son los de la marca y no otros:

  · tarjeta de papel translúcida, borde naranja a 1px y esquinas de 24-28px, ligeramente girada
  · píldora de 99px (degradé naranja→rosa, texto papel) para las etiquetas
  · líneas punteadas naranja al 25% como separador y como conector
  · la flor de seis pétalos (rose, centro naranja) — el único ornamento de la marca
  · blobs de color desenfocados como fondo; aquí, un lavado suave sobre el plano
  · aquí SÍ rebota: cubic-bezier(.34,1.56,.64,1) ≈ back.out(1.7)

El plano es único y muy luminoso: la cortina deja libre toda la franja y<540 y el puf deja libre
y>1400, así que los gráficos viven arriba y los subtítulos abajo. Ella nunca queda tapada.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("daniblooming — tres cosas que cambiaron", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="daniblooming")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens (:root de la marca)
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
# Tinta café sobre el puf, que es la banda más clara del encuadre (9,7:1 de contraste).
R.card_frags = {1, 2, 3, 8, 9, 15, 18, 23, 24, 25, 26}   # estas las dice la tipografía o la tarjeta
R.ink_frags = {f["i"] for f in R.frags}
R.punch = {4: "conversaciones", 5: "mañana", 6: "igual", 7: "dicho", 10: "patrones",
           11: "misma", 12: "ocho", 13: "Ocho.", 14: "creía", 16: "excusas", 17: "debiendo",
           19: "cuaderno", 20: "mostrar", 21: "evitando", 22: "decisiones", 27: "patrones"}
R.rail()

# ================================================================= lavado de color (blobs)
# Los blobs desenfocados del sistema, aquí como gradientes radiales sobre el plano frío.
R.scene("wash", 0.0, R.DUR, "transparent", f'''
  <defs>
    <radialGradient id="w1"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
    <radialGradient id="w2"><stop offset="0" stop-color="{PINK}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
    <radialGradient id="w3"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  </defs>
  <circle id="wb1" cx="60" cy="140" r="620" fill="url(#w1)"/>
  <circle id="wb2" cx="1030" cy="1560" r="580" fill="url(#w2)"/>
  <circle id="wb3" cx="1000" cy="520" r="400" fill="url(#w3)"/>''')
for sel, dx, dy, dur in [("#wb1", 46, 34, 11), ("#wb2", -38, -46, 13), ("#wb3", -30, 52, 9)]:
    R.raw(f'  tl.to("{sel}", {{ x: {dx}, y: {dy}, duration: {dur}, ease: "sine.inOut", '
          f'yoyo: true, repeat: 6 }}, 0.00);')

# ================================================================= bug de marca
R.clip("bug", 0.35, 46.25, f'<image id="bugw" href="{WORDMARK}" x="{M}" y="196" '
       f'width="{44 * WM_AR:.0f}" height="44" opacity="0.88"/>', hold=True)
R.fade("#bug-in", 45.95, 0.0, 0.3)
R.hidden("#bug-in", 46.25)

# ================================================================= progreso 01·02·03
# El indicador de carga del sistema es una barra que se rellena, nunca un spinner.
BX, BW, BG = 1008, 52, 12
bars = "".join(f'<rect x="{BX - 3 * BW - 2 * BG + k * (BW + BG)}" y="212" width="{BW}" height="6" '
               f'rx="3" fill="{ORANGE}" opacity="0.22"/>'
               f'<rect id="pb{k}" x="{BX - 3 * BW - 2 * BG + k * (BW + BG)}" y="212" width="{BW}" '
               f'height="6" rx="3" fill="{ORANGE}"/>' for k in range(3))
R.clip("prog", 5.02, 36.40, bars, hold=True)
R.hidden("#pb0, #pb1, #pb2", 5.02)
for k, at in enumerate([5.06, 17.96, 28.18]):
    R.fromTo(f"#pb{k}", "autoAlpha:0, scaleX:0, transformOrigin:'0% 50%'",
             "autoAlpha:1, scaleX:1", at, 0.45, EASE)
R.fade("#prog-in", 36.05, 0.0, 0.35)
R.hidden("#prog-in", 36.40)


# ================================================================= 1 · HOOK
R.card("hook", 0.0, 3.06, [
    ("a", "Tres cosas", 146, 0, 272, "center", "drop", 1.0, 0.10),
    ("b", "que cambiaron", 76, 0, 436, "center", "drop", 0.92, 0.52),
    ("c", "desde que escribo todas las noches", 40, 0, 532, "center", "drop", 0.88, 1.10)])
R.punch_cam(0.28)
R.card("hook2", 3.12, 5.06, [
    ("a", "y ninguna", 96, 0, 296, "center", "scale", 1.0, 3.20),
    ("b", "es la que uno esperaría.", 54, 0, 434, "center", "drop", 0.88, 3.58)])
R.punch_cam(3.20, 1.035)

# Dos flores flotando en los márgenes de cortina, como los ornamentos del hero del sistema.
R.clip("orn", 0.70, 5.06, flower("fl1", 148, 806, 2.1) + flower("fl2", 948, 690, 1.6, op=0.85))
R.pop("#fl1, #fl2", 0.85, 0.5, 0.18)
R.raw('  tl.to("#fl1", { y: -22, rotation: 8, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: 1 }, 1.10);')
R.raw('  tl.to("#fl2", { y: 18, rotation: -10, duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, 1.40);')


# ================================================================= número de cada punto
def badge(gid, n, tag, st, en):
    p, _ = pill(f"{gid}p", tag, M + 6, 362)
    R.clip(gid, st, en, DEFS + ed(f"{gid}n", n, M, 338, 148, INK) + p)
    R.fromTo(f"#{gid}n", "autoAlpha:0, y:34", "autoAlpha:1, y:0", st + 0.08, 0.5, BACK)
    R.fromTo(f"#{gid}p", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'",
             "autoAlpha:1, scale:1", st + 0.30, 0.45, BACK)


badge("n1", "01", "la primera", 5.10, 11.26)
badge("n2", "02", "los patrones", 17.96, 21.16)
badge("n3", "03", "la más incómoda", 28.18, 31.34)


# ================================================================= 2 · EL BUCLE DE LA 1 AM
CX, CY, CR = 540, 418, 136
L = 2 * 3.14159 * CR
R.clip("loop", 6.40, 12.74, DEFS + f'''
  <circle id="lo-c" cx="{CX}" cy="{CY}" r="{CR}" stroke="{ORANGE}" stroke-width="3" fill="none" opacity="0.75"/>
  <g id="lo-arrow"><path d="M{CX} {CY - CR} m-16,-13 l16,13 l-16,13" stroke="{ORANGE}" stroke-width="4"
     fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
  {ui("lo-h", "1:00 AM", CX, CY - 8, 54, INK, "middle", 300)}
  {ui("lo-s", "las mismas conversaciones", CX, CY + 46, 26, INK_SOFT, "middle", 300)}''')
R.draw("#lo-c", L, 6.52, 0.95)
R.hidden("#lo-arrow, #lo-h, #lo-s", 6.40)
R.show("#lo-arrow", 7.20)
R.raw(f'  tl.fromTo("#lo-arrow", {{ rotation: 0, transformOrigin: "{CX}px {CY}px" }}, '
      f'{{ rotation: 720, duration: 4.6, ease: "none" }}, 7.20);')
R.fromTo("#lo-h", "autoAlpha:0, y:12", "autoAlpha:1, y:0", 7.35, 0.4, EASE)
R.fromTo("#lo-s", "autoAlpha:0", "autoAlpha:1", 7.70, 0.35)
R.fade("#lo-c, #lo-arrow", 11.90, 0.0, 0.4)
R.fade("#lo-h, #lo-s", 12.05, 0.0, 0.4)

# Lo que sí sale: el bucle se abre en una línea recta que termina en la flor de la marca.
R.clip("out", 12.86, 16.00, DEFS + dash("ou-l", f"M250 420 L836 420", ORANGE, 5, "16 14", 0.85)
       + flower("ou-f", 892, 420, 3.1))
R.draw("#ou-l", 600, 12.96, 0.85)
R.pop("#ou-f", 13.70, 0.55)
R.raw('  tl.to("#ou-f", { rotation: 14, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, 14.30);')

R.card("repite", 16.04, 17.92, [
    ("a", "Lo que no sale", 66, 0, 296, "center", "drop", 0.82, 16.10),
    ("b", "se repite.", 114, 0, 396, "center", "scale", 1.0, 16.42)])
R.punch_cam(16.45, 1.04)


# ================================================================= 3 · LAS OCHO PÁGINAS
PW, PH, PG = 186, 126, 22
X0, Y0 = 135, 258
pages = []
for k in range(8):
    px = X0 + (k % 4) * (PW + PG)
    py = Y0 + (k // 4) * (PH + PG)
    rules = "".join(
        f'<rect x="{px + 18}" y="{py + 26 + j * 22}" width="{[150, 126, 150, 108][j]}" height="3" rx="1.5" '
        f'fill="{INK_SOFT}" opacity="0.30"/>' for j in range(4) if j != 2)
    pages.append(f'<g id="pg{k}"><rect x="{px}" y="{py}" width="{PW}" height="{PH}" rx="12" '
                 f'fill="url(#pc)" stroke="{LINE}" stroke-width="1.5"/>{rules}'
                 f'<rect id="hl{k}" x="{px + 18}" y="{py + 68}" width="96" height="6" rx="3" fill="{ORANGE}"/></g>')
tagp, tagw = pill("pgtag", "la misma cosa", 0, 560)
tagp = tagp.replace('x="0"', f'x="{(1080 - tagw) / 2:.0f}"').replace(
    f'x="{0 + tagw / 2}"', f'x="{540}"')
R.clip("grid", 21.40, 26.36, DEFS + "".join(pages) + tagp)
R.hidden("#pgtag", 21.40)
R.raw('  tl.fromTo(gsap.utils.toArray("#grid g[id^=pg]"), { autoAlpha: 0, scale: 0.72, y: 18, '
      'transformOrigin: "50% 50%" }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.42, '
      'ease: "back.out(1.7)", stagger: 0.22 }, 21.52);')
R.raw('  tl.fromTo(gsap.utils.toArray("#grid rect[id^=hl]"), { scaleX: 1, transformOrigin: "0% 50%" }, '
      '{ scaleX: 1.42, duration: 0.26, ease: "power2.out", yoyo: true, repeat: 1, stagger: 0.04 }, 25.52);')
R.show("#pgtag", 25.56)
R.fromTo("#pgtag", "autoAlpha:0, scale:0.76, transformOrigin:'50% 50%'",
         "autoAlpha:1, scale:1", 25.56, 0.45, BACK)
R.punch_cam(25.56, 1.035)


# ================================================================= 4 · LAS EXCUSAS
R.clip("exc", 30.15, 33.92, DEFS
       + ed("ex-w", "excusas", 540, 390, 132, INK, "middle")
       + dash("ex-s", "M286 348 L794 348", ORANGE, 5, "16 14", 0.9)
       + flower("ex-f", 540, 498, 2.4))
R.hidden("#ex-s, #ex-f", 30.15)
R.fromTo("#ex-w", "autoAlpha:0, y:26", "autoAlpha:1, y:0", 30.24, 0.5, BACK)
R.show("#ex-s", 30.92)
R.draw("#ex-s", 508, 30.92, 0.55)
R.fade("#ex-w", 31.32, 0.42, 0.5)
R.pop("#ex-f", 31.95, 0.55)
R.raw('  tl.to("#ex-f", { rotation: -12, duration: 1.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 32.40);')

R.card("sabias", 34.35, 36.03, [
    ("a", "Ya no puedes decir", 60, 0, 296, "center", "drop", 0.82, 34.42),
    ("b", "que no sabías.", 100, 0, 392, "center", "scale", 1.0, 34.70)])
R.punch_cam(34.72, 1.04)


# ================================================================= 5 · LO QUE SÍ CAMBIA
CARDX, CARDY, CARDW, CARDH = 150, 268, 780, 132
dp, dpw = pill("gi-p", "decisiones", (1080 - 304) / 2, 496, 30, 66)
R.clip("giro", 40.10, 46.20, DEFS
       + paper_card("gi-c", CARDX, CARDY, CARDW, CARDH, 24, -0.6)
       + ed("gi-t", "meses evitando mirar", 540, 350, 50, INK, "middle", 500) + "</g>"
       + dash("gi-a", "M540 418 L540 478", ORANGE, 3, "10 10", 0.6)
       + dp)
R.hidden("#gi-a, #gi-p", 40.10)
R.fromTo("#gi-c", "autoAlpha:0, y:26, transformOrigin:'50% 50%'", "autoAlpha:1, y:0", 40.18, 0.5, BACK)
R.show("#gi-a", 42.26)
R.draw("#gi-a", 60, 42.26, 0.4)
R.show("#gi-p", 44.70)
R.fromTo("#gi-p", "autoAlpha:0, scale:0.7, transformOrigin:'50% 50%'",
         "autoAlpha:1, scale:1", 44.70, 0.5, BACK)
R.punch_cam(44.72, 1.035)


# ================================================================= 6 · EL JOURNAL · tarjeta
JX, JY, JW, JH = 84, 180, 912, 424
JH0 = 300          # la tarjeta entra baja y crece cuando aparecen las filas
tp, tpw = pill("jo-tag", "en el link de mi bio", JX + 48, JY + 34)
verbs = []
vx = JX + 48
for k, v in enumerate(["escribas", "dibujes", "rayes"]):
    vp, vw = pill(f"jo-v{k}", v, vx, JY + 334, 30, 54, 22, INK, "pg", caps=False)
    verbs.append(vp)
    vx += vw + 16
R.clip("journal", 46.55, 55.58, DEFS
       + paper_card("jo-c", JX, JY, JW, JH0, 28, -0.7) + "</g>"
       + tp
       + ed("jo-t", "Journal Claridad", JX + 48, JY + 156, 76, INK)
       + dash("jo-d", f"M{JX + 48} {JY + 188} L{JX + JW - 48} {JY + 188}", ORANGE, 2, "10 10", 0.40)
       + ed("jo-s", "una guía de preguntas para cada noche", JX + 48, JY + 248, 42, INK_SOFT, "start", 500)
       + flower("jo-f1", JX + 62, JY + 296, 0.95)
       + ui("jo-r1", "cinco minutos", JX + 94, JY + 308, 34, INK_SOFT)
       + flower("jo-f2", JX + 418, JY + 296, 0.95)
       + ui("jo-r2", "espacio ilimitado", JX + 450, JY + 308, 34, INK_SOFT)
       + "".join(verbs), hold=True)
R.hidden("#jo-tag, #jo-t, #jo-d, #jo-s, #jo-f1, #jo-r1, #jo-f2, #jo-r2, #jo-v0, #jo-v1, #jo-v2", 46.55)
R.fromTo("#jo-c", "autoAlpha:0, y:34, scale:0.96, transformOrigin:'50% 50%'",
         "autoAlpha:1, y:0, scale:1", 46.62, 0.55, BACK)
R.show("#jo-tag", 46.92)
R.fromTo("#jo-tag", "autoAlpha:0, scale:0.72, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1", 46.92, 0.45, BACK)
R.show("#jo-t", 47.24)
R.fromTo("#jo-t", "autoAlpha:0, y:22", "autoAlpha:1, y:0", 47.24, 0.5, BACK)
R.show("#jo-d", 47.70)
R.draw("#jo-d", JW - 96, 47.70, 0.5)
for sel, at in [("#jo-s", 49.45)]:
    R.show(sel, at)
    R.fromTo(sel, "autoAlpha:0, y:16", "autoAlpha:1, y:0", at, 0.45, EASE)
for sel, at in [("#jo-f1", 51.45), ("#jo-r1", 51.52), ("#jo-f2", 52.10), ("#jo-r2", 52.17)]:
    R.show(sel, at)
    R.fromTo(sel, "autoAlpha:0, scale:0.7, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", at, 0.4, BACK)
for k, at in enumerate([53.35, 53.58, 53.81]):
    R.show(f"#jo-v{k}", at)
    R.fromTo(f"#jo-v{k}", "autoAlpha:0, scale:0.7, y:14, transformOrigin:'50% 50%'",
             "autoAlpha:1, scale:1, y:0", at, 0.42, BACK)
R.raw(f'  tl.to("#jo-cr", {{ attr: {{ height: {JH} }}, duration: 0.55, ease: "back.out(1.4)" }}, 51.30);')
R.punch_cam(46.64, 1.04)
R.fade("#journal-in", 55.22, 0.0, 0.36)
R.hidden("#journal-in", 55.58)


# ================================================================= 7 · CIERRE sobre el plano
# No hay lámina de cierre: la marca se apoya sobre el encuadre y ella se ve hasta el último fotograma.
LW = 452
R.clip("fin", 55.92, R.DUR, DEFS
       + flower("fi-f", 540, 242, 2.3)
       + f'<image id="fi-w" href="{WORDMARK}" x="{(1080 - LW) / 2:.0f}" y="302" '
         f'width="{LW}" height="{LW / WM_AR:.0f}" opacity="0.92"/>'
       + ui("fi-h", "@daniblooming", 540, 596, 36, INK, "middle", 500), hold=True)
R.hidden("#fi-f, #fi-w, #fi-h", 55.92)
R.show("#fi-w", 56.00)
R.fromTo("#fi-w", "autoAlpha:0, y:20, scale:0.94", "autoAlpha:1, y:0, scale:1", 56.00, 0.6, BACK)
R.show("#fi-f", 56.30)
R.pop("#fi-f", 56.30, 0.5)
R.show("#fi-h", 56.60)
R.fromTo("#fi-h", "autoAlpha:0, y:12", "autoAlpha:1, y:0", 56.60, 0.45, EASE)
R.slow_push(55.95, 2.3, 1.045)
R.fadeout(0.45)


# ================================================================= estilos
R.extra_css = f'''
      /* Subtítulos en tinta café sobre el puf, sin caja y sin sombra: ahí el plano es el más claro. */
      .rail {{ top: 1404px; }}
      .rail .line {{ max-width: 900px; color: {INK}; text-shadow: none;
        font-weight: 500; font-size: 54px; line-height: 1.20; letter-spacing: 0.005em; }}
      .rail .w.hot.pill {{ padding: 0.04em 0.30em 0.10em; border-radius: 99px; }}
      /* Statements: Alegreya itálica, la voz editorial de la marca. Tinta, nunca blanco con sombra. */
      .card {{ height: 920px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-family: {SERIF}; font-style: italic; font-weight: 800; letter-spacing: -0.02em; }}
      #hook-c, #hook2-b {{ font-family: {SANS}; font-style: normal; font-weight: 300;
        color: {INK_SOFT}; letter-spacing: 0; }}
      #repite-a, #sabias-a {{ font-weight: 500; }}
      #hook-b {{ color: {ORANGE}; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
