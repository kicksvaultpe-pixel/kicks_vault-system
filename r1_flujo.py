# -*- coding: utf-8 -*-
import openpyxl, datetime, collections
from decimal import Decimal

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb = openpyxl.load_workbook(P, data_only=True)

def dump(sheetname):
    ws = wb[sheetname]
    print("=== %s  dims=%s max_row=%d" % (sheetname, ws.dimensions, ws.max_row))
    rows = []
    for r in range(2, ws.max_row+1):
        f = ws.cell(r,1).value
        acc = ws.cell(r,2).value
        cod = ws.cell(r,3).value
        desc= ws.cell(r,4).value
        talla=ws.cell(r,5).value
        ing = ws.cell(r,6).value
        egr = ws.cell(r,7).value
        egrusd=ws.cell(r,8).value
        info= ws.cell(r,9).value
        if f is None and acc is None and cod is None and ing is None and egr is None and egrusd is None:
            continue
        rows.append(dict(row=r,fecha=f,accion=acc,cod=cod,desc=desc,talla=talla,
                         ing=ing,egr=egr,egrusd=egrusd,info=info))
    return rows

flujo = dump("FLUJO")
reg   = dump("Registro de FLUJO")
print("FLUJO filas no vacias:", len(flujo))
print("Registro de FLUJO filas no vacias:", len(reg))

def fmax(rows):
    fs=[r['fecha'] for r in rows if isinstance(r['fecha'], datetime.datetime)]
    return min(fs), max(fs)
print("FLUJO rango fechas:", fmax(flujo))
print("REG   rango fechas:", fmax(reg))

def mes(v):
    if isinstance(v, datetime.datetime): return "%04d-%02d"%(v.year,v.month)
    return "SIN/%r"%(v,)

# COMPRA por mes en FLUJO vivo
for name, rows in (("FLUJO",flujo),("REG",reg)):
    agg = collections.defaultdict(lambda: [0,0.0,0.0,0])  # n, soles, usd, n_soles_no_nulo
    for r in rows:
        a = (str(r['accion']) or "").strip().upper() if r['accion'] else ""
        if a != "COMPRA": continue
        k = mes(r['fecha'])
        agg[k][0]+=1
        if r['egr'] is not None:
            try: agg[k][1]+=float(r['egr']); agg[k][3]+=1
            except: print("  no num egr", name, r['row'], repr(r['egr']))
        if r['egrusd'] is not None:
            try: agg[k][2]+=float(r['egrusd'])
            except: pass
    print("--- %s COMPRA por mes (n, soles, usd, n_con_soles)" % name)
    for k in sorted(agg): print("   %s  n=%3d  S/=%12.2f  US$=%10.2f  nS=%3d" % (k,agg[k][0],agg[k][1],agg[k][2],agg[k][3]))
