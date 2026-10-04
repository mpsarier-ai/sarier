#!/usr/bin/env python3
"""FASHIONALYTICS / FOLD — reel 9:16 sobre el video original.

Montaje con los recursos de los reels de Sarier: subtítulos cinéticos centrados sobre el plano,
statements desiguales por capas, gráficos de línea en la banda segura, una escena faceless corta,
glitch, punch-in y fundido a negro. Nada de bloques blancos encima del video.

El sistema visual es el de Fashionalytics/FOLD (packages/ui/tokens.css + el brand book publicado):
  · `brand` #1a1aff es la única tinta de acción — y la palabra caliente de los subtítulos.
  · Texto `ink` sobre el plano claro; blanco solo encima del azul. Sin sombras.
  · Frases en sentence case; solo `label` (mono) y `pixel-title` van en MAYÚSCULAS.
  · Cuadrado (radius-none) para lo mono/ASCII/poster. Movimiento ease-out; nada rebota.
  · Los logos y la textura ASCII salen de brand/ tal cual los publica el sistema.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("Fashionalytics · FOLD — construir una marca", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="fold")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens (packages/ui/tokens.css)
GROUND, SURFACE, SUNKEN = "#f2f0ea", "#ffffff", "#e8e6df"
INK, INK_MUTED = "#0a0a12", "#5a5a66"
LINE, LINE_STRONG = "#c9c7c0", "#7a7a86"
BRAND, ON_BRAND = "#1a1aff", "#ffffff"
SIG_RED = "#ff3b1f"
BLUE_SOFT = "#c9c9ff"

SANS = "'Geist', -apple-system, 'SF Pro Text', system-ui, 'Liberation Sans', sans-serif"
MONO = "'IBM Plex Mono', 'SF Mono', Menlo, monospace"
PIXEL = "'DotGothic16', 'Handjet', monospace"
SERIF = "'Instrument Serif', 'Times New Roman', serif"

DOT = "●"
HAIR = f'stroke="{LINE_STRONG}" stroke-width="1" fill="none"'
M = 64
EASE = "power2.out"


# ---------------------------------------------------------------- estilos de texto del sistema
def t(id_, s, x, y, size, fam, fill=INK, anchor="start", weight=400, style="normal", tr="0", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text id="{id_}"{c} x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};font-style:{style};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def label(id_, s, x, y, size=24, fill=INK_MUTED, anchor="start", cls=""):
    """t-label · mono, SIEMPRE mayúsculas, tracking 0.08em."""
    return t(id_, s.upper(), x, y, size, MONO, fill, anchor, weight=500, tr="0.08em", cls=cls)


def data(id_, s, x, y, size=40, fill=INK, anchor="start", cls=""):
    return t(id_, s, x, y, size, MONO, fill, anchor, weight=400, tr="-0.01em", cls=cls)


def pixel(id_, s, x, y, size=88, fill=SURFACE, anchor="start"):
    """t-pixel-title · DotGothic16, solo marketing y posters."""
    return t(id_, s.upper(), x, y, size, PIXEL, fill, anchor, weight=400)


def tag(cid, s, x, y, w, h=58, size=23):
    """Tag mono cuadrado: radius-none, hairline, mayúsculas."""
    return (f'<g id="{cid}" class="tag"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
            f'stroke="{LINE_STRONG}" stroke-width="1"/>'
            + t(f"{cid}t", s.upper(), x + 16, y + h / 2 + 8, size, MONO, INK, weight=500, tr="0.08em") + '</g>')


ASCII_BLUE = "brand/ascii-field-blue.svg"
FOLD_W, FOLD_INK = "brand/fold-lockup-white.svg", "brand/fold-lockup.svg"
FA_W = "brand/fashionalytics-lockup-white.svg"


def img(id_, href, x, y, h, aspect):
    return f'<image id="{id_}" href="{href}" x="{x}" y="{y}" width="{h * aspect:.1f}" height="{h}"/>'


# ================================================================= subtítulos
R.card_frags = {1, 2, 5, 6}          # estas líneas las dice la tipografía grande
# Los subtítulos van en el tercio inferior, donde el plano es oscuro: blanco, sin caja y sin sombra.
R.punch = {3: "SaaS", 4: "vibecoding", 7: "fábricas", 8: "físico", 9: "complejo",
           10: "logística", 11: "inventario", 12: "campaña", 13: "marca", 14: "media",
           15: "conversión", 16: "contratar", 17: "diez"}
R.rail()

# ================================================================= bug de marca
# El lockup arriba a la izquierda y, al lado, el módulo de FOLD que resuelve lo que ella dice.
SAAS_IN, SAAS_OUT = S(3) - 0.10, E(4) + 0.08
LOGO = img("bg-logo", FOLD_INK, M, 246, 38, 3.972)
R.clip("bug", 0.35, SAAS_IN, LOGO)          # el bug sale antes de la escena azul
R.clip("bug2", SAAS_OUT, 35.92, LOGO.replace("bg-logo", "bg-logo2"), hold=True)
R.fade("#bug2-in", 35.60, 0.0, 0.3); R.hidden("#bug2-in", 35.92)
MODULES = [(0.35, SAAS_IN, "Core"), (SAAS_OUT, 14.10, "Product"), (14.10, 19.34, "Production"),
           (19.34, 23.60, "Inventory"), (23.60, 28.68, "Marketing"), (28.68, 35.60, "Commerce")]
for k, (st, en, name) in enumerate(MODULES):
    R.clip(f"mod{k}", st, en, label(f"modl{k}", name, M + 184, 276, 24, INK_MUTED))

# ================================================================= 1 · HOOK · statement por capas
R.card("hook", 0.0, E(2) + 0.20, [
    ("a", "Construir una marca de ropa", 54, M + 8, 300, "left", "left", 0.80),
    ("b", "es más difícil", 128, M, 352, "left", "scale", 1.0, 0.75),
    ("c", "que crear una startup.", 56, M + 8, 506, "right", "right", 0.88, 1.70)],
    glitch_key="b")
R.glitch(0.80)
R.punch_cam(0.95)

# ================================================================= 2 · VIBECODING · escena faceless
# El único momento de "marca cruda": pantalla completa en blue-electric con la textura ASCII.
st, en = S(3) - 0.10, E(4) + 0.08
R.scene("saas", st, en, BRAND, f'''
  <image href="{ASCII_BLUE}" x="-230" y="0" width="1540" height="1920"
     preserveAspectRatio="xMidYMid slice" opacity="0.55"/>
  <rect x="0" y="560" width="1080" height="560" fill="{BRAND}"/>
  <path d="M0 560 L1080 560" stroke="{BLUE_SOFT}" stroke-width="1" fill="none"/>
  <path d="M0 1120 L1080 1120" stroke="{BLUE_SOFT}" stroke-width="1" fill="none"/>
  {label("sa0", "Producto SaaS", 540, 648, 26, BLUE_SOFT, "middle")}
  {pixel("sa1", "vibecoding", 540, 820, 122, SURFACE, "middle")}
  {data("sa2", "$ crear producto saas", 540, 920, 36, SURFACE, "middle")}
  <g id="sa-run">{data("sa3", "|  generando", 540, 986, 36, BLUE_SOFT, "middle")}</g>
  {data("sa4", DOT + "  listo", 540, 986, 36, SURFACE, "middle")}''')
R.hidden("#sa0, #sa1, #sa2, #sa-run, #sa4", st)
R.fromTo("#sa0", "autoAlpha:0", "autoAlpha:1", st + 0.14, 0.2)
R.fromTo("#sa1", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.24, 0.26, EASE)
R.fromTo("#sa2", "autoAlpha:0", "autoAlpha:1", st + 0.46, 0.16)
# El loader de la marca: un carácter mono que rota, nunca un spinner circular.
R.show("#sa-run", st + 0.64)
R.raw(f'''  tl.to({{ k: 0 }}, {{ k: 12, duration: 1.4, ease: "none",
    onUpdate: function () {{ const c = "|/-\\\\\\\\"; const i = Math.floor(this.targets()[0].k) % 4;
      const el = document.getElementById("sa3"); if (el) el.textContent = c[i] + "  generando"; }} }}, {st + 0.64:.2f});''')
R.hidden("#sa-run", st + 2.10)
R.show("#sa4", st + 2.10)
R.fromTo("#sa4", "autoAlpha:0, x:-10", "autoAlpha:1, x:0", st + 2.10, 0.2, EASE)
R.punch_cam(en + 0.02)

# ================================================================= 3 · LA PRENDA · statement
R.card("prenda", 8.95, E(6) + 0.20, [
    ("a", "Pero una prenda todavía toma", 54, M + 8, 300, "left", "left", 0.80),
    ("b", "semanas", 132, M, 352, "left", "scale", 1.0, 9.90),
    ("c", "y excelentes fábricas.", 54, M + 8, 506, "right", "right", 0.88, 11.80)])

# ================================================================= 4 · ESCALAR · el dither
# El lenguaje cuadrado de Fashionalytics: celdas que crecen de ruido a señal.
st, en = S(8) - 0.05, E(9) + 0.20
GX, GY, CELL, GAP, N = 352, 372, 52, 12, 6
cells, order = "", []
for r in range(N):
    for c in range(N):
        cells += (f'<rect id="g{r}{c}" class="cell" x="{GX + c * (CELL + GAP)}" y="{GY + r * (CELL + GAP)}" '
                  f'width="{CELL}" height="{CELL}" fill="{BRAND}"/>')
        order.append((r + c, f"#g{r}{c}"))
R.clip("grid", st, en, f'''
  {label("gr0", "Escalar un producto físico", 540, 348, 26, INK_MUTED, "middle")}
  {cells}
  {data("gr1", "ruido", GX - 26, GY + 200, 24, INK_MUTED, "end")}
  {data("gr2", "señal", GX + N * (CELL + GAP) - GAP + 26, GY + 200, 24, BRAND)}''')
R.hidden("#gr0, #grid .cell, #gr1, #gr2", st)
R.fromTo("#gr0", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
for d, sel in order:
    R.fromTo(sel, "autoAlpha:0, scale:0.4, transformOrigin:'50% 50%'",
             f"autoAlpha:{0.16 + 0.084 * d:.2f}, scale:1", st + 0.20 + d * 0.13, 0.22, EASE)
R.fromTo("#gr1, #gr2", "autoAlpha:0", "autoAlpha:1", st + 0.40, 0.2)

# ================================================================= 5-7 · LA PILA DE DIEZ
# Diez tags cuadrados que se acumulan: uno por cada cosa que ella enumera.
st, en = S(10) - 0.05, E(16) + 0.20
TAGS = ["Cadena de suministro", "Logística", "Inventario", "Fábricas", "Campaña",
        "Tu marca", "Paid media", "Tienda online", "Conversión", "+ mil cosas más"]
TW, TH, TSTEP = 464, 58, 74
TX, TY2 = (1080 - (2 * TW + 32)) / 2, 332
grid_tags = "".join(tag(f"st{k}", s_, TX + (k // 5) * (TW + 32), TY2 + (k % 5) * TSTEP, TW, TH)
                    for k, s_ in enumerate(TAGS))
R.clip("pila", st, en, grid_tags)
R.hidden("#pila .tag", st)
for k, a in enumerate([0.10, 0.95, 1.75, 2.90, 4.40, 6.05, 9.30, 10.55, 12.10, 13.40]):
    R.fromTo(f"#st{k}", "autoAlpha:0, y:14", "autoAlpha:1, y:0", st + a, 0.24, EASE)

# ================================================================= 8 · DIEZ PERSONAS
st, en = S(17) - 0.05, 35.92
SQ, SG = 58, 26
SX = (1080 - (10 * SQ + 9 * SG)) / 2
sq = "".join(f'<rect id="p{k}" class="per" x="{SX + k * (SQ + SG):.0f}" y="470" width="{SQ}" height="{SQ}" fill="{BRAND}"/>'
             for k in range(10))
R.clip("team", st, en, sq)
R.hidden("#team .per", st)
for k in range(10):
    R.fromTo(f"#p{k}", "autoAlpha:0, scale:0.4, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1",
             st + 0.06 + k * 0.055, 0.2, EASE)
R.punch_cam(st + 0.60, 1.04)

# ================================================================= 9 · CIERRE · tema Screen
# El tema de marca: la página entera en blue-electric, para portada y cierre.
st = 35.92
R.scene("cierre", st, R.DUR, BRAND, f'''
  <image href="{ASCII_BLUE}" x="-230" y="0" width="1540" height="1920"
     preserveAspectRatio="xMidYMid slice" opacity="0.55"/>
  <rect x="0" y="700" width="1080" height="880" fill="{BRAND}"/>
  <path d="M0 700 L1080 700" stroke="{BLUE_SOFT}" stroke-width="1" fill="none"/>
  <path d="M0 1580 L1080 1580" stroke="{BLUE_SOFT}" stroke-width="1" fill="none"/>''')
MODS = ["Core", "Commerce", "Inventory", "Product", "Production", "Intelligence", "Marketing", "Finance"]
mods = "".join(label(f"cm{k}", m, 540 + (-1 if k < 4 else 1) * 24, 1160 + (k % 4) * 62, 26,
                     BLUE_SOFT, "end" if k < 4 else "start") for k, m in enumerate(MODS))
R.clip("cta", st, R.DUR, f'''
  {img("c-fold", FOLD_W, (1080 - 112 * 3.972) / 2, 790, 112, 3.972)}
  <path id="c-r" d="M{M + 80} 1040 L{1080 - M - 80} 1040" stroke="{BLUE_SOFT}" stroke-width="1" fill="none"/>
  {mods}
  {img("c-fa", FA_W, (1080 - 34 * 11.81) / 2, 1450, 34, 11.81)}''', hold=True)
R.hidden("#c-fold, #c-r, #c-fa", st)
R.raw(f'  tl.set("#cta text", {{ autoAlpha: 0 }}, {st:.2f});')
R.fromTo("#c-fold", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.16, 0.3, EASE)
R.show("#c-r", st + 0.42); R.draw("#c-r", 1080 - 2 * M - 160, st + 0.42, 0.4, "power2.inOut")
R.raw(f'  tl.fromTo("#cta text", {{ autoAlpha: 0, y: 8 }}, {{ autoAlpha: 1, y: 0, duration: 0.22, stagger: 0.05, ease: "{EASE}" }}, {st + 0.56:.2f});')
R.fromTo("#c-fa", "autoAlpha:0", "autoAlpha:1", st + 1.15, 0.3)
R.slow_push(st)
R.fadeout(0.45)

# ================================================================= estilo propio del reel
R.extra_css = f'''
      /* Subtítulos centrados sobre el plano, sin ninguna caja detrás y sin sombra. */
      .rail {{ top: 1424px; }}
      .rail .line {{ max-width: 920px; color: {SURFACE}; text-shadow: none;
        font-weight: 500; font-size: 56px; line-height: 1.18; letter-spacing: -0.02em; }}
      /* `brand` es la única tinta de acción: también la palabra caliente. Sin halo. */
      .rail .w.hot {{ color: #8f8fff; text-shadow: none; }}
      /* Statements: ink sobre el plano claro, nunca blancos con sombra. */
      .card {{ height: 900px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-weight: 500; }}
      /* El glitch usa los dos acentos del sistema, no los de Sarier. */
      .gstack .warm {{ color: {SIG_RED}; }}
      .gstack .cool {{ color: {BRAND}; }}
      /* La palabra en serif cursiva dentro de un titular sans: "todavía toma semanas". */
      #prenda-b {{ font-family: {SERIF}; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
