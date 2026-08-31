import openpyxl
p="C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wbv=openpyxl.load_workbook(p,data_only=True)
wbf=openpyxl.load_workbook(p,data_only=False)
def show(sh,r1,r2,cols="LMNOP"):
    wv,wf=wbv[sh],wbf[sh]
    print("=== ",sh,r1,r2)
    for r in range(r1,r2+1):
        for c in cols:
            v=wv[c+str(r)].value; f=wf[c+str(r)].value
            if v is not None or f is not None:
                print(f"  {c}{r}: val={v!r} formula={f!r}")
show('STOCK 1',450,460)
show('Registro de STOCK 1',414,424)
show('STOCK 2',690,700)
show('Registro de STOCK 2',690,700)
