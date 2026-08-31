# -*- coding: utf-8 -*-
import openpyxl, datetime, requests, json

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb = openpyxl.load_workbook(P, data_only=True)
s1=wb["STOCK 1"]; s2=wb["STOCK 2"]; r1=wb["Registro de STOCK 1"]; r2=wb["Registro de STOCK 2"]
def f(v): return float(v) if isinstance(v,(int,float)) else 0.0
def mes(v):
    if isinstance(v,(datetime.datetime,datetime.date)): return f"{v.year}-{v.month:02d}"
    return "SIN-FECHA"

rows=[]
for sl,sp,lo,hi,tag in [(s1,r1,197,418,"S1"),(s2,r2,600,695,"S2")]:
    for r in range(lo,hi+1):
        dg=f(sl[f"G{r}"].value)-f(sp[f"G{r}"].value)
        if abs(dg)<0.001: continue
        de=f(sl[f"E{r}"].value)-f(sp[f"E{r}"].value)
        df=f(sl[f"F{r}"].value)-f(sp[f"F{r}"].value)
        rows.append((tag,r,sl[f"B{r}"].value,mes(sl[f"A{r}"].value),de,df,dg))

no_ago=[x for x in rows if x[3]!="2026-08"]
si_ago=[x for x in rows if x[3]=="2026-08"]
print("=== LAS 9 FILAS YA FECHADAS EN AGOSTO (doble conteo del analista) ===")
for x in si_ago:
    print(f"  {x[0]} fila {x[1]:<5} {str(x[2]):<11} dE={x[4]:>8,.2f} dF={x[5]:>8,.2f} dG={x[6]:>8,.2f}")
print(f"  subtotal = {sum(x[6] for x in si_ago):,.2f}  en {len(si_ago)} filas")
print()
print("=== EL NUMERO CORRECTO: crecimiento sobre filas NO fechadas en agosto ===")
print(f"  {sum(x[6] for x in no_ago):,.2f} en {len(no_ago)} filas")
print(f"    de los cuales PRECIO DE COMPRA (E) = {sum(x[4] for x in no_ago):,.2f}")
print(f"    de los cuales COSTOS          (F) = {sum(x[5] for x in no_ago):,.2f}")
print()

# cross-check base de datos
H={"apikey":"sb_publishable_qgRu9snBNMnDpQ3o9UOR4A_HAzXUhA1",
   "Authorization":"Bearer sb_publishable_qgRu9snBNMnDpQ3o9UOR4A_HAzXUhA1"}
codes=[x[2] for x in no_ago if x[2]]
inv={}
for i in range(0,len(codes),40):
    ch=codes[i:i+40]
    q="https://erpkxogskfrtfttawapg.supabase.co/rest/v1/inventario?select=codigo_producto,fecha_compra,estado,pago_estado,tipo_pago,precio_compra_soles,precio_final&codigo_producto=in.("+",".join(ch)+")"
    rr=requests.get(q,headers=H,timeout=60)
    for d in rr.json(): inv[d["codigo_producto"]]=d
print("=== CRUCE CON LA BASE: las 33 filas no-agosto ===")
print(f"  encontradas en inventario: {len(inv)}/{len(codes)}")
cnt={}
for x in no_ago:
    d=inv.get(x[2])
    if not d: continue
    k=(d.get("tipo_pago"),d.get("pago_estado"))
    cnt[k]=cnt.get(k,0)+1
for k,v in sorted(cnt.items(),key=lambda z:-z[1]):
    print(f"    tipo_pago={str(k[0]):<10} pago_estado={str(k[1]):<10} -> {v} productos")
print()
print("  detalle (fecha_compra en la base vs mes de la fila del Excel):")
for x in no_ago[:40]:
    d=inv.get(x[2])
    if d:
        print(f"    {str(x[2]):<11} excelmes={x[3]:<8} base_fecha={str(d.get('fecha_compra'))[:10]:<12} "
              f"{str(d.get('tipo_pago')):<9} {str(d.get('pago_estado')):<9} precio_final={d.get('precio_final')} dG={x[6]:,.2f}")
    else:
        print(f"    {str(x[2]):<11} excelmes={x[3]:<8} NO ESTA EN LA BASE  dG={x[6]:,.2f}")
