#!/usr/bin/env python3
"""Independent semantic reconstruction of the 228,266,and abc91 quartics.

No producer is imported. Changed factor rows are assembled directly in
Q(sqrt(2)) from their mathematical definitions, independently of the
producer's substitution of stored fourth-power equations.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, linear,
    product, variable, scalar, field_mul, field_sum, field_constant)

HERE = Path(__file__).resolve().parent
CONFIG = {
    'inherited': ('family238_v18/quadratic-family238-v18.json',
      'bc97c0d10cd270c2bb856857eaaef7836c4a7a9a0cb039d3cd1e664e0e5db19a',
      'family228_v19', '228-v19', 228, 202, 2829),
    'explicit': ('family276_v19/quadratic-family276-v19.json',
      'c191e1b87651b6b14903a90092a13adf02803c6266274beea4477f6c3a3b5587',
      'family266_v19', '266-v19', 266, 238, 3474),
    'abc': ('family_abc93_v18/quadratic-family-abc93-v18.json',
      '82a409221257575b74406868532c5662323e6ab33afa11a6e41087baeb6ce1b0',
      'family_abc91_v19', '-abc91-v19', 91, 79, 926),
}
COPIED_IDS = [38,39,40,41,346,347,348,352,360,361,362,380,381,383,385,386,388,390,20000]+list(range(22000,22016))


def pair(i, imaginary_factor=1):
    return variable(i), linear((imaginary_factor, variable(i+1)))


def times(s, value):
    return tuple(product(s, component) for component in value)


def inherited_factors(q, r1, r2, r4, outputs):
    # These are the source's actual field values; several stored second
    # components are half the coefficient of sqrt(2).
    B = [pair(i, -2) for i in (178,190,196,208,220)]
    G2 = (linear((1, variable(319)), (-2, variable(253)), (1, scalar(1))),
          linear((4, variable(320)), (-4, variable(254))))
    factors = [
        field_sum((1, times(q, pair(313,2))), (1, times(r2, pair(311,2))),
                  (1, field_mul(B[1],B[1]))),
        field_sum((1, times(q, G2)), (1, times(r2, pair(259,2))),
                  (1, field_mul(B[0],B[0]))),
        field_sum((1, times(q, pair(21002))), (1, times(r1, pair(257,2))),
                  (1, times(r2, pair(261,2))), (1, field_mul(B[3],B[3]))),
        field_sum((1, times(q, pair(315,2))), (1, times(r2, pair(21000))),
                  (1, field_mul(B[4],B[4]))),
        field_sum((1, times(q, pair(317,2))), (1, times(r2, pair(255,2))),
                  (1, field_mul(B[2],B[2]))),
    ]
    rows = []
    for output, factor in zip(outputs, factors):
        difference = field_sum((1, (r4, {})), (1, factor),
                               (-1, times(r4, (variable(output), variable(output+1)))))
        rows.extend(canonical(component) for component in difference)
    return rows


def verify_valuation_residues():
    # The finite residue checks certify the disjoint valuation classes;
    # the inequalities below use exact rational numbers, not a finite
    # approximation to all possible p-adic valuations.
    for nu in (1,3,5,7):
        for even in (0,2,4,6):
            assert (2*even-2*nu)%4 == 2
            assert (4*even-4*nu)%8 == 4
            assert (2*even-3*nu)%4 == nu%4
        for arbitrary in range(8):
            assert (2*arbitrary-5*nu)%2 == 1
            assert (4*arbitrary-5*nu)%4 == (-nu)%4
            assert (4*arbitrary-2*nu)%4 == 2
        assert nu%4 != (-nu)%4
    assert (5-Q(1,2))/2 == Q(9,4) > 2
    assert (5-Q(1,2))/4 == Q(9,8) > 1
    assert (3-Q(1,2))/2 == Q(5,4) > 0
    assert (2-Q(1,2))/2 == Q(3,4) > 0
    assert (2-Q(1,2))/4 == Q(3,8) > 0
    assert (4-Q(1,2))/4 == Q(7,8) > 0
    # Formal error is order4; the three deep test terms have positive
    # valuation at all selected simple contacts in complete witnesses.
    assert 2*4-5 > 0 and 2*2-3 > 0 and 4*2-4 > 0
    return True


def verify(kind, source_root=HERE, output_root=HERE):
    path,pin,directory,suffix,count,row_count,monomial_count = CONFIG[kind]
    raw = (source_root/path).read_bytes()
    assert sha256(raw).hexdigest() == pin
    old = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    root = output_root/directory
    system_raw = (root/('quadratic-family'+suffix+'.json')).read_bytes()
    quartic_raw = (root/('polynomial-family'+suffix+'.json')).read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(quartic_raw)
    report = json.loads((root/('construction-report'+suffix+'.json')).read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    assert list(ids) == list(range(1,count+1))
    assert system['variables'] == polynomial['variables'] == report['variables'] == count
    assert system['coordinates'] == polynomial['coordinates']
    expected_parameter = dict(old['fixedParameter'])
    if kind == 'explicit':
        expected_parameter['N'] = 'Every integer N>=14521; this effective sufficient threshold uses the abscissa-sum height theorem.'
    assert system['fixedParameter'] == polynomial['fixedParameter'] == expected_parameter
    changes, extra = {}, []
    if kind == 'abc':
        removed = {30002,30003,30004,30005}
        removed_rows = {f'{which}Numerator.fourthPower.{j}.definition'
                        for which in ('primary','alternate') for j in (0,1)}
        assert list(ids.values()) == [x for x in old_ids.values() if x not in removed]+[51000,51001]
        for j,q in enumerate((30010,30032)):
            r2,r3,r4 = map(variable, (q+3,51000+j,q+4))
            prefix = f'detector{j}.'
            changes[prefix+'weightSquared.definition'] = canonical(linear((1,product(variable(q),r4)),(-1,r3)))
            changes[prefix+'weightFourthPower.definition'] = canonical(linear((1,product(r2,r2)),(-1,r4)))
            extra.append(canonical(linear((1,product(variable(q),r3)),(-1,r2))))
            right_sides = [
                field_sum((1,(r4,{})), (1,times(r3,pair(305,2))),
                          (1,times(r2,pair(311,2))), (1,field_mul(pair(255,2),pair(255,2)))),
                field_sum((1,(r4,{})), (1,times(r3,pair(30000))),
                          (1,times(r2,pair(178,-2))), (1,field_mul(pair(190,-2),pair(190,-2)))),
            ]
            for k,right in enumerate(right_sides):
                equation = field_sum((1,right), (-1,times(r4,pair(q+5+2*k))))
                for component in range(2):
                    changes[prefix+f'factor{k}.{component}.definition'] = canonical(equation[component])
    else:
        removed = {180,181,198,199,210,211,222,223,21004,21005}
        removed_rows = {f'logV{i}.wPower2.{j}.definition' for i in (0,2,3,4) for j in (0,1)}
        removed_rows |= {'residue.V1.power4.0.definition','residue.V1.power4.1.definition'}
        assert list(ids.values()) == [x for x in old_ids.values() if x not in removed]
        copied = dict(zip(COPIED_IDS,range(50000,50035)))
        detectors = [(352,360,361,362,list(range(22000,22010,2))),
                     (400,408,409,410,list(range(22030,22040,2)))]
        if kind == 'explicit':
            detectors.append(tuple(copied[x] for x in (352,360,361,362))+
                             ([copied[x] for x in range(22000,22010,2)],))
        for j,(q,r1,r2,r4,outputs) in enumerate(detectors):
            prefix = f'detector{j}.'
            changes[prefix+'E1.power2.definition'] = canonical(linear((1,product(variable(q),variable(r1))),(-1,scalar(1))))
            changes[prefix+'E1.power4.definition'] = canonical(linear((1,product(variable(r1),variable(r1))),(-1,variable(r2))))
            changes[f'reflected.{prefix}weightPower7.definition'] = canonical(linear((1,product(variable(r2),variable(r2))),(-1,variable(r4))))
            factor_rows = inherited_factors(*map(variable,(q,r1,r2,r4)),outputs)
            for k,p in enumerate(factor_rows):
                changes[f'residue.det{j}.factor{k//2}.{k%2}.definition'] = p
    assert sorted(removed) == report['removedSourceCoordinates']
    assert removed_rows == set(report['removedSourceRows'])
    expected,unchanged,changed = [],0,0
    for row in old['residuals']:
        name = row['name']
        if name in removed_rows:
            continue
        if name in changes:
            expected.append(changes.pop(name));changed += 1
        else:
            expected.append(canonical(decode(row,old_ids)));unchanged += 1
    assert not changes
    expected += extra
    actual = [decode(row,ids) for row in system['residuals']]
    assert len(actual) == row_count and actual == expected
    assert all(max(sum(x != PARAMETER for x in m) for m in p)<=2 for p in actual)
    expanded = linear(*((1,product(p,p)) for p in actual))
    assert expanded == decode(polynomial,ids)
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert max(sum(x != PARAMETER for x in m) for m in expanded)==4
    assert {x for m in expanded for x in m if x != PARAMETER}==set(ids.values())
    profiles = defaultdict(dict)
    for m,c in expanded.items():
        profiles[tuple(x for x in m if x!=PARAMETER)][m.count(PARAMETER)]=int(c)
    assert len(profiles)==monomial_count==report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded)==monomial_count+1==report['symbolicTerms']
    assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
    C=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    L=max(abs(p[1]) for p in profiles.values() if set(p)=={1})
    assert str(C)==report['constantCoefficientMaximum'] and L==report['linearCoefficientMultiplierMaximum']
    certificate = {
        'status':'PASS','variables':count,'quadraticRows':row_count,'degree':4,'content':1,
        'ordinaryMonomialsForEveryPositiveParameter':monomial_count,'symbolicTerms':len(expanded),
        'sourceSha256':pin,'systemSha256':sha256(system_raw).hexdigest(),
        'polynomialSha256':sha256(quartic_raw).hexdigest(),
        'unchangedSourceRowsComparedExactly':unchanged,'changedRowsReconstructedFromFieldFormulas':changed,
        'addedReciprocalRowsReconstructed':len(extra),'removedSharedFieldFourthPowers':len(removed)//2,
        'arithmeticScope':'Coefficient identities and stated finite or integer checks are certified; the defining theorem uses the separately proved arithmetic hypotheses and zero-stratum analysis.'}
    if kind=='abc':
        offset=profiles[()][0]
        assert profiles[()][2]==1
        assert report['coefficientHeightForEveryIntegerBAtLeast3']==f'max({C},B^2+{offset})'
        assert C==4153456 and offset==797683
        threshold=report['coefficientHeightThresholdOddB']
        assert threshold%2 and threshold**2+offset>=C and (threshold-2)**2+offset<C
        certificate.update(coefficientHeight=f'max({C},B^2+{offset})',
                           coefficientHeightThresholdOddB=threshold)
    else:
        assert profiles[(489,489)]=={0:1,2:1}
        assert C>L*L and 149**214+1>C>149**210+1
        assert verify_valuation_residues()
        assert Q(4)*Q(7,6)/3==Q(14,9)<2
        certificate.update(heightFormula='max(C,A^2+1);149^(4*N+2)+1 for N>=53',
                           comparisonPrecision=3,valuationResidueCertificate=True,
                           contactHeightExponent='7/6',residualGrowthExponent='14/9')
        if kind=='explicit':
            N=14521;depth=19*(2*N-1)//8+1;c=149**depth
            H,H2=1<<221234,1<<221284
            assert depth==68973 and 5**18<14**11
            assert (c-1)**4>(14*H2)**9 and c>40*H and c>40*265546
            previous=149**(19*(2*(N-1)-1)//8+1)
            assert (previous-1)**4<=(14*H2)**9
            assert 2029147<2**21 and (1<<221283)+2<H2
            assert 149**3>10*(1+149**2) and 25*(10+9792)<17*10**5
            height=149**58086+1
            assert height.bit_length()==419333
            certificate.update(definingThresholdN=N,forcedIndexDepth=depth,
                               specifiedParameter='149^29043',specifiedCoefficientHeight='149^58086+1',
                               specifiedCoefficientHeightBinaryDigits=419333,
                               integerThresholdChecks={'lucasResidual':True,'scalarHeight':True,
                               'inputHeightAdditiveTerm':True,'realCompleteness':True,
                               'previousNDoesNotMeetThisSufficientCriterion':True})
    (root/('independent-verification'+suffix+'.json')).write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps(certificate,sort_keys=True))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kind',choices=(*CONFIG,'all'),default='all')
    parser.add_argument('--source-root',type=Path,default=HERE)
    parser.add_argument('--output-root',type=Path,default=HERE)
    args=parser.parse_args()
    for kind in CONFIG if args.kind=='all' else (args.kind,):
        verify(kind,args.source_root,args.output_root)
