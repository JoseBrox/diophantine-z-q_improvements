#!/usr/bin/env python3
"""Independent exact verification of the two-scale quartic family."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from math import gcd
import hashlib,json

HERE=Path(__file__).resolve().parent

def parse(terms):
    out={}
    for t in terms:
        k=(t['parameterPower'],tuple(t['monomial']))
        assert k not in out
        out[k]=int(t['coefficient'])
    return out
def square(rows):
    out=defaultdict(int)
    for row in rows:
        p=list(parse(row['terms']).items())
        for i,((a,m),c) in enumerate(p):
            for j in range(i,len(p)):
                (b,n),d=p[j]
                out[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
    return {k:c for k,c in out.items() if c}

def main():
    raw=(HERE/'final389/quadratic-system389.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394'
    old=json.loads(raw)
    ir=json.loads((HERE/'family329/quadratic-family329.json').read_text())
    p=json.loads((HERE/'family329/polynomial-family329.json').read_text())
    # Specify the removed source-coordinate ranges independently of gate names.
    discarded_sources={46,47,48,49,337,338,339,340,341,342,344,345}
    discarded_sources.update(range(439,487))
    discarded_sources.update(range(674,694))
    old_coordinates=[x for x in old['coordinates'] if x['sourceId'] not in discarded_sources]
    mapping={x['id']:i+1 for i,x in enumerate(old_coordinates)}
    assert len(old['coordinates'])-len(old_coordinates)==60
    assert len(old_coordinates)==329
    expected_coordinates=[]
    for x in old_coordinates:
        name='aggregateTrace.quarterSquare' if x['sourceId']==343 else x['name']
        expected_coordinates.append(dict(x,id=mapping[x['id']],name=name))
    assert ir['coordinates']==p['coordinates']==expected_coordinates
    source_to_new={x['sourceId']:x['id'] for x in ir['coordinates']}
    expected_rows=[];removed_rows=[]
    for row in old['residuals']:
        if row['sourceId']==295:
            trace={82:1,84:1,86:2,88:1};rowterms=defaultdict(int)
            for x,c in trace.items():
                for y,d in trace.items():rowterms[tuple(sorted((source_to_new[x],source_to_new[y])))]+=c*d
            rowterms[(source_to_new[343],)]=-4
            terms=[{'parameterPower':0,'monomial':list(m),'coefficient':str(c)} for m,c in sorted(rowterms.items())]
            expected_rows.append(dict(row,name='aggregateTrace.quarterSquare.definition',terms=terms))
        elif any(v not in mapping for t in row['terms'] for v in t['monomial']):
            removed_rows.append(row)
        else:
            expected_rows.append(dict(row,terms=[dict(t,monomial=[mapping[v] for v in t['monomial']]) for t in row['terms']]))
    assert len(expected_rows)==303
    assert ir['residuals']==expected_rows
    coeff=square(expected_rows)
    assert coeff==parse(p['terms'])
    # Second route: subtract old squares and insert the new scale square.
    old_poly=json.loads((HERE/'final389/polynomial389.json').read_text())
    assert square(old['residuals'])==parse(old_poly['terms'])
    old_scale=next(r for r in old['residuals'] if r['sourceId']==295)
    sub=square(removed_rows+[old_scale]);difference=parse(old_poly['terms'])
    for k,c in sub.items():difference[k]=difference.get(k,0)-c
    difference={k:c for k,c in difference.items() if c}
    assert all(v in mapping for a,m in difference for v in m)
    renumbered={(a,tuple(mapping[v] for v in m)):c for (a,m),c in difference.items()}
    inserted=next(r for r in expected_rows if r['sourceId']==295)
    for k,c in square([inserted]).items():renumbered[k]=renumbered.get(k,0)+c
    assert coeff=={k:c for k,c in renumbered.items() if c}
    assert max(len(m) for a,m in coeff)==4
    assert max(a for a,m in coeff)==2
    assert set(v for a,m in coeff for v in m)==set(range(1,330))
    grouped=defaultdict(dict)
    for (a,m),c in coeff.items():grouped[m][a]=c
    assert len(grouped)==5294 and len(coeff)==5315
    # A constant coefficient of one, independent of A, certifies content one.
    unit_monomial=next(m for m,c in grouped.items() if c=={0:1})
    factor=max(sum(abs(c) for c in p.values()) for p in grouped.values())
    assert factor.bit_length()==1520
    # A>2^1521 makes the leading A term dominate every lower term.
    # The published anchor exponent already exceeds this sufficient cutoff.
    assert (80989**54929).bit_length()>1521
    assert ir['fixedParameter']==p['fixedParameter']
    assert ir['fixedParameter']['exponent']=='2*N+1'
    # The modified scale row equals F^2-4*s; its consumers are unchanged.
    retained_sources={r['sourceId']:r for r in expected_rows}
    old_by_source={r['sourceId']:r for r in old['residuals']}
    for sid in list(range(345,355))+[385,386,387]:
        if sid not in old_by_source:continue
        assert retained_sources[sid]['terms']==[
            dict(t,monomial=[mapping[v] for v in t['monomial']])
            for t in old_by_source[sid]['terms']]
    report={'status':'passed','variables':329,'quadraticResiduals':303,'degree':4,
        'ordinaryMonomialsForNAtLeast27464':5294,'symbolicTerms':5315,
        'contentForEveryIntegerParameter':1,'unitCoefficientMonomial':list(unit_monomial),
        'coefficientHeightBound':'H(P_N)<2^1520*80989^(4*N+2)',
        'completeCoefficientTableCheckedTwoWays':True,'everyRetainedRowChecked':True,
        'newTraceScaleChecked':True,'definingParameterThreshold':'Ineffective; the computation does not establish it.',
        'polynomialSHA256':hashlib.sha256((HERE/'family329/polynomial-family329.json').read_bytes()).hexdigest(),
        'systemSHA256':hashlib.sha256((HERE/'family329/quadratic-family329.json').read_bytes()).hexdigest()}
    (HERE/'family329/independent-verification329.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
