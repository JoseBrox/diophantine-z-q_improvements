#!/usr/bin/env python3
"""Exact square-prefactor incidence and branch-discriminant identities."""
import json
from pathlib import Path
import sympy as sp

s,a,N,u,c,d=sp.symbols('s a N u c d')
g=s*s
w=g-1
V=2*a/N
J=1/N
R=(1-V/g+J/g**2)*(1+(1-V/2)/w)
f=(s*s-1)*(N*s*s-a)*(N*s**4-2*a*s*s+1)
assert sp.cancel(R*(s*s*(s*s-1)*N)**2-f)==0
disc=4096*a*N**6*(a-N)**4*(a*a-N)**6*(2*a-N-1)**4
assert sp.expand(sp.discriminant(f,s)-disc)==0
assert sp.cancel(1+4*u/(1-u)**2-((1+u)/(1-u))**2)==0

# When W=Z^2, Z=c+d sqrt2, the quartic splits over Q(sqrt2).
sqrt2=sp.sqrt(2)
Z=c+d*sqrt2
Zbar=c-d*sqrt2
aa=c*c+2*d*d
NN=(c*c-2*d*d)**2
assert sp.expand((s*Z-1)*(s*Z+1)*(s*Zbar-1)*(s*Zbar+1)
                 -(NN*s**4-2*aa*s*s+1))==0

out={'status':'PASS',
     'native_curve':'Y^2=(s^2-1)(N s^2-a)(N s^4-2 a s^2+1)',
     'square_multiplier':'s^2(s^2-1)N',
     'discriminant':str(disc),
     'degree':8,'genus_when_discriminant_nonzero':3,
     'weight_normalizer':'4u/(1-u)^2',
     'scope':'Exact algebra and branch discriminant; no prescribed finite rational point is deduced.'}
Path(__file__).with_name('g_square_incidence_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
