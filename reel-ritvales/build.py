#!/usr/bin/env python3
"""LUXUR — reel 9:16 · tres outfits para Ritvales (Q4 Trimestre Dorado).

Design system Q4 Trimestre Dorado: el LUXUR de siempre (papel, cream, blush, tinta) con el dorado
#8C7B5E como único acento por pantalla. Poppins 300 a tamaño grande para titulares y valores,
600 en versalitas para cintillos y etiquetas. Reglas de la marca: ningún gráfico tapa la pantalla
completa, ella nunca queda tapada y el logo de LUXUR solo entra cuando lo dicen en el audio (en
Montserrat 600 sin espaciado).

El plano manda. Dos encuadres:
  · plano medio hablado (0–13,07 s y 52,5 s–fin): su cabeza nunca sube de y≈380, así que la
    franja y 150..350 queda libre → tarjetas de 200 de alto.
  · plano entero en la tienda (13,07–52,5 s): su cabeza no sube de y≈640 → la ficha del outfit
    crece hasta y≈412 y nunca se le acerca.
Los subtítulos van abajo en blanco con halo (y 1420): el fondo va de 0 a 255 de luminancia y
ninguna tinta plana aguanta; terminan antes de la cintura de Instagram (1600).
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("LUXUR — tres outfits para Ritvales", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="luxur")

# ---------------------------------------------------------------- tokens Q4 Trimestre Dorado
PAPER, CREAM, BLUSH, INK = "#FBFAF7", "#EDEBE6", "#EECDCC", "#1C1C1C"
MUTE, LINE, SOFT, GOLD = "#5A5A5A", "#BDBAB3", "#E6E2DC", "#8C7B5E"
SANS = "'Poppins', 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
MONT = "'Montserrat', 'Poppins', 'Helvetica Neue', Helvetica, sans-serif"
BACK, EASE = "back.out(1.6)", "power2.out"

CX, CY, CW = 96, 150, 888          # la franja alta, libre en los dos encuadres
IX, IW = CX + 40, CW - 80
RIGHT = CX + CW - 40


def t(id_, s, x, y, size, fam=SANS, fill=INK, anchor="start", weight=400, tr="0", op=1.0):
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" opacity="{op}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def caps(id_, s, x, y, size=22, fill=INK, anchor="start", weight=600, op=1.0):
    return t(id_, s.upper(), x, y, size, SANS, fill, anchor, weight, "0.18em", op)


def light(id_, s, x, y, size=54, fill=INK, anchor="start"):
    """La firma del trimestre: Poppins 300 grande, -0,02em."""
    return t(id_, s, x, y, size, SANS, fill, anchor, 300, "-0.02em")


def brand(id_, x, y, size, anchor="start", fill=INK):
    """El wordmark solo cuando lo dicen: Montserrat 600 sin espaciado."""
    return t(id_, "LUXUR", x, y, size, MONT, fill, anchor, 600, "0")


def pill(cid, s, x, y, size=20, h=44, pad=24, bg=BLUSH, fg=INK, weight=600):
    """Cintillo como píldora: versalitas 600, 0,18em, ≈0,92em por carácter + padding."""
    s = s.upper()
    w = len(s) * size * 0.92 + 2 * pad
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{bg}"/>'
            + t(f"{cid}t", s, x + w / 2, y + h / 2 + size * 0.36, size, SANS, fg, "middle", weight, "0.18em")
            + '</g>'), w


def width300(s, size):
    """Ancho aproximado de Poppins 300: las mayúsculas abren más que las minúsculas."""
    return sum(size * (0.66 if c.isupper() else 0.30 if c == " " else 0.53) for c in s)


def enter(sel, at, origin="0% 50%", dur=0.4):
    R.fromTo(sel, f"autoAlpha:0, scale:0.7, transformOrigin:'{origin}'", "autoAlpha:1, scale:1", at, dur, BACK)


def slide(sel, at, dx=-16, dur=0.4):
    R.fromTo(sel, f"autoAlpha:0, x:{dx}", "autoAlpha:1, x:0", at, dur, EASE)


# ================================================================= subtítulos
# Lo que ya dice una tarjeta no se subtitula: 3 (Ritvales), 6 (tres outfits), 8–9 (regia, bella,
# apoteósica), 15 (súper ritvaludo), 29–30 (la pregunta del cierre).
R.card_frags = {3, 6, 8, 9, 15, 29, 30}
R.punch = {1: "yo,", 2: "octubre", 4: "electrónica.", 5: "amiga", 10: "primer", 11: "color.",
           12: "body", 14: "negro", 16: "segundo", 17: "monocromático.", 18: "cruces",
           19: "topcito", 20: "mangas", 21: "tercera", 22: "favorita.", 23: "body",
           24: "espalda,", 26: "hermoso", 27: "brillitos", 28: "ocasión."}
R.rail()
# La palabra LUXUR del subtítulo se compone como el wordmark (Montserrat 600, tracking 0).
R.rail_html = [re.sub(r'class="w" (id="r\d+w\d+")>LUXUR', r'class="w brand" \1>LUXUR', h)
               for h in R.rail_html]


# ================================================================= 1 · OCTUBRE · RITVALES
H1 = 184
op_, opw = pill("a-p", "octubre", IX, CY + 34, 20, 42, 20)
A = (f'<g id="a"><rect x="{CX}" y="{CY}" width="{CW}" height="{H1}" rx="32" fill="{PAPER}"/>'
     + op_
     + caps("a-e", "un mes lleno de eventos", IX + opw + 18, CY + 63, 20, MUTE, "start", 600)
     + light("a-t", "Ritvales", IX, CY + 152, 72)
     + f'<rect id="a-r" x="{IX}" y="{CY + 164}" width="44" height="4" fill="{GOLD}"/>'
     + caps("a-m1", "para los amantes de", RIGHT, CY + 112, 20, MUTE, "end", 600)
     + caps("a-m2", "la música electrónica", RIGHT, CY + 144, 20, INK, "end", 600)
     + '</g>')
R.clip("intro", 0.10, 6.85, A)
R.fromTo("#a", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", 0.14, 0.5, BACK)
enter("#a-p", 0.95)
slide("#a-e", 1.80)
R.fromTo("#a-t", "autoAlpha:0, y:18", "autoAlpha:1, y:0", 3.16, 0.45, BACK)
R.fromTo("#a-r", "attr:{width:0}", "attr:{width:44}", 3.50, 0.4, EASE)
slide("#a-m1", 4.30, 16)
slide("#a-m2", 4.55, 16)
R.punch_cam(3.18, 1.03)


# ================================================================= 2 · TRES OUTFITS, TODOS EN LUXUR
NX = IX + 112
p1, w1 = pill("b-p0", "regia", NX, CY + 128, 20, 40, 22)
p2, w2 = pill("b-p1", "bella", NX + w1 + 12, CY + 128, 20, 40, 22)
p3, w3 = pill("b-p2", "apoteósica", NX + w1 + w2 + 24, CY + 128, 20, 40, 22, GOLD, PAPER)
B = (f'<g id="b"><rect x="{CX}" y="{CY}" width="{CW}" height="{H1}" rx="32" fill="{PAPER}"/>'
     + light("b-n", "3", IX - 4, CY + 150, 140)
     + caps("b-o", "outfits", NX, CY + 78, 30, INK, "start", 600)
     + caps("b-r", "para ritvales", NX, CY + 114, 20, MUTE, "start", 600)
     + caps("b-l1", "todos en", RIGHT, CY + 62, 18, MUTE, "end", 600)
     + brand("b-l2", RIGHT, CY + 112, 48, "end")
     + p1 + p2 + p3 + '</g>')
R.clip("outfits", 6.85, 13.02, B)
R.fromTo("#b", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", 6.88, 0.45, BACK)
R.fromTo("#b-n", "autoAlpha:0, scale:0.6, transformOrigin:'0% 100%'", "autoAlpha:1, scale:1", 7.00, 0.5, BACK)
slide("#b-o", 7.20)
slide("#b-r", 7.35)
slide("#b-l1", 8.70, 16)                          # "...todos en LUXUR"
R.fromTo("#b-l2", "autoAlpha:0, y:10", "autoAlpha:1, y:0", 9.05, 0.4, BACK)
for k, at in enumerate([9.95, 10.75, 11.55]):     # regia · bella · apoteósica
    enter(f"#b-p{k}", at)
R.punch_cam(7.02, 1.03)


# ================================================================= 3 · LOS TRES OUTFITS
# Ficha que crece: cabecera (número + titular + contador de tres barras con la activa en dorado),
# y una fila por prenda, que entra cuando ella la nombra. El fondo crece con cada fila para que
# no haya hueco muerto. La píldora de detalle va en la misma fila, detrás del valor.
H0, HR1, HR2 = 128, 202, 268
R1, R2 = CY + 174, CY + 240                       # líneas base de las filas
VX = IX + 196                                     # columna de valores

OUTFITS = [
    # (inicio, fin, titular, [(entra, etiqueta, valor, ¿wordmark?, (píldora, entra) | None)])
    (13.07, 23.30, "las arriesgadas", [
        (16.60, "body", "MAI PETIT", False, None),
        (19.95, "jean", "negro", False, ("súper ritvaludo", 22.40))]),
    (23.36, 35.15, "monocromático", [
        (26.30, "jean", "cruces negras", False, None),
        (29.40, "topcito", "MAI PETIT", False, ("las mangas", 32.20))]),
    (35.20, 51.80, "mi favorita", [
        (39.35, "body", "MAI PETIT", False, ("la espalda", 42.65)),
        (44.75, "jean", "LUXUR", True, ("con brillitos", 47.30))]),
]
bw = (IW - 2 * 12) / 3
for k, (st, en, title, rows) in enumerate(OUTFITS, 1):
    p = f"o{k}"
    np_, nw = pill(f"{p}-n", f"0{k}", IX, CY + 30, 22, 48, 20, INK, PAPER)
    bars = []
    for j in range(3):
        bx = IX + j * (bw + 12)
        bars.append(f'<rect x="{bx:.1f}" y="{CY + 104}" width="{bw:.1f}" height="4" rx="2" fill="{SOFT}"/>')
        if j < k - 1:
            bars.append(f'<rect x="{bx:.1f}" y="{CY + 104}" width="{bw:.1f}" height="4" rx="2" fill="{LINE}"/>')
        if j == k - 1:
            bars.append(f'<rect id="{p}-g" x="{bx:.1f}" y="{CY + 104}" width="0" height="4" rx="2" fill="{GOLD}"/>')
    body = []
    for r, (at, lab, val, isbrand, acc) in enumerate(rows):
        y = R1 if r == 0 else R2
        body.append(caps(f"{p}-l{r}", lab, IX, y - 8, 20, MUTE, "start", 600))
        if isbrand:
            body.append(brand(f"{p}-v{r}", VX, y, 44))
            vw = 5 * 44 * 0.74
        else:
            body.append(light(f"{p}-v{r}", val, VX, y, 44))
            vw = width300(val, 44)
        if acc:
            pg, _ = pill(f"{p}-a{r}", acc[0], VX + vw + 26, y - 36, 19, 44, 20)
            body.append(pg)
        if r == 0:
            body.append(f'<path id="{p}-h" d="M{IX} {R1 + 22} L{RIGHT} {R1 + 22}" stroke="{SOFT}" '
                        f'stroke-width="2" fill="none"/>')
    g = (f'<g id="{p}"><rect id="{p}-bg" x="{CX}" y="{CY}" width="{CW}" height="{H0}" rx="32" fill="{PAPER}"/>'
         + np_ + light(f"{p}-t", title, IX + nw + 22, CY + 72, 54)
         + "".join(bars) + "".join(body) + '</g>')
    R.clip(f"{p}c", st, en, g)
    R.fromTo(f"#{p}", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", st + 0.04, 0.5, BACK)
    enter(f"#{p}-n", st + 0.16)
    slide(f"#{p}-t", st + 0.28, -18)
    R.fromTo(f"#{p}-g", "attr:{width:0}", f"attr:{{width:{bw:.1f}}}", st + 0.45, 0.5, EASE)
    R.punch_cam(st + 0.02, 1.03)
    for r, (at, lab, val, isbrand, acc) in enumerate(rows):
        R.to(f"#{p}-bg", f"attr:{{height:{HR1 if r == 0 else HR2}}}", at - 0.05, 0.4, EASE)
        slide(f"#{p}-l{r}", at)
        R.fromTo(f"#{p}-v{r}", "autoAlpha:0, x:-18", "autoAlpha:1, x:0", at + 0.10, 0.45, BACK)
        if r == 0:
            R.draw(f"#{p}-h", IW, at + 0.20, 0.5)
        if acc:
            enter(f"#{p}-a{r}", acc[1])


# ================================================================= 4 · CIERRE
H4 = 200
q = [pill(f"q-p{j}", f"0{j + 1}", IX + j * 92, CY + 126, 20, 44, 18, CREAM, INK) for j in range(3)]
dm, dmw = pill("q-dm", "coméntanos o dm", RIGHT - (len("COMÉNTANOS O DM") * 20 * 0.92 + 48), CY + 126, 20, 44, 24)
Q = (f'<g id="q"><rect x="{CX}" y="{CY}" width="{CW}" height="{H4}" rx="32" fill="{PAPER}"/>'
     + f'<rect id="q-r" x="{IX}" y="{CY + 30}" width="44" height="4" fill="{GOLD}"/>'
     + light("q-t", "¿cuál fue tu favorito?", IX, CY + 96, 54)
     + "".join(g for g, _ in q) + dm + '</g>')
R.clip("fin", 51.90, R.DUR, Q, hold=True)
R.fromTo("#q", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", 51.94, 0.5, BACK)
R.fromTo("#q-r", "attr:{width:0}", "attr:{width:44}", 52.10, 0.4, EASE)
slide("#q-t", 52.20, -18)
for j in range(3):
    enter(f"#q-p{j}", 52.80 + j * 0.25)
enter("#q-dm", 54.15, "100% 50%")
R.slow_push(52.52, 2.6, 1.03)
R.fadeout(0.45)


# ================================================================= estilos
R.extra_css = f'''
      /* Subtítulos en blanco con halo: el fondo va de 0 a 255 y ninguna tinta plana aguanta.
         Terminan antes de y=1600, donde empieza la interfaz de Instagram. */
      .rail {{ top: 1420px; }}
      .rail .line {{ max-width: 880px; font-weight: 500; font-size: 50px; line-height: 1.20;
        text-shadow: 0 0 4px rgba(0,0,0,0.60), 0 0 12px rgba(0,0,0,0.85), 0 2px 5px rgba(0,0,0,0.70), 0 8px 30px rgba(0,0,0,0.45); }}
      .rail .w.brand {{ font-family: {MONT}; font-weight: 600; letter-spacing: 0; }}
      .rail .w.hot.pill {{ padding: 0.04em 0.30em 0.10em; border-radius: 99px; }}
      .card {{ height: 1920px; }}
      .mg svg text, .mg svg rect, .mg svg path {{ shape-rendering: geometricPrecision; }}
'''

R.write()
