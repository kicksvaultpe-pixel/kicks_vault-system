-- =============================================
-- KICKS VAULT SYSTEM — Supabase Setup v2
-- Pega esto en: Supabase → SQL Editor → Run
-- =============================================

-- =============================================
-- 1. CLIENTES
-- =============================================
create table if not exists clientes (
  id_cliente      bigint generated always as identity primary key,
  nombre          text not null,
  telefono        text,
  instagram       text,
  talla_frecuente text,
  notas           text,
  fecha_registro  date default current_date,
  created_at      timestamptz default now()
);

-- =============================================
-- 2. INVENTARIO
-- =============================================
create table if not exists inventario (
  fecha_compra          date default current_date,
  codigo_producto       text primary key,  -- P-00001
  marca                 text not null,
  silueta               text,
  colorway              text,
  categoria             text default 'ZAPATILLAS'
                          check (categoria in ('ZAPATILLAS','ROPA','ACCESORIOS','OTROS')),
  talla                 text,
  precio_compra_usd     numeric(10,2),
  tipo_cambio           numeric(6,3),
  precio_compra_soles   numeric(10,2),
  precio_final          numeric(10,2),     -- precio_compra_soles + sum(costos)
  precio_venta_sugerido numeric(10,2),
  estado                text default 'DISPONIBLE'
                          check (estado in ('DISPONIBLE','VENDIDO')),
  factura               text,
  descripcion_factura   text,
  comentarios           text,
  created_at            timestamptz default now()
);

-- =============================================
-- 3. COSTOS (adicionales por producto)
-- =============================================
create table if not exists costos (
  id              bigint generated always as identity primary key,
  codigo_producto text references inventario(codigo_producto) on delete cascade,
  concepto        text not null,  -- DHL, ADUANA, LIMPIEZA, REPARACION, OTRO
  costo_soles     numeric(10,2) not null,
  fecha           date default current_date,
  created_at      timestamptz default now()
);

-- =============================================
-- 4. VENTAS
-- =============================================
create table if not exists ventas (
  codigo_venta       text primary key,  -- V-00001
  codigo_producto    text references inventario(codigo_producto),
  id_cliente         bigint references clientes(id_cliente),
  precio_venta_soles numeric(10,2) not null,
  canal              text default 'INSTAGRAM'
                       check (canal in ('INSTAGRAM','WHATSAPP','PRESENCIAL','OTRO')),
  comprador          text,
  ganancia           numeric(10,2),   -- calculado: precio_venta - precio_final
  rentabilidad       numeric(6,4),    -- ganancia / precio_final
  fecha              date default current_date,
  created_at         timestamptz default now()
);

-- =============================================
-- 5. RESERVAS
-- =============================================
create table if not exists reservas (
  id_reserva      bigint generated always as identity primary key,
  codigo_producto text references inventario(codigo_producto),  -- NULL si es a pedido
  marca           text,
  silueta         text,
  colorway        text,
  talla           text,
  id_cliente      bigint references clientes(id_cliente),
  monto_adelanto  numeric(10,2) default 0,
  canal           text default 'INSTAGRAM'
                    check (canal in ('INSTAGRAM','WHATSAPP','PRESENCIAL','OTRO')),
  tipo            text default 'EN_STOCK'
                    check (tipo in ('EN_STOCK','A_PEDIDO')),
  fecha           date default current_date,
  fecha_limite    date,
  notas           text,
  created_at      timestamptz default now()
);

-- =============================================
-- 6. PAGOS (gastos operativos)
-- =============================================
create table if not exists pagos (
  id          bigint generated always as identity primary key,
  concepto    text not null,
  monto_soles numeric(10,2) not null,  -- siempre negativo
  categoria   text default 'OPERATIVO'
                check (categoria in ('OPERATIVO','PERSONAL','IMPORTACION','MARKETING')),
  fecha       date default current_date,
  created_at  timestamptz default now()
);

-- =============================================
-- 7. FLUJO_CAJA (se llena automático via triggers)
-- =============================================
create table if not exists flujo_caja (
  id            bigint generated always as identity primary key,
  fecha         date not null,
  tipo          text check (tipo in ('COMPRA','VENTA','COSTO','PAGO')),
  referencia_id text,   -- codigo_producto, codigo_venta, etc.
  descripcion   text,
  ingreso_soles numeric(10,2) default 0,
  egreso_soles  numeric(10,2) default 0,
  created_at    timestamptz default now()
);

-- =============================================
-- SECUENCIA PARA CODIGOS AUTOMATICOS
-- =============================================

-- Función para generar codigo_producto (P-00001)
create sequence if not exists seq_producto start 1;

create or replace function gen_codigo_producto()
returns text language plpgsql as $$
begin
  return 'P-' || lpad(nextval('seq_producto')::text, 5, '0');
end;
$$;

-- Función para generar codigo_venta (V-00001)
create sequence if not exists seq_venta start 1;

create or replace function gen_codigo_venta()
returns text language plpgsql as $$
begin
  return 'V-' || lpad(nextval('seq_venta')::text, 5, '0');
end;
$$;

-- =============================================
-- TRIGGERS — flujo_caja automático
-- =============================================

-- Al insertar en inventario → egreso en flujo_caja
create or replace function trigger_compra_flujo()
returns trigger language plpgsql as $$
begin
  insert into flujo_caja (fecha, tipo, referencia_id, descripcion, egreso_soles)
  values (
    NEW.fecha_compra,
    'COMPRA',
    NEW.codigo_producto,
    NEW.marca || ' ' || coalesce(NEW.silueta,'') || ' ' || coalesce(NEW.colorway,'') || ' (' || coalesce(NEW.talla,'') || ')',
    coalesce(NEW.precio_compra_soles, 0)
  );
  return NEW;
end;
$$;

create trigger after_compra
after insert on inventario
for each row execute function trigger_compra_flujo();

-- Al insertar en costos → egreso en flujo_caja + actualizar precio_final en inventario
create or replace function trigger_costo_flujo()
returns trigger language plpgsql as $$
declare
  v_nombre text;
  v_total_costos numeric;
  v_precio_compra numeric;
begin
  -- Actualizar precio_final en inventario
  select 
    marca || ' ' || coalesce(silueta,'') || ' ' || coalesce(colorway,''),
    precio_compra_soles
  into v_nombre, v_precio_compra
  from inventario where codigo_producto = NEW.codigo_producto;

  select coalesce(sum(costo_soles), 0) into v_total_costos
  from costos where codigo_producto = NEW.codigo_producto;

  update inventario
  set precio_final = v_precio_compra + v_total_costos
  where codigo_producto = NEW.codigo_producto;

  -- Registrar en flujo_caja
  insert into flujo_caja (fecha, tipo, referencia_id, descripcion, egreso_soles)
  values (NEW.fecha, 'COSTO', NEW.codigo_producto, NEW.concepto || ' — ' || v_nombre, NEW.costo_soles);

  return NEW;
end;
$$;

create trigger after_costo
after insert on costos
for each row execute function trigger_costo_flujo();

-- Al insertar en ventas → ingreso en flujo_caja + marcar VENDIDO en inventario
create or replace function trigger_venta_flujo()
returns trigger language plpgsql as $$
declare
  v_nombre text;
  v_precio_final numeric;
begin
  select 
    marca || ' ' || coalesce(silueta,'') || ' ' || coalesce(colorway,''),
    precio_final
  into v_nombre, v_precio_final
  from inventario where codigo_producto = NEW.codigo_producto;

  -- Marcar como VENDIDO
  update inventario set estado = 'VENDIDO'
  where codigo_producto = NEW.codigo_producto;

  -- Calcular ganancia y rentabilidad
  update ventas set
    ganancia = NEW.precio_venta_soles - coalesce(v_precio_final, 0),
    rentabilidad = case 
      when coalesce(v_precio_final, 0) > 0 
      then round((NEW.precio_venta_soles - v_precio_final) / v_precio_final, 4)
      else 0 
    end
  where codigo_venta = NEW.codigo_venta;

  -- Registrar en flujo_caja
  insert into flujo_caja (fecha, tipo, referencia_id, descripcion, ingreso_soles)
  values (NEW.fecha, 'VENTA', NEW.codigo_venta, 'Venta: ' || v_nombre, NEW.precio_venta_soles);

  return NEW;
end;
$$;

create trigger after_venta
after insert on ventas
for each row execute function trigger_venta_flujo();

-- Al insertar en pagos → egreso en flujo_caja
create or replace function trigger_pago_flujo()
returns trigger language plpgsql as $$
begin
  insert into flujo_caja (fecha, tipo, referencia_id, descripcion, egreso_soles)
  values (NEW.fecha, 'PAGO', NEW.id::text, NEW.concepto, abs(NEW.monto_soles));
  return NEW;
end;
$$;

create trigger after_pago
after insert on pagos
for each row execute function trigger_pago_flujo();

-- =============================================
-- RLS — Row Level Security
-- =============================================
alter table clientes     enable row level security;
alter table inventario   enable row level security;
alter table costos       enable row level security;
alter table ventas       enable row level security;
alter table reservas     enable row level security;
alter table pagos        enable row level security;
alter table flujo_caja   enable row level security;

-- Políticas temporales (abiertas hasta implementar login)
create policy "public_clientes"    on clientes    for all using (true) with check (true);
create policy "public_inventario"  on inventario  for all using (true) with check (true);
create policy "public_costos"      on costos      for all using (true) with check (true);
create policy "public_ventas"      on ventas      for all using (true) with check (true);
create policy "public_reservas"    on reservas    for all using (true) with check (true);
create policy "public_pagos"       on pagos       for all using (true) with check (true);
create policy "public_flujo_caja"  on flujo_caja  for all using (true) with check (true);

-- =============================================
-- FIN
-- =============================================
