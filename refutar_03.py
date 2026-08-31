# -*- coding: utf-8 -*-
import openpyxl

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb = openpyxl.load_workbook(P, data_only=True)
s1 = wb["STOCK 1"]; r1 = wb["Registro de STOCK 1"]

print("=== STOCK 1: alineacion por CODIGO en 197..454 vs Registro 197..418 ===")
desal = 0
for r in range(197, 419):
    c1 = s1[f"B{r}"].value; c2 = r1[f"B{r}"].value
    if c1 != c2:
        desal += 1
        if desal <= 20:
            print(f"  DESALINEADA fila {r}: STOCK1 B={c1!r}  REG B={c2!r}")
print(f"  filas desalineadas 197-418: {desal}")
print()

print("=== De donde sale delta1 = 13,884.42 ? ===")
# parte A: filas 197-418 que existen en AMBAS hojas -> revaluacion
rev = 0.0; nrev = 0
detalle = []
for r in range(197, 419):
    g1 = s1[f"G{r}"].value; g2 = r1[f"G{r}"].value
    v1 = float(g1) if isinstance(g1,(int,float)) else 0.0
    v2 = float(g2) if isinstance(g2,(int,float)) else 0.0
    if abs(v1-v2) > 0.001:
        rev += (v1-v2); nrev += 1
        detalle.append((r, s1[f"B{r}"].value, s1[f"A{r}"].value, v2, v1, v1-v2))
# parte B: filas 419-454 -> solo existen en la hoja viva
nue = 0.0; nnue = 0
nuevas = []
for r in range(419, 455):
    g1 = s1[f"G{r}"].value
    v1 = float(g1) if isinstance(g1,(int,float)) else 0.0
    if isinstance(g1,(int,float)):
        nnue += 1
    if abs(v1) > 0.001:
        nuevas.append((r, s1[f"B{r}"].value, s1[f"A{r}"].value, v1))
    nue += v1
print(f"  A) REVALUACION filas 197-418 (existen en las dos fotos): {rev:>12,.2f}  en {nrev} filas")
print(f"  B) FILAS NUEVAS 419-454 (fuera del rango de la foto):     {nue:>12,.2f}  en {len(nuevas)} filas con valor != 0 ({nnue} celdas numericas)")
print(f"  A + B = {rev+nue:,.2f}   (delta1 debe ser 13,884.42)")
print()
print("  --- filas 197-418 que CAMBIARON de valor (revaluacion) ---")
for d in detalle:
    print(f"    fila {d[0]:<5} {str(d[1]):<12} fecha={str(d[2])[:10]:<12} antes={d[3]:>10,.2f} ahora={d[4]:>10,.2f} delta={d[5]:>10,.2f}")
print()
print("  --- filas 419-454 con valor ---")
for d in nuevas:
    print(f"    fila {d[0]:<5} {str(d[1]):<12} fecha={str(d[2])[:10]:<12} G={d[3]:>10,.2f}")
