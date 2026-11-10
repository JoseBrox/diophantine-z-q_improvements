#!/usr/bin/env python3
"""Replace the common elliptic chart by four field coordinates.

Three quadrics store both reciprocal formal parameters, so each
numerator pair uses its alternate ratio without a separate z-coordinate.
This is an exact change of the retained open elliptic chart. Arithmetic
premises and ineffective coefficient thresholds remain unchanged.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, fm, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCES = {
    'inherited': ('family248_v17/quadratic-family248-v17.json', 4, 238),
    'abc': ('family_abc97_v17/quadratic-family-abc97-v17.json', 1, 93),
}
PINS = {
    'inherited': 'b1bf58c470365a7b330af4a33a17a1f7e9aa10c997853c9078a9b8593f43a7ff',
    'abc': 'e50b41cb15194418771262045afa97fc86ad5c47f376591b732106b690a5491b',
}
ROW_BASIS = [
    ['-233/136612', '991/819672', '233/136612', '-991/819672', '0', '0'],
    ['-845/204918', '2389/819672', '845/204918', '-2389/819672', '0', '0'],
    ['5489/1317904', '-969/329476', '5489/1317904', '-969/329476', '167/392', '-25/98'],
    ['2263/1317904', '-1613/1317904', '2263/1317904', '-1613/1317904', '-1535/392', '1109/392'],
    ['-5489/1317904', '969/329476', '-5489/1317904', '969/329476', '1009/392', '-171/98'],
    ['-969/164738', '5489/1317904', '-969/164738', '5489/1317904', '-25/49', '167/392'],
]


def fadd(*values):
    return tuple(add(*(value[i] for value in values)) for i in range(2))


def fs(value, coefficient):
    return tuple(scale(component, coefficient) for component in value)


def constant(a, b=0):
    return scale(one, Q(a)), scale(one, Q(b))


def common_rows():
    a, b, D = constant(Q(57, 8), Q(-7, 2)), constant(Q(-165, 8), Q(417, 32)), constant(11, -6)
    a2, b2 = fm(a, a), fm(b, b)
    plus, minus = fadd(a2, D), fadd(a2, fs(D, -1))
    S, T = (v(142), v(143)), (v(90), v(91))
    f, g = (v(140), v(141)), (v(160), v(161))
    ST = fm(S, T)
    lf = fs(fm(fm(b, D), fadd(fm(a, T), fs(b, -1))), 2)
    lg = fs(fm(fm(b, D), fadd(fm(a, S), b)), 2)
    qf = fadd(fm(fm(a, plus), ST), fm(fm(b, plus), S),
               fs(fm(fm(b, minus), T), -1), fs(fm(a2, D), 4))
    qg = fadd(fs(fm(fm(a, plus), ST), -1), fs(fm(fm(b, minus), S), -1),
               fm(fm(b, plus), T), fs(fm(a2, D), -4))
    relations = [fadd(fm(lf, f), fs(qf, -1)),
                 fadd(fm(lg, g), fs(qg, -1)),
                 fadd(fm(fm(D, D), fm(f, g)), fm(fm(a, D), fadd(f, g)),
                      fm(a, ST), fm(b, fadd(S, fs(T, -1))), D)]
    components = [primitive(relation[j]) for relation in relations for j in range(2)]
    return [(f'commonPoint.reducedQuadratic.{i}',
             primitive(add(*(scale(component, Q(c)) for component, c in zip(components, coefficients)))))
            for i, coefficients in enumerate(ROW_BASIS)]


def build(kind, source_root=HERE, output_root=HERE):
    path, pairs, count = SOURCES[kind]
    raw = (source_root/path).read_bytes()
    assert sha256(raw).hexdigest() == PINS[kind]
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    deleted_coordinates = {700, 701, *(164+4*i+j for i in range(pairs) for j in (0, 1))}
    deleted_rows = {661, 662, *(116+4*i+j for i in range(pairs) for j in (0, 1))}
    common_source_rows = [34, 35, 92, 93, 112, 113]
    changes = dict(zip(common_source_rows, common_rows()))
    for i in range(pairs):
        LP = (v(234+4*i), v(235+4*i))
        K = (v(114+8*i), v(115+8*i))
        numerator = (v(110+8*i), v(111+8*i))
        T = (v(90), v(91))
        equation = fadd(fm(LP, K), fs(fm(numerator, T), -1))
        for j in range(2):
            key = 146+12*i+j if kind == 'inherited' else f'alternateRatio.cleared.{j}'
            changes[key] = (f'alternateRatio{i+1}.direct.{j}', equation[j])
    coords = [dict(c, id=i+1) for i, c in enumerate(c for c in source['coordinates']
              if c['sourceId'] not in deleted_coordinates)]
    for c in coords:
        if c['sourceId'] in (90, 91):
            c['name'] = 'alternate.negativeReciprocalZ0.'+str(c['sourceId']-90)
        if c['sourceId'] in (142, 143):
            c['name'] = 'primary.negativeReciprocalZ0.'+str(c['sourceId']-142)
    mapping = {c['sourceId']: c['id'] for c in coords}
    rows, changed = [], []
    expanded = defaultdict(int)
    for row in source['residuals']:
        sid = row['sourceId']
        if sid in deleted_rows:
            continue
        key = sid if sid in changes else row['name']
        if key in changes:
            name, p = changes.pop(key)
            changed.append({'sourceId': sid, 'oldName': row['name'], 'newName': name})
        else:
            name = row['name']
            p = {(t['parameterPower'], tuple(sorted(old_ids[i] for i in t['monomial']))):
                 Q(t['coefficient']) for t in row['terms']}
        assert not any(deleted_coordinates.intersection(m) for a, m in p), name
        p = primitive(p)
        p = {(a, tuple(sorted(mapping[i] for i in m))): c for (a, m), c in p.items()}
        assert max(len(m) for a, m in p) <= 2
        rows.append(dict(row, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not changes, changes
    expanded = {key: c for key, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(coords) == count
    assert len(rows) == (212 if kind == 'inherited' else 81)
    assert gcd(*expanded.values()) == 1
    assert max(len(m) for a, m in expanded) == 4
    assert {i for a, m in expanded for i in m} == set(range(1, count+1))
    parameter = source['fixedParameter']
    system = dict(source, variables=count,
                  source={'construction': path, 'sha256': sha256(raw).hexdigest()},
                  coordinates=coords, residuals=rows)
    polynomial = dict(format='integer-quartic-family-fixed-difference-v18', variables=count,
                      degree=4, inputCoordinate=1, fixedParameter=parameter,
                      coordinates=coords, terms=terms(expanded))
    report = {
        'status': 'Exact polynomial reconstruction; the projection theorem retains all source arithmetic premises and the ineffective sufficient coefficient threshold.',
        'variables': count, 'quadraticResiduals': len(rows), 'degree': 4,
        'content': 1, 'symbolicTerms': len(expanded),
        'ordinaryMonomialsForEveryPositiveParameter': len(profiles),
        'sourceSha256': sha256(raw).hexdigest(),
        'removedSourceCoordinates': sorted(deleted_coordinates),
        'removedSourceRows': sorted(deleted_rows), 'changedRows': changed,
        'field': 'Q(sqrt(2))', 'commonPointFieldCoordinates': ['S', 'T', 'f', 'g'],
        'commonPointQuadraticEquations': 3, 'numeratorPairs': pairs,
        'rationalComponentRowBasis': ROW_BASIS,
        'rationalComponentRowBasisDeterminant': '-1/362963666515968',
        'coordinateSaving': 2+2*pairs,
        'projectionEquivalence': 'The common four-coordinate chart is exactly H and H-P with both finite nonzero abscissas. Direct equations LP_i*K_i=Q_i*T compute the alternate ratios. P is nontorsion, so all exceptional constants are nonzero.'}
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    report['constantCoefficientMaximum'] = str(C)
    report['constantCoefficientMaximumBits'] = C.bit_length()
    if kind == 'inherited':
        assert profiles[(mapping[489], mapping[489])] == {0: 1, 2: 1}
        assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
        L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
        assert C > L*L
        threshold = next(n for n in range(1, 200) if 149**(4*n+2)+1 > C)
        report.update(heightFormulaForEveryPositiveParameter='max(C,A^2+1)',
                      linearCoefficientMultiplierMaximum=L, exactHeightThresholdN=threshold,
                      exactHeightForNAtLeastThreshold='149^(4*N+2)+1',
                      forcedPrime=149)
        suffix = str(count)+'-v18'
        directory = 'family'+str(count)+'_v18'
    else:
        assert set(profiles[()]) == {0, 2} and profiles[()][2] == 1
        constant_term = profiles[()][0]
        assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
        threshold = max(3, isqrt(max(0, C-constant_term)))
        if threshold % 2 == 0:
            threshold += 1
        if threshold*threshold+constant_term < C:
            threshold += 2
        report.update(coefficientHeightForEveryIntegerBAtLeast3=f'max({C},B^2+{constant_term})',
                      constantCoefficientWithoutParameter=str(constant_term),
                      coefficientHeightThresholdOddB=threshold,
                      fixture={'B': 3, 'definesIntegersCertified': False})
        suffix = '-abc'+str(count)+'-v18'
        directory = 'family_abc'+str(count)+'_v18'
    folder = output_root/directory
    folder.mkdir(parents=True, exist_ok=True)
    for name, obj in [('quadratic-family'+suffix+'.json', system),
                      ('polynomial-family'+suffix+'.json', polynomial),
                      ('construction-report'+suffix+'.json', report)]:
        (folder/name).write_text(json.dumps(obj, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
        'ordinaryMonomialsForEveryPositiveParameter', 'constantCoefficientMaximumBits')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=('inherited', 'abc', 'both'), default='both')
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    for kind in ('inherited', 'abc') if args.kind == 'both' else (args.kind,):
        build(kind, args.source_root, args.output_root)
