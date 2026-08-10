# Kicks Vault — Sistema de Gestión

Sistema de inventario, ventas y flujo de caja para negocio de sneakers y prendas.

## Stack
- Frontend: HTML/CSS/JS (single file, dark theme, mobile-ready)
- Base de datos: Supabase (PostgreSQL)
- Hosting: Vercel

## Setup

1. Crear proyecto en [Supabase](https://supabase.com)
2. Ejecutar `database/supabase-setup-v2.sql` en el SQL Editor
3. Ejecutar `database/supabase-update-v3.sql` para la lógica de crédito
4. Copiar la URL y anon key de Supabase en `index.html` (líneas con `SUPA_URL` y `SUPA_KEY`)
5. Deploy en Vercel apuntando a este repo

## Base de datos

Los schemas SQL están en la carpeta `/database`:

| Archivo | Descripción |
|---|---|
| `supabase-setup-v2.sql` | Schema principal — 7 tablas + triggers + secuencias |
| `supabase-update-v3.sql` | Migración v3 — lógica CONTADO/CRÉDITO |
| `seed-data.sql` | Datos de prueba (27 productos) |
