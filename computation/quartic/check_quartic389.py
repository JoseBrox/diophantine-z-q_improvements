#!/usr/bin/env python3
"""Independent exact coefficient, deletion, local-algebra and height checker."""
from pathlib import Path
from fractions import Fraction
from math import gcd,isqrt
from collections import defaultdict
import gzip,hashlib,json

HERE=Path(__file__).resolve().parent

def parse(terms):
    result={}
    for t in terms:
        key=(int(t['parameterPower']),tuple(t['monomial']))
        assert key not in result
        result[key]=int(t['coefficient'])
    return result

def expand(rows):
    result=defaultdict(int)
    for r in rows:
        items=list(parse(r['terms']).items())
        for i,((e,m),c) in enumerate(items):
            for j in range(i,len(items)):
                (f,n),d=items[j]
                result[e+f,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
    return {k:v for k,v in result.items() if v}

def main():
    base={}
    for name,pin in [('quadratic-system392','b66609c16f649481ea8edb14785af2fb6f9da151f76d75dfa203f9db189e93a0'),
                     ('polynomial392','65f978c8b6418395535816a485093213631623766024555c69ef5db6c185450d')]:
        raw=gzip.decompress((HERE/'baseline392'/(name+'.json.gz')).read_bytes())
        assert hashlib.sha256(raw).hexdigest()==pin
        base[name]=json.loads(raw)
    old=base['quadratic-system392']
    assert expand(old['residuals'])==parse(base['polynomial392']['terms'])
    src_rows={r['sourceId']:r for r in old['residuals']}
    deleted={334:(219,221),384:(248,250),434:(277,279)}
    removed={pair[1] for pair in deleted.values()}
    for sid,(w,v) in deleted.items():
        assert parse(src_rows[sid]['terms'])=={(0,()):1,(0,(w,v)):-1}
        appearances=[r['sourceId'] for r in old['residuals']
                     if any(v in t['monomial'] for t in r['terms'])]
        assert appearances==[sid]
    # The remaining half-trace equations force W=0 if its rational part vanishes.
    for sid,(w,v) in deleted.items():
        assert parse(src_rows[sid+1]['terms'])=={
             (0,(w,w)):1,(0,(w,w+3)):-2,(0,(w+1,w+1)):-2}
    ir=json.loads((HERE/'final389/quadratic-system389.json').read_text())
    poly=json.loads((HERE/'final389/polynomial389.json').read_text())
    assert ir['variables']==poly['variables']==389
    assert len(ir['coordinates'])==389 and len(ir['residuals'])==361
    retained=[c for c in old['coordinates'] if c['id'] not in removed]
    mapping={c['id']:i+1 for i,c in enumerate(retained)}
    assert ir['coordinates']==[dict(c,id=mapping[c['id']]) for c in retained]
    assert poly['coordinates']==ir['coordinates']
    expected=[]
    for row in old['residuals']:
        if row['sourceId'] in deleted:continue
        terms=[dict(t,monomial=[mapping[v] for v in t['monomial']]) for t in row['terms']]
        expected.append(dict(row,terms=terms))
    assert ir['residuals']==expected
    coefficients=expand(expected)
    assert coefficients==parse(poly['terms'])
    assert max(map(lambda k:len(k[1]),coefficients))==4
    assert gcd(*coefficients.values())==1
    assert {v for e,m in coefficients for v in m}==set(range(1,390))
    # Independent difference: precisely three guard squares disappear.
    removed_square=expand([src_rows[s] for s in deleted])
    old_poly=parse(base['polynomial392']['terms'])
    difference={k:c-removed_square.get(k,0) for k,c in old_poly.items()}
    difference={k:c for k,c in difference.items() if c}
    assert not any(set(m)&removed for e,m in difference)
    renumbered={(e,tuple(mapping[v] for v in m)):c for (e,m),c in difference.items()}
    assert coefficients==renumbered
    # Every collision or exceptional contact difference has small prime support.
    theta=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
    for a in theta:
        for b in theta+[Fraction(1)]:
            if a==b:continue
            d=a-b
            num=abs(d.numerator)
            for p in range(2,isqrt(num)+1):
                if num%p==0:
                    assert p<=76176
                    while num%p==0:num//=p
            assert num<=76176
            # A denominator product is supported on2,2399,407.
            den=d.denominator
            for p in (2,11,37,2399):
                while den%p==0:den//=p
            assert den==1
    # Integer valuations of a unit and an odd-valuation square multiple cannot tie.
    for nu in range(1,100,2):
        for m in (1,10,40):
            for val in range(-120,121):
                assert (nu+2*(val-m*nu))%2==1
    ordinary=defaultdict(dict)
    for (e,m),c in coefficients.items():ordinary[m][e]=c
    a=80989**54929
    specialized={m:sum(c*a**e for e,c in d.items()) for m,d in ordinary.items()}
    maximum=max(specialized,key=lambda m:abs(specialized[m]))
    assert maximum==() and specialized[maximum]>0
    assert specialized[maximum].bit_length()==1791357
    assert len(ordinary)==6198 and len(coefficients)==6219
    assert all(specialized.values())
    # The largest coefficient is the old largest coefficient minus three.
    old_constant=sum(c*a**e for (e,m),c in old_poly.items() if not m)
    assert specialized[()]==old_constant-3
    report={'status':'passed','variables':389,'quadraticResiduals':361,'degree':4,
        'ordinaryMonomials':6198,'symbolicTerms':6219,'content':1,
        'largestCoefficientBitLength':1791357,'heightChange':'old maximum minus3',
        'sourceSOSChecked':True,'everyRetainedRowChecked':True,
        'everyCoefficientCheckedTwoWays':True,'soleUseInverseCoordinatesChecked':True,
        'normalizedHalfTraceRowsChecked':True,
        'scope':'Exact finite identities and coefficient assertions. The complete prime-by-prime proof, including empty contact radicals, is mathematical and stated separately.',
        'polynomialSHA256':hashlib.sha256((HERE/'final389/polynomial389.json').read_bytes()).hexdigest(),
        'systemSHA256':hashlib.sha256((HERE/'final389/quadratic-system389.json').read_bytes()).hexdigest()}
    (HERE/'final389/independent-verification389.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
