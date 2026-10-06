# Sheet
Panel de detalle o edición que se abre sobre la vista: lateral en escritorio, inferior en móvil. Un solo patrón para Editar inventario, Detalle de reserva y Perfil de cliente.

- `.kv-sheet` (también `#inv-edit-panel`, `#rsv-panel`, `.cl-panel`): `glass-strong`, radio `radius-xl`, separado 12px de los bordes, ancho `sheet-w` (antes 400, 440 y 460px), `z-sheet`.
- Estructura fija: `.kv-sheet-hd` (overline + `title-2` + cerrar) · `.kv-sheet-body` (único scroll, con `overscroll-behavior:contain` para que no arrastre la página) · `.kv-sheet-ft` (acciones a todo el ancho, siempre visibles).
- Velo `.kv-overlay`: `overlay` + blur 4px (antes 3 opacidades distintas).
- Móvil: sube desde abajo, hasta 92dvh, con `.kv-grabber`, y respeta el safe-area inferior.
- `.modal` usa el mismo material para confirmaciones cortas; en móvil también se ancla abajo.
- El consumidor provee: título, contenido, acciones y el cierre (Esc, clic en el velo, botón).
