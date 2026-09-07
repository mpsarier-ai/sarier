# Sarier · reel "¿Puede la IA hacernos pensar más?"

Composición HyperFrames lista. El preview se hizo con un proxy de 576×1024.
Para el render final con tu original, sin perder calidad:

## 1. Requisitos (una sola vez)
- Node 22+  → https://nodejs.org
- FFmpeg    → Mac: `brew install ffmpeg`

## 2. Pon el original en su sitio
Desde esta carpeta, con tu archivo original (el pesado) — re-encodea con keyframes densos
(obligatorio: sin esto el video se congela bajo los gráficos). `-crf 18` es visualmente sin pérdida:

    ffmpeg -i /ruta/a/tu-original.mp4 -c:v libx264 -crf 18 -g 30 -keyint_min 30 \
      -pix_fmt yuv420p -movflags +faststart -c:a aac public/input-video.mp4

El video debe durar lo mismo que el proxy (73.98 s). Si el original es más largo o más corto,
avísame y reajusto la alineación.

## 3. Verifica y renderiza
    npx hyperframes check
    npx hyperframes render

El MP4 sale en `renders/`. 1080×1920, 30 fps, H.264, listo para Instagram.

## Qué hay aquí
- `index.html`     la composición (video + subtítulos cinéticos + 3 statements + 10 gráficos de línea)
- `captions.json`  los tiempos de cada frase (anclados a las pausas del audio; `retime.py` los regenera)
- `guion.txt`      el guion en líneas de subtítulo — edita y corre `python3 build.py` para regenerar
- `build.py`       generador de `index.html` a partir de `captions.json`
- `public/fonts`   Archivo (respaldo oficial del sistema Sarier); en Mac usará Helvetica Neue
- `public/vendor`  GSAP local

## Renders finales (desde el original HEVC 1080×1920)
- `renders/sarier-reel-final.mp4`            master · 1080×1920 · 30 fps · ~9.9 Mbps · 87 MB
- `renders/sarier-reel-final-instagram.mp4`  copia para Instagram · 3 Mbps · 27 MB
