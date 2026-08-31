import openpyxl, datetime
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(p,data_only=True)
def rows(sh,r1,r2):
    w=wb[sh]; out=[]
    for r in range(r1,r2+1):
        out.append(dict(row=r,A=w['A'+str(r)].value,B=w['B'+str(r)].value,C=w['C'+str(r)].value,
                        D=w['D'+str(r)].value,E=w['E'+str(r)].value,F=w['F'+str(r)].value,
                        G=w['G'+str(r)].value,H=w['H'+str(r)].value))
    return out
def s(v): return v if isinstance(v,(int,float)) else 0.0
def mk(a):
    if isinstance(a,(datetime.datetime,datetime.date)): return a.strftime("%Y-%m")
    return "SINFECHA"
S1=rows('STOCK 1',197,454); RS1=rows('Registro de STOCK 1',197,418)
# cumulative to find what 84285.52 / 72135.87 correspond to
cum=0
for x in S1:
    cum+=s(x['G'])
    if abs(cum-84285.52)<0.02: print("STOCK1: 84285.52 == cum G197:G%d  (codigo %s fecha %s)"%(x['row'],x['B'],x['A']))
cum=0
for x in RS1:
    cum+=s(x['G'])
    if abs(cum-72135.87)<0.02 or abs(cum-72000)<0.02: print("RegS1: %.2f == cum G197:G%d"%(cum,x['row']))
print()
# row-by-row compare by row number (same positional range 197-418)
diffs=[]
for a,b in zip(S1[:222],RS1):
    assert a['row']==b['row']
    if abs(s(a['G'])-s(b['G']))>0.005 or a['B']!=b['B']:
        diffs.append((a['row'],b['B'],s(b['G']),a['B'],s(a['G']),a['A']))
print("Filas 197-418 que CAMBIARON entre foto julio y agosto:",len(diffs))
for d in diffs[:60]: print("  r%d  jul[%s %.2f] -> ago[%s %.2f] fechaA=%s"%d)
print()
new=[x for x in S1 if x['row']>418]
print("Filas NUEVAS 419-454:",len([x for x in new if x['G'] is not None]),"suma",round(sum(s(x['G']) for x in new),2))
from collections import defaultdict
g=defaultdict(lambda:[0,0])
for x in new:
    if x['G'] is None: continue
    k=mk(x['A']); g[k][0]+=s(x['G']); g[k][1]+=1
for k in sorted(g): print("   %s : %.2f (%d filas)"%(k,g[k][0],g[k][1]))
