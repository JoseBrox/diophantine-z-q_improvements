"""Exact block statistics and identities for three safe trace classes."""
from pathlib import Path
import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output', type=Path, default=Path(__file__).with_name('certificate.json'))
output_path = _parser.parse_args().output
output_path.parent.mkdir(parents=True, exist_ok=True)
from fractions import Fraction as Q
import json
import sympy as S

V,w,x,Y=S.symbols("V w x Y")
C=V*V+w*(2-V)
deltas=[V+2,V*V-V+2,1+w*(2-V)]
Rs=[S.expand(d*C) for d in deltas]
expected=[(3,3,4,4),(4,4,7,4),(4,3,8,4)]
stats=[]
for i,(r,ex) in enumerate(zip(Rs,expected),1):
    P=S.Poly(r,V,w)
    val=(P.total_degree(),P.degree(V),len(P.monoms()),max(abs(c) for c in P.coeffs()))
    assert val==ex
    full=S.Poly(Y**2-r,Y,V,w)
    assert len(full.monoms())==ex[2]+1
    assert full.total_degree()==ex[0]
    assert max(abs(c) for c in full.coeffs())==4
    stats.append({"class":i,"expanded":str(r),"degree":ex[0],"degree_in_trace":ex[1],
                  "radicand_monomials":ex[2],"equation_monomials":ex[2]+1,"height":4})

model1=x*(x*x-(w+4)*x+4*(w+1))
assert S.expand(Rs[0].subs(V,x-2)-model1)==0
assert S.factor(16*S.discriminant(model1,x))==256*w*(w-8)*(w+1)**2
assert S.factor(S.discriminant(Rs[1],V))==-112*w*(w-8)*(w-1)**4
model3=x*(x*x+(w*w-4*w-2)*x+(w+1)*(3*w+1))
assert S.cancel(w*w*Rs[2].subs(V,(1+2*w-x)/w)-model3)==0
assert S.factor(16*S.discriminant(model3,x))==16*w**3*(w-8)*(w+1)**2*(3*w+1)**2
assert S.expand(Rs[2]-((1-w)*V+2*w)**2+w*(V-2)*(V-1)**2)==0
xx=1+w*(2-V)
translate=(1+2*w-(w+1)*(3*w+1)/xx)/w
assert S.cancel(translate-(w-(1+2*w)*V)/xx)==0
for i in range(3):
    assert Rs[i].subs(V,2)==[16,16,4][i]
assert S.expand(Rs[2].subs(V,1)-(1+w)**2)==0

# Exact residues at selected contacts; neither local hypothesis nor a
# global rational witness is inferred from a finite-field search.
contact_checks=0
for p in list(S.primerange(5,2000)):
    if p%24!=1:continue
    for v in [1,2]:
        for delta in deltas:
            res=int(delta.subs({V:v,w:0}))%p
            assert res and pow(res,(p-1)//2,p)==1
            contact_checks+=1

# All bad-pole multipliers are units, via reduction w=V=0.
assert [d.subs({V:0,w:0}) for d in deltas]==[2,2,1]

# Explicit sufficient 2-adic preparation, with bounded possible w poles.
def v2(q):
    q=Q(q)
    if not q:return 10**9
    n,d=abs(q.numerator),q.denominator;a=0
    while n%2==0:n//=2;a+=1
    while d%2==0:d//=2;a-=1
    return a
two_checks=0
for b in range(-6,7):
    ww=Q(2**b) if b>=0 else Q(1,2**(-b))
    for eexp in range(max(5,5-b),max(5,5-b)+3):
        ee=Q(2**eexp);vv=2+ee
        ds=[vv+2,vv*vv-vv+2,1+ww*(2-vv)]
        cc=vv*vv+ww*(2-vv)
        assert v2(ds[0]/4-1)>=3
        assert v2(ds[1]/4-1)>=3
        assert v2(ds[2]-1)>=3
        assert v2(cc/(vv*vv)-1)>=3
        two_checks+=1

cert={"status":"PASS","block_statistics":stats,
      "curve_models_and_discriminants":"verified symbolically",
      "selected_contact_residue_checks":contact_checks,
      "fixed_two_adic_neighborhood_checks":two_checks,
      "scope":"Sound square tests and local preparation; actual simultaneous rational realization remains unproved."}
output_path.write_text(json.dumps(cert,indent=2)+"\n")
print(json.dumps(cert,indent=2))
