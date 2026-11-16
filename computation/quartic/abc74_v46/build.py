#!/usr/bin/env python3
"""Exact producer for the 74-coordinate weighted pair-product family."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd, lcm
import argparse
import importlib.util
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PARENT=ROOT/'computation/quartic/abc76_v44/quadratic-family.json'
PARENT_SHA256='5f03efc8629210d3da25f7b2fad6428ea4f8f288d806bd32f26a87954bc012e8'
SPEC=importlib.util.spec_from_file_location('abc76_producer', ROOT/'computation/quartic/abc76_v44/build.py')
OPS=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OPS)
add,scale,multiply,square,variable=(getattr(OPS,n) for n in ('add','scale','multiply','square','variable'))
kplus,ktimes,ksquare,kminus,rational,field,conjugate=(getattr(OPS,n) for n in ('kplus','ktimes','ksquare','kminus','rational','field','conjugate'))
ONE={(0,()):Q(1)}
PARAM={(1,()):Q(1)}
D=(scale(ONE,11),scale(ONE,-6))

def serialize(p):
    return [dict(parameterPower=j,monomial=list(m),coefficient=str(c))
            for (j,m),c in sorted(p.items())]

def build(output):
    raw=PARENT.read_bytes()
    assert sha256(raw).hexdigest()==PARENT_SHA256, 'Pinned parent table changed'
    parent=json.loads(raw)
    deleted={f'detector{j}.inverseWeightSquare' for j in range(2)} | {'height.inputFourth'}
    rename={f'detector{j}.poleScaledInput':f'detector{j}.poleInput' for j in range(2)}
    rename['height.inputSquare']='height.betaSquare'
    names=[rename.get(c['name'],c['name']) for c in parent['coordinates'] if c['name'] not in deleted]
    names.append('height.betaFourth')
    ids={n:i+1 for i,n in enumerate(names)}
    oldnames={c['id']:c['name'] for c in parent['coordinates']}
    changes={}
    f,h,g,k,s=(field(n) for n in ('pair.f','pair.h','pair.g','pair.k','pair.slope'))
    FU,FV,FH,GH=(field(n) for n in ('square.pair.f','square.pair.g','square.common.f','square.common.g'))
    L,L0,S,TH=(field(n) for n in ('ratio.primary','ratio.alternate','common.S','common.T'))
    C2,I2=field('square.comparison'),field('square.input')
    b2,b4,T=(variable(n) for n in ('height.betaSquare','height.betaFourth','height.trace'))
    changes['height.inputSquare']=add(scale(b2,4),scale(square(variable('input')),-1))
    tangent=kplus(ktimes(s,kminus(h,k)),rational(scale(b4,-1)),ktimes(D,kplus(FU,ktimes(f,g),FV)))
    primary=kplus(ktimes(kminus(rational(b4),ktimes(D,FU)),L),ktimes(h,S))
    alternate=kplus(ktimes(kminus(rational(b4),ktimes(D,FV)),L0),ktimes(k,TH))
    input_square=kminus(I2,ksquare(kminus(L,rational(ONE))))
    for i in range(2):
        changes[f'pair.tangent.{i}']=tangent[i]
        changes[f'ratio.primary.regular.{i}']=primary[i]
        changes[f'ratio.alternate.regular.{i}']=alternate[i]
        changes[f'square.input.{i}']=input_square[i]
    trace=kplus(ksquare(s),ktimes(D,kplus(f,g)))[0]
    changes['height.trace']=add(multiply(b2,T),scale(trace,-2))
    changes['detector1.argument']=add(variable('detector1.argument'),scale(variable('slope'),-1),scale(PARAM,-1),scale(square(b4),-1),scale(square(T),-1))
    extra=('height.betaFourth',add(b4,scale(square(b2),-1)))

    for j in range(2):
        prefix=f'detector{j}.'
        w=variable(prefix+'inverseWeight')
        eta=variable(prefix+'trace')
        pole_b=variable(prefix+'poleInput')
        e,u,v=(variable(prefix+'pole.'+n) for n in ('e','u','v'))
        for number,comp,ref,point in ((1,C2,FH,FU),(2,I2,conjugate(GH),conjugate(FV))):
            A=field(prefix+f'factor{number}')
            rhs=kplus(rational(square(w)),ktimes(rational(w),comp),ktimes(ref,point))
            row=kminus(ktimes(rational(w),A),rhs)
            for i in range(2): changes[prefix+f'factor{number}.{i}']=row[i]
        product=kminus(ktimes(rational(w),field(prefix+'product')),
                       ktimes(field(prefix+'factor1'),field(prefix+'factor2')))
        for i in range(2): changes[prefix+f'product.{i}']=product[i]
        changes[prefix+'poleScaledInput']=add(multiply(w,pole_b),scale(square(eta),-1))
        changes[prefix+'pole.factor']=add(multiply(u,v),scale(e,-1),multiply(e,pole_b))

    def primitive(p):
        p={(j,tuple(sorted(ids[n] for n in m))):Q(c) for (j,m),c in p.items() if c}
        den=lcm(*(c.denominator for c in p.values()))
        content=gcd(*(int(den*c) for c in p.values()))
        if p[min(p)]<0: content=-content
        return {m:int(den*c/content) for m,c in p.items()}

    rows=[]
    retained=[]
    for row in parent['residuals']:
        name=row['name']
        if name in deleted: continue
        if name in changes: p=changes[name]
        else:
            p={(t['parameterPower'],tuple(sorted(rename.get(oldnames[i],oldnames[i]) for i in t['monomial']))):Q(t['coefficient']) for t in row['terms']}
            retained.append(name)
        p=primitive(p)
        assert max(len(m) for _,m in p)<=2
        rows.append(dict(id=len(rows)+1,name=rename.get(name,name),terms=serialize(p)))
    rows.append(dict(id=len(rows)+1,name=extra[0],terms=serialize(primitive(extra[1]))))
    assert len(names)==74 and len(rows)==64
    expanded=defaultdict(int)
    for row in rows:
        p={(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in row['terms']}
        for m,c in square(p).items():
            assert c.denominator==1
            expanded[m]+=int(c)
    expanded={m:c for m,c in expanded.items() if c}
    assert max(len(m) for _,m in expanded)==4
    assert expanded[0,(1,1,1,1)]==1
    assert gcd(*expanded.values())==1
    assert {i for _,m in expanded for i in m}==set(range(1,75))
    profiles=defaultdict(dict)
    for (j,m),c in expanded.items(): profiles[m][j]=c
    constant=profiles[()]
    fixedmax=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    assert set(constant)=={0,2} and constant[2]==1
    for p in profiles.values():
        if 1 in p:
            assert abs(p[1])<=2
            assert p[1]*p.get(0,0)>=0
            assert constant[0]>=abs(p.get(0,0))+1
        elif 2 in p: assert p==constant
    coordinates=[dict(id=i+1,name=n) for i,n in enumerate(names)]
    system=dict(format='integer-quadratic-family-pair-product74-v46',variables=74,inputCoordinate=1,
                fixedParameter=parent['fixedParameter'],coordinates=coordinates,residuals=rows,
                parentQuadraticSha256=sha256(raw).hexdigest(),deletedCoordinates=sorted(deleted),
                coordinateConvention='beta=X/2; beta=0 is a permitted degenerate integral-input stratum. Pair f,g are beta^2-scaled; h,k beta^3-scaled; slope beta-scaled; pair squares beta^4-scaled; ratios are divided by beta. Pole inputs are native b=w*tau^2.')
    polynomial=dict(format='integer-quartic-family-pair-product74-v46',variables=74,degree=4,inputCoordinate=1,
                    fixedParameter=parent['fixedParameter'],coordinates=coordinates,terms=serialize(expanded))
    report=dict(status='PROVED_CONDITIONAL_FAMILY_EXACT_ALGEBRA',variables=74,quadraticRows=64,degree=4,
                integerContentForEveryPositiveB=1,ordinaryMonomialsForEveryPositiveB=len(profiles),
                parameterSeparatedTerms=len(expanded),constantCoefficient=str(constant[0]),
                largestFixedCoefficient=str(fixedmax),exactHeight=f'max({fixedmax},B^2+{constant[0]})',
                parentQuadraticSha256=sha256(raw).hexdigest(),changedRows=sorted(changes),
                retainedRows=retained,removedRows=sorted(deleted),addedRows=[extra[0]],
                physicalPoleInput='b=w*(Norm(T1*T2)/Trace(T1*T2))^2',
                inputMap='beta=X/2; beta=0 is treated separately',heightScale='B+beta^8+T^2',
                localResidual='beta*(n-beta)',heightAbsorption='602/679',
                zeroWeight='For X!=0, impossible by paired raw/regular ratios; X=0 is already an integral input.',
                scope='Defining family under ordinary rational abc and the retained elliptic-group, simultaneous-prime, trace-height and congruent-number pole inputs stated in the companion paper. The sufficient fixed odd B threshold is ineffective. No full rational zero-set equivalence with the parent76 family is claimed.')
    output.mkdir(parents=True,exist_ok=True)
    for filename,obj in [('quadratic-family.json',system),('polynomial-family.json',polynomial),('construction-report.json',report)]:
        (output/filename).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE)
    build(parser.parse_args().output)
