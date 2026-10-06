# SegmentedControl
Control segmentado tipo iOS para elegir una opción entre 2 y 6: tipo de movimiento, Contado/Crédito, Stock/Pedido y periodos.

- Contenedor: pastilla `tile` con borde `glass-border` y 4px de padding. Opciones de 14px/600, sin mayúsculas.
- **De color** (`.tipo-selector`, `.pago-toggle`, `.rv-tipo-wrap`): la opción activa se rellena con el color del movimiento — Compra/Contado `accent`, Venta `positive`, Reserva/Pedido `reserve`, Gasto `negative`, Costo `cost`, Inversión `invest`, Crédito/Stock `warning` — con su `on-…`.
- **Neutro** (`.kv-seg`, `.an-toggle`): la activa es una pastilla `glass-strong` con sombra suave, como en iOS. Para filtros y periodos.
- En móvil `.tipo-selector` pasa a grilla 3×2 para que los 6 tipos se vean sin scroll escondido.
- El consumidor provee: las opciones, la activa y el handler. Usar `role="tablist"`/`aria-selected`.
