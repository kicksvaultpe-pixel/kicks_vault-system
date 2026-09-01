-- ============================================================
-- Cerrar la base a quien no tenga sesion.
--
-- Hoy la clave publica que viaja en index.html permite leer Y escribir todas
-- las tablas: 1239 ventas, 24 clientes, 1065 productos, todo el flujo de caja.
-- Cualquiera que abra el codigo fuente de la pagina la tiene.
--
-- Esa clave es publica por diseño y no hay nada malo en que se vea. Lo que
-- falta es lo otro: que la base decida quien pasa. Con RLS activo, la clave
-- deja de ser una llave maestra y pasa a ser un simple identificador de
-- proyecto — quien manda es la politica.
--
-- IMPORTANTE — el orden importa:
--   1. Crear el usuario en Supabase: Authentication > Users > Add user.
--   2. Publicar el index.html con el login (ya esta en el repo).
--   3. Comprobar que puedes entrar con tu correo y contraseña.
--   4. RECIEN AHI correr este archivo.
-- Si lo corres antes del paso 3, la app deja de ver los datos y te quedas
-- afuera hasta que subas el login.
--
-- Correr en el SQL Editor de Supabase.
-- ============================================================


-- ── 1. RLS en todas las tablas ──────────────────────────────
-- Se recorre el esquema en vez de nombrarlas una por una: asi cubre tambien
-- las que se creen mañana, y no depende de que la lista este completa.
DO $do$
DECLARE
  t record;
BEGIN
  FOR t IN SELECT tablename FROM pg_tables WHERE schemaname = 'public'
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t.tablename);
    EXECUTE format('DROP POLICY IF EXISTS kv_solo_autenticados ON public.%I', t.tablename);
    EXECUTE format(
      'CREATE POLICY kv_solo_autenticados ON public.%I '
      'FOR ALL TO authenticated USING (true) WITH CHECK (true)',
      t.tablename);
  END LOOP;
END
$do$;


-- ── 2. Las funciones tambien ────────────────────────────────
-- Una funcion SECURITY DEFINER se salta el RLS: si `anon` puede llamarla, la
-- puerta de arriba no sirve de nada. pagar_credito mueve plata y los
-- gen_codigo_* escriben, asi que se le quita el permiso de ejecucion a anon
-- sobre todo el esquema. Los triggers no se ven afectados: corren dentro de la
-- sentencia, no por permiso de quien llama.
DO $do$
DECLARE
  f record;
BEGIN
  FOR f IN
    SELECT p.oid::regprocedure AS firma
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE n.nspname = 'public'
  LOOP
    EXECUTE format('REVOKE EXECUTE ON FUNCTION %s FROM anon', f.firma);
  END LOOP;
END
$do$;


-- ── 3. Sacar las politicas viejas que dejaban pasar a cualquiera ──
-- El setup original creo una politica por tabla con rol PUBLIC y comando ALL:
-- public_ventas, public_clientes, public_inventario, public_pagos,
-- public_costos, public_flujo_caja y caja_mensual_all. PUBLIC incluye a `anon`,
-- que es el rol con el que entra cualquiera desde el navegador.
--
-- Las politicas de RLS se SUMAN: basta con que una permita para que se entre.
-- Mientras esas siete existan, agregar kv_solo_autenticados no cierra nada
-- —comprobado leyendo 1239 ventas y 24 clientes sin sesion, y escribiendo un
-- gasto de prueba— asi que hay que eliminarlas.
--
-- Solo toca el esquema `public`: no roza nada de Supabase Auth ni Storage.
DO $do$
DECLARE
  p record;
BEGIN
  FOR p IN
    SELECT c.relname AS tabla, pol.polname AS politica
    FROM pg_policy pol
    JOIN pg_class c ON c.oid = pol.polrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public'
      AND pol.polname <> 'kv_solo_autenticados'
  LOOP
    RAISE NOTICE 'Eliminando % en %', p.politica, p.tabla;
    EXECUTE format('DROP POLICY %I ON public.%I', p.politica, p.tabla);
  END LOOP;
END
$do$;


-- ── COMPROBACION ────────────────────────────────────────────
-- `rls` debe decir true en todas, y `politicas` EXACTAMENTE 1 en todas.
-- Si alguna dice 2, le quedo una politica vieja abierta.
SELECT c.relname AS tabla,
       c.relrowsecurity AS rls,
       count(pol.polname) AS politicas
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_policy pol ON pol.polrelid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'r'
GROUP BY c.relname, c.relrowsecurity
ORDER BY c.relrowsecurity, c.relname;
