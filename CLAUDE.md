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

## Pipeline

`reel-tools/prep.sh` (descarga + alineación + corte de pausas + encode) →
`python3 build.py` → `npx hyperframes check` → `reel-tools/finish.sh <dir> <nombre>`
(master crf 17 + copia Instagram). Los subtítulos se alinean sin ASR: espeak-ng → MFCC → DTW →
reanclaje a las pausas de `silencedetect`.

## Entregas

Copia Instagram ≤30 MB por chat; master en `<reel>/renders/`.
