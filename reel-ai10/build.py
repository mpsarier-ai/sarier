#!/usr/bin/env python3
"""FASHIONALYTICS / FOLD — reel 10: IA y pensamiento crítico.

Mismo montaje que los reels 8 y 9: recursos de Sarier (subtítulos cinéticos centrados, statements
por capas, glitch, punch-in, fundido a negro) con el design system de Fashionalytics/FOLD.

El guion trae datos duros, así que este reel se apoya en lo que mejor hace el sistema: `data-lg`
en mono con números tabulares, barras con relleno `brand` y los badges de procedencia.

Encuadre: su cabeza empieza en y=636, así que la banda limpia de gráficos va de 290 a 600 y los
subtítulos van al tercio inferior, que es oscuro.

El logo de Claude Code: si existe `brand/claude-code.svg` se usa; mientras no exista, el momento se
resuelve con la tarjeta de terminal, que es lo que Claude Code es. No se redibuja una marca ajena.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("Fashionalytics · FOLD — IA y pensamiento crítico", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="fold")
S, E = R.S, R.E

GROUND, SURFACE, SUNKEN = "#f2f0ea", "#ffffff", "#e8e6df"
INK, INK_MUTED = "#0a0a12", "#5a5a66"
LINE, LINE_STRONG = "#c9c7c0", "#7a7a86"
BRAND = "#1a1aff"
DANGER, SUCCESS = "#c42408", "#0f7a2a"
SIG_RED = "#ff3b1f"

SANS = "'Geist', -apple-system, 'SF Pro Text', system-ui, 'Liberation Sans', sans-serif"
MONO = "'IBM Plex Mono', 'SF Mono', Menlo, monospace"
SERIF = "'Instrument Serif', 'Times New Roman', serif"

M, EASE, TOP = 64, "power2.out", 290
DOWN = "\u25bc"   # glifo de variación del sistema
CC_LOGO = "brand/claude-code.svg"
HAS_CC = os.path.exists(CC_LOGO)


def t(id_, s, x, y, size, fam, fill=INK, anchor="start", weight=400, style="normal", tr="0", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text id="{id_}"{c} x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};font-style:{style};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def label(id_, s, x, y, size=24, fill=INK_MUTED, anchor="start", cls=""):
    return t(id_, s.upper(), x, y, size, MONO, fill, anchor, weight=500, tr="0.08em", cls=cls)


def data(id_, s, x, y, size=34, fill=INK, anchor="start", cls=""):
    """t-data · mono con números tabulares."""
    return t(id_, s, x, y, size, MONO, fill, anchor, weight=400, tr="-0.01em", cls=cls)


def hair(id_, x1, y1, x2, y2, col=LINE_STRONG):
    return f'<path id="{id_}" d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1" fill="none"/>'


def card(id_, x, y, w, h, fill=SURFACE, stroke=LINE_STRONG, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<rect id="{id_}"{c} x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1"/>')


def badge(id_, s, x, y, w=168, h=30, bg=SUNKEN, fg=INK, bd="none"):
    """fx-badge · los cinco niveles de verdad. radius-none, mono, mayúsculas."""
    return (f'<g id="{id_}" class="bdg"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" '
            f'stroke="{bd}" stroke-width="1"/>'
            + t(f"{id_}t", s.upper(), x + w / 2, y + h / 2 + 7, 19, MONO, fg, "middle", 500, tr="0.08em") + '</g>')


def img(id_, href, x, y, h, aspect):
    return f'<image id="{id_}" href="{href}" x="{x}" y="{y}" width="{h * aspect:.1f}" height="{h}"/>'


FOLD_INK = "brand/fold-lockup.svg"

# ================================================================= subtítulos
R.card_frags = {1, 39}
R.punch = {2: "Claude", 3: "clásica", 4: "mundo", 5: "datos", 6: "convencer", 7: "persona",
           8: "futuro", 9: "IA", 10: "problema", 11: "crítico", 12: "artificial", 13: "otro",
           14: "igual", 15: "haciendo", 16: "británico", 17: "frecuente", 18: "cognitivas",
           19: "negativamente", 20: "usan", 21: "éxito", 22: "perderse", 23: "libros",
           24: "largo", 25: "mental", 26: "cognitiva", 27: "complejos", 28: "filosóficas",
           29: "entrenan", 30: "ninguna", 31: "único", 32: "protege", 33: "nadie",
           34: "ochenta", 35: "veinte", 36: "cinco", 37: "destreza", 38: "subconjunto"}
R.rail()

# ================================================================= bug de marca
R.clip("bug", 0.40, R.DUR, img("bg-logo", FOLD_INK, M, 214, 32, 3.972), hold=True)

# ================================================================= A · HOOK
R.card("hook", 0.0, E(1) + 0.25, [
    ("a", "La persona más exitosa", 56, 0, TOP + 40, "center", "drop", 0.82),
    ("b", "que conoces", 128, 0, TOP + 104, "center", "scale", 1.0, 0.70)], glitch_key="b")
R.glitch(0.80)
R.punch_cam(0.90)

# ================================================================= B · EL DÍPTICO
# De nueve a cinco, la terminal. Y luego, en la casa, el libro.
st, en = S(2) - 0.08, E(3) + 0.25
DW_, DH_, DY_ = 420, 236, TOP + 20
LX, RX = 70, 590
cc = (img("cc-logo", CC_LOGO, LX + 28, DY_ + 34, 44, 1.0) if HAS_CC else "")
R.clip("diptico", st, en, f'''
  <g id="dp-l">
    {card("dp-lc", LX, DY_, DW_, DH_)}
    {cc}
    {data("dp-lt", "~ $ claude", LX + (96 if HAS_CC else 28), DY_ + 68, 34, INK)}
    <rect id="dp-cur" x="{LX + (96 if HAS_CC else 28)}" y="{DY_ + 92}" width="18" height="34" fill="{BRAND}"/>
    {hair("dp-lr", LX + 28, DY_ + 152, LX + DW_ - 28, DY_ + 152)}
    {label("dp-ll", "De nueve a cinco", LX + 28, DY_ + 196, 23, INK_MUTED)}
  </g>
  <g id="dp-r">
    {card("dp-rc", RX, DY_, DW_, DH_)}
    {t("dp-rt", "literatura", RX + 28, DY_ + 78, 52, SERIF, INK, "start", 400, "italic")}
    {t("dp-rt2", "clásica", RX + 28, DY_ + 146, 52, SERIF, INK, "start", 400, "italic")}
    {hair("dp-rr", RX + 28, DY_ + 152, RX + DW_ - 28, DY_ + 152, "none")}
    {label("dp-rl", "Y luego en la casa", RX + 28, DY_ + 196, 23, INK_MUTED)}
  </g>''')
R.hidden("#dp-l, #dp-r", st)
R.fromTo("#dp-l", "autoAlpha:0, y:18", "autoAlpha:1, y:0", st + 0.12, 0.30, EASE)
R.raw(f'  tl.to("#dp-cur", {{ autoAlpha: 0, duration: 0.01, repeat: 9, yoyo: true, repeatDelay: 0.26, ease: "none" }}, {st + 0.55:.2f});')
R.fromTo("#dp-r", "autoAlpha:0, y:18", "autoAlpha:1, y:0", S(3) + 0.10, 0.30, EASE)

# ================================================================= C · SESENTA SEGUNDOS DE DATOS
st, en = S(5) - 0.06, E(9) + 0.20
BX_, BW_, BY_ = 210, 660, TOP + 186
R.clip("brief", st, en, f'''
  {label("br-l", "Sesenta segundos de datos", 540, TOP + 6, 25, INK_MUTED, "middle")}
  {t("br-n", "60s", 540, TOP + 136, 104, MONO, INK, "middle", 400, tr="-0.02em")}
  <rect id="br-t" x="{BX_}" y="{BY_}" width="{BW_}" height="10" fill="{SUNKEN}" stroke="{LINE_STRONG}" stroke-width="1"/>
  <rect id="br-f" x="{BX_}" y="{BY_}" width="{BW_}" height="10" fill="{BRAND}"/>
  {label("br-n2", "Las personas exitosas del futuro serán nativas de la IA", 540, BY_ + 58, 23, INK, "middle")}''')
R.hidden("#br-l, #br-n, #br-t, #br-f, #br-n2", st)
R.fromTo("#br-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.fromTo("#br-n", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.16, 0.3, EASE)
R.fromTo("#br-t", "autoAlpha:0", "autoAlpha:1", st + 0.34, 0.2)
R.show("#br-f", st + 0.40)
R.fromTo("#br-f", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:1",
         st + 0.40, 7.6, "none")
R.fromTo("#br-n2", "autoAlpha:0, y:10", "autoAlpha:1, y:0", S(8) + 0.20, 0.3, EASE)

# ================================================================= D · TODO SE VUELVE IGUAL
# Siete piezas distintas que, al delegar el juicio, terminan siendo la misma.
st, en = S(10) - 0.05, E(15) + 0.20
QN, QS, QG = 7, 100, 20
QX = (1080 - (QN * QS + (QN - 1) * QG)) / 2
QY = TOP + 70
VAR = [INK, "none", BRAND, SUNKEN, "none", INK, BRAND]
qs = "".join(f'<rect id="q{k}" class="qq" x="{QX + k * (QS + QG):.0f}" y="{QY}" width="{QS}" height="{QS}" '
             f'fill="{VAR[k]}" stroke="{LINE_STRONG}" stroke-width="1"/>' for k in range(QN))
R.clip("igual", st, en, f'''
  {label("ig-l", "Delegas el pensamiento crítico", 540, TOP + 18, 25, INK_MUTED, "middle")}
  {qs}
  {label("ig-n", "Y todo lo que produces se vuelve igual", 540, QY + QS + 56, 25, SIG_RED, "middle")}''')
R.hidden("#ig-l, #igual .qq, #ig-n", st)
R.fromTo("#ig-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.raw(f'  tl.fromTo("#igual .qq", {{ autoAlpha: 0, y: 14 }}, {{ autoAlpha: 1, y: 0, duration: 0.22, stagger: 0.07, ease: "{EASE}" }}, {st + 0.14:.2f});')
R.raw(f'  tl.to("#igual .qq", {{ fill: "{SUNKEN}", duration: 0.5, stagger: 0.05, ease: "{EASE}" }}, {S(14) - 0.20:.2f});')
R.fromTo("#ig-n", "autoAlpha:0, y:10", "autoAlpha:1, y:0", S(14) + 0.45, 0.3, EASE)

# ================================================================= E · EL ESTUDIO
st, en = S(16) - 0.05, E(22) + 0.20
SY = TOP + 64
R.clip("estudio", st, en, f'''
  {label("es-l", "Estudio británico", 180, TOP + 16, 25, INK_MUTED)}
  {badge("es-bd", "Observed", 760, TOP - 6, 150, 30)}
  {hair("es-r", 180, TOP + 36, 910, TOP + 36)}
  {label("es-a", "Uso frecuente de IA", 180, SY + 34, 24, INK)}
  <rect id="es-ab" x="620" y="{SY + 14}" width="290" height="22" fill="{INK}"/>
  {label("es-b", "Pensamiento crítico", 180, SY + 104, 24, INK)}
  <rect id="es-bb" x="620" y="{SY + 84}" width="290" height="22" fill="{DANGER}"/>
  {t("es-ar", DOWN, 944, SY + 106, 30, MONO, INK, "end")}
  {hair("es-r2", 180, SY + 160, 910, SY + 160)}
  {label("es-c1", "Al borde del éxito", 180, SY + 212, 24, SUCCESS)}
  {label("es-c2", "Al borde de perderse", 910, SY + 212, 24, DANGER, "end")}
  <rect id="es-dot" x="533" y="{SY + 196}" width="14" height="14" fill="{BRAND}"/>''')
R.hidden("#estudio text, #estudio rect, #estudio path, #es-bd", st)
R.fromTo("#es-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.fromTo("#es-bd", "autoAlpha:0, x:14", "autoAlpha:1, x:0", st + 0.20, 0.26, EASE)
R.show("#es-r", st + 0.34); R.draw("#es-r", 730, st + 0.34, 0.4, "power2.inOut")
R.fromTo("#es-a", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", S(17) + 0.10, 0.26, EASE)
R.show("#es-ab", S(17) + 0.25)
R.fromTo("#es-ab", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:1", S(17) + 0.25, 0.5, EASE)
R.fromTo("#es-b", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", S(19) + 0.10, 0.26, EASE)
R.show("#es-bb", S(19) + 0.25)
R.fromTo("#es-bb", "autoAlpha:1, scaleX:1, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:0.26", S(19) + 0.25, 0.7, "power2.inOut")
R.fromTo("#es-ar", "autoAlpha:0, y:-10", "autoAlpha:1, y:0", S(19) + 0.70, 0.3, EASE)
R.show("#es-r2", S(20) + 0.10); R.draw("#es-r2", 730, S(20) + 0.10, 0.4, "power2.inOut")
R.fromTo("#es-c1", "autoAlpha:0", "autoAlpha:1", S(21) + 0.05, 0.26)
R.fromTo("#es-dot", "autoAlpha:0, scale:0.4, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", S(21) + 0.30, 0.26, EASE)
R.fromTo("#es-c2", "autoAlpha:0", "autoAlpha:1", S(22) + 0.05, 0.26)

# ================================================================= F · ANCHO DE BANDA
st, en = S(23) - 0.05, E(26) + 0.20
FY_ = TOP + 76
R.clip("banda", st, en, f'''
  {label("bn-l", "Ancho de banda mental", 540, TOP + 18, 25, INK_MUTED, "middle")}
  {label("bn-a", "Formato corto", 180, FY_ + 28, 24, INK_MUTED)}
  <rect id="bn-ab" x="520" y="{FY_ + 10}" width="110" height="18" fill="{LINE_STRONG}"/>
  {label("bn-b", "Formato largo", 180, FY_ + 118, 24, INK)}
  <rect id="bn-bb" x="520" y="{FY_ + 86}" width="390" height="46" fill="{BRAND}"/>
  {label("bn-n", "Y capacidad cognitiva para disfrutarlos", 540, FY_ + 196, 24, INK_MUTED, "middle")}''')
R.hidden("#banda text, #banda rect", st)
R.fromTo("#bn-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.fromTo("#bn-a", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", st + 0.18, 0.26, EASE)
R.show("#bn-ab", st + 0.30)
R.fromTo("#bn-ab", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:1", st + 0.30, 0.35, EASE)
R.fromTo("#bn-b", "autoAlpha:0, x:-12", "autoAlpha:1, x:0", S(24) + 0.10, 0.26, EASE)
R.show("#bn-bb", S(24) + 0.25)
R.fromTo("#bn-bb", "autoAlpha:1, scaleX:0, transformOrigin:'0% 50%'", "autoAlpha:1, scaleX:1", S(24) + 0.25, 0.6, EASE)
R.fromTo("#bn-n", "autoAlpha:0", "autoAlpha:1", S(26) + 0.10, 0.3)

# ================================================================= G · LOS CLÁSICOS ENTRENAN
st, en = S(27) - 0.05, E(30) + 0.20
GY_, GBW, GBG = TOP + 230, 110, 24
GX_ = (1080 - (5 * GBW + 4 * GBG)) / 2
HT = [44, 76, 110, 150, 196]
bars = "".join(f'<rect id="gb{k}" class="gb" x="{GX_ + k * (GBW + GBG):.0f}" y="{GY_ - HT[k]}" '
               f'width="{GBW}" height="{HT[k]}" fill="{BRAND if k == 4 else LINE_STRONG}"/>' for k in range(5))
R.clip("entrena", st, en, f'''
  {label("en-l", "Lo que entrena tu capacidad cognitiva", 540, TOP + 18, 25, INK_MUTED, "middle")}
  {bars}
  {hair("en-ax", GX_ - 20, GY_, GX_ + 5 * GBW + 4 * GBG + 20, GY_)}
  {label("en-n", "Los clásicos y la filosofía", GX_ + 5 * GBW + 4 * GBG + 20, GY_ + 46, 24, BRAND, "end")}''')
R.hidden("#en-l, #entrena .gb, #en-ax, #en-n", st)
R.fromTo("#en-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.show("#en-ax", st + 0.14); R.draw("#en-ax", 5 * GBW + 4 * GBG + 40, st + 0.14, 0.4, "power2.inOut")
R.raw(f'  tl.fromTo("#entrena .gb", {{ autoAlpha: 1, scaleY: 0, transformOrigin: "50% 100%" }}, {{ autoAlpha: 1, scaleY: 1, duration: 0.34, stagger: 0.16, ease: "{EASE}" }}, {st + 0.30:.2f});')
R.raw(f'  tl.set("#entrena .gb", {{ autoAlpha: 1 }}, {st + 0.30:.2f});')
R.fromTo("#en-n", "autoAlpha:0", "autoAlpha:1", S(28) + 0.40, 0.3)

# ================================================================= H · LO QUE NADIE HACE
st, en = S(31) - 0.05, E(33) + 0.20
R.clip("nadie", st, en, f'''
  {card("na-c", 240, TOP + 40, 600, 190)}
  {t("na-t", "lo único que te protege", 540, TOP + 112, 50, SERIF, INK, "middle", 400, "italic")}
  {hair("na-r", 300, TOP + 142, 780, TOP + 142)}
  {label("na-l", "Es justamente lo que nadie hace", 540, TOP + 192, 24, SIG_RED, "middle")}''')
R.hidden("#na-c, #na-t, #na-r, #na-l", st)
R.fromTo("#na-c", "autoAlpha:0, y:16", "autoAlpha:1, y:0", st + 0.08, 0.3, EASE)
R.fromTo("#na-t", "autoAlpha:0", "autoAlpha:1", st + 0.26, 0.3)
R.show("#na-r", st + 0.50); R.draw("#na-r", 480, st + 0.50, 0.36, "power2.inOut")
R.fromTo("#na-l", "autoAlpha:0, y:10", "autoAlpha:1, y:0", S(33) + 0.05, 0.3, EASE)

# ================================================================= I · LOS DOS NÚMEROS
# StatTile: el número en `data-lg` mono tabular, con su etiqueta y su nota.
st, en = S(34) - 0.05, E(37) + 0.25
TW_, TH_, TY_ = 440, 250, TOP + 44
R.clip("stats", st, en, f'''
  <g id="sx-a">
    {card("sa-c", 70, TY_, TW_, TH_)}
    {label("sa-l", "De los libros del mundo", 70 + 28, TY_ + 46, 21, INK_MUTED)}
    {t("sa-n", "80%", 70 + 28, TY_ + 136, 86, MONO, INK, "start", 400, tr="-0.01em")}
    {hair("sa-r", 70 + 28, TY_ + 166, 70 + TW_ - 28, TY_ + 166)}
    {label("sa-s", "Los lee el 20% de la gente", 70 + 28, TY_ + 206, 20, INK_MUTED)}
  </g>
  <g id="sx-b">
    {card("sb-c", 570, TY_, TW_, TH_, BRAND, BRAND)}
    {label("sb-l", "De las personas", 570 + 28, TY_ + 46, 21, "#c9c9ff")}
    {t("sb-n", "5%", 570 + 28, TY_ + 136, 86, MONO, SURFACE, "start", 400, tr="-0.01em")}
    {hair("sb-r", 570 + 28, TY_ + 166, 570 + TW_ - 28, TY_ + 166, "#c9c9ff")}
    {label("sb-s", "Sabe usar IA con destreza", 570 + 28, TY_ + 206, 20, "#c9c9ff")}
  </g>''')
R.hidden("#sx-a, #sx-b", st)
R.fromTo("#sx-a", "autoAlpha:0, y:18", "autoAlpha:1, y:0", st + 0.12, 0.3, EASE)
R.fromTo("#sx-b", "autoAlpha:0, y:18", "autoAlpha:1, y:0", S(36) + 0.10, 0.3, EASE)

# ================================================================= J · EL SUBCONJUNTO
st = S(38) - 0.05
NX, NY = 540, TOP + 150
R.clip("sub", st, S(39) + 0.70, f'''
  {label("su-l", "El subconjunto de un subconjunto", 540, TOP + 18, 25, INK_MUTED, "middle")}
  <rect id="su-1" x="{NX - 230}" y="{NY - 120}" width="460" height="240" fill="none" stroke="{LINE_STRONG}" stroke-width="1"/>
  <rect id="su-2" x="{NX - 140}" y="{NY - 76}" width="280" height="152" fill="none" stroke="{LINE_STRONG}" stroke-width="1"/>
  <rect id="su-3" x="{NX - 56}" y="{NY - 30}" width="112" height="60" fill="{BRAND}"/>
  {label("su-n", "Ahí", NX, NY + 12, 24, SURFACE, "middle")}''')
R.hidden("#su-l, #su-1, #su-2, #su-3, #su-n", st)
R.fromTo("#su-l", "autoAlpha:0", "autoAlpha:1", st + 0.06, 0.2)
R.fromTo("#su-1", "autoAlpha:0, scale:0.9, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + 0.14, 0.28, EASE)
R.fromTo("#su-2", "autoAlpha:0, scale:0.9, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + 0.40, 0.28, EASE)
R.fromTo("#su-3, #su-n", "autoAlpha:0, scale:0.7, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + 0.66, 0.28, EASE)

# ================================================================= K · CIERRE
R.card("cierre", S(39) - 0.05, R.DUR, [
    ("a", "Y es ahí", 62, 0, TOP + 36, "center", "drop", 0.82),
    ("b", "donde necesitas estar.", 104, 0, TOP + 100, "center", "scale", 1.0, S(39) + 0.45)])
R.slow_push(S(39))
R.fadeout(0.40)

# ================================================================= estilo propio del reel
R.extra_css = f'''
      .rail {{ top: 1424px; }}
      .rail .line {{ max-width: 920px; color: {SURFACE}; text-shadow: none;
        font-weight: 500; font-size: 56px; line-height: 1.18; letter-spacing: -0.02em; }}
      .rail .w.hot {{ color: #a3a3ff; text-shadow: none; }}
      .card {{ height: 900px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-weight: 500; }}
      .gstack .warm {{ color: {SIG_RED}; }}
      .gstack .cool {{ color: {BRAND}; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
print("logo de Claude Code:", "sí" if HAS_CC else "no — se usa la tarjeta de terminal")
