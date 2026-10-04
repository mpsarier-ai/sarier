# Reel 9 — estética vs taste (Fashionalytics / FOLD)

Reel 9:16 (1080×1920, 30 fps, 67,4 s) sobre el original de `REEL-9`, con el design system de
Fashionalytics/FOLD y el montaje de los reels de Sarier.

## Encuadre

Mismo set que el reel 8, otro día. Ella se sienta más alta: su cabeza empieza en y=645, así que
**la banda limpia para gráficos va de y=300 a y=610** y los subtítulos van en el tercio inferior
(y=1424), que es donde el plano es oscuro y el blanco se lee sin caja ni sombra.

## Beats

| Tiempo | Qué pasa |
| --- | --- |
| 0–4,6 s | hook por capas, con glitch en **taste** y punch-in |
| 4,4–7,0 s | el bloque partido: `estética` (lo que se ve) vs `taste` (lo que decides), en azul de marca |
| 10,3–15,7 s | las tres founders, una ficha por nombre a medida que las menciona |
| 15,2–24,0 s | lo que sí se puede copiar: tres casillas que se marcan y una línea que las tacha |
| 23,7–28,6 s | las muestras de paleta bajan de peso y queda "era ese taste" |
| 28,4–35,8 s | el taste es juicio: lo que construye lleva barra `brand`, lo que se corta solo hairline |
| 35,6–42,0 s | lo que se ve y lo que no: bloque `ink` arriba de la línea, 130 celdas azules debajo |
| 41,7–47,7 s | la retícula del feed: nueve fichas que terminan todas iguales |
| 47,4–62,6 s | dos barras: la estética se descarga al 100 %, el taste se construye por pasos |
| 62,4–67,4 s | cierre: statement centrado, *slow push* y fundido a negro |

## Las tres founders

Las fotos vienen del release `FOTOS-FOUNDERS`, recortadas a vertical y puestas a sangre y sin
filtros, como pide el brand book. El nombre va en una franja `surface` dentro de la ficha, en
`label` mono. **El orden lo confirmó el cliente**: 1 Emily Oberg · 2 Danielle Guizio · 3 Matilda
Djerf; no se dedujo de las caras.

## Reglas del sistema

`brand` #1a1aff es la única tinta de acción y la palabra caliente de los subtítulos (en el tono
Ink `#a3a3ff`, que es el que pasa contraste sobre el plano oscuro). Sin sombras en todo el reel.
Sentence case salvo mono. Cuadrado en todo lo mono. Movimiento ease-out; nada rebota. El
resaltador `accent-acid` no se usa.

## Subtítulos

Alineación forzada sin ASR: espeak-ng es-419 por línea → MFCC → DTW contra el audio real. **No se
cortaron pausas**: la locución es continua, `silencedetect` no encuentra ningún silencio de 0,35 s.
Cinco de las 34 líneas no llevan subtítulo porque las dice la tipografía grande.

## Regenerar

1. `python3 build.py` → `index.html`
2. `npx hyperframes check`
3. `../reel-tools/finish.sh reel-taste9 taste9`
