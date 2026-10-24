# LUXUR · Q4 2026 · Trimestre Dorado — el sistema

De dónde sale: el artifact **Asesoría Q4 LUXUR**
(`https://claude.ai/artifact/NHJWvGqKbWq8QHVBD1L8or`), que lo declara en su propio CSS —
`Identity: Q4 Trimestre Dorado (LUXUR)` — y lo usa en el cintillo: *LUXUR · Q4 2026 · Trimestre
dorado*. Los artifacts hermanos del trimestre (`LUXUR · Q4 2026 Planning`,
`LUXUR · Semana 43 · Arranque Q4`) comparten la misma paleta.

No es una marca nueva: es **LUXUR con la paleta estirada para Q4**. El beige, la tinta y el blush
son los de siempre; lo que añade el trimestre dorado es una familia de neutros cálidos y tostados
—el dorado `#8C7B5E` entre ellos— y una voz tipográfica más ligera (Poppins 300 a tamaño grande).

Si el cliente pide "el reel de LUXUR" a secas, fuera de Q4, usa el tema `luxur` de `reelkit.py` sin
los tostados. El trimestre dorado es para octubre, noviembre y diciembre.

## Tokens

```
--paper  #FBFAF7   el papel del trimestre, un punto más cálido que el beige de siempre
--cream  #EDEBE6   el beige LUXUR de siempre; superficies y chips
--pink   #EECDCC   el blush de siempre; cintillos, barras de capítulo, destacados
--ink    #1C1C1C   la tinta
--mute   #5A5A5A   texto secundario
--line   #BDBAB3   reglas
--soft   #E6E2DC   separadores y rejilla
```

Series y acentos (el orden importa: así se reparten en gráficos y en jerarquía):

```
--s1   #1C1C1C   tinta            serie principal
--s2   #D59C9B   rosa             segunda serie
--s3   #C9C4BB   arena
--acc  #B0645F   terracota        enlaces y énfasis
--acc2 #8C7B5E   DORADO           el acento del trimestre
--g2   #B9B3A9   --g3 #9A948A   --g4 #DAD5CC    grises cálidos
```

Estado: `--good #4F7A55` · `--warn #A67A1F` · `--bad #B0453A`.

**El dorado se usa una vez por pantalla.** Es el acento del trimestre, no un color de relleno: una
cifra, una píldora o un subrayado. En cuanto aparece dos veces deja de significar nada.

## Tipografía

Poppins para todo, display y cuerpo. Lo que cambia es el peso según el papel que juega:

| Voz | Peso | Uso |
| --- | --- | --- |
| cifra / titular | **300** | números grandes y titulares; `letter-spacing: -0.02em` |
| cintillo, etiqueta | **600** | versalitas con `0.18em` de tracking |
| cuerpo | 400 | subtítulos y texto corrido |
| énfasis | 500–600 | píldoras, encabezados de tabla |

La Poppins 300 a tamaño grande es la firma del trimestre. Si un número o un titular sale en 600,
el reel se parece al de LUXUR de siempre y se pierde el Q4.

## Componentes y cómo se traducen a un reel 9:16

El sistema nació en una página web de una columna. Estas son las equivalencias que ya están
probadas en vídeo:

| En la web | En el reel |
| --- | --- |
| cintillo `600 12px` tracking `.18em` sobre blush | la píldora de capítulo (`01`, `02`, `03`) |
| `h2` con una barra blush de **44×4** encima | la regla que se dibuja dentro de la tarjeta de capítulo |
| cuadrícula de KPI sobre blush, separada por reglas de 1px | la fila de cifras del cierre o del producto |
| `.pill` versalitas con borde de `1.5px` de `currentColor` | píldoras de atributo: fit, uso, "qué sí / qué no" |
| `.chip` sobre cream | etiquetas pequeñas dentro de una tarjeta |
| segmentado: pista cream, activo tinta sobre papel | el estado marcado de una píldora |
| `.callout` cream, radio 4 | tarjeta de dato |
| tabla: encabezado `600 11px` versalitas, regla de `1.5px` tinta | comparativa de dos o tres columnas |

**La superficie beige es el recurso central.** En una tienda, sobre un plano entero, contra un
escaparate o un espejo no hay ninguna tinta plana que aguante: el fondo se mueve entre 16 y 242 de
luminancia en el mismo reel. La marca ya resolvió eso en la web y en la tienda poniendo el texto
sobre una superficie beige, y en vídeo funciona igual. Una tarjeta `#FBFAF7` o `#EDEBE6` con tinta
encima se lee sobre cualquier fotograma y además es inconfundiblemente LUXUR.

## Geometría que ya está calibrada

- Tarjeta de capítulo: `x 96, w 888`, radio `32`, alto `240`. Margen interior `40`.
- Dentro: `LUXUR` en Montserrat 600, 19px, tracking `.26em`, alfa `.5`, arriba a la derecha.
- Píldora de número a `y+70`, titular a `y+112` en 54px, regla a `y+150`, fila de píldoras o
  muestras a `y+156`.
- Píldora: alto `44–50`, radio = alto/2, padding lateral `20–26`.
- **Ancho de una píldora en versalitas con `0.18em` de tracking ≈ `0.92em` por carácter**, más el
  padding. Con `0.80` se montan unas sobre otras; está medido con Poppins 500.

## Contraste, que es donde se cae el sistema

Dos combinaciones del sistema no pasan AA a tamaño de reel, y las dos tienen arreglo dentro de la
propia marca:

- **Blanco sobre blush o sobre naranja** da ~2,8:1. La píldora conserva el degradé o el relleno de
  la marca y toma **tinta** en vez de blanco: sube a 5,2:1.
- **Terracota o dorado como texto** sobre papel da 2,6–2,9:1. Sirven para rellenos, reglas y
  píldoras; para texto largo usa tinta o `--mute`.

Comprueba siempre con `hyperframes check`: devuelve el ratio medido por fotograma y cuenta el halo
de los subtítulos, que el ojo sí ve y una fórmula de contraste plano no.
