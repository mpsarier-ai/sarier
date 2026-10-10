# Reel daniblooming 2 — beneficios del journaling

Reel 9:16 (1080×1920, 30 fps, 98,6 s) sobre el video original, con el **design system de
daniblooming**. Misma gramática que `reel-daniblooming/`: los dos reels se leen como una serie.

## Lo que cambia respecto al primero: el encuadre está al revés

| | reel 1 (puf blanco) | reel 2 (silla mint) |
| --- | --- | --- |
| franja alta (y<620) | 210–225 | **211–217** |
| franja baja (y≈1500) | 204–219 | **46–50** |
| subtítulos | tinta café, y=1404 | **papel, y=1500** |

La mampara esmerilada deja arriba muy claro, así que los gráficos siguen en tinta café ahí. Pero
abajo la silla, el pantalón y el suelo son oscuros, así que los subtítulos van en **papel**.

Dos cosas se midieron, no se supusieron:

- **La banda de subtítulos.** En y=1392 y en y=1440 el **cuaderno color crema** le pasa por detrás
  y el papel cae a 1,4:1. En y=1500 el plano se mantiene entre 46 y 50 durante todo el video, y ahí
  el papel da ~9,8:1 sin caja y sin sombra.
- **El largo de las líneas.** Para que ninguna frase llegue a tres renglones y se meta en la
  interfaz de Instagram, las dos frases más largas van partidas en dos líneas en `guion.txt`
  ("porque es donde empiezo el día / soltando todo lo que tengo en la cabeza" y "porque nos permite
  ver más allá / del nudo mental que tenemos en la cabeza").

## Beats

1. **0–6,3** hook: "desde muy chiquita / **escribo**", con dos flores flotando.
2. **9,2–11,6** "un antes / y un después".
3. **11,6–18,1** **me permite**: tres tarjetas de papel con flor que entran una a una —
   aterrizar ideas · estar más clara · desenredar nudos mentales.
4. **18,3–21,0** **gigantes → pequeñas**: un círculo punteado grande que se encoge hasta un punto
   naranja.
5. **21,4–24,3** dos píldoras: por dónde empezar · cómo me siento.
6. **26,9–30,9** "el journaling / es mi momento".
7. **30,9–35,2** tres píldoras: mi rutina · mi ritual sagrado · mi momento de presencia.
8. **35,3–39,2** **el nudo mental**: una maraña que se dibuja a mano, se suelta y se convierte en
   una línea recta punteada que termina en la flor. Es el gráfico que define este reel.
9. **42,3–47,3 · la pregunta.** El único hueco grande del audio son los 2,3 s de silencio en
   42,09–44,42: la tarjeta "¿cuál es / la diferencia?" entra justo ahí, en el silencio.
10. **52,4–57,3** claridad · certeza · luces, escalonadas y giradas como las tarjetas del sistema.
11. **57,4–61,4** la tarjeta llena de renglones que se vacía: "todo en la cabeza" → "nos lo sacamos".
12. **61,6–75,9** **a mano vs digital**: dos fichas de papel; la de "a mano" con hairline naranja y
    flor, la de "digital" apagada. En "perspectiva" las dos se abren en ángulo. Cierra con las
    píldoras "qué sí" (rellena) y "qué no" (contorno).
13. **76,4–82,3** tres flores que abren en secuencia sobre "tranquilidad".
14. **83,0–92,6** la tarjeta del **Journal Claridad**, el mismo componente que en el reel 1.
15. **96,2–98,6** cierre sobre el plano: flor, wordmark y @daniblooming, con *slow push* y un
    fundido de 0,45 s. Ella se ve hasta el último fotograma.

Catorce de las 44 líneas no llevan subtítulo porque las dice la tipografía o una tarjeta.

## Subtítulos

Igual que en el reel 1: sin ASR (`huggingface.co` está bloqueado) y sin el binario `espeak-ng`
(no está en el contenedor). `espeak_say.py` llama a `libespeak-ng` por ctypes, `align.py` hace
MFCC + DTW contra el audio real y `snap.py` pega las fronteras a las pausas de `silencedetect`
solo cuando no deja la línea ilegible.

Dos correcciones a mano sobre el resultado automático:

- **La pausa de 2,33 s antes de la pregunta** (42,09–44,42). `snap.py` no la aplicaba porque
  recortaba la línea por debajo del 70 % de su duración DTW, pero una pausa tan larga manda: la
  pregunta empieza en 44,42.
- **Un arranque en falso** del transcript ("qué queremos priorizar, que no, que nos está.") se
  limpió a "qué queremos priorizar y qué no", práctica normal de subtitulado.

**No se cortaron pausas.**

## Regenerar

1. `python3 build.py` → `index.html`
2. `hyperframes check` (0 errores, 23/23 WCAG AA)
3. `../reel-tools/finish.sh reel-dani2 daniblooming2`

El tema `daniblooming` vive en `reelkit.py`; las fuentes en `public/fonts/` y los logos en `brand/`.
