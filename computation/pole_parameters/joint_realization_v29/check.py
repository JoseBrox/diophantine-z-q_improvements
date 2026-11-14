#!/usr/bin/env python3
"""Exact checks for joint pole realization and the fixed-scale correspondences.

The default mode reconstructs the deterministic certificate and compares it
with the published bytes. --output writes a certificate to the specified path.
These checks do not certify the retained infinite arithmetic inputs.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import isqrt
from pathlib import Path
import sys
from typing import Optional

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / 'data/audits/joint_pole_realization_20261114_v29.json'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def zero(expr: sp.Expr, label: str) -> None:
    require(sp.cancel(expr) == 0, label)


def nonsquare(value: F) -> bool:
    return value < 0 or isqrt(value.numerator)**2 != value.numerator or isqrt(value.denominator)**2 != value.denominator


def rational(value: F) -> str:
    return str(value)


def v2(value: F) -> int:
    require(value != 0, 'v2 requires a nonzero argument')
    def valuation(n: int) -> int:
        return (abs(n) & -abs(n)).bit_length() - 1
    return valuation(value.numerator) - valuation(value.denominator)


def prepared(value: F) -> bool:
    if not 0 < value < 1 or isqrt(value.denominator)**2 != value.denominator:
        return False
    v = v2(value)
    if v < 4 or v % 2:
        return False
    unit = value / F(2)**v
    return unit.numerator * pow(unit.denominator, -1, 8) % 8 == 1


def symbolic_transfers() -> dict:
    b, B, V, z, c, e, p, s, q, t, u, v = sp.symbols('b B V z c e p s q t u v')
    old0 = p**2 - B*(1-e)*(1+3*e)
    old1 = B*q**2 - (s**2-e*V)*(s**2+3*e*V)
    sub = {B:z**2*B, V:z**4*c**2*V, p:z*p, s:z**2*c*s, q:z**3*c**2*q}
    zero(old0.subs(sub, simultaneous=True)-z**2*old0, 'old first equation')
    zero(old1.subs(sub, simultaneous=True)-z**8*c**4*old1, 'old second equation')
    compat17 = 17-z**2*b-c**2*(17-b)
    zero(17*(z**2*b)**2*(17-z**2*b)-z**4*c**2*17*b**2*(17-b)-17*z**4*b**2*compat17,
         'old V scaling modulo the compatibility equation')
    et = (t**2-B)/(t**2+3*B)
    pt = -4*B*t/(t**2+3*B)
    zero(et.subs({t:z*t, B:z**2*B}, simultaneous=True)-et, 'old common e chart')
    zero(pt.subs({t:z*t, B:z**2*B}, simultaneous=True)-z*pt, 'old scaled tau chart')
    new = [e**2+b*p**2-1, u*v-e*(1-b), u**2-v**2-b*q**2]
    subn = {b:z**2*b,p:p/z,u:c*u,v:c*v,q:c*q/z}
    compat1 = 1-z**2*b-c**2*(1-b)
    zero(new[0].subs(subn, simultaneous=True)-new[0], 'new first equation')
    zero(new[1].subs(subn, simultaneous=True)-c**2*new[1]+e*compat1, 'new middle equation')
    zero(new[2].subs(subn, simultaneous=True)-c**2*new[2], 'new last equation')
    # Four deliberate incorrect replacements must fail an exact identity.
    mutations = []
    for name, expression in [
        ('old q scaled by z^2 instead of z^3', old1.subs({**sub,q:z**2*c**2*q}, simultaneous=True)-z**8*c**4*old1),
        ('old s scaled by z instead of z^2', old1.subs({**sub,s:z*c*s}, simultaneous=True)-z**8*c**4*old1),
        ('new p multiplied rather than divided by z',new[0].subs({**subn,p:z*p}, simultaneous=True)-new[0]),
        ('new q not divided by z',new[2].subs({**subn,q:c*q}, simultaneous=True)-c**2*new[2])
    ]:
        require(sp.cancel(expression) != 0, 'corruption escaped: '+name)
        mutations.append(name)
    return dict(exact_identities=8, corruption_controls=mutations)


def elliptic_scaling() -> dict:
    n,b,a0,a1,Y0,Y1,c,theta,x,y = sp.symbols('n b a0 a1 Y0 Y1 c theta x y')
    e=n/(b*a0**2);p=Y0/(b**2*a0**3)
    u=a1/a0;v=e*(1-b)/u;q=Y1/(b**2*a0**3*u**2)
    f0=Y0**2-(b*a0**2)**3+n**2*b*a0**2
    f1=Y1**2-(b*a1**2)**3+n**2*(1-b)**2*b*a1**2
    zero(e**2+b*p**2-1-f0/(b**3*a0**6), 'first elliptic division')
    zero(u*v-e*(1-b), 'common e middle equation')
    zero(u**2-v**2-b*q**2+f1/(b**3*a0**6*u**4), 'second elliptic division')
    zero((c**3*y)**2-(c**2*x)**3+(n*theta*c**2)**2*c**2*x-c**6*(y**2-x**3+(n*theta)**2*x),
         'twist scaling')
    # The two radicals used in the retained (e,u) presentation.
    E,U = sp.symbols('E U')
    aa=b*(1-E**2);cc=b*(U**4-E**2*(1-b)**2)
    zero(E**2+b*aa/b**2-1,'first square-root recovery')
    zero(U**2-(E*(1-b)/U)**2-b*cc/(b**2*U**2),'second square-root recovery')
    return dict(exact_identities=6)


def check_witness(b: F, w: tuple[F,F,F,F,F]) -> None:
    e,p,u,v,q=w
    require(e*e+b*p*p==1,'rational first residual')
    require(u*v==e*(1-b),'rational middle residual')
    require(u*u-v*v==b*q*q,'rational last residual')


def exact_example() -> dict:
    b0=F(4880,9801)
    base=(F(41,81),F(11,9),F(41,81),F(4921,9801),F(1,11))
    check_witness(b0,base)
    e,p,u,v,q=base
    samples=[]
    for t in [F(2),F(3),F(5),F(1,3),F(8),F(16),F(17),F(33),F(65)]:
        z=((1-b0)*t*t-2*(1-b0)*t-b0)/(b0+(1-b0)*t*t)
        c=1+t*(z-1)
        b1=b0*z*z
        require(b0*z*z+(1-b0)*c*c==1,'compatibility conic')
        require(z*c!=0 and prepared(b0) and prepared(b1),'prepared example')
        w1=(e,p/z,c*u,c*v,c*q/z)
        check_witness(b1,w1)
        require(all(w1),'nondegenerate transferred example')
        samples.append(dict(t=rational(t),z=rational(z),c=rational(c),input=rational(b1),witness=[rational(a) for a in w1]))
    beta,theta=305,4921
    require(b0==F(beta)*F(4,99)**2 and 1-b0==F(theta)*F(1,99)**2,'exact square classes')
    require(beta%8==theta%8==1 and sp.gcd(beta,theta)==1,'twist congruences')
    for ell in sp.factorint(beta): require(pow(theta,(int(ell)-1)//2,int(ell))==1,'theta is a residue')
    for ell in sp.factorint(theta): require(pow(beta,(int(ell)-1)//2,int(ell))==1,'beta is a residue')
    # Outside a common square class the first conic cannot share nondegenerate e.
    b2=F(409,441)*b0
    require(prepared(b2), 'incompatible control is still prepared')
    require(nonsquare(b2/b0), 'incompatible input control')
    require(nonsquare((1-e*e)/b2), 'common e fails on incompatible class')
    return dict(base_input=str(b0),base_witness=[str(a) for a in base],common_beta=beta,common_theta=theta,
                prepared_transfers=samples,incompatible_class_control=True)


def sqrt_selector_matrix(values: list[int]) -> tuple[sp.Matrix,sp.Rational]:
    vals=list(map(sp.Rational,values));k=len(vals);dim=1<<k
    L=4*(1+sum(a*a for a in vals))*(1+sum(1/(a*a) for a in vals))
    M=sp.eye(dim)
    for col in range(dim):
        for i,a in enumerate(vals):
            row=col^(1<<i)
            M[row,col]+=L**(i+1)*(a if col&(1<<i) else 1)
    return M,L


def finite_algebra() -> dict:
    x=sp.symbols('x')
    cases=[[1],[2],[-1],[1,4],[2,8],[2,2],[-1,-4],[1,-1],[4,9],[2,3],[1,4,9],[2,8,18],[1,2,8]]
    output=[]
    for values in cases:
        M,L=sqrt_selector_matrix(values)
        cp=sp.Poly(M.charpoly(x).as_expr(),x,domain=sp.QQ)
        factors=sp.factor_list(cp)[1]
        linear=sum(mult for f,mult in factors if f.degree()==1)
        want=all(not nonsquare(F(a)) for a in values)
        require((linear>0)==want,'rational selector root criterion')
        require(sp.gcd(cp,cp.diff()).degree()==0,'selector is squarefree')
        require(cp.eval(0)!=0,'selector has no zero root')
        output.append(dict(radicands=values,dimension=M.rows,linear_factors=linear,all_rational_squares=want,
                           characteristic_polynomial_sha256=hashlib.sha256(str(cp.as_expr()).encode()).hexdigest()))
    # Without separation, sqrt(8)-2sqrt(2)=0 is a false rational-root certificate.
    values=[2,8];dim=4;bad=sp.zeros(dim)
    for col in range(dim):
        for i,a in enumerate(values):
            bad[col^(1<<i),col]+=(-2 if i==0 else 1)*(a if col&(1<<i) else 1)
    require(bad.det()==0 and nonsquare(F(2)),'unseparated-element negative control')
    # A full polynomial with a guard: D=a^2, C=D*M, P=det(I-Y*D*C).
    a,Y=sp.symbols('a Y')
    C=sp.Matrix([[a**2,4*a*(a*a+1)**2],[4*(a*a+1)**2,a**2]])
    P=sp.expand((sp.eye(2)-Y*a**2*C).det())
    require(P.subs(a,0)==1,'zero radicand boundary is excluded')
    at=sp.Rational(4);L=4*(1+at**2)*(1+at**-2)
    yy=1/(at**4*(1+L*2))
    require(P.subs({a:at,Y:yy})==0,'guarded polynomial positive control')
    return dict(examples=output,negative_controls=['unseparated radical cancellation','zero-radicand boundary'],
                guarded_one_radical_polynomial=str(P))


def contacts_and_genera() -> dict:
    theta=[F(0),F(-1,2),F(-1,4),F(-2,5),F(-1),F(-1,3)]
    nonzero=theta[1:]
    ratios=sorted({u/v for u in nonzero for v in nonzero})
    require(min(ratios)==F(1,4) and max(ratios)==4,'six-contact scale collision range')
    t,a=sp.symbols('t a')
    G=sp.prod(t-sp.Rational(c.numerator,c.denominator) for c in nonzero)
    result=sp.factor(sp.resultant(G,G.subs(t,a*t),t))
    output=[]
    for scale in [F(5),F(81),F(729),F(25,4),F(409,17)]:
        rr=sp.Rational(scale.numerator,scale.denominator)
        curve=sp.Poly(rr*G*G.subs(t,rr*t),t)
        require(curve.degree()==10 and sp.gcd(curve,curve.diff()).degree()==0,'genus-four branch count')
        output.append(dict(scale=str(scale),distinct_branch_points=10,genus=4))
    # At a=1 the squarefree assertion must fail; this is not in the theorem's domain.
    bad=sp.Poly(G**2,t)
    require(sp.gcd(bad,bad.diff()).degree()>0,'colliding scale control')
    xi=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    sets=[{F(4*j+k)+c for k in (2,4) for c in xi} for j in range(3)]
    require(all(len(x)==10 and 0 not in x for x in sets),'ten-contact block distinctness')
    scales=[F(1),F(100),F(10000)]
    scaled=[{c/scales[j] for c in sets[j]} for j in range(3)]
    require(all(not scaled[i]&scaled[j] for i in range(3) for j in range(i)),'three disjoint ten-contact blocks')
    genera=[]
    for r in (2,3):
        degree=2**(r-1);branch_count=10*r
        twice_g_minus_two=-2*degree+branch_count*degree//2
        genus=(twice_g_minus_two+2)//2
        require(genus==(9 if r==2 else 27),'multiquadratic genus arithmetic')
        genera.append(dict(poles=r,cover_degree=degree,branch_points=branch_count,genus=genus))
    return dict(nonzero_contacts=[str(x) for x in sorted(nonzero)],collision_ratios=[str(x) for x in ratios],
                resultant=str(result),fixed_scale_examples=output,ten_contact_examples=genera,
                degeneracy_control_scale_one=True)


Point=Optional[tuple[F,F]]

def add(P: Point,Q: Point) -> Point:
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u and y==-v:return None
    m=(3*x*x-36)/(2*y) if P==Q else (v-y)/(u-x)
    xx=m*m-x-u
    return xx,m*(x-xx)-y


def mul(n:int,P:Point) -> Point:
    if n<0:
        return mul(-n,None if P is None else(P[0],-P[1]))
    out=None
    while n:
        if n&1:out=add(out,P)
        P=add(P,P);n//=2
    return out


def elliptic_group_examples() -> dict:
    P=(F(12),F(36));Q=mul(2,P)
    require(Q is not None and Q[0]==F(25,4),'nonintegral double of the sample point')
    count=0;identities=0
    for n,h in itertools.product(range(-4,5),repeat=2):
        H=mul(h,P);U=mul(h*n,P);V=mul((h-1)*n,P);A=mul(n,P)
        minusV=None if V is None else(V[0],-V[1])
        require(add(U,minusV)==A,'group-coordinate automorphism example')
        minusA=None if A is None else(A[0],-A[1])
        require(add(U,minusA)==V,'inverse group-coordinate example')
        for point in (H,U,V,A):
            if point is not None:require(point[1]**2==point[0]**3-36*point[0],'sample lies on curve')
            else:identities+=1
        count+=1
    return dict(curve='y^2=x^3-36*x',point=['12','36'],double_x='25/4',index_pairs=count,
                identity_occurrences=identities,scope='Finite consistency examples only; not a proof of density.')


def build() -> dict:
    inputs=json.loads((HERE/'inputs.json').read_text())
    for row in inputs['files']:
        p=ROOT/row['path'];raw=p.read_bytes()
        require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'], 'source mismatch: '+row['path'])
    return dict(schema='joint-pole-realization-verification/v29',status='PASS',
        symbolic_transfers=symbolic_transfers(),elliptic_scaling=elliptic_scaling(),
        rational_example=exact_example(),finite_algebra=finite_algebra(),
        contact_correspondences=contacts_and_genera(),elliptic_examples=elliptic_group_examples(),
        authenticated_sources=inputs['files'],
        global_variable_count_improvement=False,independent_mathematical_review=False,
        arithmetic_realization_proved_by_computation=False,
        scope='Exact transfer, scaling and finite-choice identities; explicit prepared witnesses; finite elliptic examples; contact branch counts and corruption controls. The infinite realization and finiteness inputs, density proofs and global completeness are not computationally certified.')


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    report=build();raw=(json.dumps(report,indent=2)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(raw)
    else:
        require(CERTIFICATE.read_bytes()==raw,'published certificate differs from exact reconstruction')
    print(json.dumps(dict(status='PASS',symbolic_identities=14,prepared_transfer_examples=len(report['rational_example']['prepared_transfers']),
        finite_algebra_examples=len(report['finite_algebra']['examples']),elliptic_group_examples=report['elliptic_examples']['index_pairs'],
        global_variable_count_improvement=False),indent=2))

if __name__=='__main__':
    main()
