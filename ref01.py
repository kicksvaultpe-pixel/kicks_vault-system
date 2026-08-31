# -*- coding: utf-8 -*-
import openpyxl
from decimal import Decimal

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"

wbf = openpyxl.load_workbook(P, data_only=False)
wbv = openpyxl.load_workbook(P, data_only=True)

print("=== HOJAS ===")
print(wbf.sheetnames)

for sh, rng in [("STOCK 1", ["N455","O455","N456","O456","N457","O457"]),
                ("Registro de STOCK 1", ["N419","O419","N420","O420","N421","O421"])]:
    print("\n=== %s ===" % sh)
    f = wbf[sh]; v = wbv[sh]
    for c in rng:
        print("  %-6s formula=%-45r  valor=%r" % (c, f[c].value, v[c].value))

# Buscar cualquier celda con 84285.52 o similar en STOCK 1
print("\n=== busca constantes en formulas de STOCK 1 / STOCK 2 / Registro ===")
for sh in ["STOCK 1","STOCK 2","Registro de STOCK 1","Registro de STOCK 2"]:
    f = wbf[sh]
    for row in f.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                if "SUM(G" in c.value.replace(" ",""):
                    print("  %s!%s = %r  (val=%r)" % (sh, c.coordinate, c.value, wbv[sh][c.coordinate].value))
