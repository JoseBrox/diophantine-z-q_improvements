#!/usr/bin/env python3
"""Exact finite arithmetic for the correction-free scalar normalization.

Uses only the Python standard library.  The proof of completeness and the
number-field scope are in scalar_normalization.tex; this checks all finite
residue tables, constants, polynomial coefficients, and an obstruction to
the discarded fixed-denominator normalization.  No rational-point search
or conditional analytic computation is used.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, prod
from pathlib import Path
import json


C = 450459


def contact(b):
    return prod((b, b-1, b-2401, 32*b+343, 2*b-1))


def vp(n, p):
    assert n
    n = abs(n)
    ans = 0
    while n % p == 0:
        ans += 1
        n //= p
    return ans


def squareclass(q, p):
    q = Q(q)
    v = vp(q.numerator,p)-vp(q.denominator,p)
    unit = q / (Q(p)**v)
    mod = 8 if p == 2 else p
    u = (unit.numerator * pow(unit.denominator, -1, mod)) % mod
    if p == 2:
        a,b = {1:(0,0),3:(1,1),5:(0,1),7:(1,0)}[u]
        return (v % 2,a,b)
    return (v % 2,0 if pow(u,(p-1)//2,p)==1 else 1)


def main():
    beta={4:216,0:C}
    assert 216==2**3*3**3
    assert all(e<4 for e in (vp(216,2),vp(216,3)))
    assert 2*108==216 and 2*225228+3==C

    two = []
    for b in (3,11,19,27):
        assert contact(b) % 32 == 4
        two.append({'beta_mod32':b,'contact_mod32':4})
    assert C%8==3 and C%27==18
    assert all((216*x**4+C)%8==3 for x in range(8))
    assert all((216*x**4+C)%27==18 for x in range(27))
    assert contact(18)%27==9

    rows=[]
    for x in range(17):
        a4=pow(x,4,17)
        b=(216*a4+C)%17
        r=contact(b)%17
        assert (r==0)==(x==0)
        if r:
            assert pow(r,8,17)==1
        rows.append([x,a4,b,r])
    assert {row[1] for row in rows}=={0,1,4,13,16}
    assert {row[3] for row in rows}=={0,2,13,15}
    assert 32*C+343==17**2*49879 and 49879%17==1
    assert contact(C)%(17**3)==9*17**2
    assert prod((C,C-1,C-2401,2*C-1))%17==9
    assert all(pow(a,2,17)==b for a,b in ((8,13),(7,15),(6,2)))
    bound=Q(102**2,17**4)
    assert bound==Q(10404,83521) and 0<bound<1

    # Concrete input checks support, but are not used in, the uniform proof.
    examples=[]
    for x in (-17,-3,-1,0,1,2,17):
        b=216*x**4+C
        r=contact(b)
        delta=1+(17*r)**2
        R=Q(102**2*r,delta**2)
        assert r>0 and gcd(102*r,delta)==1
        assert R.denominator==delta**2 and 0<R<1
        depths={str(p):vp(R.numerator,p)-vp(R.denominator,p) for p in (2,3,17)}
        assert depths['2']==4 and depths['3']==4 and depths['17'] in (2,4)
        assert all(not any(squareclass(R,p)) for p in (2,3,17))
        examples.append({'input':x,'beta':str(b),'local_depths':depths})

    # Why no fixed denominator such as 23 is present in the preferred formula.
    bad23=None
    for x in range(23**2):
        b=2*x*x+3
        r=contact(b)
        if vp(r,23)==1:
            delta=1+(221*r)**2
            old=Q(204**2*r,23**2*delta**2)
            assert vp(old.numerator,23)-vp(old.denominator,23)==-1
            bad23={'input':x,'beta':b,'raw_contact_valuation':1,
                   'old_normalized_valuation':-1}
            break
    assert bad23 is not None

    here=Path(__file__).resolve().parent
    result={
        'status':'PASS',
        'input_polynomial_coefficients_ascending':sorted(beta.items()),
        'input_polynomial_degree':4,
        'constant_congruences':{'mod8':C%8,'mod27':C%27,'mod4913':C%4913},
        'two_adic_table':two,
        'three_adic_contact_mod27':contact(18)%27,
        'seventeen_adic_table_columns':['X','X^4','beta','contact'],
        'seventeen_adic_table':rows,
        'seventeen_zero_case':{'32C_plus343':32*C+343,
                              'divided_by17_squared':49879,
                              'unit_mod17':1,'contact_unit_mod17':9},
        'normalizer':{'delta':'1+(17*r)^2','R':'102^2*r/delta^2',
                      'correction_choices':1,'fixed_denominator':1,
                      'strict_real_upper_bound':str(bound)},
        'integer_examples':examples,
        'discarded_fixed_denominator_counterexample':bad23,
        'scope':{'local_finite_arithmetic':'exact',
                 'norm_tree_positivity':'proved in the accompanying TeX',
                 'global_completeness':'under the inherited source arithmetic hypotheses',
                 'number_field_transfer_claimed':False},
        'proof_sha256':sha256((here/'scalar_normalization.tex').read_bytes()).hexdigest(),
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'scalar-normalization-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','degree':4,'correction_choices':1,
                      'strict_real_upper_bound':str(bound),
                      'fixed_denominator_counterexample':bad23},indent=2))


if __name__=='__main__':
    main()
