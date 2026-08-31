# -*- coding: utf-8 -*-
import openpyxl, datetime

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb = openpyxl.load_workbook(P, data_only=True)
s1 = wb["STOCK 1"]; r1 = wb["Registro de STOCK 1"]
s2 = wb["STOCK 2"]; r2 = wb["Registro de STOCK 2"]

def f(v): return float(v) if isinstance(v,(int,float)) else 0.0
def mes(v):
    if isinstance(v, datetime.datetime): return f"{v.year}-{v.month:02d}"
    if isinstance(v, datetime.date): return f"{v.year}-{v.month:02d}"
    return "SIN-FECHA"

print("=== 1) DESCOMPONER EL DELTA EN 'PRECIO DE COMPRA' (E) vs 'COSTOS' (F) ===")
tot_e = tot_f = 0.0
rows = []
for sh_l, sh_p, lo, hi, tag in [(s1,r1,197,418,"STOCK 1"), (s2,r2,600,695,"STOCK 2")]:
    for r in range(lo, hi+1):
        dg = f(sh_l[f"G{r}"].value) - f(sh_p[f"G{r}"].value)
        if abs(dg) < 0.001: continue
        de = f(sh_l[f"E{r}"].value) - f(sh_p[f"E{r}"].value)
        df = f(sh_l[f"F{r}"].value) - f(sh_p[f"F{r}"].value)
        tot_e += de; tot_f += df
        rows.append((tag, r, sh_l[f"B{r}"].value, mes(sh_l[f"A{r}"].value), de, df, dg))
print(f"  filas con delta != 0 : {len(rows)}")
print(f"  delta por PRECIO DE COMPRA (E) : {tot_e:>12,.2f}")
print(f"  delta por COSTOS          (F) : {tot_f:>12,.2f}")
print(f"  suma                          : {tot_e+tot_f:>12,.2f}   (analista: 17,771.86)")
print()
print("  Filas donde el delta es SOLO costos (E no cambio) -> NO es una compra:")
solo_costo = [x for x in rows if abs(x[4]) < 0.001 and abs(x[5]) > 0.001]
sc = sum(x[6] for x in solo_costo)
for x in solo_costo:
    print(f"    {x[0]} fila {x[1]:<5} {str(x[2]):<11} mes-compra={x[3]:<10} dE={x[4]:>9,.2f} dF={x[5]:>9,.2f} dG={x[6]:>9,.2f}")
print(f"    -> subtotal SOLO COSTOS: {sc:,.2f} en {len(solo_costo)} filas")
print()

print("=== 2) STOCK 2: cuales son las filas que crecen? ===")
n2 = 0; t2 = 0.0
for r in range(600, 696):
    dg = f(s2[f"G{r}"].value) - f(r2[f"G{r}"].value)
    if abs(dg) > 0.001:
        n2 += 1; t2 += dg
        print(f"    fila {r:<5} {str(s2[f'B{r}'].value):<11} mes-compra={mes(s2[f'A{r}'].value):<10} "
              f"antes={f(r2[f'G{r}'].value):>8,.2f} ahora={f(s2[f'G{r}'].value):>8,.2f} dG={dg:>9,.2f}")
print(f"    -> {n2} filas, total {t2:,.2f}  (analista dice 7 filas / 3,887.44)")
print()

print("=== 3) DELTA AGRUPADO POR MES DE LA FECHA DE COMPRA (columna A) ===")
por_mes = {}
for x in rows:
    por_mes.setdefault(x[3], [0.0,0])
    por_mes[x[3]][0] += x[6]; por_mes[x[3]][1] += 1
for k in sorted(por_mes):
    print(f"    {k:<10} {por_mes[k][0]:>12,.2f}  ({por_mes[k][1]} filas)")
ago = por_mes.get("2026-08",[0,0])[0]
print(f"    -> la parte del delta que cae en filas YA fechadas en AGOSTO: {ago:,.2f}")
print()

print("=== 4) LA APP CUENTA LAS FILAS DE AGOSTO A VALOR COMPLETO. SOLAPAMIENTO ===")
ago_full = 0.0; nfull = 0
for sh, lo, hi in [(s1,197,454),(s2,600,695)]:
    for r in range(lo,hi+1):
        if mes(sh[f"A{r}"].value) == "2026-08":
            ago_full += f(sh[f"G{r}"].value); nfull += 1
print(f"  Filas fechadas AGOSTO dentro de los dos rangos, a valor COMPLETO: {ago_full:,.2f} ({nfull} filas)")
print(f"  (contexto dice que la app calcula 4,537.38)")
print(f"  Delta del analista que cae sobre esas mismas filas          : {ago:,.2f}  <-- SOLAPAMIENTO")
print()
print(f"  4,537.38 + 17,771.86            = {4537.38+17771.86:,.2f}")
print(f"  4,537.38 + 17,771.86 - {ago:,.2f} = {4537.38+17771.86-ago:,.2f}   (reportado: 21,586.66)")
print()
print("=== 5) EL 17,771.86 CONTRA EL 21,586.66 REPORTADO ===")
print(f"  21,586.66 - 17,771.86 = {21586.66-17771.86:,.2f}")
