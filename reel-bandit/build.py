#!/usr/bin/env python3
"""Sarier reel 4 — "Vas a salir a comer" (multi-armed bandit · explore vs exploit)."""
import sys; sys.path.insert(0, "..")
from reelkit import *

R = Reel("Sarier — Bandido multibrazo", gin_scale=0.58)
S, E, L = R.S, R.E, Reel.label
R.card_frags = {1, 2, 3, 5, 26, 27}
R.ink_frags = {8, 9}
R.punch = {4:"matemática",6:"invertir",7:"Netflix",8:"casino",9:"cinco",10:"bien",11:"cuatro",12:"peores",13:"mejor",14:"cambias",
           15:"central",16:"información",17:"pierdas",18:"futuro",19:"matemáticas",20:"explora",21:"explota",22:"cinco",23:"explorar",24:"mes",25:"capitalizar"}
R.rail()

# ---------------------------------------------------------------- statements
R.card("hook", 0.0, E(3) + 0.2, [
    ("a","Vas a salir a comer.",56,72,252,"left","left",0.72),
    ("b","¿Nuevo",180,40,298,"left","scale",1.0, S(2) + 0.1),
    ("c","o el de siempre?",84,60,452,"right","right",0.86, S(3) + 0.05)])
R.card("name", S(5) - 0.05, E(5) + 0.1, [
    ("a","Se llama",64,72,252,"left","left",0.72),
    ("b","bandido",160,40,300,"left","scale",1.0),
    ("c","multibrazo.",100,60,438,"right","right",0.86)], glitch_key="b")
R.glitch(S(5) + 0.2)
R.punch_cam(S(5) + 0.3)
R.card("close", S(26) - 0.1, R.DUR, [
    ("a","No es escoger lo seguro.",54,72,252,"left","left",0.72),
    ("b","Es saber cuándo",92,40,300,"left","scale",1.0, S(27) + 0.05),
    ("c","lo desconocido",92,60,378,"right","right",0.86, S(27) + 0.55),
    ("d","todavía vale.",84,60,456,"right","drop",1.0, S(27) + 1.15)])
R.slow_push(S(27))
R.fadeout()

# ---------------------------------------------------------------- icons
def icon(cls, x, y, body): return f'<g class="{cls}" transform="translate({x} {y})">{body}</g>'
HEART = f'<path d="M0 44 C-40 10 -60 -14 -34 -36 C-18 -48 0 -34 0 -20 C0 -34 18 -48 34 -36 C60 -14 40 10 0 44 Z" stroke="{INK}" {SW}/>'
PLANE = f'<path d="M0 -46 L10 -14 L46 4 L12 14 L6 44 L0 30 L-6 44 L-12 14 L-46 4 L-10 -14 Z" stroke="{INK}" {SW}/>'
CASE = f'<rect x="-44" y="-22" width="88" height="60" rx="10" stroke="{INK}" {SW}/><path d="M-16 -22 V-36 H16 V-22 M-44 4 H44" stroke="{INK}" {SW}/>'
CHART = f'<path d="M-44 36 L-14 6 L8 22 L44 -26 M22 -26 H44 V-4" stroke="{INK}" {SW}/>'
PLAY = f'<rect x="-46" y="-34" width="92" height="68" rx="12" stroke="{INK}" {SW}/><path d="M-10 -16 L18 0 L-10 16 Z" fill="{RED}"/>'
def slot(cls, x, y, s=1.0, color=INK):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<rect x="-60" y="-90" width="120" height="180" rx="14" stroke="{color}" {SW}/>'
            f'<rect x="-40" y="-60" width="80" height="50" rx="6" stroke="{color}" {SW}/>'
            f'<path d="M60 -50 H84 V-10" stroke="{color}" {SW}/><circle cx="84" cy="-58" r="10" fill="{RED}"/>'
            f'<rect x="-22" y="20" width="44" height="14" rx="7" stroke="{color}" {SW}/></g>')

# 1 · APLICA A… five icons land one per word
st, en = S(6), E(7) + 0.2
R.clip("apply", st, en, "".join([
    icon("ap ap0", 150, 220, HEART), icon("ap ap1", 345, 220, PLANE), icon("ap ap2", 540, 220, CASE), icon("ap ap3", 735, 220, CHART), icon("ap ap4", 930, 220, PLAY),
    L("apt0", "CITAS", 320, x=150), L("apt1", "VIAJAR", 320, x=345), L("apt2", "CONTRATAR", 320, x=540), L("apt3", "INVERTIR", 320, x=735), L("apt4", "NETFLIX", 320, x=930, color=RED)]))
R.hidden(".ap, #apt0, #apt1, #apt2, #apt3, #apt4", st)
for k, at in enumerate([S(6) + 0.55, S(6) + 1.15, S(6) + 1.75, S(6) + 2.35, S(7) + 1.0]):
    R.pop(f".ap{k}", at, 0.28); R.pop(f"#apt{k}", at + 0.08, 0.25)

# 2 · SCENE · CASINO — five slot machines (faceless, light)
st, en = S(8), E(9) + 0.15
R.scene("scA", st, en, LIGHT, f'''
  {L("ca-t", "EL NOMBRE VIENE DEL CASINO", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {"".join(slot(f"ca ca{k}", 150 + k * 195, 800, 1.6) for k in range(5))}
  {"".join(Reel.big(f"can{k}", str(k + 1), 1130, x=150 + k * 195, size=90) for k in range(5))}''')
R.hidden(".ca, .num, #ca-t", st)
R.pop("#ca-t", st + 0.2, 0.3)
R.pop(".ca", S(9) + 0.05, 0.25, stagger=0.1)
for k in range(5): R.pop(f"#can{k}", S(9) + 0.95 + k * 0.14, 0.2)

# 3 · overlay · which machine? — coins on #1, the other four unknown, one much better, ¿te cambias?
st, en = S(10), E(14) + 0.2
coins = "".join(f'<circle class="sl-coin" cx="{130 + k * 22 - 22}" cy="{320 + (k % 2) * 6}" r="12" fill="{INK}"/>' for k in range(3))
R.clip("slots", st, en, "".join(slot(f"sl sl{k}", 130 + k * 205, 190, 1.0) for k in range(5)) + f'''
  {coins}
  {L("sl-p", "PAGA BIEN", 380, x=130)}
  {"".join(f'<text class="sl-q" x="{335 + k * 205}" y="216" text-anchor="middle" class="big" fill="{INK}" style="font-size:70px;font-weight:700">?</text>' for k in range(4))}
  {"".join(f'<path class="sl-m" d="M{335 + k * 205 - 20} 130 H{335 + k * 205 + 20}" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>' for k in (0, 1, 3))}
  <path id="sl-plus" d="M745 110 V150 M725 130 H765" stroke="{RED}" stroke-width="12" stroke-linecap="round" fill="none"/>
  {Reel.spark(790, 100, 18, "sl-sp")}{Reel.spark(690, 90, 12, "sl-sp")}
  {L("sl-c", "¿TE CAMBIAS?", 470, color=RED)}''')
R.hidden(".sl-coin, #sl-p, .sl-q, .sl-m, #sl-plus, .sl-sp, #sl-c", st)
R.pop(".sl", st + 0.05, 0.25, stagger=0.06)
R.pop(".sl-coin", S(10) + 1.3, 0.2, stagger=0.1); R.pop("#sl-p", S(10) + 1.9, 0.25)
R.pop(".sl-q", S(11) + 0.6, 0.2, stagger=0.1)                                     # "otras cuatro que no has probado"
R.pop(".sl-m", S(12) + 0.9, 0.2, stagger=0.1)                                     # "podrían ser peores"
R.fade(".sl-q", S(13) + 1.4, 0.0, 0.2); R.pop("#sl-plus", S(13) + 1.5, 0.3); R.pop(".sl-sp", S(13) + 1.7, 0.2, stagger=0.1)   # "mucho mejor"
R.pulse("#sl-plus", S(13) + 2.3, 1.4)
R.pop("#sl-c", S(14) + 0.5, 0.3)                                                  # "¿te cambias?"

# 4 · overlay · two things: reward + information
st, en = S(15), E(18) + 0.2
R.clip("two", st, en, f'''
  <circle id="tw-a" cx="330" cy="230" r="110" stroke="{INK}" {SW} transform="rotate(-90 330 230)"/>
  <text id="tw-as" x="330" y="262" text-anchor="middle" class="big" fill="{INK}">$</text>
  <circle id="tw-b" cx="750" cy="230" r="110" stroke="{INK}" {SW} transform="rotate(-90 750 230)"/>
  <text id="tw-bs" x="750" y="262" text-anchor="middle" class="big" fill="{INK}">i</text>
  {L("tw-at", "RECOMPENSA", 400, x=330)}{L("tw-bt", "INFORMACIÓN", 400, x=750, color=RED)}
  <path id="tw-minus" d="M290 130 H370" stroke="{RED}" stroke-width="12" stroke-linecap="round" fill="none"/>
  {Reel.check("tw-ok", 750, 120, 30, RED)}
  {Reel.spark(880, 110, 22, "tw-sp")}{Reel.spark(900, 170, 12, "tw-sp")}
  {L("tw-f", "MEJOR OPCIÓN PARA EL FUTURO", 470, color=RED)}''')
R.hidden("#tw-as, #tw-bs, #tw-at, #tw-bt, #tw-minus, #tw-ok, .tw-sp, #tw-f", st)
R.draw("#tw-a, #tw-b", 700, S(16) + 0.9, 0.5, stagger=0.15)                        # "dos cosas"
R.pop("#tw-as", S(16) + 1.3, 0.25); R.pop("#tw-at", S(16) + 1.4, 0.25)              # "una recompensa"
R.pop("#tw-bs", S(16) + 1.75, 0.25); R.pop("#tw-bt", S(16) + 1.85, 0.25)            # "e información"
R.pop("#tw-minus", S(17) + 1.6, 0.25); R.to("#tw-a, #tw-as", 'scale: 0.82, transformOrigin: "50% 50%"', S(17) + 1.7, 0.4)   # "pierdas en el corto plazo"
R.draw("#tw-ok", 120, S(18) + 0.5, 0.3); R.pop(".tw-sp", S(18) + 0.7, 0.2, stagger=0.1); R.pop("#tw-f", S(18) + 0.9, 0.3)

# 5 · SCENE · LAS MATEMÁTICAS DICEN — explore while there is time (faceless, dark)
st, en = S(19), E(20) + 0.15
R.scene("scB", st, en, DARK, f'''
  {L("mt-t", "LAS MATEMÁTICAS DICEN", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  <path id="mt-bar" d="M120 900 H960" stroke="{WHITE}" stroke-width="10" stroke-linecap="round" fill="none"/>
  <path id="mt-fill" d="M120 900 H700" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  <path id="mt-w1" d="M700 850 V950" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <path id="mt-w2" d="M960 850 V950" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <g id="mt-dot"><circle cx="120" cy="900" r="22" fill="{RED}"/></g>
  {Reel.big("mt-ex", "EXPLORA", 760, WHITE, x=120, anchor="start", size=120)}
  {L("mt-t2", "MIENTRAS HAYA TIEMPO", 1020, x=120, anchor="start", color=WHITE, cls="wl2")}''')
R.hidden("#mt-t, #mt-fill, #mt-w1, #mt-w2, #mt-dot, #mt-ex, #mt-t2", st)
R.pop("#mt-t", st + 0.2, 0.3); R.draw("#mt-bar", 900, st + 0.3, 0.6)
R.pop("#mt-ex", S(20) + 0.1, 0.3); R.pop("#mt-dot", S(20) + 0.3, 0.2)
R.draw("#mt-fill", 600, S(20) + 0.4, 1.4, ease="power1.inOut")
R.fromTo("#mt-dot", "x: 0", "x: 580", S(20) + 0.4, 1.4, "power1.inOut")
R.draw("#mt-w1, #mt-w2", 110, S(20) + 1.4, 0.25, stagger=0.1); R.pop("#mt-t2", S(20) + 1.9, 0.3)

# 6 · overlay · the window closes → EXPLOTA (back on face)
st, en = S(21), E(21) + 0.25
R.clip("win", st, en, f'''
  <path id="wn-bar" d="M120 260 H960" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <g id="wn-a"><path d="M560 210 V310" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/></g>
  <g id="wn-b"><path d="M960 210 V310" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/></g>
  {Reel.big("wn-x", "EXPLOTA", 150, RED, x=540, size=96)}
  {L("wn-t", "CUANDO LA VENTANA SE CIERRA", 400)}''')
R.hidden("#wn-x, #wn-t", st)
R.draw("#wn-bar", 900, st + 0.05, 0.4); R.pop("#wn-x", st + 0.35, 0.3)
R.fromTo("#wn-a", "x: 0", "x: 190", S(21) + 0.9, 1.0, "power2.inOut"); R.fromTo("#wn-b", "x: 0", "x: -190", S(21) + 0.9, 1.0, "power2.inOut")
R.pop("#wn-t", S(21) + 1.2, 0.3)

# 7 · overlay · 5 AÑOS → explora · 1 MES → explota
st, en = S(22), E(25) + 0.2
R.clip("years", st, en, f'''
  {Reel.big("yr-5", "5 AÑOS", 250, INK, x=72, anchor="start", size=150)}
  {Reel.big("yr-1", "1 MES", 250, RED, x=72, anchor="start", size=150)}
  {L("yr-a", "EXPLORA AHORA", 330, x=72, anchor="start")}
  {L("yr-b", "CAPITALIZA LO APRENDIDO", 330, x=72, anchor="start", color=RED)}
  <path id="yr-bar" d="M72 420 H1008" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <g id="yr-dot"><circle cx="72" cy="420" r="18" fill="{RED}"/></g>''')
R.hidden("#yr-5, #yr-1, #yr-a, #yr-b, #yr-dot", st)
R.pop("#yr-5", S(22) + 1.6, 0.3); R.draw("#yr-bar", 950, st + 0.1, 0.5)
R.pop("#yr-a", S(23) + 1.0, 0.3); R.pop("#yr-dot", S(23) + 0.2, 0.2)
R.fromTo("#yr-dot", "x: 0", "x: 300", S(23) + 0.3, E(23) - S(23) - 0.3, "power1.inOut")
R.fade("#yr-5, #yr-a", S(24) + 1.2, 0.0, 0.2); R.pop("#yr-1", S(24) + 1.3, 0.3)
R.pop("#yr-b", S(25) + 0.7, 0.3)
R.fromTo("#yr-dot", "x: 300", "x: 930", S(24) + 1.3, E(25) - S(24) - 1.3, "power2.in")

R.write()
