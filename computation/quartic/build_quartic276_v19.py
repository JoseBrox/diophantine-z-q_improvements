#!/usr/bin/env python3
"""Construct the explicit three-scale quartic from the current quadratic source.

The effective sum-height inequality uses the three scales 1,S0^2,(S0+S1)^2.
All local factors and their exceptional strata are retained exactly. The
new modular contact-height bound supplies the certified parameter N=7745.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCE = 'family238_v18/quadratic-family238-v18.json'
PIN = 'bc97c0d10cd270c2bb856857eaaef7836c4a7a9a0cb039d3cd1e664e0e5db19a'


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    detector = [c for c in source['coordinates'] if any(token in c['name']
                for token in ('detector0.', 'amplified.det0.'))]
    assert len(detector) == 35
    detector_ids = {c['sourceId'] for c in detector}
    copied = {c['sourceId']: 50000+i for i, c in enumerate(detector)}
    copied[37] = 49000
    coordinates = [dict(c) for c in source['coordinates']]
    for sid, name in ((49001, 'height.firstSquareScale'),
                      (49002, 'height.secondSquareScale'),
                      (49000, 'detector2.argument')):
        coordinates.append({'id': len(coordinates)+1, 'sourceId': sid, 'name': name, 'kind': 'gate'})
    for c in detector:
        coordinates.append(dict(c, id=len(coordinates)+1, sourceId=copied[c['sourceId']],
                                copiedSourceId=c['sourceId'],
                                name=c['name'].replace('detector0.', 'detector2.').replace('.det0.', '.det2.')))
    assert len(coordinates) == 276
    mapping = {c['sourceId']: c['id'] for c in coordinates}
    assembled, duplicated_rows = [], []
    for row in source['residuals']:
        p = {(t['parameterPower'], tuple(sorted(old_ids[x] for x in t['monomial']))):
             Q(t['coefficient']) for t in row['terms']}
        if row['sourceId'] == 345:
            p = add(mul(v(37), v(49001)), scale(v(391), -1))
            name = 'detector1.firstSquareScale.argument'
        else:
            name = row['name']
        assembled.append((dict(row, name=name), primitive(p)))
        if any(detector_ids.intersection(m) for _, m in p):
            q = {(a, tuple(sorted(copied.get(x, x) for x in m))): c for (a, m), c in p.items()}
            duplicated_rows.append((dict(row, sourceId=60000+len(duplicated_rows),
                copiedSourceId=row['sourceId'],
                name=row['name'].replace('detector0.', 'detector2.').replace('.det0.', '.det2.')),
                primitive(q)))
    assert len(duplicated_rows) == 33
    S0 = add(v(82), v(84), scale(v(86), 2), v(88))
    S1 = scale(add(v(83), v(85), v(87), v(89)), 2)
    extra = [
        ({'sourceId': 61000, 'name': 'height.firstSquareScale.definition'},
         primitive(add(mul(S0, S0), scale(v(49001), -1)))),
        ({'sourceId': 61001, 'name': 'height.secondSquareScale.definition'},
         primitive(add(mul(add(S0, S1), add(S0, S1)), scale(v(49002), -1)))),
        ({'sourceId': 61002, 'name': 'detector2.argument.definition'},
         primitive(add(mul(v(49002), v(37)), scale(v(49000), -1)))),
    ]
    rows, expanded = [], defaultdict(int)
    for metadata, p in assembled+extra+duplicated_rows:
        p = {(a, tuple(sorted(mapping[x] for x in m))): c for (a, m), c in p.items()}
        assert max(len(m) for _, m in p) <= 2
        rows.append(dict(metadata, id=len(rows)+1, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    expanded = {m: c for m, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(rows) == 248 and gcd(*expanded.values()) == 1
    assert max(len(m) for _, m in expanded) == 4
    assert {x for _, m in expanded for x in m} == set(range(1, 277))
    assert profiles[(mapping[489], mapping[489])] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert C > L*L and 149**214+1 > C > 149**210+1
    parameter = 7745
    depth = 19*(2*parameter-1)//8+1
    c = 149**depth
    H, H2 = 1 << 221234, 1 << 221284
    assert depth == 36787 and (c-1)**5 > (12*H2)**6
    assert c > 40*H and c > 40*265546
    assert 149**3 > 10*(1+149**2)
    parameter_description = dict(source['fixedParameter'],
        N='Every integer N>=7745; this effective sufficient threshold uses the abscissa-sum height theorem.')
    system = dict(source, format='integer-quadratic-family-three-scales-v19', variables=276,
                  source={'construction': SOURCE, 'sha256': PIN}, fixedParameter=parameter_description,
                  coordinates=coordinates, residuals=rows)
    polynomial = dict(format='integer-quartic-family-three-scales-v19', variables=276, degree=4,
                      inputCoordinate=1, fixedParameter=parameter_description,
                      coordinates=coordinates, terms=terms(expanded))
    report = {
        'status': 'Exact algebraic specification and effective parameter certificate under the retained arithmetic premises and proved modular height refinement.',
        'variables': 276, 'quadraticResiduals': 248, 'degree': 4, 'content': 1,
        'symbolicTerms': len(expanded), 'ordinaryMonomialsForEveryPositiveParameter': len(profiles),
        'sourceSha256': PIN, 'scales': ['1', 'S0^2', '(S0+S1)^2'],
        'S0': 'x82+x84+2*x86+x88', 'S1': '2*(x83+x85+x87+x89)',
        'newSourceCoordinates': [c['sourceId'] for c in coordinates[238:]],
        'copiedSourceCoordinates': {str(k): v for k, v in copied.items() if k != 37},
        'copiedSourceRows': [r['copiedSourceId'] for r, _ in duplicated_rows],
        'changedSourceRows': [345], 'newScaleAndArgumentRows': [61000, 61001, 61002],
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'linearCoefficientMultiplierMaximum': L,
        'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 53, 'exactHeightForNAtLeastThreshold': '149^(4*N+2)+1',
        'baseContactHeightConstant': '2^221234', 'baseContactHeightExponent': '7/3',
        'tenContactHeightConstantUpperBound': '2^221284', 'tenContactHeightExponent': '7/6',
        'comparisonPrecision': 4, 'inputPrecision': 1,
        'definingThresholdN': parameter, 'forcedIndexDepthAtThreshold': depth,
        'specifiedParameter': '149^15491', 'specifiedCoefficientHeight': '149^30982+1',
        'specifiedCoefficientHeightBinaryDigits': (149**30982+1).bit_length(),
        'soundnessIntegerCertificates': {
            'lucasContradiction': '(149^36787-1)^5 > (12*2^221284)^6',
            'scalarHeight': '149^36787 > 40*2^221234',
            'additiveHeight': '149^36787 > 40*265546',
        },
        'completenessRealBound': 'For |Z0|,|Z1|<=1 and |Norm(f(H))|<=1/7, W_s<5/R_s^3; b_s<=25*(R_s+9792)/R_s^5<17 for R_s>=10. R_s>=149^(2N+1)/(1+149^2)>10 for N>=1.',
    }
    output = output_root/'family276_v19'
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [('quadratic-family276-v19.json', system),
                           ('polynomial-family276-v19.json', polynomial),
                           ('construction-report276-v19.json', report)]:
        (output/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
          'ordinaryMonomialsForEveryPositiveParameter', 'definingThresholdN',
          'specifiedCoefficientHeightBinaryDigits')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    build(args.source_root, args.output_root)
