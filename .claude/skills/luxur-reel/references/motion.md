# Motion graphics: recetas y trampas

El motor es `reelkit.py` en la raíz del repo (HyperFrames + una sola línea de tiempo de GSAP
pausada). Un `build.py` solo declara contenido y beats; el motor arma el HTML.

## Cómo se mueve LUXUR

El sistema de LUXUR tiene curvas suaves y píldoras redondas, así que **sí rebota**, pero poco:
`back.out(1.6)` para entradas, `power2.out` para texto, `draw` para reglas y trazos. Entradas de
0,4–0,5 s y *stagger* de 0,25–0,30 s entre hermanas. Nada dura más de 0,6 s: un reel de 50 s tiene
que dejar sitio a la locución.

El `punch_cam` (un empujón de 1,03–1,04 sobre el plano) marca el golpe de cada beat. Uno por
capítulo, nunca más.

## El catálogo que ya está probado

| Recurso | Para qué sirve | Cómo se hace |
| --- | --- | --- |
| **Tarjeta de capítulo** | estructurar el reel en 01 / 02 / 03 | superficie beige + píldora de número + titular + regla que se dibuja |
| **Fila de píldoras** | enumerar atributos (fits, usos, beneficios) | entran con `back.out`, *stagger* 0,30 |
| **Píldora marcada** | "este es el que importa" | una segunda píldora en tinta **dibujada encima** de la beige, mismo sitio, solo cruza su alfa |
| **Muestras** | escalas de color o de talla | rectángulos de 250×44 con la etiqueta debajo, **dentro** de la superficie |
| **Escala / barra** | una magnitud que crece | `draw` sobre un `path`, o un `rect` que crece en `attr.width` |
| **Tarjeta que crece** | una ficha que se va llenando | tween de `attr.height` del `rect`, para que no haya hueco muerto mientras está medio vacía |
| **Contador de progreso** | tres puntos en una lista | tres barras que se rellenan; el sistema pide barra, nunca un spinner circular |
| **Ficha de producto** | el momento comercial | píldora de etiqueta, nombre en 300 grande, regla punteada, atributos |

## Cuatro trampas que cuestan un render entero

**1. No animes `fill` ni `scale` sobre un `<g>` de SVG.** GSAP recalcula el origen del grupo con su
*bounding box* en el momento de construir la línea de tiempo; si el grupo aún no tiene caja, el
origen cae en (0,0) y el elemento se desplaza — y puede llevarse por delante a sus hermanos.
Dibuja los dos estados y cruza su alfa.

**2. No animes `autoAlpha` sobre un elemento `.clip`.** El framework gestiona la visibilidad de los
clips; `autoAlpha` escribe `visibility` además de `opacity` y `hyperframes check` lo rechaza. Si
necesitas fundir un clip entero, mete el contenido en un hijo y anima el hijo.

**3. Cuidado con fundir un elemento y que se apaguen sus hermanos.** Si una píldora se oculta con
`autoAlpha` y sus hermanas comparten tweens cercanos, se apagan con ella. Prefiere dibujar el
estado nuevo encima a esconder el viejo.

**4. Solo el primer `fromTo` sobre la cámara puede fijar el reposo.** GSAP aplica los valores de
origen al construir, no en su posición; el resto necesita `immediateRender: false`. `reelkit.py` ya
lo hace solo (`_cam_ir`), pero si escribes un tween de cámara a mano, acuérdate.

**Solape a propósito** (dos estados en el mismo sitio): marca el texto con
`data-layout-allow-overlap` o `check` lo cuenta como error.

## Subtítulos

Alineación forzada sin ASR: `scripts/alinear.sh`. Lo que hay que mirar del resultado:

- **Caracteres por segundo.** Entre 10 y 26 la línea cuadra con el audio. Fuera de ahí, repártela
  distinto en `guion.txt` y vuelve a alinear.
- **Pausas largas dentro de una línea.** Más de un segundo casi siempre es un corte de sección:
  mueve la frontera a mano al final de la pausa.
- **Nunca tres renglones.** Entran en la interfaz de Instagram. Parte la frase en dos líneas de
  subtítulo en `guion.txt` — es más limpio que bajar el cuerpo.
- **La palabra caliente va en píldora**, una por línea.

Las líneas que ya dice una tarjeta en pantalla no llevan subtítulo (`card_frags`): leer lo mismo
dos veces a la vez se ve descuidado.

## Dónde va cada cosa

`scripts/bandas.py` mide el plano antes de diseñar. Manda lo que diga el peor fotograma, no la
media: un cuaderno crema o el suelo de la tienda cruzando la banda tiran el contraste aunque el
promedio parezca cómodo.

- Subtítulos: la banda limpia más baja que termine **antes de y=1650** (ahí empieza la interfaz de
  Instagram).
- Gráficos: la franja de arriba que nunca cruza la persona. En un plano entero suele ser
  `y 140..400`; en un plano medio llega a `y 560`. Compruébalo con un contact sheet, no solo con la
  luminancia, y ten en cuenta que ella se mueve.
- Nada por encima de `y=140`: ahí está la interfaz de Instagram.

**Ningún gráfico tapa la pantalla completa** — es la regla propia de LUXUR — y la persona no queda
tapada en ningún momento, tampoco en el cierre.
