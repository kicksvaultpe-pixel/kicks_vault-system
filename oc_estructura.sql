-- ============================================================
-- Tab OC: pasar de un registro suelto a seguir la importacion
--
-- Hoy `ordenes_compra` solo tiene codigo, tipo, estado, fecha, nombre y notas.
-- Todo el seguimiento (tienda, numero de orden, courier, tracking, QC, valor)
-- vive en el Excel "4. Importaciones" y la app no lo ve.
--
-- Correr entero en el SQL Editor de Supabase.
-- ============================================================

-- 1. Campos del seguimiento -----------------------------------
ALTER TABLE ordenes_compra
  ADD COLUMN IF NOT EXISTS descripcion    TEXT,          -- que se compro
  ADD COLUMN IF NOT EXISTS tienda         TEXT,          -- STOCKX, GOAT, SUPREME...
  ADD COLUMN IF NOT EXISTS orden_tienda   TEXT,          -- el nro de orden de la tienda
  ADD COLUMN IF NOT EXISTS courier        TEXT,          -- UPS, FEDEX, DHL, USPS...
  ADD COLUMN IF NOT EXISTS tracking       TEXT,          -- link de seguimiento
  ADD COLUMN IF NOT EXISTS qc             TEXT,          -- Por enviar / Enviado a QC
  ADD COLUMN IF NOT EXISTS valor_usd      NUMERIC(12,2), -- lo que costo en dolares
  ADD COLUMN IF NOT EXISTS fecha_llegada  DATE;          -- cuando llego a Peru

-- 2. Estados: el pipeline real ---------------------------------
-- Antes: PENDIENTE / COMPLETADA / CANCELADA, que hablaban de si ya se habian
-- registrado los productos. Ahora describen donde esta la compra.
UPDATE ordenes_compra SET estado = 'ENTREGADO EN PERU' WHERE estado = 'COMPLETADA';
UPDATE ordenes_compra SET estado = 'COMPRADO'          WHERE estado = 'PENDIENTE';
UPDATE ordenes_compra SET estado = 'CANCELADO'         WHERE estado = 'CANCELADA';

ALTER TABLE ordenes_compra DROP CONSTRAINT IF EXISTS ordenes_compra_estado_check;
ALTER TABLE ordenes_compra ADD  CONSTRAINT ordenes_compra_estado_check
  CHECK (estado IN ('COMPRADO','EN CAMINO USA','ENTREGADO EN USA','ENTREGADO EN PERU','CANCELADO'));

-- 3. El codigo no puede quedar vacio ---------------------------
-- Hay una OC con el codigo en blanco. La restriccion UNIQUE no lo impide
-- porque el vacio se cuenta como un valor mas.
--
-- Ojo: existe la foreign key inventario.orden_compra -> ordenes_compra.codigo,
-- y el producto P-00863 (VALE FOREVER TEE) apunta a esa OC vacia. Hay que
-- soltarlo primero o el DELETE falla con error 23503.
UPDATE inventario SET orden_compra = NULL
  WHERE orden_compra IS NOT NULL AND btrim(orden_compra) = '';

DELETE FROM ordenes_compra WHERE codigo IS NULL OR btrim(codigo) = '';

ALTER TABLE ordenes_compra
  ALTER COLUMN codigo SET NOT NULL,
  ADD CONSTRAINT ordenes_compra_codigo_no_vacio CHECK (btrim(codigo) <> '');

-- comprobacion
SELECT estado, count(*) AS ordenes FROM ordenes_compra GROUP BY estado ORDER BY 2 DESC;
