# -*- coding: utf-8 -*-
import openpyxl, sys
io = sys.stdout
P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"

wbF = openpyxl.load_workbook(P, data_only=False)
wbV = openpyxl.load_workbook(P, data_only=True)

print("HOJAS:", wbF.sheetnames)
for n in wbF.sheetnames:
    print(n, "dims", wbF[n].dimensions, "max_row", wbF[n].max_row, "max_col", wbF[n].max_column)

print("\n--- Cabeceras COMPRA ---")
sc = wbV["COMPRA"]
for r in range(1,4):
    print(r, [sc.cell(r,c).value for c in range(1,12)])

print("\n--- Cabeceras STOCK 1 ---")
s1 = wbV["STOCK 1"]
for r in range(1,4):
    print(r, [s1.cell(r,c).value for c in range(1,16)])

print("\n--- N455:O457 STOCK 1 (formula / valor) ---")
s1f = wbF["STOCK 1"]
for r in range(450,462):
    print(r, [s1f.cell(r,c).value for c in range(13,16)], "||", [s1.cell(r,c).value for c in range(13,16)])

print("\n--- Registro de STOCK 1 N415:O425 ---")
rf = wbF["Registro de STOCK 1"]; rv = wbV["Registro de STOCK 1"]
for r in range(414,426):
    print(r, [rf.cell(r,c).value for c in range(13,16)], "||", [rv.cell(r,c).value for c in range(13,16)])
