#!/usr/bin/env python3
"""Sarier reel 5 — Unfold & Cosmos (Andy vs Instagram, Canva, Pinterest)."""
import sys; sys.path.insert(0, "..")
from reelkit import *

R = Reel("Sarier — Unfold y Cosmos", gin_scale=0.58)
S, E, L = R.S, R.E, Reel.label
R.card_frags = {1, 2, 12, 33}
R.ink_frags = {14, 15}
R.punch = {3:"Unfold",4:"historias",5:"Stories",6:"brutal",7:"stickers",8:"gratis",9:"Canva",10:"pagar",11:"gratis",13:"todo",14:"editorial",
           15:"revista",16:"12",17:"50",18:"2019",19:"playa",20:"hacer",21:"Cosmos",22:"Pinterest",23:"misma",24:"atender",25:"muro",
           26:"vueltas",27:"IA",28:"criterio",29:"bajo",30:"estándar",31:"21",32:"Chanel"}
R.rail()

# ---------------------------------------------------------------- statements
R.card("hook", 0.0, E(2) + 0.2, [
    ("a","Se enfrentó a",56,72,252,"left","left",0.72),
    ("b","Instagram, Canva",80,40,298,"left","scale",1.0, 0.9),
    ("c","y Pinterest.",100,60,364,"right","right",0.86, 2.2),
    ("d","Y ganó todas las veces.",52,60,458,"right","drop",1.0, S(2) + 0.1)])
R.card("free", S(12) - 0.05, E(12) + 0.1, [
    ("a","Gratis y bueno",100,40,252,"left","scale",1.0),
    ("b","son productos",70,60,340,"right","right",0.72, S(12) + 0.9),
    ("c","distintos.",110,60,398,"right","drop",0.86, S(12) + 1.4)], glitch_key="a")
R.glitch(S(12) + 0.15)
R.punch_cam(S(12) + 0.25)
R.card("close", S(33) - 0.1, R.DUR, [
    ("a","Dos veces contra gigantes,",56,72,252,"left","left",0.72),
    ("b","sin tecnología",100,40,300,"left","scale",1.0, S(33) + 1.0),
    ("c","nueva.",140,60,388,"right","right",0.86, S(33) + 1.7)])
R.slow_push(S(33))
R.fadeout()

# ---------------------------------------------------------------- graphics
# 1 · UNFOLD — a phone with story templates
st, en = S(3), E(5) + 0.2
R.clip("unfold", st, en, f'''<g transform="translate(540 250) scale(1.25) translate(-540 -235)">
  <rect id="uf-ph" x="440" y="30" width="200" height="380" rx="28" stroke="{INK}" {SW}/>
  <rect class="uf-f" x="470" y="70" width="140" height="90" rx="8" stroke="{INK}" {SW}/>
  <rect class="uf-f" x="470" y="175" width="140" height="90" rx="8" stroke="{RED}" {SW}/>
  <rect class="uf-f" x="470" y="280" width="140" height="90" rx="8" stroke="{INK}" {SW}/>
  <path class="uf-l" d="M490 110 H590 M490 130 H560" stroke="{INK}" {SW}/>
  <path class="uf-l" d="M490 215 H590 M490 235 H560" stroke="{RED}" {SW}/>
  <path class="uf-l" d="M490 320 H590 M490 340 H560" stroke="{INK}" {SW}/>
  </g>{L("uf-t", "UNFOLD · PLANTILLAS PARA STORIES", 500)}''')
R.hidden(".uf-f, .uf-l, #uf-t", st)
R.draw("#uf-ph", 1200, st + 0.05, 0.6)
R.draw(".uf-f", 480, S(4) + 0.3, 0.3, stagger=0.15); R.draw(".uf-l", 200, S(4) + 0.8, 0.2, stagger=0.1)
R.pop("#uf-t", S(5) + 0.6, 0.3)

# 2 · LA OBJECIÓN — Instagram and Canva give it away free; why pay Unfold?
st, en = S(6), E(11) + 0.2
def box(id_, x, w, text, color=INK):
    return (f'<rect id="{id_}" x="{x}" y="90" width="{w}" height="220" rx="22" stroke="{color}" {SW8}/>'
            f'{L(id_ + "t", text, 212, x=x + w / 2, color=color, cls="wl2")}')
R.clip("obj", st, en, box("ob-a", 60, 380, "INSTAGRAM") + box("ob-b", 640, 380, "CANVA") + f'''
  {L("ob-fa", "GRATIS", 50, x=250, color=RED, cls="wl2")}{L("ob-fb", "GRATIS", 50, x=830, color=RED, cls="wl2")}
  <rect id="ob-c" x="470" y="140" width="140" height="120" rx="14" stroke="{INK}" {SW}/>
  <text id="ob-cs" x="540" y="215" text-anchor="middle" class="big" fill="{RED}" style="font-size:64px">$</text>
  {L("ob-ct", "UNFOLD", 310, x=540)}
  {L("ob-q", "¿POR QUÉ PAGAR?", 420, color=RED, cls="wl2")}''')
R.hidden("#ob-at, #ob-bt, #ob-fa, #ob-fb, #ob-c, #ob-cs, #ob-ct, #ob-q", st)
R.draw("#ob-a", 1000, S(7) + 0.1, 0.5); R.pop("#ob-at", S(7) + 0.4, 0.25)
R.pop("#ob-fa", S(8) + 1.0, 0.3)                                                   # "gratis, integradas en la app"
R.draw("#ob-b", 1000, S(9) + 0.05, 0.5); R.pop("#ob-bt", S(9) + 0.35, 0.25); R.pop("#ob-fb", S(9) + 1.6, 0.3)
R.show("#ob-c", S(10) + 0.5); R.draw("#ob-c", 560, S(10) + 0.5, 0.4); R.pop("#ob-cs", S(10) + 0.9, 0.25); R.pop("#ob-ct", S(10) + 1.0, 0.25)
R.pop("#ob-q", S(11) + 0.3, 0.3)

# 3 · overlay · "no persiguió a todo el mundo"
st, en = S(13), S(14) - 0.02
grid = "".join(f'<circle class="cr-d" cx="{200 + (k % 10) * 76}" cy="{140 + (k // 10) * 76}" r="16" fill="{INK}"/>' for k in range(30))
R.clip("crowd", st, en, grid + L("cr-t", "NO A TODO EL MUNDO", 440))
R.hidden("#cr-t", st); R.pop(".cr-d", st + 0.05, 0.2, stagger=0.02); R.pop("#cr-t", st + 1.0, 0.3)

# 4 · SCENE · EDITORIAL — the few who wanted magazine quality (faceless, light)
st, en = S(14), E(15) + 0.15
grid = "".join(f'<circle class="ed-d" id="ed-d{k}" cx="{180 + (k % 6) * 144}" cy="{560 + (k // 6) * 130}" r="22" fill="{INK}"/>' for k in range(18))
R.scene("scA", st, en, LIGHT, f'''
  {L("ed-t", "FUE DETRÁS DE LA GENTE QUE QUERÍA", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {grid}
  <rect id="ed-m" x="180" y="1030" width="720" height="240" rx="10" stroke="{INK}" {SW8}/>
  <path id="ed-m1" d="M230 1090 H600" stroke="{INK}" stroke-width="16" stroke-linecap="round" fill="none"/>
  <path class="ed-ml" d="M230 1150 H850 M230 1185 H850 M230 1220 H700" stroke="{INK}" {SW}/>
  {Reel.big("ed-x", "EDITORIAL", 960, RED, x=180, anchor="start", size=90)}''')
R.hidden("#ed-m1, .ed-ml, #ed-x, #ed-t", st)
R.pop("#ed-t", st + 0.2, 0.3); R.pop(".ed-d", st + 0.3, 0.2, stagger=0.03)
for k in (2, 7, 9, 14): R.to(f"#ed-d{k}", f'fill: "{RED}", scale: 1.5, transformOrigin: "50% 50%"', S(14) + 1.9 + (k % 4) * 0.1, 0.3)   # "algo editorial"
R.fade(".ed-d", S(14) + 2.3, 0.35, 0.3)
for k in (2, 7, 9, 14): R.to(f"#ed-d{k}", "autoAlpha: 1", S(14) + 2.3, 0.3)
R.pop("#ed-x", S(14) + 2.2, 0.3)
R.draw("#ed-m", 2000, S(15) + 0.05, 0.6); R.draw("#ed-m1", 380, S(15) + 0.5, 0.25); R.draw(".ed-ml", 700, S(15) + 0.7, 0.3)   # "calidad de revista"

# 5 · STATS — 12M usuarios / 8 meses → $50M Squarespace 2019
st, en = S(16), E(18) + 0.2
R.clip("stats", st, en, f'''
  {Reel.big("st-12", "12M", 250, INK, x=72, anchor="start", size=200)}
  {L("st-u", "USUARIOS · 8 MESES · BOOTSTRAPPED", 330, x=72, anchor="start")}
  {Reel.big("st-50", "$50M", 250, RED, x=1008, anchor="end", size=200)}
  {L("st-s", "SQUARESPACE · 2019", 330, x=1008, anchor="end", color=RED)}''')
R.hidden("#st-12, #st-u, #st-50, #st-s", st)
R.pop("#st-12", S(16) + 0.8, 0.3); R.pop("#st-u", S(16) + 1.8, 0.3)
R.to("#st-12, #st-u", "x: -1000", S(17) + 1.0, 0.4, "power2.in")
R.pop("#st-50", S(17) + 1.6, 0.3); R.pop("#st-s", S(18) + 0.3, 0.3)

# 6 · BEACH → lo vuelve a hacer
st, en = S(19), E(20) + 0.2
R.clip("beach", st, en, f'''
  <path id="bc-u" d="M400 250 A140 140 0 0 1 680 250 Z" stroke="{INK}" {SW}/>
  <path id="bc-p" d="M540 250 V400 M540 110 V250" stroke="{INK}" {SW}/>
  <path id="bc-w" d="M300 430 Q360 400 420 430 T540 430 T660 430 T780 430" stroke="{INK}" {SW}/>
  <g id="bc-r"><path d="M880 140 A60 60 0 1 1 940 200" stroke="{RED}" {SW8}/><path d="M915 180 L940 200 L960 175" stroke="{RED}" {SW8}/></g>
  {L("bc-t", "LO VUELVE A HACER", 500, color=RED)}''')
R.hidden("#bc-r, #bc-t", st)
R.draw("#bc-u", 700, st + 0.05, 0.5); R.draw("#bc-p", 320, st + 0.3, 0.3); R.draw("#bc-w", 600, st + 0.5, 0.5)
R.pop("#bc-r", S(20) + 0.1, 0.25); R.pop("#bc-t", S(20) + 0.4, 0.3)
R.fromTo("#bc-r", 'rotation: 0, svgOrigin: "910 170"', "rotation: 720", S(20) + 0.2, E(20) - S(20), "power2.inOut")

# 7 · COSMOS — a moodboard vs the Pinterest wall
st, en = S(21), E(25) + 0.2
TILES = [(150,60,180,130),(350,60,140,200),(510,60,200,110),(730,60,200,160),(150,210,180,150),(510,190,200,170),(730,240,200,120),(350,280,140,90)]
tiles = "".join(f'<rect class="cs-t" id="cs-t{k}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" stroke="{INK}" {SW}/>' for k,(x,y,w,h) in enumerate(TILES))
R.clip("cosmos", st, en, tiles + f'''
  <rect id="cs-p" x="110" y="20" width="860" height="360" rx="14" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12" fill="none"/>
  {L("cs-pt", "PINTEREST", 435, x=930, anchor="end")}
  {L("cs-t", "COSMOS · REFERENCIAS VISUALES", 470, x=150, anchor="start", color=RED)}''')
R.hidden("#cs-p, #cs-pt, #cs-t", st)
R.draw(".cs-t", 700, st + 0.1, 0.3, stagger=0.08); R.pop("#cs-t", st + 0.5, 0.3)
R.show("#cs-p", S(22) + 1.0); R.draw("#cs-p", 2500, S(22) + 1.0, 0.7); R.pop("#cs-pt", S(22) + 1.6, 0.3)   # "Pinterest domina"
for k in (1, 5, 6): R.to(f"#cs-t{k}", f'stroke: "{RED}", strokeWidth: 9', S(24) + 1.2 + (k % 3) * 0.12, 0.3)   # "el segmento que dejó de atender"
for k, (x, y, w, h) in enumerate(TILES):                                            # "cómo se ve el muro": tiles snap to a clean grid
    gx, gy = 150 + (k % 4) * 210, 60 + (k // 4) * 170
    R.to(f"#cs-t{k}", f"x: {gx - x}, y: {gy - y}, attr: {{ width: 180, height: 140 }}", S(25) + 0.9 + k * 0.04, 0.5, "power3.inOut")

# 8 · IA chip — "Cosmos usa IA igual que todo el mundo"
st, en = S(26), E(27) + 0.2
pins = "".join(f'<path class="ia-p" d="M{460 + k * 40} 130 V100 M{460 + k * 40} 370 V400" stroke="{INK}" {SW}/>' for k in range(5))
R.clip("chip", st, en, f'''
  <rect id="ia-c" x="420" y="130" width="240" height="240" rx="20" stroke="{INK}" {SW}/>
  <rect id="ia-i" x="480" y="190" width="120" height="120" rx="10" stroke="{RED}" {SW}/>
  {pins}
  {L("ia-t", "IA · IGUAL QUE TODO EL MUNDO", 470)}''')
R.hidden("#ia-i, .ia-p, #ia-t", st)
R.draw("#ia-c", 1000, S(27) + 0.05, 0.5); R.draw(".ia-p", 40, S(27) + 0.4, 0.15, stagger=0.04); R.draw("#ia-i", 500, S(27) + 0.7, 0.3)
R.pop("#ia-t", S(27) + 1.2, 0.3)

# 9 · SCENE · CRITERIO — score the work, drop what scores low (faceless, dark)
st, en = S(28), E(29) + 0.15
SCORES = [9, 4, 8, 3, 7, 9, 2, 6, 8]
tiles = "".join(f'<rect class="cr-r" id="cr-r{k}" x="{150 + (k % 3) * 280}" y="{520 + (k // 3) * 230}" width="220" height="180" rx="14" stroke="{WHITE}" {SW}/>' for k in range(9))
nums = "".join(Reel.big(f"cr-n{k}", str(v), 640 + (k // 3) * 230, RED if v < 5 else WHITE, x=260 + (k % 3) * 280, size=90) for k, v in enumerate(SCORES))
xs = "".join(Reel.xmark(f"cr-x{k}", 260 + (k % 3) * 280, 610 + (k // 3) * 230, 60, RED, 12) for k, v in enumerate(SCORES) if v < 5)
R.scene("scB", st, en, DARK, f'''
  {L("cr-t", "LA APUNTA AL CRITERIO", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {tiles}{nums}{xs}
  {L("cr-b", "CALIFICA · QUITA LO QUE PUNTÚA BAJO", 1290, x=72, anchor="start", color=WHITE, cls="wl2")}''')
R.hidden("#cr-t, .num, #cr-b", st)
for k, v in enumerate(SCORES):
    if v < 5: R.hidden(f"#cr-x{k}a, #cr-x{k}b", st)
R.pop("#cr-t", st + 0.2, 0.3); R.draw(".cr-r", 800, st + 0.25, 0.3, stagger=0.05)
for k in range(9): R.pop(f"#cr-n{k}", S(29) + 0.3 + k * 0.09, 0.2)                 # "califica el trabajo"
for k, v in enumerate(SCORES):
    if v < 5:
        R.draw(f"#cr-x{k}a, #cr-x{k}b", 180, S(29) + 1.7 + k * 0.08, 0.2, stagger=0.1)   # "quita lo que puntúa bajo"
        R.fade(f"#cr-r{k}, #cr-n{k}", S(29) + 2.2 + k * 0.08, 0.25, 0.3)
R.pop("#cr-b", S(29) + 1.5, 0.3)

# 10 · ESTÁNDAR ≠ NÚMERO (back on face)
st, en = S(30), E(30) + 0.2
R.clip("std", st, en, f'''
  {Reel.big("sd-a", "UN ESTÁNDAR", 220, INK, x=540, size=96)}
  {Reel.big("sd-b", "UN NÚMERO", 380, INK, x=540, size=96)}
  <path id="sd-s" d="M250 350 H830" stroke="{RED}" stroke-width="14" stroke-linecap="round" fill="none"/>''')
R.hidden("#sd-a, #sd-b", st)
R.pop("#sd-a", S(30) + 1.5, 0.3); R.pop("#sd-b", S(30) + 2.4, 0.3); R.draw("#sd-s", 600, S(30) + 2.8, 0.3)

# 11 · $21M · Apple Nike Chanel
st, en = S(31), E(32) + 0.2
R.clip("money", st, en, f'''
  {Reel.big("mo-n", "$21M", 250, RED, x=540, size=220)}
  {L("mo-t", "LEVANTADOS", 330)}
  {L("mo-a", "APPLE", 460, x=300, cls="wl2")}{L("mo-b", "NIKE", 460, x=540, cls="wl2")}{L("mo-c", "CHANEL", 460, x=790, cls="wl2")}''')
R.hidden("#mo-n, #mo-t, #mo-a, #mo-b, #mo-c", st)
R.pop("#mo-n", S(31) + 1.9, 0.3); R.pop("#mo-t", S(31) + 2.4, 0.3)
R.pop("#mo-a", S(32) + 1.2, 0.25); R.pop("#mo-b", S(32) + 1.7, 0.25); R.pop("#mo-c", S(32) + 2.2, 0.25)

R.write()
