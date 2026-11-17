#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s

q,V=s.symbols('q V')
d=(q*q-2*q-1)**2+4*q*(q*q-1)*V
assert s.expand(d.subs(V,0)-(q*q-2*q-1)**2)==0
assert s.expand(d.subs(V,1)-(q*q+1)**2)==0
assert s.expand(d.subs(V,2)-(q*q+2*q-1)**2)==0
assert s.expand(d.subs(q,2)-(1+24*V))==0

def val(z,p):
    z=F(z)
    if not z:return None
    a,b=abs(z.numerator),z.denominator
    r=0
    while a%p==0:a//=p;r+=1
    while b%p==0:b//=p;r-=1
    return r

cases=0
for p in [3,5,7,11,17,113]:
    for nu in [1,3,5]:
        ww=F(p)**nu
        for cv in range(-5,4):
            cc=F(p)**cv
            qq=2+ww*cc*cc
            uu=nu+2*cv
            assert uu%2 and uu!=0
            for m in [1,3,7]:
                vv=F(p)**m
                dd=(qq*qq-2*qq-1)**2+4*qq*(qq*qq-1)*vv
                if uu>0:
                    assert val(dd,p)==0 and val(dd-1,p)>=1
                else:
                    aa=(qq*qq-2*qq-1)**2
                    assert val(dd,p)==4*uu
                    assert val(dd/aa-1,p)==m-uu
                cases+=1

general_slope=[]
for p in [2,3,7,17]:
    for vv in [F(2),F(2)+F(p)**8]:
        ww=F(7,16)
        lam=F(p)**(-12)
        qq=2+ww*lam*lam
        aa=(qq*qq-2*qq-1)**2
        dd=aa+4*qq*(qq*qq-1)*vv
        depth=val(dd/aa-1,p)
        assert depth>=3
        general_slope.append({'p':p,'v_p_relative_correction':depth})

out={'status':'PASS','square_identities_at_V':[0,1,2],
     'c_zero_recovers_linear_class':True,
     'exact_bad_pole_cases':cases,
     'general_slope_fixed_place_fixtures':general_slope,
     'new_free_coordinate':False,'lost_soundness_contacts':False,
     'global_rational_realization_proved':False}
path=Path(__file__).with_name('adaptive_trace_class_independent_certificate.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','certificate':str(path),'bad_pole_cases':cases}))
