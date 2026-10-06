# Button
Botones de acción: uno principal por vista, del color del movimiento que registra, y acciones de fila como pastillas suaves.

- `.btn` + variante: `btn-primary` (`accent`), `btn-green` (`positive`), `btn-purple` (`reserve`), `btn-red` (`negative`), `btn-yellow` (`warning`), `btn-ghost` (vidrio). El texto siempre usa el `on-…` del relleno: en tema oscuro es texto oscuro sobre color claro.
- Alto mínimo 44px (`btn-sm`: 36px, solo con mouse o en barras). Radio `radius-md`, texto 15px/700 sin mayúsculas.
- El botón de envío de Registro toma el color del tipo elegido (Compra azul, Venta verde, Reserva violeta, Gasto rojo, Costo `cost`, Inversión `invest`). En móvil va dentro de `.kv-submit-bar`, pegado abajo y a todo el ancho.
- Acciones dentro de tablas: `.btn-pay` (`warning-soft` → `warning` al pasar), `.btn-cancel` (`negative-soft`), `.oc-edit-btn` (vidrio). En las tarjetas móviles se estiran a todo el ancho.
- Presionado: `scale(.97)`. Deshabilitado: opacidad 40%.
- No usar `filter:brightness` para el hover, texto negro fijo sobre color, ni `transform:translateY` al pasar el mouse.
