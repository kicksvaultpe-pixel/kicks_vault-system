import openpyxl, datetime
from collections import defaultdict
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(p,data_only=True)
def s(v): return v if isinstance(v,(int,float)) else 0.0
def mk(a):
    if isinstance(a,(datetime.datetime,datetime.date)): return a.strftime("%Y-%m")
    return "SINFECHA"
for sh,lo,hi in [('STOCK 1',2,454),('STOCK 2',2,695)]:
    w=wb[sh]; g=defaultdict(lambda:[0.0,0])
    for r in range(lo,hi+1):
        a=w['A'+str(r)].value; gg=w['G'+str(r)].value; b=w['B'+str(r)].value
        if b is None and gg in (None,0): continue
        k=mk(a); g[k][0]+=s(gg); g[k][1]+=1
    print("==",sh,"(filas %d-%d) por mes de col A:"%(lo,hi))
    for k in sorted(g): print("   %-9s %10.2f  (%d filas)"%(k,g[k][0],g[k][1]))
    print("   AGOSTO 2026 -> %.2f"%g['2026-08'][0])
print()
w=wb['STOCK 1']
print("STOCK 1 filas 403-420 (fecha, codigo, G):")
for r in range(403,421):
    a=w['A'+str(r)].value
    print("   r%d %-22s %-9s G=%s H=%s"%(r,(a.strftime('%Y-%m-%d') if isinstance(a,datetime.datetime) else str(a)),str(w['B'+str(r)].value),w['G'+str(r)].value,w['H'+str(r)].value))
w=wb['STOCK 2']
print("STOCK 2 ultimas filas 686-700:")
for r in range(686,701):
    a=w['A'+str(r)].value
    print("   r%d %-22s %-9s G=%s"%(r,(a.strftime('%Y-%m-%d') if isinstance(a,datetime.datetime) else str(a)),str(w['B'+str(r)].value),w['G'+str(r)].value))
