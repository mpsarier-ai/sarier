# Reel daniblooming — tres cosas que cambiaron

Reel 9:16 (1080×1920, 30 fps, 58,25 s) sobre el video original, con el **design system de
daniblooming** (`mpsarier-ai/daniblooming`), no con el de ninguna otra marca.

## De dónde sale el sistema

Del propio repo de la marca: el `:root` y el CSS de `index.html` y `bloom-reset.html`.
No se inventó ningún color ni ninguna fuente.

| Token | Valor | Dónde se usa en el reel |
| --- | --- | --- |
| `paper` | `#FFFAF3` | tarjetas y páginas |
| `cream-l` | `#FDF3EA` | degradé de las tarjetas |
| `ink` | `#3A2418` | subtítulos, titulares, numerales |
| `ink-soft` | `#7A5C48` | textos secundarios y renglones |
| `orange` | `#E97C41` | píldoras, hairlines, flores, barras de progreso |
| `pink` | `#E18C8F` | fin del degradé de las píldoras |
| `rose` | `#E2B8BC` | pétalos de la flor |
| `blue` | `#B9C8FF` | uno de los blobs del fondo |

**Tipografía:** Alegreya itálica (800 titulares y numerales, 500 los sub) y Poppins 300/400/500
para la interfaz. Los `.woff2` de Alegreya salen de `@fontsource/alegreya`; Poppins viene del mismo
paquete que ya usaba LUXUR.

**Componentes, los de la marca y no otros:**

- Tarjeta de papel translúcida con hairline naranja y esquinas de 24–28 px, girada medio grado.
- Píldora de 99 px con el degradé naranja→rosa.
- Líneas punteadas naranja al 25–45 % como separador y como conector.
- La **flor de seis pétalos** (seis elipses rx7/ry13 giradas cada 60°, rose, centro naranja): está
  copiada tal cual de `.svg-flower` en `bloom-reset.html`. Es el único ornamento de la marca.
- Blobs de color desenfocados: aquí son tres gradientes radiales que derivan lento sobre el plano
  y le quitan el frío al blanco del set.
- Los logos (`logo1.png`, `logo2.png`) se copian, no se redibujan.
- **Aquí sí rebota**: el sistema usa `cubic-bezier(.34,1.56,.64,1)`, así que las entradas son
  `back.out(1.7)`. (Al revés que FOLD, donde nada rebota.)

## Dos desvíos del sistema, por contraste

El sitio escribe las píldoras en **blanco sobre naranja**: eso da **2,8:1**, y a tamaño de reel no
se lee. La píldora conserva el degradé de la marca y toma su propia tinta café (5,2:1). Lo mismo
con `.card-sub`, que en el sitio va en naranja: sobre la tarjeta translúcida daba 2,6:1, así que el
subtítulo de la tarjeta usa `ink-soft` y el naranja se queda en la píldora, las flores y los
hairlines. Con eso pasan **22/22** las comprobaciones WCAG AA de `hyperframes check`.

## Cómo manda el encuadre

Plano único: ella sentada en un puf blanco contra una cortina clara. Medí la luminancia por bandas
(146–225 sobre 255, todo claro), así que:

- **Los gráficos viven arriba**, entre y=180 y y=560, que es cortina limpia y queda por debajo de
  la franja donde Instagram pone su interfaz.
- **Los subtítulos viven abajo**, en y=1404, sobre el puf: ahí el plano mide 204–219 y la tinta café
  da 9,7:1. Sin caja y sin sombra.
- **Ella nunca queda tapada.** Ningún gráfico ocupa la pantalla completa y la tarjeta del Journal
  entra baja (300 px de alto) y **crece** a 424 cuando aparecen las filas, para no comerle la frente
  mientras está medio vacía.

## Beats

1. **0–5,1** hook en Alegreya itálica: "Tres cosas / que cambiaron", con dos flores flotando en los
   márgenes de cortina, y "y ninguna / es la que uno esperaría".
2. **5,1–18,0 · 01** el bucle de la 1 AM: un círculo naranja que se dibuja, una flecha que da dos
   vueltas y "1:00 AM / las mismas conversaciones" al centro. A los 12,9 el bucle se abre en una
   línea recta punteada que termina en la flor —lo que sí salió— y cierra con el titular
   "Lo que no sale / se repite."
3. **18,0–28,2 · 02** las ocho páginas: ocho tarjetas de papel con renglones que entran una a una
   con rebote, y en todas el mismo renglón resaltado en naranja. En "Ocho." los ocho resaltados
   laten a la vez y aparece la píldora "LA MISMA COSA".
4. **28,2–36,1 · 03** "excusas" en Alegreya itálica, una línea punteada que la tacha, la palabra
   se apaga y en su lugar florece la flor. Cierra con "Ya no puedes decir / que no sabías."
5. **37,1–46,4** el giro: tarjeta "meses evitando mirar" → conector punteado → píldora "DECISIONES".
6. **46,4–55,5** la tarjeta del Journal, que es el componente estrella de la marca y se arma por
   partes: píldora "EN EL LINK DE MI BIO" → "Journal Claridad" → separador punteado →
   "una guía de preguntas para cada noche" → "cinco minutos · espacio ilimitado" →
   las píldoras "escribas · dibujes · rayes".
7. **55,9–58,25** cierre **sobre el plano**: la flor, el wordmark y @daniblooming en el tercio
   superior, con *slow push* y un fundido de 0,45 s. No hay lámina de cierre: ella se ve hasta el
   último fotograma.

El indicador de progreso (tres barras que se rellenan, nunca un spinner) acompaña los tres puntos
de 5,0 a 36,1, y el wordmark hace de bug arriba a la izquierda hasta que entra la tarjeta.

## Subtítulos

**No había guion ni ASR.** `hyperframes transcribe` necesita bajar el modelo de whisper de
`huggingface.co`, que está bloqueado por la política de red del entorno, así que el guion lo pasó
el cliente y los tiempos se calcularon con alineación forzada.

`espeak-ng` tampoco está instalado en este contenedor, así que `espeak_say.py` llama a
`libespeak-ng.so` por ctypes (la trae el paquete `espeakng-loader` de PyPI) y hace el mismo trabajo
que el binario: una locución sintética por línea → MFCC → DTW contra el audio real (`align.py`).

Después, `snap.py` pega cada frontera a una pausa real de `silencedetect` **solo si cae a menos de
0,45 s y la frase no pierde más del 30 % de su duración**. Así quedaron 9 de 26 fronteras ancladas
a un silencio real y ninguna línea por debajo de 0,55 s. (`retime2.py`, el reanclaje automático de
los otros reels, aquí repartía las frases entre runs de habla muy cortos y dejaba líneas de medio
segundo a 49 caracteres por segundo.)

**No se cortaron pausas:** son 58 s de monólogo en los que los silencios marcan los tres puntos.

Once de las 27 líneas no llevan subtítulo porque las dice la tipografía o la tarjeta
(1, 2, 3, 8, 9, 15, 18 y las cuatro del CTA).

## Regenerar

1. `python3 build.py` → `index.html`
2. `hyperframes check`
3. `../reel-tools/finish.sh reel-dani daniblooming` → master + copia Instagram

El tema `daniblooming` vive en `reelkit.py` (`THEMES["daniblooming"]`); las fuentes están en
`public/fonts/` y los logos en `brand/`.
