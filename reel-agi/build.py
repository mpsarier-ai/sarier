#!/usr/bin/env python3
"""Sarier reel 7 — ¿Qué es la AGI? (ANI appliances vs the AGI chef). Face sits high in this take: everything stays ≤ ~460px."""
import sys; sys.path.insert(0, "..")
from reelkit import *

R = Reel("Sarier — ¿Qué es la AGI?", gin_scale=0.44)
S, E, L = R.S, R.E, Reel.label
R.card_frags = {1, 15, 23, 24}
R.ink_frags = {5, 6}
R.punch = {2:"término",3:"difuso",4:"cocina",5:"batidora",6:"estrecha",7:"IA",8:"rotoscopiado",9:"imágenes",10:"hervir",11:"específicas",12:"general",
           13:"cocinero",14:"recetas",16:"llegamos",17:"intermedio",18:"confundida",19:"especializada",20:"confiable",21:"humano",22:"pronto",25:"ahora"}
R.rail()

# ---------------------------------------------------------------- statements
R.card("hook", 0.0, E(3) + 0.1, [
    ("a","¿Qué es la",52,72,252,"left","left",0.72),
    ("b","AGI",150,40,296,"left","scale",1.0, 0.45),
    ("c","en realidad?",60,60,426,"right","right",0.86, 1.05)], glitch_key="b")
R.glitch(0.5); R.punch_cam(0.6)
R.card("gen", S(15) - 0.05, E(15) + 0.1, [
    ("a","AGI:",72,72,252,"left","left",0.72),
    ("b","cualquier tarea",84,40,322,"left","scale",1.0, S(15) + 1.2),
    ("c","a nivel humano.",72,60,396,"right","right",0.86, S(15) + 2.0)])
R.card("close", S(23) - 0.1, R.DUR, [
    ("a","Cuando las máquinas",44,72,252,"left","left",0.72),
    ("b","sean chefs,",88,40,288,"left","scale",1.0, S(23) + 1.0),
    ("c","¿qué pasa en la cocina?",48,60,362,"right","right",0.86, S(24) + 0.05)])
R.slow_push(S(24))
R.fadeout()

# ---------------------------------------------------------------- icons (centered at 0,0)
def g(cls, x, y, body, s=1.0): return f'<g class="{cls}" transform="translate({x} {y}) scale({s})">{body}</g>'
def TOASTER(c=INK): return (f'<rect x="-70" y="-30" width="140" height="80" rx="16" stroke="{c}" {SW}/><path d="M-40 -30 V-46 H-14 V-30 M14 -30 V-46 H40 V-30" stroke="{c}" {SW}/>'
                            f'<path d="M70 -10 H90 V20" stroke="{c}" {SW}/><circle cx="90" cy="-16" r="8" fill="{RED}"/>')
def BLENDER(c=INK): return (f'<path d="M-34 -70 H34 L44 10 H-44 Z" stroke="{c}" {SW}/><rect x="-50" y="10" width="100" height="42" rx="10" stroke="{c}" {SW}/>'
                            f'<path d="M-30 -84 H30" stroke="{c}" {SW}/><circle cx="0" cy="31" r="6" fill="{RED}"/>')
def MIXER(c=INK): return (f'<path d="M-56 -4 A56 56 0 0 0 56 -4 Z" stroke="{c}" {SW}/><path d="M-14 -80 L0 -20 M14 -80 L0 -20 M-8 -86 H8" stroke="{c}" {SW}/>'
                          f'<path d="M-20 -50 C-30 -30 -20 -20 0 -20 C20 -20 30 -30 20 -50" stroke="{RED}" {SW}/>')
def HAT(c=INK): return (f'<path d="M-52 24 V-8 C-96 -18 -76 -84 -34 -64 C-24 -104 24 -104 34 -64 C76 -84 96 -18 52 -8 V24 Z" stroke="{c}" {SW}/>'
                        f'<path d="M-52 4 H52" stroke="{c}" {SW}/>')
def POT(c=INK): return (f'<rect x="-60" y="-20" width="120" height="70" rx="12" stroke="{c}" {SW}/><path d="M-60 0 H-84 M60 0 H84" stroke="{c}" {SW}/>'
                        f'<path d="M-30 -40 Q-20 -56 -30 -72 M0 -40 Q10 -56 0 -72 M30 -40 Q40 -56 30 -72" stroke="{c}" {SW}/>')
def PERSON(c=INK): return (f'<circle cx="0" cy="-46" r="26" stroke="{c}" {SW}/><path d="M-60 50 C-60 0 -30 -12 0 -12 C30 -12 60 0 60 50" stroke="{c}" {SW}/>')
def FRAME(c=INK): return (f'<rect x="-90" y="-64" width="180" height="128" rx="10" stroke="{c}" {SW}/><path d="M-70 40 L-30 -4 L-4 24 L30 -20 L70 40" stroke="{c}" {SW}/><circle cx="50" cy="-30" r="10" stroke="{c}" {SW}/>')
KNIFE = f'<path d="M-6 -70 C20 -50 20 0 -6 20 H-16 V-70 Z M-6 20 V70 H-16 V20" stroke="{INK}" {SW}/>'
WHISK = f'<path d="M0 70 V10 M-16 10 C-30 -30 -6 -70 0 -70 C6 -70 30 -30 16 10 Z M0 10 V-70" stroke="{INK}" {SW}/>'
SPOON = f'<path d="M0 70 V0 M0 0 C-24 0 -24 -60 0 -60 C24 -60 24 0 0 0 Z" stroke="{INK}" {SW}/>'

# 1 · UNA COCINA PEQUEÑA (on face, small)
st, en = S(4), S(5) - 0.02
R.clip("kit", st, en, f'<path id="kt-c" d="M120 300 H960" stroke="{INK}" {SW8}/><path id="kt-w" d="M120 300 V120 H960 V300" stroke="{INK}" {SW}/>' + L("kt-t", "UNA COCINA PEQUEÑA", 380))
R.hidden("#kt-t", st); R.draw("#kt-c", 900, st + 0.05, 0.4); R.draw("#kt-w", 1300, st + 0.3, 0.5); R.pop("#kt-t", st + 0.8, 0.3)

# 2 · SCENE · ANI — toaster, blender, mixer (faceless, light)
st, en = S(5), E(6) + 0.15
R.scene("scA", st, en, LIGHT, f'''
  {L("an-t", "UNA COCINA PEQUEÑA", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {g("an an0", 210, 760, TOASTER(), 2.1)}{g("an an1", 540, 760, BLENDER(), 2.1)}{g("an an2", 870, 760, MIXER(), 2.1)}
  {L("an-l0", "TOSTADORA", 950, x=210, cls="wl2")}{L("an-l1", "LICUADORA", 950, x=540, cls="wl2")}{L("an-l2", "BATIDORA", 950, x=870, cls="wl2")}
  {Reel.big("an-x", "ANI", 1160, RED, x=72, anchor="start", size=150)}
  {L("an-b", "INTELIGENCIA ARTIFICIAL ESTRECHA", 1230, x=72, anchor="start", cls="wl2")}''')
R.hidden(".an, #an-l0, #an-l1, #an-l2, #an-x, #an-b, #an-t", st)
R.pop("#an-t", st + 0.15, 0.3)
for k, at in enumerate([S(5) + 0.35, S(5) + 0.95, S(5) + 1.55]): R.pop(f".an{k}", at, 0.28); R.pop(f"#an-l{k}", at + 0.1, 0.25)
R.pop("#an-x", S(6) + 0.6, 0.3); R.pop("#an-b", S(6) + 1.2, 0.3)

# 3 · USAMOS MUCHA IA — rotoscope, detection
st, en = S(7), E(9) + 0.2
R.clip("uses", st, en, f'''
  {g("us us0", 300, 200, PERSON())}
  <path id="us-r" d="M240 250 C240 200 270 186 300 186 C330 186 360 200 360 250" stroke="{RED}" stroke-width="5" stroke-dasharray="12 10" fill="none"/>
  <circle id="us-rh" cx="300" cy="154" r="36" stroke="{RED}" stroke-width="5" stroke-dasharray="12 10" fill="none"/>
  {g("us us1", 760, 200, FRAME())}
  <rect id="us-b" x="790" y="150" width="46" height="46" rx="6" stroke="{RED}" {SW}/>
  {L("us-t0", "ROTOSCOPIADO", 330, x=300)}{L("us-t1", "DETECTAR EN IMÁGENES", 330, x=760)}''')
R.hidden(".us, #us-r, #us-rh, #us-b, #us-t0, #us-t1", st)
R.pop(".us0", S(8) + 0.5, 0.28); R.show("#us-r, #us-rh", S(8) + 1.0); R.draw("#us-r, #us-rh", 300, S(8) + 1.0, 0.4); R.pop("#us-t0", S(8) + 1.1, 0.25)
R.pop(".us1", S(9) + 0.4, 0.28); R.show("#us-b", S(9) + 0.9); R.draw("#us-b", 200, S(9) + 0.9, 0.3); R.pop("#us-t1", S(9) + 1.0, 0.25)

# 4 · LA TOSTADORA NO HIERVE AGUA
st, en = S(10), E(11) + 0.2
R.clip("boil", st, en, f'''
  {g("bo bo0", 320, 230, TOASTER(), 1.3)}{g("bo bo1", 760, 240, POT(), 1.2)}
  {Reel.xmark("bo-x", 760, 230, 60, RED, 12)}
  {L("bo-t", "ESPECÍFICO · NO TODO", 400, color=RED)}''')
R.hidden(".bo1, #bo-xa, #bo-xb, #bo-t", st)
R.pop(".bo0", st + 0.1, 0.28); R.pop(".bo1", S(10) + 1.2, 0.28)
R.draw("#bo-xa, #bo-xb", 180, S(10) + 1.9, 0.2, stagger=0.12)
R.pop("#bo-t", S(11) + 1.6, 0.3)

# 5 · AGI · EL COCINERO — hat, then the tools
st, en = S(12), E(14) + 0.2
R.clip("chef", st, en, f'''
  {g("ch ch0", 540, 210, HAT(), 1.5)}
  {g("ch ch1", 250, 230, KNIFE)}{g("ch ch2", 380, 230, WHISK)}{g("ch ch3", 830, 230, SPOON)}
  {Reel.big("ch-x", "AGI", 130, RED, x=1008, anchor="end", size=110)}
  {L("ch-t", "INTELIGENCIA ARTIFICIAL GENERAL", 400)}
  {L("ch-r", "DISTINTAS RECETAS · DISTINTAS HERRAMIENTAS", 400, color=RED)}''')
R.hidden(".ch, #ch-x, #ch-t, #ch-r", st)
R.pop("#ch-x", S(12) + 1.0, 0.3); R.pop("#ch-t", S(12) + 1.5, 0.3)
R.pop(".ch0", S(13) + 0.6, 0.3)                                                    # "un cocinero"
R.pop(".ch1", S(14) + 1.6, 0.25); R.pop(".ch2", S(14) + 1.9, 0.25); R.pop(".ch3", S(14) + 2.2, 0.25)   # "distintas herramientas"
R.fade("#ch-t", S(14) + 1.5, 0.0, 0.2); R.pop("#ch-r", S(14) + 1.7, 0.3)

# 6 · ¿YA LLEGAMOS? — a slider from ANI to AGI
st, en = S(16), E(17) + 0.2
R.clip("slider", st, en, f'''
  <path id="sl-bar" d="M160 240 H920" stroke="{INK}" stroke-width="8" stroke-linecap="round" fill="none"/>
  {L("sl-a", "ANI", 310, x=160)}{L("sl-b", "AGI", 310, x=920, color=RED)}
  <g id="sl-m"><circle cx="160" cy="240" r="22" fill="{RED}"/></g>
  <text id="sl-q" x="540" y="150" text-anchor="middle" class="big" fill="{RED}" style="font-size:80px">?</text>
  {L("sl-t", "EN ALGÚN PUNTO INTERMEDIO", 400)}''')
R.hidden("#sl-a, #sl-b, #sl-m, #sl-q, #sl-t", st)
R.draw("#sl-bar", 800, st + 0.05, 0.4); R.pop("#sl-a", st + 0.3, 0.25); R.pop("#sl-b", st + 0.4, 0.25)
R.pop("#sl-q", S(16) + 0.9, 0.3)
R.pop("#sl-m", S(17) + 0.3, 0.2); R.fromTo("#sl-m", "x: 0", "x: 400", S(17) + 0.4, 1.3, "power2.out"); R.pop("#sl-t", S(17) + 1.6, 0.3)

# 7 · SCENE · UNA CABEZA DE COCINA MUY CONFUNDIDA (faceless, dark)
st, en = S(18), E(19) + 0.15
R.scene("scB", st, en, DARK, f'''
  {L("cf-t", "UNA CABEZA DE COCINA", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {g("cf cf0", 540, 760, HAT(WHITE), 2.6)}
  <text id="cf-q" x="540" y="800" text-anchor="middle" class="big" fill="{RED}" style="font-size:150px">?</text>
  {Reel.big("cf-x", "CONFUNDIDA", 1080, WHITE, x=540, size=110)}
  <path id="cf-bar" d="M120 1200 H960" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" fill="none"/>
  {L("cf-a", "ESTRECHA", 1260, x=120, anchor="start", color=WHITE, cls="wl2")}{L("cf-b", "GENERAL", 1260, x=960, anchor="end", color=RED, cls="wl2")}
  <g id="cf-m"><circle cx="120" cy="1200" r="24" fill="{RED}"/></g>''')
R.hidden("#cf-t, .cf, #cf-q, #cf-x, #cf-a, #cf-b, #cf-m", st)
R.pop("#cf-t", st + 0.15, 0.3); R.pop(".cf0", st + 0.3, 0.35); R.pop("#cf-q", st + 0.7, 0.3); R.pop("#cf-x", S(18) + 1.1, 0.3)
R.draw("#cf-bar", 900, S(19) + 0.05, 0.4); R.pop("#cf-a", S(19) + 0.3, 0.25); R.pop("#cf-b", S(19) + 0.4, 0.25)
R.pop("#cf-m", S(19) + 0.5, 0.2); R.fromTo("#cf-m", "x: 0", "x: 420", S(19) + 0.6, 1.1, "power2.out")   # "ya no está estrechamente especializada"

# 8 · TODAVÍA NO ES CONFIABLE · SIN UN CHEF HUMANO (back on face, kept in the upper part of the box)
st, en = S(20), E(21) + 0.2
R.clip("rely", st, en, f'''
  {g("ry ry0", 330, 150, HAT(), 1.1)}{Reel.xmark("ry-x", 430, 90, 26, RED, 9)}
  {g("ry ry1", 760, 150, PERSON(), 1.1)}{g("ry ry2", 760, 62, HAT(), 0.55)}
  {L("ry-a", "TODAVÍA NO ES CONFIABLE", 270, x=330, color=RED)}{L("ry-b", "SIN UN CHEF HUMANO", 270, x=760)}''')
R.hidden(".ry, #ry-xa, #ry-xb, #ry-a, #ry-b", st)
R.pop(".ry0", st + 0.2, 0.28); R.draw("#ry-xa, #ry-xb", 80, S(20) + 1.3, 0.15, stagger=0.1); R.pop("#ry-a", S(20) + 1.4, 0.25)
R.pop(".ry1", S(21) + 0.7, 0.28); R.pop(".ry2", S(21) + 0.9, 0.25); R.pop("#ry-b", S(21) + 1.0, 0.25)

R.write()
