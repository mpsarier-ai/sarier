# Reel 10 — IA y pensamiento crítico (Fashionalytics / FOLD)

Reel 9:16 (1080×1920, 30 fps, 79,3 s) sobre el original de `REEL-10`, con el design system de
Fashionalytics/FOLD y el montaje de los reels de Sarier.

El guion trae datos duros, así que este reel se apoya en lo que mejor hace el sistema: `data-lg`
en mono con números tabulares, barras con relleno `brand` y los badges de procedencia.

## Beats

| Tiempo | Qué pasa |
| --- | --- |
| 0–2,9 s | hook por capas con glitch en "que conoces" y punch-in |
| 2,6–7,9 s | el díptico: la terminal de nueve a cinco, y el libro en la casa |
| 10,7–21,0 s | `60s` con una barra que se llena durante toda la sección de datos |
| 20,7–30,4 s | siete piezas distintas que, al delegar el juicio, terminan todas iguales |
| 30,1–45,6 s | el estudio: badge `OBSERVED`, barra de uso de IA arriba, pensamiento crítico abajo con `▼`, y los dos bordes |
| 45,4–54,3 s | ancho de banda: formato corto vs formato largo |
| 54,1–62,3 s | cinco barras que suben; la última, los clásicos, en `brand` |
| 62,0–67,5 s | la tarjeta de "lo único que te protege" en serif cursiva |
| 67,3–75,6 s | los dos StatTiles: **80 %** de los libros los lee el 20 % · **5 %** sabe usar IA con destreza |
| 75,3–79,3 s | el subconjunto de un subconjunto, y el cierre con *slow push* y fundido a negro |

## El logo de Claude Code

**Falta el archivo.** No hay un asset oficial descargable (ni en el repo de Claude Code ni en el
paquete de npm), y el criterio de este proyecto es no redibujar marcas ajenas de memoria — el
mismo que se aplicó con FOLD y con Ámbar.

Mientras tanto el momento se resuelve con la **tarjeta de terminal** (`~ $ claude` con cursor
parpadeando), que es literalmente lo que Claude Code es y encaja con el lenguaje mono del sistema.

`build.py` ya trae el enganche: si aparece `brand/claude-code.svg`, el logo entra en la tarjeta y
el texto se corre a la derecha. Basta con dejar el SVG ahí y volver a construir.

## Correcciones de transcripción

- "pero **no** os voy a dar sesenta segundos de datos" → se quitó el "no": con él la frase se
  contradice, porque sí da los datos. Si lo dijo literal, se revierte en `guion.txt`.
- "todo lo que produce" → "produces" · "como ningún otra cosa" → "ninguna otra cosa" ·
  "están a igual medida" → "están en igual medida" · "es estar en lo que tú necesitas estar" →
  "y es ahí donde tú necesitas estar".

## Encuadre

Su cabeza empieza en y=636, así que la banda de gráficos va de 290 a 600 y los subtítulos al
tercio inferior (y=1424), donde el plano es oscuro y el blanco se lee sin caja ni sombra.

## Regenerar

1. `python3 build.py` → `index.html`
2. `npx hyperframes check`
3. `../reel-tools/finish.sh reel-ai10 ai10`
