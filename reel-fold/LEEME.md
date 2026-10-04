# Reel 8 — Fashionalytics / FOLD

Reel 9:16 (1080×1920, 30 fps, 38.4 s) sobre el video original, editado como los de Sarier
—subtítulos cinéticos, tipografía grande, gráficos encima del plano— pero con el **design system
de Fashionalytics/FOLD**, no con el de Sarier.

## De dónde sale el sistema

- `mpsarier-ai/fashionalytics-platform` → `packages/ui/tokens.css` y `packages/ui/fx.css`.
- El brand book publicado: `claude.ai/artifact/GGCvZa3r87KowSAk58Pyy4` (`project/README.md`,
  `project/assets/Logos/README.md`, `project/assets/ASCII/README.md`).
- Los logos y las texturas ASCII están en `brand/`, **copiados tal cual** del sistema. El README
  de logos lo pide explícitamente: no se re-tipografían ni se recolorean.

`fold-fashionalytics.netlify.app` está bloqueado por la política de red del entorno, así que nada
se tomó de la web desplegada.

## Las reglas que mandaron sobre la edición

| Regla del brand book | Cómo se aplicó |
| --- | --- |
| "La marca es cruda, el producto es calmado" | un solo bloque azul-ASCII (el chiste del vibecoding) y el cierre; el resto es tema Paper |
| `brand` `#1a1aff` es la única tinta de acción | celdas del dither, cuadrados del equipo, cierre |
| `brand` `#1a1aff` es la única tinta de acción | la palabra caliente de cada subtítulo, el dither, los cuadrados y el cierre |
| Separar capas por valor y hairline, **nunca por sombra** | ningún `text-shadow` en todo el reel; los subtítulos se apoyan en la zona oscura del plano |
| Frases en sentence case; solo `label` y `pixel-title` en MAYÚSCULAS | subtítulos en sentence case, tags y labels en mono mayúscula |
| Cuadrado para lo mono/ASCII/poster | todos los tags y el dither en `radius-none` |
| 160 ms ease-out, **nada rebota** | todas las entradas son `power2.out` de 0.2–0.3 s, ningún `back.out` |
| Los logos no van sobre textura ASCII sin franja sólida detrás | el cierre lleva una banda `brand` sólida con hairline arriba y abajo |
| El loader es un carácter mono que rota, nunca un spinner | `|/-\` animado, y `●` como glifo de estado |

## Montaje: los recursos de los reels de Sarier

Nada de chrome blanco encima del plano. El montaje usa los mismos recursos que los reels de Sarier:

- **Subtítulos cinéticos centrados** sobre el video, palabra por palabra, sin caja y sin sombra.
  Van en el tercio inferior (y=1424) porque ahí el plano es oscuro; en la zona clara de arriba el
  texto `ink` chocaba con los jeans. La palabra caliente va en `brand` del tema Ink (`#8f8fff`),
  que es la tinta de acción del sistema.
- **Statements desiguales por capas** (`R.card`): tres piezas a distinto tamaño, alineación y alfa,
  que entran desde lados distintos. En `ink` sobre la pared clara, nunca blancas con sombra.
- **Glitch** sobre la palabra grande del hook, con los dos acentos del sistema (`signal-red` y
  `brand`) en vez de los de Sarier.
- **Punch-in** en el hook, en el corte de la escena azul y en los diez cuadrados; **slow push** en
  el cierre; **fundido a negro** al final.
- **Una escena faceless corta** (3,9 s): el bloque azul del vibecoding.
- **Bug de marca** arriba a la izquierda: el lockup de FOLD y, al lado, el módulo que resuelve lo
  que ella está diciendo — Core → Product → Production → Inventory → Marketing → Commerce. Sale de
  pantalla durante la escena azul, donde el lockup en `ink` no se leería.

El resaltador `accent-acid` no se usa: al cliente no le gustó, así que la única tinta de énfasis
es `brand`. El sistema lo permite — "`brand` es la única tinta de acción".

## Las cinco voces tipográficas

Geist (sans, titulares y subtítulos) · IBM Plex Mono (labels, data, tags, terminal) ·
DotGothic16 (pixel: solo el poster de VIBECODING) · Instrument Serif (una sola palabra en cursiva
dentro de un titular sans: "todavía toma *semanas*") · Handjet queda cargada pero sin uso.

## Beats

1. **0–4.7** hook en Geist con "más difícil" resaltado en acid.
2. **4.7–8.8** panel `blue-electric` con la textura ASCII del sistema: el chiste del vibecoding,
   en mono y pixel, con el loader de la marca.
3. **8.8–14.1** "todavía toma *semanas*" + tags DÍAS · SEMANAS · FÁBRICAS.
4. **14.1–19.3** el dither de Fashionalytics: 36 celdas que crecen de ruido a señal.
5. **19.3–34.3** diez tags cuadrados que se van acumulando, uno por cada cosa que ella enumera.
6. **34.3–35.9** los diez tags se resuelven en diez cuadrados: el equipo de diez personas.
7. **35.9–38.4** cierre en tema Screen: ASCII, lockup de FOLD en blanco, los ocho módulos y la
   firma de Fashionalytics.

## Dos decisiones de edición

- **"Vicodin" era un error de transcripción**: la palabra es **vibecoding**, y así quedó.
- **La última frase del original queda colgada** ("Y es por eso que creo que."). Se cortó el video
  en 35,95 s, donde termina "como un equipo de diez personas", y se añadieron 2,45 s de cola para
  el cierre de marca. Si aparece el resto de la frase, se re-monta con el original completo.

## Subtítulos

Alineación forzada sin ASR: espeak-ng es-419 por línea → MFCC → DTW contra el audio real. Las tres
pausas del original caen a menos de 0,1 s de los límites que calculó el DTW, así que no hizo falta
reanclar. **No se cortaron pausas**: solo hay 1,2 s de silencio en todo el reel y puntúan bien.

Las dos primeras líneas no llevan subtítulo porque las dice la tipografía grande.

## Regenerar

1. `python3 build.py` → `index.html`
2. `npx hyperframes check`
3. `../reel-tools/finish.sh reel-fold fold` → master + copia Instagram

El tema `fold` vive en `reelkit.py` (`THEMES["fold"]`); las fuentes están en `public/fonts/`
(Geist, IBM Plex Mono, DotGothic16, Handjet, Instrument Serif).
