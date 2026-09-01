-- ============================================================
-- Permitir la categoria INTERES en pagos.
--
-- El tab de Inversion parte cada cuota en dos: el capital va a flujo_caja como
-- INVERSION (sale de la caja pero se convierte en activo fijo) y el interes va
-- a `pagos` con categoria INTERES (gasto puro, baja el margen).
--
-- Pero `pagos_categoria_check` solo admite OPERATIVO, PERSONAL, IMPORTACION y
-- MARKETING, asi que el interes se rechazaba. Y como ese insert no revisaba el
-- error, fallaba callado: la pantalla decia "Cuota registrada" mientras los
-- S/ 1,366.66 de interes de la INV-0007 no se guardaban en ningun lado.
--
-- El tab de Flujo ya cuenta INTERES dentro de los gastos del mes, asi que en
-- cuanto la fila exista aparece sola.
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================

ALTER TABLE pagos DROP CONSTRAINT IF EXISTS pagos_categoria_check;
ALTER TABLE pagos ADD  CONSTRAINT pagos_categoria_check
  CHECK (categoria IS NULL OR categoria IN
    ('OPERATIVO','PERSONAL','IMPORTACION','MARKETING','INTERES'));

-- comprobacion: deberia listar las categorias en uso sin error
SELECT coalesce(categoria,'(sin categoria)') AS categoria,
       count(*)          AS gastos,
       sum(-monto_soles) AS total_soles
FROM pagos
GROUP BY categoria
ORDER BY 2 DESC;
