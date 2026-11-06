#!/usr/bin/env python3
"""Collect encoded kappa coefficients without materializing the fixed integer.

The only overlapping coefficient groups are a positive constant plus
1024*kappa^2, and three copies of 1-192*kappa. None vanishes for kappa>=1.
The unit input-X^4 coefficient proves primitiveness and exact degree four.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2]


def check(relative, encoded_count, ordinary_count):
    path = RESEARCH / relative
    raw = gzip.decompress(path.read_bytes())
    obj = json.loads(raw)
    groups = {}
    for monomial, k, c in obj['expanded_polynomial']:
        assert c != 0
        group = groups.setdefault(tuple(monomial), {})
        assert k not in group
        group[k] = c
    assert len(obj['expanded_polynomial']) == encoded_count
    assert len(groups) == ordinary_count
    assert groups[(0, 0, 0, 0)] == {0: 1}
    constant = groups[()]
    assert constant[0] > 0 and constant[2] == 1024 and len(constant) == 2
    overlaps = [c for m, c in groups.items() if m and len(c) > 1]
    assert overlaps == [{0: 1, 1: -192}] * 3
    assert all(max(c) <= 1 for m, c in groups.items() if m)
    max_bits = max(abs(a).bit_length() for c in groups.values() for a in c.values())
    assert max_bits <= 1020
    assert constant[0].bit_length() == 825
    assert obj['fixed_constants'] == {'K': '3^(2^28)'}
    # kappa>2^(2^28)>2^1011, so 1024*kappa^2 dominates
    # every other coefficient, whose size is <2^1020*(kappa+1).
    assert 2**28 > 1011
    return {
        'file': relative,
        'status': 'PASS',
        'uncompressed_sha256': hashlib.sha256(raw).hexdigest(),
        'encoded_entries': encoded_count,
        'ordinary_variable_monomials_after_fixed_specialization': ordinary_count,
        'primitive_integer_content': 1,
        'exact_degree': 4,
        'exact_primitive_height': {'kappa': '3^(2^28)',
                                   'formula': '1024*kappa^2+c0',
                                   'c0': str(constant[0])},
        'height_upper_bound': '2^858993471',
        'height_bound_justification': '3^5<2^8 gives log2(kappa)<429496730; '
                                      'c0<2^825 and 1024*kappa^2+c0<2^858993471',
        'noncancellation_proof': 'The four multiple-entry coefficient groups are '
                                'c0+1024*kappa^2 and three copies of 1-192*kappa; '
                                'all are nonzero for the specified positive integer kappa.'}


def main():
    result = [check('phase3/quartic/quartic-direct/polynomial.json.gz', 28991, 28987),
              check('phase2/quartic/quartic-best/polynomial.json.gz', 29419, 29415)]
    print(json.dumps({'status': 'PASS', 'sources': result,
                     'scope': 'Coefficient encoding, exact monomial support, degree and '
                              'primitive height after fixed specialization. No arithmetic '
                              'input-projection assertion is checked.'}, indent=2))


if __name__ == '__main__':
    main()
