"""Exact local identities and scoped valuation audit for the moving detector."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as S

def vp(x,p):
    x=Q(x)
    if not x:
        return None
    n,d=abs(x.numerator),x.denominator
    ans=0
    while n%p==0:
        n//=p;ans+=1
    while d%p==0:
        d//=p;ans-=1
    return ans

def pp(p,k):
    return Q(p**k) if k>=0 else Q(1,p**(-k))

def inspect(a,z,p):
    t=a*a-z*z
    if not t:
        return False
    F=Q(1)
    for c in range(1,7):
        F*=t+2*c*a+c*c
    if not F:
        return False
    nu=vp(F,p)
    if nu%2==0:
        return False
    qa,qz,qt,qd=vp(a,p),vp(z,p),vp(t,p),vp(t/a,p)
    if qa<0:
        assert qt==qa and qd==0
    elif qa==0:
        assert nu>0 and qd>=0
    else:
        assert qz==0 and qt==0 and nu>0 and qd==-qa
    return True

fixtures=odd=0
for p in [7,11,13,17,19]:
    units=sorted({1,2,p-2,p-1})
    for ka in range(-3,4):
        for kz in range(-3,4):
            for ua in units:
                for uz in units:
                    fixtures+=1
                    odd+=inspect(pp(p,ka)*ua,pp(p,kz)*uz,p)
    for ka in [-1,-2,-3]:
        for c in range(1,7):
            for prec in range(-3,16):
                a=pp(p,ka)
                z=a+c+pp(p,prec)
                fixtures+=1
                odd+=inspect(a,z,p)

# Symbolic prime factorization, with six sign reversals.
a,z,u,D,h=S.symbols("a z u D h", nonzero=True)
for c in range(1,7):
    assert S.expand((a+c)**2-z**2-(a+c-z)*(a+c+z))==0
    assert S.cancel(((a+c)**2-z**2).subs(z,u/(D**2*h**2))
                    +(u-D**2*(a+c)*h**2)*(u+D**2*(a+c)*h**2)/(D**4*h**4))==0

# The omitted numerator support is a real limitation of this mechanism.
p=17;aa=Q(17**2);zz=Q(18);tt=aa*aa-zz*zz
FF=Q(1)
for c in range(1,7):FF*=tt+2*c*aa+c*c
dd=tt/aa;ww=FF/(4*dd**8);WW=1+1/FF;VV=2/WW;bb=4*ww/(VV*VV)
assert [vp(FF,p),vp(dd,p),vp(bb,p)]==[1,-2,15]

out={"status":"PASS","exact_valuation_fixtures":fixtures,
     "odd_valuation_fixtures":odd,"symbolic_factorizations":12,
     "numerator_support_counterexample":{"p":17,"a":289,"z":18,
         "vF":1,"vdelta":-2,"vb":15,"vC1":0},
     "scope":"Detector normalization and ordered completeness only; moving-contact height inequality remains unproved."}
Path(__file__).with_name("moving_contact_detector_v58_certificate.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
