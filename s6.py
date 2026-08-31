import openpyxl, datetime
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(p,data_only=True)
def rows(sh,r1,r2):
    w=wb[sh]; return {r:dict(row=r,A=w['A'+str(r)].value,B=w['B'+str(r)].value,C=w['C'+str(r)].value,
        E=w['E'+str(r)].value,F=w['F'+str(r)].value,G=w['G'+str(r)].value,H=w['H'+str(r)].value)
        for r in range(r1,r2+1)}
def s(v): return v if isinstance(v,(int,float)) else 0.0
def isaug(a): return isinstance(a,datetime.datetime) and a.year==2026 and a.month==8
S1=rows('STOCK 1',197,454); RS1=rows('Registro de STOCK 1',197,418)
S2=rows('STOCK 2',600,695); RS2=rows('Registro de STOCK 2',600,695)

print("--- STOCK 1: descomposicion del delta en E (precio compra) vs F (costos) ---")
dE=dF=0
for r in range(197,419):
    a,b=S1[r],RS1[r]
    de,df=s(a['E'])-s(b['E']), s(a['F'])-s(b['F'])
    if abs(de)>0.005 or abs(df)>0.005:
        dE+=de; dF+=df
        print("  r%-4d %-9s %s dE=%9.2f dF=%8.2f  H=%s"%(r,a['B'],(a['A'].strftime('%Y-%m-%d') if isinstance(a['A'],datetime.datetime) else '?'),de,df,a['H']))
print("  TOTAL dE=%.2f  dF=%.2f  suma=%.2f"%(dE,dF,dE+dF))
print()
print("--- STOCK 2 ---")
dE2=dF2=0
for r in range(600,696):
    a,b=S2[r],RS2[r]
    de,df=s(a['E'])-s(b['E']), s(a['F'])-s(b['F'])
    if abs(de)>0.005 or abs(df)>0.005 or a['B']!=b['B']:
        dE2+=de; dF2+=df
        print("  r%-4d jul=%-9s ago=%-9s %s dE=%9.2f dF=%8.2f"%(r,b['B'],a['B'],(a['A'].strftime('%Y-%m-%d') if isinstance(a['A'],datetime.datetime) else '?'),de,df))
print("  TOTAL dE=%.2f dF=%.2f suma=%.2f"%(dE2,dF2,dE2+dF2))
