# DataTable
Tabla responsiva: en escritorio entra en la pantalla con cabecera fija; en móvil cada fila se convierte en una tarjeta legible.

**Escritorio y tablet**
- `.table-wrap` en `glass`, radio `radius-lg`, con `max-height: calc(100dvh − topbar-h − 180px)`: la tabla hace scroll por dentro, la cabecera (`thead th`, sticky, `glass-strong`) y la paginación (`.pag-bar`, sticky abajo) siempre se ven, y la página no salta.
- Primera columna fija con `.kv-sticky-col` (código o producto) al desplazar en horizontal.
- Sin `min-width:1200px`. Columnas por prioridad: `data-p="3"` se oculta por debajo de 1280px y `data-p="2"` por debajo de 1100px. Lo esencial (código, producto, estado, monto, acción) nunca se oculta.
- Celdas de 14px (antes 11px): dato principal `.td-main` en `text` 600, secundario en `text-secondary`, códigos en `accent-ink`, montos a la derecha y en tabular-nums. Cabeceras en `overline`.
- Hover y selección: `accent-soft`. Fila pendiente: barra interior de 3px `warning` a la izquierda. El cursor de mano solo aparece en filas clicables.
- `.is-compact` reduce el padding para pantallas con mucha data (OCs, Flujo).

**Móvil (< 768px)** — agregar `.kv-stack` al contenedor y `data-role` a cada `td`: `title` (producto), `amount` (monto, arriba a la derecha), `meta` (código · talla · fecha), `badge` (estado), `actions` (botones a todo el ancho) y `hide-m` (lo que no entra en la tarjeta). El scroll horizontal desaparece.

- El consumidor provee: columnas con su prioridad, filas, el handler de clic y la paginación.
- La barra de herramientas (`.table-toolbar`) junta buscador y chips de filtro (`.kv-chips`, que se desplazan en horizontal sin barra visible).
