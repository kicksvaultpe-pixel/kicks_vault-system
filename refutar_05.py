# -*- coding: utf-8 -*-
import openpyxl, datetime

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb  = openpyxl.load_workbook(P, data_only=True)
wbf = openpyxl.load_workbook(P, data_only=False)
s1 = wb["STOCK 1"]; s2 = wb["STOCK 2"]; r1 = wb["Registro de STOCK 1"]; r2 = wb["Registro de STOCK 2"]
def f(v): return float(v) if isinstance(v,(int,float)) else 0.0
def mes(v):
    if isinstance(v,(datetime.datetime,datetime.date)): return f"{v.year}-{v.month:02d}"
    return "SIN-FECHA"

print("=== A) COLUMNA G ES REALMENTE E+F ? ===")
for r in [197, 364, 391, 400]:
    print(f"  STOCK 1 G{r} formula = {wbf['STOCK 1'][f'G{r}'].value!r}")
print(f"  STOCK 2 G600 formula = {wbf['STOCK 2']['G600'].value!r}")
print()

print("=== B) EL TRAMO 419-454 QUE LA FOTO NO CUBRIA: aporta algo? ===")
tot = 0.0; nz = 0
for r in range(419, 455):
    v = f(s1[f"G{r}"].value); tot += v
    if abs(v) > 0.001: nz += 1
print(f"  SUM('STOCK 1'!G419:G454) = {tot:,.2f}  en {nz} filas con valor distinto de cero")
print(f"  B en esas filas: {[s1[f'B{r}'].value for r in range(419,426)]}")
print(f"  -> la AMPLIACION del rango (G418 -> G454) aporta {tot:,.2f}. Todo el delta es revaluacion.")
print()

print("=== C) LAS CONSTANTES HARDCODEADAS ===")
lvl_s1 = 101604.61; lvl_s2 = 4501.57
ago_s1 = sum(f(s1[f"G{r}"].value) for r in range(197,455) if mes(s1[f"A{r}"].value)=="2026-08")
ago_s2 = sum(f(s2[f"G{r}"].value) for r in range(600,696) if mes(s2[f"A{r}"].value)=="2026-08")
n_s1 = sum(1 for r in range(197,455) if mes(s1[f"A{r}"].value)=="2026-08")
n_s2 = sum(1 for r in range(600,696) if mes(s2[f"A{r}"].value)=="2026-08")
print(f"  STOCK 1: nivel={lvl_s1:,.2f}  constante=84,285.52  -> resto = {lvl_s1-84285.52:,.2f}")
print(f"           valor de filas fechadas AGOSTO = {ago_s1:,.2f} ({n_s1} filas)")
print(f"           NO fechadas agosto = {lvl_s1-ago_s1:,.2f}  vs constante 84,285.52 -> desvio {lvl_s1-ago_s1-84285.52:,.2f}")
print(f"  STOCK 2: nivel={lvl_s2:,.2f}  constante=234  -> resto = {lvl_s2-234:,.2f}")
print(f"           valor de filas fechadas AGOSTO = {ago_s2:,.2f} ({n_s2} filas)")
print(f"           NO fechadas agosto = {lvl_s2-ago_s2:,.2f}  vs constante 234 -> desvio {lvl_s2-ago_s2-234:,.2f}")
print(f"  TOTAL agosto full = {ago_s1+ago_s2:,.2f} ({n_s1+n_s2} filas)")
print()
print("  La constante NO es el nivel de la foto anterior:")
print(f"    nivel foto S1 = 87,720.19  vs constante nueva 84,285.52 -> difieren {87720.19-84285.52:,.2f}")
print()

print("=== D) RECONCILIACION LIMPIA ===")
delta_total = 17771.86
delta_ago   = 722.58
ago_full    = ago_s1+ago_s2
print(f"  reportado COMPRAS MES (O457)            = 21,586.66")
print(f"  filas fechadas AGOSTO a valor completo  = {ago_full:,.2f}")
print(f"  hueco a explicar                        = {21586.66-ago_full:,.2f}")
print(f"  crecimiento total del analista          = {delta_total:,.2f}")
print(f"  parte del crecimiento sobre filas AGOSTO= {delta_ago:,.2f}  (YA contada en {ago_full:,.2f})")
print(f"  crecimiento sobre filas NO-agosto       = {delta_total-delta_ago:,.2f}  <== ESTE es el numero correcto")
print(f"  comprobacion: {ago_full:,.2f} + {delta_total-delta_ago:,.2f} = {ago_full+delta_total-delta_ago:,.2f}")
print()

print("=== E) FLUJO agosto: de donde sale 21,586.66 - 17,771.86 = 3,814.80 ? ===")
fl = wb["FLUJO"]
tot_soles = 0.0; n=0; nd=0; tot_usd=0.0
for r in range(2, fl.max_row+1):
    a = fl[f"A{r}"].value; b = fl[f"B{r}"].value
    if mes(a)!="2026-08" or b!="COMPRA": continue
    n+=1
    g = f(fl[f"G{r}"].value); h = f(fl[f"H{r}"].value)
    tot_soles += g; tot_usd += h
    if abs(g)>0.001: nd+=1
print(f"  FLUJO agosto COMPRA: {n} filas | EGRESO soles G = {tot_soles:,.2f} en {nd} filas | EGRESO usd H = {tot_usd:,.2f}")
print(f"  21,586.66 - 17,771.86 = 3,814.80  -> {'COINCIDE con el egreso en soles' if abs(tot_soles-3814.80)<0.01 else 'NO coincide'}")
