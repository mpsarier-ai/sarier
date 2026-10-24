# Reel LUXUR — RESTOCK (Q4 Trimestre Dorado)

Reel 9:16 (1080×1920, 30 fps, 20,95 s) sobre el video original `Restock video.mov` (llegó por
el chat, no por release). Design system **Q4 Trimestre Dorado**: papel `#FBFAF7`, cream
`#EDEBE6`, blush `#EECDCC`, tinta `#1C1C1C`, `--mute #5A5A5A`, `--soft #E6E2DC` y el dorado
`#8C7B5E` **una vez por pantalla**. Poppins 300 para los nombres, 600 en versalitas para los
cintillos. Ningún gráfico tapa la pantalla completa y ella no queda tapada en ningún momento.

## El plano manda

Dos encuadres distintos en el mismo reel, y eso cambió la arquitectura respecto a `reel-luxur-jean`:

- **Planos hablados (0–5,8 s y 19,9–21 s).** Plano medio: ella ocupa el centro y la izquierda de
  arriba abajo y **su cabeza entra en la franja y 140–400**, así que ahí no cabe ninguna tarjeta.
  La única pared libre es la derecha, encima de su hombro: `x 740–1040, y 300–550`. Su pelo
  llega a x≈700 a la altura del hombro; su mano con el objeto, a x≈760 pero por debajo de y 700.
- **Fitting room (5,8–19,9 s).** Plano entero, ella centrada. La columna derecha
  `x 664–1040, y 300–930` queda limpia en los cuatro looks: el hombro más alto llega a y≈980
  (t=8,0) y el codo más abierto a x≈807 pero a y≈1450.
- `bandas.py` dio "ninguna tinta plana" en las 15 bandas (el fondo va de 14 a 255 de
  luminancia), así que los subtítulos van **en blanco con halo** en `y 1420` y terminan antes
  de la cintura de Instagram (1600). El halo se subió un punto respecto al reel anterior porque
  tres palabras sobre la pared clara daban 2,8–2,99:1; con el halo nuevo pasan 38/38 AA.

Cortes del plano (detección de escena a 0,12): 5,80 · 10,17 · 13,77 · 16,90 · 18,70 · 19,87.
Los dos últimos cortes del fitting room son el mismo jean (frente y espalda).

## Estructura

| Beat | Pieza | Qué hace |
| --- | --- | --- |
| **0,15–5,70** | hook en la pared derecha | píldora `RESTOCK` blush, "de vuelta" en Poppins 300 56px, regla dorada 44×4. **`LUXUR` entra solo en 3,28–5,10, cuando lo dice** |
| **5,80–10,17 · 01** | LOW WIDE azul oscuro · $199.000 | ficha con la foto de Shopify, tallas XS–XL, barra 1/4 |
| **10,17–13,77 · 02** | LOW WIDE dirty washed · $199.000 | tallas XS–XL, barra 2/4 |
| **13,77–16,90 · 03** | WIDE LEG green toned · $189.000 | tallas XS–L, barra 3/4 |
| **16,90–19,87 · 04** | WIDE LEG green vintage · $189.000 | tallas XS–M, barra 4/4 |
| **19,92–20,95** | cierre sobre el plano | regla dorada + píldora `LINK EN BIO` en papel, sin lámina |

La ficha de look: `x 664, y 300, 376×630`, radio 28; píldora de número a `y+26`; foto 280×350
(4:5, radio 18, `xMidYMid slice`) de `y+84` a `y+434`; nombre en 300 44px a `y+486`; lavado y
precio en `--mute` a `y+518`; chips cream de talla a `y+540`; contador de cuatro barras a `y+600`
con la activa en dorado (es el único dorado de esa pantalla). Un `punch_cam` de 1,03 por look.

## Regla nueva de la marca (24 oct 2026)

**El logo de LUXUR no va en la edición salvo cuando lo dicen en el audio.** Y cuando lo dicen,
va en **Montserrat SemiBold sin espaciado**. Por eso:

- se quitó el wordmark pequeño de las fichas y del cierre (la primera versión lo llevaba, como
  `reel-luxur-jean`);
- en 3,28–5,10 ("…los favoritos de LUXUR") aparece `LUXUR` en Montserrat 600 / tracking 0 en la
  tarjeta del hook, y la palabra del subtítulo (`#r04w7`) se compone igual (`.rail .w.brand`).

Esta regla también está en `.claude/skills/luxur-reel/SKILL.md`.

## Datos y de dónde salen

- **Guion**: lo pasó MP por el chat (transcripción de Instagram). "Luxor" → LUXUR. Arranca en
  "los volvieron a pedir" porque así llegó; si el audio empieza con "ustedes", la primera línea
  queda corta pero no inventamos texto.
- **Productos**: verificados en Shopify el 24 oct 2026 (`search_products`,
  `product_type:JEAN AND status:active`):
  - `9430913679578` JEAN LOW WIDE FIT TIRO BAJO ANCHO AZUL OSCURO · $199.000 · XS 15 · S 19 · M 18 · L 24 · XL 4
  - `9435413315802` JEAN LOW WIDE FIT TIRO BAJO ANCHO AZUL DIRTY WASHED · $199.000 · XS 16 · S 18 · M 31 · L 19 · XL 3
  - `9446837092570` JEAN WIDE LEG FIT GREEN TONED AZUL MEDIO · $189.000 · XS 4 · S 5 · M 7 · L 4
  - `9395011944666` JEAN WIDE LEG FIT GREEN VINTAGE WASH AZUL CLARO · $189.000 · XS 8 · S 11 · M 17
  Las tallas en los chips son las que tenían stock ese día; si se agota una, hay que regenerar.
- **Orden de los looks**: el que dio MP (azul oscuro → dirty → green toned → green vintage),
  comprobado contra los cortes: el DIRTY WASHED es el gris oscuro con rotos (su foto de Shopify
  también es gris oscuro), el green toned es el azul-verdoso y el vintage el verde claro.
- **Fotos de Shopify**: `cdn.shopify.com` está bloqueado desde el contenedor. Se abrieron en el
  Chrome de MP (Claude in Chrome) y se capturaron a 980×1225 con el zoom del extension, que
  guarda en disco; luego se bajaron a 640×800 JPEG. Son las `featuredMedia` de cada producto.
  Las cuatro llevan foto por coherencia, aunque MP pidió explícitamente las dos LOW WIDE.

## Subtítulos

Sin ASR (huggingface bloqueado) y con música debajo de la voz, así que `silencedetect` no
encontró ninguna pausa y `snap.py` no pudo reanclar: **manda el DTW** (`captions.json` =
`captions.dtw.json`). Trece líneas, 17–26 car/s, ninguna por debajo de 0,73 s. Palabras
calientes en píldora cream: vuelta · stock · vuelven · tallas · octubre · Friday · bio.
`alinear.sh` del skill falla con `pipefail` cuando no existe `orig.mp4`; aquí va parcheado
(`SRC=orig.mov`).

## Regenerar

1. Poner el original como `orig.mov` y codificarlo: `ffmpeg -i orig.mov -c:v libx264 -preset slow
   -crf 16 -g 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709
   -movflags +faststart -c:a aac -b:a 192k public/input-video.mp4`
2. `python3 build.py` → `index.html`
3. `HYPERFRAMES_BROWSER_PATH=<chromium> hyperframes check` (0 errores, 38/38 AA; las
   advertencias de tipo bajo 28 px son los chips y cintillos, y las de "line unread" son el
   ritmo de la locución)
4. `hyperframes render` → master crf 17 (31 MiB) y copia Instagram crf 24 / 3000k (8,2 MiB)

El tema `luxur` vive en `reelkit.py`; las fuentes en `public/fonts/`.
