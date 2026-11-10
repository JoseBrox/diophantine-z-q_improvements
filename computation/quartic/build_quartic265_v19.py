#!/usr/bin/env python3
"""Four comparison factors for the effective three-detector quartic."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add,scale,mul,fm,primitive,terms,v,one

HERE=Path(__file__).resolve().parent
SOURCE='family266_v19/quadratic-family266-v19.json'
PIN='23bb7d627672beecdbe2b7d833158b1c720fd30326d7bc97fceecd5518665e3c'


def pair(i,k=1):
    return v(i),scale(v(i+1),k)


def fadd(*values):
    return tuple(add(*(x[i] for x in values)) for i in range(2))


def fscale(value,c):
    return tuple(scale(x,c) for x in value)


def scalar_times(s,value):
    return tuple(mul(s,x) for x in value)


def build(source_root=HERE,output_root=HERE):
    raw=(source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest()==PIN
    source=json.loads(raw)
    old_ids={c['id']:c['sourceId'] for c in source['coordinates']}
    copied={c['copiedSourceId']:c['sourceId'] for c in source['coordinates'] if 'copiedSourceId' in c}
    detectors=[(352,360,361,362,22000,22010,22012,380),
               (400,408,409,410,22030,22040,22042,428),
               tuple(copied[x] for x in (352,360,361,362,22000,22010,22012,380))]
    removed=set()
    for _,_,_,_,f,_,p,_ in detectors:
        removed.update((f+8,f+9,p+2,p+3))
    assert len(removed)==12
    coords=[dict(c) for c in source['coordinates'] if c['sourceId'] not in removed]
    additions=[]
    squares=[pair(313,2),
             (add(v(319),scale(v(253),-2),one),scale(add(v(320),scale(v(254),-1)),4)),
             pair(315,2),pair(317,2)]
    for j,(name,value) in enumerate(zip(('C2','G','C3','C4'),squares)):
        output=80000+2*j
        fourth=fm(value,value)
        for k in range(2):
            coords.append({'sourceId':output+k,'name':f'comparison.{name}.fourthPower.{k}','kind':'gate'})
            additions.append(({'sourceId':82000+2*j+k,'name':f'comparison.{name}.fourthPower.{k}.definition'},
                              add(fourth[k],scale(v(output+k),-1))))
    changes={}
    for j,(q,r1,r2,r4,f,p1,p2,W) in enumerate(detectors):
        w=81000+j
        coords.append({'sourceId':w,'name':f'detector{j}.weightFifthPower','kind':'gate'})
        additions.append(({'sourceId':83000+j,'name':f'detector{j}.weightFifthPower.definition'},
                          add(mul(v(w),v(r4)),scale(v(q),-1))))
        right_sides=[
            fadd(scalar_times(v(w),pair(80000)),scalar_times(v(r1),pair(21000)),
                 scalar_times(v(r2),pair(311,2)),fm(pair(190,-2),pair(190,-2))),
            fadd(scalar_times(v(w),pair(80002)),scalar_times(v(r1),pair(259,2)),
                 scalar_times(v(r2),pair(178,-2)),fm(pair(196,-2),pair(196,-2))),
            fadd(scalar_times(v(w),pair(80004)),scalar_times(v(r1),pair(257,2)),
                 scalar_times(v(r2),pair(21002)),fm(pair(208,-2),pair(208,-2))),
            fadd(scalar_times(v(w),pair(80006)),scalar_times(v(r1),pair(255,2)),
                 scalar_times(v(r2),pair(261,2)),fm(pair(220,-2),pair(220,-2))),
        ]
        for k,rhs in enumerate(right_sides):
            value=fadd((v(r4),{}),rhs,fscale(scalar_times(v(r4),pair(f+2*k)),-1))
            for a in range(2):
                changes[f'residue.det{j}.factor{k}.{a}.reciprocal.definition']=(
                    f'fourFactors.det{j}.factor{k}.{a}.definition',value[a])
        final=fadd(fm(pair(p2),pair(f+6)),fscale(pair(W),-1))
        for k in range(2):
            changes[f'amplified.det{j}.product4.{k}.definition']=(
                f'fourFactors.det{j}.product3.{k}.definition',final[k])
    for i,c in enumerate(coords):c['id']=i+1
    ids={c['sourceId']:c['id'] for c in coords}
    assert len(coords)==265
    assembled=[];removed_rows=[];changed=[]
    for row in source['residuals']:
        name=row['name']
        if any(name in (f'residue.det{j}.factor4.{k}.reciprocal.definition',
                        f'amplified.det{j}.product3.{k}.definition')
               for j in range(3) for k in range(2)):
            removed_rows.append(name);continue
        p={(t['parameterPower'],tuple(sorted(old_ids[x] for x in t['monomial']))):Q(t['coefficient']) for t in row['terms']}
        if name in changes:
            new_name,p=changes.pop(name)
            changed.append({'sourceId':row['sourceId'],'oldName':name,'newName':new_name})
            name=new_name
        assert not any(removed.intersection(m) for _,m in p)
        assembled.append((dict(row,name=name),p))
    assert not changes and len(removed_rows)==12
    rows=[];expanded=defaultdict(int)
    for metadata,p in assembled+additions:
        p=primitive(p)
        p={(a,tuple(sorted(ids[x] for x in m))):c for (a,m),c in p.items()}
        assert max(len(m) for _,m in p)<=2
        rows.append(dict(metadata,id=len(rows)+1,terms=terms(p)))
        for (a,m),c in p.items():
            for (b,n),d in p.items():expanded[a+b,tuple(sorted(m+n))]+=c*d
    expanded={m:c for m,c in expanded.items() if c}
    profiles=defaultdict(dict)
    for (a,m),c in expanded.items():profiles[m][a]=c
    assert len(rows)==237 and gcd(*expanded.values())==1
    assert max(len(m) for _,m in expanded)==4
    assert {x for _,m in expanded for x in m}==set(range(1,266))
    assert profiles[(ids[489],ids[489])]=={0:1,2:1}
    assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
    C=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    L=max(abs(p[1]) for p in profiles.values() if set(p)=={1})
    assert C>L*L and 149**210+1<C<149**214+1
    fixed_parameter=dict(source['fixedParameter'],
        N='Every integer N>=9682; this effective sufficient threshold retains the logarithmic contact-height factor.')
    system=dict(source,format='integer-quadratic-family-four-factors-v19',variables=265,
                source={'construction':SOURCE,'sha256':PIN},fixedParameter=fixed_parameter,coordinates=coords,residuals=rows)
    quartic=dict(format='integer-quartic-family-four-factors-v19',variables=265,degree=4,
                 inputCoordinate=1,fixedParameter=fixed_parameter,coordinates=coords,terms=terms(expanded))
    report={
        'status':'Exact four-factor construction under the retained arithmetic premises and proved modular multiplicity height refinement.',
        'variables':265,'quadraticResiduals':237,'degree':4,'content':1,
        'ordinaryMonomialsForEveryPositiveParameter':len(profiles),'symbolicTerms':len(expanded),
        'sourceSha256':PIN,'removedSourceCoordinates':sorted(removed),'removedSourceRows':removed_rows,
        'changedRows':changed,'newFourthPowerSourceCoordinates':list(range(80000,80008)),
        'newWeightSourceCoordinates':[81000,81001,81002],
        'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),
        'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)',
        'exactHeightThresholdN':53,'exactHeightForNAtLeastThreshold':'149^(4*N+2)+1',
        'factorsPerDetector':4,'comparisonPrecision':3,'inputPrecision':1,
        'deepComparisonValuationStrictLowerBound':'17*nu/8',
        'scalarWeights':['q^-1','q^-2','q^-4','q^5'],'scales':['1','S0^2','(S0+S1)^2'],
        'baseContactHeightConstant':'2^221234','baseContactHeightExponent':'7/3',
        'tenContactHeightConstantUpperBound':'2^221274','tenContactHeightExponent':'1 with (22+log(M)/2)^2',
        'definingThresholdN':9682,'forcedIndexDepthAtThreshold':45988,
        'specifiedParameter':'149^19365','specifiedCoefficientHeight':'149^38730+1',
        'specifiedCoefficientHeightBinaryDigits':279599,
        'coordinateCountIdentity':'266+8+3-12=265',
        'arithmeticScope':'Full normalized modular realization, retained elliptic, pole and simultaneous-prime inputs; effective abscissa-sum height theorem. No additional abc hypothesis.',
    }
    folder=output_root/'family265_v19';folder.mkdir(parents=True,exist_ok=True)
    for name,data in [('quadratic-family265-v19.json',system),('polynomial-family265-v19.json',quartic),
                      ('construction-report265-v19.json',report)]:
        (folder/name).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('variables','quadraticResiduals','degree','ordinaryMonomialsForEveryPositiveParameter')}))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=HERE)
    p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
    build(a.source_root,a.output_root)
