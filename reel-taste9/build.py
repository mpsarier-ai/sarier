#!/usr/bin/env python3
"""FASHIONALYTICS / FOLD — reel 9: estética vs taste.

Mismo montaje que el reel 8: recursos de los reels de Sarier (subtítulos cinéticos centrados,
statements por capas, glitch, punch-in, escena faceless, fundido a negro) con el design system
de Fashionalytics/FOLD (packages/ui/tokens.css + el brand book publicado).

Reglas del sistema que mandan aquí:
  · `brand` #1a1aff es la única tinta de acción — y la palabra caliente de los subtítulos.
  · Texto `ink` sobre la zona clara del encuadre; blanco solo en el tercio inferior, que es oscuro.
  · Sin sombras: las capas se separan por valor y hairline.
  · Frases en sentence case; solo `label` (mono) y `pixel-title` van en MAYÚSCULAS.
  · Cuadrado (radius-none) para lo mono/ASCII/poster. La foto real va a sangre y sin filtros.
  · Movimiento 160 ms ease-out. Nada rebota.

La banda limpia del encuadre va de y=300 a y=610: su cabeza empieza en 645, así que todo gráfico
vive ahí arriba y los subtítulos abajo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("Fashionalytics · FOLD — estética vs taste", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="fold")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens (packages/ui/tokens.css)
GROUND, SURFACE, SUNKEN = "#f2f0ea", "#ffffff", "#e8e6df"
INK, INK_MUTED = "#0a0a12", "#5a5a66"
LINE, LINE_STRONG = "#c9c7c0", "#7a7a86"
BRAND = "#1a1aff"
SIG_RED = "#ff3b1f"
TAUPE = "#bda692"

SANS = "'Geist', -apple-system, 'SF Pro Text', system-ui, 'Liberation Sans', sans-serif"
MONO = "'IBM Plex Mono', 'SF Mono', Menlo, monospace"
SERIF = "'Instrument Serif', 'Times New Roman', serif"

M = 64
EASE = "power2.out"
TOP = 300          # arriba de la banda limpia


def t(id_, s, x, y, size, fam, fill=INK, anchor="start", weight=400, style="normal", tr="0", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text id="{id_}"{c} x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};font-style:{style};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def label(id_, s, x, y, size=24, fill=INK_MUTED, anchor="start", cls=""):
    """t-label · mono, SIEMPRE mayúsculas, tracking 0.08em."""
    return t(id_, s.upper(), x, y, size, MONO, fill, anchor, weight=500, tr="0.08em", cls=cls)


def data(id_, s, x, y, size=34, fill=INK, anchor="start", cls=""):
    return t(id_, s, x, y, size, MONO, fill, anchor, weight=400, tr="-0.01em", cls=cls)


def hair(id_, x1, y1, x2, y2, col=LINE_STRONG):
    return f'<path id="{id_}" d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1" fill="none"/>'


def box(id_, x, y, w, h, fill="none", stroke=LINE_STRONG, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<rect id="{id_}"{c} x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1"/>')


def img(id_, href, x, y, h, aspect):
    return f'<image id="{id_}" href="{href}" x="{x}" y="{y}" width="{h * aspect:.1f}" height="{h}"/>'


FOLD_INK = "brand/fold-lockup.svg"
FA_INK = "brand/fashionalytics-lockup.svg"

# ================================================================= subtítulos
R.card_frags = {1, 2, 32, 33, 34}
R.punch = {3: "diferentes", 4: "obsesione", 5: "Oberg", 6: "Djerf", 7: "proveedores",
           8: "fotógrafo", 9: "paleta", 10: "ella", 11: "respondiendo", 12: "taste",
           13: "juicio", 14: "pertenece", 15: "cortar", 16: "distrae", 17: "ve",
           18: "invisibles", 19: "debajo", 20: "feed", 21: "fundadores", 22: "plantillas",
           23: "descargar", 24: "no", 25: "construye", 26: "fondo", 27: "decisión",
           28: "difícil", 29: "funciona", 30: "por", 31: "taste"}
R.rail()

# ================================================================= bug de marca
R.clip("bug", 0.40, R.DUR, img("bg-logo", FOLD_INK, M, 218, 32, 3.972), hold=True)

# ================================================================= A · HOOK
R.card("hook", 0.0, E(2) + 0.20, [
    ("a", "Todo el mundo persigue una estética", 50, 0, TOP + 20, "center", "drop", 0.80),
    ("b", "taste", 150, 0, TOP + 86, "center", "scale", 1.0, 1.05),
    ("c", "y casi nadie construye", 50, 0, TOP + 254, "center", "drop", 0.88, 2.55)],
    glitch_key="b")
R.glitch(1.15)
R.punch_cam(1.25)

# ================================================================= B · DOS COSAS DISTINTAS
st, en = S(3) - 0.05, E(3) + 0.20
CW, CH, CY = 420, 220, TOP + 40
R.clip("dos", st, en, f'''
  {box("dz-a", 70, CY, CW, CH)}
  {box("dz-b", 590, CY, CW, CH, BRAND, BRAND)}
  {label("dz-la", "Lo que se ve", 70 + CW / 2, CY + 96, 25, INK_MUTED, "middle")}
  {t("dz-ta", "estética", 70 + CW / 2, CY + 160, 56, SANS, INK, "middle", 500, tr="-0.025em")}
  {label("dz-lb", "Lo que decides", 590 + CW / 2, CY + 96, 25, "#c9c9ff", "middle")}
  {t("dz-tb", "taste", 590 + CW / 2, CY + 160, 56, SANS, SURFACE, "middle", 500, tr="-0.025em")}''')
R.hidden("#dz-a, #dz-b, #dz-la, #dz-ta, #dz-lb, #dz-tb", st)
R.fromTo("#dz-a, #dz-la, #dz-ta", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.10, 0.26, EASE)
R.fromTo("#dz-b, #dz-lb, #dz-tb", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.46, 0.26, EASE)

# ================================================================= C · LAS TRES FOUNDERS
# Foto real, a sangre y sin filtros; el nombre en una franja `surface` dentro de la ficha.
st, en = S(5) - 0.10, E(6) + 0.55
FW, FH, FY, FS = 296, 308, TOP, 52
FOUNDERS = [("ob", "public/f-oberg.jpg", "Emily Oberg", 66),
            ("gz", "public/f-guizio.jpg", "Danielle Guizio", 392),
            ("dj", "public/f-djerf.jpg", "Matilda Djerf", 718)]
cards = '<defs>' + "".join(
    f'<clipPath id="cl-{k}"><rect x="{x}" y="{FY}" width="{FW}" height="{FH}"/></clipPath>'
    for k, _, _, x in FOUNDERS) + '</defs>'
for k, src, name, x in FOUNDERS:
    cards += (f'<g id="fc-{k}" class="fcard">'
              f'<image href="{src}" x="{x}" y="{FY}" width="{FW}" height="{FH}" '
              f'preserveAspectRatio="xMidYMid slice" clip-path="url(#cl-{k})"/>'
              f'<rect x="{x}" y="{FY + FH}" width="{FW}" height="{FS}" fill="{SURFACE}"/>'
              + label(f"fl-{k}", name, x + FW / 2, FY + FH + 34, 21, INK, "middle") + '</g>')
R.clip("founders", st, en, cards)
R.hidden("#founders .fcard", st)
for k, at in enumerate([0.22, 2.55, 3.70]):
    R.fromTo(f"#fc-{FOUNDERS[k][0]}", "autoAlpha:0, y:20", "autoAlpha:1, y:0", st + at, 0.30, EASE)

# ================================================================= D · LO QUE SÍ SE PUEDE COPIAR
# Tres cosas que se marcan como copiadas, y una línea que las tacha todas.
st, en = S(7) - 0.05, E(10) + 0.20
COPY = [("Los mismos proveedores", 0.15), ("El mismo fotógrafo", 2.70), ("La paleta de colores exacta", 4.30)]
RY, RH, RSTEP, RX, RW = TOP + 10, 56, 76, 150, 780
rows = ""
for k, (txt_, _) in enumerate(COPY):
    y = RY + k * RSTEP
    rows += (box(f"cp-b{k}", RX, y, 36, 36, "none", LINE_STRONG)
             + f'<rect id="cp-f{k}" x="{RX + 7}" y="{y + 7}" width="22" height="22" fill="{BRAND}"/>'
             + label(f"cp-t{k}", txt_, RX + 60, y + 27, 25, INK)
             + hair(f"cp-x{k}", RX + 52, y + 18, RX + RW, y + 18))
R.clip("copia", st, en, rows
       + label("cp-note", "y aún así no se siente igual", 540, RY + 3 * RSTEP + 36, 26, SIG_RED, "middle"))
R.hidden("#copia rect, #copia text, #copia path", st)
for k, (_, at) in enumerate(COPY):
    R.show(f"#cp-b{k}", st + at)
    R.fromTo(f"#cp-b{k}", "autoAlpha:1, scale:0.6, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + at, 0.22, EASE)
    R.fromTo(f"#cp-t{k}", "autoAlpha:0, x:-14", "autoAlpha:1, x:0", st + at + 0.06, 0.24, EASE)
    R.show(f"#cp-f{k}", st + at + 0.30)
    R.fromTo(f"#cp-f{k}", "autoAlpha:1, scale:0, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + at + 0.30, 0.22, EASE)
TACH = E(9) - st + 0.10
for k in range(3):
    R.show(f"#cp-x{k}", st + TACH + k * 0.12)
    R.draw(f"#cp-x{k}", RW - 52, st + TACH + k * 0.12, 0.34, "power2.inOut")
R.fromTo("#cp-note", "autoAlpha:0, y:10", "autoAlpha:1, y:0", st + TACH + 0.55, 0.3, EASE)

# ================================================================= E · LA PALETA NO ERA LA RESPUESTA
st, en = S(11) - 0.05, E(12) + 0.20
SWW, SWY = 150, TOP + 40
SW_COLS = [GROUND, SUNKEN, TAUPE, LINE_STRONG, INK]
sw = "".join(f'<rect id="pa{k}" class="sw" x="{150 + k * (SWW + 16)}" y="{SWY}" width="{SWW}" height="{SWW}" '
             f'fill="{c}" stroke="{LINE_STRONG}" stroke-width="1"/>' for k, c in enumerate(SW_COLS))
R.clip("paleta", st, en, f'''
  {label("pa-l", "A esto no estabas respondiendo", 540, TOP, 25, INK_MUTED, "middle")}
  {sw}
  {t("pa-t", "era ese taste", 540, SWY + SWW + 82, 72, SANS, INK, "middle", 500, tr="-0.025em")}''')
R.hidden("#pa-l, #paleta .sw, #pa-t", st)
R.fromTo("#pa-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.raw(f'  tl.fromTo("#paleta .sw", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.24, stagger: 0.08, ease: "{EASE}" }}, {st + 0.14:.2f});')
R.raw(f'  tl.to("#paleta .sw", {{ autoAlpha: 0.35, duration: 0.4, stagger: 0.04, ease: "{EASE}" }}, {E(11) - st + st + 0.20:.2f});')
R.fromTo("#pa-t", "autoAlpha:0, y:18", "autoAlpha:1, y:0", E(11) + 0.45, 0.34, EASE)

# ================================================================= F · EL TASTE ES JUICIO
# Cuatro decisiones: la que construye lleva barra `brand`, la que se corta solo hairline.
st, en = S(13) - 0.05, E(16) + 0.20
DEC = [("Pertenece a la colección", True, 0.55), ("Hay que cortarla", False, 2.05),
       ("Este color construye", True, 3.85), ("Este otro distrae", False, 5.15)]
DY, DSTEP, DX, DW = TOP + 14, 72, 170, 760
dec = label("de-l", "El taste es juicio", 540, TOP - 26, 25, INK_MUTED, "middle")
for k, (txt_, keep, _) in enumerate(DEC):
    y = DY + k * DSTEP
    dec += (f'<rect id="de-b{k}" x="{DX}" y="{y}" width="6" height="44" fill="{BRAND if keep else LINE_STRONG}"/>'
            + label(f"de-t{k}", txt_, DX + 26, y + 31, 25, INK if keep else INK_MUTED)
            + (hair(f"de-x{k}", DX + 20, y + 22, DX + DW, y + 22) if not keep else ""))
R.clip("juicio", st, en, dec)
R.hidden("#juicio rect, #juicio text, #juicio path", st)
R.fromTo("#de-l", "autoAlpha:0", "autoAlpha:1", st + 0.04, 0.2)
for k, (_, keep, at) in enumerate(DEC):
    R.show(f"#de-b{k}", st + at)
    R.fromTo(f"#de-b{k}", "autoAlpha:1, scaleY:0, transformOrigin:'50% 0%'", "autoAlpha:1, scaleY:1", st + at, 0.24, EASE)
    R.fromTo(f"#de-t{k}", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", st + at + 0.06, 0.24, EASE)
    if not keep:
        R.show(f"#de-x{k}", st + at + 0.34)
        R.draw(f"#de-x{k}", DW - 20, st + at + 0.34, 0.3, "power2.inOut")

# ================================================================= G · LO QUE SE VE Y LO QUE NO
# El gráfico central: la estética es el bloque de arriba; el taste, el campo de decisiones de abajo.
st, en = S(17) - 0.05, E(19) + 0.20
SURF_Y = TOP + 112
BW_, BH_ = 220, 62
GCOL, GROW, GSZ, GGAP = 26, 5, 14, 8
GW_ = GCOL * GSZ + (GCOL - 1) * GGAP
GX_ = (1080 - GW_) / 2
dots = ""
for r in range(GROW):
    for c in range(GCOL):
        dots += (f'<rect id="ic{r}-{c}" class="icell" x="{GX_ + c * (GSZ + GGAP):.0f}" '
                 f'y="{SURF_Y + 36 + r * (GSZ + GGAP)}" width="{GSZ}" height="{GSZ}" fill="{BRAND}"/>')
R.clip("iceberg", st, en, f'''
  <rect id="ic-top" x="{(1080 - BW_) / 2}" y="{SURF_Y - BH_ - 14}" width="{BW_}" height="{BH_}" fill="{INK}"/>
  {label("ic-lt", "Estética", 540, SURF_Y - BH_ + 26, 25, SURFACE, "middle")}
  {hair("ic-line", 90, SURF_Y, 990, SURF_Y)}
  {label("ic-ls", "Lo que se ve", 990, SURF_Y - 16, 22, INK_MUTED, "end")}
  {dots}
  {label("ic-lb", "Taste · las decisiones invisibles", 540, SURF_Y + 36 + GROW * (GSZ + GGAP) + 34, 25, BRAND, "middle")}''')
R.hidden("#ic-top, #ic-lt, #ic-line, #ic-ls, #iceberg .icell, #ic-lb", st)
R.fromTo("#ic-top, #ic-lt", "autoAlpha:0, y:-14", "autoAlpha:1, y:0", st + 0.08, 0.28, EASE)
R.show("#ic-line", st + 0.34); R.draw("#ic-line", 900, st + 0.34, 0.45, "power2.inOut")
R.fromTo("#ic-ls", "autoAlpha:0", "autoAlpha:1", st + 0.55, 0.22)
R.raw(f'  tl.fromTo("#iceberg .icell", {{ autoAlpha: 0, scale: 0.3, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, scale: 1, duration: 0.22, stagger: {{ each: 0.012, from: "start" }}, ease: "{EASE}" }}, {st + 0.95:.2f});')
R.fromTo("#ic-lb", "autoAlpha:0", "autoAlpha:1", st + 2.60, 0.3)

# ================================================================= H · EL MISMO FEED
st, en = S(20) - 0.05, E(22) + 0.20
TS, TG = 84, 12
TGX = (1080 - (3 * TS + 2 * TG)) / 2
tiles = "".join(f'<rect id="tl{k}" class="tile" x="{TGX + (k % 3) * (TS + TG):.0f}" '
                f'y="{TOP + 10 + (k // 3) * (TS + TG)}" width="{TS}" height="{TS}" fill="none" '
                f'stroke="{LINE_STRONG}" stroke-width="1"/>' for k in range(9))
fills = "".join(f'<rect id="tf{k}" class="tfill" x="{TGX + (k % 3) * (TS + TG) + 1:.0f}" '
                f'y="{TOP + 11 + (k // 3) * (TS + TG)}" width="{TS - 2}" height="{TS - 2}" fill="{SUNKEN}"/>'
                for k in range(9))
R.clip("feed", st, en, f'''
  {label("fd-l", "El feed de tantos fundadores", 540, TOP, 25, INK_MUTED, "middle")}
  {tiles}{fills}
  {label("fd-n", "Las mismas tres o cuatro plantillas", 540, TOP + 10 + 3 * (TS + TG) + 34, 25, SIG_RED, "middle")}''')
R.hidden("#fd-l, #feed .tile, #feed .tfill, #fd-n", st)
R.fromTo("#fd-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.raw(f'  tl.fromTo("#feed .tile", {{ autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%" }}, {{ autoAlpha: 1, scale: 1, duration: 0.22, stagger: 0.07, ease: "{EASE}" }}, {st + 0.16:.2f});')
R.raw(f'  tl.fromTo("#feed .tfill", {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.2, stagger: 0.06, ease: "{EASE}" }}, {st + 2.30:.2f});')
R.fromTo("#fd-n", "autoAlpha:0, y:10", "autoAlpha:1, y:0", st + 3.70, 0.3, EASE)

# ================================================================= I-J · DESCARGAR vs CONSTRUIR
# La barra de carga del sistema: una se llena sola, la otra se construye por pasos.
st, en = S(23) - 0.05, E(31) + 0.20
BX_, BW2, BH2 = 170, 740, 10
AY1, AY2 = TOP + 34, TOP + 150
STEPS = [("Estudias algo a fondo", 52.30), ("Tomas una decisión difícil", 55.00),
         ("Lanzas y averiguas por qué", 58.00)]
steps_svg = "".join(label(f"ps{k}", s_, BX_, AY2 + 78 + k * 46, 24, INK_MUTED) for k, (s_, _) in enumerate(STEPS))
R.clip("barras", st, en, f'''
  {label("ba-l1", "Una estética se descarga", BX_, AY1 - 22, 25, INK_MUTED)}
  <rect id="ba-t1" x="{BX_}" y="{AY1}" width="{BW2}" height="{BH2}" fill="{SUNKEN}" stroke="{LINE_STRONG}" stroke-width="1"/>
  <rect id="ba-f1" x="{BX_}" y="{AY1}" width="{BW2}" height="{BH2}" fill="{INK}"/>
  {label("ba-p1", "100%", BX_ + BW2, AY1 - 22, 25, INK, "end")}
  {label("ba-l2", "El taste se construye", BX_, AY2 - 22, 25, BRAND)}
  <rect id="ba-t2" x="{BX_}" y="{AY2}" width="{BW2}" height="{BH2}" fill="{SUNKEN}" stroke="{LINE_STRONG}" stroke-width="1"/>
  <rect id="ba-f2" x="{BX_}" y="{AY2}" width="{BW2}" height="{BH2}" fill="{BRAND}"/>
  {steps_svg}''')
R.hidden("#barras rect, #barras text", st)
R.fromTo("#ba-l1, #ba-t1", "autoAlpha:0", "autoAlpha:1", st + 0.10, 0.22)
R.show("#ba-f1", st + 0.30)
R.fromTo("#ba-f1", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:1", st + 0.30, 0.9, "power2.inOut")
R.fromTo("#ba-p1", "autoAlpha:0", "autoAlpha:1", st + 1.20, 0.22)
R.fromTo("#ba-l2, #ba-t2", "autoAlpha:0", "autoAlpha:1", S(24) + 0.10, 0.22)
R.show("#ba-f2", S(25))
R.fromTo("#ba-f2", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:0.08", S(25), 0.3, EASE)
for k, (_, at) in enumerate(STEPS):
    R.fromTo("#ba-f2", f"scaleX:{0.08 + k * 0.30:.2f}, transformOrigin:'0% 50%'",
             f"scaleX:{0.08 + (k + 1) * 0.30:.2f}", at, 0.55, "power2.inOut")
    R.fromTo(f"#ps{k}", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", at + 0.05, 0.26, EASE)
R.fromTo("#ba-f2", "scaleX:0.98, transformOrigin:'0% 50%'", "scaleX:1", 60.90, 0.5, "power2.inOut")

# ================================================================= K · CIERRE
R.card("cierre", S(32) - 0.05, R.DUR, [
    ("a", "Deja de preguntarte cuál es", 50, 0, TOP + 20, "center", "drop", 0.80),
    ("b", "tu estética", 92, 0, TOP + 76, "center", "drop", 0.88, S(33)),
    ("c", "construye tu taste.", 112, 0, TOP + 210, "center", "scale", 1.0, S(34) - 0.10)])
R.slow_push(S(32))
R.fadeout(0.40)

# ================================================================= estilo propio del reel
R.extra_css = f'''
      /* Subtítulos centrados sobre el plano, sin caja y sin sombra, en el tercio inferior oscuro. */
      .rail {{ top: 1424px; }}
      .rail .line {{ max-width: 920px; color: {SURFACE}; text-shadow: none;
        font-weight: 500; font-size: 56px; line-height: 1.18; letter-spacing: -0.02em; }}
      .rail .w.hot {{ color: #a3a3ff; text-shadow: none; }}
      /* Statements: ink sobre la pared clara, nunca blancos con sombra. */
      .card {{ height: 900px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-weight: 500; }}
      /* El glitch usa los dos acentos del sistema. */
      .gstack .warm {{ color: {SIG_RED}; }}
      .gstack .cool {{ color: {BRAND}; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
