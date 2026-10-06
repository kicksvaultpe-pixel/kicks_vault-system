# Prompt para Claude Code

1. Copia la carpeta `design/` a la raíz del repo `kicks_vault-system`.
2. Abre Claude Code en ese repo.
3. Pega el texto de abajo.

---

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
