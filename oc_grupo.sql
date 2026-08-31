-- ============================================================
-- Falta la columna GRUPO, que en tu hoja de Importaciones es la
-- columna I. Con esto el tab muestra las mismas columnas que el Excel.
-- Correr en el SQL Editor de Supabase.
-- ============================================================

ALTER TABLE ordenes_compra
  ADD COLUMN IF NOT EXISTS grupo TEXT;

-- comprobacion
SELECT count(*) AS ordenes, count(grupo) AS con_grupo FROM ordenes_compra;
