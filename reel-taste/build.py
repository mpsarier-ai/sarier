#!/usr/bin/env python3
"""Sarier reel 2 — "criterio excepcional" (Kolb). Same language as reel 1:
no backgrounds · kinetic word captions · big uneven statements · chained line graphics.
Every beat derives from captions.json. ink = human · red = accent."""
import json, html, math, re

W, H, FPS = 1080, 1920, 25
DUR = 68.84
VIDEO = "public/input-video.mp4"
INK, RED = "#1D1D1F", "#E1251B"

frags = json.load(open("captions.json", encoding="utf-8"))
FR = {f["i"]: f for f in frags}
def S(i): return FR[i]["start"]
def E(i): return FR[i]["end"]
CARD_FRAGS = {1, 2, 6, 25, 26}

GRAD = {
    "heat":     "linear-gradient(100deg, #FF3332, #FF9A4E, #FF3332)",
    "spectrum": "linear-gradient(100deg, #5470FD, #9C6CE6, #FA66C5, #5470FD)",
}
PUNCH = {3:"Kolb",4:"1984",5:"cuatro",7:"intención",8:"excelente",9:"diseño",10:"exponerte",11:"nota",
         12:"gusta",13:"anotar",14:"pregúntate",15:"funcionara",16:"extrae",17:"regla",18:"propio",
         19:"recrea",20:"regla",21:"falló",22:"repite",23:"buena",24:"ciclo"}

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

# ---------------------------------------------------------------- statements
CARDS = [
    ("hook",  0.00,          E(2) + 0.3,    "spectrum"),
    ("fail",  S(6) - 0.10,   E(6) + 0.0,    "heat"),
    ("close", S(25) - 0.10,  DUR,           "spectrum"),
]
STMT = {
  "hook":  [("a","Cuatro pasos para un","ink",84,72,140,"left","left"), ("b","criterio","grad",200,40,230,"left","scale"), ("c","excepcional.","grad",150,60,440,"right","right")],
  "fail":  [("a","La mayoría ya está","ink",88,80,150,"left","left"), ("b","fallando","grad",210,40,250,"left","scale"), ("c","en el primero.","grad",120,60,470,"right","right")],
  "close": [("a","No nació con él.","ink",104,72,150,"left","left"), ("b","Se enseñó","grad",160,60,280,"right","right"), ("c","a notarlo.","grad",160,60,445,"right","scale")],
}
ENTER = {"left": "{ x: -80, autoAlpha: 0 }", "right": "{ x: 90, autoAlpha: 0 }",
         "scale": "{ scale: 0.6, autoAlpha: 0 }", "drop": "{ y: -60, autoAlpha: 0 }"}
card_html = []
for cid, st, en, gname in CARDS:
    d = en - st; parts = []
    for k, (key, text, kind, size, x, y, align, enter) in enumerate(STMT[cid]):
        pid = f"{cid}-{key}"
        pos = f"left:{x}px;" if align == "left" else f"right:{x}px;"
        style = f"font-size:{size}px;" + (f"background-image:{GRAD[gname]};" if kind == "grad" else "")
        if cid == "fail" and key == "b":
            inner = (f'<span class="gstack" id="{cid}-stack"><span class="ghost warm" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="ghost cool" aria-hidden="true">{esc(text)}</span>'
                     f'<span class="piece grad" id="{pid}" style="{style}">{esc(text)}</span></span>')
        else:
            inner = f'<span class="piece {kind}" id="{pid}" style="{style}">{esc(text)}</span>'
        parts.append(f'<div class="rot" style="{pos}top:{y}px;">{inner}</div>')
        tl.append(f'  tl.fromTo("#{pid}", {ENTER[enter]}, {{ x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.6, ease: "expo.out" }}, {st + 0.05 + k * 0.14:.2f});')
        if kind == "grad":
            tl.append(f'  tl.fromTo("#{pid}", {{ backgroundPosition: "100% 50%" }}, {{ backgroundPosition: "0% 50%", duration: {d - 0.3:.2f}, ease: "none" }}, {st:.2f});')
    card_html.append(f'      <div id="{cid}" class="card clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                     f'        <div class="stmt" id="{cid}-in">{"".join(parts)}</div>\n      </div>')
    if en < DUR - 0.05:
        tl.append(f'  tl.to("#{cid}-in", {{ autoAlpha: 0, y: -20, duration: 0.30, ease: "power2.in" }}, {en - 0.30:.2f});')
        tl.append(f'  tl.set("#{cid}-in", {{ autoAlpha: 0 }}, {en:.2f});')

# glitch on "fallando" + camera punch
G0 = S(6) - 0.10; GDUR, GSTEP, GMAX = 0.45, 0.05, 10
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
tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.18, ease: "expo.out" }}, {S(6) + 0.2:.2f});')
tl.append(f'  tl.to("#video-wrap", {{ scale: 1, duration: 1.4, ease: "power2.out" }}, {S(6) + 0.38:.2f});')
tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: 1.05, duration: 1.6, ease: "sine.inOut" }}, {S(24):.2f});')
tl.append(f'  tl.to("#video-wrap", {{ scale: 1, duration: 1.4, ease: "sine.inOut" }}, {S(24) + 1.6:.2f});')

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
def label(id_, text, y=470, color=INK): return f'<text id="{id_}" x="540" y="{y}" text-anchor="middle" class="wl" fill="{color}">{text}</text>'

RING = f'<circle id="{{id}}-ring" cx="540" cy="250" r="150" stroke="{INK}" {SW} transform="rotate(-90 540 250)"/>'
def nodes(prefix):
    pts = [(540,100),(690,250),(540,400),(390,250)]
    return "".join(f'<circle class="{prefix}-n" id="{prefix}-n{i}" cx="{x}" cy="{y}" r="16" fill="{INK}"/>' for i,(x,y) in enumerate(pts))

# 1 · Kolb ring — "ciclo de Kolb… 1984… cuatro pasos"
st, en = S(3), E(5) + 0.2
clip("kolb", st, en, RING.format(id="kolb") + nodes("kolb") + label("kolb-t", "KOLB · 1984"))
draw("#kolb-ring", 960, st + 0.05, 1.0)
hidden(".kolb-n", st); hidden("#kolb-t", st)
pop("#kolb-t", S(4) + 0.3, 0.3)
pop(".kolb-n", S(5) + 0.9, 0.25, stagger=0.12)

# 2 · CONSUME — eye + three works
st, en = S(7), E(10)
clip("consume", st, en, f'''
  <path id="ey-o" d="M330 250 Q540 90 750 250 Q540 410 330 250 Z" stroke="{INK}" {SW}/>
  <circle id="ey-p" cx="540" cy="250" r="52" stroke="{INK}" {SW} transform="rotate(-90 540 250)"/>
  <circle id="ey-d" cx="540" cy="250" r="16" fill="{RED}"/>
  <rect class="ey-w" x="300" y="452" width="140" height="18" rx="9" stroke="{INK}" {SW}/>
  <rect class="ey-w" x="470" y="452" width="140" height="18" rx="9" stroke="{INK}" {SW}/>
  <rect class="ey-w" x="640" y="452" width="140" height="18" rx="9" stroke="{INK}" {SW}/>
  {label("ey-t", "01 · CONSUME", y=140)}''')
draw("#ey-o", 1300, st + 0.05, 1.0); draw("#ey-p", 340, st + 0.7, 0.5)
hidden("#ey-d", st); hidden(".ey-w", st); hidden("#ey-t", st)
pop("#ey-d", st + 1.15, 0.25); pop("#ey-t", st + 0.4, 0.3)
draw(".ey-w", 340, S(9) + 0.1, 0.35, stagger=0.55)

# 3 · NOTA — magnifier + ¿POR QUÉ?
st, en = S(11), E(15)
clip("nota", st, en, f'''
  <circle id="mg-c" cx="500" cy="220" r="120" stroke="{INK}" {SW} transform="rotate(-90 500 220)"/>
  <path id="mg-h" d="M586 306 L700 420" stroke="{INK}" stroke-width="12" stroke-linecap="round" fill="none"/>
  <text id="mg-q" x="500" y="245" text-anchor="middle" class="big" fill="{RED}">?</text>
  {label("mg-t", "02 · NOTA", y=490)}''')
draw("#mg-c", 780, st + 0.05, 0.8); draw("#mg-h", 170, st + 0.7, 0.3)
hidden("#mg-q", st); hidden("#mg-t", st)
pop("#mg-t", st + 0.4, 0.3); pop("#mg-q", S(14) + 0.4, 0.3)

# 4 · EXTRAE — a ruler ("regla")
st, en = S(16), E(18)
ticks = "".join(f'<path class="rl-t" d="M{x} 300 v{-28 if k%4==0 else -14}" stroke="{INK}" {SW}/>' for k, x in enumerate(range(240, 841, 40)))
clip("extrae", st, en, f'''
  <rect id="rl-b" x="200" y="200" width="680" height="100" rx="12" stroke="{INK}" {SW}/>
  {ticks}
  <path id="rl-r" d="M240 232 h140" stroke="{RED}" stroke-width="8" stroke-linecap="round" fill="none"/>
  {label("rl-t2", "03 · EXTRAE", y=400)}''')
draw("#rl-b", 1600, st + 0.05, 0.8); draw(".rl-t", 30, st + 0.5, 0.1, stagger=0.05)
hidden("#rl-r", st); hidden("#rl-t2", st); pop("#rl-t2", st + 0.4, 0.3)
draw("#rl-r", 150, S(17) + 0.6, 0.4)

# 5 · RECREA — two boxes: check (ink) and cross (red)
st, en = S(19), E(21)
clip("recrea", st, en, f'''
  <rect id="rc-a" x="270" y="140" width="220" height="220" rx="22" stroke="{INK}" {SW} />
  <rect id="rc-b" x="590" y="140" width="220" height="220" rx="22" stroke="{INK}" {SW} />
  <path id="rc-ok" d="M325 255 L365 300 L440 200" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path id="rc-x1" d="M650 200 L750 300" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  <path id="rc-x2" d="M750 200 L650 300" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>
  {label("rc-t", "04 · RECREA", y=450)}''')
draw("#rc-a, #rc-b", 900, st + 0.05, 0.7, stagger=0.12)
hidden("#rc-t", st); pop("#rc-t", st + 0.4, 0.3)
draw("#rc-ok", 220, S(21) + 0.7, 0.4)
draw("#rc-x1, #rc-x2", 160, S(21) + 1.5, 0.22, stagger=0.15)

# 6 · REPITE — ring returns, red dot orbits twice
st, en = S(22), E(24) + 0.3
clip("repite", st, en, RING.format(id="rp") + nodes("rp") + f'''
  <g id="rp-orb"><circle cx="540" cy="100" r="14" fill="{RED}"/></g>
  {label("rp-t", "REPITE", y=470, color=RED)}''')
draw("#rp-ring", 960, st + 0.05, 0.8)
hidden(".rp-n", st); hidden("#rp-t", st); hidden("#rp-orb", st)
pop(".rp-n", st + 0.5, 0.2, stagger=0.08); pop("#rp-t", st + 0.5, 0.3)
tl.append(f'  tl.to("#rp-orb", {{ autoAlpha: 1, duration: 0.2 }}, {S(23):.2f});')
tl.append(f'  tl.fromTo("#rp-orb", {{ rotation: 0, svgOrigin: "540 250" }}, {{ rotation: 720, duration: {E(24) - S(23) - 0.2:.2f}, ease: "power1.inOut" }}, {S(23) + 0.1:.2f});')

# ---------------------------------------------------------------- assemble
g_html = []
for gid, st, en, inner in graphics:
    d = en - st
    g_html.append(f'      <div id="{gid}" class="mg clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                  f'        <div id="{gid}-in" class="gin"><svg width="1080" height="520" viewBox="0 0 1080 520">{inner}\n        </svg></div>\n      </div>')

page = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Sarier — Criterio excepcional</title>
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
      .piece {{ display: inline-block; font-weight: 600; line-height: 0.98; letter-spacing: var(--tr-display); }}
      .piece.ink {{ color: var(--ink); text-shadow: 0 1px 12px rgba(255,255,255,0.7); }}
      .piece.grad {{ background-size: 300% 100%; background-position: 100% 50%; -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent; color: transparent; padding: 0.04em 0.06em 0.12em; margin: -0.04em -0.06em -0.12em; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.28)); }}
      .gstack {{ display: grid; }}
      .gstack > span {{ grid-area: 1 / 1; display: inline-block; font-size: 210px; font-weight: 600; line-height: 0.98; letter-spacing: var(--tr-display); }}
      .gstack .ghost {{ opacity: 0; }}
      .gstack .warm {{ color: #FF3332; }}
      .gstack .cool {{ color: #5470FD; }}

      .mg {{ position: absolute; left: 0; top: 0; width: {W}px; pointer-events: none; }}
      .gin {{ position: absolute; left: 0; top: 120px; }}
      .mg svg {{ display: block; }}
      .wl {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: var(--tr-caps); }}
      .big {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; font-size: 110px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
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
      const ghosts = gsap.utils.toArray("#fail-stack .ghost");
      const glitch = {{ amp: 0 }};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(page)
print(f"index.html: {len(rail_html)} rail clips, {len(CARDS)} statements, {len(graphics)} graphics, {len(tl)} tweens")
