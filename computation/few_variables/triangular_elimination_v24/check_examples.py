#!/usr/bin/env python3
"""Exact small-algebra checks, including nilpotent and nonreal fibers.
Requires SymPy. This implements actual multiplication matrices and does not
import the bound producer. The general theorem is proved in the paper.
"""
import itertools,json,math
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
U=sp.Symbol('U');z=sp.Symbol('z');q1,q2=sp.symbols('q1 q2')

def is_square(x):
    x=sp.Rational(x)
    return x>0 and math.isqrt(int(x.p))**2==x.p and math.isqrt(int(x.q))**2==x.q

def run_case(name,f,g,cs,factor_roots=True):
    p=1;s=len(cs);b=sp.degree(f,z);n=int(b*2**s);qs=(q1,q2)[:s];gens=(z,)+qs
    relations=[f]+[q*q-c for q,c in zip(qs,cs)]
    gb=sp.groebner(relations,*reversed(gens),order='lex',domain=sp.QQ)
    bb=sp.groebner([f],z,domain=sp.QQ)
    basis=[sp.prod(v**e for v,e in zip(gens,es))for es in itertools.product(range(b),*[range(2)]*s)]
    basis_exp=[es for es in itertools.product(range(b),*[range(2)]*s)]
    pos={es:i for i,es in enumerate(basis_exp)}
    def red(e):return gb.reduce(sp.expand(e))[1]
    def mat(e):
        M=sp.zeros(n)
        for j,m in enumerate(basis):
            pp=sp.Poly(red(e*m),*gens)
            for es,c in pp.terms():M[pos[es],j]=c
        return M
    def bmat(e):
        M=sp.zeros(b)
        for j in range(b):
            pp=sp.Poly(bb.reduce(sp.expand(e*z**j))[1],z)
            for (i,),c in pp.terms():M[i,j]=c
        return M
    T=g*g*sp.prod(cs);MT=bmat(T);aa=MT.charpoly().all_coeffs()
    r0=max((i for i,a in enumerate(aa)if a),default=0)
    Z=2+sum(a*a for a in sp.Poly(f,z).all_coeffs()[1:])
    S=b*(1+sum(a*a for c in cs for a in bmat(c)))
    delta=sp.discriminant(f,z);assert delta!=0
    k=(b*(b-1)-2)//2;D=delta**2;K=(2*Z)**k*(1+delta**2);C=D+4*Z*K
    J=4*S;Q=2*S*J**(s-1)
    Xi=sum(J**(s-j)*sp.prod(cs[:j-1])*qs[j-1] for j in range(1,s+1))
    Omega=Q*(C**2+D*C*z)+D**2*Xi
    expected=[]
    for zz in sp.polys.polytools.ground_roots(f,z):
        gg=g.subs(z,zz) if hasattr(g,'subs')else g
        cc=[sp.Rational(c.subs(z,zz) if hasattr(c,'subs')else c)for c in cs]
        if gg==0 or not all(is_square(c)for c in cc):continue
        for signs in itertools.product((-1,1),repeat=s):
            sub={z:zz};sub.update({q:sgn*sp.sqrt(c)for q,c,sgn in zip(qs,cc,signs)})
            # E_{r0} equals a_{r0} at every point where G != 0.
            val=sp.cancel(aa[r0]*Omega.subs(sub))
            assert val!=0 and val.is_Rational
            expected.append(1/val)
    assert len(expected)==len(set(expected))
    obtained=[]; rank_checks=[]
    for r in range(1,b+1):
        E=red(aa[r]-sum(aa[j]*T**(r-j)for j in range(r+1)))
        MM=mat(red(E*Omega));coeff=MM.charpoly().all_coeffs()
        H=sp.Poly(sum(coeff[j]*U**j for j in range(2**s*r+1)),U)
        tails=sum(a*a for a in aa[r+1:])
        if r>r0:
            assert MM==sp.zeros(n) and H.as_expr()==1
        if r==r0 and r0:
            assert all(c==0 for c in coeff[2**s*r+1:])
            assert H.degree()==2**s*r
            if factor_roots:
                obtained += list(sp.polys.polytools.ground_roots(H))
            else:
                # This test case has all active geometric characters rational.
                assert len(expected)==2**s*r
                exact=sp.Poly(sp.prod(1-U/root for root in expected),U)
                assert H==exact
                obtained+=expected
        if r<r0:assert tails>0
        rank_checks.append(dict(r=r,truncation_degree=2**s*r,actual_H_degree=H.degree(),tail_is_zero=(tails==0)))
    assert set(obtained)==set(expected)
    # Without E_r, the empty-guard example has spurious rational roots.
    rejected=None
    if g==0:
        bad=mat(Omega).charpoly().all_coeffs()
        badH=sp.Poly(sum(a*U**j for j,a in enumerate(bad)),U)
        rejected=bool(sp.polys.polytools.ground_roots(badH));assert rejected
    return dict(name=name,status='PASS',rank=n,nonzero_T_characters=int(r0),rational_characters=len(expected),cases=rank_checks,
                negative_control_omitting_E_rejected=rejected)

cases=[
 ('all rational, repeated T',z*z-1,sp.Integer(1),[sp.Integer(1),sp.Integer(4)],True),
 ('nonrational point roots',z*z-2,sp.Integer(1),[sp.Integer(1),sp.Integer(1)],True),
 ('nonreal point roots',z*z+1,sp.Integer(1),[sp.Integer(1),sp.Integer(1)],True),
 ('one excluded point component',z*z-1,z-1,[sp.Integer(1),sp.Integer(1)],True),
 ('inactive nilpotents; no rational character',z*z-1,sp.Integer(1),[z+1,sp.Integer(1)],True),
 ('inactive nilpotents; rational active component',z*z-1,sp.Integer(1),[2*(z+1),sp.Integer(1)],True),
 ('empty nonzero locus',z*z-1,sp.Integer(0),[sp.Integer(1),sp.Integer(1)],True),
 ('nonreal quadratic roots',z*z-1,sp.Integer(1),[sp.Integer(-1),sp.Integer(1)],True),
 ('correlated nonsquare radicands',z*z-1,z-1,[sp.Integer(2),sp.Integer(8)],True),
 ('vanishing intermediate characteristic coefficient',z*z-1,sp.Integer(1),[z,sp.Integer(1)],True),
 ('very small nonzero radicand',z*z-1,sp.Integer(1),[sp.Rational(1,10**12),sp.Integer(4)],True),
 ('quartic point algebra with an excluded root',z**4-5*z*z+4,z-1,[sp.Integer(1),sp.Integer(1)],False)
]
results=[]
for args in cases:
    result=run_case(*args);results.append(result);print(result['name'], 'PASS',flush=True)
# A second, genuinely multigenerator base algebra.  All character values
# are rational, so the complete expected determinant is known without
# factoring a large polynomial. This still constructs the matrices directly.
z1,z2,q3,q4=sp.symbols('z1 z2 q3 q4')
gens=(z1,z2,q3,q4);f1=z1*z1-1;f2=z2*z2-4
cc=[(z1+z2)**2,(z1-z2)**2];gg=z1-1
rels=[f1,f2,q3*q3-cc[0],q4*q4-cc[1]]
gb=sp.groebner(rels,*reversed(gens),order='lex',domain=sp.QQ)
bb=sp.groebner([f1,f2],z2,z1,order='lex',domain=sp.QQ)
exps=list(itertools.product(range(2),repeat=4))
bexps=list(itertools.product(range(2),repeat=2))
basis=[sp.prod(v**e for v,e in zip(gens,es))for es in exps]
bbasis=[z1**i*z2**j for i,j in bexps]
def matrix_for(e,base=False):
    bs,es,gs,G=(bbasis,bexps,(z1,z2),bb)if base else(basis,exps,gens,gb)
    pos={v:i for i,v in enumerate(es)};M=sp.zeros(len(bs))
    for j,m in enumerate(bs):
        pp=sp.Poly(G.reduce(sp.expand(e*m))[1],*gs)
        for ee,c in pp.terms(): M[pos[ee],j]=c
    return M
T=gg**2*sp.prod(cc);aa=matrix_for(T,True).charpoly().all_coeffs()
r0=max(i for i,c in enumerate(aa)if c)
Z=2+sum(c*c for f,zv in [(f1,z1),(f2,z2)]for c in sp.Poly(f,zv).all_coeffs()[1:])
S=4*(1+sum(c*c for a in cc for c in matrix_for(a,True)))
deltas=[sp.discriminant(f1,z1),sp.discriminant(f2,z2)]
D=sp.prod(d*d for d in deltas);K=sp.prod(1+d*d for d in deltas);C=D+4*Z*K
J=4*S;Q=2*S*J;Xi=J*q3+cc[0]*q4
Omega=Q*(C**3+D*C**2*z1+D**2*C*z2)+D**3*Xi
expected=[]
for a,b in itertools.product((-1,1),(-2,2)):
    if a==1:continue
    for c,d in itertools.product((-1,1),repeat=2):
        val=aa[r0]*Omega.subs({z1:a,z2:b,q3:c*abs(a+b),q4:d*abs(a-b)})
        assert val!=0 and val.is_Rational
        expected.append(1/val)
assert len(expected)==len(set(expected))==8
rank_checks=[]
for r in range(1,5):
    E=aa[r]-sum(aa[j]*T**(r-j)for j in range(r+1))
    M=matrix_for(E*Omega);coef=M.charpoly().all_coeffs()
    H=sp.Poly(sum(coef[j]*U**j for j in range(4*r+1)),U)
    if r<r0: assert sum(a*a for a in aa[r+1:])>0
    if r==r0:
        assert all(a==0 for a in coef[4*r+1:])
        assert H==sp.Poly(sp.prod(1-U/root for root in expected),U)
    if r>r0: assert M==sp.zeros(16) and H.as_expr()==1
    rank_checks.append(dict(r=r,truncation_degree=4*r,actual_H_degree=H.degree()))
results.append(dict(name='two point generators and dependent radicands',status='PASS',
    rank=16,nonzero_T_characters=r0,rational_characters=8,cases=rank_checks))
print(results[-1]['name'],'PASS',flush=True)
report=dict(status='PASS',sympy_version=sp.__version__,example_count=len(results),
            scope='Exact finite examples; the universal rational-projection theorem is supplied by the written proof, not by these examples.',examples=results)
(HERE/'exact-example-verification.json').write_text(json.dumps(report,indent=2)+'\n')
