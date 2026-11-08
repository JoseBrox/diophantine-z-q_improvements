#!/usr/bin/env python3
"""Build the three-scale linear-form quartic family, with exact arithmetic.

This constructor establishes the algebraic specification. The accompanying
paper proves the defining property, under its stated arithmetic premises,
for every integer N at least 27464.
"""
from collections import defaultdict
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE_PIN = 'f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394'


def add(*polys):
    result = defaultdict(Fraction)
    for poly in polys:
        for key, value in poly.items():
            result[key] += value
    return {key: value for key, value in result.items() if value}


def mul(left, right):
    result = defaultdict(Fraction)
    for (a, m), c in left.items():
        for (b, n), d in right.items():
            result[a + b, tuple(sorted(m + n))] += c * d
    return {key: value for key, value in result.items() if value}


def primitive(poly):
    den = lcm(*(value.denominator for value in poly.values()))
    result = {key: int(value * den) for key, value in poly.items()}
    common = gcd(*result.values())
    if result[min(result)] < 0:
        common = -common
    return {key: value // common for key, value in sorted(result.items())}


def term_list(poly):
    return [{'parameterPower': a, 'monomial': list(m), 'coefficient': str(c)}
            for (a, m), c in sorted(poly.items())]


def main():
    raw = gzip.decompress((HERE / 'baseline389/quadratic-system389.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SOURCE_PIN
    source = json.loads(raw)
    product_sources = set(range(337, 343))
    odd_sources = {66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80}
    deleted_sources = product_sources | odd_sources | {345}
    deleted = {c['id'] for c in source['coordinates'] if c['sourceId'] in deleted_sources}
    assert len(deleted) == 19
    coordinates = []
    mapping = {}
    renames = {
        343: 'abscissaSum.realQuarterSquare',
        344: 'abscissaSum.linearFormQuarterSquare',
    }
    for coord in source['coordinates']:
        if coord['id'] in deleted:
            continue
        mapping[coord['id']] = len(coordinates) + 1
        coordinates.append(dict(coord, id=mapping[coord['id']],
                                name=renames.get(coord['sourceId'], coord['name'])))
    by_source = {c['sourceId']: c['id'] for c in source['coordinates']}
    new_by_source = {c['sourceId']: c['id'] for c in coordinates}
    x = new_by_source[0]
    y = new_by_source[248]
    replacements = {old: {(0, (new,)): Fraction(1)} for old, new in mapping.items()}
    replacements[by_source[0]] = {(0, (x,)): Fraction(1, 2), (0, ()): Fraction(-1, 2)}
    replacements[by_source[248]] = {
        (0, (y,)): Fraction(1, 4), (0, (x,)): Fraction(-1, 2),
        (0, ()): Fraction(1, 4),
    }
    # Actual root abscissas are (x0 + 2*x1*rho), except T whose real
    # component is twice its stored x0. Both nonconstant detectors will
    # use the source detector1 normalization: the stored scale is a/4.
    sum_real = {(0, (new_by_source[sid],)): Fraction(factor)
                for sid, factor in [(82, 1), (84, 1), (86, 2), (88, 1)]}
    sum_imaginary = {(0, (new_by_source[sid],)): Fraction(2)
                     for sid in [83, 85, 87, 89]}
    linear_form = add(sum_real, sum_imaginary)
    scale_rows = {
        295: add(mul(sum_real, sum_real),
                 {(0, (new_by_source[343],)): Fraction(-4)}),
        296: add(mul(linear_form, linear_form),
                 {(0, (new_by_source[344],)): Fraction(-4)}),
    }
    by_name = {coord['name']: coord['id'] for coord in source['coordinates']}
    row_by_name = {row['name']: row for row in source['residuals']}
    detector_clone = {by_source[343]: by_source[344]}
    for coord in source['coordinates']:
        name = coord['name']
        if name.startswith('detector1.'):
            detector_clone[coord['id']] = by_name['detector2.' + name[len('detector1.'):]]
        elif name.startswith('hybrid.det1.'):
            detector_clone[coord['id']] = by_name['hybrid.det2.' + name[len('hybrid.det1.'):]]
    assert len(detector_clone) == 53
    rows = []
    removed_rows = []
    changed_rows = []
    cloned_rows = []
    for row in source['residuals']:
        sid = row['sourceId']
        if 289 <= sid <= 294 or sid == 297 or 687 <= sid <= 698:
            removed_rows.append(sid)
            continue
        if sid in scale_rows:
            rows.append(dict(row, name=renames[343 if sid == 295 else 344] + '.definition',
                             terms=term_list(primitive(scale_rows[sid]))))
            changed_rows.append(sid)
            continue
        if row['name'].startswith(('detector2.', 'hybrid.det2.')):
            template_name = row['name'].replace('detector2.', 'detector1.', 1).replace('hybrid.det2.', 'hybrid.det1.', 1)
            template = row_by_name[template_name]
            cloned_rows.append({'targetSourceId': sid, 'templateSourceId': template['sourceId']})
            row = dict(row, terms=[dict(term, monomial=sorted(detector_clone.get(j, j) for j in term['monomial']))
                                   for term in template['terms']])
        assert not any(j in deleted for t in row['terms'] for j in t['monomial']), row['name']
        poly = {}
        for term in row['terms']:
            value = int(term['coefficient'])
            if sid == 492 and value == 4896:
                value = 9792
            image = {(term['parameterPower'], ()): Fraction(value)}
            for j in term['monomial']:
                image = mul(image, replacements[j])
            poly = add(poly, image)
        normal = primitive(poly)
        assert max(len(m) for a, m in normal) <= 2
        name = row['name']
        rows.append(dict(row, name=name, terms=term_list(normal)))
        if sid == 492 or any(j in {by_source[0], by_source[248]}
                            for t in row['terms'] for j in t['monomial']):
            changed_rows.append(sid)
    coefficients = defaultdict(int)
    for row in rows:
        for left in row['terms']:
            for right in row['terms']:
                key = (left['parameterPower'] + right['parameterPower'],
                       tuple(sorted(left['monomial'] + right['monomial'])))
                coefficients[key] += int(left['coefficient']) * int(right['coefficient'])
    coefficients = {key: value for key, value in coefficients.items() if value}
    parameter = {'name': 'A', 'base': 80989, 'exponent': '2*N+1', 'coordinate': False,
                 'N': 'Any integer at least 27464 under the arithmetic premises stated in the paper.',
                 'explicitDefiningMember': {'N': 27464, 'exponent': 54929}}
    system = {
        'format': 'integer-quadratic-family-v3', 'variables': len(coordinates),
        'inputCoordinate': 1, 'fixedParameter': parameter,
        'source': {'sha256': SOURCE_PIN, 'construction': 'quartic389'},
        'coordinates': coordinates, 'residuals': rows,
    }
    polynomial = {
        'format': 'integer-quartic-family-v3', 'variables': len(coordinates),
        'degree': 4, 'inputCoordinate': 1, 'fixedParameter': parameter,
        'coordinates': coordinates, 'terms': term_list(coefficients),
    }
    ordinary = defaultdict(dict)
    for (a, m), value in coefficients.items():
        ordinary[m][a] = value
    height = max(sum(abs(value) for value in part.values()) for part in ordinary.values())
    report = {
        'status': 'Exact family, defining the integers for every N>=27464 under the stated arithmetic premises.',
        'variables': len(coordinates), 'quadraticResiduals': len(rows),
        'degree': max(len(m) for a, m in coefficients),
        'symbolicTerms': len(coefficients), 'ordinaryMonomialsForSufficientlyLargeN': len(ordinary),
        'deletedCoordinateSourceIds': sorted(deleted_sources),
        'deletedSourceRows': removed_rows, 'changedSourceRows': changed_rows,
        'detectorCloneRows': cloned_rows,
        'inputLabel': 'beta=51*X^2+2504', 'scalarShift': 9792,
        'semanticAggregate': 'S=sum_i x([n_i]P)=S0+S1*sqrt(2)',
        'semanticScales': ['1', 'S0^2', '(S0+S1)^2'],
        'heightBound': {'coefficientSumBitLength': height.bit_length(),
                        'formula': f'H(P_N)<2^{height.bit_length()}*80989^(4*N+2)'},
    }
    output = HERE / 'family370'
    output.mkdir(exist_ok=True)
    for name, value in [('quadratic-family370.json', system),
                        ('polynomial-family370.json', polynomial),
                        ('construction-report370.json', report)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['status', 'variables', 'quadraticResiduals',
                     'degree', 'symbolicTerms', 'ordinaryMonomialsForSufficientlyLargeN', 'heightBound']}, indent=2))


if __name__ == '__main__':
    main()
