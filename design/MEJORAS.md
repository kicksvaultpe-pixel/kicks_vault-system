# Mejoras

Diagnóstico visual de `index.html` (commit `71d545e`) y cómo resolver cada punto con este sistema. Ordenado por impacto.

## 1. Diagnóstico

### Contraste y color
| # | Problema actual | Mejora |
|---|---|---|
| 1 | El verde `#16A34A` como texto sobre blanco tiene 3.3:1 (no pasa AA) y se usa en ingresos, "Disponible" y totales. | `positive` `#15703A` (5.7:1 sobre vidrio). |
| 2 | En oscuro, el texto blanco sobre `--accent` `#4F86F7` tiene 3.45:1, y sobre violeta y rojo 2.7:1. Afecta a botones primarios, Compra, Costo y Gasto. | Tokens `on-…`: en oscuro el texto va oscuro (5.7–12:1). |
| 3 | Contado activo usa texto negro sobre azul (4.06:1), mientras que Compra usa blanco: el mismo azul tiene dos tratamientos. | Todo relleno usa su `on-…`. |
| 4 | El placeholder (`--muted` `#3D4B6A`) es más oscuro que el label (`--muted2`) y parece un valor ya escrito. | Token `placeholder`, más claro que cualquier texto. |
| 5 | `--accent` y `--blue` son el mismo color: Compra e Inversión se ven iguales, y Costo comparte azul en Flujo. | Inversión pasa a `invest` (neutro) y Costo a `cost` (petróleo). |
| 6 | El violeta significa 5 cosas: reserva, costo, contado (banner), compras del mes y stock. | El violeta (`reserve`) queda solo para reservas y pedidos. |
| 7 | Amarillo y naranja representan lo mismo (deuda, pendiente, crédito, por pagar). | Se unen en `warning`. |
| 8 | Unos 60 `rgba(37,99,235,…)` y similares escritos a mano usan el azul del tema claro también en oscuro. | Tintes `-soft` por tema. |
| 9 | Las categorías Zapatillas (`accent`) y Ropa (`rgba(96,165,250)`) son dos azules casi iguales. | Las categorías van sin color y el color queda para los estados. |
| 10 | Los bordes de inputs (`--border2` sobre blanco) tienen 1.6:1, así que el campo casi no se ve. | `field-border` con ≥3:1. |

### Tipografía y jerarquía
| # | Problema actual | Mejora |
|---|---|---|
| 11 | Hay 17 tamaños distintos (8, 9, 10, 10.5, 11, 11.5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 26px). | 12 estilos con nombre (`display` → `overline`). |
| 12 | Tablas a 11px, inputs a 12px y etiquetas del tab bar a 8px: difícil de leer en PC y en el celular. | Celdas de 14px, inputs de 14px (16px táctil), tab bar de 11px. Mínimo de 11px. |
| 13 | Mayúsculas con tracking de 1–2.5px en pestañas, botones, labels, cabeceras, chips y títulos de tarjeta: todo grita por igual. | Un solo estilo en mayúsculas (`overline`) para labels y cabeceras. |
| 14 | Archivo Black aparece en más de 40 clases para cifras de 13–26px, y KPIs de igual importancia usan 15, 17 o 19px. | Archivo 800 en `kpi`/`display`; Archivo Black solo para el logotipo. |

### Ruido visual
| # | Problema actual | Mejora |
|---|---|---|
| 15 | Puntos con `box-shadow` de brillo en títulos, chips y burbujas. | Se eliminan. |
| 16 | Línea degradada arriba en cada stat-card e ind-card, y en las burbujas de Flujo se suma un borde izquierdo de 3px. | Se eliminan; el color va en la cifra. |
| 17 | `.card-label` en mayúsculas con borde izquierdo de 3px y una línea que la sigue. | Título `headline` limpio. |
| 18 | Emoji en banners y tablas (💵 🗓 📦 🚚 🔒 ⏻). | Íconos de línea SVG. |
| 19 | Las tarjetas se elevan al pasar el mouse aunque no son clicables. | Sin hover en tarjetas no interactivas. |

### Consistencia
| # | Problema actual | Mejora |
|---|---|---|
| 20 | 10 radios distintos (5, 6, 7, 8, 9, 10, 12, 14, 16, 20px), y badges con 5, 6 y 20px. | 5 radios con nombre. |
| 21 | Tres paneles laterales con anchos de 400, 440 y 460px, velos de .45, .45 y .5, y z-index de 220, 230 y 240. | Un solo `Sheet` con `sheet-w`, `overlay` y `z-sheet`. |
| 22 | z-index sueltos entre 150 y 999. | Escala `z-*`. |
| 23 | Varios `<span onclick>` en lugar de `<button>`, y el foco visible solo en `.nav-tab` y `.btn`. | Botones reales y `focus-ring` en todo control. |

### Responsive y scroll (PC + móvil)
| # | Problema actual | Mejora |
|---|---|---|
| 24 | `.table-wrap table{min-width:1200px}` (800px en móvil): en laptops de 1280–1366px la tabla no entra y hay que desplazarse en horizontal sin ver la cabecera. | Sin min-width fijo, columnas por prioridad (`data-p`), primera columna fija. |
| 25 | La tabla crece con toda la página, así que al bajar se pierde la cabecera y la paginación queda al final. | `max-height` atado al viewport, `thead` y `.pag-bar` fijos. |
| 26 | En móvil las tablas siguen siendo tablas de 800px con scroll horizontal. | Filas como tarjetas (`.kv-stack` + `data-role`). |
| 27 | En móvil la toolbar se desplaza en horizontal con los combos aplastados. | Buscador a todo el ancho + chips desplazables + "Filtros" en una hoja. |
| 28 | Los KPIs se apilan en 1 columna en móvil (5 tarjetas altas antes de llegar a la data). | Carrusel horizontal con snap. |
| 29 | El tab bar de 8 pestañas a 8px necesita una manija "Más opciones" que lo expande. | Tab bar de 5: Inventario, Reservas, **+** (Registro), Flujo, Resultados; el resto de secciones desde el menú del título. |
| 30 | `overscroll-behavior:none` en `html` bloquea el rebote nativo, mientras los paneles y combos no contienen su propio scroll (arrastran la página). | `overscroll-behavior:contain` solo en tablas, hojas y menús. |
| 31 | El formulario de Registro ocupa 100% del ancho en PC (inputs de 1300px). | `.kv-split`: formulario + resumen pegado a la derecha. |
| 32 | La barra fija tapa anclas y foco al hacer scroll. | `scroll-padding-top`. |

## 2. Equivalencias de variables (index.html → tokens v2)

| Antes | Ahora |
|---|---|
| `--bg` | `--bg` (+ manchas `.kv-canvas` en `body`) |
| `--surface` | `--tile` (sub-bloques) / `--field` (inputs) |
| `--card` | `--glass` (tarjetas) / `--glass-strong` (nav, hojas, menús) |
| `--border` | `--glass-border` (bordes de vidrio) / `--separator` (líneas internas) |
| `--border2` | `--field-border` |
| `--text` | `--text` |
| `--muted` | `--text-secondary` |
| `--muted2` | `--text-tertiary` |
| placeholder (`--muted`) | `--placeholder` |
| `--accent` | `--accent` (relleno) / `--accent-ink` (texto) |
| `--blue` | `--accent` (si era Compra) / `--invest` (Inversión) / `--cost` (Costo) |
| `--green` | `--positive` |
| `--red`, `--neg`, `--accent2` | `--negative` |
| `--yellow`, `--orange` | `--warning` |
| `--purple` | `--reserve` (solo reservas/pedidos; lo demás pasa a `accent` o neutro) |
| `rgba(<color>, .05–.12)` | `--<rol>-soft` |
| `#fff` / `#000` sobre color | `--on-<rol>` |
| `--shadow` | `--shadow-glass` |
| `--radius` y radios sueltos | `--radius-sm/md/lg/xl/pill` |

Durante la migración se puede dejar un bloque de compatibilidad para no romper el JS que arma HTML con estas variables: `:root{--card:var(--glass);--muted:var(--text-secondary);--muted2:var(--text-tertiary);--green:var(--positive);--red:var(--negative);--yellow:var(--warning);--orange:var(--warning);--purple:var(--reserve);--blue:var(--accent)}`.

## 3. Plan de implementación por fases

1. **Tokens y material.** Reemplazar los bloques `:root` y `[data-theme="dark"]` por los tokens v2 (más el bloque de compatibilidad), cargar `Archivo:wght@400;500;600;700;800`, agregar `.kv-canvas` al `body` y la receta de vidrio.
2. **Tipografía.** Aplicar la escala: títulos, cifras (`kpi`, `display`), celdas a 14px y `overline` como única mayúscula. Quitar Archivo Black de todo lo que no sea el logotipo.
3. **Limpieza de ruido.** Quitar brillos, degradados, bordes izquierdos y emoji (reemplazar por SVG), y unificar radios y badges.
4. **Navegación.** Barra superior flotante (≥768px). En móvil: tab bar de 5 espacios con "+" central (`.kv-tabbar`, `.kv-tab-add`) y menú de las 8 secciones al tocar el título (`.kv-title-btn` + `.kv-section-menu`). Sin pestaña "Más".
5. **Tablas.** `.table-wrap` con alto acotado, cabecera, paginación y primera columna fijas, `data-p` en columnas secundarias, y `.kv-stack` + `data-role` en móvil para Inventario, Reservas, Clientes, OCs y Flujo.
6. **KPIs y formularios.** Stat cards nuevas con carrusel en móvil, segmented controls, Registro en `.kv-split` y `.kv-submit-bar` en móvil.
7. **Hojas, modales y toast.** Unificar los tres paneles en `Sheet` (bottom sheet en móvil) y aplicar el nuevo toast.
8. **Revisión.** Ambos temas en 375, 768, 1280 y 1440px; contraste ≥4.5:1, foco visible y sin scroll horizontal en móvil.

## 4. Prompt para Claude Code

```text
Vamos a rediseñar visualmente Kicks Vault (index.html, single file) con el design system
"Kicks Vault v2" (estilo vidrio iOS 26). Lee primero el README y la sección Mejoras del design
system (carpeta design/), usa components/bundle.css como hoja de referencia y los
mockups de design/mockups/ como referencia visual de PC y móvil: conserva los nombres de clase
actuales y agrega las clases kv-.

Reglas:
- Solo cambia lo visual (CSS y marcado). No toques la lógica JS, las llamadas a Supabase ni los SQL.
- Mantén las mismas tarjetas, indicadores y cálculos que ya existen en cada pestaña: aplica la
  estructura visual del design system a esos datos. No inventes métricas nuevas (los mockups
  usan datos de ejemplo).
- Trabaja en una rama nueva: feat/kv-v2-glass.
- Mantén el modo claro/oscuro actual (data-theme + localStorage 'kv-theme').
- Mientras migras, deja el bloque de compatibilidad de variables para no romper el HTML que genera el JS.
- Cada tabla que se genera desde el JS debe recibir data-role en sus <td> (title, amount, meta,
  badge, actions, hide-m) y data-p="2|3" en las columnas secundarias.
- Verifica cada fase en 375px, 768px, 1280px y 1440px, en claro y oscuro.

Avanza por las 8 fases del plan de la sección Mejoras. Al terminar cada fase, dime qué cambiaste
y en qué partes del archivo, y espera mi OK antes de seguir con la siguiente.
```
