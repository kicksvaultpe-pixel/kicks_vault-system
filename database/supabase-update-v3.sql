-- =============================================
-- KICKS VAULT — Update v3
-- Agrega lógica de CONTADO/CRÉDITO
-- Pega en: Supabase → SQL Editor → Run
-- =============================================

-- 1. Nuevas columnas en inventario
ALTER TABLE inventario
  ADD COLUMN IF NOT EXISTS tipo_pago     text DEFAULT 'CONTADO'
    CHECK (tipo_pago IN ('CONTADO','CREDITO')),
  ADD COLUMN IF NOT EXISTS pago_estado   text DEFAULT 'PAGADO'
    CHECK (pago_estado IN ('PAGADO','PENDIENTE')),
  ADD COLUMN IF NOT EXISTS fecha_vencimiento date,
  ADD COLUMN IF NOT EXISTS moneda        text DEFAULT 'USD'
    CHECK (moneda IN ('USD','SOLES'));

-- 2. Productos existentes: marcar como CONTADO/PAGADO
UPDATE inventario SET tipo_pago='CONTADO', pago_estado='PAGADO' WHERE tipo_pago IS NULL;

-- 3. Función para registrar pago de crédito y actualizar flujo
CREATE OR REPLACE FUNCTION pagar_credito(
  p_codigo        text,
  p_monto_soles   numeric,
  p_fecha         date
) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  -- Actualizar inventario
  UPDATE inventario SET
    precio_compra_soles   = p_monto_soles,
    precio_final          = p_monto_soles + COALESCE(
      (SELECT SUM(costo_soles) FROM costos WHERE codigo_producto = p_codigo), 0
    ),
    pago_estado           = 'PAGADO',
    tipo_pago             = 'CREDITO'
  WHERE codigo_producto = p_codigo;

  -- Registrar egreso en flujo_caja
  INSERT INTO flujo_caja (fecha, tipo, referencia_id, descripcion, egreso_soles)
  SELECT
    p_fecha,
    'COMPRA',
    p_codigo,
    'Pago crédito: ' || marca || ' ' || COALESCE(silueta,'') || ' ' || COALESCE(colorway,'') || ' (' || COALESCE(talla,'') || ')',
    p_monto_soles
  FROM inventario WHERE codigo_producto = p_codigo;
END;
$$;
