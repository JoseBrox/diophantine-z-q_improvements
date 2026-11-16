#!/usr/bin/env python3
"""Exact certificates for the field-aligned scalar, using integers only.

This checks identities, coefficient divisibilities and selected local examples.
The all-valuation proofs and source-transfer scope are in the companion note.
It does not certify actual native prescribed-trace realization or 21/9.
"""
from fractions import Fraction as Q
from math import isqrt, gcd
from pathlib import Path
from hashlib import sha256
import argparse
import json

n0=116576341082536192
D0=5951086353
ell=76249
eta=102
aa=(5951086353,5960872849,17757117551,5845158349)
theta=(Q(0),Q(1),Q(2401),Q(-343,32))
a=17*ell
K0=12556178240


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def add(p,q):
    r=[0]*max(len(p),len(q))
    for i,x in enumerate(p):r[i]+=x
    for i,x in enumerate(q):r[i]+=x
    return trim(r)


def scale(p,c):return trim([c*x for x in p])


def mul(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):r[i+j]+=x*y
    return trim(r)


def evaluate(p,x):
    z=0
    for c in reversed(p):z=z*x+c
    return z


def compose(p,q):
    z=[0]
    for c in reversed(p):z=add(mul(z,q),[c])
    return z


def norm(p,q):return add(mul(p,p),scale(mul(q,q),-2))


def kmul(P,T):
    p,q=P;r,s=T
    return add(mul(p,r),scale(mul(q,s),2)),add(mul(p,s),mul(q,r))


def val(x,p):
    x=Q(x)
    if not x:raise ValueError('valuation of zero')
    z=abs(x.numerator);v=0
    while z%p==0:z//=p;v+=1
    z=x.denominator
    while z%p==0:z//=p;v-=1
    return v


def scalar(X,L):
    R=evaluate(rpoly,X)
    C=eta*eta*M0*(ell**((L+1)//2)+1)
    return Q(eta*eta*ell**L*M0*R)/(1+C*R)**2


assert n0==2**8*11*13*101*757*5939*7013
assert all(all(p%d for d in range(2,isqrt(p)+1))
           for p in (11,13,101,757,5939,7013))
assert all(D0*D0+n0*t==v*v for t,v in zip(theta,aa))
assert 357**2-2*160**2==ell
assert 5**2-2*2**2==17
assert all(ell%d for d in range(2,isqrt(ell)+1))

# Universal norm identity in the independent variable Z.
G=([8],[4])  # 4(2+sqrt2)
for c in aa:G=kmul(G,([c],[0,1]))
betaZ=[-D0*D0,0,2]
RZ=[1]
for factor in [betaZ,add(betaZ,[-n0]),add(betaZ,[-2401*n0]),
               add(scale(betaZ,32),[343*n0])]:
    RZ=mul(RZ,factor)
assert norm(*G)==RZ

beta=compose(betaZ,[K0,0,a])
assert beta==[279899795208436154591,0,65102930354279680,0,3360439980578]
rpoly=compose(RZ,[K0,0,a])
GX=(compose(G[0],[K0,0,a]),compose(G[1],[K0,0,a]))
assert norm(*GX)==rpoly
M0=rpoly[0]
assert M0==189711668070091549022366223774716198062888712249407876629023195358725017888
assert beta[0]-2401*n0==269266757599
assert len(beta)-1==4 and len(rpoly)-1==16
assert all(c%32==0 for c in rpoly)
assert rpoly[0]//32%8==1
assert all(c//32%8==0 for c in rpoly[1:])
assert val(M0,2)==5 and val(M0,3)==0 and val(M0,17)==0
assert [evaluate(rpoly,x)%3 for x in range(3)]==[1,1,1]
assert all(c%(17**2)==0 for c in rpoly[1:])
assert [K0%ell,beta[0]%ell,M0%ell,(1+eta**2*M0**2)%ell]==[26663,14480,68886,46270]
assert all(c%ell==0 for c in beta[1:])
assert [ell%8,ell%3,ell%17]==[1,1,4]

# Uniform coefficient inequalities, rather than only sample denominators.
# For v_p(X)=-e, the difference between quadratic and quartic valuations
# is v_p(A2)-v_p(A4)+2e, so it is enough to check e=1.
leading_factorization={2:1,17:2,ell:2}
assert beta[4]==2*17**2*ell**2
dominance_certificate=[]
for p,va in leading_factorization.items():
    vb=val(beta[2],p)
    assert val(beta[4],p)==va
    assert va-4<0 and vb-va+2>0
    dominance_certificate.append({'prime':p,'v_leading':va,'v_quadratic':vb,
        'leading_order':f'{va}-4e','minimum_quadratic_minus_leading':vb-va+2})
# At every other prime the leading coefficient is a unit, while the
# remaining coefficients are integral: -4e<-2e<=v_p(A2)-2e.

denominator_examples=[]
for p in [2,3,17,ell,11,13,101,757,5939,7013,5,7,19]:
    for e in [1,2]:
        x=Q(1,p**e)
        expected=(1 if p==2 else 2 if p in (17,ell) else 0)-4*e
        assert val(evaluate(beta,x),p)==expected<0
        denominator_examples.append([p,e,expected])

scalar_examples=[]
for L in [3,5]:
    for X in range(-5,6):
        rr=scalar(Q(X),L)
        assert 0<rr<Q(1,eta**2*ell*M0**2)
        assert [val(rr,p) for p in [2,3,17,ell]]==[12,2,2,L]
        assert isqrt(rr.denominator)**2==rr.denominator
        scalar_examples.append([X,L])
    for e in [1,2]:
        assert val(scalar(Q(1,ell**e),L),ell)==L-8+16*e

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--repo',type=Path)
args=parser.parse_args()
HERE=Path(__file__).resolve().parent
if args.repo:
    REPO=args.repo.resolve()
else:
    candidates=[]
    for ancestor in (HERE,*HERE.parents):
        candidates.extend((ancestor,ancestor/'research-repo'))
    REPO=next(p for p in candidates if
              (p/'papers/finite_algebra/unit_norm_20261114_v28.tex').is_file())
source_names=[
    'papers/finite_algebra/unit_norm_20261114_v28.tex',
    'papers/few_variables25/few_variables25_merged_20261110_v19.tex',
    'papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex',
    'papers/pole_parameters/norm_compatible_scalar_20261116_v47.tex',
    'papers/conditional_few_variables/conditional13_20261109_v16.tex',
    'papers/conditional_few_variables/direct_input13_20261110_v22.tex',
]
source_hashes={name:sha256((REPO/name).read_bytes()).hexdigest() for name in source_names}
assert 'a_1=1+\\rho T^2' in (REPO/source_names[0]).read_text()
assert 'h(\\beta)\\le H_1c^{7/9}' in (REPO/source_names[1]).read_text()
assert 'p_j\\equiv1\\pmod{8\\cdot3\\cdot17}' in (REPO/source_names[2]).read_text()

certificate={
    'schema':'aligned-detector-field-scalar/v52',
    'status':'passed',
    'scope':'Exact norm identity, input coefficients, uniform dominance inequalities, local divisibilities and selected valuation examples; full source transfer is proved in the accompanying manuscript.',
    'count':'Same 25 total coordinates under retained arithmetic premises; no inherited numeric degree bound or smaller count asserted.',
    'n0':str(n0),'D0':str(D0),'ell':ell,'eta':eta,'a':a,'K0':K0,
    'norm_field_d':2,
    'norm_constants':{'17':[5,2],'ell':[357,160]},
    'beta_coefficients_ascending':[str(c) for c in beta],
    'M0':str(M0),
    'Gamma_coefficients_in_Z':[[str(c) for c in p] for p in G],
    'R_coefficients_in_X':[str(c) for c in rpoly],
    'consumed_prime_residues':[26663,14480,68886,46270],
    'integer_scalar_valuations_at_2_3_17':[12,2,2],
    'uniform_denominator_dominance':dominance_certificate,
    'input_denominator_examples':denominator_examples,
    'integer_scalar_examples':scalar_examples,
    'source_sha256':source_hashes,
    'mathematical_arguments_not_replaced_by_computation':['full source transfer','conic Hasse principle'],
    'unresolved':['simultaneous actual prescribed-trace rational realization','21/9 bounds']
}
target=args.output or HERE/'certificate.json'
encoded=json.dumps(certificate,indent=2)+'\n'
if args.output:
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(encoded)
else:
    assert target.read_text()==encoded,'Committed certificate differs; regenerate with --output.'
print(json.dumps({'status':'passed','certificate':str(target),'input_degree':4,'contact_degree':16,
                  'denominator_examples':len(denominator_examples),'scalar_examples':len(scalar_examples)}))
