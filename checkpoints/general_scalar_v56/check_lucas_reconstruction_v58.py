#!/usr/bin/env python3
"""Exact algebra supporting the scoped Lucas reconstruction results."""
from pathlib import Path
import json
import sympy as sp

s,t,b,z,a,u,v,w,r=sp.symbols('s t b z a u v w r')
d=a-2
F=t*t-a*d*t*b+d*d*b*b-1
rad=(a*a-4)*d*d*b*b+4
assert sp.expand(4*F-((2*t-a*d*b)**2-rad))==0
assert sp.expand(rad-(a*d*b)**2-4*(1-d*d*b*b))==0
R=r-u*s
A=w*w+v*w*a*d+v*v*d*d
B=R*(-2*w-v*a*d)
C=R*R-v*v
assert sp.expand(v*v*F.subs(t,(R-w*b)/v)-(A*b*b+B*b+C))==0
assert sp.expand(A-(v*(w+v)*a*a-2*v*(w+2*v)*a+w*w+4*v*v))==0
assert sp.expand(A.subs(w,-v)-v*v*(5-2*a))==0
assert sp.expand(F.subs({t:a,b:1/d}))==0

fixtures=[]
for sv in range(3,16):
 av=sv*sv;dv=av-2;kv=2*dv
 U0,U1=0,1
 for j in range(kv):
  U0,U1=U1,av*U1-U0
 assert U0%dv==0
 bv=U0//dv;tv=U1;zv=2*tv-av*dv*bv
 assert tv*tv-av*dv*tv*bv+dv*dv*bv*bv==1
 assert zv*zv==(av*av-4)*dv*dv*bv*bv+4
 assert (zv+av*dv*bv)%2==0
 assert (zv+av*dv*bv)//2==tv
 fixtures.append({'s':sv,'a':av,'k':kv,'t_bits':tv.bit_length(),
                  'b_bits':bv.bit_length(),'z_bits':abs(zv).bit_length()})

certificate={
 'status':'PASS',
 'monic_discriminant_and_parity_identity':True,
 'affine_elimination_identity':True,
 'nonzero_leading_polynomial_exception_branch':'A(a)|_{w=-v}=v^2(5-2a)',
 'rational_cofactor_counterfamily':{'b':'1/(a-2)','t':'a','residual':0},
 'exact_numerical_lucas_witnesses':fixtures,
 'scope':'The density theorem additionally uses the cited Mordell-Lang theorem and the proved conjugate-generator independence; no finite search certifies density or a variable bound.'
}
Path(__file__).with_name('lucas_reconstruction_v58_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps({k:v for k,v in certificate.items() if k!='exact_numerical_lucas_witnesses'},indent=2))
print('Exact Lucas witnesses:',len(fixtures))
