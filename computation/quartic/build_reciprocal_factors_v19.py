#!/usr/bin/env python3
"""Clear local factor equations by an inverse fourth power.

The defining factor variables and their product remain unchanged. Removing
the five shared numerator fourth powers saves ten rational coordinates in
the inherited constructions. The abc construction removes two field fourth
powers and uses one additional scalar reciprocal per detector.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCES = {
    'inherited': ('family238_v18/quadratic-family238-v18.json',
                  'bc97c0d10cd270c2bb856857eaaef7836c4a7a9a0cb039d3cd1e664e0e5db19a', 228),
    'explicit': ('family276_v19/quadratic-family276-v19.json',
                 'c191e1b87651b6b14903a90092a13adf02803c6266274beea4477f6c3a3b5587', 266),
    'abc': ('family_abc93_v18/quadratic-family-abc93-v18.json',
            '82a409221257575b74406868532c5662323e6ab33afa11a6e41087baeb6ce1b0', 91),
}


def decode(row, identifiers):
    return {(t['parameterPower'], tuple(sorted(identifiers[i] for i in t['monomial']))):
            Q(t['coefficient']) for t in row['terms']}


def clear_factor(p, q, old_weights, inverse_weights, factor_ids, definitions):
    """Transform a primitive old factor row without using its field formula."""
    weight_substitutions = dict(zip(old_weights, inverse_weights))
    # The order of old_weights is q2,q4,q7 (or q2,q4,q for abc).
    r4 = inverse_weights[3]
    result = {}
    for (parameter, monomial), coefficient in p.items():
        assert parameter == 0
        if not monomial:
            term = v(r4)
        elif len(monomial) == 1 and monomial[0] in factor_ids:
            term = mul(v(r4), v(monomial[0]))
        else:
            weights = [x for x in monomial if x in weight_substitutions]
            assert len(weights) == 1, monomial
            weight = weights[0]
            remainder = list(monomial)
            remainder.remove(weight)
            base = one
            for x in remainder:
                base = mul(base, definitions.get(x, v(x)))
            replacement = weight_substitutions[weight]
            term = base if replacement is None else mul(v(replacement), base)
        result = add(result, scale(term, coefficient))
    return primitive(result)


def build(kind, source_root=HERE, output_root=HERE):
    path, pin, count = SOURCES[kind]
    raw = (source_root/path).read_bytes()
    assert sha256(raw).hexdigest() == pin
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    old_rows = [(r, decode(r, old_ids)) for r in source['residuals']]
    if kind == 'abc':
        removed = {30002, 30003, 30004, 30005}
    else:
        removed = {180, 181, 198, 199, 210, 211, 222, 223, 21004, 21005}
    definitions, removed_rows = {}, []
    for row, p in old_rows:
        linear_outputs = [x for x in removed if (0, (x,)) in p]
        if len(linear_outputs) == 1:
            x = linear_outputs[0]
            if not any((set(m) & removed)-{x} for _, m in p):
                coefficient = p[0, (x,)]
                definitions[x] = scale(add(p, scale(v(x), -coefficient)), -1/coefficient)
                removed_rows.append(row['name'])
    assert set(definitions) == removed
    assert len(removed_rows) == len(removed)
    coordinates = [dict(c) for c in source['coordinates'] if c['sourceId'] not in removed]
    additions, changes, renamed = [], {}, {}
    if kind == 'abc':
        for j, q in enumerate((30010, 30032)):
            r2, r4, r3 = q+3, q+4, 51000+j
            prefix = f'detector{j}.'
            coordinates.append({'sourceId': r3, 'name': prefix+'inverseWeightCubed', 'kind': 'gate'})
            renamed[r2], renamed[r4] = prefix+'inverseWeightSquared', prefix+'inverseWeightFourthPower'
            changes[prefix+'weightSquared.definition'] = (prefix+'inverseWeightCubed.definition',
                add(mul(v(q), v(r4)), scale(v(r3), -1)))
            changes[prefix+'weightFourthPower.definition'] = (prefix+'inverseWeightFourthPower.definition',
                add(mul(v(r2), v(r2)), scale(v(r4), -1)))
            additions.append(({'sourceId': 71000+j, 'name': prefix+'inverseWeightSquared.definition'},
                              add(mul(v(q), v(r3)), scale(v(r2), -1))))
            factor_ids = set(range(q+5, q+9))
            for row, p in old_rows:
                if row['name'].startswith(prefix+'factor'):
                    changes[row['name']] = (row['name'].replace('.definition', '.reciprocal.definition'),
                        clear_factor(p, q, (q+3, q+4, q), (r2, None, r3, r4),
                                     factor_ids, definitions))
    else:
        detector_maps = [dict(), {352: 400, 360: 408, 361: 409, 362: 410}]
        if kind == 'explicit':
            detector_maps.append({c['copiedSourceId']: c['sourceId'] for c in source['coordinates']
                                  if 'copiedSourceId' in c})
        for j, substitution in enumerate(detector_maps):
            q, r1, r2, r4 = [substitution.get(x, x) for x in (352, 360, 361, 362)]
            prefix = f'detector{j}.'
            renamed.update({r1: prefix+'inverseWeight', r2: prefix+'inverseWeightSquared',
                            r4: prefix+'inverseWeightFourthPower'})
            changes[prefix+'E1.power2.definition'] = (prefix+'inverseWeight.definition',
                add(mul(v(q), v(r1)), scale(one, -1)))
            changes[prefix+'E1.power4.definition'] = (prefix+'inverseWeightSquared.definition',
                add(mul(v(r1), v(r1)), scale(v(r2), -1)))
            changes[f'reflected.{prefix}weightPower7.definition'] = (prefix+'inverseWeightFourthPower.definition',
                add(mul(v(r2), v(r2)), scale(v(r4), -1)))
            factor_prefix = f'residue.det{j}.factor'
            factor_ids = {c['sourceId'] for c in source['coordinates']
                          if c['name'].startswith(f'amplified.det{j}.factor')}
            assert len(factor_ids) == 10
            for row, p in old_rows:
                if row['name'].startswith(factor_prefix):
                    # q7 becomes q5 and q*A2^2 becomes q3*A2^2 before
                    # multiplying by q^-4. The last substitution is r1.
                    weights = (r2, r4, r1, q)
                    replacements = (r2, None, q, r1)
                    transformed = {}
                    for (a, m), coefficient in p.items():
                        assert a == 0
                        if not m:
                            term = v(r4)
                        elif len(m) == 1 and m[0] in factor_ids:
                            term = mul(v(r4), v(m[0]))
                        else:
                            hits = [x for x in m if x in weights]
                            assert len(hits) == 1, m
                            w = hits[0]
                            rest = list(m); rest.remove(w)
                            term = one
                            for x in rest:
                                term = mul(term, definitions.get(x, v(x)))
                            replacement = replacements[weights.index(w)]
                            if replacement is not None:
                                term = mul(v(replacement), term)
                        transformed = add(transformed, scale(term, coefficient))
                    changes[row['name']] = (row['name'].replace('.definition', '.reciprocal.definition'), transformed)
    for i, c in enumerate(coordinates):
        c['id'] = i+1
        c['name'] = renamed.get(c['sourceId'], c['name'])
    identifiers = {c['sourceId']: c['id'] for c in coordinates}
    assert len(coordinates) == count
    assembled, changed = [], []
    for row, p in old_rows:
        if row['name'] in removed_rows:
            continue
        if row['name'] in changes:
            name, p = changes.pop(row['name'])
            changed.append({'sourceId': row['sourceId'], 'oldName': row['name'], 'newName': name})
        else:
            name = row['name']
        assert not any(removed.intersection(m) for _, m in p)
        assembled.append((dict(row, name=name), p))
    assert not changes, changes
    assembled += additions
    rows, expanded = [], defaultdict(int)
    for metadata, p in assembled:
        p = primitive(p)
        p = {(a, tuple(sorted(identifiers[x] for x in m))): c for (a, m), c in p.items()}
        assert max(len(m) for _, m in p) <= 2
        rows.append(dict(metadata, id=len(rows)+1, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    expanded = {m: c for m, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(rows) == {'inherited': 202, 'explicit': 238, 'abc': 79}[kind]
    assert gcd(*expanded.values()) == 1 and max(len(m) for _, m in expanded) == 4
    assert {x for _, m in expanded for x in m} == set(range(1, count+1))
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    parameter_description = dict(source['fixedParameter'])
    if kind == 'explicit':
        parameter_description['N'] = 'Every integer N>=14521; this effective sufficient threshold uses the abscissa-sum height theorem.'
    system = dict(source, format='integer-quadratic-family-reciprocal-factors-v19', variables=count,
                  source={'construction': path, 'sha256': pin}, fixedParameter=parameter_description,
                  coordinates=coordinates, residuals=rows)
    polynomial = dict(format='integer-quartic-family-reciprocal-factors-v19', variables=count,
                      degree=4, inputCoordinate=1, fixedParameter=parameter_description,
                      coordinates=coordinates, terms=terms(expanded))
    report = {
        'status': 'Exact rational projection with reciprocal factor equations; arithmetic premises and coefficient thresholds are specified separately.',
        'variables': count, 'quadraticResiduals': len(rows), 'degree': 4, 'content': 1,
        'symbolicTerms': len(expanded), 'ordinaryMonomialsForEveryPositiveParameter': len(profiles),
        'sourceSha256': pin, 'removedSourceCoordinates': sorted(removed),
        'removedSourceRows': removed_rows, 'changedRows': changed,
        'addedSourceCoordinates': [51000, 51001] if kind == 'abc' else [],
        'addedSourceRows': [71000, 71001] if kind == 'abc' else [],
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'linearCoefficientMultiplierMaximum': L,
        'inverseWeights': ['q^-2', 'q^-3', 'q^-4'] if kind == 'abc' else ['q^-1', 'q^-2', 'q^-4'],
        'removedSharedFieldFourthPowers': 2 if kind == 'abc' else 5,
        'comparisonPrecision': 1 if kind == 'abc' else 3,
        'inputPrecision': 1,
        'zeroWeightStratum': 'Impossible: the two cleared factor equations force both numerator reciprocals zero, contrary to the exact pair chart.' if kind == 'abc' else 'Excluded by q*r1=1. Complete witnesses already have a selected contact prime with v(q)=-1.',
    }
    if kind == 'abc':
        assert profiles[()][2] == 1
        offset = profiles[()][0]
        threshold = max(3, isqrt(max(0, C-offset)))
        threshold += (threshold % 2 == 0)
        if threshold*threshold+offset < C:
            threshold += 2
        report.update(coefficientHeightForEveryIntegerBAtLeast3=f'max({C},B^2+{offset})',
                      constantCoefficientWithoutParameter=str(offset),
                      coefficientHeightThresholdOddB=threshold,
                      fixture={'B': 3, 'definesIntegersCertified': False},
                      arithmeticScope='Ordinary rational abc and the retained elliptic, pole, height, and simultaneous-prime inputs; sufficient odd B remains ineffective.')
        suffix, directory = '-abc91-v19', 'family_abc91_v19'
    else:
        assert profiles[(identifiers[489], identifiers[489])] == {0: 1, 2: 1}
        assert C > L*L
        threshold = next(n for n in range(1, 200) if 149**(4*n+2)+1 > C)
        report.update(heightFormulaForEveryPositiveParameter='max(C,A^2+1)',
                      exactHeightThresholdN=threshold,
                      exactHeightForNAtLeastThreshold='149^(4*N+2)+1',
                      baseContactHeightConstant='2^221234', baseContactHeightExponent='7/3',
                      tenContactHeightConstantUpperBound='2^221284', tenContactHeightExponent='7/6',
                      arithmeticScope='Retained modular, elliptic, pole, and simultaneous-prime inputs, with the proved modular multiplicity height refinement.')
        suffix, directory = str(count)+'-v19', 'family'+str(count)+'_v19'
        if kind == 'explicit':
            N, depth = 14521, 68973
            c, H, H2 = 149**depth, 1 << 221234, 1 << 221284
            assert depth == 19*(2*N-1)//8+1
            assert (c-1)**4 > (14*H2)**9
            assert c > 40*H and c > 40*265546
            report.update(scales=['1', 'S0^2', '(S0+S1)^2'],
                          definingThresholdN=N, forcedIndexDepthAtThreshold=depth,
                          specifiedParameter='149^29043', specifiedCoefficientHeight='149^58086+1',
                          specifiedCoefficientHeightBinaryDigits=(149**58086+1).bit_length(),
                          soundnessIntegerCertificates={
                              'lucasContradiction': '(149^68973-1)^4 > (14*2^221284)^9',
                              'scalarHeight': '149^68973 > 40*2^221234',
                              'additiveHeight': '149^68973 > 40*265546'})
    output = output_root/directory
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [('quadratic-family'+suffix+'.json', system),
                           ('polynomial-family'+suffix+'.json', polynomial),
                           ('construction-report'+suffix+'.json', report)]:
        (output/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
          'ordinaryMonomialsForEveryPositiveParameter', 'constantCoefficientMaximumBits')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=(*SOURCES, 'all'), default='all')
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    for kind in SOURCES if args.kind == 'all' else (args.kind,):
        build(kind, args.source_root, args.output_root)
