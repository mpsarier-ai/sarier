#!/usr/bin/env python3
"""ÁMBAR SCULPT STUDIO — reel 9:16 sobre el video original.

Todo sale del paquete oficial de la marca (ambar-design-system):
  · negro cálido de fondo, un solo acento `fuego` por pieza, todo el texto `perla`
  · cinco voces tipográficas que no se intercambian: poster · titular · editorial · caligrafía · versalitas
  · el anillo de beneficios es el ÚNICO gráfico de la marca
  · a sangre y en ángulo recto: radius-0, sin sombras, sin iconos, sin tarjetas redondeadas
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc
import math

R = Reel("Ámbar Sculpt Studio — el método", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="ambar")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens (tokens.json)
NEGRO, OXBLOOD, VINO = "#070100", "#250202", "#4c0c09"
BRASA, FUEGO, SENAL, AMBAR = "#982a21", "#dc3023", "#de433e", "#c25030"
ARENA, TAUPE, PERLA, PERLA_S = "#89644d", "#bda692", "#fcfbf2", "#bfb3a8"

# comillas simples: estas pilas viajan dentro de un atributo style="..." de SVG
SANS = "'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
COND = "Anton, 'Arial Narrow', Impact, sans-serif"
SERIF = "'Cormorant Garamond', 'Times New Roman', serif"
SCRIPT = "'Pinyon Script', cursive"
LABEL = "'Sackers Gothic Std', 'Sackers Gothic', 'Helvetica Neue', sans-serif"

M = 40          # space-5 · margen lateral
HAIR = 'stroke-width="1" fill="none"'   # la línea fina perla de 1px de la marca

# El degradé de luz roja va siempre de rojo a negro pasando por vino y oxblood.
DEFS = f'''<defs>
    <linearGradient id="luzFoto" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BRASA}"/><stop offset="0.40" stop-color="{VINO}"/>
      <stop offset="0.75" stop-color="{OXBLOOD}"/><stop offset="1" stop-color="{NEGRO}"/>
    </linearGradient>
    <radialGradient id="luzCierre" cx="0.92" cy="1.05" r="1.15">
      <stop offset="0" stop-color="{FUEGO}"/><stop offset="0.22" stop-color="{BRASA}"/>
      <stop offset="0.52" stop-color="{VINO}"/><stop offset="0.88" stop-color="{NEGRO}"/>
    </radialGradient>
    <linearGradient id="fundidoAbajo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NEGRO}" stop-opacity="0"/><stop offset="0.30" stop-color="{NEGRO}" stop-opacity="0.55"/>
      <stop offset="0.58" stop-color="{NEGRO}" stop-opacity="0.86"/><stop offset="1" stop-color="{NEGRO}" stop-opacity="0.97"/>
    </linearGradient>
  </defs>'''


def txt(id_, s, x, y, size, fam, fill=PERLA, anchor="start", weight=400, style="normal", tr="0", extra=""):
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};font-style:{style};letter-spacing:{tr}"{extra}>{esc(s)}</text>')


def versalitas(id_, s, x, y, size=26, fill=PERLA, anchor="start"):
    """Sackers Gothic Medium: la minúscula se dibuja como versalita, por eso va con mayúscula inicial."""
    return txt(id_, s, x, y, size, LABEL, fill, anchor, weight=500, tr="0.10em")


def titular(id_, s, x, y, size=96, fill=PERLA, anchor="start"):
    return txt(id_, s, x, y, size, COND, fill, anchor, weight=400, tr="0.005em")


def editorial(id_, a, b, x, y, size=84, fill=PERLA, anchor="start"):
    """Concepto en minúscula con la segunda palabra en cursiva — 'calor infrarrojo'."""
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{SERIF};font-size:{size}px;font-weight:300;letter-spacing:0">{esc(a)} '
            f'<tspan style="font-style:italic">{esc(b)}</tspan></text>')


def caligrafia(id_, s, x, y, size=150, fill=PERLA, anchor="start"):
    """Una sola palabra emocional por pieza, cruzándose con el titular."""
    return txt(id_, s, x, y, size, SCRIPT, fill, anchor, weight=400)


# ================================================================= banda de subtítulos
# Sin sombras: los subtítulos se sientan sobre un fundido a negro a sangre, en ángulo recto.
R.scene("band", 0.0, R.DUR, "transparent",
        f'{DEFS}<rect x="0" y="820" width="1080" height="1100" fill="url(#fundidoAbajo)"/>')

# ================================================================= firma de marca (arriba, space-5)
R.clip("firma", 0.30, 18.42, versalitas("fm", "Ámbar Sculpt Studio", M, 262, 26, PERLA), hold=True)
R.fade("#firma-in", 18.20, 0.0, 0.22)

R.card_frags = {1, 4, 6, 8}   # estas líneas se dicen con tipografía grande, no con subtítulo

# ================================================================= 1 · SÉ QUE ODIAS EL GIMNASIO
st, en = S(1), E(1) + 0.30
R.clip("hook", st, en, DEFS
       + titular("h1", "SÉ QUE ODIAS", M, 1022, 104)
       + titular("h2", "EL GIMNASIO.", M, 1158, 104)
       + f'<path id="h-r" d="M{M} 1216 L 560 1216" stroke="{PERLA}" {HAIR}/>')
R.hidden("#h1, #h2, #h-r", st)
R.fromTo("#h1", "autoAlpha:0, y:26", "autoAlpha:1, y:0", st + 0.10, 0.45, "expo.out")
R.fromTo("#h2", "autoAlpha:0, y:26", "autoAlpha:1, y:0", st + 0.26, 0.45, "expo.out")
R.show("#h-r", st + 0.50); R.draw("#h-r", 520, st + 0.50, 0.5)

# ================================================================= 3 · CERO RESULTADOS
st, en = S(3) + 0.10, E(3) + 0.15
R.clip("res", st, en, DEFS
       + editorial("e1", "cero", "resultados", 1040, 1124, 92, PERLA, "end")
       + f'<path id="e-r" d="M620 1168 L1040 1168" stroke="{PERLA}" {HAIR}/>'
       + versalitas("e2", "Semana tras semana", 1040, 1222, 24, PERLA_S, "end"))
R.hidden("#e1, #e-r, #e2", st)
R.fromTo("#e1", "autoAlpha:0, x:30", "autoAlpha:1, x:0", st + 0.08, 0.5, "expo.out")
R.show("#e-r", st + 0.34); R.draw("#e-r", 420, st + 0.34, 0.45)
R.fromTo("#e2", "autoAlpha:0", "autoAlpha:1", st + 0.52, 0.3)

# ================================================================= 4 · UNA RUTINA QUE TE MOTIVE
st, en = S(4), E(4) + 0.22
R.clip("rut", st, en, DEFS
       + f'<path id="r-r" d="M{M} 912 L 470 912" stroke="{PERLA}" {HAIR}/>'
       + titular("t1", "UNA RUTINA", M, 1000, 104)
       + titular("t2", "QUE TE MOTIVE", M, 1136, 104))
R.hidden("#r-r, #t1, #t2", st)
R.show("#r-r", st + 0.06); R.draw("#r-r", 430, st + 0.06, 0.45)
R.fromTo("#t1", "autoAlpha:0, y:24", "autoAlpha:1, y:0", st + 0.16, 0.45, "expo.out")
R.fromTo("#t2", "autoAlpha:0, y:24", "autoAlpha:1, y:0", st + 0.30, 0.45, "expo.out")

# ================================================================= 5 · EL ANILLO DE BENEFICIOS
# El único gráfico de la marca: círculo perla de 1px, un punto por atributo, concepto al centro.
st, en = S(5) - 0.05, E(5) + 0.20
CX, CY, RAD = 540, 790, 300
ATTRS = [(-90, "CALOR INFRARROJO", "middle", 0, -52),
         (-30, "PILATES", "start", 26, 10),
         (30, "FUERZA FUNCIONAL", "start", 26, 10),
         (90, "BAJO IMPACTO", "middle", 0, 66),
         (150, "45 MINUTOS", "end", -26, 10),
         (210, "YOGA", "end", -26, 10)]
dots, labels = [], []
for k, (a, name, anc, dx, dy) in enumerate(ATTRS):
    rad = math.radians(a)
    px, py = CX + RAD * math.cos(rad), CY + RAD * math.sin(rad)
    dots.append(f'<circle class="dot" id="d{k}" cx="{px:.0f}" cy="{py:.0f}" r="4" fill="{PERLA}"/>')
    if " " in name and anc == "start" and len(name) > 12:
        a_, b_ = name.split(" ", 1)
        labels.append(f'<text class="lab" id="l{k}" x="{px + dx:.0f}" y="{py + dy - 16:.0f}" text-anchor="{anc}" fill="{PERLA}" '
                      f'style="font-family:{LABEL};font-size:25px;font-weight:500;letter-spacing:0.10em">{a_}'
                      f'<tspan x="{px + dx:.0f}" dy="34">{b_}</tspan></text>')
    else:
        labels.append(f'<text class="lab" id="l{k}" x="{px + dx:.0f}" y="{py + dy:.0f}" text-anchor="{anc}" fill="{PERLA}" '
                      f'style="font-family:{LABEL};font-size:25px;font-weight:500;letter-spacing:0.10em">{esc(name)}</text>')

R.scene("wash", st, en, "transparent",
        f'{DEFS}<rect x="0" y="0" width="1080" height="1920" fill="url(#luzFoto)" opacity="0.74"/>')
R.clip("ring", st, en, DEFS
       + f'<circle id="ring-c" cx="{CX}" cy="{CY}" r="{RAD}" stroke="{PERLA}" {HAIR}/>'
       + "".join(dots) + "".join(labels)
       + editorial("ring-t", "the ámbar", "method", CX, CY + 12, 80, PERLA, "middle"))
R.hidden("#ring-c, #ring .dot, #ring .lab, #ring-t", st)
R.show("#ring-c", st + 0.10); R.draw("#ring-c", 2 * math.pi * RAD, st + 0.10, 1.5, "power2.inOut")
R.pop("#ring .dot", st + 0.55, 0.30, 0.10)
R.fromTo("#ring .lab", "autoAlpha:0, y:8", "autoAlpha:1, y:0", st + 0.70, 0.35, "power2.out")
R.raw(f'  tl.fromTo("#ring .lab", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.35, stagger: 0.10, ease: "power2.out" }}, {st + 0.70:.2f});')
R.fromTo("#ring-t", "autoAlpha:0, scale:0.94, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + 0.95, 0.6, "expo.out")

# ================================================================= 6 · ÚNICA EN LA CIUDAD
st, en = S(6) + 0.08, E(6) + 0.18
R.clip("ciu", st, en, DEFS
       + editorial("c1", "única en la", "ciudad", M, 1040, 92)
       + f'<path id="c-r" d="M{M} 1086 L 520 1086" stroke="{PERLA}" {HAIR}/>'
       + versalitas("c2", "Pinares, Pereira", M, 1142, 25, PERLA_S))
R.hidden("#c1, #c-r, #c2", st)
R.fromTo("#c1", "autoAlpha:0, x:-26", "autoAlpha:1, x:0", st + 0.06, 0.5, "expo.out")
R.show("#c-r", st + 0.32); R.draw("#c-r", 480, st + 0.32, 0.45)
R.fromTo("#c2", "autoAlpha:0", "autoAlpha:1", st + 0.50, 0.3)

# ================================================================= 7 · ENCIENDE TU FUEGO
# El lockup de la marca: titular condensado + una palabra en caligrafía cruzándolo.
st, en = S(7) - 0.05, E(7) + 0.20
R.clip("fue", st, en, DEFS
       + titular("f1", "ENCIENDE TU", M, 760, 104)
       + caligrafia("f2", "fuego", 548, 716, 168)
       + titular("f3", "ESCULPE TU", M + 60, 900, 104)
       + caligrafia("f4", "fuerza", 570, 990, 168))
R.hidden("#f1, #f2, #f3, #f4", st)
R.fromTo("#f1", "autoAlpha:0, x:-30", "autoAlpha:1, x:0", st + 0.06, 0.45, "expo.out")
R.fromTo("#f2", "autoAlpha:0, x:40", "autoAlpha:1, x:0", st + 0.26, 0.6, "expo.out")
R.fromTo("#f3", "autoAlpha:0, x:-30", "autoAlpha:1, x:0", st + 0.46, 0.45, "expo.out")
R.fromTo("#f4", "autoAlpha:0, x:40", "autoAlpha:1, x:0", st + 0.66, 0.6, "expo.out")

# ================================================================= 8 · CIERRE
# luz-cierre: resplandor fuego desde la esquina inferior derecha, el texto a la izquierda sobre lo oscuro.
st = S(8) - 0.10
R.scene("cierre", st, R.DUR, "transparent",
        f'{DEFS}<rect x="0" y="0" width="1080" height="1920" fill="{NEGRO}"/>'
        f'<rect x="0" y="0" width="1080" height="1920" fill="url(#luzCierre)"/>')
R.clip("cta", st, R.DUR, DEFS
       + versalitas("k0", "Ámbar Sculpt Studio", M, 262, 26, PERLA)
       + editorial("k1", "sé parte de", "ámbar", M, 880, 112)
       + f'<path id="k-r" d="M{M} 936 L 600 936" stroke="{PERLA}" {HAIR}/>'
       + versalitas("k2", "Hot Pilates & Sculpt", M, 998, 26, PERLA)
       + versalitas("k3", "@ambarsculptstudio", M, 1052, 26, PERLA_S)
       + versalitas("k4", "Pinares, Pereira", M, 1106, 26, PERLA_S)
       + f'<rect id="k-b" x="{M}" y="1182" width="396" height="92" rx="14" fill="{PERLA}"/>'
       + txt("k-bt", "QUIERO RESERVAR", M + 198, 1239, 30, SANS, NEGRO, "middle", weight=700, tr="0.04em")
       + versalitas("k5", "The Ámbar Method", M, 1560, 24, PERLA_S), hold=True)
R.hidden("#k0, #k1, #k-r, #k2, #k3, #k4, #k-b, #k-bt, #k5", st)
R.fromTo("#k0", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.3)
R.fromTo("#k1", "autoAlpha:0, y:22", "autoAlpha:1, y:0", st + 0.14, 0.5, "expo.out")
R.show("#k-r", st + 0.36); R.draw("#k-r", 560, st + 0.36, 0.4)
R.fromTo("#k2, #k3, #k4", "autoAlpha:0, y:10", "autoAlpha:1, y:0", st + 0.46, 0.35, "power2.out")
R.raw(f'  tl.fromTo("#k2, #k3, #k4", {{ autoAlpha: 0, y: 10 }}, {{ autoAlpha: 1, y: 0, duration: 0.35, stagger: 0.08, ease: "power2.out" }}, {st + 0.46:.2f});')
R.fromTo("#k-b, #k-bt", "autoAlpha:0, y:14", "autoAlpha:1, y:0", st + 0.72, 0.4, "expo.out")
R.fromTo("#k5", "autoAlpha:0", "autoAlpha:1", st + 0.90, 0.35)

R.rail()
R.fadeout(0.35)

# ================================================================= estilo propio del reel
R.extra_css = f'''
      /* Subtítulos: cuerpo-mayus de la marca, perla, a la izquierda, sin sombra (BRAND.md: sin sombras). */
      .rail {{ top: 1452px; justify-content: flex-start; padding: 0 {M}px; }}
      .rail .line {{ max-width: 1000px; text-align: left; color: {PERLA}; text-shadow: none;
        font-family: 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif; font-weight: 400; font-size: 44px; line-height: 1.34;
        letter-spacing: 0.02em; text-transform: uppercase; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg circle, .mg svg path, .mg svg rect {{ shape-rendering: geometricPrecision; }}
'''

R.write()
