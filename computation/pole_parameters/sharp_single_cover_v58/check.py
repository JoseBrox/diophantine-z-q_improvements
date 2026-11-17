#!/usr/bin/env python3
"""Exact certificates for the signed one-square height inequality.

This verifies denominator normalization, gcd/radical bounds, and the
algebraic implication of abc on exact fixtures. It does not verify abc.
"""
from fractions import Fraction as Q
from math import gcd, lcm
from pathlib import Path
import argparse
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output', type=Path, default=Path(__file__).with_name('certificate.json'))
output_path = _parser.parse_args().output
output_path.parent.mkdir(parents=True, exist_ok=True)
import json
import random
import sympy as sp

def rad(n):
    n=abs(n)
    assert n>0
    return sp.prod(sp.factorint(n).keys()) if n>1 else 1

def height_base(q):
    return max(abs(q.numerator),q.denominator)

def normalized(x,y,d,sign):
    u=x**d+sign*y*y
    if u==0:
        return None
    A,D=x.numerator,x.denominator
    B,E=y.numerator,y.denominator
    C,F=u.numerator,u.denominator
    if not A or not B:
        return {'zero_case':True,'x':x,'y':y,'u':u}
    m=d//2
    ell=lcm(D**m,E)
    M,N=ell//(D**m),ell//E
    X,Y=A**d*M*M,B*B*N*N
    assert (ell*ell)%F==0
    Z=abs(C)*(ell*ell//F)
    assert X+sign*Y==C*(ell*ell//F)
    G=gcd(abs(A)**m*M,abs(B)*N)
    g=G*G
    assert g==gcd(X,Y)
    assert gcd(g,ell)==1
    assert C%g==0 and B%G==0
    assert F%(M*M)==0
    assert rad(ell)<=D*rad(M)
    terms=[X//g,Y//g,Z//g]
    assert gcd(terms[0],terms[1])==1
    assert gcd(terms[0],terms[2])==1
    assert gcd(terms[1],terms[2])==1
    assert max(terms)==sum(terms)-max(terms)
    Rbound=abs(A)*(abs(B)//G)*(abs(C)//g)*int(rad(ell))
    # The support bound may be verified without factoring the large C:
    # the three primitive terms have prime support in the displayed factors.
    assert gcd(G,N)==1
    assert (abs(B)//G)*N == abs(B*N)//G
    assert (abs(C)//g)*(ell*ell//F)==Z//g
    return {'zero_case':False,'x':x,'y':y,'u':u,'A':A,'D':D,'B':B,'E':E,
            'C':C,'F':F,'ell':ell,'M':M,'N':N,'G':G,'g':g,'T':max(X,Y,Z),
            'Rbound':Rbound,'primitive_terms':terms}

def check_implication(data,d,kappa):
    eps=Q(d)-kappa*Q(d//2+2)
    assert eps>0
    coefficient=(2*kappa-1)/eps
    if data['zero_case']:
        if data['x']==0:
            assert height_base(data['x'])==1
        else:
            assert data['y']==0
            assert height_base(data['u'])==height_base(data['x'])**d
            assert coefficient>=Q(1,d)
        return
    p,q=kappa.numerator,kappa.denominator
    ep=d*q-p*(d//2+2)
    # K0=(T/g)/Rbound^kappa is no larger than the abc constant needed
    # for the actual primitive triple. This exact inequality therefore
    # checks a stronger fixture-level implication than substituting its
    # exact radical into abc.
    left=height_base(data['x'])**ep * data['Rbound']**p
    right=(data['T']//data['g'])**q * height_base(data['u'])**(2*p-q)
    assert left<=right, (data,d,kappa)

dv,kv=sp.symbols('d kappa',positive=True)
epsv=dv-kv*(dv/2+2)
Qv=(2*kv-1)/epsv
assert sp.simplify(Qv-(4*kv-2)/((2-kv)*dv-4*kv))==0
assert sp.simplify(kv-(kv+epsv)/dv-(3*kv/2-1+kv/dv))==0
assert sp.simplify(kv-1+(kv+epsv)/dv-(kv/2-kv/dv))==0
old=((4+kv)*dv-6*kv)/((2-kv)*dv-4*kv)
assert sp.simplify(old-Qv-(((4+kv)*dv-10*kv+2)/((2-kv)*dv-4*kv)))==0
assert sp.limit((dv/2)*Qv,dv,sp.oo)==(2*kv-1)/(2-kv)

rng=random.Random(580917)
parameters={6:[Q(101,100),Q(16,15)],8:[Q(101,100),Q(16,15),Q(121,100)],
            10:[Q(101,100),Q(121,100)],14:[Q(101,100),Q(121,100)]}
summary=[]
total=0
special=[]
for d,kappas in parameters.items():
    fixtures=set()
    for _ in range(260):
        fixtures.add((Q(rng.randint(-19,19),rng.randint(1,15)),
                      Q(rng.randint(-23,23),rng.randint(1,17))))
    for A in [-11,-5,-2,-1,1,2,5,11]:
        for D in [1,3,7,12]:
            x=Q(A,D)
            for eta in [Q(1),Q(-1),Q(1,13),Q(-2,17)]:
                fixtures.add((x,x**(d//2)+eta))
    # Nontrivial square gcd, denominator crossing and cancellation.
    fixtures.update([(Q(6,5),Q(6**(d//2),7)),
                     (Q(5,6),Q(7,2**(d//2+2)*3)),
                     (Q(5,3),Q(5**(d//2)-1,3**(d//2))),
                     (Q(0),Q(3,7)),(Q(5,7),Q(0))])
    signs={1:0,-1:0}
    zero_terms=0
    negative_u=0
    nontrivial_gcd=0
    denominator_cancellation=0
    for x,y in sorted(fixtures):
        for sign in [1,-1]:
            data=normalized(x,y,d,sign)
            if data is None:
                continue
            signs[sign]+=1
            total+=1
            for kappa in kappas:
                check_implication(data,d,kappa)
            if data['zero_case']:
                zero_terms+=1
            else:
                negative_u+=data['u']<0
                nontrivial_gcd+=data['g']>1
                denominator_cancellation+=data['F']<data['ell']**2
                if x==Q(6,5) and y==Q(6**(d//2),7) and sign==-1:
                    special.append({k:str(data[k]) for k in
                        ['x','y','u','D','E','F','ell','M','N','G','g','Rbound']})
    summary.append({'d':d,'fixtures':sum(signs.values()),'plus':signs[1],
                    'minus':signs[-1],'zero_term_cases':zero_terms,
                    'negative_u':negative_u,'nontrivial_square_gcd':nontrivial_gcd,
                    'denominator_cancellation':denominator_cancellation,
                    'coefficients':[{'kappa':str(k),'epsilon':str(Q(d)-k*(d//2+2)),
                        'Q':str((2*k-1)/(Q(d)-k*(d//2+2))),
                        'powered_Q':str(Q(d,2)*(2*k-1)/(Q(d)-k*(d//2+2)))} for k in kappas]})

certificate={'status':'PASS','total_exact_fixtures':total,
             'scope':'Checks algebra and exact abc-implication inequalities; does not establish abc or prime-pattern realization.',
             'formula':'Q_(kappa,d)=(2*kappa-1)/(d-kappa*(d/2+2))',
             'additive_constant':'log(K_kappa)/(d-kappa*(d/2+2))',
             'summary':summary,'nontrivial_gcd_examples':special}
output_path.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps({k:v for k,v in certificate.items() if k!='nontrivial_gcd_examples'},indent=2))
