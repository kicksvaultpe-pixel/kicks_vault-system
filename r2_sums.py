# -*- coding: utf-8 -*-
import openpyxl, datetime
from collections import defaultdict

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wv = openpyxl.load_workbook(P, data_only=True)

def num(x):
    return x if isinstance(x, (int, float)) else 0.0

def S(sheet, col, r1, r2):
    s = wv[sheet]
    return round(sum(num(s["%s%d" % (col, r)].value) for r in range(r1, r2 + 1)), 2)

print("=== SUMAS BASE ===")
s1_197_454 = S("STOCK 1", "G", 197, 454)
s1_197_418 = S("STOCK 1", "G", 197, 418)
s1_419_454 = S("STOCK 1", "G", 419, 454)
reg1_197_418 = S("Registro de STOCK 1", "G", 197, 418)
s2_600_695 = S("STOCK 2", "G", 600, 695)
reg2_600_695 = S("Registro de STOCK 2", "G", 600, 695)

print("STOCK 1 live      G197:G454 = %12.2f" % s1_197_454)
print("STOCK 1 live      G197:G418 = %12.2f" % s1_197_418)
print("STOCK 1 live      G419:G454 = %12.2f" % s1_419_454)
print("Reg STOCK 1       G197:G418 = %12.2f" % reg1_197_418)
print("  -> live - reg (G197:G418) = %12.2f   (backfill dentro del rango viejo)" % round(s1_197_418-reg1_197_418,2))
print("STOCK 2 live      G600:G695 = %12.2f" % s2_600_695)
print("Reg STOCK 2       G600:G695 = %12.2f" % reg2_600_695)
print("  -> live - reg (G600:G695) = %12.2f" % round(s2_600_695-reg2_600_695,2))

print("\n=== RECONSTRUCCION DE LAS FORMULAS ===")
print("O455 = %.2f - 84285.52 = %.2f   (excel dice 17319.09)" % (s1_197_454, round(s1_197_454-84285.52,2)))
print("O456 = %.2f - 234      = %.2f   (excel dice  4267.57)" % (s2_600_695, round(s2_600_695-234,2)))
print("O419 = %.2f - 72000 - 135.87 = %.2f (excel dice 15584.32)" % (reg1_197_418, round(reg1_197_418-72000-135.87,2)))
print("O420 = %.2f (excel dice 4501.57) -- OJO apunta a 'STOCK 2' LIVE" % s2_600_695)

print("\n=== CONSTANTES ===")
c_ago = 84285.52
c_jul = 72000 + 135.87
print("constante agosto  = %10.2f" % c_ago)
print("constante julio   = %10.2f" % c_jul)
print("delta constantes  = %10.2f" % round(c_ago - c_jul, 2))
print("constante STOCK2 agosto = 234.00 ; julio = 0.00 ; delta = 234.00")

print("\n=== FILAS NUEVAS EN STOCK 1 (419..454) por mes de A ===")
s = wv["STOCK 1"]
bym = defaultdict(lambda: [0, 0.0])
for r in range(419, 455):
    a = s["A%d" % r].value
    g = num(s["G%d" % r].value)
    if isinstance(a, datetime.datetime):
        k = "%04d-%02d" % (a.year, a.month)
    elif a is None:
        k = "(vacio)"
    else:
        k = str(a)
    bym[k][0] += 1
    bym[k][1] += g
for k in sorted(bym):
    print("  %-10s n=%3d  G=%10.2f" % (k, bym[k][0], round(bym[k][1], 2)))
