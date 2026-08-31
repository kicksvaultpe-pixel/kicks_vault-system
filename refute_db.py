import requests, collections, datetime
K="sb_publishable_qgRu9snBNMnDpQ3o9UOR4A_HAzXUhA1"
H={"apikey":K,"Authorization":"Bearer "+K}
B="https://erpkxogskfrtfttawapg.supabase.co/rest/v1/"
def get(t, sel="*"):
    out=[]; s=0
    while True:
        h=dict(H); h["Range"]=f"{s}-{s+999}"
        r=requests.get(B+t, headers=h, params={"select":sel}, timeout=60)
        r.raise_for_status(); d=r.json()
        out+=d
        if len(d)<1000: break
        s+=1000
    return out

inv=get("inventario"); cos=get("costos")
print("inventario rows:", len(inv), " costos rows:", len(cos))

def m(s):
    if not s: return None
    return s[:7]
agg=collections.defaultdict(lambda:[0.0,0])
for i in inv:
    k=m(i.get("fecha_compra"))
    pf=i.get("precio_final") or 0
    agg[k][0]+=float(pf); agg[k][1]+=1
print("\ninventario precio_final by fecha_compra month:")
for k in sorted(agg, key=lambda x:(x is None, x)):
    print(f"   {str(k):<10} {agg[k][0]:>12,.2f}  n={agg[k][1]}")

aug=[i for i in inv if m(i.get("fecha_compra"))=="2026-08"]
print(f"\nAUG inventario: n={len(aug)}  precio_final={sum(float(i.get('precio_final') or 0) for i in aug):,.2f}")
codes={i["codigo_producto"] for i in aug}
ca=[c for c in cos if c.get("codigo_producto") in codes]
print(f"  costos rows attached to those codes: n={len(ca)}  total={sum(float(c.get('costo_soles') or 0) for c in ca):,.2f}")
cam=[c for c in cos if (c.get("fecha") or "")[:7]=="2026-08"]
print(f"  costos DATED aug 2026: n={len(cam)} total={sum(float(c.get('costo_soles') or 0) for c in cam):,.2f}")

print(f"\n  AUG precio_compra_soles sum = {sum(float(i.get('precio_compra_soles') or 0) for i in aug):,.2f}")
pend=[i for i in inv if i.get("pago_estado")=="PENDIENTE"]
print(f"\n  PENDIENTE: n={len(pend)}  precio_final={sum(float(i.get('precio_final') or 0) for i in pend):,.2f}")
