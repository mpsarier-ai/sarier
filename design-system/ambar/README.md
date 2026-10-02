# Ámbar Sculpt Studio — design system

Paquete para usar la marca en código (Claude Code u otro).

- `BRAND.md`: el brand book. Reglas de voz, color, degradé, tipografía, fotografía y composición. Léelo primero.
- `metodo-consultoria.md`: el servicio The Ámbar Method y cómo se ve.
- `tokens.css`: colores, degradés, espaciado, radios, fuentes (`@font-face`) y clases de texto, listo para importar.
- `tokens.json`: los mismos tokens como datos, con la nota de uso de cada uno.
- `fonts/`: Sackers Gothic (Light, Medium, Heavy), Anton, Pinyon Script, Cormorant Garamond.
- `components/`: cada componente con su guía (`README.md`) y un ejemplo en HTML (`preview.html`).
- `referencias/`: capturas reales de la marca, solo como referencia de estilo.

## En Claude Code

1. Copia esta carpeta a tu proyecto, por ejemplo en `design-system/ambar/`.
2. Agrega esto al `CLAUDE.md` del proyecto:

```
Para cualquier interfaz o pieza de Ámbar, lee primero design-system/ambar/BRAND.md
y usa los tokens de design-system/ambar/tokens.css. No inventes colores ni fuentes.
```

3. Importa `tokens.css` en tu app y usa las variables (`var(--fuego)`, `var(--luz-hero)`) y las clases de texto (`.titular`, `.versalitas`).

Sackers Gothic es una fuente de licencia comercial: úsala según la licencia que tengas.
