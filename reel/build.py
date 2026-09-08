#!/usr/bin/env python3
"""Sarier reel — v5: every beat is derived from fragment timings (captions.json), never hardcoded.
No backgrounds · kinetic word captions · big uneven statements (no rotation) · chained line graphics.
Colour logic on the wall: ink (#1D1D1F) = human / real · red (#E1251B) = AI / artificial."""
import json, html, math, re

W, H, FPS = 1080, 1920, 30
DUR = 73.98
VIDEO = "public/input-video.mp4"
INK, RED = "#1D1D1F", "#E1251B"

frags = json.load(open("captions.json", encoding="utf-8"))
FR = {f["i"]: f for f in frags}
def S(i): return FR[i]["start"]
def E(i): return FR[i]["end"]
CARD_FRAGS = {1, 9, 26}

GRAD = {
    "heat":     "linear-gradient(100deg, #FF3332, #FF9A4E, #FF3332)",
    "spectrum": "linear-gradient(100deg, #5470FD, #9C6CE6, #FA66C5, #5470FD)",
}
PUNCH = {2:"radio",3:"buena",4:"alguien",5:"quién",6:"tablero",7:"reconoces",8:"locutor",10:"sabor",
         11:"jamás",12:"descabellado",13:"sonido",14:"máquina",15:"resto",16:"minicrisis",17:"quién",
         18:"humano",19:"artificial",20:"separar",21:"uno",22:"alguien",23:"tiempo",24:"reflexionar",
         25:"humanidad",27:"vértigo",28:"máquina",29:"nuestra",30:"queda",31:"agota",32:"prueba",
         33:"yo",34:"todo",35:"yo"}

def esc(s): return html.escape(s, quote=True)
def norm(w): return re.sub(r"[^\wáéíóúüñ]", "", w.lower())
tl = []

# ---------------------------------------------------------------- kinetic rail
rail_html = []
for f in frags:
    if f["i"] in CARD_FRAGS: continue
    st, en = f["start"], f["end"]; d = max(0.5, en - st)
    rid = f"r{f['i']:02d}"
    words = f["text"].split()
    weights = [len(w) + 1 for w in words]; tot = sum(weights)
    spans, t = [], st
    punch = PUNCH.get(f["i"])
    for k, (w, wt) in enumerate(zip(words, weights)):
        cls = "w hot" if punch and norm(w) == norm(punch) else "w"
        spans.append(f'<span class="{cls}" id="{rid}w{k}">{esc(w)}</span>')
        tl.append(f'  tl.fromTo("#{rid}w{k}", {{ autoAlpha: 0, y: 14, scale: 0.82 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.18, ease: "power3.out" }}, {t:.2f});')
        t += (en - st) * wt / tot * 0.93
    rail_html.append(f'      <div id="{rid}" class="rail clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="2"><div class="line" id="{rid}l">{" ".join(spans)}</div></div>')
    tl.append(f'  tl.to("#{rid}l", {{ autoAlpha: 0, y: -8, duration: 0.14, ease: "power2.in" }}, {max(st, st + d - 0.14):.2f});')
    tl.append(f'  tl.set("#{rid}l", {{ autoAlpha: 0 }}, {st + d:.2f});')

# ---------------------------------------------------------------- statements — big, uneven, no rotation
CARDS = [
    ("hook",  0.00,          5.20,          "spectrum"),
    ("punch", S(9) - 0.15,   S(9) + 3.30,   "heat"),
    ("philo", S(26) - 0.16,  E(26) + 1.60,  "spectrum"),
]
STMT = {   # (key, text, size, x, y, align, enter, alpha) — all white; alpha = transparency layer
  "hook":  [("a","¿Puede la IA",84,72,252,"left","left",0.72), ("b","hacernos",180,40,312,"left","scale",1.0), ("c","pensar más?",124,60,458,"right","right",0.86)],
  "punch": [("a","Eso fue",100,90,262,"left","left",0.72), ("b","IA.",270,330,332,"left","scale",1.0)],
  "philo": [("a","¿Puede volvernos",88,80,252,"left","left",0.72), ("b","más",160,120,318,"left","drop",1.0), ("c","filosóficos?",136,60,462,"right","right",0.86)],
}
ENTER = {"left": "{ x: -80, autoAlpha: 0 }", "right": "{ x: 90, autoAlpha: 0 }",
         "scale": "{ scale: 0.6, autoAlpha: 0 }", "drop": "{ y: -60, autoAlpha: 0 }"}
card_html = []
for cid, st, en, gname in CARDS:
    d = en - st; parts = []
    for k, (key, text, size, x, y, align, enter, alpha) in enumerate(STMT[cid]):
        pid = f"{cid}-{key}"
        pos = f"left:{x}px;" if align == "left" else f"right:{x}px;"
        style = f"font-size:{size}px;"
        if cid == "punch" and key == "b":
            inner = (f'<span class="gstack" id="{cid}-stack"><span class="ghost warm" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="ghost cool" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="piece white" id="{pid}" data-layout-allow-overlap style="{style}">{esc(text)}</span></span>')
        else:
            inner = f'<span class="piece white" id="{pid}" data-layout-allow-overlap style="{style}">{esc(text)}</span>'
        parts.append(f'<div class="rot" data-layout-allow-overlap style="{pos}top:{y}px;">{inner}</div>')
        tl.append(f'  tl.fromTo("#{pid}", {ENTER[enter]}, {{ x: 0, y: 0, scale: 1, autoAlpha: {alpha}, duration: 0.6, ease: "expo.out" }}, {st + 0.05 + k * 0.14:.2f});')
    card_html.append(f'      <div id="{cid}" class="card clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                     f'        <div class="stmt" id="{cid}-in">{"".join(parts)}</div>\n      </div>')
    tl.append(f'  tl.to("#{cid}-in", {{ autoAlpha: 0, y: -20, duration: 0.30, ease: "power2.in" }}, {en - 0.30:.2f});')
    tl.append(f'  tl.set("#{cid}-in", {{ autoAlpha: 0 }}, {en:.2f});')

# glitch on "IA." + camera punch
G0 = S(9) - 0.15; GDUR, GSTEP, GMAX = 0.45, 0.05, 10
tl.append(f'''  tl.set(ghosts, {{ opacity: 0.55, x: 0, y: 0 }}, {G0:.2f});
  tl.fromTo(glitch, {{ amp: 1 }}, {{ amp: 0, duration: {GDUR}, ease: "power2.in",
    onUpdate: () => {{
      const step = Math.floor(tl.time() / {GSTEP});
      ghosts.forEach((el, layer) => {{
        gsap.set(el, {{ x: (glitchHash(step * 13 + layer * 7) * 2 - 1) * {GMAX} * glitch.amp,
                       y: (glitchHash(step * 29 + layer * 11) * 2 - 1) * 4 * glitch.amp }});
      }});
    }} }}, {G0:.2f});
  tl.set(ghosts, {{ opacity: 0, x: 0, y: 0 }}, {G0 + GDUR:.2f});''')
tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.18, ease: "expo.out" }}, {S(9) + 0.15:.2f});')
tl.append(f'  tl.to("#video-wrap", {{ scale: 1, duration: 1.4, ease: "power2.out" }}, {S(9) + 0.33:.2f});')
tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: 1.06, duration: 2.0, ease: "sine.inOut" }}, {S(27):.2f});')
tl.append(f'  tl.to("#video-wrap", {{ scale: 1, duration: 1.6, ease: "sine.inOut" }}, {S(27) + 2.0:.2f});')

# ---------------------------------------------------------------- line graphics
graphics = []
def clip(gid, st, en, inner):
    graphics.append((gid, st, en, inner))
    tl.append(f'  tl.fromTo("#{gid}-in", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.25, ease: "power2.out" }}, {st:.2f});')
    tl.append(f'  tl.to("#{gid}-in", {{ autoAlpha: 0, duration: 0.25, ease: "power2.in" }}, {en - 0.25:.2f});')
    tl.append(f'  tl.set("#{gid}-in", {{ autoAlpha: 0 }}, {en:.2f});')
def draw(sel, L, at, dur, ease="power2.out", stagger=0.0):
    tl.append(f'  tl.fromTo("{sel}", {{ strokeDasharray: "{L:.0f}", strokeDashoffset: {L:.0f} }}, {{ strokeDashoffset: 0, duration: {dur}, ease: "{ease}", stagger: {stagger} }}, {at:.2f});')
def pop(sel, at, dur=0.3, stagger=0.0):
    tl.append(f'  tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, scale: 1, duration: {dur}, ease: "power3.out", stagger: {stagger} }}, {at:.2f});')
def hidden(sel, at): tl.append(f'  tl.set("{sel}", {{ autoAlpha: 0 }}, {at:.2f});')
SW = 'stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"'

# A · equalizer — after the hook, until "de quién"
EQ_ST, EQ_EN, NB = 5.30, E(5), 16
lo  = [0.18,0.30,0.22,0.40,0.26,0.34,0.20,0.44,0.28,0.36,0.24,0.32,0.20,0.38,0.26,0.30]
hi  = [0.70,1.00,0.82,0.62,0.94,0.76,1.00,0.68,0.88,0.58,0.96,0.72,0.84,0.66,0.90,0.60]
per = [0.46,0.58,0.40,0.66,0.52,0.44,0.60,0.48,0.56,0.42,0.64,0.50,0.38,0.62,0.54,0.47]
eq_inner = '<div class="eq" id="eq-in">' + "".join(f'<div class="bar" id="eqb{i}"></div>' for i in range(NB)) + '</div>'
graphics.append(("eq", EQ_ST, EQ_EN, None))
tl.append(f'  tl.fromTo("#eq-in", {{ autoAlpha: 0, y: 20 }}, {{ autoAlpha: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {EQ_ST:.2f});')
win = EQ_EN - EQ_ST - 0.35
for i in range(NB):
    half = per[i] / 2; reps = max(1, int(win / half) - 1)
    tl.append(f'  tl.fromTo("#eqb{i}", {{ scaleY: {lo[i]} }}, {{ scaleY: {hi[i]}, duration: {half:.3f}, ease: "sine.inOut", yoyo: true, repeat: {reps} }}, {EQ_ST + 0.1:.2f});')
tl.append(f'  tl.to("#eq-in", {{ autoAlpha: 0, y: -10, duration: 0.25, ease: "power2.in" }}, {EQ_EN - 0.25:.2f});')
tl.append(f'  tl.set("#eq-in", {{ autoAlpha: 0 }}, {EQ_EN:.2f});')

# B · dashboard — "tablero del carro" → "?" on "no lo reconoces"
st, en = S(6), E(7)
clip("dash", st, en, f'''
  <rect id="dash-scr" x="230" y="150" width="620" height="220" rx="24" stroke="{INK}" {SW}/>
  <circle id="dash-note" cx="318" cy="292" r="16" stroke="{INK}" {SW}/>
  <path id="dash-stem" d="M334 292 V212 l40 -12" stroke="{INK}" {SW}/>
  <path class="dash-d" d="M420 260 h70" stroke="{INK}" {SW}/><path class="dash-d" d="M510 260 h70" stroke="{INK}" {SW}/>
  <path class="dash-d" d="M600 260 h70" stroke="{INK}" {SW}/><path class="dash-d" d="M690 260 h70" stroke="{INK}" {SW}/>
  <text id="dash-q" x="790" y="285" text-anchor="middle" class="big" fill="{RED}">?</text>''')
draw("#dash-scr", 1700, st + 0.03, 0.9); draw("#dash-note", 110, st + 0.6, 0.35); draw("#dash-stem", 140, st + 0.75, 0.35)
draw(".dash-d", 80, st + 1.05, 0.18, stagger=0.16)
hidden("#dash-q", st); pop("#dash-q", S(7) + 0.05, 0.28)

# C · radio waves — "el locutor dice"
st, en = S(8), S(9) - 0.02
clip("radio", st, en, f'''
  <circle id="radio-dot" cx="540" cy="330" r="14" fill="{RED}"/>
  <path class="radio-a" d="M462 262 a110 110 0 0 1 156 0" stroke="{INK}" {SW}/>
  <path class="radio-a" d="M414 214 a178 178 0 0 1 252 0" stroke="{INK}" {SW}/>
  <path class="radio-a" d="M366 166 a246 246 0 0 1 348 0" stroke="{INK}" {SW}/>''')
hidden("#radio-dot", st); pop("#radio-dot", st + 0.07, 0.25); draw(".radio-a", 900, st + 0.2, 0.55, stagger=0.22)

# D · chip — "una máquina"
st, en = S(13), E(14)
pins = "".join(f'<path class="chip-p" d="M{x} 150 v-30" stroke="{RED}" {SW}/><path class="chip-p" d="M{x} 370 v30" stroke="{RED}" {SW}/>' for x in (470,517,563,610))
pins += "".join(f'<path class="chip-p" d="M430 {y} h-30" stroke="{RED}" {SW}/><path class="chip-p" d="M650 {y} h30" stroke="{RED}" {SW}/>' for y in (200,247,293,340))
clip("chip", st, en, f'''
  <rect id="chip-b" x="430" y="150" width="220" height="220" rx="22" stroke="{RED}" {SW}/>
  <rect id="chip-c" x="500" y="220" width="80" height="80" rx="10" stroke="{RED}" {SW}/>
  {pins}
  <text id="chip-t" x="540" y="470" text-anchor="middle" class="wl" fill="{RED}">MÁQUINA</text>''')
draw("#chip-b", 900, st + 0.06, 0.8); draw("#chip-c", 340, st + 0.66, 0.4); draw(".chip-p", 40, st + 0.86, 0.12, stagger=0.04)
hidden("#chip-t", st); pop("#chip-t", E(14) - 1.0, 0.3)

# E · clock — "El resto del día" (frag 15 only)
st, en = S(15), S(16)
ticks = "".join(f'<path class="clk-t" d="M540 120 v18" transform="rotate({a} 540 260)" stroke="{INK}" {SW}/>' for a in (0,90,180,270))
clip("clock", st, en, f'''
  <circle id="clk-r" cx="540" cy="260" r="140" stroke="{INK}" {SW} transform="rotate(-90 540 260)"/>
  {ticks}
  <path id="clk-h" d="M540 260 V150" stroke="{RED}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <circle cx="540" cy="260" r="9" fill="{INK}"/>''')
draw("#clk-r", 900, st + 0.05, 0.7); draw(".clk-t", 30, st + 0.5, 0.15, stagger=0.06)
tl.append(f'  tl.fromTo("#clk-h", {{ rotation: 0, svgOrigin: "540 260" }}, {{ rotation: 330, duration: {en - st - 0.9:.2f}, ease: "power1.inOut" }}, {st + 0.6:.2f});')

# F · minicrisis — "como una minicrisis existencial impulsada por la IA"
st, en = S(16), E(16)
clip("crisis", st, en, f'''
  <path id="cr-l" d="M120 260 H430" stroke="{INK}" {SW}/>
  <g id="cr-m"><path id="cr-mp" d="M430 260 L455 196 L480 334 L505 164 L530 346 L555 184 L580 322 L605 206 L630 300 L655 236 L680 278 L700 260" stroke="{RED}" {SW}/></g>
  <path id="cr-r" d="M700 260 H960" stroke="{INK}" {SW}/>
  <text id="cr-t" x="540" y="440" text-anchor="middle" class="wl" fill="{INK}">MINICRISIS EXISTENCIAL</text>
  <text id="cr-ia" x="565" y="128" text-anchor="middle" class="wl" fill="{RED}">IA</text>''')
draw("#cr-l", 330, st + 0.05, 0.45, ease="none"); draw("#cr-mp", 1500, st + 0.5, 0.9, ease="power1.in"); draw("#cr-r", 280, st + 1.4, 0.35, ease="none")
hidden("#cr-t", st); hidden("#cr-ia", st); pop("#cr-t", st + 0.9, 0.3); pop("#cr-ia", st + 1.75, 0.25)
SH0, SHD = st + 1.75, 0.85
tl.append(f'''  tl.fromTo(crisis, {{ amp: 1 }}, {{ amp: 0, duration: {SHD}, ease: "power2.in",
    onUpdate: () => {{
      const step = Math.floor(tl.time() / 0.04);
      gsap.set("#cr-m", {{ x: (glitchHash(step * 17 + 3) * 2 - 1) * 9 * crisis.amp, y: (glitchHash(step * 23 + 5) * 2 - 1) * 9 * crisis.amp }});
      gsap.set("#video-wrap", {{ x: (glitchHash(step * 31 + 9) * 2 - 1) * 4 * crisis.amp, y: (glitchHash(step * 37 + 1) * 2 - 1) * 4 * crisis.amp }});
    }} }}, {SH0:.2f});
  tl.set("#cr-m", {{ x: 0, y: 0 }}, {SH0 + SHD:.2f});
  tl.set("#video-wrap", {{ x: 0, y: 0 }}, {SH0 + SHD:.2f});''')

# G · human — "Piensas en quién eres / ser humano"
st, en = S(17), E(18)
clip("human", st, en, f'''
  <circle id="hu-head" cx="540" cy="200" r="52" stroke="{INK}" {SW} transform="rotate(-90 540 200)"/>
  <path id="hu-body" d="M400 400 a140 140 0 0 1 280 0" stroke="{INK}" {SW}/>
  <text id="hu-t" x="540" y="470" text-anchor="middle" class="wl" fill="{INK}">HUMANO</text>''')
draw("#hu-head", 340, st + 0.05, 0.6); draw("#hu-body", 460, st + 0.5, 0.7)
hidden("#hu-t", st); pop("#hu-t", S(18) + 0.5, 0.3)

# H · two worlds → one
st, en = S(19), E(21) + 0.6
R = 150; CIRC = 2 * math.pi * R
clip("worlds", st, en, f'''
  <g id="gA"><circle id="cA" cx="330" cy="230" r="{R}" stroke="{INK}" {SW} transform="rotate(-90 330 230)"/>
    <text id="tA" x="330" y="460" text-anchor="middle" class="wl" fill="{INK}">MUNDO REAL</text></g>
  <g id="gB"><circle id="cB" cx="750" cy="230" r="{R}" stroke="{RED}" {SW} transform="rotate(-90 750 230)"/>
    <text id="tB" x="750" y="460" text-anchor="middle" class="wl" fill="{RED}">MUNDO ARTIFICIAL</text></g>
  <text id="tOne" x="540" y="460" text-anchor="middle" class="wl" fill="{INK}">UNO SOLO</text>''')
hidden("#tA, #tB, #tOne", st)
draw("#cA, #cB", CIRC + 10, st + 0.1, 1.1, stagger=0.15)
tl.append(f'  tl.to(["#tA","#tB"], {{ autoAlpha: 1, duration: 0.35, ease: "power2.out", stagger: 0.1 }}, {st + 1.0:.2f});')
dr = S(20); meet = S(21) + 0.2
tl.append(f'  tl.fromTo("#gA", {{ x: 0 }}, {{ x: 210, duration: {meet - dr:.2f}, ease: "sine.inOut" }}, {dr:.2f});')
tl.append(f'  tl.fromTo("#gB", {{ x: 0 }}, {{ x: -210, duration: {meet - dr:.2f}, ease: "sine.inOut" }}, {dr:.2f});')
tl.append(f'  tl.to(["#tA","#tB"], {{ autoAlpha: 0, duration: 0.3, ease: "power2.in" }}, {dr + 0.25:.2f});')
tl.append(f'  tl.to("#cB", {{ stroke: "{INK}", duration: 0.5, ease: "power2.out" }}, {meet - 0.2:.2f});')
tl.append(f'  tl.to("#tOne", {{ autoAlpha: 1, duration: 0.35, ease: "power2.out" }}, {S(21) + 0.9:.2f});')

# J · five circles — "una cosa más … qué nos queda … un yo que perder"
st, en = S(28), E(33)
xs = (280, 410, 540, 670, 800)
five = "".join(f'<circle class="fv" id="fv{i}" cx="{x}" cy="260" r="46" stroke="{INK}" {SW} transform="rotate(-90 {x} 260)"/>' for i, x in enumerate(xs))
clip("five", st, en, f'''{five}
  <text id="fv-t" x="800" y="380" text-anchor="middle" class="wl" fill="{INK}">YO</text>''')
draw(".fv", 300, st + 0.06, 0.5, stagger=0.08)
span = E(28) - S(28)
for i, k in enumerate((0.32, 0.55, 0.78, 1.0)):
    at = S(28) + span * k if i < 3 else S(29) + 0.15
    tl.append(f'  tl.to("#fv{i}", {{ fill: "{RED}", stroke: "{RED}", duration: 0.28, ease: "power3.out" }}, {at:.2f});')
tl.append(f'  tl.fromTo("#fv4", {{ scale: 1, transformOrigin: "50% 50%" }}, {{ scale: 1.14, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {S(30) + 0.05:.2f});')
tl.append(f'  tl.to("#fv4", {{ fill: "{INK}", duration: 0.35, ease: "power3.out" }}, {S(33) + 1.5:.2f});')
hidden("#fv-t", st); pop("#fv-t", S(33) + 1.8, 0.3)

# L · big question mark — "sigue cuestionándolo todo"
st, en = S(34), E(35) + 0.4
clip("qm", st, en, f'''
  <path id="qm-p" d="M450 200 a90 90 0 1 1 122 84 c-26 12 -32 30 -32 60" stroke="{INK}" stroke-width="10" stroke-linecap="round" fill="none"/>
  <circle id="qm-d" cx="540" cy="400" r="11" fill="{RED}"/>''')
draw("#qm-p", 620, st + 0.1, 1.1); hidden("#qm-d", st); pop("#qm-d", st + 1.3, 0.25)

# ---------------------------------------------------------------- assemble
g_html = []
for gid, st, en, inner in graphics:
    d = en - st
    if gid == "eq":
        g_html.append(f'      <div id="eq" class="mg clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">{eq_inner}</div>')
    else:
        g_html.append(f'      <div id="{gid}" class="mg clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                      f'        <div id="{gid}-in" class="gin"><svg width="1080" height="520" viewBox="0 0 1080 520">{inner}\n        </svg></div>\n      </div>')

page = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Sarier — ¿Puede la IA hacernos pensar más?</title>
    <script src="public/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Archivo"; src: url("public/fonts/Archivo-600-latin.woff2") format("woff2"); font-weight: 500 700; font-display: block; }}
      :root {{ --ink: {INK}; --on-dark: #FFFFFF; --red: {RED}; --tr-display: -0.035em; --tr-body: -0.01em; --tr-caps: 0.08em;
        --sh-rail: 0 2px 2px rgba(0,0,0,0.45), 0 4px 22px rgba(0,0,0,0.45); }}
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000;
        font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; -webkit-font-smoothing: antialiased; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; }}
      #video-wrap {{ position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 45%; }}
      #video-wrap video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

      .rail {{ position: absolute; left: 0; right: 0; top: 1300px; display: flex; justify-content: center; pointer-events: none; }}
      .rail .line {{ max-width: 960px; text-align: center; text-wrap: balance; color: var(--on-dark); font-weight: 700; font-size: 62px; line-height: 1.15; letter-spacing: var(--tr-body); text-shadow: var(--sh-rail); }}
      .rail .w {{ display: inline-block; }}
      .rail .w.hot {{ color: var(--red); text-shadow: 0 0 2px rgba(255,255,255,0.55), 0 0 12px rgba(255,255,255,0.45), 0 2px 2px rgba(0,0,0,0.35); }}

      .card {{ position: absolute; left: 0; top: 0; width: {W}px; height: 680px; pointer-events: none; }}
      .stmt {{ position: absolute; inset: 0; }}
      .stmt .rot {{ position: absolute; white-space: nowrap; }}
      .piece {{ display: inline-block; font-weight: 600; line-height: 0.9; letter-spacing: var(--tr-display); }}
      .piece.white {{ color: #FFFFFF; text-shadow: 0 2px 3px rgba(0,0,0,0.35), 0 6px 28px rgba(0,0,0,0.38); }}
      .gstack {{ display: grid; }}
      .gstack > span {{ grid-area: 1 / 1; display: inline-block; font-size: 270px; font-weight: 600; line-height: 0.9; letter-spacing: var(--tr-display); }}
      .gstack .ghost {{ opacity: 0; }}
      .gstack .warm {{ color: #FF3332; }}
      .gstack .cool {{ color: #5470FD; }}

      .mg {{ position: absolute; left: 0; top: 0; width: {W}px; pointer-events: none; }}
      .gin {{ position: absolute; left: 0; top: 236px; transform: scale(0.70); transform-origin: top center; }}
      .mg svg {{ display: block; }}
      .wl {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: var(--tr-caps); }}
      .big {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; font-size: 84px; }}
      #eq {{ top: 330px; display: flex; justify-content: center; }}
      .eq {{ display: flex; align-items: flex-end; gap: 16px; }}
      .eq .bar {{ width: 18px; height: 160px; background: var(--ink); border-radius: 9px; transform-origin: bottom center; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <div id="video-wrap">
        <video id="src" src="{VIDEO}" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video>
      </div>
      <audio id="voice" src="{VIDEO}" data-start="0" data-duration="{DUR}" data-volume="1"></audio>

{chr(10).join(rail_html)}

{chr(10).join(g_html)}

{chr(10).join(card_html)}
    </div>
    <script>
      const glitchHash = (n) => {{ const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); }};
      const ghosts = gsap.utils.toArray("#punch-stack .ghost");
      const glitch = {{ amp: 0 }};
      const crisis = {{ amp: 0 }};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(page)
print(f"index.html: {len(rail_html)} rail clips, {len(CARDS)} statements, {len(graphics)} graphics, {len(tl)} tweens")
