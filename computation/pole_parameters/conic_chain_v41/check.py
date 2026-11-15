#!/usr/bin/env python3
"""Reconstruct exact identities and local data for conic-chain obstructions."""
import argparse
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent
CERTIFICATE=HERE/'certificate.json'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def residue(x, ell):
    x=Fraction(x)
    return x.numerator*pow(x.denominator,-1,ell)%ell


def v(x, ell):
    x=Fraction(x)
    require(x!=0, 'valuation requested at zero')
    a,b=abs(x.numerator),x.denominator
    value=0
    while a%ell==0:
        a//=ell;value+=1
    while b%ell==0:
        b//=ell;value-=1
    return value


def rational_square(x):
    x=Fraction(x)
    return x>=0 and isqrt(x.numerator)**2==x.numerator and isqrt(x.denominator)**2==x.denominator


def prepared(x):
    x=Fraction(x)
    require(0<x<1, 'positive prepared range')
    require(isqrt(x.denominator)**2==x.denominator, 'reduced denominator square')
    require(v(x,2)==4, '2-adic valuation four')
    require(residue(x/16,8)==1, 'odd 2-adic unit congruent one modulo eight')
    return {'numerator':x.numerator,'denominator':x.denominator,'valuation_2':4,'unit_mod_8':1}


def crt_numerator(modulus, target):
    # Find M=1 mod8 with16M=target modulo an odd prime power.
    for j in range(modulus):
        M=1+8*j
        if (16*M)%modulus==target:
            return M
    raise AssertionError('CRT failed')


def odd_nonresidue(ell):
    return next(a for a in range(1,ell) if pow(a,(ell-1)//2,ell)==ell-1)


def pole_example(ell, min_k=1):
    beta=odd_nonresidue(ell)
    M=crt_numerator(ell,beta)
    k=min_k
    while Fraction(16*M,ell**(2*k))>=1:
        k+=1
    x=Fraction(16*M,ell**(2*k))
    record=prepared(x)
    record.update(prime=ell,valuation=-2*k,unit_residue=16*M%ell,k=k)
    require(pow(record['unit_residue'],(ell-1)//2,ell)==ell-1,'pole unit nonsquare')
    return record


def unit_example(ell, c):
    target=pow(residue(c+1,ell),-1,ell)
    M=crt_numerator(ell,target)
    q=1+8*ell*M
    x=Fraction(16*M,q*q)
    record=prepared(x)
    record.update(prime=ell,valuation=0,residue=residue(x,ell),q=q)
    require(record['residue']==target,'unit residue')
    return record


def nonresidue_prime(x):
    x=Fraction(x)
    return next(int(ell) for ell in S.primerange(3,1000)
                if x.numerator%ell and x.denominator%ell
                and pow(residue(x,int(ell)),(int(ell)-1)//2,int(ell))==int(ell)-1)


def norm_example(ell,c):
    modulus=ell*ell
    target=pow(residue(c,modulus),-1,modulus)*(1+ell)%modulus
    M=crt_numerator(modulus,target)
    q=1+8*modulus*M
    x=Fraction(16*M,q*q)
    record=prepared(x)
    require(v(x,ell)==0,'nonsquare unit input')
    require(pow(residue(x,ell),(ell-1)//2,ell)==ell-1,'nonsquare input residue')
    require(v(c*x-1,ell)==1,'odd valuation of cb-1')
    record.update(prime=ell,valuation=0,residue=residue(x,ell),q=q,
                  residue_mod_prime_squared=residue(x,modulus),valuation_cb_minus_one=1)
    return record


def classify_sample(c):
    c=Fraction(c)
    if c==0:
        rec=prepared(Fraction(272,841))
        rec.update(prime=29,valuation=-2,unit_residue=11)
        return {'coefficient':str(c),'case':'four-coordinate even pole','input':rec}
    if not rational_square(c):
        ell=nonresidue_prime(c)
        return {'coefficient':str(c),'case':'nonsquare c, odd valuation of cb-1','input':norm_example(ell,c)}
    if not rational_square(c+1):
        ell=nonresidue_prime(c+1)
        return {'coefficient':str(c),'case':'nonsquare c+1 unit','input':unit_example(ell,c)}
    odd_primes=[int(ell) for ell in S.factorint((c+1).numerator) if ell!=2]
    require(bool(odd_primes),'odd prime factor of Pythagorean hypotenuse')
    ell=min(odd_primes)
    require(residue(c,ell)==ell-1,'c=-1 residue')
    return {'coefficient':str(c),'case':'c and c+1 squares, c=-1 modulo ell','input':pole_example(ell)}


def build():
    b,e,p,z,w,eta,s,c,P,D=S.symbols('b e p z w eta s c P D')
    f1=e**2+b*p**2-1
    f2=z**2+b*p**2-b
    X=b**2*p**2;Y=b**2*p*e*z
    require(S.expand(X-b+b*e**2-b*f1)==0,'first elliptic factor')
    require(S.expand(X-b*b+b*z**2-b*f2)==0,'second elliptic factor')
    elliptic=S.expand(Y**2-X*(X-b)*(X-b*b))
    identity=b**4*p**2*(e**2*f2+z**2*f1-f1*f2)
    require(S.expand(elliptic-identity)==0,'elliptic polynomial identity')
    require(S.expand((eta*s)**2-b*(1-p*p)-b*(p*p+w*s*s-1)-(eta**2-b*w)*s*s)==0,
            'detector conic substitution')
    require(S.expand((D-1-(c*b-1)*P)-(D-1-c+c*e**2+P)+c*(e**2+b*P-1))==0,
            'alternative quadratic D equation')
    require(pow(11,14,29)==28 and pow(17,14,29)==28 and pow(28,14,29)==1,
            'four-coordinate obstruction residues')
    require(pow(2,2,5)==4,'five-coordinate obstruction residue')
    square29=sorted({x*x%29 for x in range(1,29)})
    require(11 not in square29 and 18 not in square29,'both signed unit residues nonsquare')
    families=[]
    for name,numerator,denom_prime,obstruction_prime in [
        ('four-coordinate',272,29,29),('five-coordinate c=1',528,31,5)]:
        samples=[]
        for n in [1,2,3,8,16]:
            bn=Fraction(numerator,denom_prime**(2*n))
            rec=prepared(bn);rec['n']=n
            if obstruction_prime==29:
                require(v(bn,29)==-2*n,'29-adic pole valuation')
                rec.update(valuation_29=-2*n,unit_residue_29=11)
            else:
                require(residue(bn,5)==3,'five-adic residue one half')
                rec.update(valuation_5=0,residue_5=3)
            samples.append(rec)
        families.append({'name':name,'numerator':numerator,'denominator':str(denom_prime)+'^(2n)',
                         'n_min':1,'obstruction_prime':obstruction_prime,'samples':samples})
    # The integral reductions in the unit and c=-1 cases have no points.
    reductions=[]
    for ell,c0,beta,kind in [(5,1,3,'unit b'),(3,2,2,'scaled even pole'),(5,4,2,'scaled even pole')]:
        squares={x*x%ell for x in range(ell)}
        integral_solutions=[]
        for p0 in range(ell):
            e2=(1-beta*p0*p0)%ell
            if kind=='unit b':
                z2=beta*(1+(c0*beta-1)*p0*p0)%ell
            else:
                z2=beta*(1+c0*beta*p0*p0)%ell
            if e2 in squares and z2 in squares:integral_solutions.append(p0)
        require(not integral_solutions,'no integral residue solutions')
        reductions.append({'prime':ell,'c_residue':c0,'b_unit_residue':beta,'kind':kind,'integral_p_residues':[]})
    coefficients=[Fraction(0),Fraction(-1),Fraction(1),Fraction(3),Fraction(8),Fraction(15),
                  Fraction(63),Fraction(-3,4),Fraction(9,16),Fraction(-7,8),Fraction(1,2),Fraction(5,4),Fraction(-9,25)]
    examples=[classify_sample(c0) for c0 in coefficients]
    rational_counter=prepared(Fraction(272,441))
    rc=Fraction(-9,25);rb=Fraction(272,441);rd=rc*rb-1
    require(rd==Fraction(-1497,1225),'rational coefficient residual')
    require(v(rb,3)==-2 and residue(rb*9,3)==2 and v(rd,3)==1,
            'rational coefficient obstruction at three')
    rational_counter.update(coefficient=str(rc),prime=3,valuation_b=-2,unit_residue_b=2,
                            cb_minus_one=str(rd),valuation_cb_minus_one=1)
    return {'format':'conic-chain-obstruction/v41','symbolic_identities':5,
            'four_coordinate_predicate':{'auxiliaries':4,'quadrics':3},
            'fixed_coefficient_family':{'auxiliaries':5,'quadrics':4,'coefficient_domain':'Q',
                'negative_odd_pole_implication':'At odd primes where c is integral; all odd primes for c in Z[1/2].',
                'theorem':'Every fixed coefficient has a local obstruction on arbitrarily small prepared inputs.'},
            'explicit_families':families,'nonzero_squares_mod_29':square29,
            'finite_residue_checks':reductions,'coefficient_examples':examples,'rational_coefficient_counterexample':rational_counter,
            'global_variable_count_improvement':False,
            'scope':'Exact polynomial identities and arithmetic certificates. The accompanying proofs establish the infinite local and coefficient statements; finite examples are not their proof. No lower bound for arbitrary pole systems or quartics is claimed.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=build();raw=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(raw)
    else:
        require(CERTIFICATE.read_text()==raw,'published certificate differs from exact reconstruction')
    print(json.dumps({'status':'PASS','symbolic_identities':report['symbolic_identities'],
                      'explicit_counterexample_families':2,'coefficient_examples':len(report['coefficient_examples']),
                      'global_variable_count_improvement':False},indent=2))


if __name__=='__main__':main()
