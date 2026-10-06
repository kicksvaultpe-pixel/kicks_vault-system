# Navigation
Navegación de la app: barra superior flotante de vidrio en tablet y escritorio; en móvil, tab bar de 5 espacios con "+" central y un menú de secciones que se abre desde el título.

**Escritorio / tablet (≥ 768px)** — `.kv-topbar.kv-glass-strong`, pegada a 12px del borde superior, radio `radius-pill`, alto `topbar-h`. Logotipo `wordmark` a la izquierda, las 8 secciones como pastillas (`.nav-tab`; la activa en `accent` con `on-accent`), botón de tema a la derecha. Si no caben, las pestañas se desplazan en horizontal con un desvanecido en el borde.

**Móvil (< 768px)**
- `.kv-tabbar`: barra de vidrio `glass-strong` con 5 espacios iguales: **Inventario · Reservas · [+] · Flujo · Resultados**. El `.kv-tab-add` central (56px, `accent`) abre **Registro**. No hay pestaña "Más".
- `.kv-title-btn`: el título de la página con un chevron. Al tocarlo abre `.kv-section-menu`, un menú flotante de vidrio con las 8 secciones (`.kv-section-item`: ícono en `tile`, nombre y contador opcional en `text-tertiary`; la actual en `accent-soft`/`accent-ink`). Así se llega a Clientes, OCs y Análisis. Se cierra al tocar fuera, al elegir una opción o con Esc.
- Pestaña activa: `accent-soft` de fondo + `accent-ink`. Etiquetas de 11px.
- El contenido reserva `tabbar-h + 40px + safe-area` abajo para que nada quede tapado.

- El consumidor provee: la sección activa, el handler de cambio y los contadores del menú (opcionales).
- Accesibilidad: `aria-haspopup="menu"` y `aria-expanded` en el título; `aria-label` en el botón "+".
- No usar: subrayado animado bajo la pestaña, etiquetas < 11px, mayúsculas en las pestañas ni una pestaña "Más" con tres puntos.
