-- ============================================================
-- Que borrar un registro tambien borre su fila en flujo_caja.
--
-- Hoy los triggers solo corren al INSERT: crear un pago escribe su fila en el
-- flujo, pero borrar el pago la deja huerfana. Paso con el pago id=380
-- ("PAGO JUNIOR AGOSTO", S/ 467.00): se borro de `pagos` y el egreso siguio
-- apareciendo en setiembre. Es la misma trampa que ya nos costo caro una vez.
--
-- Cada tabla engancha su fila con una clave distinta, por eso son tres
-- triggers y no uno:
--    pagos   -> referencia_id = el id del pago, en texto
--    ventas  -> referencia_id = codigo_venta
--    costos  -> referencia_id = codigo_producto  (NO el id del costo)
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================

-- ── PAGOS ───────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION flujo_borrar_pago() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM flujo_caja
   WHERE coalesce(categoria, tipo) = 'PAGO'
     AND referencia_id = OLD.id::text;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_flujo_borrar_pago ON pagos;
CREATE TRIGGER trg_flujo_borrar_pago
  AFTER DELETE ON pagos FOR EACH ROW EXECUTE FUNCTION flujo_borrar_pago();


-- ── VENTAS ──────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION flujo_borrar_venta() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM flujo_caja
   WHERE coalesce(categoria, tipo) = 'VENTA'
     AND referencia_id = OLD.codigo_venta;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_flujo_borrar_venta ON ventas;
CREATE TRIGGER trg_flujo_borrar_venta
  AFTER DELETE ON ventas FOR EACH ROW EXECUTE FUNCTION flujo_borrar_venta();


-- ── COSTOS ──────────────────────────────────────────────────
-- Aca hay que tener cuidado: la fila del flujo apunta al PRODUCTO, no al
-- costo. Un producto con tres costos tiene tres filas con el mismo
-- referencia_id, asi que borrar "todas las del producto" se llevaria de mas.
-- Se borra UNA sola, la que coincide en monto, eligiendola por ctid.
CREATE OR REPLACE FUNCTION flujo_borrar_costo() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM flujo_caja
   WHERE ctid = (
     SELECT ctid FROM flujo_caja
      WHERE coalesce(categoria, tipo) = 'COSTO'
        AND referencia_id = OLD.codigo_producto
        AND egreso_soles  = OLD.costo_soles
      LIMIT 1
   );
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_flujo_borrar_costo ON costos;
CREATE TRIGGER trg_flujo_borrar_costo
  AFTER DELETE ON costos FOR EACH ROW EXECUTE FUNCTION flujo_borrar_costo();


-- ── COMPROBACION ────────────────────────────────────────────
-- Los tres pares tienen que dar el mismo numero. Si alguno no cuadra, quedan
-- filas huerfanas de antes de correr esto.
SELECT 'pagos'  AS tabla,
       (SELECT count(*) FROM pagos)  AS registros,
       (SELECT count(*) FROM flujo_caja WHERE coalesce(categoria,tipo)='PAGO')  AS filas_flujo
UNION ALL
SELECT 'ventas',
       (SELECT count(*) FROM ventas),
       (SELECT count(*) FROM flujo_caja WHERE coalesce(categoria,tipo)='VENTA')
UNION ALL
SELECT 'costos',
       (SELECT count(*) FROM costos),
       (SELECT count(*) FROM flujo_caja WHERE coalesce(categoria,tipo)='COSTO');
