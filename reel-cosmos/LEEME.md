# Sarier · reel "Unfold y Cosmos (guion 09)"

Composición HyperFrames v2 con capa 3D (three.js, `../reelkit.py` → `R.gl()`): monedas con los logos de `../brand/`, teléfono 3D, mark de Cosmos en tubos 3D, muro de Pinterest, chip y tiles que caen. Construida sobre `../reelkit.py` (motor común: subtítulos cinéticos, statements blancos por capas,
gráficos de línea en zona segura de Instagram, escenas faceless cortas, fundido final). Original subido como release `reel-5`.
Fuente 1080×1920 a 25 fps, pausas recortadas con `cut.py`.

## Renders finales
- `renders/*-final.mp4`            master · crf 17
- `renders/*-final-instagram.mp4`  copia para Instagram · 3 Mbps

## Regenerar
1. `../reel-tools/prep.sh <carpeta> <url-del-original> <sha256>` descarga, alinea el guion (TTS + DTW + pausas), corta silencios y codifica `public/input-video.mp4`.
2. `python3 build.py` regenera `index.html`; `npx hyperframes check`.
3. `../reel-tools/finish.sh <carpeta> <nombre>` renderiza y produce master + copia Instagram.
