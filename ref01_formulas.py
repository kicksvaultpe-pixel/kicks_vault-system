# -*- coding: utf-8 -*-
import openpyxl
p = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wf = openpyxl.load_workbook(p, data_only=False)
wv = openpyxl.load_workbook(p, data_only=True)

print("=== STOCK 1 N455:O457 ===")
for r in range(452, 460):
    for c in ("M","N","O","P"):
        f = wf["STOCK 1"][f"{c}{r}"].value
        v = wv["STOCK 1"][f"{c}{r}"].value
        if f is not None or v is not None:
            print(f"  {c}{r}: F={f!r} V={v!r}")

print("=== Registro de STOCK 1 N419:O421 ===")
for r in range(416, 424):
    for c in ("M","N","O","P"):
        f = wf["Registro de STOCK 1"][f"{c}{r}"].value
        v = wv["Registro de STOCK 1"][f"{c}{r}"].value
        if f is not None or v is not None:
            print(f"  {c}{r}: F={f!r} V={v!r}")
