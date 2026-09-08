# Sarier · reel "¿Por qué soñamos?" (sobreajuste y sueños) · v2

Composición HyperFrames: pausas del audio recortadas, subtítulos cinéticos, 3 statements blancos por capas,
dos explicaciones faceless a pantalla completa (SOBREAJUSTE sobre superficie clara `#F5F5F7`, NOCHE sobre
superficie oscura `#161618`) y 4 gráficos de línea superpuestos sobre la cara (cerebro, el mismo día, ayer/mañana, cosas nuevas).
Fuente: original HEVC 1080×1920 a 25 fps (la composición fija `data-fps="25"`). Duración ≈ 56.9 s (original 61.4 s).

## Renders finales
- `renders/sonamos-final.mp4`            master · 1080×1920 · 25 fps · 47 MB
- `renders/sonamos-final-instagram.mp4`  copia para Instagram · 3 Mbps · 14 MB

## Regenerar
1. `python3 cut.py` detecta las pausas del audio original (`audio16k.wav`, -28 dB / 0,22 s), escribe `cuts.json`,
   `captions.cut.json` (subtítulos remapeados) y `cut.filter`; luego el ffmpeg del LEEME del reel 1 con
   `-filter_complex_script cut.filter -map "[v]" -map "[a]"` y `-g 25 -keyint_min 25` produce `public/input-video.mp4`.
2. `python3 build.py` regenera `index.html` desde `captions.cut.json` (lee la duración del vídeo cortado).
3. `npx hyperframes check` y `npx hyperframes render`.

`guion.txt` son las frases de subtítulo; `align.py` + `retime2.py` alinean el guion al audio original y re-anclan a las pausas
(`captions.json`); `cut.py` remapea esos tiempos al vídeo sin pausas.
