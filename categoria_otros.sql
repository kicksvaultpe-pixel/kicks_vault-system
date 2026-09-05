-- ============================================================
-- Reclasificar productos que hoy dicen ACCESORIOS y en realidad no lo son.
--
-- De los 280 productos en ACCESORIOS, solo 63 son accesorios de verdad (lentes,
-- bolsos, medias, relojes). El resto son dos cosas distintas que se colaron ahi:
--
--   1. Cuidado y mantenimiento (154): laces, shields, hormas, cleaner, uv light,
--      y los kits de limpieza que estan cargados bajo la "marca" TABAZ Y
--      CARTERAZ (no es una marca real, es como quedo etiquetado el kit).
--   2. Coleccionables (63): LABUBU (46 de los 63), peluches, Bearbrick, cartas,
--      encendedor. No se usan puestos, son otra linea de negocio.
--
-- Los dos grupos van a OTROS. Se identifica por (marca, modelo) exacto, no por
-- palabras sueltas, para no arrastrar por error otros productos de las mismas
-- marcas que si son accesorios (los bolsos y medias de SUPREME se quedan).
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================

-- ── ANTES: como esta hoy ────────────────────────────────────
SELECT categoria, count(*) AS n
FROM inventario
WHERE (marca, modelo) IN (
  ('SIN MARCA','LACES'), ('SIN MARCA','SHIELDS'), ('SIN MARCA','SHIELDS PRO'),
  ('SIN MARCA','HORMAS'), ('SIN MARCA','CLEANER'), ('SIN MARCA','UV LIGHT'),
  ('TABAZ Y CARTERAZ','KIT DE LIMPIEZA'), ('TABAZ Y CARTERAZ','KIT GAMUZA'),
  ('POP MARKET','LABUBU'), ('SIN MARCA','PELUCHE'), ('BEARBRICK','BATMAN'),
  ('SUPREME','PLAYING CARDS'), ('SUPREME','LIGHTER')
)
GROUP BY categoria;

-- ── EL CAMBIO ────────────────────────────────────────────────
UPDATE inventario
SET categoria = 'OTROS'
WHERE categoria = 'ACCESORIOS'
  AND (marca, modelo) IN (
    -- grupo 1: cuidado y mantenimiento
    ('SIN MARCA','LACES'),
    ('SIN MARCA','SHIELDS'),
    ('SIN MARCA','SHIELDS PRO'),
    ('SIN MARCA','HORMAS'),
    ('SIN MARCA','CLEANER'),
    ('SIN MARCA','UV LIGHT'),
    ('TABAZ Y CARTERAZ','KIT DE LIMPIEZA'),
    ('TABAZ Y CARTERAZ','KIT GAMUZA'),
    -- grupo 2: coleccionables
    ('POP MARKET','LABUBU'),
    ('SIN MARCA','PELUCHE'),
    ('BEARBRICK','BATMAN'),
    ('SUPREME','PLAYING CARDS'),
    ('SUPREME','LIGHTER')
  );

-- Limpieza aparte: HORMAS quedo con dos formas de decir "sin colorway" — la
-- mitad con un guion literal y la mitad vacio. Se unifica a NULL.
UPDATE inventario
SET colorway = NULL
WHERE marca = 'SIN MARCA' AND modelo = 'HORMAS' AND colorway = '-';

-- ── DESPUES: comprobacion ────────────────────────────────────
-- Las 13 combinaciones (marca,modelo) de arriba deberian salir todas en OTROS,
-- ninguna en ACCESORIOS. Y el total de OTROS deberia haber subido en 217.
SELECT categoria, count(*) AS n
FROM inventario
WHERE (marca, modelo) IN (
  ('SIN MARCA','LACES'), ('SIN MARCA','SHIELDS'), ('SIN MARCA','SHIELDS PRO'),
  ('SIN MARCA','HORMAS'), ('SIN MARCA','CLEANER'), ('SIN MARCA','UV LIGHT'),
  ('TABAZ Y CARTERAZ','KIT DE LIMPIEZA'), ('TABAZ Y CARTERAZ','KIT GAMUZA'),
  ('POP MARKET','LABUBU'), ('SIN MARCA','PELUCHE'), ('BEARBRICK','BATMAN'),
  ('SUPREME','PLAYING CARDS'), ('SUPREME','LIGHTER')
)
GROUP BY categoria;

SELECT coalesce(categoria,'(vacío)') AS categoria, count(*) AS n
FROM inventario
GROUP BY categoria
ORDER BY 2 DESC;
