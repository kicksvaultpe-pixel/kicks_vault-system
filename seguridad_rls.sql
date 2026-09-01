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


-- ── COMPROBACION ────────────────────────────────────────────
-- `rls` debe decir true en todas, y `politicas` 1 en todas.
SELECT c.relname AS tabla,
       c.relrowsecurity AS rls,
       count(pol.polname) AS politicas
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_policy pol ON pol.polrelid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'r'
GROUP BY c.relname, c.relrowsecurity
ORDER BY c.relrowsecurity, c.relname;
