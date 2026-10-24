---
name: luxur-reel
description: Edita un reel 9:16 de LUXUR a partir de un video crudo, con motion graphics, subtítulos alineados y el design system Q4 Trimestre Dorado. Úsala SIEMPRE que la persona suba, mencione o pida editar un video, reel, clip o historia de LUXUR; cuando diga "edítame este video", "móntame el reel", "ponle subtítulos", "ponle gráficos" o "hazle motion" sobre material de la marca; cuando pase una transcripción o un guion para un video de LUXUR; cuando pida la ficha de un producto, una comparativa de fits o una escala de colores en movimiento; o cuando pida rehacer, retocar o reencodear un reel ya montado. También aplica si solo nombra Q4, trimestre dorado, Black Friday o la campaña de fin de año y hay un video de por medio. No esperes a que diga "HyperFrames", "reelkit" ni "skill".
---

# Reel de LUXUR

Convierte un video de cámara (normalmente alguien hablando a cámara en la tienda) en un reel 9:16
de 1080×1920 con subtítulos cinéticos y motion graphics, montado con HyperFrames + GSAP sobre el
plano original y con el design system de LUXUR en su variante **Q4 Trimestre Dorado**.

El motor es `reelkit.py`, en la raíz del repo: un `build.py` solo declara contenido y beats. Antes
de escribir el primer `build.py` lee **`references/motion.md`** (recetas, trampas de GSAP y dónde
va cada cosa) y **`references/q4-trimestre-dorado.md`** (tokens, componentes y la geometría ya
calibrada).

## Las cuatro reglas que no se negocian

1. **El design system es el de LUXUR, no el de otra marca.** El tema `luxur` vive en `THEMES` de
   `reelkit.py`; la paleta de Q4 está en la referencia. Si la pieza es de otro trimestre, usa
   LUXUR a secas y deja fuera los tostados.
2. **Ningún gráfico tapa la pantalla completa.** Es la regla propia de la marca.
3. **La persona nunca queda tapada**, tampoco en el cierre. Si el cliente te ve a ti en vez de
   verse a ella, el reel está mal montado.
4. **El logo de LUXUR no va en la edición salvo cuando lo dicen en el audio.** Nada de wordmark
   fijo en las tarjetas ni en el cierre. Cuando lo dicen, entra justo en ese momento y se compone
   en **Montserrat SemiBold (600) sin espaciado** (`letter-spacing: 0`), tanto en el gráfico como
   en la palabra del subtítulo. Regla de MP del 24 oct 2026; `reel-restock` es el ejemplo.

## El recorrido

### 1. Conseguir el material

El video llega como release en `mpsarier-ai/sarier`. Si el release está publicado, basta
`curl -sSL` sobre la URL de descarga; si está en **borrador** no tiene tag y hay que bajarlo por la
API: `gh api -H "Accept: application/octet-stream" repos/mpsarier-ai/sarier/releases/assets/<id>`.
`gh api repos/mpsarier-ai/sarier/releases` da los ids.

Trabaja siempre en el *scratchpad*, nunca en el repo: el `.mov` original pesa cientos de MB.

### 2. Leer el plano antes de diseñar nada

Esto es lo que más decisiones ahorra, y es lo primero:

```bash
python3 <skill>/scripts/bandas.py orig.mov
ffmpeg -i orig.mov -vf "select='not(mod(n,105))',scale=200:356,tile=7x2" -frames:v 1 sheet.jpg
```

`bandas.py` dice qué tinta aguanta cada franja **en su peor fotograma**; el contact sheet dice por
dónde se mueve ella. De ahí salen las dos decisiones de montaje: dónde van los subtítulos y de qué
color, y qué franja queda libre para los gráficos. Mira el contact sheet de verdad: la luminancia
sola no te dice que hay un cuaderno crema cruzando la banda.

Los planos de LUXUR suelen ser enteros y dentro de la tienda, con el fondo moviéndose entre 16 y
242 en el mismo reel. Cuando ninguna tinta plana aguanta, la salida es la de la marca: **apoya el
texto en una superficie beige**, o blanco con halo para los subtítulos.

### 3. El guion

Lo pone el cliente, normalmente como captura de la transcripción de Instagram. **No hay ASR**:
`huggingface.co` está bloqueado por la política de red del entorno y el modelo de whisper no se
puede descargar; dilo si falta el guion en vez de inventarlo.

Pásalo a `guion.txt`, una línea por unidad de subtítulo, y aplica lo que diga el cliente sobre
errores de transcripción. Dos cosas a vigilar mientras lo partes:

- Ninguna línea debe dar tres renglones en pantalla; parte las largas en dos.
- Corrige los arranques en falso ("qué queremos priorizar, que no, que nos está") — es práctica
  normal de subtitulado — pero **no inventes ni parafrasees**, y menos un nombre de producto.

**Si en el audio hay una referencia que no reconoces, pregunta.** Los nombres de producto de LUXUR
no se adivinan: "low white" resultó ser el **LOW WIDE**. Un nombre mal puesto en pantalla es un
error de marca que paga el cliente.

### 4. Alinear

```bash
bash <skill>/scripts/alinear.sh <dir>
```

Si la voz lleva música debajo, `silencedetect` no encuentra pausas y `snap.py` no puede
reanclar: manda el DTW tal cual (`captions.json` = `captions.dtw.json`).

Revisa la salida antes de seguir: caracteres por segundo entre 10 y 26, ninguna línea por debajo de
0,55 s, y ninguna pausa de más de un segundo cayendo dentro de una línea (eso casi siempre es un
corte de sección y se ajusta a mano).

### 5. Montar

Codifica el plano a H.264 (`crf 16`) como `public/input-video.mp4` y escribe `build.py`.

Estructura que funciona para este formato, que casi siempre es una lista ("las tres cosas que…"):
hook tipográfico → un capítulo por punto, cada uno con su tarjeta numerada y su gráfico → ficha de
producto → cierre de marca sobre el plano. Las recetas de cada pieza están en
`references/motion.md`.

Los datos de catálogo —fits, precios, referencias— salen de Shopify, no de la cabeza. Si el
conector pide re-autenticación, dilo y usa lo que ya esté verificado en los `LEEME.md` de los
reels anteriores, diciendo de dónde sale.

### 6. Comprobar

```bash
python3 build.py && HYPERFRAMES_NO_TELEMETRY=1 hyperframes check
```

Hasta que no dé **0 errores** no se renderiza. El chequeo de contraste cuenta el halo de los
subtítulos, así que es más fiable que una fórmula de contraste plano.

Después, snapshots y míralos de verdad:

```bash
./reel-tools/snap.sh <dir> "1.5,4.5,9,12.5,17,20.5,..."
```

Las bandas rojas del contact sheet marcan la interfaz de Instagram. Cosas que solo se ven mirando:
una tarjeta comiéndole la frente, un hueco muerto mientras una ficha está medio vacía, una
etiqueta que cae fuera de su superficie, un gráfico que entró y no se ve.

### 7. Entregar

```bash
bash <skill>/scripts/entregar.sh <dir> <nombre>
```

Baja el crf del master hasta que entre en los 100 MiB de GitHub y el bitrate de la copia de
Instagram hasta que entre en 30 MB. Luego: carpeta `reel-<nombre>/` en el repo con `build.py`,
`guion.txt`, `captions.json`, fuentes, renders y un `LEEME.md`; commit y push a la rama de trabajo;
y la copia de Instagram al chat.

El `LEEME.md` cuenta **por qué** está montado así —qué dijo el plano, qué se midió, qué se decidió
y qué quedó pendiente—, no solo qué contiene. Es lo que permite retomarlo meses después.

## Lo que hay que decir siempre

- Si un dato no se pudo verificar (Shopify caído, un nombre de producto dudoso), dilo en la
  entrega en vez de dejarlo pasar.
- Si el master no cabe a crf 17 y bajó de calidad, dilo.
- Los releases con material del cliente quedan **públicos** en el repo: recuérdale borrarlos.
