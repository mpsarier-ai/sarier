# Reel LUXUR — las tres cosas al comprar un jean básico

Reel 9:16 (1080×1920, 30 fps, 48,98 s) sobre el video original, con el **design system de LUXUR**:
Poppins, fondo beige `#EDEBE6`, ink `#1C1C1C`, blush `#EECDCC`, píldoras y trazos finos. Se respeta
la regla propia de la marca: **ningún gráfico tapa la pantalla completa**.

## El encuadre manda la arquitectura

Este es un plano entero dentro de la tienda: ella ocupa el centro de arriba abajo y el fondo va de
**16 a 242** de luminancia según el momento (el suelo y el arco iluminado por un lado, su jean y el
mueble oscuro por otro). No hay ninguna banda donde la tinta o el blanco se lean solos.

La solución es la de la propia marca: **todo lo que va encima del plano se apoya en una superficie
beige**, que es como LUXUR pone texto sobre cualquier cosa en la tienda y en la web. Medí dónde
nunca la tapa y la única franja libre en todo el reel es **y = 140…400** (el arco del techo), así
que ahí viven las tarjetas de capítulo.

Los subtítulos van abajo (y=1440) **en blanco con halo**: con un fondo que va de 16 a 242 ninguna
tinta plana aguanta los dos extremos, y el halo es lo que hace que pasen las 21 comprobaciones
WCAG AA. Es el mismo tratamiento del primer reel de LUXUR.

## Estructura

El reel se cuenta en tarjetas de capítulo, cada una con su píldora de número:

| Beat | Tarjeta | Gráfico |
| --- | --- | --- |
| **0,1–3,7** | `3` · cosas que miro al comprar un jean básico | — |
| **3,7–10,8 · 01** | EL FIT | las tres píldoras de fit del catálogo real: Extra Low Straight · Relaxed · Wide Leg. En "el que mejor se adecue a tu cuerpo" una se marca en tinta |
| **11,1–15,2 · 02** | EL COLOR | los tres lavados, que entran uno a uno: claro · medio · oscuro |
| **15,6–30,7 · 03** | LA CALIDAD | tres píldoras de uso (día a día · salir · todo) que dan paso a las dos exigencias en blush: súper cómodo · que te dure años |
| **34,6–45,9** | LOW WIDE | píldora `COLOR MEDIO` y la escala de lavados con el medio marcado |
| **46,2–48,98** | cierre | el wordmark LUXUR sobre el plano, con regla blush y la pregunta final |

El cierre va **sobre el plano**, sin lámina: ella se ve hasta el último fotograma.

## Datos y decisiones

- **"gym" → "jean" y "kit" → "fit"** en todo el guion, como pediste.
- **El jean es el LOW WIDE**, confirmado por ti. En el audio suena "low white" y no coincide con
  ningún fit del catálogo que verifiqué antes (Extra Low Straight, Relaxed, Wide Leg), así que se
  preguntó en vez de adivinar. En pantalla va solo `LOW WIDE`: no se añade "azul oscuro" porque ella
  dice literalmente "es un color medio" y las dos cosas se contradirían en el mismo cuadro.
- **Los tres fits de la píldora son los del catálogo vivo** (los mismos que se verificaron en
  Shopify para `reel-anto`), no inventados.
- **Los tres lavados no son colores de marca** sino producto: el oscuro `#2E374F` está muestreado
  del jean que ella lleva puesto y los otros dos salen del mismo tono aclarado.

## Dos cosas que se arreglaron en el montaje

- **El resaltado del fit.** Animar un `fill` o una escala sobre un `<g>` de SVG hace que GSAP
  recalcule el origen del grupo y la píldora se desplazaba, además de apagar la siguiente. Ahora la
  píldora marcada se dibuja **encima** de la beige con la misma geometría y solo cruza su alfa.
  Van marcadas con `data-layout-allow-overlap` porque comparten sitio a propósito.
- **El ancho de las píldoras.** Poppins en versalitas con 0.18em de tracking mide ~0,92em por
  carácter, no 0,80: con la estimación vieja las tres píldoras de fit se montaban una sobre otra.

## Subtítulos

Alineación forzada sin ASR (`huggingface.co` está bloqueado) y sin el binario `espeak-ng` (no está
en el contenedor): `espeak_say.py` llama a `libespeak-ng` por ctypes, `align.py` hace MFCC + DTW
contra el audio real y `snap.py` pega las fronteras a las pausas de `silencedetect`. Siete de las
veinte fronteras cayeron sobre una pausa real y ninguna línea baja de 0,55 s.

**No se cortaron pausas.** Siete de las 21 líneas no llevan subtítulo porque las dice una tarjeta.

## Regenerar

1. `python3 build.py` → `index.html`
2. `hyperframes check` (0 errores, 21/21 WCAG AA)
3. `../reel-tools/finish.sh reel-lux2 luxur-jean-basico`

El tema `luxur` vive en `reelkit.py` (`THEMES["luxur"]`) y las fuentes en `public/fonts/`.
