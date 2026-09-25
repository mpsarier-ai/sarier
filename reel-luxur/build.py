#!/usr/bin/env python3
"""LUXUR — reel "el dúo perfecto" (RELAXED FIT + LOW WIDE FIT).
Sistema de diseño LUXUR leído del tema de Shopify: fondo beige #EDEBE6, tinta #1C1C1C, blush #EECDCC,
Poppins (300/400/500), píldoras r60, trazo fino. Nada del sistema de Sarier.
Stock y nombres de color vienen del catálogo real de luxurjeans.com."""
import sys, os; sys.path.insert(0, "..")
from reelkit import *

R = Reel("LUXUR — el dúo perfecto", theme="luxur", gin_top=0, gin_scale=1.0, gin_h=1920)
S, E, L = R.S, R.E, Reel.label
SW, SW8 = R.SW, R.SW8
INK, BEIGE, BLUSH = "#1C1C1C", "#EDEBE6", "#EECDCC"
SAGE, CREAM, GREY, WHITE = "#B9B6A2", "#ECE4D1", "#EFEFEF", "#FFFFFF"
DENIM_D, DENIM_DIRTY, CARBON = "#34435A", "#6E7F93", "#3A3A3C"
THIN = 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"'
HALO = ('<defs><filter id="halo" x="-30%" y="-30%" width="160%" height="160%">'
        '<feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#FFFFFF" flood-opacity="0.95"/>'
        '<feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#FFFFFF" flood-opacity="0.65"/></filter></defs>')

R.card_frags = {1, 2, 35, 36, 37}
R.ink_frags = {20, 21, 29, 30, 31, 32, 33, 34}
R.punch = {3:"TikTok", 5:"GAP", 6:"perfecto", 8:"vendidos", 11:"perfecto", 12:"alto", 13:"bonito", 15:"relaxed",
           16:"segundo", 17:"vendido", 19:"Demasiado.", 21:"poquitas", 23:"otra", 24:"espectacular.", 25:"bajito",
           26:"anchito,", 27:"ombligo.", 28:"clóset", 30:"rosado,", 31:"time.", 32:"dirty,", 33:"grisáceo,", 34:"azul"}
R.rail()

# el sujeto está de pie y ocupa el centro: subtítulos abajo, tarjetas a los lados, datos en escenas beige
R.extra_css = """
      .card { height: 1920px; }
      .rail { top: 1420px; }
      .rail .line { max-width: 900px; font-weight: 500; }
      .piece.white { text-shadow: 0 2px 4px rgba(0,0,0,0.28), 0 10px 40px rgba(0,0,0,0.30); }
      .rail .line.ink .w.hot.pill { background: #1C1C1C; color: #EDEBE6; }
      .wl { font-size: 26px; font-weight: 500; }
      .wl2 { font-size: 32px; font-weight: 500; }
      #logo { position: absolute; left: 0; right: 0; top: 250px; text-align: center; pointer-events: none; }
      #logo span { display: inline-block; font-weight: 500; font-size: 54px; letter-spacing: 0.42em;
        color: #1C1C1C; text-shadow: 0 0 14px rgba(255,255,255,0.95), 0 0 34px rgba(255,255,255,0.7); padding-left: 0.42em; }
"""

def J(js, **kw):
    for k, v in kw.items(): js = js.replace("$" + k, f"{v:.2f}" if isinstance(v, float) else str(v))
    return js
def pill(id_, x, y, w, h, text, bg=BEIGE, fg=INK, size=26, rx=60):
    return (f'<g id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>'
            f'<text x="{x + w/2:.0f}" y="{y + h/2 + size*0.36:.0f}" text-anchor="middle" class="wl" fill="{fg}" style="font-size:{size}px">{esc(text)}</text></g>')
def caps(id_, text, x, y, color=WHITE, size=26, anchor="start", extra=""):
    return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="wl" fill="{color}" style="font-size:{size}px{extra}">{esc(text)}</text>'

# ------------------------------------------------------------------ silueta de jean (línea fina, 260x420)
def jean(prefix, x, y, s=1.0, rise="high", color=INK, wide=1.0):
    """rise: high = cintura alta y pierna recta; low = tiro bajo y pierna ancha."""
    waist_y, hip = (0, 150) if rise == "high" else (44, 190)
    ow, bot = 124 * wide, 640
    d = (f'M{-94:.0f} {waist_y} L{94:.0f} {waist_y} L{ow:.0f} {bot} L{26:.0f} {bot} L{6:.0f} {hip + 210} '
         f'L{-6:.0f} {hip + 210} L{-26:.0f} {bot} L{-ow:.0f} {bot} Z')
    return (f'<g class="{prefix}" transform="translate({x} {y}) scale({s})">'
            f'<path class="{prefix}-o" d="{d}" stroke="{color}" {THIN}/>'
            f'<path class="{prefix}-w" d="M{-94:.0f} {waist_y + 30} L{94:.0f} {waist_y + 30}" stroke="{color}" {THIN}/>'
            f'<path class="{prefix}-p" d="M{-72:.0f} {waist_y + 48} q22 30 0 54 M{72:.0f} {waist_y + 48} q-22 30 0 54" stroke="{color}" {THIN}/>'
            f'<path class="{prefix}-z" d="M0 {waist_y + 30} L0 {hip}" stroke="{color}" {THIN}/></g>')

# ================================================================== 1 · HOOK
R.card("hook", 0.0, E(2) + 0.25, [
    ("a", "Dos cosas", 118, 72, 1020, "left", "left", 1.0),
    ("b", "antes de comprar", 62, 72, 1128, "left", "left", 0.86, S(2) + 0.05),
    ("c", "tu LUXUR.", 92, 72, 1188, "left", "scale", 1.0, S(2) + 0.5)])
R.clip("hookp", 0.35, E(2) + 0.25, pill("hp", 72, 920, 210, 62, "SÍ O SÍ", BLUSH, INK, 26))
R.hidden("#hp", 0.35); R.pop("#hp", 0.5, 0.35)

# ================================================================== 2 · TIKTOK · BIEBER × GAP
st, en = S(3), E(5) + 0.25
R.clip("tk", st, en, f'''
  <rect id="tk-c" x="580" y="300" width="440" height="250" rx="34" fill="{BEIGE}"/>
  {caps("tk-a", "EN TIKTOK", 620, 372, INK, 26)}
  <path id="tk-r" d="M620 400 L980 400" stroke="{INK}" {THIN}/>
  {caps("tk-b", "TODO EL MUNDO", 620, 452, INK, 34, extra=";font-weight:400")}
  {caps("tk-c", "HABLA DEL BIEBER", 620, 500, INK, 24)}''')
R.hidden("#tk-c, #tk-a, #tk-b, #tk-r", st)
R.fromTo("#tk-c", "autoAlpha: 0, scaleX: 0.6, transformOrigin: '100% 50%'", "autoAlpha: 1, scaleX: 1", st + 0.05, 0.45, "expo.out")
R.pop("#tk-a", st + 0.3, 0.3); R.draw("#tk-r", 360, st + 0.45, 0.4)
R.pop("#tk-b", S(4) + 0.2, 0.35); R.pop("#tk-c", S(5) + 0.1, 0.35)

# ================================================================== 3 · EL DÚO PERFECTO — dos siluetas
st, en = S(6), E(8) + 0.25
R.clip("duo", st, en, HALO + f'''<g filter="url(#halo)">
  {jean("dj1", 210, 560, 0.52, "high")}
  {jean("dj2", 870, 560, 0.52, "low", wide=1.2)}
  {caps("du-1", "RELAXED FIT", 210, 940, INK, 26, "middle")}
  {caps("du-2", "LOW WIDE FIT", 870, 940, INK, 26, "middle")}
  <path id="du-x" d="M498 760 L582 760 M540 718 L540 802" stroke="{BLUSH}" {THIN}/>
  </g>{pill("du-p", 380, 1230, 320, 64, "EL DÚO PERFECTO", BLUSH, INK, 26)}''')
R.hidden(".dj1, .dj2, #du-1, #du-2, #du-x, #du-p", st)
R.show(".dj1", st + 0.1); R.draw(".dj1 path", 1600, st + 0.1, 0.9, stagger=0.08); R.pop("#du-1", st + 0.7, 0.3)
R.show(".dj2", S(6) + 0.8); R.draw(".dj2 path", 1600, S(6) + 0.8, 0.9, stagger=0.08); R.pop("#du-2", S(6) + 1.4, 0.3)
R.draw("#du-x", 180, S(7) + 0.2, 0.3); R.pop("#du-p", S(8) + 0.3, 0.4)

# ================================================================== 4 · FIT 1 · RELAXED (tiro alto)
st, en = S(11), E(15) + 0.25
R.clip("f1", st, en, HALO + f'''<g filter="url(#halo)">
  {jean("f1j", 270, 470, 0.72, "high")}
  <path id="f1-line" d="M96 470 L520 470" stroke="{INK}" stroke-dasharray="8 10" {THIN}/>
  {caps("f1-lt", "TIRO ALTO", 96, 446, INK, 24)}
  {caps("f1-n", "RELAXED FIT", 620, 700, INK, 44, extra=";letter-spacing:0.12em")}
  <path id="f1-r" d="M620 736 L980 736" stroke="{INK}" {THIN}/>
  {caps("f1-d", "RELAJADO · PARA USARLO BONITO", 620, 790, INK, 22)}
  </g>{pill("f1-p", 620, 840, 250, 64, "$199.000", BEIGE, INK, 30)}''')
R.hidden(".f1j, #f1-line, #f1-lt, #f1-n, #f1-r, #f1-d, #f1-p", st)
R.show(".f1j", st + 0.1); R.draw(".f1j path", 2000, st + 0.1, 1.0, stagger=0.1)
R.draw("#f1-line", 470, S(12) + 0.35, 0.45); R.pop("#f1-lt", S(12) + 0.6, 0.3)
R.pop("#f1-d", S(13) + 0.4, 0.35)
R.pop("#f1-n", S(15) + 0.1, 0.4); R.draw("#f1-r", 360, S(15) + 0.3, 0.4); R.pop("#f1-p", S(15) + 0.6, 0.35)

# ================================================================== 5 · FIT 2 · LOW WIDE (2º más vendido)
st, en = S(16), E(18) + 0.25
R.clip("f2", st, en, HALO + f'''<g filter="url(#halo)">
  {jean("f2j", 820, 470, 0.72, "low", wide=1.2)}
  {caps("f2-n", "LOW WIDE FIT", 460, 700, INK, 44, "end", extra=";letter-spacing:0.12em")}
  <path id="f2-r" d="M100 736 L460 736" stroke="{INK}" {THIN}/>
  {caps("f2-d", "TIRO BAJO · ANCHO", 460, 790, INK, 24, "end")}
  </g>{pill("f2-p", 210, 840, 250, 64, "$199.000", BEIGE, INK, 30)}
  {pill("f2-b", 100, 936, 360, 64, "2º MÁS VENDIDO", BLUSH, INK, 26)}''')
R.hidden(".f2j, #f2-n, #f2-r, #f2-d, #f2-p, #f2-b", st)
R.show(".f2j", st + 0.1); R.draw(".f2j path", 2000, st + 0.1, 1.0, stagger=0.1)
R.pop("#f2-n", S(16) + 0.9, 0.4); R.draw("#f2-r", 360, S(16) + 1.1, 0.4); R.pop("#f2-d", S(16) + 1.3, 0.3)
R.pop("#f2-p", S(17) + 0.3, 0.35); R.pop("#f2-b", S(17) + 0.9, 0.4)

# ================================================================== 6 · ESCENA · ÚLTIMAS UNIDADES (stock real)
st, en = S(20), E(21) + 0.3
STOCK = [("AZUL OSCURO", 1, DENIM_D), ("AZUL DIRTY", 10, DENIM_DIRTY), ("NEGRO", 15, CARBON), ("ROSADO", 22, "#E0BDB9")]
rows = "".join(f'''
  <g class="sk-r" id="sk-r{k}">
    <circle cx="150" cy="{700 + k * 170}" r="34" fill="{col}"/>
    <text x="230" y="{712 + k * 170}" class="wl" fill="{INK}" style="font-size:38px;font-weight:400;letter-spacing:0.1em">{name}</text>
    <text x="930" y="{716 + k * 170}" text-anchor="end" class="wl" fill="{INK}" style="font-size:54px;font-weight:500;letter-spacing:-0.02em">{n}</text>
    <path d="M150 {760 + k * 170} L930 {760 + k * 170}" stroke="{INK}" stroke-opacity="0.18" {THIN}/>
  </g>''' for k, (name, n, col) in enumerate(STOCK))
R.scene("scA", st, en, BEIGE, f'''
  {caps("sk-t", "ÚLTIMAS UNIDADES", 150, 520, INK, 34)}
  <path id="sk-tr" d="M150 560 L930 560" stroke="{INK}" {THIN}/>
  {rows}
  {pill("sk-p", 150, 1310, 420, 76, "QUEDAN POQUITAS", BLUSH, INK, 30)}''')
R.hidden("#sk-t, #sk-tr, .sk-r, #sk-p", st)
R.pop("#sk-t", st + 0.15, 0.35); R.draw("#sk-tr", 800, st + 0.3, 0.5)
for k in range(4):
    R.fromTo(f"#sk-r{k}", "autoAlpha: 0, x: 40", "autoAlpha: 1, x: 0", st + 0.45 + k * 0.22, 0.5, "expo.out")
R.pop("#sk-p", S(21) + 0.6, 0.4)

# ================================================================== 7 · TIRO ALTO vs TIRO BAJO
st, en = S(25), E(27) + 0.3
R.clip("rise", st, en, HALO + f'''<g filter="url(#halo)">
  {jean("rj1", 235, 520, 0.5, "high")}
  {jean("rj2", 845, 520, 0.5, "low", wide=1.2)}
  <path id="rs-1" d="M96 520 L380 520" stroke="{INK}" stroke-dasharray="8 10" {THIN}/>
  <path id="rs-2" d="M700 542 L990 542" stroke="{INK}" stroke-dasharray="8 10" {THIN}/>
  {caps("rs-t1", "TIRO ALTO", 96, 498, INK, 24)}
  {caps("rs-t2", "TIRO BAJO", 990, 520, INK, 24, "end")}
  <path id="rs-om" d="M150 690 L930 690" stroke="{INK}" stroke-opacity="0.75" stroke-dasharray="4 12" {THIN}/>
  {caps("rs-omt", "OMBLIGO", 540, 672, INK, 22, "middle")}
  </g>{pill("rs-p", 330, 1230, 420, 64, "MÁS BAJITO Y ANCHITO", BLUSH, INK, 26)}''')
R.hidden(".rj1, .rj2, #rs-1, #rs-2, #rs-t1, #rs-t2, #rs-om, #rs-omt, #rs-p", st)
R.show(".rj1", st + 0.1); R.show(".rj2", st + 0.1)
R.draw(".rj1 path, .rj2 path", 1800, st + 0.1, 0.8, stagger=0.06)
R.draw("#rs-1", 310, st + 0.7, 0.35); R.pop("#rs-t1", st + 0.9, 0.3)
R.draw("#rs-2", 310, S(26) + 0.3, 0.35); R.pop("#rs-t2", S(26) + 0.5, 0.3)
R.pop("#rs-p", S(26) + 1.1, 0.4)
R.draw("#rs-om", 800, S(27) + 0.2, 0.5); R.pop("#rs-omt", S(27) + 0.5, 0.3)

# ================================================================== 8 · ESCENA · LOS COLORES (discos 3D)
st, en = S(29), E(34) + 0.3
COLORS = [("ROSADO", "FULLY BLUSH", "#E0BDB9"), ("AZUL DIRTY", "DIRTY WASHED", DENIM_DIRTY),
          ("NEGRO", "GRISÁCEO", CARBON), ("AZUL", "AZUL OSCURO", DENIM_D)]
labels = "".join(f'''
  <g class="cl-l" id="cl-l{k}">
    <text x="540" y="{1150 + k * 0}" text-anchor="middle" class="wl" fill="{INK}" style="font-size:44px;font-weight:400;letter-spacing:0.14em">{nm}</text>
    <text x="540" y="1208" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.55" style="font-size:26px">{sub}</text>
  </g>''' for k, (nm, sub, _) in enumerate(COLORS))
R.scene("scB", st, en, BEIGE, f'''
  <circle id="cl-ring" cx="540" cy="840" r="196" stroke="#1C1C1C" stroke-opacity="0.22" stroke-width="2" fill="none"/>
  {caps("cl-t", "LOS COLORES", 540, 520, INK, 34, "middle")}
  <path id="cl-tr" d="M330 560 L750 560" stroke="{INK}" {THIN}/>
  {labels}
  {pill("cl-p", 300, 1268, 480, 72, "MEJOR VENDIDO ALL TIME", BLUSH, INK, 26)}''')
R.hidden("#cl-t, #cl-tr, .cl-l, #cl-p, #cl-ring", st)
R.pop("#cl-t", st + 0.15, 0.35); R.draw("#cl-tr", 430, st + 0.3, 0.45); R.draw("#cl-ring", 1240, st + 0.3, 0.9)
BEATS = [S(30) + 0.2, S(32) + 0.2, S(33) + 0.2, S(34) + 0.2]
for k, at in enumerate(BEATS):
    nxt = BEATS[k + 1] if k + 1 < len(BEATS) else en - 0.3
    R.fromTo(f"#cl-l{k}", "autoAlpha: 0, y: 26", "autoAlpha: 1, y: 0", at, 0.45, "expo.out")
    if k + 1 < len(BEATS): R.to(f"#cl-l{k}", "autoAlpha: 0, y: -22", nxt - 0.18, 0.25, "power2.in")
R.pop("#cl-p", S(31) + 0.3, 0.45); R.fade("#cl-p", S(32) - 0.45, 0.0, 0.25); R.hidden("#cl-p", S(32) - 0.15)

R.gl({})
R.gl_add(f"""
      KEY.intensity = 0.40; FILL.intensity = 0.18; scene.children.forEach((o) => {{ if (o.isHemisphereLight) o.intensity = 1.05; }});
      const shade = (hex, f) => {{ const c = new THREE.Color(hex); c.multiplyScalar(f); return c; }};
      const LUX = ["{COLORS[0][2]}", "{COLORS[1][2]}", "{COLORS[2][2]}", "{COLORS[3][2]}"].map((c) => [new THREE.MeshBasicMaterial({{ color: shade(c, 0.86) }}), new THREE.MeshBasicMaterial({{ color: new THREE.Color(c) }}), new THREE.MeshBasicMaterial({{ color: shade(c, 0.94) }})]);
      function disc(mat, r = 0.95, h = 0.16) {{
        const g = new THREE.Group();
        const d = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 96), mat); d.rotation.x = Math.PI / 2; g.add(d);
        return g;
      }}
""")
R.gl_beat(st + 0.25, en, J(r"""
    if (!g.built) { g.built = true; g.ds = LUX.map((m, k) => { const d = disc(m); d.position.set(X(540), Y(840), 0); d.visible = false; g.add(d); return d; }); }
    const B = [$b0, $b1, $b2, $b3].map((x) => x - $st);
    g.ds.forEach((d, k) => {
      const inU = easeOut(seg(t, B[k], B[k] + 0.55));
      const outU = k + 1 < B.length ? easeInOut(seg(t, B[k + 1] - 0.3, B[k + 1] + 0.1)) : 0;
      d.visible = inU > 0 && outU < 1;
      d.scale.setScalar(inU * (1 - 0.35 * outU));
      d.position.y = Y(840) + (1 - inU) * -0.9 + outU * 1.1;
      d.rotation.y = (1 - inU) * 1.5 + (t - B[k]) * 0.5;
      d.rotation.x = 0.16 + Math.sin((t - B[k]) * 0.8) * 0.07;
    });
""", st=st, b0=BEATS[0], b1=BEATS[1], b2=BEATS[2], b3=BEATS[3]))

# ================================================================== 9 · CIERRE · LUXURJEANS.COM
st, en = S(35) - 0.1, R.DUR
R.scene("scC", st, en, BEIGE, f'''
  {caps("cs-w", "L U X U R", 540, 900, INK, 92, "middle", extra=";letter-spacing:0.22em;font-weight:400")}
  <path id="cs-r" d="M280 960 L800 960" stroke="{INK}" {THIN}/>
  {caps("cs-u", "LUXURJEANS.COM", 540, 1030, INK, 34, "middle")}
  {pill("cs-p", 330, 1100, 420, 76, "ENVÍOS A TODO EL PAÍS", BLUSH, INK, 26)}''')
R.hidden("#cs-w, #cs-r, #cs-u, #cs-p", st)
R.fromTo("#cs-w", "autoAlpha: 0, scaleX: 1.22, transformOrigin: '50% 50%'", "autoAlpha: 1, scaleX: 1", st + 0.15, 0.8, "expo.out")
R.draw("#cs-r", 520, st + 0.5, 0.5)
R.pop("#cs-u", S(36) + 0.2, 0.4); R.pop("#cs-p", S(37) + 0.3, 0.45)
R.fadeout(0.45)

# marca de agua tipográfica arriba (se reemplaza por el logo oficial cuando llegue)
R.cards_html.append(f'      <div id="logo" class="clip" data-start="0" data-duration="{E(2) + 0.25:.2f}" data-track-index="4"><span id="logo-w">LUXUR</span></div>')
R.raw(f'  tl.fromTo("#logo-w", {{ autoAlpha: 0, y: -14 }}, {{ autoAlpha: 0.9, y: 0, duration: 0.6, ease: "expo.out" }}, 0.15);')
R.raw(f'  tl.to("#logo-w", {{ autoAlpha: 0, duration: 0.3 }}, {E(2) - 0.1:.2f});')
R.raw(f'  tl.set("#logo-w", {{ autoAlpha: 0 }}, {E(2) + 0.25:.2f});')

R.write()
