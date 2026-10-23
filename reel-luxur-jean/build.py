#!/usr/bin/env python3
"""LUXUR — reel 9:16: las tres cosas que mira al comprar un jean básico.

Design system de LUXUR: Poppins, fondo beige #EDEBE6, ink #1C1C1C, blush #EECDCC, píldoras,
trazos finos. Regla propia de la marca: **ningún gráfico tapa la pantalla completa**.

El plano manda la arquitectura. Es un plano entero dentro de la tienda, ella ocupa el centro de
arriba abajo y el fondo va de 16 a 242 de luminancia según el momento, así que no hay ninguna
banda donde la tinta o el blanco se lean solos. La solución es la de la propia marca: **todo lo
que va encima del plano se apoya en una superficie beige**, que es como LUXUR pone texto sobre
cualquier cosa en la tienda y en la web. La única franja siempre libre es y=140..400 (el arco del
techo), así que ahí viven las tarjetas de capítulo; los subtítulos van abajo en blanco.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import Reel, esc

R = Reel("LUXUR — tres cosas al comprar un jean básico", captions="captions.json",
         gin_top=0, gin_scale=1.0, gin_h=1920, theme="luxur")
S, E = R.S, R.E

# ---------------------------------------------------------------- tokens de LUXUR
BEIGE, INK, BLUSH, WHITE = "#EDEBE6", "#1C1C1C", "#EECDCC", "#FFFFFF"
HAIR = "rgba(28,28,28,0.22)"
SOFT = "rgba(28,28,28,0.62)"
# Lavados de denim, no colores de marca: el oscuro está muestreado del jean que ella lleva
# puesto (#2E374F) y los otros dos salen del mismo tono, aclarado.
DEN_CLARO, DEN_MEDIO, DEN_OSCURO = "#9DB3CC", "#5B7392", "#2E374F"

SANS = "'Poppins', 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif"
MONT = "'Montserrat', 'Poppins', 'Helvetica Neue', Helvetica, sans-serif"

# La única franja del encuadre que nunca la tapa.
CX, CY, CW, CH = 96, 150, 888, 240
IX = CX + 40                 # margen interior
IW = CW - 80
BACK = "back.out(1.6)"
EASE = "power2.out"


def t(id_, s, x, y, size, fam=SANS, fill=INK, anchor="start", weight=400, tr="0", op=1.0):
    return (f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" opacity="{op}" '
            f'style="font-family:{fam};font-size:{size}px;font-weight:{weight};'
            f'letter-spacing:{tr}">{esc(s)}</text>')


def caps(id_, s, x, y, size=24, fill=INK, anchor="start", weight=500, op=1.0):
    return t(id_, s.upper(), x, y, size, SANS, fill, anchor, weight, "0.18em", op)


def surface(cid, x=CX, y=CY, w=CW, h=CH, rx=32):
    """La superficie beige de LUXUR: es lo único que se lee sobre este plano."""
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{BEIGE}"/>'
            + t(f"{cid}w", "LUXUR", x + w - 40, y + 46, 19, MONT, INK, "end", 600, "0.26em", 0.5))


def pill(cid, s, x, y, size=22, h=46, pad=26, bg=INK, fg=BEIGE, caps_=True, stroke=None):
    s = s.upper() if caps_ else s
    w = len(s) * size * (0.92 if caps_ else 0.60) + 2 * pad
    sk = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{bg}"{sk}/>'
            + t(f"{cid}t", s, x + w / 2, y + h / 2 + size * 0.36, size, SANS, fg, "middle", 500,
                "0.18em" if caps_ else "0")), w


def chapter(cid, st, en, num, title, extra="", hold=False):
    """Tarjeta de capítulo: superficie beige + píldora del número + titular."""
    np_, nw = pill(f"{cid}n", num, IX, CY + 70, 24, 50, 22)
    g = (surface(cid + "g") + np_
         + t(f"{cid}h", title, IX + nw + 22, CY + 112, 54, SANS, INK, "start", 600, "0.02em")
         + f'<path id="{cid}r" d="M{IX} {CY + 150} L{CX + CW - 40} {CY + 150}" stroke="{HAIR}" '
           f'stroke-width="2" fill="none"/>' + extra + '</g>')  # cierra el <g> de surface()
    R.clip(cid, st, en, g, hold=hold)
    R.fromTo(f"#{cid}g", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", st + 0.06, 0.5, BACK)
    R.fromTo(f"#{cid}n", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'",
             "autoAlpha:1, scale:1", st + 0.22, 0.4, BACK)
    R.fromTo(f"#{cid}h", "autoAlpha:0, x:-18", "autoAlpha:1, x:0", st + 0.32, 0.4, EASE)
    R.draw(f"#{cid}r", IW, st + 0.46, 0.5)
    return nw


def swatches(prefix, y, marked=None):
    """Los tres lavados: claro, medio, oscuro."""
    out = []
    for k, (col, lab) in enumerate([(DEN_CLARO, "claro"), (DEN_MEDIO, "medio"), (DEN_OSCURO, "oscuro")]):
        x = IX + k * 279
        mk = f' stroke="{INK}" stroke-width="3"' if marked == k else ""
        out.append(f'<g id="{prefix}{k}"><rect x="{x}" y="{y}" width="250" height="44" rx="10" '
                   f'fill="{col}"{mk}/>'
                   + caps(f"{prefix}l{k}", lab, x + 125, y + 70, 20, INK, "middle", 500) + '</g>')
    return "".join(out)


# ================================================================= subtítulos
# Blanco con la sombra del kit: el fondo va de 16 a 242 y ninguna tinta plana aguanta las dos.
R.card_frags = {1, 2, 3, 6, 8, 16, 18}
R.punch = {4: "fits", 5: "cuerpo.", 7: "oscuro.", 9: "día,", 10: "todo,", 11: "cómodo,",
           12: "calidad", 13: "años.", 14: "perfecto", 15: "necesidades.", 17: "cuerpo.",
           19: "claro", 20: "buscando.", 21: "jean."}
R.rail()


# ================================================================= 1 · HOOK
HOOK = (surface("hk")
        + t("hk-n", "3", IX + 10, CY + 158, 150, SANS, INK, "start", 600, "-0.04em")
        + caps("hk-a", "cosas que miro", IX + 132, CY + 108, 30, INK, "start", 500)
        + caps("hk-b", "al comprar un jean básico", IX + 132, CY + 156, 30, INK, "start", 500)
        + f'<path id="hk-r" d="M{IX + 132} {CY + 186} L{CX + CW - 40} {CY + 186}" stroke="{HAIR}" '
          f'stroke-width="2" fill="none"/>' + '</g>')
R.clip("hook", 0.10, 3.66, HOOK)
R.fromTo("#hk", "autoAlpha:0, y:-28", "autoAlpha:1, y:0", 0.16, 0.55, BACK)
R.fromTo("#hk-n", "autoAlpha:0, scale:0.6, transformOrigin:'0% 100%'", "autoAlpha:1, scale:1", 0.40, 0.5, BACK)
R.fromTo("#hk-a", "autoAlpha:0, x:-16", "autoAlpha:1, x:0", 0.70, 0.38, EASE)
R.fromTo("#hk-b", "autoAlpha:0, x:-16", "autoAlpha:1, x:0", 0.88, 0.38, EASE)
R.draw("#hk-r", IW - 132, 1.10, 0.5)
R.punch_cam(0.30)


# ================================================================= 2 · 01 EL FIT
FITS = ["extra low straight", "relaxed", "wide leg"]
fit_g = []
fx = IX
mark_x = 0
for k, f in enumerate(FITS):
    p, w = pill(f"ft{k}", f, fx, CY + 172, 19, 44, 20, BEIGE, INK, True, HAIR)
    fit_g.append(p)
    if k == 1:
        mark_x = fx          # la versión marcada se dibuja encima, en el mismo sitio
    fx += w + 14
# El resaltado es un cruce entre dos píldoras dibujadas en el mismo punto: animar un fill o una
# escala sobre un <g> de SVG recalcula su origen y desplaza la píldora.
mk, _ = pill("ftm", FITS[1], mark_x, CY + 172, 19, 44, 20, INK, BEIGE)
# Las dos comparten sitio a propósito, así que el chequeo de solape no aplica aquí.
fit_g = [g.replace('id="ft1t"', 'id="ft1t" data-layout-allow-overlap') for g in fit_g]
fit_g.append(mk.replace('id="ftmt"', 'id="ftmt" data-layout-allow-overlap'))
chapter("c1", 3.70, 10.80, "01", "EL FIT", "".join(fit_g))
R.hidden("#ft0, #ft1, #ft2", 3.70)
for k, at in enumerate([5.45, 5.75, 6.05]):
    R.show(f"#ft{k}", at)
    R.fromTo(f"#ft{k}", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'",
             "autoAlpha:1, scale:1", at, 0.4, BACK)
# "el que mejor se adecue a tu cuerpo": uno se marca
# La píldora marcada se dibuja encima de la beige, con la misma geometría: no hace falta
# esconder la de debajo, y así no hay dos tweens peleando por el mismo elemento.
R.hidden("#ftm", 3.70)
R.show("#ftm", 8.15)
R.fromTo("#ftm", "autoAlpha:0", "autoAlpha:1", 8.15, 0.3, EASE)
R.punch_cam(8.17, 1.03)


# ================================================================= 3 · 02 EL COLOR
chapter("c2", 11.06, 15.18, "02", "EL COLOR", swatches("sw", CY + 156))
R.hidden("#sw0, #sw1, #sw2", 11.06)
for k, at in enumerate([12.40, 12.95, 13.50]):
    R.show(f"#sw{k}", at)
    R.fromTo(f"#sw{k}", "autoAlpha:0, y:16, scale:0.9, transformOrigin:'50% 50%'",
             "autoAlpha:1, y:0, scale:1", at, 0.42, BACK)


# ================================================================= 4 · 03 LA CALIDAD
USO = ["para tu día a día", "para salir", "para todo"]
uso_g = []
ux = IX
for k, u in enumerate(USO):
    p, w = pill(f"us{k}", u, ux, CY + 170, 19, 44, 20, BEIGE, INK, True, HAIR)
    uso_g.append(p)
    ux += w + 14
req_g = []
rx_ = IX
for k, q in enumerate(["súper cómodo", "que te dure años"]):
    p, w = pill(f"rq{k}", q, rx_, CY + 170, 22, 48, 24, BLUSH, INK)
    req_g.append(p)
    rx_ += w + 16
chapter("c3", 15.58, 30.66, "03", "LA CALIDAD", "".join(uso_g) + "".join(req_g))
R.hidden("#us0, #us1, #us2, #rq0, #rq1", 15.58)
for k, at in enumerate([19.00, 21.30, 22.60]):
    R.show(f"#us{k}", at)
    R.fromTo(f"#us{k}", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'",
             "autoAlpha:1, scale:1", at, 0.4, BACK)
R.fade("#us0, #us1, #us2", 23.95, 0.0, 0.3)
for k, at in enumerate([24.20, 26.70]):
    R.show(f"#rq{k}", at)
    R.fromTo(f"#rq{k}", "autoAlpha:0, scale:0.7, y:12, transformOrigin:'0% 50%'",
             "autoAlpha:1, scale:1, y:0", at, 0.45, BACK)
R.punch_cam(24.22, 1.03)


# ================================================================= 5 · EL JEAN
pm, pmw = pill("pj-c", "color medio", IX + 348, CY + 78, 22, 48, 24, BLUSH, INK)
PROD = (surface("pj")
        + t("pj-t", "LOW WIDE", IX, CY + 116, 58, SANS, INK, "start", 600, "0.04em")
        + pm
        + f'<path id="pj-r" d="M{IX} {CY + 150} L{CX + CW - 40} {CY + 150}" stroke="{HAIR}" '
          f'stroke-width="2" fill="none"/>'
        + swatches("pw", CY + 156, marked=1) + '</g>')
R.clip("prod", 34.64, 45.90, PROD)
R.hidden("#pj-c, #pw0, #pw1, #pw2", 34.64)
R.fromTo("#pj", "autoAlpha:0, y:-26", "autoAlpha:1, y:0", 34.70, 0.5, BACK)
R.fromTo("#pj-t", "autoAlpha:0, x:-20", "autoAlpha:1, x:0", 34.92, 0.45, BACK)
R.draw("#pj-r", IW, 35.30, 0.5)
R.show("#pj-c", 39.95)
R.fromTo("#pj-c", "autoAlpha:0, scale:0.7, transformOrigin:'0% 50%'", "autoAlpha:1, scale:1", 39.95, 0.45, BACK)
for k, at in enumerate([40.20, 40.45, 40.70]):
    R.show(f"#pw{k}", at)
    R.fromTo(f"#pw{k}", "autoAlpha:0, y:14, scale:0.9, transformOrigin:'50% 50%'",
             "autoAlpha:1, y:0, scale:1", at, 0.4, BACK)
R.punch_cam(34.72, 1.035)


# ================================================================= 6 · CIERRE sobre el plano
CTA = (f'<g id="ct">'
       + t("ct-w", "LUXUR", 540, CY + 120, 72, MONT, BEIGE, "middle", 600, "0.22em")
       + f'<path id="ct-r" d="M330 {CY + 158} L750 {CY + 158}" stroke="{BLUSH}" stroke-width="3" fill="none"/>'
       + caps("ct-s", "cuéntame qué más consideras", 540, CY + 212, 24, BEIGE, "middle", 500) + '</g>')
R.clip("fin", 46.20, R.DUR, CTA, hold=True)
R.hidden("#ct-r, #ct-s", 46.20)
R.fromTo("#ct-w", "autoAlpha:0, y:18, scale:0.94", "autoAlpha:1, y:0, scale:1", 46.30, 0.6, BACK)
R.show("#ct-r", 46.70)
R.draw("#ct-r", 420, 46.70, 0.55)
R.show("#ct-s", 47.00)
R.fromTo("#ct-s", "autoAlpha:0, y:12", "autoAlpha:1, y:0", 47.00, 0.45, EASE)
R.slow_push(46.25, 2.3, 1.04)
R.fadeout(0.45)


# ================================================================= estilos
R.extra_css = f'''
      /* Subtítulos en blanco con la sombra del kit: el fondo de este plano va de 16 a 242
         y ninguna tinta plana aguanta los dos extremos. */
      .rail {{ top: 1440px; }}
      .rail .line {{ max-width: 900px; font-weight: 500; font-size: 52px; line-height: 1.20; }}
      .rail .w.hot.pill {{ padding: 0.04em 0.30em 0.10em; border-radius: 99px; }}
      .card {{ height: 1920px; }}
      .piece.white {{ text-shadow: 0 2px 4px rgba(0,0,0,0.28), 0 10px 40px rgba(0,0,0,0.30); }}
      .rail .line {{ text-shadow: 0 0 10px rgba(0,0,0,0.62), 0 2px 4px rgba(0,0,0,0.55),
        0 8px 30px rgba(0,0,0,0.40); }}
      /* El cierre va sobre el plano, sin lámina: el wordmark necesita separarse del fondo. */
      #ct-w, #ct-s {{ paint-order: stroke; }}
      #ct {{ filter: drop-shadow(0 2px 10px rgba(0,0,0,0.45)); }}
      .scene, .scin {{ opacity: 1; }}
      .mg svg text, .mg svg rect, .mg svg path {{ shape-rendering: geometricPrecision; }}
'''

R.write()
