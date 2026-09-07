# Sarier · reel "Criterio excepcional" (ciclo de Kolb)

Composición HyperFrames: subtítulos cinéticos, 3 statements, 6 gráficos de línea que siguen el ciclo.
Fuente: original HEVC 1080×1920 a 25 fps (la composición fija `data-fps="25"`).

## Renders finales
- `renders/criterio-final.mp4`            master · 1080×1920 · 25 fps · 81 MB
- `renders/criterio-final-instagram.mp4`  copia para Instagram · 3 Mbps · 26 MB

## Regenerar
1. Pon el original convertido en `public/input-video.mp4` (ver el LEEME del reel 1; usa `-g 25 -keyint_min 25`).
2. `python3 build.py` regenera `index.html` desde `captions.json`.
3. `npx hyperframes check` y `npx hyperframes render`.

`guion.txt` son las frases de subtítulo; `retime2.py` re-ancla los tiempos a las pausas del audio.
