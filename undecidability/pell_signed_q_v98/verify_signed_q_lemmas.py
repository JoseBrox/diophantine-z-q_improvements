#!/usr/bin/env python3
"""Independent exact lemma checks for signed-q recovery and margin absorption.

No table builder is imported. Finite fixtures are not asserted to satisfy the
complete source; universal arithmetic assertions are proved in the manuscript.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import argparse
import json
import sympy as sp


def pell_y(a,n):
    previous,current=0,1
    if n==0:return 0
    for _ in range(1,n):
        previous,current=current,2*a*current-previous
    return current


def verify():
    n,t,k,e,C=sp.symbols('n t k e C')
    M=n*n
    assert sp.expand((2*t+2)*(M-n)-t*(M-1)-(t*(n-1)**2+2*(M-n)))==0
    assert sp.expand((k-2*e)*(k+2*e)-(k*k-4*e*e))==0
    assert sp.expand((2*(k*k-4*e*e)-2)-2*C*C-(2*(k*k-4*e*e-C*C)-2))==0
    # Exact endpoints; the written proof supplies the indicated monotonicity.
    assert 2**4-2>=7*2
    assert F(15,32)*2**5-F(2,2**3)>14
    assert F(1,2)+F(1,4*2**5)<1
    assert F(6*4+1,32)+1<=4-2 and F(26,32)>0
    assert 2**374>50
    assert 5**60<2**140<2**640

    prefix_checks=0
    signed_congruence_checks=0
    for b in range(2,101):
        for Q in (b**5-2,b**5-1,b**5,b**5+1,2*b**5,b**6):
            assert Q>=b**5-2>=b**4 and Q>=2
            c0_upper=1+(b-1)*b**5+F(Q,b**3)
            assert c0_upper<b*Q
            lam=F(Q**4-1,b**5-1)
            assert lam>F(Q**4,2*b**5)>0
            assert 1+(b**5-2)*lam<Q**4
            S_lower=F(15,32)*Q**12-F(Q**5+Q**7,b**3)
            T_upper=Q**7+Q**6+F(Q**2,b**2)
            assert S_lower>14*Q**7 and T_upper<2*Q**7
            prefix_checks+=1
            for K in (b**3,b**5):
                for sign in (-1,1):
                    q=sign*Q
                    assert 0<abs(q*K+1)<=Q*K+1
                    assert abs(q-K)<=Q+K<=Q*K+1
                    signed_congruence_checks+=1

    margin_checks=0
    signed_guard_checks=0
    for kv in range(1,129):
        for ev in range(-(kv-1)//2,(kv-1)//2+1):
            eta=kv*kv-4*ev*ev
            if eta<=0:continue
            assert kv-2*abs(ev)>=1
            assert eta==(kv-2*abs(ev))*(kv+2*abs(ev))>=kv
            cv=isqrt(kv-1)
            assert cv*cv<kv<=eta and eta-cv*cv>0
            margin_checks+=1
            for ks in (-1,1):
                for y in (-16,16):
                    old_c=ks*kv*y+ev
                    assert abs(old_c)>kv and cv*cv<kv*kv<old_c*old_c
                    signed_guard_checks+=1

    pell_completeness_checks=0
    for a in range(2,21):
        for ell in range(3,9):
            p=4*a*a+1
            r=ell+1
            cc=pell_y(a,ell)
            kk=pell_y(p,r+1)
            assert cc*cc<(2*a)**(2*ell-2)<p**(ell-1)<p**r<kk
            pell_completeness_checks+=1

    return {
        'status':'PASS',
        'proof':'undecidability/pell_signed_q_v98/signed_q_and_absorbed_bound.tex',
        'absorbed_bound_proof':'undecidability/pell_signed_q_v98/bound_absorption.tex',
        'instance_tail':'x>32*z',
        'symbolic_identities':['Signed prefix lower-bound identity',
                               'Integral eta factorization',
                               'Strengthened positivity-row monomial'],
        'prefix_bound_fixtures':prefix_checks,
        'signed_integer_congruence_bound_fixtures':signed_congruence_checks,
        'integral_margin_fixtures':margin_checks,
        'signed_guard_reconstruction_fixtures':signed_guard_checks,
        'pell_completeness_bound_fixtures':pell_completeness_checks,
        'changes_checked':['Delete the private q>b^5 positivity wrapper',
                           'Absorb C_star^2<c^2 into eta-C_star^2>0'],
        'independent_of_table_builders':True,
        'fixture_scope':'Exact identities and inequalities, not complete source solutions',
        'not_machine_verified':['Universal source equivalence',
                                'The complete coefficient transformation and its extra abc fourth-power reuse',
                                'Jones coding theorem','Retained integer-interface arithmetic premises'],
        'unconditional_undecidability_claim':False,
        'variable_count_claim':None,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    out=verify()
    path=Path(__file__).with_name('signed_q_lemmas_certificate.json')
    if args.write:path.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    else:assert json.loads(path.read_text())==out
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
