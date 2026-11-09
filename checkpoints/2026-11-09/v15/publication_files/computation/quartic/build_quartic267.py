#!/usr/bin/env python3
"""An even contact polynomial permits a normalization independent of the scale.

This reconstructs a 267-coordinate family from the pinned 273 table,
using the positive trace itself as the second scale.  The
projection proof is given independently for R=F20(t)/(t-1)^22; it is not an
assertion of equivalence with every witness in the prior normalization.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from build_quartic273 import primitive, terms

HERE = Path(__file__).resolve().parent
PIN = 'c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b'
DELETED = {343, 395, 396, 397, 20100, 20101}
DELETED_ROWS = {295, 349, 350, 351, 20100, 20101}


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family273/quadratic-family273.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    coordinates = [dict(c, id=i+1) for i,c in
                   enumerate(c for c in source['coordinates'] if c['sourceId'] not in DELETED)]
    mapping = {c['sourceId']: c['id'] for c in coordinates}
    residuals, expanded = [], defaultdict(int)
    changed = []
    for row in source['residuals']:
        if row['sourceId'] in DELETED_ROWS: continue
        p = {(t['parameterPower'], tuple(sorted(old_ids[i] for i in t['monomial']))):
             Fraction(int(t['coefficient'])) for t in row['terms']}
        if row['name'] == 'detector1.t.definition':
            p = {(0, (37,82)): Fraction(1), (0, (37,84)): Fraction(1),
                 (0, (37,86)): Fraction(2), (0, (37,88)): Fraction(1),
                 (0, (391,)): Fraction(-2)}
            changed.append(row['sourceId'])
        if row['name'] == 'detector1.eWeight.definition':
            p = {(0, (394,398)): Fraction(1), (0, (20022,20022)): Fraction(-1)}
            changed.append(row['sourceId'])
        assert all(not DELETED.intersection(m) for a,m in p)
        p = primitive(p)
        p = {(a, tuple(sorted(mapping[i] for i in m))): c for (a,m),c in p.items()}
        assert max(len(m) for a,m in p) <= 2
        residuals.append(dict(row, terms=terms(p)))
        for (a,m),c in p.items():
            for (b,n),d in p.items(): expanded[a+b,tuple(sorted(m+n))] += c*d
    assert changed == [345,352]
    expanded = {m:c for m,c in expanded.items() if c}
    ordinary = defaultdict(dict)
    for (a,m),c in expanded.items(): ordinary[m][a] = c
    assert len(coordinates) == 267 and len(residuals) == 241
    assert gcd(*expanded.values()) == 1 and max(len(m) for a,m in expanded) == 4
    assert {i for a,m in expanded for i in m} == set(range(1,268))
    assert ordinary[(mapping[489],mapping[489])] == {0:1,2:1}
    assert all(set(p) in ({0},{1},{0,2}) for p in ordinary.values())
    C = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    L = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert C.bit_length() == 1520 and L == 13118436242 and C > L*L
    assert 80989**90+1 < C < 80989**94+1
    system = dict(source, format='integer-quadratic-family-v10', variables=267,
                  source={'construction':'quartic-family273','sha256':PIN},
                  coordinates=coordinates,residuals=residuals)
    polynomial = {'format':'integer-quartic-family-v10','variables':267,'degree':4,
                  'inputCoordinate':1,'fixedParameter':source['fixedParameter'],
                  'coordinates':coordinates,'terms':terms(expanded)}
    report = {'status':'Exact polynomial specification; projection proved with a normalization independent of the positive rational scale.',
              'variables':267,'quadraticResiduals':241,'degree':4,'content':1,
              'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'symbolicTerms':len(expanded),
              'sourceSha256':PIN,'removedSourceCoordinates':sorted(DELETED),
              'removedSourceRows':sorted(DELETED_ROWS),'changedSourceRows':changed,
              'detectorNormalization':{'contactDegree':20,'R':'F20(t)/(t-1)^22',
                  'e':'(t-1)^20/F20(t)','q':'(t-1)^18/F20(t)',
                  'clearingEquations':['F20(t)*e=V10(t)^2','q*(t-1)^2=e','traceScale=e*(t-1)^2'],
                  'scales':['1','T'],'T':'one quarter of the trace of the sum of four root abscissas',
                  'fixedPlaceFormulas':{'v(e)':'0','v(q)':'-2*v(t)','v(R)':'-2*v(t)'},
                  'realAsymptotic':'R~q~t^(-2); pole input~1/(4*t^2)'},
              'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':1520,
              'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)',
              'exactHeightThresholdN':23,'exactHeightForNAtLeast23':'80989^(4*N+2)+1',
              'effectiveness':'Every sufficiently large N under the stated arithmetic premises; no numerical sufficient threshold is asserted.'}
    output = output_root/'family267';output.mkdir(parents=True,exist_ok=True)
    for filename,data in [('quadratic-family267.json',system),('polynomial-family267.json',polynomial),('construction-report267.json',report)]:
        (output/filename).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['variables','quadraticResiduals','degree','ordinaryMonomialsForEveryPositiveParameter','symbolicTerms']}))


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=HERE);p.add_argument('--output-root',type=Path,default=HERE)
    args=p.parse_args();build(args.source_root,args.output_root)
