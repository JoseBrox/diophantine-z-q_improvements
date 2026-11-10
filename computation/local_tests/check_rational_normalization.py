#!/usr/bin/env python3
"""Exact finite arithmetic supporting the rational-normalization lemmas.

The unrestricted valuation statements are proved in the companion paper.
This checker verifies rational examples, every sign/cancellation branch in
the stated finite ranges, the linear precision inequalities, and the fixed
contact arithmetic. It does not certify a defining-polynomial theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def vp(x, p):
    x=F(x)
    if not x:
        return None
    n,d=x.numerator,x.denominator
    v=0
    while n%p==0:n//=p;v+=1
    while d%p==0:d//=p;v-=1
    return v


def pfactors(n):
    n=abs(n); out=[]; p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out


def run():
    count=0; cancellation_count=0
    for p in (3,5,7,11,13):
        for nu in range(-7,8):
            for unit in (1,2,-1,-2):
                if unit%p==0:continue
                z=unit*F(p)**nu
                for d in range(-9,10):
                    for du in range(1,p):
                        D=du*F(p)**d; denominator=1+z*D*D
                        if not denominator:
                            assert nu%2==0
                            continue
                        got=vp(z*D*D/denominator,p)
                        upper=max(0,nu+2*d)
                        assert got<=upper
                        if nu+2*d!=0:assert got==upper
                        else:cancellation_count+=int(got<0)
                        if nu%2:assert got==upper and got>=0
                        if nu==0:
                            assert (got>0)==(d>0)
                            if d>0:assert got==2*d
                        count+=1
    m=100;K=206
    assert F(K)-2*m-F(9,2)==F(3,2)>0
    precision_cases=0
    for mu in range(-400,401,2):
        for nu in range(1,402,2):
            rho=mu+nu
            assert rho%2 and rho!=0
            if rho<0:continue
            threshold=(F(K)-F(7,4))*rho
            if 0<=mu<=nu:
                bad_upper=(K+1)*mu+2*m*nu
                assert threshold>bad_upper
            elif mu>nu:
                bad_upper=(K+1)*nu+2*m*mu
                assert threshold>bad_upper
            else:
                bound=((F(K)-F(7,4))*nu-F(11,4)*mu)/2
                assert bound>m*nu
            precision_cases+=1
    base=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    contacts=[[x+j for j in shifts for x in base] for shifts in ((2,4),(6,8))]
    poles=[F(-1),F(-2)]
    values=contacts[0]+[poles[0]]+contacts[1]+[poles[1]]
    assert len(values)==len(set(values))==22 and all(values)
    primes=set()
    for i,x in enumerate(values):
        primes.update(pfactors(x.numerator));primes.update(pfactors(x.denominator))
        for y in values[:i]:
            diff=x-y
            primes.update(pfactors(diff.numerator));primes.update(pfactors(diff.denominator))
    ell=76249
    residues=[x.numerator*pow(x.denominator,-1,ell)%ell for x in values]
    assert 0 not in residues and len(set(residues))==22 and ell not in primes
    def contact_value(i,t):
        value=F(1)
        for theta in contacts[i]:value*=t-theta
        return value/(t-poles[i])**10
    unit_cases=0
    for p in (101,103,107,127):
        if p in primes:continue
        for mu in (-3,-1,1,3):
            for ru in (1,-1,2):
                r=ru*F(p)**mu
                for td in (-3,-1,0,1,3):
                    T=F(p)**td;a=(1+r*T*T)**2
                    for lam in [F(p)**j for j in (-3,-1,0,1,3)]+[c+F(p) for c in values]:
                        ts=[lam,a*lam]
                        if any(ts[i]==poles[i] or ts[i] in contacts[i] for i in range(2)):continue
                        vals=[vp(contact_value(i,ts[i]),p) for i in range(2)]
                        assert 0 in vals
                        unit_cases+=1
    return {
        'status':'passed',
        'rational_normalization_cases':count,
        'nontrivial_equal_valuation_cancellations':cancellation_count,
        'even_coefficient_precision_cases':precision_cases,
        'two_contact_unit_cases':unit_cases,
        'precision':m,'switch_exponent':K,'norm_denominator_exponent':K-1,
        'linear_inequality_margin':'3/2',
        'contacts':[[str(x) for x in xs] for xs in contacts],
        'poles':[str(x) for x in poles],
        'exceptional_contact_primes':sorted(primes),
        'extra_contact_primes_above_76176':[p for p in sorted(primes) if p>76176],
        'forced_prime':ell,'forced_prime_contact_residues':residues,
        'scope':'Exact finite checks supporting separately proved local lemmas; no defining-polynomial variable reduction is certified by this program.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();result=run()
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
