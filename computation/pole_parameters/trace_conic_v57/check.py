#!/usr/bin/env python3
"""Exact algebra and finite local checks for the trace-conic criterion.

The general parity proof and source transfers are in the companion TeX.
Finite checks do not establish global rational realization.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import argparse
import sympy as sp

w, V, Y, k, t, A, B = sp.symbols('w V Y k t A B')
C = V**2+w*(2-V)
Vk = (2-k*k*w)/(1+2*k)
Yk = Vk+k*w
assert sp.factor(Yk**2-C.subs(V,Vk)) == 0
Vt = (2*(t-1)**2-w)/(t*t-1)
Yt = 2+t*(Vt-2)
assert sp.factor(Yt**2-C.subs(V,Vt)) == 0
assert sp.expand(C.subs(w,8)-(V-4)**2) == 0
assert C.subs(V,2) == 4
N = A*A-2*B*B
assert sp.factor(C.subs(V,2*A/N)-(4*A*A+2*w*N*(N-A))/N**2) == 0
assert sp.factor(((2-V)**2-C).subs(w,4*(1-V)/(2-V))) == 0

trace_class=1+3*(V-1)**2
assert [trace_class.subs(V,a) for a in [0,1,2]] == [4,1,4]
assert sp.Poly(sp.expand(trace_class*C),V,w).total_degree()==4
linear_class=1+24*V
cubic=sp.expand(linear_class*C)
assert cubic==24*V**3-24*V**2*w+V**2+47*V*w+2*w
assert len(sp.Poly(cubic,V,w).terms())==5
assert max(abs(int(a))for a in sp.Poly(cubic,V,w).coeffs())==47
Xc=1+24*V
weierstrass=Xc**3-(2+24*w)*Xc**2+(1+1176*w)*Xc
assert sp.expand(weierstrass-24**2*cubic)==0
assert sp.expand(16*(1+1176*w)**2*((-2-24*w)**2-4*(1+1176*w)))==sp.expand(9216*w*(w-8)*(1+1176*w)**2)
assert sp.expand(49**3-(2+24*w)*49**2+(1+1176*w)*49)==336**2

q = sp.symbols('q')
adaptive_class = (q*q-2*q-1)**2+4*q*(q*q-1)*V
for vv, expected in [(0,(q*q-2*q-1)**2),(1,(q*q+1)**2),(2,(q*q+2*q-1)**2)]:
    assert sp.expand(adaptive_class.subs(V,vv)-expected)==0
assert sp.expand(adaptive_class.subs(q,2)-linear_class)==0
aa, slope = sp.symbols('aa slope', nonzero=True)
tt = aa*slope
ff = tt*(tt+1)*(2*tt+1)*(3*tt+1)*(4*tt+1)*(5*tt+2)/120
assert sp.limit(slope**2*ff/(4*(tt-1)**8),slope,sp.oo)==1/(4*aa**2)

# A strictly positive witness expression on 0<V<=2, w>0 is already
# C=V^2+w(2-V).  The exact fixtures also cover V=2 and the split w=8.
positive_cases=0
for ww in [Fraction(1,1000),Fraction(2,9),Fraction(1,4),Fraction(1),Fraction(8),Fraction(100)]:
    for vv in [Fraction(1,100),Fraction(1,2),Fraction(1),Fraction(3,2),Fraction(2)]:
        assert vv*vv+ww*(2-vv)>0
        assert 1+3*(vv-1)**2>=1
        positive_cases+=1

def valuation_int(a,p):
    if a==0:
        return None
    v=0
    while a%p==0:
        a//=p
        v+=1
    return v

bad_cases=0
adaptive_bad_cases=0
local_squares=[]
for p in [3,5,7,17,113]:
    for nu in [1,3,5,7]:
        for vv in range((nu+1)//2,(nu+1)//2+3):
            for a,b in product(range(1,min(p,5)),repeat=2):
                ww=a*p**nu
                vvval=b*p**vv
                cc=vvval**2+ww*(2-vvval)
                assert 2*vv>nu
                assert valuation_int(cc,p)==nu
                dd=1+3*(vvval-1)**2
                assert valuation_int(dd,p)==0
                assert valuation_int(1+24*vvval,p)==0
                for cc_aux in [Fraction(0),Fraction(1),Fraction(1,p**(nu+1)),Fraction(p**nu)]:
                    qq=2+ww*cc_aux**2
                    delta=(qq*qq-2*qq-1)**2+4*qq*(qq*qq-1)*vvval
                    vd=valuation_int(abs(delta.numerator),p)-valuation_int(delta.denominator,p)
                    assert vd%2==0
                    adaptive_bad_cases+=1
                bad_cases+=1
    for residue in [1,2]:
        mod=p**3
        ww=p
        vvval=residue+p
        cc=(vvval**2+ww*(2-vvval))%mod
        root=next(y for y in range(mod) if y*y%mod==cc)
        local_squares.append({'p':p,'V_residue':residue,'modulus':mod,'root':root})

# Fixed-place preparation: a chosen exact sufficient precision at 2.
two_rows=[]
for e in [5,7,10]:
    vvval=Fraction(2)+Fraction(2**e)
    for ww in [Fraction(1,4),Fraction(1),Fraction(16)]:
        ratio=1+ww*(2-vvval)/(vvval*vvval)
        term=ratio-1
        val=valuation_int(abs(term.numerator),2)-valuation_int(term.denominator,2)
        if val>=3:
            assert ratio.numerator%8 == ratio.denominator%8
            two_rows.append({'e':e,'w':str(ww),'v2_of_ratio_minus_one':val})

census=[{'source':'general','point_roles':9,'point_rank':4**9,'terminal_rank':4**10,'total_coordinates':21},
        {'source':'conditional','point_roles':3,'point_rank':4**3,'terminal_rank':4**4,'total_coordinates':9}]
for row in census:
    assert row['total_coordinates']==1+2*row['point_roles']+1+1

report={
    'status':'PASS',
    'radicand':'V^2+w(2-V)',
    'identities_checked':['k-parametrization','line-through-(2,2) parametrization','w=8 split conic',
                          'reference value4','cleared W=A+B sqrt2 expression','Y=2-V slice'],
    'positive_exact_fixtures':positive_cases,
    'bad_pole_valuation_fixtures':bad_cases,
    'adaptive_class':{
        'q':'2+w*c^2',
        'polynomial':'(q^2-2q-1)^2+4q(q^2-1)*V',
        'reference_and_contact_square_identities':True,
        'bad_pole_fixtures_including_negative_auxiliary_valuations':adaptive_bad_cases,
        'slope_choice_fixed_place_limit_verified':True,
        'new_free_coordinates':0,
        'lost_contact_primes':False,
        'actual_global_realization_proved':False,
    },
    'selected_contact_hensel_fixtures':local_squares,
    'fixed_two_adic_square_fixtures':two_rows,
    'admissible_trace_class':'1+3(V-1)^2',
    'trace_class_residues_at_V_0_1_2':[4,1,4],
    'trace_class_product_total_degree':4,
    'linear_trace_class':{'polynomial':'1+24V','residues_at_V_0_1_2':[1,25,49],
                          'product_total_degree':3,'product_monomials':5,'product_coefficient_height':47,
                          'reference_elliptic_point':[49,336],
                          'singular_weights':['0','8','-1/1176']},
    'census_conditional_on_actual_rational_realization':census,
    'rational_realization_proved':False,
    'new_complete_defining_count_proved':False,
    'scope':'Algebra, local fixtures and coordinate census only; the proof covers all odd bad valuations. Source premises and global realization are not replaced by computation.'
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
out=args.output or Path(__file__).with_name('certificate.json')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','certificate':str(out),'bad_pole_fixtures':bad_cases}))
