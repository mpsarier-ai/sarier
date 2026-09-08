#!/usr/bin/env python3
"""Sarier reel 5 v2 — Unfold & Cosmos. Real brand marks as 3D coins, 3D phone, 3D Cosmos mark, Pinterest wall,
3D chip, falling tiles (three.js layer, seek-safe) + the 2D kinetic system. Andy's photo card if public/andy.jpg exists."""
import sys, os; sys.path.insert(0, "..")
from reelkit import *

R = Reel("Sarier — Unfold y Cosmos", gin_scale=0.58)
S, E, L = R.S, R.E, Reel.label
R.card_frags = {1, 2, 12, 33}
R.ink_frags = {14, 15}
R.punch = {3:"Unfold",4:"historias",5:"Stories",6:"brutal",7:"stickers",8:"gratis",9:"Canva",10:"pagar",11:"gratis",13:"todo",14:"editorial",
           15:"revista",16:"12",17:"50",18:"2019",19:"playa",20:"hacer",21:"Cosmos",22:"Pinterest",23:"misma",24:"atender",25:"muro",
           26:"vueltas",27:"IA",28:"criterio",29:"bajo",30:"estándar",31:"21",32:"Chanel"}
R.rail()
R.gl({n: f"../brand/{n}.svg" for n in ["instagram", "canva", "pinterest", "unfold", "squarespace", "apple", "nike", "chanel", "cosmos"]})
ANDY = os.path.exists("public/andy.jpg")
def J(js, **kw):
    for k, v in kw.items(): js = js.replace("$" + k, f"{v:.2f}" if isinstance(v, float) else str(v))
    return js

# ---------------------------------------------------------------- statements
R.card("hook", 0.0, E(2) + 0.2, [
    ("a","Se enfrentó a",56,72,252,"left","left",0.72),
    ("d","Y ganó todas las veces.",52,60,470,"right","drop",1.0, S(2) + 0.1)])
R.card("free", S(12) - 0.05, E(12) + 0.1, [
    ("a","Gratis y bueno",100,40,252,"left","scale",1.0),
    ("b","son productos",70,60,340,"right","right",0.72, S(12) + 0.9),
    ("c","distintos.",110,60,398,"right","drop",0.86, S(12) + 1.4)], glitch_key="a")
R.glitch(S(12) + 0.15)
R.punch_cam(S(12) + 0.25)
R.card("close", S(33) - 0.1, R.DUR, [
    ("a","Dos veces contra gigantes,",56,72,252,"left","left",0.72),
    ("b","sin tecnología",100,40,300,"left","scale",1.0, S(33) + 1.0),
    ("c","nueva.",140,60,388,"right","right",0.86, S(33) + 1.7)])
R.slow_push(S(33))
R.fadeout()

# ---------------------------------------------------------------- 3D helpers (JS)
R.gl_add(r"""
      // text on a canvas texture (numbers / short labels)
      function textTex(str, color = "#1D1D1F", size = 220, w = 512, h = 512) {
        const c = document.createElement("canvas"); c.width = w; c.height = h; const x = c.getContext("2d");
        x.fillStyle = color; x.font = `700 ${size}px Archivo, "Helvetica Neue", Helvetica, Arial, sans-serif`; x.textAlign = "center"; x.textBaseline = "middle";
        x.fillText(str, w / 2, h / 2 + size * 0.05); const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; return t;
      }
      function tile(w, h, d = 0.06, mat = M.light) { return new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); }
      function seg2(a, b, r = 0.06, mat = M.ink) {      // tube between two points (x,y) in the XY plane + round joints
        const g = new THREE.Group(); const dx = b[0] - a[0], dy = b[1] - a[1]; const len = Math.hypot(dx, dy);
        const m = tube(len, r, mat); m.position.set((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0); m.rotation.z = Math.atan2(dy, dx) - Math.PI / 2; g.add(m);
        const s = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 16), mat); s.position.set(b[0], b[1], 0); g.add(s); return g;
      }
      // the Cosmos mark as 3D tubes (two arcs + Z band), ~2.2 units tall
      function cosmosMark(s = 0.00917, r = 0.06, mat = M.ink) {
        const g = new THREE.Group(); const P = (x, y) => [(x - 120) * s, -(y - 120) * s];
        const R0 = 62 * s;
        const la = arc(R0, r, Math.PI / 2, Math.PI * 1.5, mat); la.position.set(...P(96, 120), 0); g.add(la);
        const ra = arc(R0, r, -Math.PI / 2, Math.PI / 2, mat); ra.position.set(...P(144, 120), 0); g.add(ra);
        [[P(144, 58), P(144, 110)], [P(96, 58), P(144, 110)], [P(144, 110), P(96, 140)], [P(96, 140), P(96, 182)], [P(96, 140), P(144, 182)]]
          .forEach(([a, b]) => g.add(seg2(a, b, r, mat)));
        return g;
      }
      function phone() {                                   // a phone with a light screen + the Unfold mark
        const g = new THREE.Group(); const body = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.8, 0.09), M.ink); g.add(body);
        const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.76, 1.56), M.light); scr.position.z = 0.047; g.add(scr);
        const logo = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.42), new THREE.MeshBasicMaterial({ map: TEX.unfold, transparent: true })); logo.position.set(0, 0.55, 0.05); g.add(logo);
        g.frames = [0, 1, 2].map((k) => { const f = tile(0.6, 0.26, 0.02, k === 1 ? M.red : M.white); f.position.set(0, 0.05 - k * 0.33, 0.06); f.visible = false; g.add(f); return f; });
        return g;
      }
      function chip() {
        const g = new THREE.Group(); g.add(new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.1, 0.16), M.ink));
        const core = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.04), M.red); core.position.z = 0.1; g.add(core);
        for (let i = 0; i < 6; i++) { const p = 0.72 * (i / 5 - 0.5) * 1.35;
          [[p, 0.66], [p, -0.66]].forEach(([x, y]) => { const pin = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.2, 0.06), M.grey); pin.position.set(x, y, 0); g.add(pin); });
          [[0.66, p], [-0.66, p]].forEach(([x, y]) => { const pin = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.06, 0.06), M.grey); pin.position.set(x, y, 0); g.add(pin); }); }
        return g;
      }
      function umbrella() {
        const g = new THREE.Group(); const top = new THREE.Mesh(new THREE.ConeGeometry(0.75, 0.42, 48, 1, true), M.red); top.position.y = 0.45; g.add(top);
        const pole = tube(1.5, 0.03, M.ink); pole.position.y = -0.25; g.add(pole); return g;
      }
""")

# ---------------------------------------------------------------- 1 · HOOK — three brand coins fly in (0 → E(2))
R.gl_beat(0.0, E(2) + 0.2, J(r"""
    if (!g.built) { g.built = true; g.coins = ["instagram", "canva", "pinterest"].map((n, k) => { const c = coin(n, 0.44); c.position.set(X(230 + k * 310), Y(385), 0); g.add(c); return c; }); }
    g.coins.forEach((c, k) => { const u0 = easeOut(seg(t, $a + k * 0.45, $a + k * 0.45 + 0.75));
      c.visible = u0 > 0; c.position.x = X(230 + k * 310) + (1 - u0) * 7; c.rotation.y = (1 - u0) * Math.PI * 2.5 + Math.sin(t * 1.3 + k) * 0.18; c.rotation.x = Math.sin(t * 0.9 + k) * 0.08;
      const bump = 1 + 0.18 * Math.sin(Math.PI * seg(t, $w + k * 0.12, $w + k * 0.12 + 0.35)); c.scale.setScalar(u0 * bump); });
""", a=0.55, w=S(2) + 0.25))

# ---------------------------------------------------------------- 2 · UNFOLD — 3D phone + the Unfold coin (S3 → E5)
st, en = S(3), E(5) + 0.2
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.ph = phone(); g.ph.position.set(X(330), Y(380), 0); g.add(g.ph); g.cn = coin("unfold", 0.5); g.cn.position.set(X(780), Y(380), 0); g.add(g.cn); }
    const u0 = easeOut(seg(t, 0.05, 0.8)); g.ph.scale.setScalar(u0); g.ph.rotation.y = -0.95 + 0.7 * u0 + Math.sin(t * 0.7) * 0.08; g.ph.rotation.x = 0.12;
    const u1 = easeOut(seg(t, 0.35, 1.0)); g.cn.visible = u1 > 0; g.cn.scale.setScalar(u1); g.cn.rotation.y = (1 - u1) * Math.PI * 2 + Math.sin(t) * 0.2;
    g.ph.frames.forEach((f, k) => { const uf = easeOut(seg(t, $f + k * 0.18, $f + k * 0.18 + 0.4)); f.visible = uf > 0; f.position.y = 0.05 - k * 0.33 - (1 - uf) * 0.8; f.scale.setScalar(0.6 + 0.4 * uf);
      const pulse = 1 + 0.12 * Math.sin(Math.PI * seg(t, $p + k * 0.15, $p + k * 0.15 + 0.3)); f.scale.multiplyScalar(pulse); });
""", f=S(4) - st + 0.3, p=S(5) - st + 0.5))
R.clip("unfold", st, en, L("uf-t", "UNFOLD · PLANTILLAS PARA STORIES", 500))
R.hidden("#uf-t", st); R.pop("#uf-t", S(5) + 0.6, 0.3)

# ---------------------------------------------------------------- 3 · LA OBJECIÓN — Instagram & Canva give it away; why pay Unfold? (S6 → E11)
st, en = S(6), E(11) + 0.2
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.a = coin("instagram", 0.5); g.a.position.set(X(250), Y(330), 0); g.b = coin("canva", 0.5); g.b.position.set(X(830), Y(330), 0);
      g.c = coin("unfold", 0.3); g.c.position.set(X(540), Y(345), 0); g.add(g.a, g.b, g.c); }
    const ua = easeOut(seg(t, $a, $a + 0.7)), ub = easeOut(seg(t, $b, $b + 0.7)), uc = easeOut(seg(t, $c, $c + 0.6));
    const fa = easeInOut(seg(t, $fa, $fa + 0.8)), fb = easeInOut(seg(t, $fb, $fb + 0.8));
    g.a.visible = ua > 0; g.a.scale.setScalar(ua); g.a.rotation.y = (1 - ua) * Math.PI * 2 + fa * Math.PI * 2 + Math.sin(t) * 0.15;
    g.b.visible = ub > 0; g.b.scale.setScalar(ub); g.b.rotation.y = (1 - ub) * Math.PI * 2 + fb * Math.PI * 2 + Math.sin(t + 1) * 0.15;
    g.c.visible = uc > 0; g.c.scale.setScalar(uc); g.c.rotation.y = (1 - uc) * Math.PI * 3 + Math.sin(t * 1.4) * 0.3; g.c.position.y = Y(345) + Math.sin(t * 2) * 0.03;
""", a=S(7) - st + 0.1, b=S(9) - st + 0.05, c=S(10) - st + 0.5, fa=S(8) - st + 1.0, fb=S(9) - st + 1.6))
R.clip("obj", st, en, f'''
  {L("ob-fa", "GRATIS", 440, x=250, color=RED, cls="wl2")}{L("ob-fb", "GRATIS", 440, x=830, color=RED, cls="wl2")}
  <text id="ob-cs" x="540" y="120" text-anchor="middle" class="big" fill="{RED}" style="font-size:72px">$</text>
  {L("ob-q", "¿POR QUÉ PAGAR?", 470, color=RED, cls="wl2")}''')
R.hidden("#ob-fa, #ob-fb, #ob-cs, #ob-q", st)
R.pop("#ob-fa", S(8) + 1.0, 0.3); R.pop("#ob-fb", S(9) + 1.6, 0.3); R.pop("#ob-cs", S(10) + 0.9, 0.25); R.pop("#ob-q", S(11) + 0.3, 0.3)

# ---------------------------------------------------------------- 4 · "no persiguió a todo el mundo" (2D crowd)
st, en = S(13), S(14) - 0.02
grid = "".join(f'<circle class="cr-d" cx="{200 + (k % 10) * 76}" cy="{140 + (k // 10) * 76}" r="16" fill="{INK}"/>' for k in range(30))
R.clip("crowd", st, en, grid + L("cr-t", "NO A TODO EL MUNDO", 440))
R.hidden("#cr-t", st); R.pop(".cr-d", st + 0.05, 0.2, stagger=0.02); R.pop("#cr-t", st + 1.0, 0.3)

# ---------------------------------------------------------------- 5 · SCENE · EDITORIAL — 3D people, four turn red, a magazine flips up (S14 → E15)
st, en = S(14), E(15) + 0.15
R.scene("scA", st, en, LIGHT, f'''
  {L("ed-t", "FUE DETRÁS DE LA GENTE QUE QUERÍA", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {Reel.big("ed-x", "EDITORIAL", 1000, RED, x=180, anchor="start", size=90)}''')
R.hidden("#ed-x, #ed-t", st); R.pop("#ed-t", st + 0.2, 0.3); R.pop("#ed-x", S(14) + 2.2, 0.3)
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.dots = []; const dim = new THREE.MeshStandardMaterial({ color: 0x1D1D1F, roughness: 0.6, transparent: true, opacity: 1 }); g.dim = dim;
      for (let k = 0; k < 18; k++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.13, 24, 24), dim); d.position.set(X(180 + (k % 6) * 144), Y(560 + Math.floor(k / 6) * 130), 0); g.dots.push(d); g.add(d); }
      g.mag = new THREE.Group(); const cover = tile(4.0, 1.34, 0.06, M.white); g.mag.add(cover);
      const bar = tile(2.0, 0.12, 0.02, M.ink); bar.position.set(-0.8, 0.42, 0.04); g.mag.add(bar);
      [0.1, -0.1, -0.3].forEach((y, i) => { const ln = tile(3.4 - i * 0.6, 0.04, 0.02, M.ink); ln.position.set(-0.3 - i * 0.3, y, 0.04); g.mag.add(ln); });
      g.mag.position.set(X(540), Y(1160), 0); g.add(g.mag); }
    g.dots.forEach((d, k) => { const u0 = easeOut(seg(t, 0.3 + k * 0.03, 0.55 + k * 0.03)); const hot = [2, 7, 9, 14].includes(k);
      const uh = easeOut(seg(t, $h + (k % 4) * 0.1, $h + 0.4 + (k % 4) * 0.1)); d.visible = u0 > 0; d.scale.setScalar(u0 * (1 + 0.6 * (hot ? uh : 0)));
      d.material = hot && uh > 0.3 ? M.red : g.dim; d.position.z = hot ? uh * 1.4 : 0; });
    g.dim.opacity = 1 - 0.65 * easeOut(seg(t, $h + 0.4, $h + 0.8));
    const um = easeOut(seg(t, $m, $m + 0.7)); g.mag.visible = um > 0; g.mag.rotation.x = (1 - um) * -1.3; g.mag.scale.setScalar(0.7 + 0.3 * um); g.mag.rotation.y = Math.sin(t) * 0.06;
""", h=S(14) - st + 1.9, m=S(15) - st + 0.05))

# ---------------------------------------------------------------- 6 · STATS — 12M → Squarespace coin + $50M (S16 → E18)
st, en = S(16), E(18) + 0.2
R.clip("stats", st, en, f'''
  {Reel.big("st-12", "12M", 250, INK, x=72, anchor="start", size=200)}
  {L("st-u", "USUARIOS · 8 MESES · BOOTSTRAPPED", 330, x=72, anchor="start")}
  {Reel.big("st-50", "$50M", 250, RED, x=1008, anchor="end", size=180)}
  {L("st-s", "SQUARESPACE · 2019", 330, x=1008, anchor="end", color=RED)}''')
R.hidden("#st-12, #st-u, #st-50, #st-s", st)
R.pop("#st-12", S(16) + 0.8, 0.3); R.pop("#st-u", S(16) + 1.8, 0.3)
R.to("#st-12, #st-u", "x: -1000", S(17) + 1.0, 0.4, "power2.in")
R.pop("#st-50", S(17) + 1.6, 0.3); R.pop("#st-s", S(18) + 0.3, 0.3)
R.gl_beat(S(17) + 1.0, en, r"""
    if (!g.built) { g.built = true; g.c = coin("squarespace", 0.42); g.c.position.set(X(250), Y(330), 0); g.add(g.c); }
    const u0 = easeOut(seg(t, 0.2, 0.9)); g.c.scale.setScalar(u0); g.c.rotation.y = (1 - u0) * Math.PI * 3 + Math.sin(t) * 0.2;
""")

# ---------------------------------------------------------------- 7 · PLAYA — umbrella (3D) + Andy's photo card if available (S19 → E20)
st, en = S(19), E(20) + 0.2
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.u = umbrella(); g.u.position.set(X($ux), Y(330), 0); g.add(g.u);
      g.rep = cosmosMark(0.004, 0.035, M.red); g.rep.position.set(X(860), Y(330), 0); g.add(g.rep); }
    const u0 = easeOut(seg(t, 0.05, 0.7)); g.u.scale.setScalar(u0 * 1.25); g.u.rotation.z = -0.25 + Math.sin(t * 1.5) * 0.06; g.u.rotation.y = Math.sin(t) * 0.3;
    const u1 = easeOut(seg(t, $r, $r + 0.6)); g.rep.visible = u1 > 0; g.rep.scale.setScalar(u1); g.rep.rotation.y = (t - $r) * 4;
""", ux=(700 if ANDY else 300), r=S(20) - st + 0.1))
R.clip("beach", st, en, L("bc-t", "LO VUELVE A HACER", 500, color=RED))
R.hidden("#bc-t", st); R.pop("#bc-t", S(20) + 0.4, 0.3)
if ANDY:
    R.extra_css += "\n      #andy { position: absolute; left: 90px; top: 250px; width: 300px; height: 380px; perspective: 900px; pointer-events: none; }\n      #andy img { width: 300px; height: 380px; object-fit: cover; border-radius: 18px; box-shadow: 0 18px 40px rgba(0,0,0,0.35); display: block; }\n"
    R.cards_html.append(f'      <div id="andy" class="clip" data-start="{st:.2f}" data-duration="{en - st:.2f}" data-track-index="4"><img id="andy-img" src="public/andy.jpg" alt=""></div>')
    R.raw(f'  tl.fromTo("#andy-img", {{ autoAlpha: 0, rotationY: -70, x: -120, transformPerspective: 900 }}, {{ autoAlpha: 1, rotationY: -8, x: 0, duration: 0.7, ease: "expo.out" }}, {st + 0.1:.2f});')
    R.raw(f'  tl.to("#andy-img", {{ rotationY: 8, duration: {en - st - 0.9:.2f}, ease: "sine.inOut" }}, {st + 0.8:.2f});')
    R.raw(f'  tl.to("#andy-img", {{ autoAlpha: 0, duration: 0.25 }}, {en - 0.25:.2f});')
    R.raw(f'  tl.set("#andy-img", {{ autoAlpha: 0 }}, {en:.2f});')

# ---------------------------------------------------------------- 8 · COSMOS — the mark in 3D, then the Pinterest wall (S21 → E25)
st, en = S(21), E(25) + 0.2
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.mk = cosmosMark(); g.mk.position.set(X(540), Y(360), 0); g.add(g.mk);
      g.wall = new THREE.Group(); g.tiles = [];
      for (let k = 0; k < 12; k++) { const tl_ = tile(0.6, 0.28 + (k % 3) * 0.06, 0.05, M.white); tl_.userData.gy = Y(290 + Math.floor(k / 4) * 90); tl_.userData.gx = X(560 + (k % 4) * 130);
        tl_.userData.sy = tl_.userData.gy + ((k * 7) % 5 - 2) * 0.12; tl_.userData.sx = tl_.userData.gx + ((k * 3) % 4 - 1.5) * 0.06; tl_.position.set(tl_.userData.sx, tl_.userData.sy, -0.3 - (k % 3) * 0.25);
        g.wall.add(tl_); g.tiles.push(tl_); }
      g.wall.visible = false; g.add(g.wall); g.pin = coin("pinterest", 0.34); g.pin.position.set(X(950), Y(440), 0.5); g.pin.visible = false; g.add(g.pin); }
    const u0 = easeOut(seg(t, 0.05, 0.9)); g.mk.scale.setScalar(u0 * 1.0); g.mk.rotation.y = (1 - u0) * Math.PI + Math.sin(t * 0.8) * 0.45; g.mk.rotation.x = Math.sin(t * 0.5) * 0.15;
    const um = easeInOut(seg(t, $w - 0.4, $w + 0.3)); g.mk.position.x = X(540) + (X(260) - X(540)) * um; g.mk.scale.setScalar(u0 * (1 - 0.25 * um));
    const uw = easeOut(seg(t, $w, $w + 0.8)); g.wall.visible = uw > 0; g.wall.rotation.y = -0.55 * (1 - 0.0) ;
    const ua = easeInOut(seg(t, $al, $al + 0.7)); g.wall.rotation.y = -0.55 + 0.55 * ua;
    g.tiles.forEach((tl_, k) => { const ut = easeOut(seg(t, $w + k * 0.05, $w + 0.5 + k * 0.05)); tl_.scale.setScalar(ut); tl_.visible = ut > 0;
      const hot = [1, 6, 9].includes(k); const uh = easeOut(seg(t, $sg + (k % 3) * 0.12, $sg + 0.4 + (k % 3) * 0.12)); tl_.material = hot && uh > 0.3 ? M.red : M.white;
      tl_.position.x = tl_.userData.sx + (tl_.userData.gx - tl_.userData.sx) * ua; tl_.position.y = tl_.userData.sy + (tl_.userData.gy - tl_.userData.sy) * ua; tl_.position.z = (-0.3 - (k % 3) * 0.25) * (1 - ua) + (hot ? uh * 0.35 : 0); });
    const up = easeOut(seg(t, $w + 0.6, $w + 1.3)); g.pin.visible = up > 0; g.pin.scale.setScalar(up); g.pin.rotation.y = (1 - up) * Math.PI * 3 + Math.sin(t) * 0.2;
""", w=S(22) - st + 0.8, sg=S(24) - st + 1.2, al=S(25) - st + 0.9))
R.clip("cosmos", st, en, L("cs-t", "COSMOS · REFERENCIAS VISUALES", 480, x=72, anchor="start", color=RED) + L("cs-pt", "PINTEREST", 480, x=1008, anchor="end") + L("cs-w", "EL MURO", 480, x=1008, anchor="end", color=RED))
R.hidden("#cs-t, #cs-pt, #cs-w", st); R.pop("#cs-t", st + 0.5, 0.3); R.pop("#cs-pt", S(22) + 1.6, 0.3)
R.fade("#cs-pt", S(25) + 0.9, 0.0, 0.2); R.pop("#cs-w", S(25) + 1.0, 0.3)

# ---------------------------------------------------------------- 9 · IA CHIP 3D (S26 → E27)
st, en = S(26), E(27) + 0.2
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.ch = chip(); g.ch.position.set(X(540), Y(340), 0); g.add(g.ch); }
    const u0 = easeOut(seg(t, $a, $a + 0.8)); g.ch.visible = u0 > 0; g.ch.scale.setScalar(u0); g.ch.rotation.x = 0.55 - 0.2 * u0; g.ch.rotation.y = (1 - u0) * Math.PI + t * 0.9; g.ch.rotation.z = 0.1;
""", a=S(27) - st + 0.05))
R.clip("chip", st, en, L("ia-t", "IA · IGUAL QUE TODO EL MUNDO", 480))
R.hidden("#ia-t", st); R.pop("#ia-t", S(27) + 1.2, 0.3)

# ---------------------------------------------------------------- 10 · SCENE · CRITERIO — 3D tiles get scored, low ones fall (S28 → E29)
st, en = S(28), E(29) + 0.15
SCORES = [9, 4, 8, 3, 7, 9, 2, 6, 8]
R.scene("scB", st, en, DARK, f'''
  {L("cr-t", "LA APUNTA AL CRITERIO", y=330, x=72, anchor="start", color=RED, cls="wl2")}
  {L("cr-b", "CALIFICA · QUITA LO QUE PUNTÚA BAJO", 1290, x=72, anchor="start", color=WHITE, cls="wl2")}''')
R.hidden("#cr-t, #cr-b", st); R.pop("#cr-t", st + 0.2, 0.3); R.pop("#cr-b", S(29) + 1.5, 0.3)
R.gl_beat(st, en, J(r"""
    if (!g.built) { g.built = true; g.tiles = []; const SC = [9, 4, 8, 3, 7, 9, 2, 6, 8];
      SC.forEach((v, k) => { const tg = new THREE.Group(); const b = tile(1.15, 0.95, 0.08, M.white); tg.add(b);
        const n = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.7), new THREE.MeshBasicMaterial({ map: textTex(String(v), v < 5 ? "#E1251B" : "#1D1D1F", 300), transparent: true })); n.position.z = 0.05; n.visible = false; tg.add(n); tg.num = n;
        if (v < 5) { const x1 = tile(0.9, 0.09, 0.03, M.red), x2 = tile(0.9, 0.09, 0.03, M.red); x1.rotation.z = Math.PI / 4; x2.rotation.z = -Math.PI / 4; x1.position.z = x2.position.z = 0.08; x1.visible = x2.visible = false; tg.add(x1, x2); tg.xs = [x1, x2]; }
        tg.userData.x = X(260 + (k % 3) * 280); tg.userData.y = Y(640 + Math.floor(k / 3) * 230); tg.position.set(tg.userData.x, tg.userData.y, 0); tg.low = v < 5; g.add(tg); g.tiles.push(tg); });
      g.rotation.x = -0.28; }
    g.tiles.forEach((tg, k) => { const u0 = easeOut(seg(t, 0.25 + k * 0.05, 0.6 + k * 0.05)); tg.scale.setScalar(u0); tg.visible = u0 > 0;
      const un = seg(t, $n + k * 0.09, $n + 0.2 + k * 0.09); tg.num.visible = un > 0; tg.num.scale.setScalar(0.6 + 0.4 * easeOut(un));
      if (tg.low) { const ux = seg(t, $x + k * 0.08, $x + 0.25 + k * 0.08); tg.xs.forEach((x, i) => { x.visible = ux > 0; x.scale.x = easeOut(seg(ux, i * 0.4, i * 0.4 + 0.6)); });
        const uf = seg(t, $f + k * 0.08, $f + 1.2 + k * 0.08); tg.position.y = tg.userData.y - 9 * uf * uf; tg.rotation.z = -1.4 * uf; tg.rotation.x = 1.2 * uf; } });
""", n=S(29) - st + 0.3, x=S(29) - st + 1.7, f=S(29) - st + 2.3))

# ---------------------------------------------------------------- 11 · ESTÁNDAR ≠ NÚMERO (2D)
st, en = S(30), E(30) + 0.2
R.clip("std", st, en, f'''
  {Reel.big("sd-a", "UN ESTÁNDAR", 220, INK, x=540, size=96)}
  {Reel.big("sd-b", "UN NÚMERO", 380, INK, x=540, size=96)}
  <path id="sd-s" d="M250 350 H830" stroke="{RED}" stroke-width="14" stroke-linecap="round" fill="none"/>''')
R.hidden("#sd-a, #sd-b", st)
R.pop("#sd-a", S(30) + 1.5, 0.3); R.pop("#sd-b", S(30) + 2.4, 0.3); R.draw("#sd-s", 600, S(30) + 2.8, 0.3)

# ---------------------------------------------------------------- 12 · $21M · Apple Nike Chanel coins (S31 → E32)
st, en = S(31), S(33) - 0.15
R.clip("money", st, en, Reel.big("mo-n", "$21M", 200, RED, x=540, size=200) + L("mo-t", "LEVANTADOS", 270))
R.hidden("#mo-n, #mo-t", st); R.pop("#mo-n", S(31) + 1.9, 0.3); R.pop("#mo-t", S(31) + 2.4, 0.3)
R.gl_beat(S(32), en, r"""
    if (!g.built) { g.built = true; g.coins = ["apple", "nike", "chanel"].map((n, k) => { const c = coin(n, 0.36); c.position.set(X(270 + k * 270), Y(470), 0); g.add(c); return c; }); }
    g.coins.forEach((c, k) => { const u0 = easeOut(seg(t, 1.2 + k * 0.5, 1.9 + k * 0.5)); c.visible = u0 > 0; c.scale.setScalar(u0); c.rotation.y = (1 - u0) * Math.PI * 3 + Math.sin(t + k) * 0.2; });
""")

R.write()
