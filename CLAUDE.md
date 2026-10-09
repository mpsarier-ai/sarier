# sarier — reels

Cada carpeta `reel-*` es un reel 9:16 hecho con HyperFrames + GSAP sobre el video original.
El motor compartido es `reelkit.py`; un `build.py` solo declara contenido y beats.

## Marcas

Cada reel usa el design system de SU marca, no el de otra. El tema vive en `THEMES` de `reelkit.py`.

- **Sarier** (`sarier`) — Archivo, ink `#1D1D1F`, acento rojo `#E1251B`.
- **LUXUR** (`luxur`) — Poppins, fondo beige `#EDEBE6`, ink `#1C1C1C`, blush `#EECDCC`, píldoras.
  Regla propia: ningún gráfico tapa la pantalla completa.
- **Ámbar Sculpt Studio** (`ambar`) — paquete oficial en `design-system/ambar/`.
  Para cualquier pieza de Ámbar lee primero `design-system/ambar/BRAND.md` y usa los tokens de
  `design-system/ambar/tokens.css`. No inventes colores ni fuentes. Sin sombras, sin iconos,
  sin esquinas redondeadas (solo el botón), y el anillo de beneficios es el único gráfico de la marca.
- **daniblooming** (`daniblooming`) — el sistema vive en el repo `mpsarier-ai/daniblooming` (el `:root` y
  el CSS de `index.html` / `bloom-reset.html`). Papel `#FFFAF3`, crema `#F9E8D8`, tinta café `#3A2418`,
  tinta suave `#7A5C48`, naranja `#E97C41`, rosa `#E18C8F`, rose `#E2B8BC`, oro `#B8AA2D`, azul `#B9C8FF`.
  Alegreya itálica (800 para títulos y números, 500 para los sub) + Poppins 300/400/500 para la interfaz.
  Tarjetas translúcidas con borde naranja y esquinas de 28px, píldoras de 99px, líneas punteadas,
  blobs desenfocados y la flor de seis pétalos (rose, centro naranja) como único ornamento. Aquí sí
  hay rebote: `cubic-bezier(.34,1.56,.64,1)`. Los logos se copian de `logo1.png` / `logo2.png`.
- **Fashionalytics / FOLD** (`fold`) — el sistema vive en el repo `mpsarier-ai/fashionalytics-platform`
  (`packages/ui/tokens.css`, `packages/ui/fx.css`) y en el brand book publicado
  `claude.ai/artifact/GGCvZa3r87KowSAk58Pyy4`. Geist + IBM Plex Mono + DotGothic16 + Instrument Serif,
  ink `#0a0a12`, brand `#1a1aff`, acid `#e6ff47` como único resaltador (uno por pantalla).
  Sin sombras, sentence case salvo mono y pixel, nada rebota (160 ms ease-out).
  Los logos y las texturas ASCII se copian del sistema, nunca se redibujan: ver `reel-fold/brand/`.

## Pipeline

`reel-tools/prep.sh` (descarga + alineación + corte de pausas + encode) →
`python3 build.py` → `npx hyperframes check` → `reel-tools/finish.sh <dir> <nombre>`
(master crf 17 + copia Instagram). Los subtítulos se alinean sin ASR: espeak-ng → MFCC → DTW →
reanclaje a las pausas de `silencedetect`.

## Entregas

Copia Instagram ≤30 MB por chat; master en `<reel>/renders/`.
