#!/usr/bin/env python3
"""Exact identities and finite-field certificate for the second section."""
from pathlib import Path
import json
import sympy as s

r,u=s.symbols('r u')
w=r*r-1
A=-2-24*w
B=1+1176*w
def rhs(x):return x**3+A*x*x+B*x
P=(s.Integer(49),s.Integer(336))
Q=(s.Integer(25),120*r)
assert s.expand(P[1]**2-rhs(P[0]))==0
assert s.expand(Q[1]**2-rhs(Q[0]))==0
def add(P,Q):
    x,y=P;z,t=Q
    m=s.cancel((t-y)/(z-x))
    xx=s.factor(m*m-A-x-z)
    yy=s.factor(-y+m*(x-xx))
    assert s.expand(yy*yy-rhs(xx))==0
    return xx,yy
plus=add(P,Q)
minus=add(P,(Q[0],-Q[1]))
assert s.expand(plus[0]-(7*r-10)**2)==0
assert s.expand(minus[0]-(7*r+10)**2)==0
assert s.cancel(1+4*u/(1-u)**2-((1+u)/(1-u))**2)==0

rows=[]
for p in (7,11,13):
    aa=-74%p;bb=3529%p
    assert 16*bb*bb*(aa*aa-4*bb)%p != 0
    pts=[(x,y) for x in range(p) for y in range(p)
         if (y*y-x*x*x-aa*x*x-bb*x)%p==0]
    rows.append({'p':p,'affine_points':pts,'order':len(pts)+1})
assert [z['order']for z in rows]==[12,16,18]

report={'status':'PASS','P':['49','336'],'Q':['25','120*r'],
        'P_plus_Q':[str(z)for z in plus],
        'P_minus_Q':[str(z)for z in minus],
        'specialization':'r=2,w=3','point_count_certificates':rows,
        'generic_independence_argument':'r -> -r fixes P and negates Q; both specialize to non-torsion points',
        'actual_detector_matching_proved':False}
here=Path(__file__).resolve().parent
(here/'second_trace_section_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','orders':[z['order']for z in rows]}))
