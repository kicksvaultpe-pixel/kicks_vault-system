-- =============================================
-- KICKZ SYSTEM — Setup Supabase
-- Pega esto en: Supabase → SQL Editor → Run
-- =============================================

-- 1. INVENTARIO
create table if not exists inventario (
  id bigint generated always as identity primary key,
  nombre text not null,
  categoria text default 'Sneakers',
  talla text,
  stock integer default 0,
  costo numeric(10,2) default 0,
  precio numeric(10,2) default 0,
  proveedor text,
  fecha date default current_date,
  notas text,
  created_at timestamptz default now()
);

-- 2. VENTAS
create table if not exists ventas (
  id bigint generated always as identity primary key,
  inventario_id bigint references inventario(id),
  producto text not null,
  cantidad integer default 1,
  precio_venta numeric(10,2) default 0,
  costo_unitario numeric(10,2) default 0,
  ganancia numeric(10,2) default 0,
  canal text,
  comprador text,
  fecha date default current_date,
  created_at timestamptz default now()
);

-- 3. TRANSACCIONES (Flujo de Caja)
create table if not exists transacciones (
  id bigint generated always as identity primary key,
  tipo text check (tipo in ('ingreso','gasto')) not null,
  descripcion text,
  monto numeric(10,2) default 0,
  categoria text,
  canal text,
  ganancia numeric(10,2),
  referencia_id bigint,
  fecha date default current_date,
  created_at timestamptz default now()
);

-- =============================================
-- Permisos públicos (anon key puede leer/escribir)
-- =============================================
alter table inventario enable row level security;
alter table ventas enable row level security;
alter table transacciones enable row level security;

create policy "public_all_inventario" on inventario for all using (true) with check (true);
create policy "public_all_ventas" on ventas for all using (true) with check (true);
create policy "public_all_transacciones" on transacciones for all using (true) with check (true);
