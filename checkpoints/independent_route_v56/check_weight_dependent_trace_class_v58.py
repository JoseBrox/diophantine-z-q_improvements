#!/usr/bin/env python3
"""Exact identities; does not assert actual detector realization."""
import json
from pathlib import Path
import sympy as s
V,w,x,z,u=s.symbols('V w x z u')
C=V**2+w*(2-V)
D=1+w*(2-V)
f=s.expand(C*D)
a=w**2-4*w-2
b=(w+1)*(3*w+1)
g=x*(x*x+a*x+b)
assert s.expand(w*w*f-g.subs(x,D))==0
assert s.factor(s.discriminant(f,V))==w*(w-8)*(w+1)**2*(3*w+1)**2
assert s.factor(16*b*b*(a*a-4*b))==16*w**3*(w-8)*(w+1)**2*(3*w+1)**2
assert s.factor(f-((1-w)*V+2*w)**2)==-w*(V-2)*(V-1)**2
assert s.expand(f.subs(V,1)-(1+w)**2)==0
assert s.expand(f.subs(V,2)-4)==0
assert s.expand(f.subs(V,-1)-(1+3*w)**2)==0
assert s.cancel((1+2*w-b/D)/w-(w-(1+2*w)*V)/D)==0
assert s.factor(f-(s.Rational(1,4)*(4-5*w)*(V-2)+2)**2)==-w*(V-2)**2*(16*V+9*w-8)/16

# Exact first multiplication coordinates in the Weierstrass model.
P=(1+w,w*(1+w))
def add(P,Q):
    xx,yy=P;xx2,yy2=Q
    m=s.cancel((3*xx*xx+2*a*xx+b)/(2*yy) if P==Q else (yy2-yy)/(xx2-xx))
    xx3=s.cancel(m*m-a-xx-xx2)
    yy3=s.cancel(-yy+m*(xx-xx3))
    return xx3,yy3
P2=add(P,P)
P3=add(P2,P)
assert all(s.cancel(a-b)==0 for a,b in zip(P2,(1,-2*w)))
assert all(s.cancel(a-b)==0 for a,b in zip(P3,(9*(1+w),-3*(1+w)*(3*w+8))))

certificate={
 'class':str(D),
 'test':str(f),
 'weierstrass_a2':str(a),
 'weierstrass_a4':str(b),
 'discriminant':str(s.factor(16*b*b*(a*a-4*b))),
 'trace_sections':[[1,'1+w'],[2,2],[-1,'1+3*w']],
 'twice_Q':[str(t) for t in P2],
 'three_times_Q':[str(s.factor(t)) for t in P3],
 'linear_class_split3_primary_source':'Sun, arXiv:2610.20691v3, Theorem4.1,p16',
 'prime_congruence': 'p=Norm(pi)=1 mod24 from pi=9 mod16, pi=i mod3',
 'scope':'Sound and locally prepared criterion; actual simultaneous rational realization unproved',
 'new_defining_variable_bound':False,
}
Path(__file__).with_name('weight_dependent_trace_class_v58_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
