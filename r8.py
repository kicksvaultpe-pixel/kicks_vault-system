# -*- coding: utf-8 -*-
import openpyxl, datetime, collections, json, urllib.request
P="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(P,data_only=True)
w=wb["STOCK 1"]
print("### STOCK 1 filas 419-454 (existen en vivo, ausentes en 'Registro de STOCK 1')")
n=0;sE=0.0;sG=0.0
for r in range(419,455):
    v=[w.cell(r,c).value for c in range(1,9)]
    if all(x is None for x in v): continue
    n+=1
    if isinstance(v[4],(int,float)): sE+=float(v[4])
    if isinstance(v[6],(int,float)): sG+=float(v[6])
    if n<=6: print("   r%-4d A=%s cod=%s E=%s F=%s G=%s est=%s"%(r,str(v[0])[:19],v[1],v[4],v[5],v[6],v[7]))
print("   n=%d sumaE=%.2f sumaG=%.2f  -> filas vacias de valor, no aportan al gap"%(n,sE,sG))

print("\n### Agosto dentro de 'Registro de STOCK 1' 197:418")
w2=wb["Registro de STOCK 1"]; na=0
for r in range(197,419):
    f=w2.cell(r,1).value
    if isinstance(f,datetime.datetime) and f.year==2026 and f.month==8: na+=1
print("   filas fechadas ago-2026 en la supuesta FOTO DE JULIO: %d"%na)
w3=wb["Registro de STOCK 2"]; nb=0
for r in range(600,696):
    f=w3.cell(r,1).value
    if isinstance(f,datetime.datetime) and f.year==2026 and f.month==8: nb+=1
print("   idem 'Registro de STOCK 2': %d"%nb)

def get(t):
    out=[];off=0
    while True:
        q=urllib.request.Request("https://erpkxogskfrtfttawapg.supabase.co/rest/v1/%s?select=*"%t)
        q.add_header("apikey","sb_publishable_qgRu9snBNMnDpQ3o9UOR4A_HAzXUhA1")
        q.add_header("Authorization","Bearer sb_publishable_qgRu9snBNMnDpQ3o9UOR4A_HAzXUhA1")
        q.add_header("Range","%d-%d"%(off,off+999))
        d=json.loads(urllib.request.urlopen(q).read().decode()); out+=d
        if len(d)<1000: break
        off+=1000
    return out
inv=get("inventario")
print("\n### inventario: distribucion tipo_pago / pago_estado (n=%d)"%len(inv))
print("   ",dict(collections.Counter((r.get('tipo_pago'),r.get('pago_estado')) for r in inv)))
pend=[r for r in inv if r.get('pago_estado')=='PENDIENTE']
print("   PENDIENTE n=%d deuda=%.2f"%(len(pend),sum(float(r.get('precio_compra_soles') or 0) for r in pend)))
mm=collections.Counter(str(r.get('fecha_compra'))[:7] for r in pend)
print("   PENDIENTE por mes de compra:",dict(sorted(mm.items())))
