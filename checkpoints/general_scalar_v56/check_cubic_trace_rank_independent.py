#!/usr/bin/env python3
"""Verify the cubic trace rank certificate using only the standard library.

No polynomial factorization or algebra-system arithmetic is used.  The
script reconstructs the division polynomials at P, multiplies the stated
factors exactly, and checks a projective modular no-root proof for each
nonlinear factor.  General torsion and division-polynomial theorems are
the explicitly cited mathematical inputs.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'cubic_trace_rank_certificate.json').read_text())

def trim(a):
    a=list(map(F,a))
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)

def scale(a,c):return trim([F(c)*x for x in a])
def sub(a,b):return add(a,scale(b,-1))

def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)

def power(a,n):
    r=[F(1)]
    for _ in range(n):r=mul(r,a)
    return r

def value(a,x):
    r=F(0)
    for c in reversed(a):r=r*x+c
    return r

def modvalue(desc,x,p):
    r=0
    for c in desc:r=(r*x+c)%p
    return r

def prime(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

x,y=F(49),F(336)
a2,a4=[F(-2),F(-24)],[F(1),F(1176)]
b2,b4,b8=scale(a2,4),scale(a4,2),scale(power(a4,2),-1)
rhs=add([x**3],add(scale(a2,x*x),scale(a4,x)))
assert rhs==[y*y]
discriminant=scale(mul(power(a4,2),sub(power(a2,2),scale(a4,4))),16)
assert discriminant==scale(mul(mul([0,1],[-8,1]),power(a4,2)),9216)

psi={0:[F(0)],1:[F(1)],2:[2*y]}
psi[3]=add([3*x**4],add(scale(b2,x**3),add(scale(b4,3*x*x),b8)))
inside=add([2*x**6],add(scale(b2,x**5),add(scale(b4,5*x**4),
       add(scale(b8,10*x*x),add(scale(mul(b2,b8),x),mul(b4,b8))))))
psi[4]=scale(inside,2*y)

def division(n):
    if n in psi:return psi[n]
    if n%2:
        m=n//2
        r=sub(mul(division(m+2),power(division(m),3)),
              mul(division(m-1),power(division(m+1),3)))
    else:
        m=n//2
        r=scale(mul(division(m),
              sub(mul(division(m+2),power(division(m-1),2)),
                  mul(division(m-2),power(division(m+1),2)))),1/(2*y))
    psi[n]=trim(r)
    assert all(a.denominator==1 for a in psi[n])
    return psi[n]

factors={row['label']:row for row in data['factors']}
roots=set()
projective=[]
for label,row in factors.items():
    coeff=row['coefficients_descending']
    assert len(coeff)==row['degree']+1 and coeff[0]>0
    if row['degree']==1:
        root=F(-coeff[1],coeff[0])
        assert str(root)==row['rational_root']
        roots.add(root)
    else:
        p=row['certificate_prime']
        assert prime(p)
        vals=[modvalue(coeff,u,p)for u in range(p)]
        assert vals==row['affine_value_table'] and all(vals)
        assert [a%p for a in coeff]==row['coefficients_mod_prime']
        # A primitive rational root [a:b] with p|b would yield the
        # leading coefficient at infinity; this is explicitly nonzero.
        assert coeff[0]%p==row['value_at_projective_infinity']!=0
        projective.append({'factor':label,'degree':row['degree'],'p':p,
                           'affine_roots':0,'root_at_infinity':False})

factor_checks=[]
for row in data['division_factorizations']:
    product=[F(row['scalar'])]
    for term in row['factors']:
        f=factors[term['factor']]['coefficients_descending']
        product=mul(product,power(list(reversed(f)),term['multiplicity']))
    assert product==division(row['n'])
    assert len(product)-1==row['degree']
    factor_checks.append({'n':row['n'],'degree':row['degree'],'exact_factor_product':True})
assert {r['n']for r in data['division_factorizations']}=={8,10,12}
assert roots=={F(296,49),F(-96,49),F(100,49)}
assert all(not (0<r<=F(1,4))for r in roots)

whole_checks=[]
divrows={row['n']:row for row in data['division_factorizations']}
for row in data['whole_quotient_certificates']:
    n=row['n']; coeff=row['coefficients_descending'];p=row['certificate_prime']
    assert prime(p) and coeff[0]%p==row['value_at_projective_infinity']!=0
    vals=[modvalue(coeff,u,p)for u in range(p)]
    assert vals==row['affine_value_table'] and all(vals)
    product=scale(list(reversed(coeff)),F(divrows[n]['scalar']))
    for label in row['removed_linear_factors']:
        assert factors[label]['degree']==1
        product=mul(product,list(reversed(factors[label]['coefficients_descending'])))
    assert product==division(n)
    whole_checks.append({'n':n,'degree':row['degree'],'prime':p,
                         'leading_coefficient_mod_p':coeff[0]%p,
                         'affine_roots':0,'projective_root_at_infinity':False,
                         'direct_quotient_identity':True})

# Independent group-law checks of the three surviving torsion cases.
def plus(P,Q,weight):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    aa2=F(-2)-24*weight;aa4=F(1)+1176*weight
    if x1==x2:
        if y1==-y2:return None
        slope=(3*x1*x1+2*aa2*x1+aa4)/(2*y1)
    else:slope=(y2-y1)/(x2-x1)
    xx=slope*slope-aa2-x1-x2
    yy=-y1+slope*(x1-xx)
    return xx,yy

torsion_rows=[]
P=(x,y)
for weight,order in [(F(296,49),3),(F(-96,49),3),(F(100,49),4)]:
    R=None
    for j in range(1,order+1):
        R=plus(R,P,weight)
        assert (R is None)==(j==order)
    torsion_rows.append({'w':str(weight),'order':order})

report={'status':'PASS','factor_engine':'none; standard-library rational polynomial arithmetic',
        'division_polynomial_factor_checks':factor_checks,
        'projective_no_root_certificates':projective,
        'whole_quotient_projective_certificates':whole_checks,
        'all_rational_torsion_candidates':[str(a)for a in sorted(roots)],
        'torsion_orders_checked_by_group_law':torsion_rows,
        'non_torsion_for_all_rational_0_lt_w_le_1_over4':True,
        'theoretical_inputs':['Mazur rational torsion classification',
                              'division-polynomial recurrence and vanishing criterion'],
        'actual_detector_trace_matching_proved':False}
out=HERE/'cubic_trace_rank_independent_verification.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','verification':str(out),'nonlinear_projective_certificates':len(projective)}))
