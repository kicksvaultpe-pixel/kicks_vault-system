# StatCard
Tarjeta de indicador en vidrio: cabecera corta, una cifra protagonista y, si hace falta, 2–4 tiles o filas de detalle.

- `.stat-card` (también `.ind-card`, `.fc-bubble`): `glass`, radio `radius-lg`, padding `space-5` (`space-4` en móvil).
- Cabecera `.kv-stat-hd` en `subhead` 13px/600 `text-secondary`, sin mayúsculas, con tendencia opcional (`.kv-trend.up/.down`) a la derecha.
- Cifra: `kpi` (24px/800) o, para el único dato héroe de la pantalla, `display` (40px/800; 34px en móvil). Siempre tabular-nums.
- Detalle: `.kv-tiles` > `.kv-tile` (`tile`, `l` + `v`) o filas `.fc-row` separadas por `separator`. Barras de composición con `.kv-bar`.
- El color va en el número, no en la tarjeta: sin líneas degradadas arriba, sin borde izquierdo de color, sin puntos con brillo, sin elevarse al pasar el mouse.
- Grilla `auto-fit` de mínimo 240px en escritorio; en móvil la fila pasa a carrusel horizontal con snap (cada tarjeta al 82% del ancho) en vez de apilar 5 tarjetas altas.
