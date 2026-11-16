#!/usr/bin/env python3
"""Independent exact check of the physical-trace completion obstruction.

Reconstructs every matrix entry from the certificate parameters using
SymPy's algebraic field and finite-field DomainMatrix determinant.
Imports no producer or sibling checker code.
"""
import argparse,json
from pathlib import Path
from itertools import combinations_with_replacement
import sympy as sp
from sympy.polys.domains import GF
from sympy.polys.matrices import DomainMatrix

rho=sp.sqrt(2);KD=sp.QQ.algebraic_field(rho)
z=sp.symbols('f0 x0 l0 i0 g0 y0 n0 j0 a0 b0 f1 x1 l1 i1 g1 y1 n1 j1 a1 b1 height')

def constants(rt):
 e=-1+sp.Rational(7,4)*rt;a=e**2;c=-sp.Rational(87,41)+sp.Rational(129,164)*rt;D=(3-rt)**2
 v=(c*c-2*a)/(2*c);r=1/v**2;q=1/a;u=1/v;w=v/a;S=v-c-a/v;T=c
 return [e,a,c,D,v,r,q,u,w,S,T]
cs=[constants(rho),constants(-rho)]
cks=[[KD.from_sympy(x) for x in c] for c in cs]

def identities(c,off):
 e,a,c0,D,v,r,q,u,w,S,T=c
 F,X,L,I,G,Y,N,J,A,B=z[off:off+10]
 base=[I-(L-1)**2,F*X+D*F**2-r**2,(I+2*L-1)*X-(1-D*r**2),
       J-(N-1)**2,G*Y+D*G**2-q**2,(J+2*N-1)*Y-(1-D*q**2),
       A*(X+D*F)-B*(Y+D*G),A*G-(q/r)*A*F-e*w*(q/r)*F*(S*N+T*L)]
 lin=e*(w*B-u*A)-S*N-T*L
 return base+[lin]+[x*lin for x in z]
polys=[sp.Poly(h,*z,domain=KD) for c,off in zip(cs,[0,10]) for h in identities(c,off)]
assert len(polys)==60

# Exact common false family with independent coupling parameters and height.
eta0,eta1,h=sp.symbols('eta0 eta1 h')
PD=KD.poly_ring(eta0,eta1,h)
vals=[]
for c,Z in zip(cks,PD.gens[:2]):
 e,a,c0,D,v,r,q,u,w,S,T=c
 assert e*e==a and D==a*(a-c0*c0) and a*u*w==KD.one
 assert r*S*S==1-D*r*r and q*T*T==1-D*q*q
 LN=-(S/c0)
 consts=[r/a,r*c0*c0,S/c0,(S/c0-1)**2,q/a,q*c0*c0,-KD.one,KD.convert(4)]
 vals += [PD.convert(x,KD) for x in consts]+[PD.convert(e*w*LN,KD)*Z,PD.convert(e*u*LN,KD)*Z]
vals.append(PD.gens[2])
for poly in polys:
 result=PD.zero
 for powers,co in poly.rep.terms():
  term=PD.convert(co,KD)
  for value,power in zip(vals,powers):term*=value**power
  result+=term
 assert result==PD.zero

# Universal algebraic certificate for the physical difference abscissa.
f,g,s,t,Dsymbol=sp.symbols('f g s t D')
M=(g*s+f*t)/(g-f);hh=f*g*(s+t)**2/(g-f)**2
cu=s*s-1/f+Dsymbol*f;cv=t*t-1/g+Dsymbol*g
assert sp.cancel((g-f)**2*(hh-(M*M-1/f-1/g))+(g-f)*(g*cu-f*cv))==0

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('trace-certificate.json'))
parser.add_argument('--output',type=Path)
args=parser.parse_args()
cert=json.loads(args.certificate.read_text());p=cert['prime'];rt=cert['rho_residue']
assert p==1009 and sp.isprime(p) and rt==439 and rt*rt%p==2

def mod(x):
 result=0
 for co in x.to_list():
  n=int(co.numerator);d=int(co.denominator);assert d%p
  result=(result*rt+n*pow(d,-1,p))%p
 return result
cms=[[mod(x) for x in c] for c in cks]
assert all(all(c) for c in cms)
mons=[()]+[(i,) for i in range(21)]+list(combinations_with_replacement(range(21),2))
assert len(mons)==253
powers=[]
for mon in mons:
 po=[0]*21
 for i in mon:po[i]+=1
 powers.append(tuple(po))
known=[[mod(poly.rep.to_dict().get(power,KD.zero)) for power in powers] for poly in polys]

def chart(c,data):
 e,a,c0,D,v,r,q,u,w,S,T=c;f,s,g,t=data
 assert f*g*s*t*(g-f)%p
 assert s*s%p==(pow(f,-1,p)-D*f)%p
 assert t*t%p==(pow(g,-1,p)-D*g)%p
 L=S*pow(s,-1,p)%p;N=T*pow(t,-1,p)%p
 C=L*N*(s+t)*pow(g-f,-1,p)%p
 vs=[r*f%p,r*s*s%p,L,(L-1)**2%p,q*g%p,q*t*t%p,N,(N-1)**2%p,e*w*f*C%p,e*u*g*C%p]
 hx=f*g*(s+t)**2*pow(g-f,-2,p)%p
 return vs,hx

def vector(values):
 row=[]
 for mon in mons:
  value=1
  for i in mon:value=value*values[i]%p
  row.append(value)
 return row
rows=[]
for parameters in cert['independent_parameter_rows']:
 plus,h0=chart(cms[0],parameters[:4]);minus,h1=chart(cms[1],parameters[4:])
 row=vector(plus+minus+[(h0+h1)%p])
 assert all(sum(a*b for a,b in zip(row,k))%p==0 for k in known)
 rows.append(row)
assert len(rows)==194
cols=cert['evaluation_minor_columns'];assert len(cols)==194 and len(set(cols))==194
mat=DomainMatrix.from_list([[row[j] for j in cols] for row in rows],GF(p))
det=int(mat.det());assert det==cert['evaluation_minor_determinant_mod_p']==451
kr=cert['identity_minor_rows'];kc=cert['identity_minor_columns']
assert len(kr)==len(kc)==59
kmat=DomainMatrix.from_list([[known[i][j] for j in kc] for i in kr],GF(p))
kdet=int(kmat.det());assert kdet==cert['identity_minor_determinant_mod_p']==929
receipt={'status':'PASS','independent_implementation':'SymPy algebraic fields, symbolic false-family identities and DomainMatrix over GF(1009)',
         'physical_difference_formula':'verified by an explicit curve-ideal identity',
         'rational_components_plus_trace':21,'monomials':253,
         'evaluation_rank':194,'known_identity_rank':59,
         'evaluation_minor_determinant':det,'identity_minor_determinant':kdet,
         'false_family_arbitrary_height_checked_symbolically':True,
         'characteristic_zero_lift':'rank16 Laurent algebra of four monic curve quadratics, as proved in manuscript',
         'scope':'same embedding and physical trace; no extra helper, no changed embedding, complete geometric image'}
blob=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if args.output:
 args.output.write_text(blob);print(json.dumps({'status':'PASS','output':str(args.output),'minors':[det,kdet]}))
else:print(blob,end='')
