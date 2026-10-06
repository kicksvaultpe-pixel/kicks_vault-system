# Toast
Confirmación breve y flotante después de guardar, con un punto de color que indica el resultado.

- `#toast` / `.kv-toast`: pastilla `glass-strong` con `shadow-float`, texto `text` 14px/600 y punto `.kv-dot` (`positive` ok, `negative` error, `warning` aviso). Antes era un bloque azul, rojo o amarillo sólido.
- Abajo al centro; en móvil queda encima del tab bar (`tabbar-h + 24px + safe-area`). `z-toast`.
- Mensajes en voz activa y con el dato: "Venta registrada · P01020", no "¡Éxito!".
