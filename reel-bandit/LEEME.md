# Sarier · reel "Bandido multibrazo (guion 05)"

Composición HyperFrames construida sobre `../reelkit.py` (motor común: subtítulos cinéticos, statements blancos por capas,
gráficos de línea en zona segura de Instagram, escenas faceless cortas, fundido final). Original subido como release `reel-4`.
Fuente 1080×1920 a 25 fps, pausas recortadas con `cut.py`.

## Renders finales
- `renders/*-final.mp4`            master · crf 17
- `renders/*-final-instagram.mp4`  copia para Instagram · 3 Mbps

## Regenerar
1. `../reel-tools/prep.sh <carpeta> <url-del-original> <sha256>` descarga, alinea el guion (TTS + DTW + pausas), corta silencios y codifica `public/input-video.mp4`.
2. `python3 build.py` regenera `index.html`; `npx hyperframes check`.
3. `../reel-tools/finish.sh <carpeta> <nombre>` renderiza y produce master + copia Instagram.
