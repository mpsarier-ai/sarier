# Sarier · reel "¿Por qué soñamos?" (sobreajuste y sueños)

Composición HyperFrames: subtítulos cinéticos, 3 statements blancos por capas, 6 gráficos de línea encadenados
(curva de sobreajuste, cerebro, el mismo día en bucle, ayer/mañana, noche imposible, datos de entrenamiento).
Fuente: original HEVC 1080×1920 a 25 fps (la composición fija `data-fps="25"`). Duración 61.44 s.

## Renders finales
- `renders/sonamos-final.mp4`            master · 1080×1920 · 25 fps · 85 MB
- `renders/sonamos-final-instagram.mp4`  copia para Instagram · 3 Mbps · 24 MB

## Regenerar
1. Pon el original convertido en `public/input-video.mp4` (ver el LEEME del reel 1; usa `-g 25 -keyint_min 25`).
2. `python3 build.py` regenera `index.html` desde `captions.json`.
3. `npx hyperframes check` y `npx hyperframes render`.

`guion.txt` son las frases de subtítulo; `align.py` + `retime2.py` alinean el guion al audio y re-anclan los tiempos a las pausas.
