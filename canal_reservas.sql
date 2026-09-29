-- Agrega el canal de venta a Reservas -- hoy solo lo tenia Ventas, y una
-- reserva que se completaba quedaba con canal fijo en 'PRESENCIAL' sin
-- importar por donde llego el cliente de verdad.
--
-- Sin valor por defecto a proposito: una reserva vieja sin este dato no
-- se debe rellenar con un canal inventado, mejor que quede en blanco.

ALTER TABLE reservas
  ADD COLUMN IF NOT EXISTS canal text
    CHECK (canal IN ('INSTAGRAM','WHATSAPP','FACEBOOK','PRESENCIAL','OTRO'));
