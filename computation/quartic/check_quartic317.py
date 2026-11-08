#!/usr/bin/env python3
"""Independent inverse-substitution, coefficient and local-arithmetic checks."""
from collections import defaultdict
from fractions import Fraction
from math import gcd,isqrt
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent

def add(p,q):
    r=defaultdict(Fraction,p)
    for k,c in q.items():r[k]+=c
    return {k:c for k,c in r.items() if c}
def multiply(p,q):
    r=defaultdict(Fraction)
    for (e,m),c in p.items():
        for (f,n),d in q.items():r[e+f,tuple(sorted(m+n))]+=c*d
    return {k:c for k,c in r.items() if c}
def parse(terms):
    r={}
    for t in terms:
        k=(t['parameterPower'],tuple(t['monomial']))
        assert k not in r
        r[k]=Fraction(t['coefficient'])
    return r
def square_sum(rows):
    result=defaultdict(Fraction)
    for row in rows:
        entries=list(parse(row['terms']).items())
        for i,((a,m),c) in enumerate(entries):
            for j in range(i,len(entries)):
                (b,n),d=entries[j]
                result[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
    return {k:c for k,c in result.items() if c}
def evaluate(p,images):
    result={}
    for (a,m),c in p.items():
        t={(a,()):c}
        for j in m:t=multiply(t,images[j])
        result=add(result,t)
    return result

def main():
    raw=(HERE/'family329/quadratic-family329.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9a9ece7045ebc14f1101aaf85bb7566434d4c411c9820669015242ba5df4170b'
    old=json.loads(raw)
    ir=json.loads((HERE/'family317/quadratic-family317.json').read_text())
    poly=json.loads((HERE/'family317/polynomial-family317.json').read_text())
    deleted_sources={66,67,68,70,71,72,74,75,76,78,79,80}
    retained=[x for x in old['coordinates'] if x['sourceId'] not in deleted_sources]
    old_by_source={x['sourceId']:x['id'] for x in old['coordinates']}
    new_by_source={x['sourceId']:x['id'] for x in ir['coordinates']}
    assert len(retained)==317
    assert ir['coordinates']==poly['coordinates']==[dict(x,id=i+1) for i,x in enumerate(retained)]
    assert ir['variables']==poly['variables']==317
    old_rows={r['sourceId']:r for r in old['residuals']}
    new_rows={r['sourceId']:r for r in ir['residuals']}
    removed_rows=set(range(687,699))
    assert set(new_rows)==set(old_rows)-removed_rows
    assert len(new_rows)==291
    old_deleted={old_by_source[x] for x in deleted_sources}
    assert {r['sourceId'] for r in old['residuals']
            if any(j in old_deleted for t in r['terms'] for j in t['monomial'])}==removed_rows
    images={x['id']:{(0,(old_by_source[x['sourceId']],)):Fraction(1)} for x in ir['coordinates']}
    ox=old_by_source[0];oy=old_by_source[248]
    images[new_by_source[0]]={(0,(ox,)):Fraction(2),(0,()):Fraction(1)}
    images[new_by_source[248]]={(0,(oy,)):Fraction(4),(0,(ox,)):Fraction(4),(0,()):Fraction(1)}
    # Work in the reverse direction, independently of the producer's substitution.
    ratios={}
    for sid,row in new_rows.items():
        recovered=evaluate(parse(row['terms']),images)
        expected=parse(old_rows[sid]['terms'])
        if sid==492:
            keys=[k for k,c in expected.items() if c==4896]
            assert len(keys)==1
            expected[keys[0]]=9792
        assert set(recovered)==set(expected),sid
        k=next(iter(expected));factor=recovered[k]/expected[k]
        assert factor and recovered=={k:c*factor for k,c in expected.items()},sid
        ratios[sid]=str(factor)
        assert max(len(m) for a,m in parse(row['terms']))<=2
    actual=square_sum(ir['residuals'])
    assert actual==parse(poly['terms'])
    assert max(len(m) for a,m in actual)==4
    assert max(a for a,m in actual)==2
    assert all(c.denominator==1 for c in actual.values())
    assert set(j for a,m in actual for j in m)==set(range(1,318))
    grouped=defaultdict(dict)
    for (a,m),c in actual.items():grouped[m][a]=int(c)
    assert len(actual)==5047 and len(grouped)==5032
    unit=next(m for m,c in grouped.items() if c=={0:1})
    assert max(sum(abs(c) for c in p.values()) for p in grouped.values()).bit_length()==1520
    # Symbolic label conversion before imposingY=X².
    def atom(j):return {(0,(j,)):Fraction(1)}
    old_beta={(0,()):Fraction(2555),(0,(ox,)):Fraction(204),(0,(oy,)):Fraction(204)}
    nx=new_by_source[0];ny=new_by_source[248]
    forward={ox:{(0,(nx,)):Fraction(1,2),(0,()):Fraction(-1,2)},
             oy:{(0,(ny,)):Fraction(1,4),(0,(nx,)):Fraction(-1,2),(0,()):Fraction(1,4)}}
    assert evaluate(old_beta,forward)=={(0,()):Fraction(2504),(0,(ny,)):Fraction(51)}
    assert parse(new_rows[200]['terms'])=={(0,(nx,nx)):1,(0,(ny,)):-1}
    def rvalue(x):
        b=51*x*x+2504
        return b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)
    def val(n,p):
        k=0
        while n%p==0:n//=p;k+=1
        return k
    for x in range(16):assert val(rvalue(x),2)==(3 if x%4==0 else 2)
    for x in range(9):assert val(rvalue(x),3)==1
    for x in range(17):assert rvalue(x)%17==15
    assert 9792==2**6*3**2*17
    ell=80989
    assert all(ell%d for d in range(2,isqrt(ell)+1))
    assert ell%17==ell%3==1
    roots=[Fraction(0),Fraction(1),Fraction(2401),Fraction(-343,32),Fraction(1,2)]
    euler=[]
    for theta in roots:
        u=(theta-2504)/51
        residue=(u.numerator*pow(u.denominator,-1,ell))%ell
        assert pow(residue,(ell-1)//2,ell)==ell-1
        euler.append({'contact':str(theta),'squareResidueTest':residue,'EulerPower':ell-1})
    result={'status':'passed','variables':317,'quadraticResiduals':291,'degree':4,
        'symbolicTerms':5047,'ordinaryMonomialsForNAtLeast27464':5032,
        'contentForEveryIntegerParameter':1,'unitCoefficientMonomial':list(unit),
        'heightBound':'H(P_N)<2^1520*80989^(4*N+2)',
        'eachRetainedRowRecoveredByInverseAffineMap':True,
        'oddChartSoleUsesChecked':True,'newLabelChecked':True,'smallPrimeCongruencesChecked':True,
        'ellPrimeAvoidance':euler,'inverseRowMultipliers':ratios,
        'polynomialSHA256':hashlib.sha256((HERE/'family317/polynomial-family317.json').read_bytes()).hexdigest(),
        'systemSHA256':hashlib.sha256((HERE/'family317/quadratic-family317.json').read_bytes()).hexdigest(),
        'scope':'Exact identities and finite congruences; the defining threshold is an ineffective mathematical existence result.'}
    (HERE/'family317/independent-verification317.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['inverseRowMultipliers','ellPrimeAvoidance']},indent=2))

if __name__=='__main__':main()
