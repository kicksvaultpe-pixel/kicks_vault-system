-- ============================================================
-- precio_final SIEMPRE = precio de compra + costos del producto.
--
-- `precio_final` es lo que vale un producto en el stock, y hasta ahora no lo
-- mantenia nadie: cada camino lo calculaba por su cuenta y uno lo rompia.
--
--   * el RPC pagar_credito lo deja igual al monto pagado, y ahi se lleva por
--     delante los costos: un producto de S/ 1,000 con S/ 100 de importacion
--     quedaba valorizado en 1,000 en vez de 1,100.
--   * el formulario de Registro > Costo no lo tocaba.
--   * solo el modal de editar producto lo recalculaba bien.
--
-- El sintoma no aparece al registrar el costo sino semanas despues, al pagar el
-- credito o vender el producto: la caja baja el monto completo y el stock solo
-- sube la parte sin costos, asi que el CONTROL del tab Flujo se rompe por el
-- monto de los costos. Paso con P-00989 y P-00990, S/ 106.00 cada uno.
--
-- Estos triggers ponen la regla en la base, de modo que da igual quien escriba
-- —la app, el RPC, o una consulta a mano en Supabase—: el valor sale correcto.
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================


-- ── 1. El valor correcto para un producto ───────────────────
CREATE OR REPLACE FUNCTION kv_precio_final(p_codigo text, p_compra numeric)
RETURNS numeric
LANGUAGE sql STABLE AS $func$
  SELECT round(
    coalesce(p_compra, 0) +
    coalesce((SELECT sum(costo_soles) FROM costos WHERE codigo_producto = p_codigo), 0)
  , 2);
$func$;


-- ── 2. Al escribir un producto ──────────────────────────────
-- BEFORE, para corregir el valor en la misma fila que se esta grabando: no
-- dispara otro UPDATE y por lo tanto no puede entrar en bucle. Cubre a
-- pagar_credito, que hace UPDATE sobre inventario.
CREATE OR REPLACE FUNCTION kv_inv_precio_final() RETURNS TRIGGER AS $func$
BEGIN
  NEW.precio_final := kv_precio_final(NEW.codigo_producto, NEW.precio_compra_soles);
  RETURN NEW;
END;
$func$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_inv_precio_final ON inventario;
CREATE TRIGGER trg_inv_precio_final
  BEFORE INSERT OR UPDATE ON inventario
  FOR EACH ROW EXECUTE FUNCTION kv_inv_precio_final();


-- ── 3. Al agregar, cambiar o borrar un costo ────────────────
-- AFTER, porque la suma tiene que incluir (o ya no incluir) la fila que se
-- acaba de tocar. El UPDATE que hace dispara el trigger de arriba, que recalcula
-- lo mismo: sin recursion, porque aquel es BEFORE y no genera otro UPDATE.
CREATE OR REPLACE FUNCTION kv_costos_precio_final() RETURNS TRIGGER AS $func$
DECLARE
  cod text;
BEGIN
  cod := coalesce(NEW.codigo_producto, OLD.codigo_producto);
  UPDATE inventario
     SET precio_final = kv_precio_final(cod, precio_compra_soles)
   WHERE codigo_producto = cod;
  RETURN NULL;
END;
$func$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_costos_precio_final ON costos;
CREATE TRIGGER trg_costos_precio_final
  AFTER INSERT OR UPDATE OR DELETE ON costos
  FOR EACH ROW EXECUTE FUNCTION kv_costos_precio_final();


-- ── 4. Reparar lo que ya estuviera torcido ──────────────────
UPDATE inventario
   SET precio_final = kv_precio_final(codigo_producto, precio_compra_soles)
 WHERE precio_final IS DISTINCT FROM kv_precio_final(codigo_producto, precio_compra_soles);


-- ── COMPROBACION ────────────────────────────────────────────
-- Tiene que devolver 0 en `descuadrados`.
SELECT count(*) FILTER (
         WHERE abs(coalesce(precio_final,0)
                   - kv_precio_final(codigo_producto, precio_compra_soles)) > 0.01
       ) AS descuadrados,
       count(*) AS productos
FROM inventario;
