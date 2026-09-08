#!/usr/bin/env python3
"""Sarier reel 6 — Mech interp (how does AI think?)."""
import sys; sys.path.insert(0, "..")
from reelkit import *

R = Reel("Sarier — Mech interp", gin_scale=0.50)
S, E, L = R.S, R.E, Reel.label
R.card_frags = {1, 10, 23, 24}
R.ink_frags = set()
R.punch = {2:"investigación",3:"misterios",4:"planta",5:"crecer",6:"adentro",7:"IA",8:"arquitectura",9:"adentro",11:"números",12:"matemáticas",
           13:"geometrías",14:"investigadores",15:"semana",16:"reloj",17:"empujaban",18:"bellísima",19:"importa",20:"enseñarnos",21:"decisiones",22:"piensa"}
R.rail()

# ---------------------------------------------------------------- statements
R.card("hook", 0.0, E(1) + 0.4, [
    ("a","¿Has oído hablar de",56,72,252,"left","left",0.72),
    ("b","mech interp?",130,40,298,"left","scale",1.0, 0.55)], glitch_key="b")
R.glitch(0.6); R.punch_cam(0.7)
R.card("q", S(10) - 0.05, E(10) + 0.1, [
    ("a","¿Cómo piensa",100,40,252,"left","scale",1.0, S(10) + 1.3),
    ("b","la IA?",150,60,340,"right","right",0.86, S(10) + 1.8)])
R.punch_cam(S(10) + 1.85)
R.card("close", S(23) - 0.1, R.DUR, [
    ("a","Podríamos entender",56,72,252,"left","left",0.72),
    ("b","qué es realmente",84,40,300,"left","scale",1.0, S(23) + 1.5),
    ("c","pensar.",150,60,370,"right","right",0.86, S(24) + 0.05)])
R.slow_push(S(24))
R.fadeout()

# ---------------------------------------------------------------- graphics
# 1 · MISTERIO — magnifier with a question mark
st, en = S(2), E(3) + 0.2
R.clip("myst", st, en, f'''
  <circle id="my-c" cx="500" cy="220" r="130" stroke="{INK}" {SW} transform="rotate(-90 500 220)"/>
  <path id="my-h" d="M595 315 L700 420" stroke="{INK}" stroke-width="12" stroke-linecap="round" fill="none"/>
  <text id="my-q" x="500" y="258" text-anchor="middle" class="big" fill="{RED}">?</text>
  {L("my-t", "UNO DE LOS MAYORES MISTERIOS", 500)}''')
R.hidden("#my-q, #my-t", st)
R.draw("#my-c", 850, st + 0.05, 0.7); R.draw("#my-h", 160, st + 0.6, 0.3)
R.pop("#my-q", S(3) + 0.2, 0.3); R.pop("#my-t", S(3) + 1.0, 0.3)

# 2 · PLANTA — seed, stem grows, leaves; "adentro" stays a question
st, en = S(4), E(6) + 0.2
R.clip("plant", st, en, f'''
  <path id="pl-g" d="M300 420 H780" stroke="{INK}" {SW}/>
  <circle id="pl-seed" cx="540" cy="405" r="14" fill="{INK}"/>
  <path id="pl-s" d="M540 405 C540 320 535 240 545 150" stroke="{INK}" {SW8}/>
  <path id="pl-l1" d="M541 300 C480 300 450 250 455 220 C500 225 540 260 541 300 Z" stroke="{INK}" {SW}/>
  <path id="pl-l2" d="M543 230 C600 230 635 180 630 150 C585 155 545 190 543 230 Z" stroke="{INK}" {SW}/>
  <rect id="pl-box" x="470" y="140" width="150" height="270" rx="12" stroke="{RED}" stroke-width="5" stroke-dasharray="14 10" fill="none"/>
  <text id="pl-q" x="640" y="300" text-anchor="middle" class="big" fill="{RED}">?</text>
  {L("pl-t", "¿QUÉ PASA ADENTRO?", 480, color=RED)}''')
R.hidden("#pl-seed, #pl-box, #pl-q, #pl-t", st)
R.draw("#pl-g", 500, st + 0.05, 0.4); R.pop("#pl-seed", S(5) + 0.4, 0.25)          # "cómo empieza"
R.draw("#pl-s", 300, S(5) + 1.0, 0.7); R.draw("#pl-l1", 300, S(5) + 1.5, 0.35); R.draw("#pl-l2", 300, S(5) + 1.7, 0.35)   # "hacerla crecer"
R.show("#pl-box", S(6) + 1.6); R.draw("#pl-box", 900, S(6) + 1.6, 0.4); R.pop("#pl-q", S(6) + 2.0, 0.3); R.pop("#pl-t", S(6) + 2.2, 0.3)

# 3 · RED NEURONAL — the architecture we know, the inside we don't
st, en = S(7), E(9) + 0.2
cols = [(300, [140, 260, 380]), (540, [100, 200, 300, 400]), (780, [180, 320])]
nodes = "".join(f'<circle class="nn-n nn-c{c}" cx="{x}" cy="{y}" r="16" stroke="{INK}" {SW}/>' for c, (x, ys) in enumerate(cols) for y in ys)
links = "".join(f'<path class="nn-l" d="M{cols[c][0]} {y1} L{cols[c+1][0]} {y2}" stroke="{INK}" stroke-width="3" fill="none"/>'
                for c in range(2) for y1 in cols[c][1] for y2 in cols[c + 1][1])
qs = "".join(f'<text class="nn-q" x="540" y="{y + 12}" text-anchor="middle" fill="{RED}" style="font-size:36px;font-weight:700">?</text>' for y in cols[1][1])
R.clip("net", st, en, links + nodes + qs + L("nn-t", "SABEMOS LA ARQUITECTURA", 470) + L("nn-t2", "NO SABEMOS QUÉ OCURRE ADENTRO", 470, color=RED))
R.hidden(".nn-q, #nn-t, #nn-t2", st)
R.pop(".nn-c0", S(8) + 0.5, 0.2, stagger=0.06); R.pop(".nn-c1", S(8) + 0.9, 0.2, stagger=0.06); R.pop(".nn-c2", S(8) + 1.3, 0.2, stagger=0.06)
R.draw(".nn-l", 300, S(8) + 0.7, 0.4, stagger=0.02); R.pop("#nn-t", S(8) + 1.0, 0.3)
R.fade(".nn-c1", S(9) + 1.2, 0.0, 0.2); R.pop(".nn-q", S(9) + 1.3, 0.25, stagger=0.06)   # "qué ocurre adentro"
R.fade("#nn-t", S(9) + 1.2, 0.0, 0.2); R.pop("#nn-t2", S(9) + 1.4, 0.3)

# 4 · SCENE · UNA MENTE HECHA DE NÚMEROS (faceless, dark)
st, en = S(11), E(12) + 0.15
import random; random.seed(7)
digits = "".join(f'<text class="nm-d" x="{x}" y="{y}" text-anchor="middle" fill="{RED if random.random() < 0.25 else WHITE}" style="font-size:40px;font-weight:700">{random.choice("0101010110")}</text>'
                 for x in range(360, 760, 50) for y in range(640, 1000, 48) if (x - 540) ** 2 / 210 ** 2 + (y - 810) ** 2 / 160 ** 2 < 1)
R.scene("scA", st, en, DARK, f'''
  {L("nm-t", "UNA MENTE HECHA DE NÚMEROS", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {R.brain("nm", WHITE, extra='transform="translate(-125 480) scale(1.2)"', sw=SW8)}
  {digits}
  {Reel.big("nm-a", "LENGUAJE", 1180, WHITE, x=72, anchor="start", size=90)}
  {Reel.big("nm-e", "=", 1180, RED, x=640, size=90)}
  {Reel.big("nm-b", "MATEMÁTICAS", 1290, RED, x=72, anchor="start", size=90)}''')
R.hidden("#nm-t, .nm-d, .nm-gy, #nm-f, #nm-a, #nm-e, #nm-b", st)
R.pop("#nm-t", st + 0.2, 0.3); R.draw_brain("nm", st + 0.05, 0.7)
R.hidden(".nm-gy, #nm-f", st + 0.05)
R.pop(".nm-d", S(11) + 1.3, 0.15, stagger=0.02)                                    # "enteramente de números"
R.pop("#nm-a", S(12) + 0.2, 0.3); R.pop("#nm-e", S(12) + 0.9, 0.25); R.pop("#nm-b", S(12) + 1.1, 0.3)

# 5 · DIRECCIONES EN EL ESPACIO — vectors from a point, then a geometry
st, en = S(13), E(13) + 0.25
angs = [-80, -30, 20, 70, 130, 200, 250]
import math
vecs = "".join(f'<path class="vc-v" d="M540 250 L{540 + 150 * math.cos(math.radians(a)):.0f} {250 + 150 * math.sin(math.radians(a)):.0f}" stroke="{INK}" {SW}/>' for a in angs)
tips = " ".join(f'{540 + 150 * math.cos(math.radians(a)):.0f},{250 + 150 * math.sin(math.radians(a)):.0f}' for a in angs)
R.clip("vec", st, en, f'''
  <circle cx="540" cy="250" r="10" fill="{INK}"/>{vecs}
  <polygon id="vc-g" points="{tips}" stroke="{RED}" {SW}/>
  {L("vc-t", "ORDENADAS EN GEOMETRÍAS", 470, color=RED)}''')
R.hidden("#vc-t", st)
R.draw(".vc-v", 160, st + 0.1, 0.3, stagger=0.08)                                   # "direcciones en el espacio"
R.draw("#vc-g", 1100, S(13) + 1.3, 0.6); R.pop("#vc-t", S(13) + 1.6, 0.3)          # "ordenadas en geometrías"

# 6 · EL RELOJ DE LOS DÍAS — days on a circle; push one and the answer changes
st, en = S(14), E(18) + 0.2
DAYS = ["L", "M", "X", "J", "V", "S", "D"]
dn = "".join(f'<g class="dy-n" id="dy-n{k}" transform="rotate({k * 360 / 7} 540 250)"><circle cx="540" cy="90" r="26" fill="#FFFFFF" stroke="{INK}" {SW}/>'
             f'<text x="540" y="100" text-anchor="middle" fill="{INK}" style="font-size:28px;font-weight:700" transform="rotate({-k * 360 / 7} 540 90)">{d}</text></g>' for k, d in enumerate(DAYS))
R.clip("clock", st, en, f'''
  <circle id="dy-r" cx="540" cy="250" r="160" stroke="{INK}" {SW} transform="rotate(-90 540 250)"/>
  {dn}
  <path id="dy-h" d="M540 250 L540 140" stroke="{RED}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <circle cx="540" cy="250" r="8" fill="{RED}"/>
  {Reel.spark(760, 120, 22, "dy-sp")}{Reel.spark(800, 190, 12, "dy-sp")}{Reel.spark(300, 150, 14, "dy-sp")}
  {L("dy-t", "LOS DÍAS DE LA SEMANA", 470)}
  {L("dy-b", "BELLÍSIMO", 470, color=RED)}''')
R.hidden(".dy-n, #dy-h, .dy-sp, #dy-t, #dy-b", st)
R.draw("#dy-r", 1050, S(15) + 0.3, 0.7); R.pop(".dy-n", S(15) + 0.9, 0.2, stagger=0.07); R.pop("#dy-t", S(15) + 1.2, 0.3)   # "días de la semana"
R.pop("#dy-h", S(16) + 1.5, 0.25)                                                   # "parecida a un reloj"
R.fromTo("#dy-h", 'rotation: 0, svgOrigin: "540 250"', "rotation: 360", S(16) + 1.6, E(17) - S(16) - 1.6, "none")
R.to("#dy-n2", f'attr: {{ transform: "rotate({2 * 360 / 7 + 30} 540 250)" }}', S(17) + 1.2, 0.5, "back.out(2)")   # "empujaban un poco esas posiciones"
R.to("#dy-n2 circle", f'fill: "{RED}"', S(17) + 1.2, 0.3)
R.pop(".dy-sp", S(18) + 0.8, 0.25, stagger=0.1); R.fade("#dy-t", S(18) + 0.7, 0.0, 0.2); R.pop("#dy-b", S(18) + 0.9, 0.3)   # "bellísima"

# 7 · POR QUÉ IMPORTA — teach · advise · decide
st, en = S(19), E(22) + 0.2
BOOK = f'<path d="M-50 -34 H-6 Q0 -34 0 -28 V36 Q0 30 -6 30 H-50 Z M50 -34 H6 Q0 -34 0 -28 V36 Q0 30 6 30 H50 Z" stroke="{INK}" {SW}/>'
BUBBLE = f'<path d="M-50 -36 H50 Q60 -36 60 -26 V14 Q60 24 50 24 H-6 L-30 44 V24 H-50 Q-60 24 -60 14 V-26 Q-60 -36 -50 -36 Z" stroke="{INK}" {SW}/>'
CHECK = f'<rect x="-44" y="-44" width="88" height="88" rx="14" stroke="{INK}" {SW}/><path d="M-22 0 L-6 16 L24 -18" stroke="{RED}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
R.clip("why", st, en, f'''
  <g class="wy wy0" transform="translate(260 220)">{BOOK}</g><g class="wy wy1" transform="translate(540 220)">{BUBBLE}</g><g class="wy wy2" transform="translate(820 220)">{CHECK}</g>
  {L("wy-t0", "ENSEÑAR", 330, x=260)}{L("wy-t1", "ACONSEJAR", 330, x=540)}{L("wy-t2", "DECIDIR", 330, x=820)}
  {L("wy-b", "NECESITAMOS SABER CÓMO PIENSA", 470, color=RED)}''')
R.hidden(".wy, #wy-t0, #wy-t1, #wy-t2, #wy-b", st)
R.pop(".wy0", S(20) + 0.6, 0.28); R.pop("#wy-t0", S(20) + 0.7, 0.25)
R.pop(".wy1", S(20) + 1.4, 0.28); R.pop("#wy-t1", S(20) + 1.5, 0.25)
R.pop(".wy2", S(21) + 0.6, 0.28); R.pop("#wy-t2", S(21) + 0.7, 0.25)
R.pop("#wy-b", S(22) + 0.5, 0.3)

R.write()
