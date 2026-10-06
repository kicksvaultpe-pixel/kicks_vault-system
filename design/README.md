Sistema de gestión de inventario, ventas, reservas y flujo de caja de una tienda de sneakers y prendas. Es una herramienta de trabajo diario que se usa tanto en PC como en el celular: tiene que ser rápida de leer, cifras primero, y verse premium sin estorbar. El lenguaje visual es **vidrio translúcido estilo iOS 26** sobre un lienzo con manchas de color difusas, con el azul Kicks Vault como único color de marca.

## Principios

1. **Cifras primero.** Cada pantalla tiene un número protagonista (`display`) y el resto en `kpi` o `num`. Todos los montos en tabular-nums, alineados a la derecha.
2. **Un color, un significado.** El color comunica el tipo de movimiento o el estado, nunca decora. Las tarjetas son neutras (vidrio) y el color va en la cifra, el badge o el botón.
3. **Vidrio sobre color.** Todas las superficies son `glass` sobre `bg` + 3 manchas (`blob-a/b/c`). Lo que flota (barras, hojas, menús, toasts) usa `glass-strong`.
4. **Mismo sistema en PC y móvil.** En PC: barra superior flotante, tablas completas con cabecera fija y formularios a 2 columnas. En móvil: tab bar flotante de 5 con "+" central, menú de secciones desde el título, filas como tarjetas, KPIs en carrusel y botones de envío fijos abajo.
5. **Menos ruido.** Sin puntos con brillo, sin líneas degradadas, sin bordes izquierdos de color, sin emoji y con un solo estilo en mayúsculas (`overline`).

## Contenido y tono

- Español de Perú, tuteo: "Ingresa para continuar", "Cuando pagues, usa Pagar en Inventario".
- Mayúscula solo al inicio: "Precio de compra", no "PRECIO DE COMPRA". Lo único en mayúsculas son los labels de campo y las cabeceras de tabla (`overline`).
- Moneda: `S/ 1,280.00` (con espacio) y `US$ 345.00`. Tipo de cambio: "TC S/ 3.70 por USD".
- Los códigos se muestran tal cual (`P01020`, `R00311`, `OC-0042`) en `accent-ink`.
- Toasts con el dato: "Venta registrada · P01020". Errores que dicen qué hacer: "No se pudo guardar. Revisa tu conexión."
- Sin emoji en la interfaz: se usan íconos de línea.

## Color

**Superficies**: `bg` (lienzo) → `glass` (tarjetas) → `tile` (sub-bloques dentro de una tarjeta) → `field` (inputs). Lo flotante va en `glass-strong`. Bordes de vidrio en `glass-border` con brillo `glass-highlight`; separadores en `separator`.

**Texto**: `text` para datos y títulos, `text-secondary` para descripciones y celdas secundarias, `text-tertiary` para labels, cabeceras y fechas, y `placeholder` solo para placeholders. Todos pasan 4.5:1 sobre `glass` y sobre los tintes `-soft` en ambos temas.

**Marca**: `accent` (botón principal, pestaña activa, foco, progreso) con `on-accent` encima; `accent-ink` cuando el azul es texto (links, códigos); `accent-soft` para selección y estados activos suaves.

**Movimientos y estados**: cada uno tiene su color, su `-soft` (badge o banner) y su `on-` (texto sobre el relleno):

| Significado | Token | Dónde |
|---|---|---|
| Compra, Contado | `accent` | segmento Compra/Contado, badge COMPRA |
| Venta, ingreso, ganancia, pagado | `positive` | montos de ingreso, badge VENTA, Disponible |
| Gasto, egreso, pérdida, error | `negative` | montos de egreso, badge GASTO, Eliminar |
| Crédito, pendiente, por pagar, saldo | `warning` | Pendiente, Pagar, saldo de reserva, barra de pago de OCs |
| Reserva, pedido, adelanto | `reserve` | badge RESERVA, segmento Reserva/Pedido |
| Costo operativo | `cost` | segmento Costo, badge COSTO |
| Inversión / aporte | `invest` | segmento Inversión, badge INVERSIÓN |

- En tema oscuro los rellenos son más claros, así que `on-…` es texto oscuro: nunca blanco fijo sobre `accent`, `negative` o `reserve` en oscuro.
- Las categorías (Zapatillas, Ropa, Accesorios, Otros) no llevan color: contorno `separator` + `text-secondary`.
- Las manchas `blob-a/b/c` son solo fondo; no se usan en componentes.

## Tipografía

**Archivo** en todos sus pesos para toda la interfaz (`--font-sans`). **Archivo Black** solo para el logotipo (`wordmark`: KICKS en `text`, VAULT en `accent-ink`, tracking .32em). Se carga desde Google Fonts: `Archivo:wght@400;500;600;700;800` y `Archivo+Black`.

Jerarquía (de mayor a menor):

| Estilo | Tamaño / interlínea / peso | Uso |
|---|---|---|
| `display` | 40/44 · 800 (móvil 34/38) | Un solo número héroe por pantalla |
| `title-1` | 28/34 · 800 (móvil 26/32) | Título de página |
| `title-2` | 20/26 · 700 | Título de hoja, modal y mes en Flujo |
| `kpi` | 24/28 · 800 | Cifra principal de una stat card |
| `headline` | 16/22 · 700 | Título de tarjeta |
| `kpi-sm` | 17/22 · 700 | Valores en tiles y totales |
| `body` | 15/22 · 400 | Texto corrido y banners |
| `callout` | 14/20 · 500 | Celdas de tabla, inputs, menús |
| `num` | 14/20 · 600 | Montos en tablas y listas |
| `subhead` | 13/18 · 500 | Meta, subtítulos, cabecera de stat |
| `footnote` | 12/16 · 600 | Badges, chips, tab bar, ayudas |
| `overline` | 11/14 · 700 · +.08em · MAYÚSC. | Labels de campo y cabeceras de tabla |

- El mínimo de la app es 11px (antes había textos de 8, 9 y 10px). En pantallas táctiles los inputs van a 16px.
- Títulos con tracking negativo leve. Mayúsculas solo en `overline`.
- Cifras siempre con `font-variant-numeric: tabular-nums`.

## Espaciado, radios y estructura

- Escala de 4px: `space-1` 4 · `space-2` 8 · `space-3` 12 · `space-4` 16 · `space-5` 20 · `space-6` 24 · `space-8` 32 · `space-10` 40.
- Gutter lateral `space-6` en PC y `space-4` en móvil. Padding de tarjeta `space-5` / `space-4`. Gap de grillas `space-4`.
- Radios: `radius-sm` 10 (botones pequeños) · `radius-md` 14 (inputs, botones, tiles) · `radius-lg` 22 (tarjetas, tablas) · `radius-xl` 30 (héroe, hojas, modales) · `radius-pill` (badges, chips, barras flotantes, FAB, segmented). Antes había 10 radios distintos (5–20px).
- Puntos de quiebre: móvil < `bp-tablet` (768) ≤ tablet < `bp-desktop` (1100) ≤ escritorio. Contenido hasta `content-max` (1440).
- Capas: `z-topbar` < `z-dropdown` < `z-sheet` < `z-modal` < `z-toast` < `z-gate`.

## Material, sombras y movimiento

- Receta de vidrio: fondo `glass`, `backdrop-filter: blur(var(--blur-glass)) saturate(180%)`, borde 1px `glass-border`, `shadow-glass` (que incluye el brillo interior de 1px). Lo flotante: `glass-strong` + `blur-bar` + `shadow-float`. Hojas y modales: `shadow-sheet`.
- Si el navegador no soporta `backdrop-filter`, el vidrio pasa a `glass-strong` sólido.
- Velo de hojas y modales: `overlay` + `blur-overlay`.
- Movimiento corto y con propósito: presionar `scale(.97)` en 120ms, hojas 250ms `cubic-bezier(.23,1,.32,1)`, cambio de vista con fundido de 200ms. Sin elevación al pasar el mouse. Con `prefers-reduced-motion` todo baja a casi cero.

## Estados

- Foco: anillo `focus-ring` de 2px sólido con 2px de separación en todo control (≥4.6:1 sobre vidrio en ambos temas).
- Hover de fila y selección: `accent-soft`. Celda seleccionada: además, contorno `accent` de 2px.
- Deshabilitado: opacidad 40%. Pendiente: barra interior `warning` de 3px a la izquierda de la fila.
- Cargando: spinner `accent` de 16px o filas esqueleto en `tile`. Vacío: ícono de línea de 32px en `text-tertiary` + una frase + acción.

## Scroll y diseño responsivo

- **Un scroll por vista.** La página hace scroll en `body`; tablas, hojas y menús hacen scroll propio con `overscroll-behavior: contain` para no arrastrar la página ni activar el pull-to-refresh.
- **Las tablas entran en la pantalla.** `.table-wrap` limita su alto al viewport (`100dvh − topbar-h − 180px`), con cabecera y paginación fijas y la primera columna fija al desplazar en horizontal. Las columnas tienen prioridad (`data-p`) y las secundarias se ocultan en pantallas medianas en lugar de forzar `min-width: 1200px`.
- **Móvil sin scroll horizontal.** Las tablas pasan a tarjetas (`.kv-stack` + `data-role`), los KPIs a un carrusel con snap, el selector de 6 tipos a una grilla de 3×2 y los filtros a chips que se desplazan sin barra visible.
- **Barras fijas.** Barra superior pegada (`scroll-padding-top` evita que tape anclas). En móvil el contenido reserva espacio para el tab bar y el safe-area, y los formularios largos tienen el botón de envío fijo (`.kv-submit-bar`).
- **Registro en PC** a 2 columnas (`.kv-split`): formulario a la izquierda y resumen del movimiento (precio, margen, efecto en caja) pegado a la derecha.
- Áreas táctiles de mínimo `tap-min` (44px).

## Iconografía

- Íconos de línea de 24×24 con trazo 1.8–2px, puntas y uniones redondeadas, en `currentColor` (el mismo estilo que los íconos actuales de la navegación). Se recomienda Lucide como set de referencia.
- Tamaños: 22px en el tab bar, 18px en botones y banners, 16px dentro de inputs.
- No se usan emoji. El repositorio no incluye logotipo en imagen: la marca es el logotipo tipográfico KICKSVAULT en Archivo Black.

## Componentes

Navigation · Button · SegmentedControl · Field · Badge · StatCard · DataTable · Sheet · InfoBanner · Toast. `components/bundle.css` es la hoja de estilos de referencia: conserva los nombres de clase actuales de `index.html` (`.card`, `.btn-primary`, `.tipo-btn`, `.table-wrap`, `.badge-green`…) para que el cambio sea directo, y agrega clases nuevas con prefijo `kv-`. La sección **Mejoras** tiene el diagnóstico, la tabla de equivalencias de variables y el plan para aplicarlo con Claude Code.
