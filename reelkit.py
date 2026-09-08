#!/usr/bin/env python3
"""Sarier reel kit — shared engine for the talking-head reels (HyperFrames + GSAP).
Kinetic word captions · big uneven white statements (layered transparency) · chained SVG line graphics
overlaid inside the Instagram safe zone · short full-screen faceless scenes · fade to black.
ink = human · red = AI / accent.  A reel's build.py only declares content."""
import json, html, re, subprocess, sys, os

W, H = 1080, 1920
INK, RED = "#1D1D1F", "#E1251B"
LIGHT, DARK, WHITE = "#F5F5F7", "#161618", "#FFFFFF"
SW = 'stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
SW8 = 'stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"'

def esc(s): return html.escape(s, quote=True)
def norm(w): return re.sub(r"[^\wáéíóúüñ]", "", w.lower())
def probe(video, entries):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", entries, "-of", "csv=p=0", video],
                          capture_output=True, text=True).stdout.strip()

ENTER = {"left": "{ x: -80, autoAlpha: 0 }", "right": "{ x: 90, autoAlpha: 0 }",
         "scale": "{ scale: 0.6, autoAlpha: 0 }", "drop": "{ y: -60, autoAlpha: 0 }"}

class Reel:
    def __init__(self, title, captions="captions.cut.json", video="public/input-video.mp4", gin_top=226, gin_scale=0.66):
        self.title, self.video = title, video
        fr = probe(video, "stream=r_frame_rate"); a, b = fr.split("/"); self.FPS = round(int(a) / int(b))
        self.DUR = round(float(probe(video, "format=duration").splitlines()[-1]) - 0.02, 2)
        self.frags = json.load(open(captions, encoding="utf-8"))
        self.FR = {f["i"]: f for f in self.frags}
        self.tl, self.graphics, self.scenes, self.cards_html, self.rail_html = [], [], [], [], []
        self.card_frags, self.ink_frags, self.punch = set(), set(), {}
        self.glitch_stack = None
        self.gin_top, self.gin_scale = gin_top, gin_scale
        self.extra_css = ""
    def S(self, i): return self.FR[i]["start"]
    def E(self, i): return self.FR[i]["end"]

    # ------------------------------------------------------------ captions
    def rail(self):
        tl = self.tl
        for f in self.frags:
            if f["i"] in self.card_frags: continue
            st, en = f["start"], f["end"]; d = max(0.5, en - st)
            rid = f"r{f['i']:02d}"
            words = f["text"].split()
            weights = [len(w) + 1 for w in words]; tot = sum(weights)
            spans, t = [], st
            punch = self.punch.get(f["i"])
            for k, (w, wt) in enumerate(zip(words, weights)):
                cls = "w hot" if punch and norm(w) == norm(punch) else "w"
                spans.append(f'<span class="{cls}" id="{rid}w{k}">{esc(w)}</span>')
                tl.append(f'  tl.fromTo("#{rid}w{k}", {{ autoAlpha: 0, y: 14, scale: 0.82 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.18, ease: "power3.out" }}, {t:.2f});')
                t += (en - st) * wt / tot * 0.93
            lcls = "line ink" if f["i"] in self.ink_frags else "line"
            self.rail_html.append(f'      <div id="{rid}" class="rail clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="2"><div class="{lcls}" id="{rid}l">{" ".join(spans)}</div></div>')
            tl.append(f'  tl.to("#{rid}l", {{ autoAlpha: 0, y: -8, duration: 0.14, ease: "power2.in" }}, {max(st, st + d - 0.14):.2f});')
            tl.append(f'  tl.set("#{rid}l", {{ autoAlpha: 0 }}, {st + d:.2f});')

    # ------------------------------------------------------------ statements
    def card(self, cid, st, en, pieces, glitch_key=None):
        """pieces: (key, text, size, x, y, align, enter, alpha[, at])"""
        tl = self.tl; d = en - st; parts = []
        for k, piece in enumerate(pieces):
            key, text, size, x, y, align, enter, alpha = piece[:8]
            at = piece[8] if len(piece) > 8 else st + 0.05 + k * 0.14
            pid = f"{cid}-{key}"
            pos = f"left:{x}px;" if align == "left" else f"right:{x}px;"
            style = f"font-size:{size}px;"
            if glitch_key == key:
                self.glitch_stack = f"{cid}-stack"
                inner = (f'<span class="gstack" id="{cid}-stack" style="{style}"><span class="ghost warm" aria-hidden="true">{esc(text)}</span>'
                         f'<span class="ghost cool" aria-hidden="true">{esc(text)}</span>'
                         f'<span class="piece white" id="{pid}" data-layout-allow-overlap>{esc(text)}</span></span>')
            else:
                inner = f'<span class="piece white" id="{pid}" data-layout-allow-overlap style="{style}">{esc(text)}</span>'
            parts.append(f'<div class="rot" data-layout-allow-overlap style="{pos}top:{y}px;">{inner}</div>')
            tl.append(f'  tl.fromTo("#{pid}", {ENTER[enter]}, {{ x: 0, y: 0, scale: 1, autoAlpha: {alpha}, duration: 0.6, ease: "expo.out" }}, {at:.2f});')
        self.cards_html.append(f'      <div id="{cid}" class="card clip" data-start="{st:.2f}" data-duration="{d:.2f}" data-track-index="3">\n'
                               f'        <div class="stmt" id="{cid}-in">{"".join(parts)}</div>\n      </div>')
        if en < self.DUR - 0.05:
            tl.append(f'  tl.to("#{cid}-in", {{ autoAlpha: 0, y: -20, duration: 0.30, ease: "power2.in" }}, {en - 0.30:.2f});')
            tl.append(f'  tl.set("#{cid}-in", {{ autoAlpha: 0 }}, {en:.2f});')

    def glitch(self, at, dur=0.5, step=0.05, amp=12):
        self.tl.append(f'''  tl.set(ghosts, {{ opacity: 0.55, x: 0, y: 0 }}, {at:.2f});
  tl.fromTo(glitch, {{ amp: 1 }}, {{ amp: 0, duration: {dur}, ease: "power2.in",
    onUpdate: () => {{
      const step = Math.floor(tl.time() / {step});
      ghosts.forEach((el, layer) => {{
        gsap.set(el, {{ x: (glitchHash(step * 13 + layer * 7) * 2 - 1) * {amp} * glitch.amp,
                       y: (glitchHash(step * 29 + layer * 11) * 2 - 1) * 4 * glitch.amp }});
      }});
    }} }}, {at:.2f});
  tl.set(ghosts, {{ opacity: 0, x: 0, y: 0 }}, {at + dur:.2f});''')

    def punch_cam(self, at, amount=1.05, hold=0.18, back=1.4, sel="#video-wrap"):
        self.tl.append(f'  tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: {amount}, duration: {hold}, ease: "expo.out" }}, {at:.2f});')
        self.tl.append(f'  tl.to("{sel}", {{ scale: 1, duration: {back}, ease: "power2.out" }}, {at + hold:.2f});')
    def slow_push(self, at, dur=2.2, amount=1.05):
        self.tl.append(f'  tl.fromTo("#video-wrap", {{ scale: 1 }}, {{ scale: {amount}, duration: {dur}, ease: "sine.inOut" }}, {at:.2f});')
    def fadeout(self, dur=0.5):
        self.tl.append(f'  tl.fromTo("#fadeout", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: {dur}, ease: "power1.in" }}, {self.DUR - dur - 0.05:.2f});')

    # ------------------------------------------------------------ graphics primitives
    def clip(self, gid, st, en, inner, hold=False):
        self.graphics.append((gid, st, en, inner))
        self.tl.append(f'  tl.fromTo("#{gid}-in", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.25, ease: "power2.out" }}, {st:.2f});')
        if not hold:
            self.tl.append(f'  tl.to("#{gid}-in", {{ autoAlpha: 0, duration: 0.25, ease: "power2.in" }}, {en - 0.25:.2f});')
            self.tl.append(f'  tl.set("#{gid}-in", {{ autoAlpha: 0 }}, {en:.2f});')
    def scene(self, sid, st, en, bg, inner):
        self.scenes.append((sid, st, en, bg, inner))
        self.tl.append(f'  tl.fromTo("#{sid}-in", {{ autoAlpha: 0, scale: 1.05 }}, {{ autoAlpha: 1, scale: 1, duration: 0.2, ease: "power2.out" }}, {st:.2f});')
        self.tl.append(f'  tl.to("#{sid}-in", {{ autoAlpha: 0, duration: 0.15, ease: "power2.in" }}, {en - 0.15:.2f});')
        self.tl.append(f'  tl.set("#{sid}-in", {{ autoAlpha: 0 }}, {en:.2f});')
    def draw(self, sel, L, at, dur, ease="power2.out", stagger=0.0):
        self.tl.append(f'  tl.fromTo("{sel}", {{ strokeDasharray: "{L:.0f}", strokeDashoffset: {L:.0f} }}, {{ strokeDashoffset: 0, duration: {dur}, ease: "{ease}", stagger: {stagger} }}, {at:.2f});')
    def pop(self, sel, at, dur=0.3, stagger=0.0):
        self.tl.append(f'  tl.fromTo("{sel}", {{ autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, scale: 1, duration: {dur}, ease: "power3.out", stagger: {stagger} }}, {at:.2f});')
    def fade(self, sel, at, to=0.0, dur=0.3): self.tl.append(f'  tl.to("{sel}", {{ autoAlpha: {to}, duration: {dur}, ease: "power2.inOut" }}, {at:.2f});')
    def hidden(self, sel, at): self.tl.append(f'  tl.set("{sel}", {{ autoAlpha: 0 }}, {at:.2f});')
    def show(self, sel, at): self.tl.append(f'  tl.set("{sel}", {{ autoAlpha: 1 }}, {at:.2f});')
    def to(self, sel, props, at, dur=0.4, ease="power2.out"): self.tl.append(f'  tl.to("{sel}", {{ {props}, duration: {dur}, ease: "{ease}" }}, {at:.2f});')
    def fromTo(self, sel, a, b, at, dur=0.4, ease="power2.out"): self.tl.append(f'  tl.fromTo("{sel}", {{ {a} }}, {{ {b}, duration: {dur}, ease: "{ease}" }}, {at:.2f});')
    def pulse(self, sel, at, scale=1.6, dur=0.14, color=None):
        col = f', fill: "{color}"' if color else ""
        self.tl.append(f'  tl.fromTo("{sel}", {{ scale: 1, transformOrigin: "50% 50%" }}, {{ scale: {scale}{col}, duration: {dur}, yoyo: true, repeat: 1 }}, {at:.2f});')
    def raw(self, s): self.tl.append(s)

    @staticmethod
    def label(id_, text, y=470, color=INK, x=540, anchor="middle", cls="wl"):
        return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" fill="{color}">{esc(text)}</text>'
    @staticmethod
    def big(id_, text, y, color=INK, x=540, anchor="middle", size=110):
        return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="num" style="font-size:{size}px" fill="{color}">{esc(text)}</text>'
    @staticmethod
    def spark(cx, cy, r=18, cls="sp", color=RED):
        return f'<path class="{cls}" d="M{cx} {cy-r} L{cx+r*0.3:.0f} {cy-r*0.3:.0f} L{cx+r} {cy} L{cx+r*0.3:.0f} {cy+r*0.3:.0f} L{cx} {cy+r} L{cx-r*0.3:.0f} {cy+r*0.3:.0f} L{cx-r} {cy} L{cx-r*0.3:.0f} {cy-r*0.3:.0f} Z" fill="{color}"/>'
    @staticmethod
    def xmark(id_, cx, cy, r=28, color=RED, w=9):
        return (f'<path id="{id_}a" d="M{cx-r} {cy-r} L{cx+r} {cy+r}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none"/>'
                f'<path id="{id_}b" d="M{cx+r} {cy-r} L{cx-r} {cy+r}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none"/>')
    @staticmethod
    def check(id_, cx, cy, r=36, color=INK, w=10):
        return f'<path id="{id_}" d="M{cx-r} {cy} L{cx-r*0.25:.0f} {cy+r*0.7:.0f} L{cx+r} {cy-r*0.8:.0f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'

    # anatomical brain (side view, front to the left) · bbox x 330..778 · y 80..452 in the 1080×520 box
    def brain(self, p, color=INK, extra="", sw=SW):
        sys.path.insert(0, "brain"); from brainpath import CEREBRUM, CEREBELLUM, STEM, FISSURE, GYRI
        g = "".join(f'<path class="{p}-gy" d="{d}" stroke="{color}" {sw}/>' for d in GYRI)
        return (f'<g id="{p}-g" {extra}><path id="{p}-o" d="{CEREBRUM}" stroke="{color}" {sw}/>'
                f'<path id="{p}-c" d="{CEREBELLUM}" stroke="{color}" {sw}/><path id="{p}-s" d="{STEM}" stroke="{color}" {sw}/>'
                f'<path id="{p}-f" d="{FISSURE}" stroke="{color}" {sw}/>{g}</g>')
    def draw_brain(self, p, at, k=1.0):
        self.draw(f"#{p}-o", 2100, at, 0.9 * k); self.draw(f"#{p}-c", 450, at + 0.55 * k, 0.35 * k); self.draw(f"#{p}-s", 220, at + 0.75 * k, 0.3 * k)
        self.draw(f"#{p}-f", 360, at + 0.5 * k, 0.4 * k); self.draw(f".{p}-gy", 120, at + 0.7 * k, 0.25 * k, stagger=0.06 * k)

    # ------------------------------------------------------------ assemble
    def write(self, out="index.html"):
        g_html = []
        for gid, st, en, inner in self.graphics:
            g_html.append(f'      <div id="{gid}" class="mg clip" data-start="{st:.2f}" data-duration="{en - st:.2f}" data-track-index="3">\n'
                          f'        <div id="{gid}-in" class="gin"><svg width="1080" height="520" viewBox="0 0 1080 520">{inner}\n        </svg></div>\n      </div>')
        s_html = []
        for sid, st, en, bg, inner in self.scenes:
            s_html.append(f'      <div id="{sid}" class="scene clip" data-start="{st:.2f}" data-duration="{en - st:.2f}" data-track-index="5">\n'
                          f'        <div id="{sid}-in" class="scin" style="background:{bg}"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}\n        </svg></div>\n      </div>')
        ghosts = f'gsap.utils.toArray("#{self.glitch_stack} .ghost")' if self.glitch_stack else "[]"
        DUR, FPS = self.DUR, self.FPS
        page = f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{esc(self.title)}</title>
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
      #fadeout {{ position: absolute; inset: 0; background: #000; opacity: 0; pointer-events: none; }}
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
      .gin {{ position: absolute; left: 0; top: {self.gin_top}px; transform: scale({self.gin_scale}); transform-origin: top center; }}
      .mg svg {{ display: block; }}
      .wl, .wl2, .cnt, .big, .num {{ font-family: "Archivo", "Helvetica Neue", Helvetica, "Liberation Sans", Arial, sans-serif; font-weight: 700; }}
      .wl {{ font-size: 28px; letter-spacing: var(--tr-caps); }}
      .wl2 {{ font-size: 34px; letter-spacing: var(--tr-caps); }}
      .cnt {{ font-size: 200px; letter-spacing: -0.05em; }}
      .num {{ letter-spacing: -0.04em; }}
      .big {{ font-size: 96px; }}
      {self.extra_css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
      <div id="video-wrap">
        <video id="src" src="{self.video}" data-start="0" data-duration="{DUR}" data-track-index="1" muted playsinline></video>
      </div>
      <audio id="voice" src="{self.video}" data-start="0" data-duration="{DUR}" data-volume="1"></audio>

{chr(10).join(s_html)}

{chr(10).join(self.rail_html)}

{chr(10).join(g_html)}

{chr(10).join(self.cards_html)}
      <div id="fadeout" class="clip" data-start="{DUR - 0.6:.2f}" data-duration="0.60" data-track-index="6"></div>
    </div>
    <script>
      const glitchHash = (n) => {{ const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); }};
      const ghosts = {ghosts};
      const glitch = {{ amp: 0 }};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
        open(out, "w", encoding="utf-8").write(page)
        print(f"{out}: DUR={DUR} fps={FPS} {len(self.rail_html)} rail clips, {len(self.cards_html)} statements, {len(self.graphics)} overlays, {len(self.scenes)} scenes, {len(self.tl)} tweens")
