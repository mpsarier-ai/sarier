# Reel LUXUR — los tres fits que más piden (Anto)

Reel 9:16 (1080×1920, 30 fps, 24,2 s) **100 % motion graphics**: del video original solo se usa el
audio. El fondo es el beige de la marca y todo lo que se ve está construido. La única imagen de
persona es el recorte de Anto al inicio.

## Cómo se arma

El fondo es un video beige `#EDEBE6` generado con ffmpeg que lleva pegado el audio del original,
así el motor de HyperFrames lo trata como cualquier otro plano y el resto del kit funciona igual.

## Datos reales del catálogo

Los números de cada ficha salen del **catálogo vivo de Shopify** (44 jeans activos), no están
inventados:

| Fit | Referencias | Unidades | Desde | Tiro |
| --- | --- | --- | --- | --- |
| Extra Low Straight | 3 | 110 | $199.000 | bajo |
| Relaxed | 19 | 584 | $199.000 | medio |
| Wide Leg | 7 | 36 | $189.000 | alto |

Los tres fits del guion existen tal cual en el catálogo, con sus metafields `custom.fit` y
`custom.tiro`.

## La guía de fit

Es el gráfico propio del reel y es un **esquema técnico, no un dibujo de un jean**: un eje con las
tres alturas de tiro, la pretina en blush que cae a la altura que le toca a ese fit, y la pierna
colgando hasta un ruedo común, con el ancho real de bota. Así los tres se comparan de un vistazo,
y al final los tres aparecen juntos en el recap.

## Lo que falta: fotos de producto

**`cdn.shopify.com` y `luxurjeans.com` están bloqueados** por la política de red del entorno, así
que no se pueden bajar las fotos de los productos. De las tres fichas, solo la segunda lleva foto
real (`fit-relaxed.png`, del release `fotos-luxur`).

Para completarlo hacen falta dos fotos más, en PNG sin fondo:
- `public/fit-extralow.png` — un **Extra Low Straight Fit**
- `public/fit-wideleg.png` — un **Wide Leg Fit**

Al dejarlas ahí basta con añadir el `photo=` de cada fit en `build.py` y volver a construir.
La otra salida es desbloquear `cdn.shopify.com` en la configuración de red del entorno; con eso
las fotos se bajan solas desde el catálogo.

## Regenerar

1. `python3 build.py` → `index.html`
2. `npx hyperframes check`
3. `../reel-tools/finish.sh reel-anto anto`
