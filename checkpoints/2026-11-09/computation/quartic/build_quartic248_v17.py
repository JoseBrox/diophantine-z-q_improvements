#!/usr/bin/env python3
"""Exact quartic using a fourth-power scalar norm certificate.

The projection proof uses h(a) <= C M5(a)^3(1+log M5(a)), the
separate forced-prime divisibility, and the sharpened Lucas bound.
The underlying modular, elliptic, prime-pattern and pole inputs remain.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from build_quartic273 import primitive, terms

HERE = Path(__file__).resolve().parent
PIN = '5bf51acf7575c5ed41d364c8716fd3db7644f2ed8711657a5f28d00ac49302c0'
FORCED_PRIME = 149


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family249_v17/quadratic-family249-v17.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    coords = [dict(c,id=i+1) for i,c in enumerate(
        c for c in source['coordinates'] if c['sourceId'] != 602)]
    mapping = {c['sourceId']:c['id'] for c in coords}
    rows = []
    expanded = defaultdict(int)
    changed = []
    for row in source['residuals']:
        if row['sourceId'] == 564:
            continue
        p = defaultdict(Q)
        for term in row['terms']:
            ids = [old_ids[i] for i in term['monomial']]
            if 602 in ids:
                changed.append(row['sourceId'])
            monomial = tuple(sorted(mapping[601 if i == 602 else i] for i in ids))
            coefficient = Q(term['coefficient'])
            if row['sourceId'] == 733 and ids == [489,702]:
                assert coefficient == 80989**2 and term['parameterPower'] == 0
                coefficient = Q(FORCED_PRIME**2)
                changed.append(733)
            p[term['parameterPower'],monomial] += coefficient
        p = primitive({key:c for key,c in p.items() if c})
        name = row['name'].replace('.power8','.power4')
        rows.append(dict(row,id=len(rows)+1,name=name,terms=terms(p)))
        for (a,m),c in p.items():
            for (b,n),d in p.items():
                expanded[a+b,tuple(sorted(m+n))] += c*d
    assert sorted(changed) == [512,566,733]
    expanded = {key:c for key,c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a,m),c in expanded.items():
        profiles[m][a] = c
    assert len(coords) == 248 and len(rows) == 222
    assert max(len(m) for a,m in expanded) == 4 and gcd(*expanded.values()) == 1
    assert {i for a,m in expanded for i in m} == set(range(1,249))
    assert profiles[(mapping[489],mapping[489])] == {0:1,2:1}
    assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert C > L*L
    threshold = next(n for n in range(1,100) if FORCED_PRIME**(4*n+2)+1 > C)
    parameter = dict(source['fixedParameter'],base=FORCED_PRIME)
    system = dict(source,variables=248,
                  source={'construction':'quartic-family249-v17','sha256':PIN},
                  fixedParameter=parameter,coordinates=coords,residuals=rows)
    polynomial = dict(format='integer-quartic-family-v13',variables=248,degree=4,
                      inputCoordinate=1,fixedParameter=parameter,
                      coordinates=coords,terms=terms(expanded))
    report = {
        'status':'Exact quartic specification. The projection theorem uses the proved one-logarithm contact-height bound and the retained modular-realization, elliptic, pole and prime-pattern inputs; no abc conjecture is added.',
        'variables':248,'quadraticResiduals':222,'degree':4,'content':1,
        'ordinaryMonomialsForEveryPositiveParameter':len(profiles),
        'symbolicTerms':len(expanded),'sourceSha256':PIN,
        'removedSourceCoordinates':[602],'removedSourceRows':[564],
        'changedSourceRows':sorted(changed),'literalSourceSubstitutions':{'602':601},
        'forcedPrime':FORCED_PRIME,'forcedPrimeEulerResidues':[59,97,109,108,78],
        'forcedPrimeEulerPowers':[148,148,148,148,148],
        'forcedPrimeNormalizingCoefficient':FORCED_PRIME**2,
        'baseContactHeightBound':'h(a)<=2^330770*M5(a)^3*(1+log(M5(a)))',
        'comparisonContactHeightBound':'h(a)<2^330789*M5(a)^(7/2)',
        'heightExponentOfComparisonContactRadical':'7/4',
        'scalarNormalizationPower':4,'scalarContactIndexOrder':3,
        'scalarForcedIndexDepth':'floor(19*(2*N-1)/8)+1',
        'separateDivisibility':'149^L_N * M5(beta)^3 divides |a-1|',
        'scalarHeightBound':'2^330770*149^(-L_N)*c*(1+log(c)/3)',
        'lucasLowerBound':'log(B)>=(c-5)*log(c-2) for c>=8',
        'scalarRealPreparation':'W=O(R^-3), b_s=O(R^-4) uniformly in the input',
        'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),
        'linearCoefficientMultiplierMaximum':L,
        'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)',
        'exactHeightThresholdN':threshold,
        'exactHeightForNAtLeastThreshold':'149^(4*N+2)+1',
        'effectiveness':'Every sufficiently large N; the sufficient defining threshold remains ineffective.'}
    folder = output_root/'family248_v17'
    folder.mkdir(parents=True,exist_ok=True)
    for name,obj in [('quadratic-family248-v17.json',system),
                     ('polynomial-family248-v17.json',polynomial),
                     ('construction-report248-v17.json',report)]:
        (folder/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('variables','quadraticResiduals','degree',
        'ordinaryMonomialsForEveryPositiveParameter','symbolicTerms',
        'constantCoefficientMaximumBits','exactHeightThresholdN')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root',type=Path,default=HERE)
    parser.add_argument('--output-root',type=Path,default=HERE)
    args = parser.parse_args()
    build(args.source_root,args.output_root)
