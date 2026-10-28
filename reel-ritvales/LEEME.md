# Reel LUXUR — tres outfits para Ritvales (Q4 Trimestre Dorado)

Reel 9:16 (1080×1920, 30 fps, 55,6 s) montado sobre el video original `Ritvales_video_.mov`, que
llegó por el chat y no por release. Usa el design system **Q4 Trimestre Dorado**: papel `#FBFAF7`,
cream `#EDEBE6`, blush `#EECDCC`, tinta `#1C1C1C`, `--mute #5A5A5A`, `--soft #E6E2DC` y el dorado
`#8C7B5E` **una vez por pantalla**. Los titulares y valores van en Poppins 300, y los cintillos y
etiquetas en 600 versalitas. Ningún gráfico tapa la pantalla completa, ella no queda tapada en
ningún momento y el logo de LUXUR solo aparece cuando lo dicen.

Ritvales es el festival de música electrónica de Medellín (edición 2026: 31 oct – 1 nov, Parque
Norte). En pantalla va solo el nombre, porque ella no dice fechas.

## El plano manda

Hay dos encuadres, separados por cortes duros (detección de escena: 13,07 · 23,40 · 35,17 · 52,50):

- **Plano medio hablado (0–13,07 s y 52,5 s–fin).** Su cabeza llega a y≈362 cuando se acerca a
  cámara (t≈10). Por eso las tarjetas de esta parte miden **184** de alto (y 150–334), y el
  `punch_cam` que había en "apoteósica" se quitó porque le subía la cabeza contra la tarjeta.
- **Plano entero en la tienda (13,07–52,5 s).** La cabeza no sube de y≈640, así que la ficha del
  outfit puede crecer hasta y≈418 con mucho aire.
- `bandas.py` no encontró ninguna tinta plana que aguante a partir de y 720 (el fondo va de 0 a 255).
  Los subtítulos van **en blanco con halo** en y 1420. El halo se subió un punto respecto a
  `reel-restock`, porque dos palabras sobre la pared clara daban 2,77–2,82:1. Ahora pasan 37/37 AA.

## Estructura

| Beat | Pieza | Qué hace |
| --- | --- | --- |
| **0,10–6,85** | octubre · Ritvales | píldora blush `OCTUBRE` + "un mes lleno de eventos"; "Ritvales" en 300 cuando lo dice (3,14) con la regla dorada 44×4; "para los amantes de la música electrónica" a la derecha |
| **6,85–13,02** | 3 outfits · todos en LUXUR | entra cuando dice "tres outfits" (en la primera versión entraba en 5,85 y quedaba un segundo vacía). "3" en 300 a 140 px. **`LUXUR` en Montserrat 600 / tracking 0 entra en 9,05, cuando lo dice.** Píldoras regia · bella · apoteósica (esta última en dorado, el único de la pantalla) |
| **13,07–23,30 · 01** | las arriesgadas | BODY · MAI PETIT → JEAN · negro + píldora `SÚPER RITVALUDO` |
| **23,36–35,15 · 02** | monocromático | JEAN · cruces negras → TOPCITO · MAI PETIT + píldora `LAS MANGAS` |
| **35,20–51,80 · 03** | mi favorita | BODY · MAI PETIT + `LA ESPALDA` → JEAN · **LUXUR** (wordmark, porque lo dice) + `CON BRILLITOS` |
| **51,90–fin** | cierre | regla dorada, "¿cuál fue tu favorito?" en 300, píldoras 01 · 02 · 03 y `COMÉNTANOS O DM` |

La ficha del outfit es una **tarjeta que crece**: cabecera de 128 (píldora del número en tinta, titular
en 300 54 px y un contador de tres barras con la activa en dorado y las anteriores en `--line`).
Luego pasa a 202 con la primera prenda y a 268 con la segunda, a medida que ella las nombra, para
que no quede hueco vacío. La píldora de detalle va en la misma fila, detrás del valor. Hay un
`punch_cam` de 1,03 por outfit.

## Datos y decisiones

- **Guion**: lo pasó MP por el chat. Lo que corregí:
  - **"rituales" → "Ritvales"** donde habla del festival ("entre ellos Ritvales", "apoteósica en
    Ritvales"); MP confirmó que Ritvales es el festival.
  - **"súper ritualudo" → "súper ritvaludo"**: un juego de palabras con el nombre del festival.
    **Pendiente de confirmar con MP** cómo lo quiere escrito.
  - "Luxur" → LUXUR.
  - No se tocó nada más.
- **Prendas**: en pantalla va solo lo que ella dice (tipo de prenda y marca o detalle), **no el modelo
  exacto**. En Shopify hay 80 productos MAI PETIT, varios bodies rojos y negros parecidos, y adivinar el
  modelo desde el video sería un error de marca. Si MP pasa los nombres, se pueden añadir en la fila.
- **LUXUR solo cuando lo dicen** (regla del 24 oct 2026). Lo dicen tres veces: en 9,05 entra en
  la tarjeta de "3 outfits" y en 44,75 en la fila del jean del outfit 03. En la de 18,25 ("lo pueden
  encontrar aquí en LUXUR") va solo en el subtítulo. Cuando la palabra sale en el subtítulo se
  compone igual (`.rail .w.brand`, Montserrat 600 sin espaciado).
- **No se subtitula lo que ya dice una tarjeta**: líneas 3, 6, 8, 9, 15, 29 y 30.

## Subtítulos

Sin ASR (los modelos no se pueden descargar desde aquí) y con la voz sobre música, así que
`silencedetect` solo encontró pausas en 4 de las 29 fronteras. Manda el DTW de `alinear.sh`, con
dos fronteras movidas a mano a los cortes de plano: 9→10 en 13,07 y 20→21 en 35,20. Son 30 líneas
de 11–31 car/s; ella habla rápido, y ninguna baja de 0,9 s. El `alinear.sh` del skill sincronizado
todavía tiene el fallo de `pipefail` cuando no existe `orig.mp4`; aquí se resolvió con un enlace
`orig.mp4 → orig.mov`. La versión del repo ya lo trae corregido.

## Regenerar

1. Poner el original como `orig.mov` y codificarlo: `ffmpeg -i orig.mov -c:v libx264 -crf 16 -g 30
   -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart
   -c:a aac -b:a 192k public/input-video.mp4`
2. `python3 build.py` → `index.html`
3. `HYPERFRAMES_BROWSER_PATH=<chromium> npx hyperframes@0.8.31 check` (0 errores, 37/37 AA; los
   avisos que quedan son de tamaño de archivo y densidad de pista)
4. `entregar.sh ritvales luxur-ritvales` → master y copia Instagram en `renders/`
