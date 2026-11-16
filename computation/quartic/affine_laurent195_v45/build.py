#!/usr/bin/env python3
"""Reconstruct the 195-variable quartic from the pinned quadratic source."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'computation/quartic/laurent_recovery_v38'))
import algebra


def multiply(left, right):
    result = defaultdict(Q)
    for (a, m), c in left.items():
        for (b, n), d in right.items():
            result[a + b, tuple(sorted(m + n))] += c * d
    return {k: v for k, v in result.items() if v}


def build(output):
    certificate = json.loads((HERE / 'transformation.json').read_text())
    source = ROOT / certificate['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == certificate['source_sha256']
    centered = json.loads(source.read_text())
    substitutions = {int(i): algebra.parse(p)
                     for i, p in certificate['affine_substitutions'].items()}
    affine_rows = []
    for row in centered['residuals']:
        result = defaultdict(Q)
        for term in row['terms']:
            polynomial = {(int(term['parameterPower']), ()): Q(term['coefficient'])}
            for i in term['monomial']:
                polynomial = multiply(polynomial, substitutions.get(i, {(0, (i,)): Q(1)}))
            for key, value in polynomial.items():
                result[key] += value
        result = {k: v for k, v in result.items() if v}
        clear = max(0, -min(a for a, m in result))
        row['terms'] = algebra.serial({(a + clear, m): c for (a, m), c in result.items()})
        affine_rows.append({'name': row['name'], 'multiplyByParameterPower': clear})
    assert affine_rows == certificate['affine_rows']
    config = {k: v for k, v in certificate['laurent'].items()
              if k not in ('old_to_new', 'rows')}
    system, laurent = algebra.convert(centered, config)
    assert laurent == certificate['laurent']
    parameter = certificate['parameter_scaling']
    weights = {int(i): v for i, v in parameter['weights'].items()}
    for row in system['residuals']:
        shift = parameter['row_shifts'][row['name']]
        for term in row['terms']:
            term['parameterPower'] += sum(weights.get(i, 0) for i in term['monomial']) - shift
            assert term['parameterPower'] in (0, 1)
        assert min(t['parameterPower'] for t in row['terms']) == 0
        row['terms'].sort(key=lambda t: (t['parameterPower'], tuple(t['monomial'])))
    system['format'] = 'affine-Laurent-parameter-quartic195/v45'
    system['coordinate_convention'] = (
        'Apply the certified triangular affine change, Laurent unit rescaling, '
        'and fixed-parameter coordinate rescaling. The input remains coordinate 1.')
    system['transformation'] = 'transformation.json'
    polynomial = algebra.sum_squares(system)
    polynomial['format'] = 'integer-quartic195/v45'
    profiles = defaultdict(lambda: [0, 0, 0])
    for term in polynomial['terms']:
        profiles[tuple(term['monomial'])][term['parameterPower']] = int(term['coefficient'])
    assert profiles[(1, 1, 1, 1)] == [1, 0, 0]
    constant = 126616122944180358034867798936
    leader = [0, 0, 22201]
    threshold = 149**6
    for profile in profiles.values():
        sign = 1 if next(v for v in reversed(profile) if v) > 0 else -1
        a, b, c = (sign * v for v in profile)
        assert a + 149*b + 149**2*c > 0
        assert b + 298*c >= 0 and c >= 0
        for sign in (-1, 1):
            a, b, c = (u - sign*v for u, v in zip(leader, profile))
            assert a + threshold*b + threshold**2*c >= 0
            assert b + 2*threshold*c >= 0 and c >= 0
    assert leader in profiles.values()
    assert [constant, 0, 0] in profiles.values() or [-constant, 0, 0] in profiles.values()
    for n in range(1, 6):
        C = 149**n
        assert max(abs(a + b*C + c*C*C) for a, b, c in profiles.values()) == constant
        assert 22201*C*C <= constant
    assert 22201*149**12 > constant
    report = {
        'schema': 'affine-Laurent-quartic195-construction/v45',
        'source_sha256': certificate['source_sha256'],
        'variables': 195, 'input_coordinate': 1, 'quadratic_rows': 175,
        'degree': 4, 'integer_content': 1,
        'ordinary_monomials': len(profiles),
        'parameter_separated_terms': len(polynomial['terms']),
        'parameter': 'C=149^N, N>=1',
        'coefficient_height': 'max(126616122944180358034867798936,149^(2N+2))',
        'height_crossover_N': 6,
        'coefficient_parameter_degree': 2,
        'maximum_C_coefficient_in_quadratic_rows': max(
            abs(int(t['coefficient'])) for r in system['residuals']
            for t in r['terms'] if t['parameterPower'] == 1),
        'zero_set_equivalence': 'Input-preserving bijection for every nonzero rational C.',
        'nonzero_conditions': 'The source unit guard is retained; no additional guard.',
        'arithmetic_scope': 'Same inherited source premises and sufficient N threshold; no additional abc assumption.',
        'defining_threshold_effective': False,
        'support_certificate': 'Each coefficient has constant nonzero sign for every C>=149, by nonnegative translated coefficients.',
        'height_certificate': 'Exact finite checks at N=1,...,5, and nonnegative translated coefficient differences for every C>=149^6.',
    }
    assert len(profiles) == 2956 and len(polynomial['terms']) == 2965
    output.mkdir(parents=True, exist_ok=True)
    for name, value in [('quadratic-family.json', system),
                        ('polynomial-family.json', polynomial),
                        ('construction-report.json', report)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE)
    build(parser.parse_args().output)
