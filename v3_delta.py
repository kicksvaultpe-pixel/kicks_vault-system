# -*- coding: utf-8 -*-
import openpyxl
from datetime import datetime
P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wbF = openpyxl.load_workbook(P, data_only=False)
wbV = openpyxl.load_workbook(P, data_only=True)

def num(x):
    return float(x) if isinstance(x,(int,float)) else 0.0

def grab(sheet, r0, r1):
    """dict codigo -> (row, fecha, E, F, G, H, Eesformula)"""
    v=wbV[sheet]; f=wbF[sheet]; d={}
    for r in range(r0,r1+1):
        cod=v.cell(r,2).value
        if not cod: continue
        ef=f.cell(r,5).value
        d[cod]=dict(row=r, fecha=v.cell(r,1).value, E=num(v.cell(r,5).value),
                    F=num(v.cell(r,6).value), G=num(v.cell(r,7).value),
                    H=v.cell(r,8).value, Eform=isinstance(ef,str) and ef.startswith("="),
                    Fform=isinstance(f.cell(r,6).value,str) and str(f.cell(r,6).value).startswith("="),
                    desc=v.cell(r,3).value)
    return d

for live, snap, r0, rL, rS in [("STOCK 1","Registro de STOCK 1",197,454,418),
                               ("STOCK 2","Registro de STOCK 2",600,695,695)]:
    L=grab(live,r0,rL); S=grab(snap,r0,rS)
    sumL=sum(x["G"] for x in L.values()); sumS=sum(x["G"] for x in S.values())
    print("="*70)
    print(f"{live}: SUM(G{r0}:G{rL}) live = {sumL:,.2f}   |  {snap} SUM(G{r0}:G{rS}) = {sumS:,.2f}")
    print(f"  DELTA total = {sumL-sumS:,.2f}")
    nuevos = [c for c in L if c not in S]
    dn = sum(L[c]["G"] for c in nuevos)
    print(f"  (a) FILAS NUEVAS: {len(nuevos)} filas, G = {dn:,.2f}")
    cambios=[]
    for c in L:
        if c in S and abs(L[c]["G"]-S[c]["G"])>0.005:
            cambios.append(c)
    dc = sum(L[c]["G"]-S[c]["G"] for c in cambios)
    print(f"  (b) FILAS PREEXISTENTES CON G CAMBIADO: {len(cambios)} filas, delta = {dc:,.2f}")
    # subdividir (b): E pasó de formula(0) a literal  vs otros
    e_override=[c for c in cambios if S[c]["Eform"] and S[c]["E"]==0 and not L[c]["Eform"] and L[c]["E"]>0]
    de=sum(L[c]["G"]-S[c]["G"] for c in e_override)
    print(f"      b1) E era formula VLOOKUP=0 y ahora es literal>0: {len(e_override)} filas, delta {de:,.2f}")
    otros=[c for c in cambios if c not in e_override]
    print(f"      b2) resto: {len(otros)} filas, delta {sum(L[c]['G']-S[c]['G'] for c in otros):,.2f}")
    for c in otros:
        print(f"          {c} r{L[c]['row']} {str(L[c]['fecha'])[:10]} Gsnap={S[c]['G']:.2f} Glive={L[c]['G']:.2f} "
              f"Esnap={S[c]['E']:.2f}(f={S[c]['Eform']}) Elive={L[c]['E']:.2f}(f={L[c]['Eform']}) "
              f"Fsnap={S[c]['F']:.2f} Flive={L[c]['F']:.2f}")
    desap=[c for c in S if c not in L]
    print(f"  (c) codigos en snapshot que ya NO estan: {len(desap)} {desap[:10]}")
    # detalle e_override
    print(f"  --- detalle b1 (overrides de E) ---")
    tot=0
    for c in sorted(e_override, key=lambda k:L[k]['row']):
        x=L[c]; y=S[c]
        print(f"    {c} r{x['row']} fecha={str(x['fecha'])[:10]} E {y['E']:.2f}->{x['E']:.2f} F {y['F']:.2f}->{x['F']:.2f} G {y['G']:.2f}->{x['G']:.2f} {x['H']}")
        tot+=x['G']-y['G']
    print(f"    SUBTOTAL b1 = {tot:,.2f}")
