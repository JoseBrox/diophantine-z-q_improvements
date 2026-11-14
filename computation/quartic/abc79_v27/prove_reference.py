#!/usr/bin/env python3
"""Produce explicit ideal-membership certificates; SymPy is producer only."""
from pathlib import Path
import json,importlib.util
import sympy as s
from reference import equations
HERE=Path(__file__).resolve().parent
rho=s.sqrt(2);T,S,f,B,w=s.symbols('T S f B w');VARS=(T,S,f)
D=11-6*rho;a=s.Rational(57,8)-s.Rational(7,2)*rho;b=-s.Rational(165,8)+s.Rational(417,32)*rho
q=lambda v:({(0,(v,)):1},{})
raw=equations(q(1),q(2),q(3),q(4),q(5))
symbols={1:f,2:S,3:B,4:w,5:T}
def expr(p):
 return sum(s.Rational(c.numerator,c.denominator)*s.prod(symbols[i] for i in m) for (aa,m),c in p.items())
Q1,MW,Q3,M,L=[s.expand(expr(p)+rho*expr(q)) for p,q in raw]
P=lambda x:s.Poly(x,*VARS,extension=rho)
F1=P(Q1.subs(B,f*f));F2=P(Q3.subs(B,f*f))
# A small Buchberger computation carrying representations in the original pair.
zero=P(0);one=P(1)
G=[F1.monic(),F2.monic()];R=[(P(1/F1.LC()),zero),(zero,P(1/F2.LC()))]
pairs=[(0,1)]
def multmon(exponent,coefficient):return P(coefficient*s.prod(v**n for v,n in zip(VARS,exponent)))
def divide(g):
 qs=[zero for _ in G];rem=zero
 while not g.is_zero:
  me=g.monoms()[0];ce=g.coeffs()[0]
  for i,h in enumerate(G):
   mh=h.monoms()[0]
   if all(x>=y for x,y in zip(me,mh)):
    z=multmon(tuple(x-y for x,y in zip(me,mh)),ce/h.coeffs()[0]);qs[i]+=z;g-=z*h;break
  else:
   z=multmon(me,ce);rem+=z;g-=z
 return qs,rem
while pairs:
 i,j=pairs.pop(0);mi=G[i].monoms()[0];mj=G[j].monoms()[0];mm=tuple(max(x,y) for x,y in zip(mi,mj))
 u=multmon(tuple(x-y for x,y in zip(mm,mi)),1/G[i].LC());v=multmon(tuple(x-y for x,y in zip(mm,mj)),1/G[j].LC())
 ss=u*G[i]-v*G[j];rr=[u*R[i][k]-v*R[j][k] for k in range(2)]
 qs,rem=divide(ss)
 for z,rep in zip(qs,R):
  for k in range(2):rr[k]-=z*rep[k]
 if not rem.is_zero:
  lc=rem.LC();rem=rem.monic();rr=tuple(x.mul_ground(1/lc) for x in rr)
  assert rr[0]*F1+rr[1]*F2==rem
  nn=len(G);pairs.extend((i,nn) for i in range(nn));G.append(rem);R.append(rr)
  if len(G)>30:raise RuntimeError('Unexpected basis growth')
print('Basis size',len(G),flush=True)
g=(((118+60*rho)*S+156+s.Rational(69,2)*rho)*T-(156+s.Rational(69,2)*rho)*S+288+128*rho)/(252-672*rho)
AP=a*a+D;BP=a*a-D
Lf=2*b*D*(a*T-b);Lg=2*b*D*(a*S+b)
Qf=a*AP*S*T+b*AP*S-b*BP*T+4*a*a*D
Qg=-a*AP*S*T-b*BP*S+b*AP*T-4*a*a*D
M0=M.subs(B,f*f);L0=L.subs(B,f*f)
targets={'curve':f*S*S+D*f*f-1,'first':Lf*f-Qf,'second':Lg*g*g-f*Qg,'third':D*D*f*g*g+a*D*(f*f+g*g)+f*(a*S*T+b*(S-T)+D),'weight':M0*g**4+f*f*L0}
def ser(poly):
 out=[]
 for m,c in poly.terms():
  c=s.expand(c);aa=c.coeff(rho,0);bb=c.coeff(rho,1)
  assert s.simplify(c-aa-bb*rho)==0
  out.append(dict(m=list(m),c=[str(aa),str(bb)]))
 return out
cert=[]
for name,target in targets.items():
 target=P(target);qs,rem=divide(target);assert rem.is_zero,name
 rr=[zero,zero]
 for z,rep in zip(qs,R):
  for k in range(2):rr[k]+=z*rep[k]
 assert rr[0]*F1+rr[1]*F2==target,name
 cert.append(dict(name=name,target=ser(target),U=ser(rr[0]),V=ser(rr[1])))
 print(name,'terms',len(rr[0].terms()),len(rr[1].terms()),flush=True)
# These coefficients and targets are independently reconstructed by the checker.
NN=b*AP*S+4*a*a*D+2*b*b*D*f
DD=2*a*b*D*f-a*AP*S+b*BP
curve=P(f*S*S+D*f*f-1)
forward=[]
for name,ff in [('Q1',F1),('Q3',F2)]:
    degree=ff.degree(T)
    target=P(sum(c*NN**m[0]*DD**(degree-m[0])*S**m[1]*f**m[2] for m,c in ff.terms()))
    qq,rr=target.div(curve);assert rr.is_zero,name
    forward.append(dict(name=name,degreeT=degree,target=ser(target),quotient=ser(qq)))
report=dict(schema='compressed-reference-identity-certificate/v27',variableOrder=['T','S','f'],Q1=ser(F1),Q3=ser(F2),identities=cert,forward=forward,basisSize=len(G),scope='Explicit polynomial identities; the rational-point exception proof is stated separately.')
(HERE/'reference-certificate.json').write_text(json.dumps(report,indent=2)+'\n')
# Machine-readable original five-variable equations, preserving their exact field coefficients.
def rawser(pq):
 keys=sorted(set(pq[0])|set(pq[1]));return [dict(m=list(m),c=[str(pq[0].get((aa,m),0)),str(pq[1].get((aa,m),0))]) for aa,m in keys]
(HERE/'reference-equations.json').write_text(json.dumps(dict(schema='compressed-reference-equations/v27',variableOrder=['f','S','B','w','T'],equations={n:rawser(p) for n,p in zip(['Q1','Mw+L','Q3','M','L'],raw)}),indent=2)+'\n')
