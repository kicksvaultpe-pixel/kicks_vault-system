-- ============================================================
-- Agregar FACEBOOK como canal de venta.
--
-- `ventas.canal` tiene un CHECK que solo admite INSTAGRAM, WHATSAPP,
-- PRESENCIAL y OTRO, asi que guardar una venta por Facebook falla con
-- "violates check constraint ventas_canal_check".
--
-- `clientes.canal_preferido` no tiene esa restriccion y ya lo acepta.
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================

ALTER TABLE ventas DROP CONSTRAINT IF EXISTS ventas_canal_check;
ALTER TABLE ventas ADD  CONSTRAINT ventas_canal_check
  CHECK (canal IS NULL OR canal IN ('INSTAGRAM','WHATSAPP','FACEBOOK','PRESENCIAL','OTRO'));

-- comprobacion: deberia listar los canales en uso sin error
SELECT coalesce(canal,'(sin canal)') AS canal, count(*) AS ventas
FROM ventas GROUP BY canal ORDER BY 2 DESC;
