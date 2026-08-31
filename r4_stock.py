# -*- coding: utf-8 -*-
import openpyxl, datetime, collections
P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb = openpyxl.load_workbook(P, data_only=True)

def load(s, r0, r1):
    ws=wb[s]; rows=[]
    for r in range(r0, r1+1):
        v=[ws.cell(r,c).value for c in range(1,9)]
        if all(x is None for x in v): continue
        rows.append(dict(sh=s,row=r,fecha=v[0],cod=str(v[1]).strip() if v[1] else None,
                         desc=v[2],talla=v[3],pc=v[4],costos=v[5],pf=v[6],estado=v[7]))
    return rows

s1  = load("STOCK 1",197,454)
s2  = load("STOCK 2",600,695)
r1  = load("Registro de STOCK 1",197,418)
r2  = load("Registro de STOCK 2",600,695)

def tot(rows,k='pf'):
    return sum(float(x[k]) for x in rows if isinstance(x[k],(int,float)))
print("STOCK1 197:454  n=%d  sumG=%.2f" % (len(s1),tot(s1)))
print("STOCK2 600:695  n=%d  sumG=%.2f" % (len(s2),tot(s2)))
print("RegS1  197:418  n=%d  sumG=%.2f" % (len(r1),tot(r1)))
print("RegS2  600:695  n=%d  sumG=%.2f" % (len(r2),tot(r2)))
print()
print("COMPRAS MES S1 = %.2f - 84285.52 = %.2f" % (tot(s1), tot(s1)-84285.52))
print("COMPRAS MES S2 = %.2f - 234      = %.2f" % (tot(s2), tot(s2)-234))
print("TOTAL          = %.2f" % (tot(s1)-84285.52 + tot(s2)-234))
print("Reg COMPRAS S1 = %.2f -72000-135.87 = %.2f" % (tot(r1), tot(r1)-72000-135.87))
print("Reg COMPRAS S2 = %.2f" % tot(r2))
print()

# comparacion por codigo
def idx(rows):
    d=collections.defaultdict(list)
    for r in rows: d[r['cod']].append(r)
    return d
live = idx(s1+s2); snap = idx(r1+r2)
print("codigos live=%d snap=%d" % (len(live),len(snap)))

lista=['P-00961','P-00962','P-00963','P-00964','P-00967','P-00969','P-00972','P-00975','P-00976','P-00978','P-00979','P-00980','P-00981','P-00982','P-00983','P-00984','P-00986','P-00987','P-00988','P-00996']
print("\n### Los 20 codigos del hallazgo, en las hojas STOCK")
print("%-9s | %-28s | %-28s" % ("COD","LIVE (STOCK1/2)","SNAP (Registro de STOCK)"))
sum_live=0.0; sum_snap=0.0; solo_live=[]
for k in lista:
    L=live.get(k); S=snap.get(k)
    ls = "  ".join("%s r%d E=%s G=%s %s"%(x['sh'][:7],x['row'],x['pc'],x['pf'],x['estado']) for x in L) if L else "AUSENTE"
    ss = "  ".join("%s r%d E=%s G=%s %s"%(x['sh'][:9],x['row'],x['pc'],x['pf'],x['estado']) for x in S) if S else "AUSENTE"
    print("%-9s | %s\n          | %s" % (k, ls, ss))
    if L: sum_live += sum(float(x['pf']) for x in L if isinstance(x['pf'],(int,float)))
    if S: sum_snap += sum(float(x['pf']) for x in S if isinstance(x['pf'],(int,float)))
    if L and not S: solo_live.append(k)
print("\nsuma G (precio final) de los 20 en LIVE = %.2f" % sum_live)
print("suma G (precio final) de los 20 en SNAP = %.2f" % sum_snap)
print("codigos que estan en LIVE y NO en SNAP:", solo_live)

# suma precio compra E de los 20 en live
sE=0.0
for k in lista:
    for x in live.get(k,[]):
        if isinstance(x['pc'],(int,float)): sE+=float(x['pc'])
print("suma E (precio compra) de los 20 en LIVE = %.2f" % sE)
