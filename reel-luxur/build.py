#!/usr/bin/env python3
"""LUXUR — reel "el dúo perfecto" (RELAXED FIT + LOW WIDE FIT).
Sistema de diseño LUXUR leído del tema de Shopify: fondo beige #EDEBE6, tinta #1C1C1C, blush #EECDCC,
Poppins (300/400/500), píldoras r60, trazo fino. Wordmark en Montserrat SemiBold con espaciado mínimo.
Las fichas usan la foto real de cada fit (public/fit-relaxed.png, public/fit-low.png); mientras no estén,
se dibuja el encaje marcado. Stock y nombres de color vienen del catálogo real de luxurjeans.com."""
import sys, os; sys.path.insert(0, "..")
from reelkit import *

R = Reel("LUXUR — el dúo perfecto", theme="luxur", gin_top=0, gin_scale=1.0, gin_h=1920)
S, E, L = R.S, R.E, Reel.label
INK, BEIGE, BLUSH = "#1C1C1C", "#EDEBE6", "#EECDCC"
SAGE, CREAM, GREY, WHITE = "#B9B6A2", "#ECE4D1", "#EFEFEF", "#FFFFFF"
DENIM_D, DENIM_DIRTY, CARBON, ROSA = "#34435A", "#6E7F93", "#3A3A3C", "#E0BDB9"
THIN = 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"'
HALO = ('<defs><filter id="halo" x="-30%" y="-30%" width="160%" height="160%">'
        '<feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#FFFFFF" flood-opacity="0.95"/>'
        '<feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#FFFFFF" flood-opacity="0.65"/></filter>'
        '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#1C1C1C" flood-opacity="0.18"/></filter></defs>')
MONT = ";font-family:Montserrat;font-weight:600;letter-spacing:0.02em"

R.card_frags = {1, 2, 35, 36, 37}
R.punch = {3:"TikTok", 5:"GAP", 6:"perfecto", 8:"vendidos", 11:"perfecto", 12:"alto", 13:"bonito", 15:"relaxed",
           16:"segundo", 17:"vendido", 19:"Demasiado.", 21:"poquitas", 23:"otra", 24:"espectacular.", 25:"bajito",
           26:"anchito,", 27:"ombligo.", 28:"clóset", 30:"rosado,", 31:"time.", 32:"dirty,", 33:"grisáceo,", 34:"azul"}
R.rail()

# el sujeto está de pie y ocupa el centro: subtítulos abajo, fichas a los lados, datos en escenas beige
R.extra_css = """
      .card { height: 1920px; }
      .rail { top: 1420px; }
      .rail .line { max-width: 900px; font-weight: 500; }
      .piece.white { text-shadow: 0 2px 4px rgba(0,0,0,0.28), 0 10px 40px rgba(0,0,0,0.30); }
      .rail .line.ink .w.hot.pill { background: #1C1C1C; color: #EDEBE6; }
      .wl { font-size: 26px; font-weight: 500; }
      .wl2 { font-size: 32px; font-weight: 500; }
      #logo { position: absolute; left: 0; right: 0; top: 250px; text-align: center; pointer-events: none; }
      #logo span { display: inline-block; font-family: Montserrat, Poppins, sans-serif; font-weight: 600;
        font-size: 58px; letter-spacing: 0.02em; color: #1C1C1C;
        text-shadow: 0 0 14px rgba(255,255,255,0.95), 0 0 34px rgba(255,255,255,0.7); }
"""

def J(js, **kw):
    for k, v in kw.items(): js = js.replace("$" + k, f"{v:.2f}" if isinstance(v, float) else str(v))
    return js
def pill(id_, x, y, w, h, text, bg=BEIGE, fg=INK, size=26, rx=60):
    return (f'<g id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>'
            f'<text x="{x + w/2:.0f}" y="{y + h/2 + size*0.36:.0f}" text-anchor="middle" class="wl" fill="{fg}" style="font-size:{size}px">{esc(text)}</text></g>')
def caps(id_, text, x, y, color=WHITE, size=26, anchor="start", extra=""):
    return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="wl" fill="{color}" data-layout-allow-overlap style="font-size:{size}px{extra}">{esc(text)}</text>'

# ------------------------------------------------------------------ ficha de producto con la foto del fit
FIT_SRC = {"relaxed": "public/fit-relaxed.png", "low": "public/fit-low.png"}
def fitcard(cid, fit, x, y, w, h, title, sub="", pad=22):
    """Tarjeta beige (como la de la tienda) con la foto del fit. Sin foto todavía, deja el encaje marcado."""
    src = FIT_SRC[fit]
    iw = w - pad * 2
    ih = h - pad * 2 - (76 if title else 0)
    if os.path.exists(src):
        art = f'<image class="{cid}-img" href="{src}" x="{x + pad}" y="{y + pad}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid meet"/>'
    else:
        # sin foto todavía: ficha tipográfica de la tienda (nombre grande + specs), no un hueco vacío
        cx, cy = x + w / 2, y + pad + ih / 2
        spec = {"relaxed": ["TIRO ALTO", "PIERNA RECTA", "RELAJADO"], "low": ["TIRO BAJO", "PIERNA ANCHA", "OVERSIZE"]}[fit]
        lines = "".join(f'<text x="{cx:.0f}" y="{cy - 4 + k * 42:.0f}" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.62" style="font-size:24px">{t}</text>' for k, t in enumerate(spec))
        art = (f'<text x="{cx:.0f}" y="{cy - 86:.0f}" text-anchor="middle" class="wl" fill="{INK}" style="font-size:46px{MONT}">LUXUR</text>'
               f'<path d="M{x + pad + 30:.0f} {cy - 52:.0f} L{x + w - pad - 30:.0f} {cy - 52:.0f}" stroke="{INK}" stroke-opacity="0.3" {THIN}/>{lines}')
    lab = (f'<text x="{x + w/2:.0f}" y="{y + h - 42:.0f}" text-anchor="middle" class="wl" fill="{INK}" style="font-size:26px">{esc(title)}</text>'
           f'<text x="{x + w/2:.0f}" y="{y + h - 14:.0f}" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.55" style="font-size:20px">{esc(sub)}</text>') if title else ""
    return (f'<g class="{cid}" filter="url(#soft)"><rect class="{cid}-bg" x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{BEIGE}"/>'
            f'{art}{lab}</g>')

# ================================================================== 1 · HOOK
R.card("hook", 0.0, E(2) + 0.25, [
    ("a", "Dos cosas", 112, 72, 1000, "left", "left", 1.0),
    ("b", "antes de comprar", 60, 72, 1104, "left", "left", 0.86, S(2) + 0.05),
    ("c", "tu LUXUR.", 88, 72, 1162, "left", "scale", 1.0, S(2) + 0.5)])
R.clip("hookp", 0.35, E(2) + 0.25, pill("hp", 72, 908, 210, 62, "SÍ O SÍ", BLUSH, INK, 26))
R.hidden("#hp", 0.35); R.pop("#hp", 0.5, 0.35)

# ================================================================== 3 · EL DÚO PERFECTO — dos fichas
st, en = S(6), E(8) + 0.25
R.clip("duo", st, en, HALO
  + fitcard("d1", "relaxed", 40, 300, 300, 430, "RELAXED FIT", "TIRO ALTO")
  + fitcard("d2", "low", 740, 300, 300, 430, "LOW WIDE FIT", "TIRO BAJO")
  + f'''<path id="du-x" d="M498 515 L582 515 M540 473 L540 557" stroke="{BLUSH}" {THIN}/>
  {pill("du-p", 380, 790, 320, 64, "EL DÚO PERFECTO", BLUSH, INK, 26)}''')
R.hidden(".d1, .d2, #du-x, #du-p", st)
R.fromTo(".d1", "autoAlpha: 0, x: -60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.fromTo(".d2", "autoAlpha: 0, x: 60", "autoAlpha: 1, x: 0", S(6) + 0.75, 0.6, "expo.out")
R.draw("#du-x", 180, S(7) + 0.2, 0.3); R.pop("#du-p", S(8) + 0.3, 0.4)

# ================================================================== 4 · FIT 1 · RELAXED (tiro alto)
st, en = S(11), E(15) + 0.25
R.clip("f1", st, en, HALO
  + fitcard("f1c", "relaxed", 40, 300, 320, 470, "RELAXED FIT", "$199.000")
  + f'''<g filter="url(#halo)">
  <path id="f1-line" d="M390 392 L1000 392" stroke="{INK}" stroke-dasharray="8 10" {THIN}/>
  {caps("f1-lt", "TIRO ALTO", 1000, 368, INK, 24, "end")}
  {caps("f1-n", "RELAJADO", 1000, 540, INK, 40, "end", extra=";letter-spacing:0.12em")}
  <path id="f1-r" d="M660 576 L1000 576" stroke="{INK}" {THIN}/>
  {caps("f1-d", "HECHO PARA USARLO BONITO", 1000, 624, INK, 22, "end")}</g>
  {pill("f1-p", 700, 664, 300, 62, "PARA QUE LO ANOTEN", BEIGE, INK, 24)}''')
R.hidden(".f1c, #f1-line, #f1-lt, #f1-n, #f1-r, #f1-d, #f1-p", st)
R.fromTo(".f1c", "autoAlpha: 0, x: -60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.draw("#f1-line", 540, S(12) + 0.35, 0.5); R.pop("#f1-lt", S(12) + 0.6, 0.3)
R.pop("#f1-n", S(14) + 0.1, 0.4); R.draw("#f1-r", 360, S(14) + 0.3, 0.4); R.pop("#f1-d", S(14) + 0.5, 0.3)
R.pop("#f1-p", S(15) + 0.5, 0.35)

# ================================================================== 5 · FIT 2 · LOW WIDE (2º más vendido)
st, en = S(16), E(18) + 0.25
R.clip("f2", st, en, HALO
  + fitcard("f2c", "low", 720, 300, 320, 470, "LOW WIDE FIT", "$199.000")
  + f'''<g filter="url(#halo)">
  {caps("f2-n", "EL SEGUNDO", 60, 540, INK, 40, extra=";letter-spacing:0.12em")}
  <path id="f2-r" d="M60 576 L400 576" stroke="{INK}" {THIN}/>
  {caps("f2-d", "TIRO BAJO · ANCHO", 60, 624, INK, 22)}</g>
  {pill("f2-b", 60, 664, 340, 62, "2º MÁS VENDIDO", BLUSH, INK, 26)}''')
R.hidden(".f2c, #f2-n, #f2-r, #f2-d, #f2-b", st)
R.fromTo(".f2c", "autoAlpha: 0, x: 60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.pop("#f2-n", S(16) + 0.9, 0.4); R.draw("#f2-r", 360, S(16) + 1.1, 0.4); R.pop("#f2-d", S(16) + 1.3, 0.3)
R.pop("#f2-b", S(17) + 0.9, 0.4)

# ================================================================== 6 · ÚLTIMAS UNIDADES (panel lateral)
st, en = S(20), E(21) + 0.3
STOCK = [("AZUL OSCURO", 1, DENIM_D), ("AZUL DIRTY", 10, DENIM_DIRTY), ("NEGRO", 15, CARBON), ("ROSADO", 22, ROSA)]
PX, PY, PW = 48, 300, 520
rows = "".join(f'''
  <g class="sk-r" id="sk-r{k}">
    <circle cx="{PX + 66}" cy="{PY + 186 + k * 96}" r="24" fill="{col}"/>
    <text x="{PX + 116}" y="{PY + 197 + k * 96}" class="wl" fill="{INK}" style="font-size:26px;font-weight:400;letter-spacing:0.1em">{name}</text>
    <text x="{PX + PW - 44}" y="{PY + 200 + k * 96}" text-anchor="end" class="wl" fill="{INK}" style="font-size:40px;font-weight:500;letter-spacing:-0.02em">{n}</text>
    <path d="M{PX + 44} {PY + 228 + k * 96} L{PX + PW - 44} {PY + 228 + k * 96}" stroke="{INK}" stroke-opacity="0.16" {THIN}/>
  </g>''' for k, (name, n, col) in enumerate(STOCK))
R.clip("stock", st, en, HALO + f'''
  <g filter="url(#soft)"><rect id="sk-bg" x="{PX}" y="{PY}" width="{PW}" height="656" rx="34" fill="{BEIGE}"/></g>
  {caps("sk-t", "ÚLTIMAS UNIDADES", PX + 44, PY + 88, INK, 28)}
  <path id="sk-tr" d="M{PX + 44} {PY + 118} L{PX + PW - 44} {PY + 118}" stroke="{INK}" {THIN}/>
  {rows}
  {pill("sk-p", PX + 44, PY + 546, PW - 88, 64, "QUEDAN POQUITAS", BLUSH, INK, 26)}''')
R.hidden("#sk-bg, #sk-t, #sk-tr, .sk-r, #sk-p", st)
R.fromTo("#sk-bg", "autoAlpha: 0, x: -50", "autoAlpha: 1, x: 0", st + 0.05, 0.5, "expo.out")
R.pop("#sk-t", st + 0.3, 0.35); R.draw("#sk-tr", 440, st + 0.4, 0.45)
for k in range(4):
    R.fromTo(f"#sk-r{k}", "autoAlpha: 0, x: 30", "autoAlpha: 1, x: 0", st + 0.5 + k * 0.2, 0.45, "expo.out")
R.pop("#sk-p", S(21) + 0.6, 0.4)

# ================================================================== 7 · TIRO ALTO vs TIRO BAJO (las dos fotos)
st, en = S(25), E(27) + 0.3
R.clip("rise", st, en, HALO
  + fitcard("r1c", "relaxed", 40, 300, 300, 430, "TIRO ALTO", "RELAXED")
  + fitcard("r2c", "low", 740, 300, 300, 430, "TIRO BAJO", "LOW WIDE")
  + f'''<g filter="url(#halo)">
  <path id="rs-om" d="M150 790 L930 790" stroke="{INK}" stroke-opacity="0.7" stroke-dasharray="4 12" {THIN}/>
  {caps("rs-omt", "OMBLIGO", 540, 774, INK, 22, "middle")}</g>
  {pill("rs-p", 330, 830, 420, 64, "MÁS BAJITO Y ANCHITO", BLUSH, INK, 26)}''')
R.hidden(".r1c, .r2c, #rs-om, #rs-omt, #rs-p", st)
R.fromTo(".r1c", "autoAlpha: 0, x: -50", "autoAlpha: 1, x: 0", st + 0.1, 0.55, "expo.out")
R.fromTo(".r2c", "autoAlpha: 0, x: 50", "autoAlpha: 1, x: 0", st + 0.25, 0.55, "expo.out")
R.pop("#rs-p", S(26) + 1.1, 0.4)
R.draw("#rs-om", 800, S(27) + 0.2, 0.5); R.pop("#rs-omt", S(27) + 0.5, 0.3)

# ================================================================== 8 · LOS COLORES (tarjeta lateral + disco 3D)
st, en = S(29), E(34) + 0.3
COLORS = [("ROSADO", "FULLY BLUSH", ROSA), ("AZUL DIRTY", "DIRTY WASHED", DENIM_DIRTY),
          ("NEGRO", "GRISÁCEO", CARBON), ("AZUL", "AZUL OSCURO", DENIM_D)]
CX, CY, CW, CH = 596, 286, 440, 620          # tarjeta a la derecha
DCX, DCY = CX + CW / 2, CY + 250             # centro del disco 3D
# el fondo va en una escena transparente (queda debajo del lienzo 3D)
R.scene("scB", st, en, "transparent", f'''
  <rect id="cl-bg" x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="34" fill="{BEIGE}"/>
  <circle id="cl-ring" cx="{DCX:.0f}" cy="{DCY:.0f}" r="132" stroke="{INK}" stroke-opacity="0.2" stroke-width="2" fill="none"/>''')
labels = "".join(f'''
  <g class="cl-l" id="cl-l{k}">
    <text x="{DCX:.0f}" y="{CY + 452}" text-anchor="middle" class="wl" fill="{INK}" style="font-size:34px;font-weight:400;letter-spacing:0.14em">{nm}</text>
    <text x="{DCX:.0f}" y="{CY + 492}" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.55" style="font-size:22px">{sub}</text>
  </g>''' for k, (nm, sub, _) in enumerate(COLORS))
R.clip("clt", st, en, f'''
  {caps("cl-t", "LOS COLORES", DCX, CY + 74, INK, 28, "middle")}
  <path id="cl-tr" d="M{CX + 60} {CY + 104} L{CX + CW - 60} {CY + 104}" stroke="{INK}" {THIN}/>
  {labels}
  {pill("cl-p", CX + 40, CY + 524, CW - 80, 62, "MEJOR VENDIDO ALL TIME", BLUSH, INK, 22)}''')
R.hidden("#cl-bg, #cl-ring, #cl-t, #cl-tr, .cl-l, #cl-p", st)
R.fromTo("#cl-bg", "autoAlpha: 0, x: 50", "autoAlpha: 1, x: 0", st + 0.05, 0.5, "expo.out")
R.pop("#cl-t", st + 0.3, 0.35); R.draw("#cl-tr", 320, st + 0.4, 0.45); R.draw("#cl-ring", 840, st + 0.4, 0.8)
BEATS = [S(30) + 0.2, S(32) + 0.2, S(33) + 0.2, S(34) + 0.2]
for k, at in enumerate(BEATS):
    R.fromTo(f"#cl-l{k}", "autoAlpha: 0, y: 22", "autoAlpha: 1, y: 0", at, 0.45, "expo.out")
    if k + 1 < len(BEATS): R.to(f"#cl-l{k}", "autoAlpha: 0, y: -18", BEATS[k + 1] - 0.18, 0.25, "power2.in")
R.pop("#cl-p", S(31) + 0.3, 0.45); R.fade("#cl-p", S(32) - 0.45, 0.0, 0.25); R.hidden("#cl-p", S(32) - 0.15)

R.gl({})
R.gl_add(f"""
      KEY.intensity = 0.40; FILL.intensity = 0.18; scene.children.forEach((o) => {{ if (o.isHemisphereLight) o.intensity = 1.05; }});
      const shade = (hex, f) => {{ const c = new THREE.Color(hex); c.multiplyScalar(f); return c; }};
      const LUX = ["{COLORS[0][2]}", "{COLORS[1][2]}", "{COLORS[2][2]}", "{COLORS[3][2]}"].map((c) => [new THREE.MeshBasicMaterial({{ color: shade(c, 0.86) }}), new THREE.MeshBasicMaterial({{ color: new THREE.Color(c) }}), new THREE.MeshBasicMaterial({{ color: shade(c, 0.94) }})]);
      function disc(mat, r = 0.62, h = 0.12) {{
        const g = new THREE.Group();
        const d = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 96), mat); d.rotation.x = Math.PI / 2; g.add(d);
        return g;
      }}
""")
R.gl_beat(st + 0.25, en, J(r"""
    if (!g.built) { g.built = true; g.ds = LUX.map((m, k) => { const d = disc(m); d.position.set(X($dcx), Y($dcy), 0); d.visible = false; g.add(d); return d; }); }
    const B = [$b0, $b1, $b2, $b3].map((x) => x - $st);
    g.ds.forEach((d, k) => {
      const inU = easeOut(seg(t, B[k], B[k] + 0.55));
      const outU = k + 1 < B.length ? easeInOut(seg(t, B[k + 1] - 0.3, B[k + 1] + 0.1)) : 0;
      d.visible = inU > 0 && outU < 1;
      d.scale.setScalar(inU * (1 - 0.35 * outU));
      d.position.y = Y($dcy) + (1 - inU) * -0.6 + outU * 0.8;
      d.rotation.y = (1 - inU) * 1.4 + Math.sin((t - B[k]) * 0.55) * 0.30;
      d.rotation.x = 0.14 + Math.sin((t - B[k]) * 0.7) * 0.06;
    });
""", st=st, b0=BEATS[0], b1=BEATS[1], b2=BEATS[2], b3=BEATS[3], dcx=DCX, dcy=DCY))

# ================================================================== 9 · CIERRE · LUXURJEANS.COM (tarjeta)
st, en = S(35) - 0.1, R.DUR
BX, BY, BW, BH = 130, 620, 820, 420
R.clip("cta", st, en, HALO + f'''
  <g filter="url(#soft)"><rect id="cs-bg" x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="40" fill="{BEIGE}"/></g>
  {caps("cs-w", "LUXUR", 540, BY + 168, INK, 104, "middle", extra=MONT)}
  <path id="cs-r" d="M{BX + 150} {BY + 218} L{BX + BW - 150} {BY + 218}" stroke="{INK}" {THIN}/>
  {caps("cs-u", "LUXURJEANS.COM", 540, BY + 272, INK, 30, "middle")}
  {pill("cs-p", BX + 200, BY + 306, BW - 400, 70, "ENVÍOS A TODO EL PAÍS", BLUSH, INK, 24)}''')
R.hidden("#cs-bg, #cs-w, #cs-r, #cs-u, #cs-p", st)
R.fromTo("#cs-bg", "autoAlpha: 0, scale: 0.94, transformOrigin: '50% 50%'", "autoAlpha: 1, scale: 1", st + 0.05, 0.6, "expo.out")
R.fromTo("#cs-w", "autoAlpha: 0, scale: 0.94, transformOrigin: '50% 50%'", "autoAlpha: 1, scale: 1", st + 0.2, 0.6, "expo.out")
R.draw("#cs-r", 520, st + 0.5, 0.5)
R.pop("#cs-u", S(36) + 0.2, 0.4); R.pop("#cs-p", S(37) + 0.3, 0.45)
R.fadeout(0.4)

# wordmark de apertura (Montserrat SemiBold, espaciado mínimo)
R.cards_html.append(f'      <div id="logo" class="clip" data-start="0" data-duration="{E(2) + 0.25:.2f}" data-track-index="4"><span id="logo-w">LUXUR</span></div>')
R.raw('  tl.fromTo("#logo-w", { autoAlpha: 0, y: -14 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "expo.out" }, 0.15);')
R.raw(f'  tl.to("#logo-w", {{ autoAlpha: 0, duration: 0.3 }}, {E(2) - 0.1:.2f});')
R.raw(f'  tl.set("#logo-w", {{ autoAlpha: 0 }}, {E(2) + 0.25:.2f});')

R.write()
