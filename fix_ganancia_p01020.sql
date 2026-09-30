-- P-01020 se vendio ANTES de pagar su credito. pagar_credito() despues
-- sobreescribio precio_compra_soles/precio_final con el monto REAL pagado
-- (puede diferir del estimado al comprar), pero la venta ya grabada se quedo
-- con la ganancia calculada contra el costo viejo. De ahi el descuadre de
-- S/ 265.20 en el CONTROL de Flujo.

-- 1. Revisa esto primero -- compara ganancia_actual vs ganancia_correcta
SELECT
  v.codigo_venta, v.precio_venta_soles,
  v.ganancia        AS ganancia_actual,
  v.rentabilidad    AS rentabilidad_actual,
  i.precio_final    AS costo_real_hoy,
  round(v.precio_venta_soles - i.precio_final, 2) AS ganancia_correcta,
  round((v.precio_venta_soles - i.precio_final) / i.precio_final, 4) AS rentabilidad_correcta
FROM ventas v
JOIN inventario i ON i.codigo_producto = v.codigo_producto
WHERE v.codigo_producto = 'P-01020';

-- 2. Si los numeros de arriba tienen sentido, corre esto para corregir:
UPDATE ventas v
SET ganancia     = round(v.precio_venta_soles - i.precio_final, 2),
    rentabilidad = round((v.precio_venta_soles - i.precio_final) / i.precio_final, 4)
FROM inventario i
WHERE i.codigo_producto = v.codigo_producto
  AND v.codigo_producto = 'P-01020';
