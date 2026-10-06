#!/usr/bin/env python3
"""LUXUR — los tres fits que más piden. 100 % motion graphics.

Del video original solo se usa el audio: el fondo es el beige de la marca, y todo lo que se ve
está construido. La única imagen de persona es el recorte de Anto al inicio.

Design system LUXUR (THEMES["luxur"] de reelkit, leído del tema vivo de Shopify):
  ground `#EDEBE6` · ink `#1C1C1C` · blush `#EECDCC` · sage `#B9B6A2` · cream `#ECE4D1`
  Poppins para todo, Montserrat SemiBold solo para el wordmark, versalitas con tracking 0.18em,
  botones y píldoras con radio 60, trazos finos.

Los datos de cada fit salen del catálogo vivo de Shopify (44 jeans activos), no están inventados:
  Extra Low Straight ·  3 referencias · 110 unidades · desde $199.000 · tiro bajo
  Relaxed            · 19 referencias · 584 unidades · desde $199.000 · tiro medio
  Wide Leg           ·  7 referencias ·  36 unidades · desde $189.000 · tiro alto

La guía de fit es un esquema técnico, no un dibujo de un jean: una escala de tiro con un marcador
que se desliza, y un perfil de pierna cuyo ancho se anima. Igual que la guía de la web.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("LUXUR — los tres fits que más piden", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="luxur")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens LUXUR
BEIGE, INK, BLUSH = "#EDEBE6", "#1C1C1C", "#EECDCC"
SAGE, CREAM, GREY = "#B9B6A2", "#ECE4D1", "#EFEFEF"
DENIM, DENIM_L = "#34435A", "#8C9BB0"

POP = "'Poppins', 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
MONT = "'Montserrat', 'Poppins', 'Liberation Sans', sans-serif"

M = 72
EASE = "expo.out"


def t(id_, s, x, y, size, fill=INK, anchor="start", weight=400, tr="0", fam=POP, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text id="{id_}"{c} x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};letter-spacing:{tr}">{esc(s)}</text>')


def caps(id_, s, x, y, size=26, fill=INK, anchor="start", cls=""):
    """Versalitas de la marca: mayúsculas, tracking 0.18em, peso 400."""
    return t(id_, s.upper(), x, y, size, fill, anchor, weight=400, tr="0.18em", cls=cls)


def pill(id_, s, x, y, w, h, bg=BLUSH, fg=INK, size=24, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<g id="{id_}"{c}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{bg}"/>'
            + t(f"{id_}t", s.upper(), x + w / 2, y + h / 2 + size * 0.36, size, fg, "middle", 400, "0.18em") + '</g>')


def numbadge(id_, n, x, y, size=150, fs=78):
    """El número dentro de una píldora blush con la cifra en ink: blush no es tinta de texto."""
    return (f'<g id="{id_}"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*0.3:.0f}" fill="{BLUSH}"/>'
            + t(f"{id_}t", n, x + size / 2, y + size / 2 + fs * 0.36, fs, INK, "middle", 600, "-0.02em") + '</g>')


def rule(id_, x1, y, x2, col=INK, op=0.25):
    return f'<path id="{id_}" d="M{x1} {y} L{x2} {y}" stroke="{col}" stroke-opacity="{op}" stroke-width="1.5" fill="none"/>'


# ---------------------------------------------------------------- guía de fit
# Escala de tiro: eje vertical con tres marcas y un marcador que se desliza al valor del fit.
# Perfil de pierna: dos líneas cuya separación es el ancho de bota.
RISE = {"bajo": 0, "medio": 1, "alto": 2}


def fit_guide(cid, x, y, rise, leg_top, leg_bot, k=1.0):
    """Guía de tiro: el eje marca dónde cae la pretina y la pierna cuelga desde ahí hasta
    un ruedo común, así los tres fits se comparan de un vistazo.
    rise: 'bajo'|'medio'|'alto'. leg_top/leg_bot: ancho en la pretina y en la bota."""
    SH, HEM = 160 * k, 360 * k               # alto de la escala y caída hasta el ruedo
    wy = y + (2 - RISE[rise]) * (SH / 2)     # altura de la pretina
    lx = x + 150 * k
    lt, lb = leg_top * k, leg_bot * k
    g = f'<g id="{cid}">'
    g += f'<path d="M{x} {y} L{x} {y + SH}" stroke="{INK}" stroke-opacity="0.3" stroke-width="1.5" fill="none"/>'
    for name, i in (("Alto", 0), ("Medio", 1), ("Bajo", 2)):
        my = y + i * (SH / 2)
        g += (f'<path d="M{x - 10} {my} L{x + 10} {my}" stroke="{INK}" stroke-opacity="0.3" stroke-width="1.5" fill="none"/>'
              + caps(f"{cid}-m{i}", name, x - 24, my + 6 * k, 19 * k, INK, "end"))
    # la pierna: lados que caen de la pretina al ruedo, abierta arriba, ruedo marcado
    g += (f'<g id="{cid}-lg">'
          f'<path d="M{lx - lt / 2} {wy} L{lx - lb / 2} {y + HEM}" stroke="{INK}" stroke-width="{2.5 * k}" fill="none" stroke-linecap="round"/>'
          f'<path d="M{lx + lt / 2} {wy} L{lx + lb / 2} {y + HEM}" stroke="{INK}" stroke-width="{2.5 * k}" fill="none" stroke-linecap="round"/>'
          f'<path d="M{lx - lb / 2} {y + HEM} L{lx + lb / 2} {y + HEM}" stroke="{INK}" stroke-width="{2.5 * k}" fill="none" stroke-linecap="round"/>'
          '</g>')
    # la pretina: barra blush a la altura del tiro, unida al eje por una línea
    g += (f'<g id="{cid}-mk">'
          f'<path d="M{x + 12} {wy} L{lx - lt / 2 - 10} {wy}" stroke="{INK}" stroke-opacity="0.45" stroke-width="1.5" fill="none" stroke-dasharray="5 6"/>'
          f'<rect x="{lx - lt / 2}" y="{wy - 9 * k}" width="{lt}" height="{18 * k}" rx="{9 * k}" fill="{BLUSH}"/>'
          f'<rect x="{lx - lt / 2}" y="{wy - 9 * k}" width="{lt}" height="{18 * k}" rx="{9 * k}" fill="none" stroke="{INK}" stroke-width="1.5"/>'
          '</g>')
    return g + '</g>'


# ================================================================= wordmark
R.clip("wm", 0.25, R.DUR, t("wm-t", "LUXUR", M, 196, 46, INK, "start", 600, "0.02em", MONT), hold=True)

R.card_frags = {1, 2, 14}

# ================================================================= A · HOLA, SOY ANTO
st, en = 0.0, E(2) + 0.25
R.clip("anto", st, en, f'''
  <image id="an-img" href="public/anto.png" x="586" y="448" width="460" height="1275"/>
  <rect id="an-bg" x="0" y="1390" width="1080" height="530" fill="{CREAM}"/>''')
R.hidden("#an-img, #an-bg", st)
R.fromTo("#an-bg", "autoAlpha:1, scaleY:0, transformOrigin:'50% 100%'", "autoAlpha:1, scaleY:1", st + 0.10, 0.5, EASE)
R.fromTo("#an-img", "autoAlpha:0, y:90", "autoAlpha:1, y:0", st + 0.18, 0.7, EASE)

R.card("hola", st, en, [
    ("a", "Hola,", 86, M, 470, "left", "left", 1.0, 0.25),
    ("b", "yo soy", 86, M, 576, "left", "left", 1.0, 0.42),
    ("c", "Anto.", 128, M, 682, "left", "scale", 1.0, 0.60)])
R.clip("rol", 1.60, en, f'''
  {pill("ro-p", "Encargada de los fits", M, 858, 560, 66, BLUSH, INK, 24)}
  {caps("ro-s", "Los fits que más piden", M, 968, 24, INK)}''')
R.hidden("#ro-p, #ro-s", 1.60)
R.pop("#ro-p", 1.60, 0.4)
R.fromTo("#ro-s", "autoAlpha:0, x:-18", "autoAlpha:1, x:0", 1.85, 0.4, EASE)

# ================================================================= B · LOS TRES
st, en = S(3) - 0.05, E(3) + 0.25
NUMS = [("01", "Extra low straight"), ("02", "Relaxed"), ("03", "Wide leg")]
tiles = ""
for k, (n, nm) in enumerate(NUMS):
    ty = 520 + k * 240
    tiles += (f'<g id="tr{k}" class="tri"><rect x="{M}" y="{ty}" width="{1080 - 2 * M}" height="200" rx="28" fill="{CREAM}"/>'
              + numbadge(f"tn{k}", n, M + 40, ty + 40, 120, 58)
              + caps(f"tl{k}", nm, M + 190, ty + 116, 30, INK) + '</g>')
R.clip("tres", st, en, tiles)
R.hidden("#tres .tri", st)
for k in range(3):
    R.fromTo(f"#tr{k}", "autoAlpha:0, x:70", "autoAlpha:1, x:0", st + 0.12 + k * 0.17, 0.5, EASE)

# ================================================================= C-E · LAS TRES FICHAS
FITS = [
    dict(cid="f1", st=S(4) - 0.05, en=E(6) + 0.20, num="01", name="Extra low straight fit",
         chips=["Rígido", "Bota recta", "Tiro extra low"], rise="bajo", lt=112, lb=118,
         badge="El más sexy", refs="3 referencias", price="Desde $199.000", photo=None),
    dict(cid="f2", st=S(7) - 0.05, en=E(9) + 0.20, num="02", name="Relaxed fit",
         chips=["Bota recta", "Tiro medio", "Para cualquier outfit"], rise="medio", lt=132, lb=172,
         badge="El más viral", refs="19 referencias", price="Desde $199.000", photo="public/fit-relaxed.png"),
    dict(cid="f3", st=S(10) - 0.05, en=E(13) + 0.20, num="03", name="Wide leg fit",
         chips=["Semirredonda ancha", "Tiro medio alto", "El OG"], rise="alto", lt=150, lb=300,
         badge="El OG", refs="7 referencias", price="Desde $189.000", photo=None),
]
for f in FITS:
    c, st, en = f["cid"], f["st"], f["en"]
    PH = f'<image id="{c}-ph" href="{f["photo"]}" x="648" y="690" width="372" height="700" preserveAspectRatio="xMidYMid meet"/>' if f["photo"] else ""
    chips = ""
    for k, ch in enumerate(f["chips"]):
        w = 56 + len(ch) * 18
        chips += pill(f"{c}-c{k}", ch, M, 1186 + k * 88, w, 68, BLUSH if k == 0 else CREAM, INK, 24, cls=f"{c}chip")
    R.clip(c, st, en, f'''
      {numbadge(f"{c}-n", f["num"], M, 352, 158, 80)}
      {caps(f"{c}-b", f["badge"], M + 186, 448, 26, INK)}
      {t(f"{c}-t", f["name"], M, 614, 62, INK, "start", 500, "-0.02em")}
      {rule(f"{c}-r", M, 672, 1080 - M)}
      {fit_guide(f"{c}-g", M + 96, 700, f["rise"], f["lt"], f["lb"], 1.2)}
      {PH}
      {chips}
      {caps(f"{c}-d1", f["refs"], M, 1502, 23, INK)}
      {caps(f"{c}-d2", f["price"], 1080 - M, 1502, 23, INK, "end")}''')
    R.hidden(f"#{c}-n, #{c}-b, #{c}-t, #{c}-r, #{c}-g, #{c} .{c}chip, #{c}-d1, #{c}-d2" + (f", #{c}-ph" if f["photo"] else ""), st)
    R.fromTo(f"#{c}-n", "autoAlpha:0, y:40", "autoAlpha:1, y:0", st + 0.06, 0.5, EASE)
    R.fromTo(f"#{c}-b", "autoAlpha:0, x:-20", "autoAlpha:1, x:0", st + 0.20, 0.4, EASE)
    R.fromTo(f"#{c}-t", "autoAlpha:0, y:24", "autoAlpha:1, y:0", st + 0.26, 0.5, EASE)
    R.show(f"#{c}-r", st + 0.42); R.draw(f"#{c}-r", 1080 - 2 * M, st + 0.42, 0.5, "power2.inOut")
    # la guía se arma: eje, marcas, marcador que baja a su tiro, y la pierna que se abre
    R.fromTo(f"#{c}-g", "autoAlpha:0", "autoAlpha:1", st + 0.55, 0.3)
    R.fromTo(f"#{c}-g-mk", "autoAlpha:0, y:-60", "autoAlpha:1, y:0", st + 0.80, 0.6, EASE)
    R.fromTo(f"#{c}-g-lg", "autoAlpha:0, scaleX:0.2, transformOrigin:'50% 50%'", "autoAlpha:1, scaleX:1", st + 0.95, 0.7, EASE)
    if f["photo"]:
        R.fromTo(f"#{c}-ph", "autoAlpha:0, x:60", "autoAlpha:1, x:0", st + 0.70, 0.6, EASE)
    R.raw(f'  tl.fromTo("#{c} .{c}chip", {{ autoAlpha: 0, x: -30 }}, {{ autoAlpha: 1, x: 0, duration: 0.42, stagger: 0.14, ease: "{EASE}" }}, {st + 1.15:.2f});')
    R.fromTo(f"#{c}-d1, #{c}-d2", "autoAlpha:0", "autoAlpha:1", st + 1.70, 0.35)

# ================================================================= F · CIERRE
st = S(14) - 0.10
RY = 560
recap = ""
for k, f in enumerate(FITS):
    rx = 72 + k * 318
    recap += (f'<g id="rc{k}" class="rc"><rect x="{rx}" y="{RY}" width="296" height="420" rx="28" fill="{CREAM}"/>'
              + numbadge(f"rn{k}", f["num"], rx + 32, RY + 32, 96, 48)
              + fit_guide(f"rg{k}", rx + 72, RY + 158, f["rise"], f["lt"], f["lb"], 0.52)
              + '</g>')
R.clip("cierre", st, R.DUR, f'''
  {recap}
  {t("cl-t", "¿Parte dos?", 540, 1180, 96, INK, "middle", 500, "-0.02em")}
  {pill("cl-p", "Cuéntame en comentarios", 240, 1246, 600, 72, BLUSH, INK, 24)}
  {t("cl-w", "LUXUR", 540, 1444, 52, INK, "middle", 600, "0.02em", MONT)}
  {caps("cl-u", "luxurjeans.com", 540, 1500, 22, INK)}''', hold=True)
R.hidden("#cierre .rc, #cl-t, #cl-p, #cl-w, #cl-u", st)
R.raw(f'  tl.fromTo("#cierre .rc", {{ autoAlpha: 0, y: 36 }}, {{ autoAlpha: 1, y: 0, duration: 0.5, stagger: 0.12, ease: "{EASE}" }}, {st + 0.08:.2f});')
R.fromTo("#cl-t", "autoAlpha:0, y:24", "autoAlpha:1, y:0", st + 0.55, 0.5, EASE)
R.pop("#cl-p", st + 0.80, 0.4)
R.fromTo("#cl-w, #cl-u", "autoAlpha:0", "autoAlpha:1", st + 1.00, 0.4)

R.rail()
R.fadeout(0.35)

# ================================================================= estilo propio del reel
R.extra_css = f'''
      #root {{ background: {BEIGE}; }}
      /* Subtítulos en ink sobre el beige, sin sombra. */
      .rail {{ top: 1596px; }}
      .rail .line {{ max-width: 940px; color: {INK}; text-shadow: none;
        font-weight: 400; font-size: 50px; line-height: 1.22; letter-spacing: -0.01em; }}
      .rail .w.hot.pill {{ background: {BLUSH}; color: {INK}; border-radius: 60px; }}
      /* Statements: ink sobre el beige, nunca blancos con sombra. */
      .card {{ height: 1100px; }}
      .piece.white {{ color: {INK}; text-shadow: none; }}
      .piece {{ font-weight: 500; }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path, .mg svg image {{ shape-rendering: geometricPrecision; }}
'''

R.write()
