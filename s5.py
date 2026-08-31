import openpyxl, datetime
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(p,data_only=True)
def rows(sh,r1,r2):
    w=wb[sh]; return [dict(row=r,A=w['A'+str(r)].value,B=w['B'+str(r)].value,
        E=w['E'+str(r)].value,F=w['F'+str(r)].value,G=w['G'+str(r)].value,H=w['H'+str(r)].value)
        for r in range(r1,r2+1)]
def s(v): return v if isinstance(v,(int,float)) else 0.0
S1=rows('STOCK 1',197,454); RS1=rows('Registro de STOCK 1',197,418)
# 1) is 84285.52 a prefix of the AUGUST column?
cum=0; hits=[]
for x in S1:
    cum+=s(x['G'])
    hits.append((x['row'],round(cum,2)))
for r,c in hits:
    if abs(c-84285.52)<5: print("AUG prefix near 84285.52 -> G197:G%d = %.2f"%(r,c))
print("AUG cum at r390 = %.2f ; at r391 = %.2f"%(dict(hits)[390],dict(hits)[391]))
# same prefix but using JULY values for rows 197-390
juljul={x['row']:s(x['G']) for x in RS1}
print("JUL-values cum G197:G390 = %.2f"%sum(juljul.get(r,0) for r in range(197,391)))
print("AUG-values cum G197:G390 = %.2f"%dict(hits)[390])
print("  -> delta sobre el prefijo congelado = %.2f"%(dict(hits)[390]-sum(juljul.get(r,0) for r in range(197,391))))
print("AUG SUM G391:G454 = %.2f"%(sum(s(x['G']) for x in S1 if x['row']>=391)))
print()
# 2) max date present in the "July snapshot"
ds=[x['A'] for x in RS1 if isinstance(x['A'],(datetime.datetime,datetime.date))]
print("Registro de STOCK 1: rango de fechas %s .. %s"%(min(ds),max(ds)))
ags=[x for x in RS1 if isinstance(x['A'],datetime.datetime) and x['A'].year==2026 and x['A'].month==8]
print("  filas fechadas AGOSTO ya presentes en la foto 'de julio':",len(ags))
for x in ags: print("    r%d %s %s G=%.2f"%(x['row'],x['B'],x['A'].strftime('%Y-%m-%d'),s(x['G'])))
