# -*- coding: utf-8 -*-
import openpyxl, datetime
from collections import defaultdict

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wv = openpyxl.load_workbook(P, data_only=True)

def num(x):
    return round(x, 2) if isinstance(x, (int, float)) else 0.0

def mk(x):
    if isinstance(x, datetime.datetime):
        return "%04d-%02d" % (x.year, x.month)
    return "(vacio)" if x is None else str(x)[:10]

def rows(sheet, r1, r2):
    s = wv[sheet]
    out = {}
    for r in range(r1, r2 + 1):
        cod = s["B%d" % r].value
        out[r] = dict(row=r, cod=cod, fecha=s["A%d" % r].value, mes=mk(s["A%d" % r].value),
                      desc=s["C%d" % r].value, E=num(s["E%d" % r].value),
                      F=num(s["F%d" % r].value), G=num(s["G%d" % r].value),
                      H=s["H%d" % r].value)
    return out

# ---------- STOCK 1: rango viejo 197..418, live vs registro ----------
L1 = rows("STOCK 1", 197, 418)
R1 = rows("Registro de STOCK 1", 197, 418)

print("=== STOCK 1: filas del rango VIEJO (197..418) que CAMBIARON de G ===")
tot_new = 0.0   # G aparecio donde antes 0
tot_chg = 0.0   # G cambio de un valor a otro
n_new = n_chg = 0
changed = []
for r in range(197, 419):
    a, b = L1[r], R1[r]
    if abs(a["G"] - b["G"]) > 0.005:
        d = round(a["G"] - b["G"], 2)
        changed.append((r, b["G"], a["G"], d, a["mes"], a["cod"], a["H"], str(a["desc"])[:34]))
        if b["G"] == 0:
            tot_new += d; n_new += 1
        else:
            tot_chg += d; n_chg += 1
print("  %-5s %10s %10s %10s  %-8s %-9s %-11s %s" % ("fila","G_jul","G_ago","delta","mesA","codigo","estado","desc"))
for c in changed:
    print("  %-5d %10.2f %10.2f %10.2f  %-8s %-9s %-11s %s" % c)
print("  filas con G nuevo (0 -> x): n=%d  suma=%.2f" % (n_new, round(tot_new,2)))
print("  filas con G modificado    : n=%d  suma=%.2f" % (n_chg, round(tot_chg,2)))
print("  DELTA TOTAL G197:G418     : %.2f" % round(tot_new+tot_chg,2))

# ---------- Filas fechadas AGOSTO ----------
print("\n=== STOCK 1 (197..418): filas con FECHA de AGOSTO 2026 ===")
tot_ago_live = tot_ago_reg = 0.0
print("  %-5s %-11s %-9s %10s %10s  %-11s %s" % ("fila","fecha","codigo","G_live","G_jul","estado","desc"))
for r in range(197, 419):
    a = L1[r]
    if a["mes"] == "2026-08":
        b = R1[r]
        tot_ago_live += a["G"]; tot_ago_reg += b["G"]
        print("  %-5d %-11s %-9s %10.2f %10.2f  %-11s %s" % (
            r, a["fecha"].strftime("%Y-%m-%d"), a["cod"], a["G"], b["G"], a["H"], str(a["desc"])[:32]))
print("  SUMA G live (agosto, STOCK 1) = %.2f" % round(tot_ago_live,2))
print("  SUMA G jul  (agosto, STOCK 1) = %.2f  <-- 'ya valorizadas en la foto de julio'" % round(tot_ago_reg,2))

# ---------- STOCK 2 ----------
L2 = rows("STOCK 2", 600, 695)
R2 = rows("Registro de STOCK 2", 600, 695)
print("\n=== STOCK 2 (600..695): resumen por mes de A (live) ===")
bym = defaultdict(lambda: [0,0.0,0.0])
for r in range(600, 696):
    a, b = L2[r], R2[r]
    bym[a["mes"]][0]+=1; bym[a["mes"]][1]+=a["G"]; bym[a["mes"]][2]+=b["G"]
for k in sorted(bym):
    print("  %-10s n=%3d  G_live=%10.2f  G_jul=%10.2f" % (k, bym[k][0], round(bym[k][1],2), round(bym[k][2],2)))

print("\n=== STOCK 2: filas fechadas AGOSTO con G en la foto de julio (G_jul != 0) ===")
t = 0.0
for r in range(600, 696):
    a, b = L2[r], R2[r]
    if a["mes"] == "2026-08" and b["G"] != 0:
        t += b["G"]
        print("  fila %d %s %-9s G_live=%9.2f G_jul=%9.2f %s" % (
            r, a["fecha"].strftime("%Y-%m-%d"), a["cod"], a["G"], b["G"], str(a["desc"])[:30]))
print("  SUMA G_jul de filas agosto en STOCK 2 = %.2f" % round(t,2))

print("\n=== STOCK 2: TODAS las filas con G_jul != 0 (la foto de julio) ===")
t2 = 0.0
for r in range(600, 696):
    a, b = L2[r], R2[r]
    if b["G"] != 0:
        t2 += b["G"]
        print("  fila %d  mesA=%-8s %-9s G_live=%9.2f G_jul=%9.2f" % (r, a["mes"], a["cod"], a["G"], b["G"]))
print("  SUMA = %.2f" % round(t2,2))
