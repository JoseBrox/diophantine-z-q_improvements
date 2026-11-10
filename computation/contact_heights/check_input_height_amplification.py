#!/usr/bin/env python3
"""Exact identities for input heights and the four-contact counterexample.

Uses only the Python standard library. Infinitude is certified mathematically
by the displayed Nagell--Lutz witness, not by sampling many multiples.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json


def add(*polynomials):
    n=max(map(len,polynomials));out=[Q(0)]*n
    for p in polynomials:
        for i,c in enumerate(p):out[i]+=c
    while len(out)>1 and out[-1]==0:out.pop()
    return out


def scale(p,c):return [c*x for x in p]


def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return out


def power(p,n):
    out=[Q(1)]
    for _ in range(n):out=mul(out,p)
    return out


def evaluate(p,x):
    out=Q(0)
    for c in reversed(p):out=out*x+c
    return out


def doubled(point,a2,a4):
    x,y=point
    slope=(3*x*x+2*a2*x+a4)/(2*y)
    x2=slope*slope-a2-2*x
    y2=-y+slope*(x-x2)
    return slope,(x2,y2)


f=[Q(36000),Q(-2400),Q(10),Q(1)]
assert mul(mul([60,1],[-20,1]),[-30,1])==f
# F(60/X)=360*f(X)/X^4, while 10*(6Y/X^2)^2=360Y^2/X^4.
assert scale(mul(mul([60,1],[60,-2]),[60,-3]),60)==scale(f,360)
P=(Q(15),Q(75))
assert P[1]**2==evaluate(f,P[0])
slope,twoP=doubled(P,Q(10),Q(-2400))
assert slope==Q(-19,2) and twoP==(Q(201,4),Q(2079,8))
assert twoP[1]**2==evaluate(f,twoP[0])
t,y=Q(60)/P[0],6*P[1]/P[0]**2
assert (t,y)==(Q(4),Q(2))
assert 10*y*y==(t+1)*t*(t-2)*(t-3)

A,B=-197100,32130000
short=[Q(B),Q(A),Q(0),Q(1)]
assert mul(mul([510,1],[-210,1]),[-300,1])==short
short_transform=add(power([30,9],3),scale([30,9],A),[B])
assert short_transform==scale(f,729)
Pshort=(9*P[0]+30,27*P[1])
twoPshort=(9*twoP[0]+30,27*twoP[1])
assert Pshort==(Q(165),Q(2025))
assert twoPshort[0]==Q(1929,4) and twoPshort[0].denominator!=1
assert doubled(Pshort,Q(0),Q(A))[1]==twoPshort
discriminant=-16*(4*A**3+27*B**2)
assert discriminant!=0
assert isqrt(36000)**2!=36000
assert Q(2,5).numerator==2 and Q(2,5).denominator==5
theta=[-1,0,2,3]
differences=sorted({abs(x-y) for x in theta for y in theta if x!=y})
assert differences==[1,2,3,4]

table=[]
for degree,eps,input_power in [(8,Q(1,2),1),(6,Q(1,4),2),(5,Q(1,36),3)]:
    contact=1/(degree-4-2*eps)
    residual=Q(8,3)*contact
    absorption=residual/input_power
    assert absorption<1
    table.append({'contacts':degree,'epsilon':str(eps),'contact_height_coefficient':str(contact),
                  'input_power':input_power,'residual_coefficient':str(residual),
                  'absorption_coefficient':str(absorption),
                  'log_index_coefficient_after_absorption':str(residual/(1-absorption))})
assert [r['absorption_coefficient'] for r in table]==['8/9','8/9','16/17']
assert table[1]['log_index_coefficient_after_absorption']=='16'
assert table[2]['log_index_coefficient_after_absorption']=='48'
alpha=Q(4)/Q(16,15)-3
assert alpha==Q(3,4)
assert (alpha+1)/(4*alpha)==Q(7,12)
assert 1/(Q(16,15)*alpha)==Q(5,4)

report={
    'status':'PASS',
    'proof_scope':'Exact algebraic certificates. Uniform height inequalities and infinitude are established by the accompanying mathematical proofs.',
    'input_height_lemma':{
        'scale':'beta=gamma^r+B',
        'hypotheses':'integers r>=1 and B>=1; gamma>=1 or r even',
        'conclusion':'beta>=B and r*h(gamma)<=h(beta)',
        'reduced_numerator':'a^r+B*b^r',
        'reduced_denominator':'b^r',
        'coprimality_reason':'gcd(a,b)=1 implies gcd(a^r+B*b^r,b^r)=1',
        'verification':'Uniform conclusion established in Lemma 2.1 of the companion proof.'
    },
    'height_table':table,
    'four_contact_counterexample':{
        'contacts':theta,'twist_coefficient':10,'initial_quartic_point':['4','2'],
        'long_weierstrass_coefficients':[0,10,0,-2400,36000],
        'point':[str(x) for x in P],'double':[str(x) for x in twoP],
        'short_weierstrass_coefficients':[0,0,0,A,B],
        'short_discriminant':str(discriminant),
        'short_point':[str(x) for x in Pshort],
        'short_double':[str(x) for x in twoPshort],
        'nontorsion_certificate':'Integral short Weierstrass equation; doubled x-coordinate 1929/4 is not integral, contradicting Nagell--Lutz for torsion.',
        'contact_difference_values':differences,'bounded_odd_contact_prime_support':[2,3,5],
        'odd_contact_radical_outside_support':1,
        'identity_checks':['quartic-to-cubic substitution','factorization of both cubic models',
                           'integral short-model transformation','doubling in both models',
                           'quartic initial point','nonzero discriminant','excluded X_E=0 and t=1 values']
    },
    'references':{
        'Granville_Proposition_1':'https://dms.umontreal.ca/~andrew/PDF/hyperelliptics.pdf',
        'Alpoge_Theorem_1_1':'https://people.math.harvard.edu/~alpoge/papers/nagell-lutz,%20quickly.pdf',
        'Milne_II_5_1':'https://www.jmilne.org/math/Books/EC2.pdf'
    }
}
path=Path(__file__).with_name('input-height-amplification-certificate.json')
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
