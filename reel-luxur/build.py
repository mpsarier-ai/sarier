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
R.ink_frags = {20, 21, 29, 30, 31, 32, 33, 34}
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
    return f'<text id="{id_}" x="{x}" y="{y}" text-anchor="{anchor}" class="wl" fill="{color}" style="font-size:{size}px{extra}">{esc(text)}</text>'

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
        art = (f'<rect class="{cid}-img" x="{x + pad}" y="{y + pad}" width="{iw}" height="{ih}" rx="18" fill="{WHITE}" fill-opacity="0.5" stroke="{INK}" stroke-opacity="0.25" stroke-dasharray="10 10" {THIN}/>'
               f'<text x="{x + w/2:.0f}" y="{y + pad + ih/2:.0f}" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.45" style="font-size:22px">FOTO {esc(fit.upper())}</text>')
    lab = (f'<text x="{x + w/2:.0f}" y="{y + h - 42:.0f}" text-anchor="middle" class="wl" fill="{INK}" style="font-size:26px">{esc(title)}</text>'
           f'<text x="{x + w/2:.0f}" y="{y + h - 14:.0f}" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.55" style="font-size:20px">{esc(sub)}</text>') if title else ""
    return (f'<g class="{cid}" filter="url(#soft)"><rect class="{cid}-bg" x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{BEIGE}"/>'
            f'{art}{lab}</g>')

# ================================================================== 1 · HOOK
R.card("hook", 0.0, E(2) + 0.25, [
    ("a", "Dos cosas", 118, 72, 1020, "left", "left", 1.0),
    ("b", "antes de comprar", 62, 72, 1128, "left", "left", 0.86, S(2) + 0.05),
    ("c", "tu LUXUR.", 92, 72, 1188, "left", "scale", 1.0, S(2) + 0.5)])
R.clip("hookp", 0.35, E(2) + 0.25, pill("hp", 72, 920, 210, 62, "SÍ O SÍ", BLUSH, INK, 26))
R.hidden("#hp", 0.35); R.pop("#hp", 0.5, 0.35)

# ================================================================== 2 · TIKTOK · BIEBER × GAP
st, en = S(3), E(5) + 0.25
R.clip("tk", st, en, HALO + f'''
  <g filter="url(#soft)"><rect id="tk-c" x="580" y="300" width="440" height="250" rx="34" fill="{BEIGE}"/></g>
  {caps("tk-a", "EN TIKTOK", 620, 372, INK, 26)}
  <path id="tk-r" d="M620 400 L980 400" stroke="{INK}" {THIN}/>
  {caps("tk-b", "TODO EL MUNDO", 620, 452, INK, 34, extra=";font-weight:400")}
  {caps("tk-c", "HABLA DEL BIEBER", 620, 500, INK, 24)}''')
R.hidden("#tk-c, #tk-a, #tk-b, #tk-r", st)
R.fromTo("#tk-c", "autoAlpha: 0, scaleX: 0.6, transformOrigin: '100% 50%'", "autoAlpha: 1, scaleX: 1", st + 0.05, 0.45, "expo.out")
R.pop("#tk-a", st + 0.3, 0.3); R.draw("#tk-r", 360, st + 0.45, 0.4)
R.pop("#tk-b", S(4) + 0.2, 0.35); R.pop("#tk-c", S(5) + 0.1, 0.35)

# ================================================================== 3 · EL DÚO PERFECTO — dos fichas
st, en = S(6), E(8) + 0.25
R.clip("duo", st, en, HALO
  + fitcard("d1", "relaxed", 34, 470, 330, 520, "RELAXED FIT", "TIRO ALTO")
  + fitcard("d2", "low", 716, 470, 330, 520, "LOW WIDE FIT", "TIRO BAJO")
  + f'''<path id="du-x" d="M498 726 L582 726 M540 684 L540 768" stroke="{BLUSH}" {THIN}/>
  {pill("du-p", 380, 1040, 320, 64, "EL DÚO PERFECTO", BLUSH, INK, 26)}''')
R.hidden(".d1, .d2, #du-x, #du-p", st)
R.fromTo(".d1", "autoAlpha: 0, x: -60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.fromTo(".d2", "autoAlpha: 0, x: 60", "autoAlpha: 1, x: 0", S(6) + 0.75, 0.6, "expo.out")
R.draw("#du-x", 180, S(7) + 0.2, 0.3); R.pop("#du-p", S(8) + 0.3, 0.4)

# ================================================================== 4 · FIT 1 · RELAXED (tiro alto)
st, en = S(11), E(15) + 0.25
R.clip("f1", st, en, HALO
  + fitcard("f1c", "relaxed", 40, 430, 400, 640, "RELAXED FIT", "$199.000")
  + f'''<g filter="url(#halo)">
  <path id="f1-line" d="M470 560 L1000 560" stroke="{INK}" stroke-dasharray="8 10" {THIN}/>
  {caps("f1-lt", "TIRO ALTO", 1000, 536, INK, 24, "end")}
  {caps("f1-n", "RELAJADO", 1000, 700, INK, 44, "end", extra=";letter-spacing:0.12em")}
  <path id="f1-r" d="M640 736 L1000 736" stroke="{INK}" {THIN}/>
  {caps("f1-d", "HECHO PARA USARLO BONITO", 1000, 786, INK, 22, "end")}</g>
  {pill("f1-p", 700, 830, 300, 64, "PARA QUE LO ANOTEN", BEIGE, INK, 24)}''')
R.hidden(".f1c, #f1-line, #f1-lt, #f1-n, #f1-r, #f1-d, #f1-p", st)
R.fromTo(".f1c", "autoAlpha: 0, x: -60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.draw("#f1-line", 540, S(12) + 0.35, 0.5); R.pop("#f1-lt", S(12) + 0.6, 0.3)
R.pop("#f1-n", S(14) + 0.1, 0.4); R.draw("#f1-r", 360, S(14) + 0.3, 0.4); R.pop("#f1-d", S(14) + 0.5, 0.3)
R.pop("#f1-p", S(15) + 0.5, 0.35)

# ================================================================== 5 · FIT 2 · LOW WIDE (2º más vendido)
st, en = S(16), E(18) + 0.25
R.clip("f2", st, en, HALO
  + fitcard("f2c", "low", 640, 430, 400, 640, "LOW WIDE FIT", "$199.000")
  + f'''<g filter="url(#halo)">
  {caps("f2-n", "EL SEGUNDO", 80, 700, INK, 44, extra=";letter-spacing:0.12em")}
  <path id="f2-r" d="M80 736 L440 736" stroke="{INK}" {THIN}/>
  {caps("f2-d", "TIRO BAJO · ANCHO", 80, 786, INK, 22)}</g>
  {pill("f2-b", 80, 830, 360, 64, "2º MÁS VENDIDO", BLUSH, INK, 26)}''')
R.hidden(".f2c, #f2-n, #f2-r, #f2-d, #f2-b", st)
R.fromTo(".f2c", "autoAlpha: 0, x: 60", "autoAlpha: 1, x: 0", st + 0.1, 0.6, "expo.out")
R.pop("#f2-n", S(16) + 0.9, 0.4); R.draw("#f2-r", 360, S(16) + 1.1, 0.4); R.pop("#f2-d", S(16) + 1.3, 0.3)
R.pop("#f2-b", S(17) + 0.9, 0.4)

# ================================================================== 6 · ESCENA · ÚLTIMAS UNIDADES (stock real)
st, en = S(20), E(21) + 0.3
STOCK = [("AZUL OSCURO", 1, DENIM_D), ("AZUL DIRTY", 10, DENIM_DIRTY), ("NEGRO", 15, CARBON), ("ROSADO", 22, ROSA)]
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

# ================================================================== 7 · TIRO ALTO vs TIRO BAJO (las dos fotos)
st, en = S(25), E(27) + 0.3
R.clip("rise", st, en, HALO
  + fitcard("r1c", "relaxed", 34, 430, 330, 520, "TIRO ALTO", "RELAXED")
  + fitcard("r2c", "low", 716, 430, 330, 520, "TIRO BAJO", "LOW WIDE")
  + f'''<g filter="url(#halo)">
  <path id="rs-om" d="M150 700 L930 700" stroke="{INK}" stroke-opacity="0.7" stroke-dasharray="4 12" {THIN}/>
  {caps("rs-omt", "OMBLIGO", 540, 684, INK, 22, "middle")}</g>
  {pill("rs-p", 330, 1040, 420, 64, "MÁS BAJITO Y ANCHITO", BLUSH, INK, 26)}''')
R.hidden(".r1c, .r2c, #rs-om, #rs-omt, #rs-p", st)
R.fromTo(".r1c", "autoAlpha: 0, x: -50", "autoAlpha: 1, x: 0", st + 0.1, 0.55, "expo.out")
R.fromTo(".r2c", "autoAlpha: 0, x: 50", "autoAlpha: 1, x: 0", st + 0.25, 0.55, "expo.out")
R.pop("#rs-p", S(26) + 1.1, 0.4)
R.draw("#rs-om", 800, S(27) + 0.2, 0.5); R.pop("#rs-omt", S(27) + 0.5, 0.3)

# ================================================================== 8 · ESCENA · LOS COLORES (discos 3D)
st, en = S(29), E(34) + 0.3
COLORS = [("ROSADO", "FULLY BLUSH", ROSA), ("AZUL DIRTY", "DIRTY WASHED", DENIM_DIRTY),
          ("NEGRO", "GRISÁCEO", CARBON), ("AZUL", "AZUL OSCURO", DENIM_D)]
labels = "".join(f'''
  <g class="cl-l" id="cl-l{k}">
    <text x="540" y="1150" text-anchor="middle" class="wl" fill="{INK}" style="font-size:44px;font-weight:400;letter-spacing:0.14em">{nm}</text>
    <text x="540" y="1208" text-anchor="middle" class="wl" fill="{INK}" fill-opacity="0.55" style="font-size:26px">{sub}</text>
  </g>''' for k, (nm, sub, _) in enumerate(COLORS))
R.scene("scB", st, en, BEIGE, f'''
  <circle id="cl-ring" cx="540" cy="840" r="196" stroke="{INK}" stroke-opacity="0.22" stroke-width="2" fill="none"/>
  {caps("cl-t", "LOS COLORES", 540, 520, INK, 34, "middle")}
  <path id="cl-tr" d="M330 560 L750 560" stroke="{INK}" {THIN}/>
  {labels}
  {pill("cl-p", 300, 1268, 480, 72, "MEJOR VENDIDO ALL TIME", BLUSH, INK, 26)}''')
R.hidden("#cl-t, #cl-tr, .cl-l, #cl-p, #cl-ring", st)
R.pop("#cl-t", st + 0.15, 0.35); R.draw("#cl-tr", 430, st + 0.3, 0.45); R.draw("#cl-ring", 1240, st + 0.3, 0.9)
BEATS = [S(30) + 0.2, S(32) + 0.2, S(33) + 0.2, S(34) + 0.2]
for k, at in enumerate(BEATS):
    R.fromTo(f"#cl-l{k}", "autoAlpha: 0, y: 26", "autoAlpha: 1, y: 0", at, 0.45, "expo.out")
    if k + 1 < len(BEATS): R.to(f"#cl-l{k}", "autoAlpha: 0, y: -22", BEATS[k + 1] - 0.18, 0.25, "power2.in")
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
  {caps("cs-w", "LUXUR", 540, 900, INK, 128, "middle", extra=MONT)}
  <path id="cs-r" d="M320 962 L760 962" stroke="{INK}" {THIN}/>
  {caps("cs-u", "LUXURJEANS.COM", 540, 1032, INK, 34, "middle")}
  {pill("cs-p", 330, 1104, 420, 76, "ENVÍOS A TODO EL PAÍS", BLUSH, INK, 26)}''')
R.hidden("#cs-w, #cs-r, #cs-u, #cs-p", st)
R.fromTo("#cs-w", "autoAlpha: 0, scale: 0.94, transformOrigin: '50% 50%'", "autoAlpha: 1, scale: 1", st + 0.15, 0.7, "expo.out")
R.draw("#cs-r", 440, st + 0.5, 0.5)
R.pop("#cs-u", S(36) + 0.2, 0.4); R.pop("#cs-p", S(37) + 0.3, 0.45)
R.fadeout(0.45)

# wordmark de apertura (Montserrat SemiBold, espaciado mínimo)
R.cards_html.append(f'      <div id="logo" class="clip" data-start="0" data-duration="{E(2) + 0.25:.2f}" data-track-index="4"><span id="logo-w">LUXUR</span></div>')
R.raw('  tl.fromTo("#logo-w", { autoAlpha: 0, y: -14 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "expo.out" }, 0.15);')
R.raw(f'  tl.to("#logo-w", {{ autoAlpha: 0, duration: 0.3 }}, {E(2) - 0.1:.2f});')
R.raw(f'  tl.set("#logo-w", {{ autoAlpha: 0 }}, {E(2) + 0.25:.2f});')

R.write()
