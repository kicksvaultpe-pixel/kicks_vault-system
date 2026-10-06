# Badge
Pastilla de estado o tipo de movimiento con punto de color; las categorías van sin color.

- Alto 24px, radio `radius-pill`, texto `footnote` (12px/600), punto de 6px en `currentColor`: el estado se entiende aunque no se distinga el color.
- Mapa único: Compra `accent-soft`/`accent-ink`, Venta `positive`, Reserva `reserve`, Gasto/Pago `negative`, Costo `cost`, Inversión `invest`, Pendiente/Crédito/VIP `warning`, Cancelado neutro (`tile`).
- Categorías (`.cat-zap`, `.cat-ropa`, `.cat-acc`, `.cat-otros`): solo contorno `separator` y texto `text-secondary`. Antes Zapatillas y Ropa eran dos azules casi iguales.
- Un solo radio para todos los badges (antes había 5px, 6px y 20px).
