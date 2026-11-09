#!/usr/bin/env python3
"""A quartic source using the proved contact-height exponent seven halves.

Two reflected contact blocks, plain parameter ratios, three local weight
outputs, and an eighth-power scalar normalization give 249 coordinates.
The construction retains the elliptic, prime-pattern and pole premises.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from build_quartic273 import add, scale, mul, fm, primitive, terms, v, one, pmul

HERE = Path(__file__).resolve().parent
PIN = 'bf123dd6decac657ca8c0c567fb7f58d7289860567e387b70f86c03ae2c1be9d'
DELETED_COORDINATES = {188, 189, 359, 369, 407, 417, 603, 604, 20001, 20021}
DELETED_ROWS = {140, 141, 541, 546, 547, 552, 559, 561, 20001, 20021}
SUBSTITUTIONS = {369: 361, 417: 409, 604: 602}


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family259_v17/quadratic-family259-v17.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    theta = [Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407)]
    contacts = sorted(theta+[2-x for x in theta])
    assert len(set(contacts)) == 10 and 0 in contacts and 1 not in contacts
    squared = sorted({(t-1)**2 for t in contacts})
    assert len(squared) == 5
    contact = [Q(1)]
    for root in squared:
        contact = pmul(contact, [-root, Q(1)])

    changes, renames = {}, {}
    for d in range(2):
        r, r2, ff, r3, q, q2, q4, q3, q7 = ((346,347,348,20000,352,361,362,359,360)
              if d == 0 else (392,393,394,20020,400,409,410,407,408))
        prefix = 'reflected.detector'+str(d)
        base = {0: one, 1: v(r), 2: v(r2), 3: v(r3)}
        value = []
        for power, coefficient in enumerate(contact):
            a, b = next((a,b) for a in base for b in base if a+b == power)
            value.append(scale(mul(base[a],base[b]), coefficient))
        changes[300+48*d] = (prefix+'.contactPolynomial.definition', add(*value, scale(v(ff),-1)))
        changes[20000+20*d] = (prefix+'.deltaSixthPower.definition', add(mul(v(r),v(r2)),scale(v(r3),-1)))
        changes[304+50*d] = (prefix+'.weight.definition', add(mul(v(ff),add(one,v(q))),scale(mul(v(r2),v(r3)),-1)))
        changes[526+7*d] = (prefix+'.weightPower7.definition', add(mul(v(q),v(q7)),scale(mul(v(q4),v(q4)),-1)))
        renames.update({r3:prefix+'.deltaSixthPower',q3:prefix+'.weightPower3',q7:prefix+'.weightPower7'})

    # z(H-P)=N/D0 on the admissible point chart, after multiplication
    # of numerator and denominator by the same unit 3+2*sqrt(2).
    S=(v(142),v(143)); g=(v(700),v(701))
    numerator=(add(scale(one,-312),scale(S[0],-236),scale(S[1],-240)),
               add(scale(one,-69),scale(S[0],-120),scale(S[1],-236)))
    denominator=(add(scale(one,-576),scale(S[0],312),scale(S[1],138),scale(g[0],504),scale(g[1],-2688)),
                 add(scale(one,-256),scale(S[0],69),scale(S[1],312),scale(g[0],-1344),scale(g[1],504)))
    for i in range(4):
        ratio=(v(234+4*i),v(235+4*i)); z=(v(164+4*i),v(165+4*i))
        left=fm(ratio,numerator); right=fm(z,denominator)
        for j in range(2):
            changes[146+12*i+j]=(f'plain.alternateRatio{i+1}.cleared.{j}',add(left[j],scale(right[j],-1)))

    coords=[dict(c,id=i+1,name=renames.get(c['sourceId'],c['name'])) for i,c in
            enumerate(c for c in source['coordinates'] if c['sourceId'] not in DELETED_COORDINATES)]
    mapping={c['sourceId']:c['id'] for c in coords}
    rows, changed=[],[]
    expanded=defaultdict(int)
    for row in source['residuals']:
        sid=row['sourceId']
        if sid in DELETED_ROWS:
            continue
        if sid in changes:
            name,p=changes.pop(sid)
            changed.append(sid)
        else:
            name=row['name']
            p={}
            for term in row['terms']:
                monomial=tuple(sorted(SUBSTITUTIONS.get(old_ids[i],old_ids[i]) for i in term['monomial']))
                key=(term['parameterPower'],monomial)
                p[key]=p.get(key,Q(0))+Q(term['coefficient'])
            p={key:c for key,c in p.items() if c}
            if any(old_ids[i] in SUBSTITUTIONS for term in row['terms'] for i in term['monomial']):
                changed.append(sid)
                if sid in (512,566): name=name+'.power8'
        assert not any(DELETED_COORDINATES.intersection(m) for a,m in p),name
        p=primitive(p)
        p={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in p.items()}
        assert max(len(m) for a,m in p)<=2
        rows.append(dict(row,id=len(rows)+1,name=name,terms=terms(p)))
        for (a,m),c in p.items():
            for (b,n),e in p.items(): expanded[a+b,tuple(sorted(m+n))]+=c*e
    assert not changes,changes
    expanded={key:c for key,c in expanded.items() if c}
    ordinary=defaultdict(dict)
    for (a,m),c in expanded.items():ordinary[m][a]=c
    assert len(coords)==249 and len(rows)==223,(len(coords),len(rows))
    assert gcd(*expanded.values())==1 and max(len(m) for a,m in expanded)==4
    assert {i for a,m in expanded for i in m}==set(range(1,250))
    assert ordinary[(mapping[489],mapping[489])]=={0:1,2:1}
    assert all(set(p) in ({0},{1},{0,2}) for p in ordinary.values())
    C=max(abs(p[0]) for p in ordinary.values() if set(p)=={0})
    L=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
    assert C>L*L
    threshold=next(n for n in range(1,100) if 80989**(4*n+2)+1>C)
    system=dict(source,format='integer-quadratic-family-v13',variables=249,
                source={'construction':'quartic-family259-v17','sha256':PIN},coordinates=coords,residuals=rows)
    polynomial={'format':'integer-quartic-family-v13','variables':249,'degree':4,'inputCoordinate':1,
                'fixedParameter':source['fixedParameter'],'coordinates':coords,'terms':terms(expanded)}
    report={'status':'Exact quartic specification. The projection theorem uses the proved contact-height bound and the retained elliptic, pole and prime-pattern inputs; no abc conjecture is added.',
            'variables':249,'quadraticResiduals':223,'degree':4,'content':1,
            'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'symbolicTerms':len(expanded),
            'sourceSha256':PIN,'removedSourceCoordinates':sorted(DELETED_COORDINATES),
            'removedSourceRows':sorted(DELETED_ROWS),'changedSourceRows':sorted(changed),
            'literalSourceSubstitutions':{str(k):vv for k,vv in SUBSTITUTIONS.items()},
            'contacts':[str(x) for x in contacts],'squaredDistancesFromOne':[str(x) for x in squared],
            'degreeFivePolynomialCoefficients':[str(x) for x in contact],
            'newExceptionalPrimes':[2029147],
            'baseContactHeightBound':'h(a)<2^330789*M5(a)^(7/2)',
            'heightExponentOfContactRadical':'7/4',
            'normalization':{'R':'F10(t)/(t-1)^10','q':'(t-1)^10/F10(t)-1',
                 'contactEquation':'F10*(1+q)=r^2*r^3','poleEquation':'(1+q)*b=(408/409)^2*tau^2'},
            'weightRelations':['q2=q^2','q4=q2^2','q*q7=q4^2'],
            'requiredOrders':{'C2_C3_C4_G':4,'I':2,'H':2,'C1':1,'otherReciprocalAbscissas':1},
            'formalApproximation':'Plain z=-x/y at every comparison point; relative error order4.',
            'scalarNormalizationPower':8,'scalarContactIndexOrder':6,
            'scalarHeightExponent':'7/12','scalarForcedIndexDepth':'floor(43*(2*N-1)/8)+1',
            'lucasGrowthExponent':'7/4',
            'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),
            'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)',
            'exactHeightThresholdN':threshold,'exactHeightForNAtLeastThreshold':'80989^(4*N+2)+1',
            'effectiveness':'Every sufficiently large N; the sufficient defining threshold remains ineffective.'}
    folder=output_root/'family249_v17';folder.mkdir(parents=True,exist_ok=True)
    for name,obj in [('quadratic-family249-v17.json',system),('polynomial-family249-v17.json',polynomial),('construction-report249-v17.json',report)]:
        (folder/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('variables','quadraticResiduals','degree','ordinaryMonomialsForEveryPositiveParameter','symbolicTerms','constantCoefficientMaximumBits','exactHeightThresholdN')}))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path,default=HERE);parser.add_argument('--output-root',type=Path,default=HERE)
    args=parser.parse_args();build(args.source_root,args.output_root)
