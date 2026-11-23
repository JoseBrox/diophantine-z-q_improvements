#!/usr/bin/env python3
"""Independent exact algebra checks for the v97 Pell power-replacement proof.

This checker imports no source/table builder. Finite fixtures verify only the
stated identities and sign congruences, not source completeness or hypotheses.
"""
from fractions import Fraction
from math import gcd
from pathlib import Path
import argparse
import json
import sympy as sp


def pell(parameter, index):
    x,y=1,0
    for _ in range(index):
        x,y=parameter*x+(parameter*parameter-1)*y,x+parameter*y
    return x,y


def verify():
    b,s,A,X,Y=sp.symbols('b s A X Y')
    tb=b**5-1
    a0=(b**9+8*b**5+b-8)/2
    parameter=a0+5*tb*s
    modulus=2*b*parameter-b*b-1
    assert sp.expand(modulus-tb*(b**5+8*b+1+10*b*s))==0
    # These finite residue checks cover all integers because the tested
    # expressions are integer polynomials reduced modulo the displayed modulus.
    numerator=2*a0
    assert all(int(numerator.subs(b,j))%2==0 for j in range(2))
    assert all(int(numerator.subs(b,j))%5==2 for j in range(5))
    assert sp.expand(2*parameter-(b**4*b**5+8*b**5+b-8+10*(b**5-1)*s))==0
    parameter_checks=0
    negative_parameters=0
    for bv in range(2,257):
        a0v=Fraction(bv**9+8*bv**5+bv-8,2)
        assert a0v.denominator==1 and a0v%5==1
        assert 0<a0v<bv**16
        assert 0<(bv-1)**2<bv**5-1
        for sv in (-10000,-3,-1,0,1,5):
            av=int(a0v+5*(bv**5-1)*sv)
            mv=2*bv*av-bv*bv-1
            assert av%5==1 and abs(av)>=2 and mv!=0
            assert mv%(bv**5-1)==0 and gcd(bv,mv)==1
            parameter_checks+=1
            negative_parameters+=av<0
    assert negative_parameters>0

    # Universal one-step Pell polynomial identities.
    m=2*b*A-b*b-1
    rm=X-(A-b)*Y
    rp=X+(A-b)*Y
    xn=A*X+(A*A-1)*Y
    yn=X+A*Y
    assert sp.expand((xn-(A-b)*yn)-(b*rm+m*Y))==0
    assert sp.expand(rm*rp-(1+m*Y*Y)-(X*X-(A*A-1)*Y*Y-1))==0
    assert sp.expand(xn*xn-(A*A-1)*yn*yn-(X*X-(A*A-1)*Y*Y))==0

    signed_checks=0
    zero_index_checks=0
    negative_parameter_signed_checks=0
    for bv in range(2,10):
        for sv in (-10000,-3,-1,0,1,5):
            av=int(Fraction(bv**9+8*bv**5+bv-8,2)+5*(bv**5-1)*sv)
            mv=2*bv*av-bv*bv-1
            mod=abs(mv)
            tv=bv**5-1
            for index in (0,1,2,5,10,15):
                xv,yv=pell(av,index)
                assert xv*xv-(av*av-1)*yv*yv==1
                assert (yv-index)%5==0
                assert (xv-(av-bv)*yv-pow(bv,index,mod))%mod==0
                assert (xv+(av-bv)*yv-pow(pow(bv,-1,mod),index,mod))%mod==0
                for ds in (-1,1):
                    for cs in (-1,1):
                        for alpha in (-2,0,3):
                            q=ds*xv-(av-bv)*cs*yv-alpha*mv
                            exponent_sign=1 if ds==cs else -1
                            expected=ds*pow(bv,exponent_sign*index,mod)
                            assert (q-expected)%mod==0
                            if index%5==0:
                                assert q%tv in (1,tv-1)
                            signed_checks+=1
                            zero_index_checks+=index==0
                            negative_parameter_signed_checks+=av<0
    assert zero_index_checks>0 and negative_parameter_signed_checks>0

    # Exact endpoints for monotone inequalities used by the written proof.
    exponent=5**60
    assert 2**139<exponent<2**140<2**160
    assert Fraction(7*4,16)>1
    assert Fraction(6*4+1,32)+1<=4-2
    assert Fraction(26,32)>0
    assert 4**3>7*3+2
    assert 3*7*3+6-7>0  # induction margin for 4^r>7r+2, r>=3
    # n^2-n-1>=1 for n>=2, with positive derivative thereafter.
    assert 2**2-2-1>=1 and 2*2-1>0

    return {
        'status':'PASS',
        'fixed_exponent':str(exponent),
        'instance_tail':'x>32*z',
        'parameter_formula':'A=(b^9+8*b^5+b-8)/2+5*(b^5-1)*s',
        'exact_factorization':'2*b*A-b^2-1=(b^5-1)*(b^5+8*b+1+10*b*s)',
        'modular_parity_checks':'All residue classes modulo2 and modulo5',
        'parameter_fixture_checks':parameter_checks,
        'negative_parameter_fixtures':negative_parameters,
        'signed_pell_fixture_checks':signed_checks,
        'zero_index_fixture_checks':zero_index_checks,
        'negative_parameter_signed_fixture_checks':negative_parameter_signed_checks,
        'symbolic_identities':['Parameter factorization','Quadratic A assignment',
                               'Pell norm preservation','R recurrence','R-minus/R-plus product'],
        'new_integer_inputs':['power_delta','power_alpha'],
        'strict_integer_inequalities':['q>b^5','C_star^2<c^2'],
        'proof':'undecidability/pell_power_v97/pell_power_replacement.tex',
        'independent_of_table_builders':True,
        'not_machine_verified':['Infinite source equivalence and growth proof',
                                'Jones coding theorem',
                                'Arithmetic premises of the integer interfaces',
                                'Complete coefficient-table transformation'],
        'fixture_scope':'Signed recurrence and congruence identities, not full source solutions',
        'source_equivalence_proved_in_manuscript':True,
        'unconditional_undecidability_claim':False,
        'variable_count_claim':None,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=verify()
    path=Path(__file__).with_name('power_lemmas_certificate.json')
    if args.write:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(path.read_text())==result
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
