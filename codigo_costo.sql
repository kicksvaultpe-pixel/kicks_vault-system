-- ============================================================
-- Codigo propio para cada costo (CT-0001, CT-0002...), igual que ventas,
-- pagos, inversiones y OC ya lo tienen.
--
-- `costos` nunca tuvo un codigo de negocio, solo el `id` interno de la tabla.
-- En el tab de Flujo, una fila COSTO mostraba la columna CÓD. OP. vacia por
-- esto mismo: no habia nada que mostrar ahi.
--
-- flujo_caja.referencia_id para las filas COSTO SIGUE apuntando al producto,
-- no se toca: de eso depende el trigger de borrado (flujo_borrar_costo, que
-- hace match por producto+monto) y las filas ya guardadas. El codigo_costo
-- vive solo en esta tabla; la app lo resuelve aparte para pintarlo en
-- pantalla.
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================

-- 1. La columna
ALTER TABLE costos ADD COLUMN IF NOT EXISTS codigo_costo text;

-- 2. Backfill de los costos existentes, en orden cronologico
WITH numerados AS (
  SELECT id, 'CT-' || lpad(row_number() OVER (ORDER BY fecha, id)::text, 4, '0') AS nuevo_codigo
  FROM costos
  WHERE codigo_costo IS NULL
)
UPDATE costos c
SET codigo_costo = n.nuevo_codigo
FROM numerados n
WHERE c.id = n.id;

-- 3. De aca en adelante, todo costo debe traer su codigo
ALTER TABLE costos ALTER COLUMN codigo_costo SET NOT NULL;
ALTER TABLE costos DROP CONSTRAINT IF EXISTS costos_codigo_costo_key;
ALTER TABLE costos ADD CONSTRAINT costos_codigo_costo_key UNIQUE (codigo_costo);

-- ── COMPROBACION ────────────────────────────────────────────
-- sin_codigo debe ser 0, repetidos debe ser 0.
SELECT count(*) AS total,
       count(*) FILTER (WHERE codigo_costo IS NULL) AS sin_codigo,
       count(*) - count(DISTINCT codigo_costo) AS repetidos,
       min(codigo_costo) AS primero,
       max(codigo_costo) AS ultimo
FROM costos;
