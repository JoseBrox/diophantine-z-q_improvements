#!/usr/bin/env python3
"""Independently reconstruct the characteristic-zero identities and rank minors.

Uses SymPy's algebraic number field and finite-field matrix implementation;
imports no code from check.py. The product-closure extension is proved in
the manuscript and does not rely on a numerical sample.
"""
import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path
import sympy as sp
from sympy.polys.domains import GF
from sympy.polys.matrices import DomainMatrix

rho=sp.sqrt(2)
KD=sp.QQ.algebraic_field(rho)
e=-1+sp.Rational(7,4)*rho
a=sp.Rational(57,8)-sp.Rational(7,2)*rho
c=-sp.Rational(87,41)+sp.Rational(129,164)*rho
D=(3-rho)**2
v=(c*c-2*a)/(2*c)
r=1/v**2;q=1/a;u=1/v;w=v/a
S=v-c-a/v;T=c
E,A,C,DD,V,R,Q,U,W,SS,TT=map(KD.from_sympy,[e,a,c,D,v,r,q,u,w,S,T])
assert E*E==A and DD==A*(A-C*C)
assert A*U*W==KD.one and V*(V-A*(U+W)-2*C)==DD/A
assert R*SS*SS==1-DD*R*R and Q*TT*TT==1-DD*Q*Q

names=['F','X','L','I','G','Y','N','J','a1','a2']
z=sp.symbols(' '.join(names))
F,X,L,I,G,Y,N,J,a1,a2=z
base=[I-(L-1)**2,F*X+D*F**2-r**2,(I+2*L-1)*X-(1-D*r**2),
      J-(N-1)**2,G*Y+D*G**2-q**2,(J+2*N-1)*Y-(1-D*q**2),
      a1*(X+D*F)-a2*(Y+D*G)]
extra=a1*G-(q/r)*a1*F-e*w*(q/r)*F*(S*N+T*L)
linear=e*(w*a2-u*a1)-S*N-T*L
expressions=base+[extra,linear]+[zz*linear for zz in z]
polys=[sp.Poly(expr,*z,domain=KD) for expr in expressions]
assert len(polys)==19

def evaluate(poly,values,domain=KD):
    result=domain.zero
    for powers,coeff in poly.rep.terms():
        term=domain.convert(coeff,KD)
        for value,power in zip(values,powers):term*=value**power
        result+=term
    return result

def pair(x,y):return KD.from_sympy(sp.Rational(x)+sp.Rational(y)*rho)

def dbl(point):
    x,y=point;m=(3*x*x-DD)/(2*y);xx=m*m-2*x
    return xx,m*(x-xx)-y

R0=(KD.from_sympy(1+rho),KD.from_sympy(2*rho))
PP=dbl(R0);HH=dbl(PP)
assert PP==(A,A*C) and HH[0]==V*V and HH[1]/HH[0]==SS

# The fixed-reference false tangent family is polynomial in its free value.
zz=sp.Symbol('zeta');PD=KD.poly_ring(zz);ZETA=PD.gens[0]
consts=[R/A,R*C*C,SS/C,(SS/C-1)**2,Q/A,Q*C*C,-KD.one,KD.convert(4)]
LN=(SS/C)*(-KD.one)
family=[PD.convert(x,KD) for x in consts]+[PD.convert(E*W*LN,KD)*ZETA,PD.convert(E*U*LN,KD)*ZETA]
assert all(evaluate(poly,family,PD)==PD.zero for poly in polys)
false_nonzero=consts+[E*W*LN*2*V,E*U*LN*2*V]
assert all(evaluate(poly,false_nonzero)==KD.zero for poly in polys)
assert false_nonzero[8] and false_nonzero[9]
assert false_nonzero[8]*false_nonzero[9]/(LN*LN)==4*HH[0]

# The R0-reference fixture is separately evaluated from its own constants.
r0=rho-1;S0=4-2*rho;v0=(S0+c)/(1-a*r0);u0=v0*r0
r0k,S0k,v0k,u0k=map(KD.from_sympy,[r0,S0,v0,u0])
assert A*u0k*u0k==KD.one
small_vals=[pair(3,-2),pair(-56,40),KD.one,KD.zero,
            pair(3,-2),pair(-56,40),KD.one,KD.zero,KD.zero,KD.zero]
small_rows=[I-(L-1)**2,F*X+D*F**2-r0**2,(I+2*L-1)*X-(1-D*r0**2),
            J-(N-1)**2,G*Y+D*G**2-r0**2,(J+2*N-1)*Y-(1-D*r0**2),
            a1*(X+D*F)-a2*(Y+D*G),e*u0*(a2-a1)-S0*N+S0*L]
assert all(evaluate(sp.Poly(h,*z,domain=KD),small_vals)==KD.zero for h in small_rows)
assert sp.simplify(2*a.expand().coeff(rho,0))==sp.Rational(57,4)

# Exact universal identities in the function field, before reduction modulo p.
f,g,s,t=sp.symbols('f g s t')
FD=KD.frac_field(f,g)
fmap=[r*f,r*s**2,S/s,(S/s-1)**2,q*g,q*t**2,T/t,(T/t-1)**2,
      e*w*(S/s)*(T/t)*f*(s+t)/(g-f),
      e*u*(S/s)*(T/t)*g*(s+t)/(g-f)]
common=s**4*t**4*(g-f)**2
s_square=FD.from_sympy(1/f-D*f);t_square=FD.from_sympy(1/g-D*g)
normal_form_checks=[]
for number,expr in enumerate(base+[extra,linear]):
    cleared=sp.cancel(expr.subs(dict(zip(z,fmap)))*common)
    poly=sp.Poly(cleared,s,t,domain=FD)
    coeffs=[FD.zero]*4
    for (i,j),co in poly.rep.terms():
        coeffs[(i%2)+2*(j%2)]+=co*s_square**(i//2)*t_square**(j//2)
    assert all(co==FD.zero for co in coeffs),(number,coeffs)
    normal_form_checks.append(number)

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
parser.add_argument('--output',type=Path)
args=parser.parse_args()
cert=json.loads(args.certificate.read_text())
qs=cert['quadratic_span'];p=qs['prime'];rt=qs['rho_residue']
assert p==1009 and sp.isprime(p) and rt==439 and rt*rt%p==2

def mod(x):
    ans=0
    for coefficient in x.to_list():
        n=int(coefficient.numerator);d=int(coefficient.denominator)
        assert d%p
        ans=(ans*rt+n*pow(d,-1,p))%p
    return ans

em,am,cm,dm,vm,rm,qm,um,wm,sm,tm=map(mod,[E,A,C,DD,V,R,Q,U,W,SS,TT])
assert all([em,am,cm,dm,vm,rm,qm,um,wm,sm,tm])
mons=[()]+[(i,) for i in range(10)]+list(combinations_with_replacement(range(10),2))
powers=[]
for mon in mons:
    power=[0]*10
    for i in mon:power[i]+=1
    powers.append(tuple(power))
known=[[mod(poly.rep.to_dict().get(power,KD.zero)) for power in powers] for poly in polys]

def vector(values):
    result=[]
    for mon in mons:
        x=1
        for i in mon:x=x*values[i]%p
        result.append(x)
    return result

rows=[]
for f0,s0,g0,t0 in qs['minor_sample_pairs']:
    assert f0*g0*s0*t0*(g0-f0)%p
    assert s0*s0%p==(pow(f0,-1,p)-dm*f0)%p
    assert t0*t0%p==(pow(g0,-1,p)-dm*g0)%p
    ll=sm*pow(s0,-1,p)%p;nn=tm*pow(t0,-1,p)%p
    hh=ll*nn*(s0+t0)*pow(g0-f0,-1,p)%p
    values=[rm*f0%p,rm*s0*s0%p,ll,(ll-1)**2%p,
            qm*g0%p,qm*t0*t0%p,nn,(nn-1)**2%p,
            em*wm*f0*hh%p,em*um*g0*hh%p]
    row=vector(values)
    assert all(sum(a*b for a,b in zip(row,k))%p==0 for k in known)
    rows.append(row)
assert len(rows)==47
columns=qs['minor_columns'];assert len(columns)==47 and len(set(columns))==47
minor=DomainMatrix.from_list([[row[j] for j in columns] for row in rows],GF(p))
det=int(minor.det());assert det==qs['minor_determinant_mod_p']==541
kc=qs['known_minor_columns'];kr=qs['known_minor_rows']
kminor=DomainMatrix.from_list([[known[i][j] for j in kc] for i in kr],GF(p))
kdet=int(kminor.det());assert kdet==qs['known_minor_determinant_mod_p']==968
assert DomainMatrix.from_list(known,GF(p)).rank()==19
assert DomainMatrix.from_list(rows,GF(p)).rank()==47
assert DomainMatrix.from_list([row[:11] for row in rows],GF(p)).rank()==10
for label,values in [('zero',consts+[KD.zero,KD.zero]),('nonzero',false_nonzero)]:
    row=vector([mod(x) for x in values])
    assert all(sum(x*y for x,y in zip(row,k))%p==0 for k in known),label

receipt={'status':'PASS','independent_implementation':'SymPy exact algebraic field, Laurent normal forms, and DomainMatrix over GF(1009)',
         'universal_normal_form_identities':len(normal_form_checks),'tangent_family_checked_symbolically':True,
         'exact_counterexamples':['zero coupling: trace 0 instead of 57/4','nonzero coupling: four times true abscissa'],
         'evaluations':47,'evaluation_minor_determinant':det,'identity_minor_determinant':kdet,
         'evaluation_rank':47,'identity_rank':19,'linear_evaluation_rank':10,
         'characteristic_zero_lift':'monic normal-form proof in manuscript',
         'conjugate_component_extension':'product-closure proof in manuscript',
         'global_variable_count_lower_bound':False}
blob=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if args.output:
    args.output.write_text(blob);print(json.dumps({'status':'PASS','output':str(args.output)}))
else:print(blob,end='')
