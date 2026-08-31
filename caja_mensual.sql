-- ============================================================
-- Caja de apertura de cada mes, tomada de los Excel del negocio:
--   2024-01 .. 2025-10  ->  "3. Flujo de Caja.xlsx" (SALDO INICIAL de cada hoja)
--   2025-11 .. 2026-07  ->  "Registro KV Excel.xlsx", hoja Registro de FLUJO
--   2026-08             ->  misma planilla, hoja FLUJO
--
-- Sin estas filas el tab Flujo deriva la caja mirando solo el mes anterior,
-- asi que arranca de cero y ningun mes cerrado cuadra.
-- Correr tal cual en el SQL Editor de Supabase.
-- ============================================================

DELETE FROM caja_mensual;

INSERT INTO caja_mensual (mes, caja_inicio) VALUES
  ('2024-01',      6000.00),
  ('2024-02',     11002.10),
  ('2024-03',      1790.01),
  ('2024-04',      7905.50),
  ('2024-05',      9782.00),
  ('2024-06',      3629.38),
  ('2024-07',       506.33),
  ('2024-08',      5668.83),
  ('2024-09',      7684.66),
  ('2024-10',     13227.90),
  ('2024-11',     12913.65),
  ('2024-12',     17594.59),
  ('2025-01',     22021.21),
  ('2025-02',     26360.06),
  ('2025-03',     27098.34),
  ('2025-04',     26007.37),
  ('2025-05',     29874.31),
  ('2025-06',     29234.70),
  ('2025-07',     24750.99),
  ('2025-08',     29001.67),
  ('2025-09',     28019.79),
  ('2025-10',     26842.56),
  ('2025-11',     29509.38),
  ('2025-12',     25773.01),
  ('2026-01',     43593.56),
  ('2026-02',     39215.40),
  ('2026-03',     39522.46),
  ('2026-04',     31526.93),
  ('2026-05',     21233.51),
  ('2026-06',     14587.30),
  ('2026-07',     11066.11),
  ('2026-08',     21538.25);

-- comprobacion: deben salir 32 filas, de 2024-01 a 2026-08
SELECT count(*) AS meses, min(mes) AS desde, max(mes) AS hasta FROM caja_mensual;
