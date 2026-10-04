#!/usr/bin/env python3
"""FASHIONALYTICS / FOLD — reel 9:16 sobre el video original.

Design system: packages/ui/tokens.css del monorepo fashionalytics-platform + el brand book
publicado. Reglas que mandan sobre la edición:
  · "la marca es cruda, el producto es calmado": el azul-ASCII a todo volumen solo en los
    bloques de marca; la capa que acompaña a la locución es calmada, tema Paper.
  · `brand` es la única tinta de acción. `accent-acid` es el resaltador: UNO por pantalla.
  · Separar capas por valor y hairline, NUNCA por sombra.
  · Frases en sentence case; solo `label` (mono) y `pixel-title` van en MAYÚSCULAS.
  · Dos lenguajes de forma que no se mezclan: cuadrado (radius-none) para lo mono/ASCII/poster,
    redondeado para la UI.
  · Movimiento 160 ms ease-out, 240 ms para láminas. Nada rebota.
  · Los logos no se redibujan: salen de brand/ tal cual los publica el sistema.

El reel va enmarcado como el producto: barra superior con el lockup y el módulo de FOLD que
resuelve lo que ella está diciendo, y franja inferior `surface` para los subtítulos.
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
ACID, ON_ACCENT = "#e6ff47", "#0a0a12"
SIG_RED, SIG_GREEN = "#ff3b1f", "#2bff4a"

SANS = "'Geist', -apple-system, 'SF Pro Text', system-ui, 'Liberation Sans', sans-serif"
MONO = "'IBM Plex Mono', 'SF Mono', Menlo, monospace"
PIXEL = "'DotGothic16', 'Handjet', monospace"
SERIF = "'Instrument Serif', 'Times New Roman', serif"

DOT = "\u25cf"   # glifo de estado de la marca
HAIR = f'stroke="{LINE}" stroke-width="1" fill="none"'          # stroke-hairline
CTRL = f'stroke="{LINE_STRONG}" stroke-width="1.5" fill="none"'  # stroke-control
M = 56                                                           # margen lateral

BAR_Y, BAR_H = 190, 96          # barra superior
STRIP_Y, STRIP_H = 1440, 256    # franja de subtítulos
EASE = "power2.out"             # 160 ms ease-out · nada rebota


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
    """t-data · mono tabular."""
    return t(id_, s, x, y, size, MONO, fill, anchor, weight=400, tr="-0.01em", cls=cls)


def headline(id_, s, x, y, size=76, fill=INK, anchor="start", cls=""):
    """t-headline / t-display · Geist medium, tracking negativo, sentence case."""
    return t(id_, s, x, y, size, SANS, fill, anchor, weight=500, tr="-0.025em", cls=cls)


def pixel(id_, s, x, y, size=88, fill=SURFACE, anchor="start"):
    """t-pixel-title · DotGothic16, solo marketing y posters."""
    return t(id_, s.upper(), x, y, size, PIXEL, fill, anchor, weight=400)


def tag(cid, s, x, y, w, h=58, fill=INK, border=LINE_STRONG, bg="none", size=23):
    """Tag mono cuadrado: radius-none, hairline, mayúsculas."""
    return (f'<g id="{cid}" class="tag"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" '
            f'stroke="{border}" stroke-width="1"/>'
            + t(f"{cid}t", s.upper(), x + 16, y + h / 2 + 8, size, MONO, fill, weight=500, tr="0.08em") + '</g>')


ASCII_BLUE = "brand/ascii-field-blue.svg"
FOLD_W = "brand/fold-lockup-white.svg"
FOLD_INK = "brand/fold-lockup.svg"
FA_W = "brand/fashionalytics-lockup-white.svg"


def img(id_, href, x, y, h, aspect, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<image id="{id_}"{c} href="{href}" x="{x}" y="{y}" width="{h * aspect:.1f}" height="{h}"/>'


# ================================================================= chrome · el marco del producto
# Barra superior y franja de subtítulos en `surface`, separadas por hairline. Sin sombra.
R.scene("chrome", 0.0, 35.92, "transparent", f'''
  <rect x="0" y="{BAR_Y}" width="1080" height="{BAR_H}" fill="{SURFACE}"/>
  <path d="M0 {BAR_Y + BAR_H} L1080 {BAR_Y + BAR_H}" {HAIR}/>
  {img("bar-logo", FOLD_INK, M, BAR_Y + 26, 44, 3.972)}
  <path d="M{M + 206} {BAR_Y + 24} L{M + 206} {BAR_Y + 72}" {HAIR}/>''')
# La franja solo existe mientras corre un subtítulo: una banda blanca vacía no es un elemento.
R.scene("strip", S(3) - 0.20, 35.92, "transparent", f'''
  <rect x="0" y="{STRIP_Y}" width="1080" height="{STRIP_H}" fill="{SURFACE}"/>
  <path d="M0 {STRIP_Y} L1080 {STRIP_Y}" {HAIR}/>''')

# El módulo de FOLD que resuelve lo que ella está diciendo, en la barra.
MODULES = [(0.0, "Core"), (8.82, "Product"), (14.10, "Production"),
           (19.34, "Inventory"), (23.60, "Marketing"), (28.68, "Commerce")]
for k, (st, name) in enumerate(MODULES):
    en = MODULES[k + 1][0] if k + 1 < len(MODULES) else 35.92
    R.clip(f"mod{k}", st, en, label(f"modl{k}", name, M + 238, BAR_Y + 62, 26, INK_MUTED))

R.card_frags = {1, 2}   # el arranque lo dice la tipografía grande
# El resaltador acid, una vez por pantalla: nunca en un momento que ya tenga otro elemento acid.
R.punch = {9: "complejo", 15: "conversión"}

# ================================================================= 1 · EL HOOK
st, en = S(1), E(2) + 0.25
HX, HY = M, 430
R.clip("hook", st, en, f'''
  <rect id="hk-hl" x="{HX - 6}" y="{HY + 104}" width="408" height="92" fill="{ACID}"/>
  {headline("hk1", "Construir una marca", HX, HY, 76)}
  {headline("hk2", "de ropa es", HX, HY + 92, 76)}
  {headline("hk3", "más difícil", HX + 6, HY + 174, 76, ON_ACCENT)}
  {headline("hk4", "que crear una startup.", HX, HY + 266, 76)}''')
R.hidden("#hk1, #hk2, #hk3, #hk4, #hk-hl", st)
for k, at in enumerate([0.10, 0.26, 0.42, 0.58]):
    R.fromTo(f"#hk{k + 1}", "autoAlpha:0, y:18", "autoAlpha:1, y:0", st + at, 0.26, EASE)
R.show("#hk-hl", st + 0.40)
R.fromTo("#hk-hl", "scaleX:0, transformOrigin:'0% 50%'", "scaleX:1", st + 0.40, 0.24, EASE)

# ================================================================= 2 · VIBECODING · bloque crudo
# El único momento "marca cruda": panel blue-electric con la textura ASCII del sistema.
st, en = S(3) - 0.05, E(4) + 0.25
PY_, PH = 316, 940
R.clip("saas", st, en, f'''
  <defs><clipPath id="pclip"><rect x="0" y="{PY_}" width="1080" height="{PH}"/></clipPath></defs>
  <g id="saas-g">
    <rect x="0" y="{PY_}" width="1080" height="{PH}" fill="{BRAND}"/>
    <g clip-path="url(#pclip)"><image href="{ASCII_BLUE}" x="-230" y="{PY_}" width="1540" height="{PH}"
       preserveAspectRatio="xMidYMid slice" opacity="0.5"/></g>
    {label("sa0", "Producto SaaS", M, PY_ + 86, 26, "#c9c9ff")}
    {pixel("sa1", "vibecoding", M, PY_ + 300, 128, SURFACE)}
    {data("sa2", "$ crear producto saas", M, PY_ + 420, 38, SURFACE)}
    <g id="sa-run">{data("sa3", "|  generando", M, PY_ + 486, 38, "#c9c9ff")}</g>
    {data("sa4", DOT + "  listo", M, PY_ + 486, 38, ACID)}
  </g>''')
R.hidden("#saas-g, #sa0, #sa1, #sa2, #sa-run, #sa4", st)
R.show("#saas-g", st)
R.fromTo("#saas-g", "autoAlpha:0", "autoAlpha:1", st, 0.24, EASE)
R.fromTo("#sa0", "autoAlpha:0", "autoAlpha:1", st + 0.14, 0.2)
R.fromTo("#sa1", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.26, 0.26, EASE)
R.fromTo("#sa2", "autoAlpha:0", "autoAlpha:1", st + 0.50, 0.16)
# El loader de la marca: un carácter mono que rota, nunca un spinner circular.
R.show("#sa-run", st + 0.70)
R.raw(f'''  tl.to({{ k: 0 }}, {{ k: 12, duration: 1.5, ease: "none",
    onUpdate: function () {{ const c = "|/-\\\\\\\\"; const i = Math.floor(this.targets()[0].k) % 4;
      const el = document.getElementById("sa3"); if (el) el.textContent = c[i] + "  generando"; }} }}, {st + 0.70:.2f});''')
R.hidden("#sa-run", st + 2.25)
R.show("#sa4", st + 2.25)
R.fromTo("#sa4", "autoAlpha:0, x:-10", "autoAlpha:1, x:0", st + 2.25, 0.2, EASE)
R.fade("#saas-g", en - 0.24, 0.0, 0.24)
R.hidden("#saas-g", en)

# ================================================================= 3 · LA PRENDA · editorial
st, en = S(5) - 0.05, E(7) + 0.20
TY = 470
R.clip("prenda", st, en, f'''
  {label("pr0", "Producto físico", M, TY, 26, INK_MUTED)}
  <text id="pr1" x="{M}" y="{TY + 94}" fill="{INK}"
    style="font-family:{SANS};font-size:76px;font-weight:500;letter-spacing:-0.025em">todavía toma
    <tspan style="font-family:{SERIF};font-style:italic;font-weight:400">semanas</tspan></text>
  <path id="pr-r" d="M{M} {TY + 150} L{1080 - M} {TY + 150}" {HAIR}/>
  <g id="pr-t1">{tag("pt1", "días", M, TY + 184, 180)}</g>
  <g id="pr-t2">{tag("pt2", "semanas", M + 204, TY + 184, 254)}</g>
  <g id="pr-t3">{tag("pt3", "fábricas", M + 482, TY + 184, 256)}</g>''')
R.hidden("#pr0, #pr1, #pr-r, #pr-t1, #pr-t2, #pr-t3", st)
R.fromTo("#pr0", "autoAlpha:0", "autoAlpha:1", st + 0.08, 0.2)
R.fromTo("#pr1", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.18, 0.26, EASE)
R.show("#pr-r", st + 0.42); R.draw("#pr-r", 1080 - 2 * M, st + 0.42, 0.5, "power2.inOut")
for k, at in enumerate([1.30, 2.40, 3.60]):
    R.fromTo(f"#pr-t{k + 1}", "autoAlpha:0, y:12", "autoAlpha:1, y:0", st + at, 0.24, EASE)

# ================================================================= 4 · ESCALAR · el dither
# El lenguaje cuadrado de Fashionalytics: celdas que crecen de ruido a señal.
st, en = S(8) - 0.05, E(9) + 0.20
GX, GY, CELL, GAP, N = 352, 392, 52, 12, 6
cells = ""
order = []
for r in range(N):
    for c in range(N):
        cells += (f'<rect id="g{r}{c}" class="cell" x="{GX + c * (CELL + GAP)}" y="{GY + r * (CELL + GAP)}" '
                  f'width="{CELL}" height="{CELL}" fill="{BRAND}"/>')
        order.append((r + c, f"#g{r}{c}"))
R.clip("grid", st, en, f'''
  {label("gr0", "Escalar un producto físico", M, 356, 26, INK_MUTED)}
  {cells}
  {data("gr1", "ruido", GX - 26, GY + 200, 24, INK_MUTED, "end")}
  {data("gr2", "señal", GX + N * (CELL + GAP) - GAP + 26, GY + 200, 24, BRAND)}''')
R.hidden("#gr0, #grid .cell, #gr1, #gr2", st)
R.fromTo("#gr0", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
for d, sel in order:
    at = st + 0.20 + d * 0.13
    R.fromTo(sel, "autoAlpha:0, scale:0.4, transformOrigin:'50% 50%'",
             f"autoAlpha:{0.16 + 0.084 * d:.2f}, scale:1", at, 0.22, EASE)
R.fromTo("#gr1, #gr2", "autoAlpha:0", "autoAlpha:1", st + 0.40, 0.2)

# ================================================================= 5-7 · LA PILA DE DIEZ
# Diez tags cuadrados que se van acumulando: cada uno es una de las cosas que ella enumera.
st, en = S(10) - 0.05, E(16) + 0.20
TAGS = [("Cadena de suministro", 0), ("Logística", 1), ("Inventario", 2), ("Fábricas", 3),
        ("Campaña", 4), ("Tu marca", 5), ("Paid media", 6), ("Tienda online", 7),
        ("Conversión", 8), ("+ mil cosas más", 9)]
TX, TY2, TW, TH, TSTEP = M, 352, 464, 58, 74
grid_tags = ""
for s_, k in TAGS:
    col, row = k // 5, k % 5
    grid_tags += tag(f"st{k}", s_, TX + col * (TW + 32), TY2 + row * TSTEP, TW, TH)
R.clip("pila", st, en, grid_tags)
R.hidden("#pila .tag", st)
AT = [0.10, 0.95, 1.75, 2.90, 4.40, 6.05, 9.30, 10.55, 12.10, 13.40]
for k, a in enumerate(AT):
    R.fromTo(f"#st{k}", "autoAlpha:0, y:14", "autoAlpha:1, y:0", st + a, 0.24, EASE)

# ================================================================= 8 · DIEZ PERSONAS
st, en = S(17) - 0.05, 35.92
SQ, SG = 58, 26
SX = (1080 - (10 * SQ + 9 * SG)) / 2
sq = "".join(f'<rect id="p{k}" class="per" x="{SX + k * (SQ + SG):.0f}" y="520" width="{SQ}" height="{SQ}" fill="{BRAND}"/>'
             for k in range(10))
R.clip("team", st, en, sq)
R.hidden("#team .per", st)
for k in range(10):
    R.fromTo(f"#p{k}", "autoAlpha:0, scale:0.4, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1",
             st + 0.06 + k * 0.055, 0.2, EASE)

# ================================================================= 9 · CIERRE · tema Screen
# El tema de marca: la página entera en blue-electric, para portada y cierre.
st = 35.92
R.scene("cierre", st, R.DUR, "transparent", f'''
  <rect x="0" y="0" width="1080" height="1920" fill="{BRAND}"/>
  <image href="{ASCII_BLUE}" x="-230" y="0" width="1540" height="1920"
     preserveAspectRatio="xMidYMid slice" opacity="0.55"/>
  <rect x="0" y="760" width="1080" height="880" fill="{BRAND}"/>
  <path d="M0 760 L1080 760" stroke="#c9c9ff" stroke-width="1" fill="none"/>
  <path d="M0 1640 L1080 1640" stroke="#c9c9ff" stroke-width="1" fill="none"/>''')
MODS = ["Core", "Commerce", "Inventory", "Product", "Production", "Intelligence", "Marketing", "Finance"]
mods = "".join(label(f"cm{k}", m, M + (k // 4) * 470, 1180 + (k % 4) * 62, 26, "#c9c9ff")
               for k, m in enumerate(MODS))
R.clip("cta", st, R.DUR, f'''
  {img("c-fold", FOLD_W, M, 820, 112, 3.972)}
  <path id="c-r" d="M{M} 1070 L{1080 - M} 1070" stroke="#c9c9ff" stroke-width="1" fill="none"/>
  {mods}
  {img("c-fa", FA_W, M, 1560, 34, 11.81)}''', hold=True)
R.hidden("#c-fold, #c-r, #cta .lab, #c-fa", st)
R.raw(f'  tl.set("#cta text", {{ autoAlpha: 0 }}, {st:.2f});')
R.fromTo("#c-fold", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.16, 0.3, EASE)
R.show("#c-r", st + 0.42); R.draw("#c-r", 1080 - 2 * M, st + 0.42, 0.4, "power2.inOut")
R.raw(f'  tl.fromTo("#cta text", {{ autoAlpha: 0, y: 8 }}, {{ autoAlpha: 1, y: 0, duration: 0.22, stagger: 0.05, ease: "{EASE}" }}, {st + 0.56:.2f});')
R.fromTo("#c-fa", "autoAlpha:0", "autoAlpha:1", st + 1.20, 0.3)

R.rail()

# ================================================================= estilo propio del reel
R.extra_css = f'''
      /* Subtítulos: Geist, sentence case, ink sobre la franja `surface`. Sin sombra. */
      .rail {{ top: 1496px; justify-content: flex-start; padding: 0 {M}px; }}
      .rail .line {{ max-width: 980px; text-align: left; color: {INK}; text-shadow: none;
        font-weight: 400; font-size: 46px; line-height: 1.26; letter-spacing: -0.01em; }}
      /* `accent-acid` es el resaltador: cuadrado, radius-none, nunca pastilla. */
      .rail .w.hot.pill {{ border-radius: 0; padding: 0.04em 0.18em 0.1em; margin: 0 0.02em; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
