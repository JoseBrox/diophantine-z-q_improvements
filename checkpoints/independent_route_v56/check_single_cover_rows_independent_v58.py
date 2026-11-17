"""Independent integer-inequality audit of the signed-height application."""
from fractions import Fraction
from pathlib import Path
import json

rows=[(101,100,0,4,6,48),(25,24,0,4,6,48),(16,15,0,4,6,48),(121,100,0,6,8,96),
      (101,100,2,5,6,60),(25,24,2,6,6,72),(16,15,2,4,10,80),(121,100,2,6,14,168),
      (16,15,2,5,8,80),(121,100,2,7,12,168)]
checks=[]
for p,q,k,e,d,degree in rows:
    # Clear all denominators before testing contraction. This formula is
    # independently obtained from kappa=p/q, rather than calling the source checker.
    def parts(E,D):
        f1=D*(2*q-p)-4*p
        f2=E*q-3*p
        f3=8*q-6*p
        num=(2*k+1)*p*p*(2*p-q)
        return min(f1,f2,f3)>0,num,f1*f2*f3
    positive,num,den=parts(e,d)
    assert positive and 0<num<den and degree==2*e*d
    eliminated=[]
    for E in range(4,degree):
        for D in range(6,degree,2):
            if 2*E*D>=degree:continue
            pos,nn,dd=parts(E,D)
            assert not pos or nn>=dd
            eliminated.append([E,D])
    contraction=Fraction(num,den)
    total=contraction/Fraction(2*k+1,2)
    checks.append({"kappa":str(Fraction(p,q)),"support_budget":k,"e":e,"d":d,
                   "degree":degree,"q":str(total),"contraction":str(contraction),
                   "excluded_smaller_pairs":eliminated})
result={"status":"PASS","rows":checks,
        "ordinary_abc_minima":{"fixed_class":48,"support_budget_two":60},
        "scope":"All integer e>=4 and even d>=6; actual source realization remains unproved."}
Path(__file__).with_name("single_cover_rows_independent_v58_certificate.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
