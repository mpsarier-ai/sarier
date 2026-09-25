# LUXUR · reel "el dúo perfecto" (RELAXED FIT + LOW WIDE FIT)

Primer reel con el **sistema de diseño de LUXUR**, no el de Sarier. Los tokens se leyeron del tema real
de la tienda (Shopify → tema `LUXUR DEV - Menú FITS`, `config/settings_data.json`), no de una interpretación:

| Token | Valor | Uso en el reel |
|---|---|---|
| Fondo | `#EDEBE6` | escenas faceless, píldoras claras |
| Tinta | `#1C1C1C` | texto, líneas, píldora invertida |
| Blush | `#EECDCC` | píldoras de acento (badge custom del tema) |
| Crema / salvia | `#ECE4D1` / `#B9B6A2` | reserva |
| Tipografía | Poppins 300/400/500 | títulos −0.04em, versalitas +0.18em |
| Botón / píldora | radio 60px, mayúsculas +0.02em | todas las píldoras |
| Trazo de icono | 1.6–2px | siluetas y reglas |

La palabra destacada de los subtítulos no va en rojo (eso es Sarier): va en **píldora**, beige sobre video
y tinta sobre las escenas beige, igual que los badges de la tienda.

## Datos reales
El stock y los nombres de color salen del catálogo vivo: AZUL OSCURO 1 · AZUL DIRTY 10 · NEGRO 15 · ROSADO 22,
todos LOW WIDE FIT a $199.000. Si el video se publica semanas después, hay que volver a consultarlos.

## Estado
- `luxur-diseno.jpg` es la lámina de diseño aprobada sobre un **fotograma de relleno** (sacado del pantallazo del chat).
- Falta el video original (`Facetune…-esv2-50p-bg-m-music-10p`) y el logo oficial: el proxy de red bloquea
  `cdn.shopify.com` y `luxurjeans.com`, así que ambos tienen que subirse a una release del repo.
- Los tiempos de `captions.cut.json` son provisionales (repartidos por longitud sobre 90 s); se recalculan
  con el audio real usando `cut.py` + `align.py` + `retime2.py`.

## Regenerar
1. `../reel-tools/prep.sh reel-luxur <url> <sha256>` (descarga, alinea, corta pausas, codifica).
2. `python3 build.py` → `index.html`; `npx hyperframes check`.
3. `../reel-tools/finish.sh reel-luxur luxur` → master + copia Instagram.
