# Reel ÁMBAR SCULPT STUDIO

Reel 9:16 (1080×1920, 30 fps, 20.06 s) montado sobre el video original de la marca, con el
**design system oficial de Ámbar** (`ambar-design-system`, entregado por el cliente).

## Qué manda aquí

El brand book de Ámbar, no el de Sarier ni el de LUXUR. Lo que cambia la forma de trabajar:

| Regla | Cómo se aplicó |
| --- | --- |
| Fondo negro cálido `#070100`, nunca `#000` | fundidos y cierre |
| Un solo acento `fuego` `#dc3023` por pieza | solo el degradé de cierre |
| Todo el texto `perla` `#fcfbf2`; secundario `perla-suave` | subtítulos, titulares, anillo |
| **Sin sombras** | los subtítulos no llevan `text-shadow`: se sientan sobre un fundido |
| **Sin iconos, sin tarjetas redondeadas, radius-0** | todo a sangre y en ángulo recto |
| `radius-boton` 14px | único redondeo: el botón QUIERO RESERVAR |
| Margen lateral `space-5` 40px | todos los bloques |
| Firma arriba, "The Ámbar Method" abajo | versalitas Sackers Gothic |

### Las cinco voces tipográficas (no se intercambian)

- `titular` — Anton, mayúsculas: "SÉ QUE ODIAS EL GIMNASIO.", "UNA RUTINA QUE TE MOTIVE", "ENCIENDE TU / ESCULPE TU".
- `editorial` — Cormorant Garamond Light, minúscula, **segunda palabra en cursiva**: "cero *resultados*",
  "única en la *ciudad*", "the ámbar *method*", "sé parte de *ámbar*".
- `caligrafia` — Pinyon Script, **una palabra emocional por pieza**, cruzando el titular: *fuego*, *fuerza*.
- `versalitas` — Sackers Gothic Medium: la firma, las etiquetas del anillo, los datos del cierre.
- `cuerpo-mayus` — Helvetica en mayúsculas: los subtítulos.

### El anillo de beneficios

Es el **único gráfico de la marca**, así que es el centro del reel (9.8–13.4 s): círculo `perla` de 1px que
se dibuja, un punto por atributo y las etiquetas por fuera. Al centro, el concepto en `editorial`.
Los seis atributos son datos reales de la marca: CALOR INFRARROJO · PILATES · FUERZA FUNCIONAL ·
BAJO IMPACTO · 45 MINUTOS · YOGA.

Debajo va el `luz-foto` (lavado de luz roja de arriba a negro) al 74% sobre el video: es el recurso que la
marca usa para teñir una foto, y deja ver el salón por debajo.

## Degradés

Solo los de `tokens.json`, siempre de rojo a negro pasando por vino y oxblood:

- `fundido-abajo` — base permanente desde y=820 para sentar el texto perla sobre el video sin usar sombras.
- `luz-foto` — el lavado del anillo.
- `luz-cierre` — resplandor `fuego` desde la esquina inferior derecha, con el texto a la izquierda sobre la
  zona oscura, exactamente como lo pide el brand book. Va con alfa: **el cierre es una capa de luz sobre el
  plano, no una lámina**, así que el video se ve hasta el último fotograma. Ningún gráfico del reel tapa la
  imagen.

## Iconos — excepción al brand book

`BRAND.md` dice: *"La marca no usa iconos. Las listas se separan con puntos medios (·) o con los puntos del
anillo."* El cliente pidió iconos, así que se usan **Material Symbols (outlined)** de Google dibujados en el
lenguaje de la marca: perla plano, sin color propio, sin sombra y al mismo grosor visual que la línea de 1px.

Están en `icons/` y se colocan con `icon()`. Dónde aparecen:

| Beat | Icono | Para qué |
| --- | --- | --- |
| 2 · razones equivocadas | `groups` · `timer` · `sentiment_dissatisfied` | tres motivos que se tachan uno a uno |
| 3 · cero resultados | `trending_flat` | la flecha plana del progreso que no se mueve |
| 4 · una rutina | `calendar_month` | la rutina |
| 5 · anillo | `device_thermostat` · `sports_gymnastics` · `fitness_center` · `spa` · `timer` · `self_improvement` | un símbolo por atributo, en un anillo interior |
| 6 y 8 · ubicación | `location_on` | Pinares, Pereira |
| 7 · enciende tu fuego | `local_fire_department` | late con la caligrafía |

Para volver al brand book puro basta con borrar las llamadas a `icon()` en `build.py`.

## Datos de marca

Salieron del propio video (en los últimos segundos aparece el perfil de la marca en pantalla) y del
design system: **@ambarsculptstudio · ÁMBAR | Hot Pilates & Sculpt · Pinares, Pereira · The Ámbar Method™**.
El original termina con una captura del perfil en vista de administrador ("Your dashboard", "Edit profile").
Se deja a la vista, porque el cierre ya no tapa el plano; si se quiere esconder, hay que recortar esa cola
del video en vez de poner una lámina encima.

## Subtítulos

Alineación forzada sin ASR: espeak-ng es-419 por línea → MFCC → DTW contra el audio real, y después se
reanclan a las pausas que detecta `silencedetect`. **No se cortaron pausas**: son 20 s de anuncio y los
cortes romperían el ritmo de la locución y los planos de recurso.

Cuatro de las ocho líneas no llevan subtítulo porque las dice la tipografía grande (1, 4, 6 y 8).

## Regenerar

1. `python3 build.py` → `index.html`
2. `npx hyperframes check`
3. `../reel-tools/finish.sh reel-ambar ambar` → master + copia Instagram

El tema `ambar` vive en `reelkit.py` (`THEMES["ambar"]`) con los tokens oficiales; las fuentes de la marca
están en `public/fonts/` (Sackers Gothic Light/Medium/Heavy, Anton, Pinyon Script, Cormorant Garamond).

## Nota

`ambarsculptstudio.com` está bloqueado por la política de red de este entorno, así que nada se tomó de la
web: todo viene del paquete de design system y del propio video.
