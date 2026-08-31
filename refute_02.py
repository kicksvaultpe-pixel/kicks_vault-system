import openpyxl, datetime

P = "C:/Users/usuario/Downloads/Registro KV Excel.xlsx"
wbv = openpyxl.load_workbook(P, data_only=True)

def s(ws, c1, c2, col=7):
    w = wbv[ws]; t=0.0; n=0
    for r in range(c1, c2+1):
        v = w.cell(r, col).value
        if isinstance(v,(int,float)): t+=v; n+=1
    return round(t,2), n

print("=== ACTUAL SUMS FROM DATA ===")
a,na = s("STOCK 1",197,454);            print(f"  STOCK 1            G197:G454 = {a:>12,.2f}  ({na} num cells)")
b,nb = s("Registro de STOCK 1",197,418);print(f"  Reg de STOCK 1     G197:G418 = {b:>12,.2f}  ({nb})")
c,nc = s("STOCK 2",600,695);            print(f"  STOCK 2            G600:G695 = {c:>12,.2f}  ({nc})")
d,nd = s("Registro de STOCK 2",600,695);print(f"  Reg de STOCK 2     G600:G695 = {d:>12,.2f}  ({nd})")

print()
print("=== WHAT THE FORMULAS ACTUALLY REFERENCE ===")
print("  STOCK 1!O456        = SUM('STOCK 2'!G600:G695) - 234       <- LIVE stock 2")
print("  Reg STOCK 1!O420    = SUM('STOCK 2'!G600:G695)             <- ALSO LIVE stock 2 (NOT the Registro copy!)")
print()
print(f"  live  STOCK 2 G600:G695            = {c:>12,.2f}")
print(f"  -> O456 = {c:.2f} - 234 = {c-234:>10,.2f}   (cached 4267.57)")
print(f"  -> O420 = {c:.2f}       = {c:>10,.2f}   (cached 4501.57)")
print(f"  frozen Reg STOCK 2 G600:G695       = {d:>12,.2f}")

print()
print("=== 'GROWTH OF THE TWO RANGES' (the analyst's Camino 1 claim = 17,771.86) ===")
g1 = round(a-b,2)
g2_live = 0.0                 # same range on both sides
g2_frozen = round(c-d,2)
print(f"  STOCK 1 range growth        = {a:,.2f} - {b:,.2f} = {g1:>10,.2f}")
print(f"  STOCK 2 growth (as written) = same live range on both sides = {g2_live:>10,.2f}")
print(f"  STOCK 2 growth (if it had pointed at the frozen copy) = {g2_frozen:>10,.2f}")
print(f"  TOTAL growth as written  = {g1+g2_live:>10,.2f}")
print(f"  TOTAL growth if frozen   = {round(g1+g2_frozen,2):>10,.2f}")
print(f"  analyst claims             17,771.86")

print()
print("=== CONSTANT REBATE (analyst's 3,814.80) ===")
prev_const = 72000+135.87
cur_const  = 84285.52
print(f"  STOCK 1: prev consts {prev_const:,.2f} -> cur {cur_const:,.2f} : delta = {round(cur_const-prev_const,2):,.2f}")
print(f"  STOCK 2: prev const 0.00 -> cur 234.00 : delta = 234.00")
print(f"  total extra subtracted this month = {round(cur_const-prev_const+234,2):,.2f}")
print(f"  i.e. constants REDUCE the figure by that much (analyst says they ADD 3,814.80)")

print()
print("=== IDENTITY CHECK ===")
cur_total  = round((a-cur_const) + (c-234), 2)
prev_total = round((b-prev_const) + c, 2)
print(f"  reproduced TOTAL COMPRAS MES (aug) = ({a:,.2f}-{cur_const:,.2f}) + ({c:,.2f}-234) = {cur_total:,.2f}   [excel cached 21,586.66]")
print(f"  reproduced TOTAL (jul snapshot)    = ({b:,.2f}-{prev_const:,.2f}) + ({c:,.2f})     = {prev_total:,.2f}   [excel cached 20,085.89]")
