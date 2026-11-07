#!/usr/bin/env python3
"""Certify an explicit nonintegral input over a quadratic extension.

This is a base-change statement about the one polynomial, not a claim about
the rational input projection or the defining system over other fields.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter, defaultdict
from math import isqrt
import argparse
import gzip
import hashlib
import json


def bytes_at(path):
    if path.exists():
        return path.read_bytes()
    return gzip.decompress(path.with_suffix(path.suffix + '.gz').read_bytes())


def specialize(terms, coordinate):
    result = defaultdict(Q)
    for term in terms:
        monomial = term['monomial']
        if not set(monomial).issubset({0, coordinate}):
            continue
        key = (monomial.count(coordinate), term.get('sPower', 0))
        result[key] += Q(term['coefficient']) * Q(1, 2) ** monomial.count(0)
    return {key: value for key, value in result.items() if value}


def square(poly):
    result = defaultdict(Q)
    for (e, s), a in poly.items():
        for (f, t), b in poly.items():
            result[(e+f, s+t)] += a*b
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    poly_bytes = bytes_at(args.directory / 'polynomial.json')
    residual_bytes = bytes_at(args.directory / 'residuals.json')
    polynomial = json.loads(poly_bytes)
    residuals = json.loads(residual_bytes)
    name = 'V0.yProduct.0.quadratic'
    candidates = [c for c in polynomial['coordinates'] if c['name'] == name]
    assert len(candidates) == 1
    coordinate = candidates[0]['id']
    individual_degree = max(t['monomial'].count(coordinate) for t in polynomial['terms'])
    assert individual_degree == 2
    direct = specialize(polynomial['terms'], coordinate)
    independent = defaultdict(Q)
    for row in residuals['residuals']:
        p = specialize(row['terms'], coordinate)
        assert all(e <= 1 for e, s in p)
        for key, value in square(p).items():
            independent[key] += value
    independent = {key: value for key, value in independent.items() if value}
    assert direct == independent
    assert set(direct) == {(2, 0), (0, 0)}
    assert direct[(2, 0)] == 1
    constant = direct[(0, 0)]
    assert constant > 0
    denominator = isqrt(constant.denominator)
    assert denominator * denominator == constant.denominator
    N = constant.numerator
    # In Q[Z]/(Z^2+N), the proposed point has Y=Z/denominator.
    assert Q(-N, denominator**2) + constant == 0
    result = {
        'status': 'PASS', 'total_variables': len(polynomial['coordinates']),
        'input': '1/2', 'nonzero_witness_coordinate': coordinate,
        'nonzero_witness_name': name, 'all_other_witnesses': '0',
        'individual_degree': 2,
        'specialized_polynomial': f'Y^2 + {constant.numerator}/{constant.denominator}',
        'quadratic_field': f'Q[Z]/(Z^2+{N})',
        'witness_value': f'Z/{denominator}',
        'field_degree': 2, 'field_irreducibility_reason': 'N is a positive integer, so -N is not a rational square.',
        'integrality_obstruction': '1/2 is not an algebraic integer.',
        'verified_by': ['direct specialization of every quartic coefficient',
                        'independent specialization and squaring of every residual'],
        'polynomial_sha256': hashlib.sha256(poly_bytes).hexdigest(),
        'residuals_sha256': hashlib.sha256(residual_bytes).hexdigest(),
        'scope': 'Explicit failure of the unchanged single equation over one quadratic extension. No assertion against field-dependent Diophantine definability.'
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
