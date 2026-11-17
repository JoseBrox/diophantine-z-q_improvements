#!/usr/bin/env python3
"""Independently parse and verify every coefficient of the literal N=15 quartic.

Only Python's standard library is used. This checker does not import the
literal producer or either quadratic-family producer.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
FAMILY_DIGEST = '72d80d57ad9514b184649bfa11dbc43dfce035b6248fa09f93ceb7011bd1cfd7'


def parse_literal(raw):
    lines = raw.decode('ascii').splitlines()
    assert lines[:3] == [
        '# Integer quartic in x1,...,x229; distinguished input x1.',
        '# Fixed specialization N=15. All 3312 terms are listed with literal integer coefficients.',
        'P =',
    ]
    assert len(lines) == 3315
    answer = {}
    for line in lines[3:]:
        match = re.fullmatch(r'  ([+-]) ([1-9][0-9]*)(.*)', line)
        assert match is not None, 'Invalid term syntax'
        sign, magnitude, suffix = match.groups()
        coefficient = int(magnitude) * (1 if sign == '+' else -1)
        monomial = []
        previous = 0
        while suffix:
            factor = re.match(r'\*x([1-9][0-9]*)(?:\^([2-4]))?', suffix)
            assert factor is not None, 'Invalid monomial syntax'
            variable = int(factor.group(1))
            exponent = int(factor.group(2) or '1')
            assert previous < variable <= 229, 'Noncanonical variable order or variable index'
            previous = variable
            monomial.extend([variable] * exponent)
            suffix = suffix[factor.end():]
        key = tuple(monomial)
        assert len(key) <= 4 and key not in answer, 'Excess degree or duplicate monomial'
        answer[key] = coefficient
    assert list(answer) == sorted(answer), 'Noncanonical term order'
    return answer


def specialized_square_expansion(quadratic):
    assert quadratic['variables'] == 229
    assert quadratic['inputCoordinate'] == 1
    assert len(quadratic['residuals']) == 207
    fixed = 149 ** 15
    result = defaultdict(int)
    for row in quadratic['residuals']:
        terms = defaultdict(int)
        for term in row['terms']:
            m = tuple(sorted(term['monomial']))
            assert len(m) <= 2 and term['parameterPower'] in (0, 1)
            terms[m] += int(term['coefficient']) * fixed ** term['parameterPower']
        terms = [(m, c) for m, c in terms.items() if c]
        for i, j in combinations_with_replacement(range(len(terms)), 2):
            a, c = terms[i]
            b, d = terms[j]
            m = tuple(sorted(a + b))
            result[m] += c * d * (1 if i == j else 2)
    return {m: c for m, c in result.items() if c}


def main():
    literal_path = ROOT / 'quartic229-N15.txt'
    literal_raw = literal_path.read_bytes()
    actual = parse_literal(literal_raw)
    quadratic_raw = (ROOT / 'quadratic.json').read_bytes()
    expected = specialized_square_expansion(json.loads(quadratic_raw))
    assert actual == expected, 'The literal expression differs from the complete sum of squares'

    family_raw = (ROOT / 'polynomial.json').read_bytes()
    assert sha256(family_raw).hexdigest() == FAMILY_DIGEST
    family = json.loads(family_raw)
    by_monomial = defaultdict(dict)
    for term in family['terms']:
        m = tuple(term['monomial'])
        a = int(term['parameterPower'])
        assert a in (0, 1, 2) and a not in by_monomial[m]
        by_monomial[m][a] = int(term['coefficient'])
    fixed = 149 ** 15
    evaluated = {}
    for m, profile in by_monomial.items():
        coefficient = 0
        for a in (2, 1, 0):
            coefficient = coefficient * fixed + profile.get(a, 0)
        if coefficient:
            evaluated[m] = coefficient
    assert actual == evaluated, 'The literal expression differs from the coefficient family'
    assert len(actual) == 3312
    assert {i for m in actual for i in m} == set(range(1, 230))
    assert max(map(len, actual)) == 4
    assert gcd(*actual.values()) == 1
    assert actual[(1, 1, 1, 1)] == 1
    height = max(abs(c) for c in actual.values())
    assert height == 149 ** 32
    assert height.bit_length() == 232

    report = {
        'schema': 'literal-integer-quartic-verification/v62',
        'status': 'PASS',
        'scope': 'Exact parser comparison with every coefficient of the specialized 207-square expansion and coefficient family.',
        'artifact': literal_path.name,
        'artifact_sha256': sha256(literal_raw).hexdigest(),
        'artifact_bytes': len(literal_raw),
        'artifact_lines': len(literal_raw.splitlines()),
        'fixed_N': 15,
        'literal_integer_coefficients': True,
        'family_parameter_absent_from_expression': True,
        'variables_including_input': 229,
        'input_variable': 'x1',
        'all_variables_used': True,
        'degree': 4,
        'content': 1,
        'terms': 3312,
        'coefficient_height': '149^32',
        'coefficient_height_bits': 232,
        'source_quadratic_sha256': sha256(quadratic_raw).hexdigest(),
        'source_family_sha256': sha256(family_raw).hexdigest(),
        'producer_imported': False,
    }
    (ROOT / 'literal_certificate.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
