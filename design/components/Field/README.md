# Field
Campo de formulario (label + input/select/textarea + ayuda) dentro de una tarjeta de vidrio.

- `.field` > `label` (estilo `overline`, `text-tertiary`) + control. Control: alto 44px, `field` de fondo, borde `field-border` (≥3:1), radio `radius-md`, texto 14px/500 (16px en táctil para evitar el zoom de iOS).
- Placeholder en `placeholder`, más claro que cualquier valor: nunca debe parecer un dato ya escrito.
- Foco: borde `accent` + halo de 3px `accent-soft`. Error: `.field.is-error` → borde y ayuda en `negative`.
- Grilla de 12 columnas: 1 columna en móvil, `g2`/`g4` a 2 columnas en tablet, `g4` a 4 en ≥1280px.
- La cabecera de la tarjeta es `.card-label` en estilo `headline` (sin mayúsculas ni borde izquierdo).
- Listas desplegables (`.combo-list`) en `glass-strong` con `shadow-float`, máximo 320px de alto con scroll propio.
