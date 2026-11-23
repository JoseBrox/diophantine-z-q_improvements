#!/usr/bin/env python3
"""Exact checks accompanying three proved, narrowly scoped compression barriers."""
from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path
import sympy as sp


def verify():
    target = 5**60
    assert 2**139 < target < 2**140
    sequence = [(target + 2**i - 1)//2**i for i in range(137, -1, -1)]
    assert sequence[0] == 5 and sequence[-1] == target
    exponents = {0, 1, 2}
    steps = [(3, 1, 2, 0), (5, 3, 2, 0)]
    steps += [(b, a, a, 2*a-b) for a, b in zip(sequence, sequence[1:])]
    assert len(steps) == 139
    for new, left, right, denominator in steps:
        assert left in exponents and right in exponents and denominator in exponents
        assert new == left + right - denominator
        old_width = max(exponents)-min(exponents)
        exponents.add(new)
        assert max(exponents)-min(exponents) <= 2*old_width
    assert target in exponents

    edge_cases = 0
    for old in ([F(0)], [F(0),F(1)], [F(-1),F(0)],
                [F(-3),F(-1),F(0),F(1,2),F(2),F(5)]):
        width=max(old)-min(old)
        for a,b,c in product(old,repeat=3):
            new=a+b-c
            assert max(*old,new)-min(*old,new) <= 2*width
            edge_cases+=1
        for a,b in product(old,repeat=2):
            new=(a+b)/2
            assert min(old)<=new<=max(old)
            edge_cases+=1

    # Independent symbolic check of the rational point on any quadratic level set.
    ell, quad=sp.symbols('ell quad', nonzero=True)
    scale=-ell/quad
    assert sp.cancel(scale*ell+scale**2*quad)==0
    assert F(3,5)**2+F(4,5)**2==1

    # Polynomial norm preservation and three-square identity, then exact examples.
    n,t=sp.symbols('n t')
    assert sp.expand((3*n+4*t)**2-2*(2*n+3*t)**2-(n*n-2*t*t))==0
    discrepancy=(n**4-1)**2+(2*n*t)**2+(2*t)**2-(n**8-1)
    assert sp.expand(discrepancy+2*(n*n+1)*(n*n-2*t*t-1))==0
    k=12
    n,t=1,0
    examples=[]
    for j in range(1,13):
        n,t=3*n+4*t,2*n+3*t
        assert n*n-2*t*t==1 and n>=3**j
        inputs=[F(1,n)]+[F(1)]*(k-1)
        traces=[F(n**4-1,n**4),F(2*n*t,n**4),F(2*t,n**4)]+[F(0)]*(k-3)
        assert all(q>0 for q in inputs)
        assert all(q>0 for q in traces[:3])
        assert sum(q**8 for q in inputs)+sum(q*q for q in traces)==k
        examples.append({'index':j,'n':str(n),'t':str(t),
                         'input_1_height':'log('+str(n)+')','sum':k})
    return {'status':'PASS', 'target_exponent':str(target),
            'strict_lower_power':139,'strict_upper_power':140,
            'power_coordinates':139,'triangular_laurent_lower_bound':139,
            'rational_interval_edge_cases':edge_cases,
            'quadratic_level_identity':True,'pell_norm_identity':True,
            'height_sum_identity':True,'height_counterexample_tuple_length':k,
            'height_counterexamples':examples,
            'scope':['Triangular quadratic binomial Laurent coordinates only',
                     'One quadratic integer-valued test on an unrestricted tuple',
                     'Unrestricted shared-height inequality, without elliptic constraints'],
            'new_undecidability_claim':False,'new_variable_count_claim':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    out=verify()
    path=Path(__file__).with_name('certificate.json')
    if args.write:
        path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(path.read_text())==out
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':
    main()
