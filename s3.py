import openpyxl, datetime
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wb=openpyxl.load_workbook(p,data_only=True)
def rows(sh,r1,r2):
    w=wb[sh]; out=[]
    for r in range(r1,r2+1):
        a=w['A'+str(r)].value; b=w['B'+str(r)].value; c=w['C'+str(r)].value
        d=w['D'+str(r)].value; e=w['E'+str(r)].value; f=w['F'+str(r)].value
        g=w['G'+str(r)].value; h=w['H'+str(r)].value
        out.append((r,a,b,c,d,e,f,g,h))
    return out
def s(v): return v if isinstance(v,(int,float)) else 0.0
def mk(a):
    if isinstance(a,datetime.datetime): return a.strftime("%Y-%m")
    if isinstance(a,datetime.date): return a.strftime("%Y-%m")
    return "NOFECHA:"+repr(a)

S1=rows('STOCK 1',197,454); RS1=rows('Registro de STOCK 1',197,418)
S2=rows('STOCK 2',600,695); RS2=rows('Registro de STOCK 2',600,695)
print("SUM STOCK1 G197:G454      =", round(sum(s(x[7]) for x in S1),2), " nonblank rows:",sum(1 for x in S1 if x[7] is not None))
print("SUM RegS1 G197:G418       =", round(sum(s(x[7]) for x in RS1),2)," nonblank rows:",sum(1 for x in RS1 if x[7] is not None))
print("SUM STOCK2 G600:G695      =", round(sum(s(x[7]) for x in S2),2), " nonblank:",sum(1 for x in S2 if x[7] is not None))
print("SUM RegS2 G600:G695       =", round(sum(s(x[7]) for x in RS2),2), " nonblank:",sum(1 for x in RS2 if x[7] is not None))
print()
print("Check O455:", round(sum(s(x[7]) for x in S1)-84285.52,2))
print("Check O456:", round(sum(s(x[7]) for x in S2)-234,2))
print("Check O419:", round(sum(s(x[7]) for x in RS1)-72000-135.87,2))
print("Check O420:", round(sum(s(x[7]) for x in RS2),2))
