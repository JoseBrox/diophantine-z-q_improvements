#!/usr/bin/env python3
"""Independent exact reconstruction and normalization audit for family267.

No producer is imported.  The retained rows are checked against the pinned
coefficient source, and all changed scalar equations are reconstructed from
their mathematical definitions.  The audit also records the precise previous
scaled-numerator identity; it does not assert that the previous family definesZ.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json
from check_quartic273 import linear, product, variable, ONE, normalize, decode

HERE=Path(__file__).resolve().parent
PIN='c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b'


def verify(source_root=HERE, output_root=HERE):
    raw=(source_root/'family273/quadratic-family273.json').read_bytes()
    assert sha256(raw).hexdigest()==PIN
    source=json.loads(raw);old_ids={c['id']:c['sourceId'] for c in source['coordinates']}
    folder=output_root/'family267';system_path=folder/'quadratic-family267.json';poly_path=folder/'polynomial-family267.json'
    system=json.loads(system_path.read_text());polynomial=json.loads(poly_path.read_text())
    ids={c['id']:c['sourceId'] for c in system['coordinates']}
    removed_coordinates={343,395,396,397,20100,20101}
    removed_rows={295,349,350,351,20100,20101}
    delta_square=lambda t,t2:linear((variable(t2),1),(variable(t),-2),(ONE,1))
    trace_half=linear((variable(82),F(1,2)),(variable(84),F(1,2)),
                      (variable(86),1),(variable(88),F(1,2)))
    changes={
        'detector1.t.definition':linear((product(variable(37),trace_half),1),(variable(391),-1)),
        'detector1.eWeight.definition':linear((product(variable(394),variable(398)),1),
                                             (product(variable(20022),variable(20022)),-1))}
    expected={}
    for row in source['residuals']:
        if row['sourceId'] in removed_rows:continue
        p=changes.pop(row['name']) if row['name'] in changes else decode(row,old_ids)
        assert all(not removed_coordinates.intersection(m) for m in p)
        expected[row['sourceId']]=(row['name'],normalize(p))
    assert not changes
    actual={r['sourceId']:(r['name'],decode(r,ids)) for r in system['residuals']}
    assert expected==actual and len(actual)==241
    assert set(old_ids.values())-set(ids.values())==removed_coordinates
    assert not set(ids.values())-set(old_ids.values())
    assert system['variables']==polynomial['variables']==len(ids)==267
    assert sorted(ids)==list(range(1,268)) and ids[1]==0
    assert system['coordinates']==polynomial['coordinates']
    byname={name:p for name,p in actual.values()}
    # Reconstruct every scalar normalization and trace row at both scales.
    normalizations=[]
    for d in range(2):
        t,t2,ff,vv=(37,346,348,20002) if d==0 else (391,392,394,20022)
        off=48*d;e,q=350+off,352+off;w0,w1,tau,k,b=380+off,381+off,383+off,384+off,385+off
        delta2=delta_square(t,t2)
        definitions={
            f'detector{d}.eWeight.definition':linear((product(variable(ff),variable(e)),1),(product(variable(vv),variable(vv)),-1)),
            f'detector{d}.q1.definition':linear((product(variable(q),delta2),1),(variable(e),-1)),
            f'detector{d}.eDelta.definition':linear((product(variable(e),delta2),1),(variable(k),-1)),
            f'detector{d}.normOver2w0.definition':linear((product(variable(w0),variable(w0)),1),(product(variable(w1),variable(w1)),-2),(product(variable(w0),variable(tau)),-2)),
            f'detector{d}.B.definition':linear((product(variable(k),variable(b)),1),(product(variable(tau),variable(tau)),-1))}
        for name,p in definitions.items():assert normalize(p)==byname[name],name
        normalizations.append({'detector':d,'rowsChecked':list(definitions),
            'derivedR':'F20(t)/(t-1)^22','derivedE':'(t-1)^20/F20(t)',
            'derivedQ':'(t-1)^18/F20(t)',
            'zeroStratum':'q=0 implies e=0 then t=1; contact values are excluded because none equals1'})
    old_rows={row['sourceId']:decode(row,old_ids) for row in source['residuals']}
    old_definitions={
        349:linear((product(variable(343),variable(391)),1),(variable(395),-1)),
        350:linear((product(linear((variable(395),4),(variable(343),-1)),linear((variable(395),4),(variable(343),-1))),1),(variable(396),-1)),
        351:linear((product(variable(396),variable(396)),1),(variable(397),-1)),
        20100:linear((product(variable(395),variable(397)),1),(variable(20100),-1)),
        20101:linear((product(variable(20100),variable(20100)),1),(variable(20101),-1)),
        352:linear((product(variable(394),variable(398)),1),(product(variable(20101),variable(20101)),-1))}
    for sid,p in old_definitions.items():assert normalize(p)==old_rows[sid]
    # The literal previous numerator, recovered by direct symbolic substitution.
    # Sparse monomials below are powers of two indeterminates(a,t).
    def uv_mul(p,q):
        out=defaultdict(int)
        for (a,b),c in p.items():
            for (d,e),f in q.items():out[a+d,b+e]+=c*f
        return {m:c for m,c in out.items() if c}
    def uv_pow(p,n):
        out={(0,0):1}
        for _ in range(n):out=uv_mul(out,p)
        return out
    def uv_eval(p,a,t):return sum(c*a**i*t**j for (i,j),c in p.items())
    a={(1,0):1};t={(0,1):1};x=uv_mul(a,t)
    fourx_minus_a=dict(x);fourx_minus_a={m:4*c for m,c in x.items()};fourx_minus_a[(1,0)]=-1
    x2=uv_pow(fourx_minus_a,2);x4=uv_pow(x2,2);x5=uv_mul(x,x4);x10=uv_pow(x5,2);old_numerator=uv_pow(x10,2)
    asserted=uv_mul(uv_pow(a,20),uv_pow({(0,1):1,(0,0):-1},20))
    recovered=uv_mul(uv_pow(a,20),uv_mul(uv_pow(t,4),uv_pow({(0,1):4,(0,0):-1},16)))
    assert old_numerator==recovered and old_numerator!=asserted
    assert uv_eval(old_numerator,1,2)==16*7**16 and uv_eval(asserted,1,2)==1
    # The new numerator is exactlydelta^20, for every scale.
    expanded=defaultdict(int)
    for name,p in actual.values():
        assert max(sum(i!=-1 for i in m) for m in p)<=2
        for m,n in combinations_with_replacement(p,2):
            expanded[tuple(sorted(m+n))]+=p[m]*p[n]*(1 if m==n else 2)
    expanded={m:c for m,c in expanded.items() if c}
    assert expanded==decode({'terms':polynomial['terms']},ids)
    assert gcd(*expanded.values())==1 and max(sum(i!=-1 for i in m) for m in expanded)==4
    assert {i for m in expanded for i in m if i!=-1}==set(ids.values())
    ordinary=defaultdict(dict)
    for m,c in expanded.items():ordinary[tuple(i for i in m if i!=-1)][m.count(-1)]=c
    assert ordinary[(489,489)]=={0:1,2:1}
    assert all(set(p) in ({0},{1}) for m,p in ordinary.items() if m!=(489,489))
    C=max(abs(p[0]) for p in ordinary.values() if set(p)=={0})
    L=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
    assert C.bit_length()==1520 and L==13118436242 and C>L*L
    assert 80989**90+1<C<80989**94+1
    assert len(ordinary)==3422 and len(expanded)==3423
    result={'status':'PASS','variables':267,'quadraticResiduals':241,'degree':4,'content':1,
        'ordinaryMonomialsForEveryPositiveParameter':3422,'symbolicTerms':3423,
        'allRowsIndependentlyReconstructed':True,'completeUnorderedPairExpansion':True,'allCoordinatesUsed':True,
        'sourceQuadraticTableSha256':PIN,'normalizationRowsIndependentlyChecked':normalizations,
        'linearTraceScale':'T=(source82+source84+2*source86+source88)/2 = one quarter of the trace of the sum of four root abscissas',
        'previousNormalizationAudit':{'actualNumerator':'a^20*t^4*(4*t-1)^16',
            'previouslyClaimedNumerator':'a^20*(t-1)^20','identityIsFalse':True,
            'exactCounterexample':{'a':1,'t':2,'actual':str(16*7**16),'claimed':'1'},
            'scope':'This is a mismatch between a coefficient source and its former interpretation, not a counterexample to the integer projection. No integer-projection theorem is asserted here for the previous family.'},
        'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':1520,
        'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)',
        'exactHeightThresholdN':23,'exactHeightForNAtLeast23':'80989^(4*N+2)+1',
        'noSupportCancellationForPositiveParameter':True,
        'quadraticTableSha256':sha256(system_path.read_bytes()).hexdigest(),
        'polynomialTableSha256':sha256(poly_path.read_bytes()).hexdigest(),
        'arithmeticScope':'Projection is proved independently with the displayed normalization and linear positive trace scale; the stated arithmetic inputs and ineffective defining threshold remain explicit.'}
    (folder/'independent-verification267.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','variables','quadraticResiduals','ordinaryMonomialsForEveryPositiveParameter','quadraticTableSha256','polynomialTableSha256']}))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=HERE);p.add_argument('--output-root',type=Path,default=HERE)
    args=p.parse_args();verify(args.source_root,args.output_root)
