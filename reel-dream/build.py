#!/usr/bin/env python3
"""Sarier reel 3 — "¿Por qué soñamos?" (overfitting / dreams). v2: pauses cut + two faceless scenes.
Same language as reels 1-2: no backgrounds on text · kinetic word captions · big uneven white statements ·
chained line graphics. Two full-screen faceless explainers: OVERFIT (light surface) and NIGHT (dark surface).
Every beat derives from captions.cut.json (timings remapped after cutting the pauses). ink = human · red = AI."""
import json, html, re, subprocess

W, H, FPS = 1080, 1920, 25
VIDEO = "public/input-video.mp4"
DUR = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VIDEO],
                                 capture_output=True, text=True).stdout) - 0.02, 2)
INK, RED = "#1D1D1F", "#E1251B"
LIGHT, DARK, WHITE = "#F5F5F7", "#161618", "#FFFFFF"

frags = json.load(open("captions.cut.json", encoding="utf-8"))
FR = {f["i"]: f for f in frags}
def S(i): return FR[i]["start"]
def E(i): return FR[i]["end"]
CARD_FRAGS = {1, 2, 9, 10, 25, 26}
SCENE_A = {3, 4, 5, 6, 7, 8}          # faceless · overfitting (light)
SCENE_B = {18, 19, 20, 21, 22, 23}    # faceless · night (dark)

PUNCH = {3:"vez",4:"romperse",5:"patrón",6:"memorizar",7:"memorizados",8:"nuevo",11:"2021",12:"cerebro",
         13:"misma",14:"mismas",15:"bucle",16:"ayer",17:"mañana",18:"extraño",19:"ocurrieron",20:"imposibles",
         21:"nunca",22:"entrenamiento",23:"vivido",24:"nuevas"}

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
    lcls = "line ink" if f["i"] in SCENE_A else "line"
    rail_html.append(f'      <div id="{rid}" class="rail clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="2"><div class="{lcls}" id="{rid}l">{" ".join(spans)}</div></div>')
    tl.append(f'  tl.to("#{rid}l", {{ autoAlpha: 0, y: -8, duration: 0.14, ease: "power2.in" }}, {max(st, st + d - 0.14):.2f});')
    tl.append(f'  tl.set("#{rid}l", {{ autoAlpha: 0 }}, {st + d:.2f});')

# ---------------------------------------------------------------- statements
CARDS = [
    ("hook",    0.00,         E(2) + 0.2),
    ("overfit", S(9) - 0.05,  E(10) + 0.3),
    ("close",   S(25) - 0.10, DUR),
]
# (key, text, size, x, y, align, enter, alpha[, at]) — all white; alpha = transparency layer; at = absolute enter time
STMT = {
  "hook":    [("a","Cien años sin entender",72,72,252,"left","left",0.72), ("b","por qué",210,40,302,"left","scale",1.0),
              ("c","soñamos.",150,60,470,"right","right",0.86), ("d","La respuesta: machine learning.",56,60,612,"right","drop",0.86, S(2) + 0.35)],
  "overfit": [("a","Se llama",84,72,252,"left","left",0.72), ("b","sobreajuste.",150,40,312,"left","scale",1.0),
              ("c","Overfitting.",110,60,452,"right","right",0.86, S(10) + 0.05)],
  "close":   [("a","No soñamos porque dormimos.",62,72,252,"left","left",0.72), ("b","Dormimos",180,40,302,"left","scale",1.0, S(26) + 0.05),
              ("c","para soñar.",120,60,464,"right","right",0.86, S(26) + 0.95)],
}
ENTER = {"left": "{ x: -80, autoAlpha: 0 }", "right": "{ x: 90, autoAlpha: 0 }",
         "scale": "{ scale: 0.6, autoAlpha: 0 }", "drop": "{ y: -60, autoAlpha: 0 }"}
card_html = []
for cid, st, en in CARDS:
    d = en - st; parts = []
    for k, piece in enumerate(STMT[cid]):
        key, text, size, x, y, align, enter, alpha = piece[:8]
        at = piece[8] if len(piece) > 8 else st + 0.05 + k * 0.14
        pid = f"{cid}-{key}"
        pos = f"left:{x}px;" if align == "left" else f"right:{x}px;"
        style = f"font-size:{size}px;"
        if cid == "overfit" and key == "b":
            inner = (f'<span class="gstack" id="{cid}-stack" style="{style}"><span class="ghost warm" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="ghost cool" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="piece white" id="{pid}" data-layout-allow-overlap>{esc(text)}</span></span>')
        else:
            inner = f'<span class="piece white" id="{pid}" data-layout-allow-overlap style="{style}">{esc(text)}</span>'
        parts.append(f'<div class="rot" data-layout-allow-overlap style="{pos}top:{y}px;">{inner}</div>')
        tl.append(f'  tl.fromTo("#{pid}", {ENTER[enter]}, {{ x: 0, y: 0, scale: 1, autoAlpha: {alpha}, duration: 0.6, ease: "expo.out" }}, {at:.2f});')
    card_html.append(f'      <div id="{cid}" class="card clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                     f'        <div class="stmt" id="{cid}-in">{"".join(parts)}</div>\n      </div>')
    if en < DUR - 0.05:
        tl.append(f'  tl.to("#{cid}-in", {{ autoAlpha: 0, y: -20, duration: 0.30, ease: "power2.in" }}, {en - 0.30:.2f});')
        tl.append(f'  tl.set("#{cid}-in", {{ autoAlpha: 0 }}, {en:.2f});')

# glitch on "sobreajuste." (the model breaking) + camera punches
G0 = S(9) + 0.10; GDUR, GSTEP, GMAX = 0.5, 0.05, 12
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
def punch_cam(at, amount=1.05, hold=0.18, back=1.4, sel="#video-wrap"):
    tl.append(f'  tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: {amount}, duration: {hold}, ease: "expo.out" }}, {at:.2f});')
    tl.append(f'  tl.to("{sel}", {{ scale: 1, duration: {back}, ease: "power2.out" }}, {at + hold:.2f});')
punch_cam(S(10) + 0.05)                      # "Overfitting."
punch_cam(S(15) + 0.9, 1.04, 0.16, 1.2)      # "en bucle"
tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: 1.05, duration: 2.2, ease: "sine.inOut" }}, {S(26):.2f});')

# ---------------------------------------------------------------- helpers
graphics, scenes = [], []
def clip(gid, st, en, inner):
    graphics.append((gid, st, en, inner))
    tl.append(f'  tl.fromTo("#{gid}-in", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.25, ease: "power2.out" }}, {st:.2f});')
    tl.append(f'  tl.to("#{gid}-in", {{ autoAlpha: 0, duration: 0.25, ease: "power2.in" }}, {en - 0.25:.2f});')
    tl.append(f'  tl.set("#{gid}-in", {{ autoAlpha: 0 }}, {en:.2f});')
def scene(sid, st, en, bg, inner):
    scenes.append((sid, st, en, bg, inner))
    tl.append(f'  tl.fromTo("#{sid}-in", {{ autoAlpha: 0, scale: 1.05 }}, {{ autoAlpha: 1, scale: 1, duration: 0.2, ease: "power2.out" }}, {st:.2f});')
    tl.append(f'  tl.to("#{sid}-in", {{ autoAlpha: 0, duration: 0.15, ease: "power2.in" }}, {en - 0.15:.2f});')
    tl.append(f'  tl.set("#{sid}-in", {{ autoAlpha: 0 }}, {en:.2f});')
def draw(sel, L, at, dur, ease="power2.out", stagger=0.0):
    tl.append(f'  tl.fromTo("{sel}", {{ strokeDasharray: "{L:.0f}", strokeDashoffset: {L:.0f} }}, {{ strokeDashoffset: 0, duration: {dur}, ease: "{ease}", stagger: {stagger} }}, {at:.2f});')
def pop(sel, at, dur=0.3, stagger=0.0):
    tl.append(f'  tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, scale: 1, duration: {dur}, ease: "power3.out", stagger: {stagger} }}, {at:.2f});')
def fade(sel, at, to=0.0, dur=0.3): tl.append(f'  tl.to("{sel}", {{ autoAlpha: {to}, duration: {dur}, ease: "power2.inOut" }}, {at:.2f});')
def hidden(sel, at): tl.append(f'  tl.set("{sel}", {{ autoAlpha: 0 }}, {at:.2f});')
SW = 'stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
SW8 = 'stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"'
def label(id_, text, y=470, color=INK, x=540, anchor="middle", cls="wl"):
    return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" fill="{color}">{text}</text>'

BRAIN = ("M540 105 C640 85 745 150 745 250 C745 340 655 405 565 392 C525 420 445 412 420 372 "
         "C340 362 322 282 350 222 C338 150 440 95 540 105 Z")
BRAIN_FISSURE = "M540 105 C572 180 518 265 552 392"
BRAIN_GYRI = ["M400 240 C430 210 470 215 490 245", "M600 200 C640 175 690 190 705 230", "M450 320 C480 300 520 305 540 335", "M600 300 C630 280 675 285 690 320"]
def brain(prefix, color=INK, extra="", sw=SW):
    g = "".join(f'<path class="{prefix}-gy" d="{d}" stroke="{color}" {sw}/>' for d in BRAIN_GYRI)
    return (f'<g id="{prefix}-g" {extra}><path id="{prefix}-o" d="{BRAIN}" stroke="{color}" {sw}/>'
            f'<path id="{prefix}-f" d="{BRAIN_FISSURE}" stroke="{color}" {sw}/>{g}</g>')

# ================================================================ SCENE A · OVERFIT (faceless, light)
DOTS = [(180,300),(280,230),(380,200),(480,260),(580,320),(680,280),(780,210),(880,240)]
st, en = S(3), E(8) + 0.15
dots = "".join(f'<circle class="sa-d" id="sa-d{k}" cx="{x}" cy="{y}" r="20" fill="{INK}"/>' for k,(x,y) in enumerate(DOTS))
jag = "M180 300 L230 170 L280 230 L330 330 L380 200 L430 120 L480 260 L530 380 L580 320 L630 180 L680 280 L730 360 L780 210 L830 130 L880 240"
counters = "".join(f'<text class="cnt" id="sa-c{k}" x="1008" y="560" text-anchor="end" fill="{INK if k < 4 else RED}">{t}</text>'
                   for k, t in enumerate(["×1", "×2", "×3", "×4", "×∞"]))
scene("scA", st, en, LIGHT, f'''
  {label("sa-t", "MODELO DE IA · MISMOS DATOS", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {counters}
  <g transform="translate(0 640)">
    {dots}
    <path id="sa-s" d="M180 300 C270 220 350 190 450 240 S620 330 720 270 S840 220 880 240" stroke="{INK}" {SW8}/>
    <path id="sa-j" d="{jag}" stroke="{RED}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <circle id="sa-n" cx="1000" cy="260" r="20" fill="{INK}"/>
    {label("sa-nt", "NUEVO", y=200, x=1000, cls="wl2")}
    <path id="sa-x1" d="M964 224 L1036 296" stroke="{RED}" stroke-width="12" stroke-linecap="round" fill="none"/>
    <path id="sa-x2" d="M1036 224 L964 296" stroke="{RED}" stroke-width="12" stroke-linecap="round" fill="none"/>
  </g>
  {label("sa-p", "PATRÓN", y=1130, x=180, anchor="start", cls="wl2")}
  <path id="sa-ps" d="M166 1116 L342 1116" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  {label("sa-m", "MEMORIZA", y=1130, x=900, anchor="end", color=RED, cls="wl2")}''')
hidden(".sa-d, .cnt, #sa-t, #sa-n, #sa-nt, #sa-p, #sa-m", st)
pop("#sa-t", st + 0.25, 0.3)
pop(".sa-d", st + 0.35, 0.25, stagger=0.07)
draw("#sa-s", 900, st + 1.0, 0.8); pop("#sa-p", st + 1.5, 0.3)
for k, at in enumerate([S(3) + 1.7, S(3) + 2.15, S(3) + 2.6, S(3) + 3.0]):       # "una y otra vez": ×1 ×2 ×3 ×4
    if k: hidden(f"#sa-c{k-1}", at)
    pop(f"#sa-c{k}", at, 0.18)
hidden("#sa-c3", S(4) + 0.1); pop("#sa-c4", S(4) + 0.1, 0.25)                     # ×∞
punch_cam(S(4) + 0.3, 1.03, 0.14, 1.0, sel="#scA-in")                             # "empieza a romperse"
draw("#sa-j", 2200, S(4) + 0.15, 0.7, ease="power3.in")
fade("#sa-s", S(5) + 0.3, 0.18, 0.5); draw("#sa-ps", 180, S(5) + 0.5, 0.2)       # "deja de aprender el patrón"
pop("#sa-m", S(6) + 0.6, 0.3)                                                     # "empieza a memorizar los ejemplos"
for k in range(len(DOTS)):
    at = S(6) + 0.7 + k * 0.16
    tl.append(f'  tl.fromTo("#sa-d{k}", {{ fill: "{INK}", scale: 1, transformOrigin: "50% 50%" }}, {{ fill: "{RED}", scale: 1.6, duration: 0.14, yoyo: true, repeat: 1 }}, {at:.2f});')
tl.append(f'  tl.fromTo("#sa-j", {{ strokeWidth: 10 }}, {{ strokeWidth: 16, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {S(7) + 0.4:.2f});')
pop("#sa-n", S(8) + 0.9, 0.25); pop("#sa-nt", S(8) + 1.0, 0.25)                  # "algo nuevo" → can't reach it
draw("#sa-x1, #sa-x2", 110, S(8) + 1.5, 0.18, stagger=0.12)

# ================================================================ overlay · BRAIN (on face)
st, en = S(11), E(12) + 0.2
clip("brain", st, en, brain("br") + f'''
  <path id="br-j" d="M400 220 L430 160 L460 265 L490 180 L520 305 L550 200 L580 295 L610 170 L640 265 L670 205" stroke="{RED}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  {label("br-y", "2021", y=470, x=540, color=RED)}
  {label("br-t", "TU CEREBRO")}''')
draw("#br-o", 1500, st + 0.05, 0.9); draw("#br-f", 320, st + 0.6, 0.4); draw(".br-gy", 140, st + 0.8, 0.3, stagger=0.08)
hidden("#br-y", st); hidden("#br-t", st); pop("#br-y", st + 0.4, 0.3)
fade("#br-y", S(12) + 0.2, 0.0, 0.2); pop("#br-t", S(12) + 0.4, 0.3)
draw("#br-j", 900, S(12) + 1.1, 0.6, ease="power3.in")

# ================================================================ overlay · SAME DAY (on face)
st, en = S(13), E(15) + 0.2
def face(prefix, cx, cy):
    return (f'<g class="{prefix}-face"><circle cx="{cx}" cy="{cy}" r="36" fill="#FFFFFF" stroke="{INK}" {SW}/>'
            f'<circle cx="{cx-12}" cy="{cy-8}" r="4" fill="{INK}"/><circle cx="{cx+12}" cy="{cy-8}" r="4" fill="{INK}"/>'
            f'<path d="M{cx-12} {cy+10} Q{cx} {cy+20} {cx+12} {cy+10}" stroke="{INK}" {SW}/></g>')
clip("day", st, en, f'''
  <circle id="dy-ring" cx="540" cy="250" r="150" stroke="{INK}" {SW} transform="rotate(-90 540 250)"/>
  <circle id="dy-red" cx="540" cy="250" r="150" stroke="{RED}" stroke-width="8" fill="none" transform="rotate(-90 540 250)"/>
  <g id="dy-orb"><circle cx="540" cy="100" r="14" fill="{INK}"/></g>
  {face("dy", 540, 400)}{face("dy", 410, 175)}{face("dy", 670, 175)}
  {label("dy-t", "EL MISMO DÍA")}
  {label("dy-b", "EN BUCLE", color=RED)}''')
draw("#dy-ring", 960, st + 0.05, 0.8)
hidden("#dy-orb", st); hidden(".dy-face", st); hidden("#dy-t", st); hidden("#dy-b", st); hidden("#dy-red", st)
pop("#dy-t", st + 0.5, 0.3); pop("#dy-orb", st + 0.8, 0.2)
ORB = E(14) - st - 0.9
tl.append(f'  tl.fromTo("#dy-orb", {{ rotation: 0, svgOrigin: "540 250" }}, {{ rotation: 720, duration: {ORB:.2f}, ease: "none" }}, {st + 0.9:.2f});')
pop(".dy-face", S(14) + 0.7, 0.25, stagger=0.14)
draw("#dy-red", 960, S(15) + 0.9, 0.7, ease="power2.inOut")
fade("#dy-t", S(15) + 0.9, 0.0, 0.2); pop("#dy-b", S(15) + 1.0, 0.3)
tl.append(f'  tl.fromTo("#dy-orb", {{ rotation: 720 }}, {{ rotation: 1800, duration: {E(15) + 0.2 - S(15) - 0.9:.2f}, ease: "power2.in" }}, {S(15) + 0.9:.2f});')

# ================================================================ overlay · AYER / MAÑANA (on face)
st, en = S(16), E(17) + 0.2
clip("when", st, en, f'''
  <rect id="wh-a" x="270" y="140" width="220" height="220" rx="22" stroke="{INK}" {SW}/>
  <rect id="wh-b" x="590" y="140" width="220" height="220" rx="22" stroke="{INK}" {SW}/>
  <path id="wh-ok" d="M325 255 L365 300 L440 200" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path id="wh-x1" d="M650 200 L750 300" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  <path id="wh-x2" d="M750 200 L650 300" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  {label("wh-ta", "AYER", y=420, x=380)}
  {label("wh-tb", "MAÑANA", y=420, x=700, color=RED)}''')
draw("#wh-a", 900, st + 0.05, 0.6); hidden("#wh-ta", st); hidden("#wh-tb", st); hidden("#wh-b", st)
pop("#wh-ta", st + 0.4, 0.3); draw("#wh-ok", 220, st + 0.9, 0.35)
tl.append(f'  tl.set("#wh-b", {{ autoAlpha: 1 }}, {S(17):.2f});')
draw("#wh-b", 900, S(17) + 0.05, 0.6); pop("#wh-tb", S(17) + 0.4, 0.3)
draw("#wh-x1, #wh-x2", 160, S(17) + 0.9, 0.22, stagger=0.15)

# ================================================================ SCENE B · NIGHT (faceless, dark)
st, en = S(18), E(23) + 0.15
def spark(cx, cy, r=18, cls="sb-sp"):
    return f'<path class="{cls}" d="M{cx} {cy-r} L{cx+r*0.3:.0f} {cy-r*0.3:.0f} L{cx+r} {cy} L{cx+r*0.3:.0f} {cy+r*0.3:.0f} L{cx} {cy+r} L{cx-r*0.3:.0f} {cy+r*0.3:.0f} L{cx-r} {cy} L{cx-r*0.3:.0f} {cy-r*0.3:.0f} Z" fill="{RED}"/>'
cube = ["M480 1100 H600 V1220 H480 Z", "M530 1050 H650 V1170 H530 Z", "M480 1100 L530 1050", "M600 1100 L650 1050", "M600 1220 L650 1170", "M480 1220 L530 1170"]
STREAM = [(0, 0), (1, -30), (2, 30), (3, -60), (4, 60), (5, -15), (6, 15), (7, 45)]
stream = "".join(f'<circle class="sb-p" id="sb-p{k}" cx="540" cy="{800 + dy}" r="14" fill="{RED}"/>' for k, dy in STREAM)
scene("scB", st, en, DARK, f'''
  {label("sb-t1", "DE NOCHE", y=330, x=72, anchor="start", color=WHITE, cls="wl2")}
  {label("sb-t2", "NO OCURRIÓ", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {label("sb-t3", "DATOS DE ENTRENAMIENTO", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  <path id="sb-m" d="M250 390 A130 130 0 1 0 250 650 A100 100 0 1 1 250 390 Z" stroke="{WHITE}" {SW8}/>
  {spark(410, 450, 22)}{spark(450, 540, 14)}{spark(380, 630, 14)}
  {brain("sb", WHITE, extra='transform="translate(-100 498) scale(1.2)"', sw=SW8)}
  <g id="sb-mem">
    <path d="M120 1080 Q200 1060 280 1085 Q300 1150 275 1220 Q200 1240 125 1215 Q105 1150 120 1080 Z" stroke="{RED}" {SW}/>
    <path d="M140 1195 L180 1140 L210 1170 L250 1120 L268 1150" stroke="{RED}" {SW}/>
    <circle cx="240" cy="1110" r="8" fill="{RED}"/>
  </g>
  {"".join(f'<path class="sb-c" d="{d}" stroke="{WHITE}" {SW}/>' for d in cube)}
  <path id="sb-w" d="M480 1220 L650 1050" stroke="{RED}" stroke-width="8" stroke-linecap="round" fill="none"/>
  <circle id="sb-f" cx="880" cy="1150" r="72" stroke="{WHITE}" {SW} transform="rotate(-90 880 1150)"/>
  <text id="sb-q" x="880" y="1184" text-anchor="middle" class="big" fill="{RED}">?</text>
  {stream}
  <rect id="sb-box" x="740" y="420" width="220" height="180" rx="18" stroke="{WHITE}" {SW}/>
  {label("sb-bt", "VIDA NO VIVIDA", y=650, x=850, color=WHITE)}''')
hidden("#sb-t1, #sb-t2, #sb-t3, .sb-sp, #sb-mem, #sb-q, .sb-p, #sb-box, #sb-bt", st)
pop("#sb-t1", st + 0.25, 0.3)
draw("#sb-m", 1400, st + 0.2, 0.9)
pop(".sb-sp", S(18) + 1.5, 0.25, stagger=0.1)                                     # "algo extraño"
draw("#sb-o", 1800, S(19) + 0.05, 0.7); draw("#sb-f", 400, S(19) + 0.5, 0.3); draw(".sb-gy", 170, S(19) + 0.6, 0.25, stagger=0.06)
fade("#sb-t1", S(19) + 0.5, 0.0, 0.2); pop("#sb-t2", S(19) + 0.6, 0.3)          # "que no ocurrieron"
tl.append(f'  tl.set("#sb-mem", {{ autoAlpha: 1 }}, {S(20):.2f});')
draw("#sb-mem path", 700, S(20) + 0.1, 0.4, stagger=0.1)                          # "recuerdos distorsionados"
draw(".sb-c", 500, S(20) + 1.0, 0.3, stagger=0.05)                                # "cuartos imposibles"
draw("#sb-w", 260, S(20) + 1.6, 0.25)
draw("#sb-f", 460, S(21) + 0.05, 0.4); pop("#sb-q", S(21) + 0.5, 0.3)             # "gente que nunca has conocido"
fade("#sb-t2", S(22) + 0.5, 0.0, 0.2); pop("#sb-t3", S(22) + 0.6, 0.3)          # "genera datos de entrenamiento"
fade("#sb-mem, .sb-c, #sb-w, #sb-f, #sb-q", S(22) + 0.4, 0.0, 0.3)
tl.append(f'  tl.set("#sb-box", {{ autoAlpha: 1 }}, {S(23):.2f});')
draw("#sb-box", 900, S(23) + 0.05, 0.5); pop("#sb-bt", S(23) + 0.4, 0.3)          # "para una vida que no has vivido"
for k, dy in STREAM:
    at = S(22) + 0.8 + k * 0.2
    tl.append(f'  tl.fromTo("#sb-p{k}", {{ autoAlpha: 0, x: 0, y: 0, scale: 0.5, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, x: 310, y: {-290 - dy}, scale: 1, duration: 1.2, ease: "power1.inOut" }}, {at:.2f});')
    tl.append(f'  tl.to("#sb-p{k}", {{ autoAlpha: 0, duration: 0.15 }}, {at + 1.2:.2f});')
    tl.append(f'  tl.set("#sb-p{k}", {{ autoAlpha: 0 }}, {at + 1.35:.2f});')

# ================================================================ overlay · COSAS NUEVAS (back on face)
st, en = S(24), E(24) + 0.25
clip("newbox", st, en, f'''
  <rect id="nb-box" x="430" y="120" width="220" height="180" rx="18" stroke="{INK}" {SW}/>
  <path id="nb-ok" d="M490 215 L525 252 L595 165" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  {label("nb-t", "COSAS NUEVAS", y=370, color=RED)}''')
draw("#nb-box", 900, st + 0.05, 0.45); hidden("#nb-t", st)
draw("#nb-ok", 220, st + 0.5, 0.3); pop("#nb-t", st + 0.6, 0.3)

# ---------------------------------------------------------------- assemble
g_html = []
for gid, st, en, inner in graphics:
    d = en - st
    g_html.append(f'      <div id="{gid}" class="mg clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                  f'        <div id="{gid}-in" class="gin"><svg width="1080" height="520" viewBox="0 0 1080 520">{inner}\n        </svg></div>\n      </div>')
s_html = []
for sid, st, en, bg, inner in scenes:
    d = en - st
    s_html.append(f'      <div id="{sid}" class="scene clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="5">\n'
                  f'        <div id="{sid}-in" class="scin" style="background:{bg}"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}\n        </svg></div>\n      </div>')

page = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Sarier — ¿Por qué soñamos?</title>
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

      .scene {{ position: absolute; inset: 0; pointer-events: none; }}
      .scin {{ position: absolute; inset: 0; transform-origin: 50% 50%; opacity: 0; }}
      .scin svg {{ display: block; }}

      .rail {{ position: absolute; left: 0; right: 0; top: 1300px; display: flex; justify-content: center; pointer-events: none; }}
      .rail .line {{ max-width: 960px; text-align: center; text-wrap: balance; color: var(--on-dark); font-weight: 700; font-size: 62px; line-height: 1.15; letter-spacing: var(--tr-body); text-shadow: var(--sh-rail); }}
      .rail .line.ink {{ color: var(--ink); text-shadow: none; }}
      .rail .w {{ display: inline-block; }}
      .rail .w.hot {{ color: var(--red); text-shadow: 0 0 2px rgba(255,255,255,0.55), 0 0 12px rgba(255,255,255,0.45), 0 2px 2px rgba(0,0,0,0.35); }}
      .rail .line.ink .w.hot {{ text-shadow: none; }}

      .card {{ position: absolute; left: 0; top: 0; width: {W}px; height: 700px; pointer-events: none; }}
      .stmt {{ position: absolute; inset: 0; }}
      .stmt .rot {{ position: absolute; white-space: nowrap; }}
      .piece {{ display: inline-block; font-weight: 600; line-height: 0.9; letter-spacing: var(--tr-display); }}
      .piece.white {{ color: #FFFFFF; text-shadow: 0 2px 3px rgba(0,0,0,0.35), 0 6px 28px rgba(0,0,0,0.38); }}
      .gstack {{ display: grid; }}
      .gstack > span {{ grid-area: 1 / 1; display: inline-block; font-size: inherit; font-weight: 600; line-height: 0.9; letter-spacing: var(--tr-display); }}
      .gstack .ghost {{ opacity: 0; }}
      .gstack .warm {{ color: #FF3332; }}
      .gstack .cool {{ color: #5470FD; }}

      .mg {{ position: absolute; left: 0; top: 0; width: {W}px; pointer-events: none; }}
      .gin {{ position: absolute; left: 0; top: 226px; transform: scale(0.66); transform-origin: top center; }}
      .mg svg {{ display: block; }}
      .wl, .wl2, .cnt, .big {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; }}
      .wl {{ font-size: 28px; letter-spacing: var(--tr-caps); }}
      .wl2 {{ font-size: 34px; letter-spacing: var(--tr-caps); }}
      .cnt {{ font-size: 200px; letter-spacing: -0.05em; }}
      .big {{ font-size: 96px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
      <div id="video-wrap">
        <video id="src" src="{VIDEO}" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video>
      </div>
      <audio id="voice" src="{VIDEO}" data-start="0" data-duration="{DUR}" data-volume="1"></audio>

{chr(10).join(s_html)}

{chr(10).join(rail_html)}

{chr(10).join(g_html)}

{chr(10).join(card_html)}
    </div>
    <script>
      const glitchHash = (n) => {{ const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); }};
      const ghosts = gsap.utils.toArray("#overfit-stack .ghost");
      const glitch = {{ amp: 0 }};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(page)
print(f"index.html: DUR={DUR} {len(rail_html)} rail clips, {len(CARDS)} statements, {len(graphics)} overlays, {len(scenes)} scenes, {len(tl)} tweens")
