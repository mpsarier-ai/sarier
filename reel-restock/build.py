#!/usr/bin/env python3
"""LUXUR — reel 9:16 · RESTOCK (Q4 Trimestre Dorado).

Design system Q4 Trimestre Dorado: el LUXUR de siempre (papel, cream, blush, tinta) con los
neutros cálidos del trimestre y el dorado #8C7B5E como único acento por pantalla. Poppins 300 a
tamaño grande para nombres y cifras, 600 en versalitas para cintillos. Regla de la marca:
ningún gráfico tapa la pantalla completa y ella nunca queda tapada.

El plano manda. Hay dos encuadres:
  · planos hablados (0–5,8 s y 19,9–21 s): plano medio, ella ocupa el centro y la izquierda de
    arriba abajo, y su cabeza entra en la franja alta. La única pared libre es la derecha
    (x ≥ 740), encima de su hombro.
  · fitting room (5,8–19,9 s): plano entero, ella centrada; la columna derecha x 664..1040
    entre y 300 y 900 queda limpia en los cuatro looks (el hombro más alto llega a y≈980).
Los subtítulos van abajo en blanco con halo (y 1420): el fondo va de 14 a 255 de luminancia y
ninguna tinta plana aguanta; terminan antes de la cintura de Instagram (1600).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("LUXUR — restock", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="luxur")

# ---------------------------------------------------------------- tokens Q4 Trimestre Dorado
PAPER, CREAM, BLUSH, INK = "#FBFAF7", "#EDEBE6", "#EECDCC", "#1C1C1C"
MUTE, LINE, SOFT, GOLD = "#5A5A5A", "#BDBAB3", "#E6E2DC", "#8C7B5E"
SANS = "'Poppins', 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
MONT = "'Montserrat', 'Poppins', 'Helvetica Neue', Helvetica, sans-serif"
BACK, EASE = "back.out(1.6)", "power2.out"


def t(id_, s, x, y, size, fam=SANS, fill=INK, anchor="start", weight=400, tr="0", op=1.0, extra=""):
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" opacity="{op}" {extra} '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def caps(id_, s, x, y, size=22, fill=INK, anchor="start", weight=600, op=1.0):
    return t(id_, s.upper(), x, y, size, SANS, fill, anchor, weight, "0.18em", op)


def pill(cid, s, x, y, size=22, h=44, pad=24, bg=BLUSH, fg=INK, weight=600):
    """Cintillo del sistema como píldora: versalitas 600 con 0,18em de tracking, tinta encima
    (blanco sobre blush no pasa AA). Ancho ≈ 0,92em por carácter + padding."""
    s = s.upper()
    w = len(s) * size * 0.92 + 2 * pad
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{bg}"/>'
            + t(f"{cid}t", s, x + w / 2, y + h / 2 + size * 0.36, size, SANS, fg, "middle", weight, "0.18em")
            + '</g>'), w


def chip(cid, s, x, y, size=22, h=40, pad=16):
    w = len(s) * size * 0.72 + 2 * pad
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="8" fill="{CREAM}"/>'
            + t(f"{cid}t", s, x + w / 2, y + h / 2 + size * 0.36, size, SANS, INK, "middle", 500, "0.04em")
            + '</g>'), w


# ================================================================= subtítulos
R.card_frags = set()
R.punch = {2: "vuelta.", 5: "stock.", 8: "vuelven.", 10: "tallas", 11: "octubre,",
           12: "Friday.", 13: "bio."}
R.rail()
# El logo solo aparece cuando lo dice: la palabra LUXUR del subtítulo se compone como el
# wordmark (Montserrat SemiBold, sin espaciado).
R.rail_html = [h.replace('class="w" id="r04w7">LUXUR', 'class="w brand" id="r04w7">LUXUR') for h in R.rail_html]


# ================================================================= 1 · HOOK (plano hablado)
# Pared derecha, encima de su hombro: x 740..1040. Su pelo llega a x≈700 a la altura del hombro.
HX, HY, HW, HH = 740, 300, 300, 250
hp, hpw = pill("hk-p", "restock", HX + 28, HY + 30, 20, 42, 20)
HOOK = (f'<g id="hk"><rect x="{HX}" y="{HY}" width="{HW}" height="{HH}" rx="28" fill="{PAPER}"/>'
        + t("hk-l", "LUXUR", HX + HW - 28, HY + 226, 26, MONT, INK, "end", 600, "0")
        + hp
        + t("hk-a", "de", HX + 28, HY + 140, 56, SANS, INK, "start", 300, "-0.02em")
        + t("hk-b", "vuelta", HX + 28, HY + 196, 56, SANS, INK, "start", 300, "-0.02em")
        + f'<rect id="hk-r" x="{HX + 28}" y="{HY + 216}" width="44" height="4" fill="{GOLD}"/>'
        + '</g>')
R.clip("hook", 0.15, 5.70, HOOK)
R.fromTo("#hk", "autoAlpha:0, x:34", "autoAlpha:1, x:0", 0.20, 0.5, BACK)
R.fromTo("#hk-p", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1", 0.42, 0.4, BACK)
R.fromTo("#hk-a", "autoAlpha:0, x:-14", "autoAlpha:1, x:0", 0.60, 0.4, EASE)
R.fromTo("#hk-b", "autoAlpha:0, x:-14", "autoAlpha:1, x:0", 0.74, 0.4, EASE)
R.fromTo("#hk-r", "attr:{width:0}", "attr:{width:44}", 0.95, 0.4, EASE)
R.hidden("#hk-l", 0.15)
R.show("#hk-l", 3.28)          # "...los favoritos de LUXUR"
R.fromTo("#hk-l", "autoAlpha:0, y:8", "autoAlpha:1, y:0", 3.28, 0.3, EASE)
R.fade("#hk-l", 5.10, 0.0, 0.25)
R.punch_cam(0.25, 1.03)


# ================================================================= 2 · LOS CUATRO LOOKS
# Columna derecha del fitting room. Ficha: píldora de número, foto de Shopify, nombre en 300,
# lavado y precio, tallas en chips, y el contador de cuatro barras (la activa en dorado).
CX, CY, CW, CH = 664, 300, 376, 630
PX, PY, PW, PH = CX + 48, CY + 84, 280, 350       # la foto, 4:5, termina en y+434

LOOKS = [
    # (inicio, fin, nombre, lavado, precio, tallas, foto)
    (5.80, 10.17, "LOW WIDE", "azul oscuro", "$199.000", ["XS", "S", "M", "L", "XL"], "low-wide-azul-oscuro"),
    (10.17, 13.77, "LOW WIDE", "dirty washed", "$199.000", ["XS", "S", "M", "L", "XL"], "low-wide-dirty"),
    (13.77, 16.90, "WIDE LEG", "green toned", "$189.000", ["XS", "S", "M", "L"], "wide-leg-green-toned"),
    (16.90, 19.87, "WIDE LEG", "green vintage", "$189.000", ["XS", "S", "M"], "wide-leg-green-vintage"),
]
CLIPS = ""
for k, (st, en, name, wash, price, sizes, photo) in enumerate(LOOKS, 1):
    p = f"lk{k}"
    np_, nw = pill(f"{p}-n", f"0{k}", CX + 28, CY + 26, 20, 40, 18)
    chips, cx_ = [], CX + 28
    for j, s in enumerate(sizes):
        c, w = chip(f"{p}-c{j}", s, cx_, CY + 540, 20, 36, 14)
        chips.append(c)
        cx_ += w + 8
    bars = []
    bw = (CW - 56 - 3 * 10) / 4
    for j in range(4):
        bx = CX + 28 + j * (bw + 10)
        bars.append(f'<rect x="{bx:.1f}" y="{CY + 600}" width="{bw:.1f}" height="4" rx="2" fill="{SOFT}"/>')
        if j == k - 1:
            bars.append(f'<rect id="{p}-g" x="{bx:.1f}" y="{CY + 600}" width="0" height="4" rx="2" fill="{GOLD}"/>')
    g = (f'<defs><clipPath id="{p}-clip"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="18"/></clipPath></defs>'
         f'<g id="{p}"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="28" fill="{PAPER}"/>'
         + np_
         + f'<g id="{p}-ph"><image href="public/{photo}.jpg" x="{PX}" y="{PY}" width="{PW}" height="{PH}" '
           f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{p}-clip)"/></g>'
         + t(f"{p}-t", name, CX + 28, CY + 486, 44, SANS, INK, "start", 300, "-0.02em")
         + t(f"{p}-s", f"{wash} · {price}", CX + 28, CY + 518, 22, SANS, MUTE, "start", 400)
         + "".join(chips) + "".join(bars) + '</g>')
    R.clip(p + "c", st, en, g)
    R.fromTo(f"#{p}", "autoAlpha:0, x:40", "autoAlpha:1, x:0", st + 0.04, 0.5, BACK)
    R.fromTo(f"#{p}-n", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1", st + 0.10, 0.4, BACK)
    R.fromTo(f"#{p}-ph", "autoAlpha:0, scale:0.96, transformOrigin:'50% 50%'", "autoAlpha:1, scale:1", st + 0.12, 0.4, EASE)
    R.fromTo(f"#{p}-t", "autoAlpha:0, x:-14", "autoAlpha:1, x:0", st + 0.24, 0.4, EASE)
    R.fromTo(f"#{p}-s", "autoAlpha:0, x:-14", "autoAlpha:1, x:0", st + 0.32, 0.4, EASE)
    for j in range(len(sizes)):
        R.fromTo(f"#{p}-c{j}", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1",
                 st + 0.40 + j * 0.07, 0.35, BACK)
    R.fromTo(f"#{p}-g", "attr:{width:0}", f"attr:{{width:{bw:.1f}}}", st + 0.55, 0.45, EASE)
    R.punch_cam(st + 0.02, 1.03)


# ================================================================= 3 · CIERRE sobre el plano
FX, FY = 890, 360
fpw = len("link en bio") * 24 * 0.92 + 2 * 26
fp, _ = pill("fn-p", "link en bio", FX - fpw, FY + 70, 24, 50, 26, PAPER, INK)
FIN = (f'<g id="fn">'
       + f'<rect id="fn-r" x="{FX - 44}" y="{FY + 44}" width="44" height="4" fill="{GOLD}"/>'
       + fp + '</g>')
R.clip("fin", 19.92, R.DUR, FIN, hold=True)
R.fromTo("#fn-r", "attr:{width:0}", "attr:{width:44}", 19.96, 0.3, EASE)
R.fromTo("#fn-p", "autoAlpha:0, scale:0.8, transformOrigin:'100% 50%'", "autoAlpha:1, scale:1", 20.05, 0.4, BACK)
R.slow_push(19.95, 1.0, 1.03)
R.fadeout(0.4)


# ================================================================= estilos
R.extra_css = f'''
      /* Subtítulos en blanco con halo: el fondo va de 14 a 255 y ninguna tinta plana aguanta.
         Terminan antes de y=1600, donde empieza la interfaz de Instagram. */
      .rail {{ top: 1420px; }}
      .rail .line {{ max-width: 880px; font-weight: 500; font-size: 50px; line-height: 1.20;
        text-shadow: 0 0 12px rgba(0,0,0,0.78), 0 2px 5px rgba(0,0,0,0.65), 0 8px 30px rgba(0,0,0,0.45); }}
      .rail .w.brand {{ font-family: {MONT}; font-weight: 600; letter-spacing: 0; }}
      .rail .w.hot.pill {{ padding: 0.04em 0.30em 0.10em; border-radius: 99px; }}
      .card {{ height: 1920px; }}
      /* El cierre va sobre el plano, sin lámina. */
      #fn {{ filter: drop-shadow(0 2px 10px rgba(0,0,0,0.45)); }}
      .mg svg text, .mg svg rect, .mg svg path {{ shape-rendering: geometricPrecision; }}
'''

R.write()
