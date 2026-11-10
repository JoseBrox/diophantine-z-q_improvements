#!/usr/bin/env python3
"""Independent field-formula, coefficient and threshold audit for265."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER,canonical,decode,linear,product,
                                       variable,scalar,field_mul,field_sum)

HERE=Path(__file__).resolve().parent
PIN='23bb7d627672beecdbe2b7d833158b1c720fd30326d7bc97fceecd5518665e3c'


def f(i,k=1):
    return variable(i),linear((k,variable(i+1)))


def sf(i,value):
    return tuple(product(variable(i),part) for part in value)


def verify(source_root=HERE,output_root=HERE):
    raw=(source_root/'family266_v19/quadratic-family266-v19.json').read_bytes()
    assert sha256(raw).hexdigest()==PIN
    old=json.loads(raw);old_ids={c['id']:c['sourceId'] for c in old['coordinates']}
    folder=output_root/'family265_v19'
    system_raw=(folder/'quadratic-family265-v19.json').read_bytes()
    polynomial_raw=(folder/'polynomial-family265-v19.json').read_bytes()
    system=json.loads(system_raw);polynomial=json.loads(polynomial_raw)
    report=json.loads((folder/'construction-report265-v19.json').read_text())
    ids={c['id']:c['sourceId'] for c in system['coordinates']}
    removed={22008,22009,22014,22015,22038,22039,22044,22045,50027,50028,50033,50034}
    assert list(ids)==list(range(1,266))
    assert list(ids.values())==[x for x in old_ids.values() if x not in removed]+list(range(80000,80008))+[81000,81001,81002]
    assert system['variables']==polynomial['variables']==report['variables']==265
    assert system['coordinates']==polynomial['coordinates']
    assert system['fixedParameter']==polynomial['fixedParameter']
    assert {k:v for k,v in system['fixedParameter'].items() if k!='N'}=={k:v for k,v in old['fixedParameter'].items() if k!='N'}
    assert system['fixedParameter']['N'].startswith('Every integer N>=9682;')
    # Direct expressions for the four shared comparison squares, including
    # the source's affine G-square coordinate and half imaginary components.
    G2=(linear((1,variable(319)),(-2,variable(253)),(1,scalar(1))),
        linear((4,variable(320)),(-4,variable(254))))
    powers=[]
    for k,p in enumerate((f(313,2),G2,f(315,2),f(317,2))):
        square=field_mul(p,p)
        for j in range(2):powers.append(canonical(linear((1,square[j]),(-1,variable(80000+2*k+j)))))
    blocks=[(352,360,361,362,22000,22012,380),
            (400,408,409,410,22030,22042,428),
            (50007,50008,50009,50010,50019,50031,50011)]
    changes={};weight_rows=[]
    for j,(q,r1,r2,r4,base,partial,W) in enumerate(blocks):
        fifth=81000+j
        weight_rows.append(canonical(linear((1,product(variable(fifth),variable(r4))),(-1,variable(q)))))
        # Each row below is reconstructed from the intended four-factor
        # formula, not by substituting any producer expression.
        specifications=[(80000,21000,1,311,2,190),
                        (80002,259,2,178,-2,196),
                        (80004,257,2,21002,1,208),
                        (80006,255,2,261,2,220)]
        for k,(deep,middle,mult1,low,mult2,last) in enumerate(specifications):
            rhs=field_sum((1,(variable(r4),{})),(1,sf(fifth,f(deep))),
                          (1,sf(r1,f(middle,mult1))),(1,sf(r2,f(low,mult2))),
                          (1,field_mul(f(last,-2),f(last,-2))),
                          (-1,sf(r4,f(base+2*k))))
            for n in range(2):changes[f'residue.det{j}.factor{k}.{n}.reciprocal.definition']=canonical(rhs[n])
        final=field_sum((1,field_mul(f(partial),f(base+6))),(-1,f(W)))
        for n in range(2):changes[f'amplified.det{j}.product4.{n}.definition']=canonical(final[n])
    removed_names={name for j in range(3) for k in range(2) for name in
                   (f'residue.det{j}.factor4.{k}.reciprocal.definition',f'amplified.det{j}.product3.{k}.definition')}
    expected=[];unchanged=changed=0
    for row in old['residuals']:
        name=row['name']
        if name in removed_names:continue
        if name in changes:expected.append(changes.pop(name));changed+=1
        else:expected.append(canonical(decode(row,old_ids)));unchanged+=1
    assert not changes
    expected+=powers+weight_rows
    actual=[decode(row,ids) for row in system['residuals']]
    assert len(actual)==237 and actual==expected
    assert len(powers)==8 and len(weight_rows)==3 and changed==30 and unchanged==196
    assert all(max(sum(x!=PARAMETER for x in m) for m in row)<=2 for row in actual)
    expanded=linear(*((1,product(row,row)) for row in actual))
    assert expanded==decode(polynomial,ids)
    assert gcd(*(int(c) for c in expanded.values()))==1
    assert max(sum(x!=PARAMETER for x in m) for m in expanded)==4
    assert {x for m in expanded for x in m if x!=PARAMETER}==set(ids.values())
    profiles=defaultdict(dict)
    for m,c in expanded.items():profiles[tuple(x for x in m if x!=PARAMETER)][m.count(PARAMETER)]=int(c)
    assert len(profiles)==3485==report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded)==3486==report['symbolicTerms']
    assert profiles[(489,489)]=={0:1,2:1}
    assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
    C=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
    L=max(abs(p[1]) for p in profiles.values() if set(p)=={1})
    assert str(C)==report['constantCoefficientMaximum'] and C.bit_length()==1520
    assert L==44402==report['linearCoefficientMultiplierMaximum']
    assert C>L*L and 149**210+1<C<149**214+1
    # Every possible residue of the odd contact valuation and test
    # valuations occurs in the following finite residue census.
    for nu in (1,3,5,7):
        for n in range(8):
            assert (4*n-9*nu)%4==(-nu)%4
            assert (4*n-3*nu)%4==nu%4
            assert (4*n-2*nu)%4==2
        for even in (0,2,4,6):
            assert (2*even-3*nu)%4==nu%4
            assert (2*even-2*nu)%4==2
            assert (4*even-4*nu)%8==4
        assert len({0,(-nu)%4,nu%4,2})==4
    assert (9-Q(1,2))/4==Q(17,8)>2
    assert (3-Q(1,2))/4==Q(5,8)>0
    assert (2-Q(1,2))/4==Q(3,8)>0
    assert 4*4-9>0 and 4*4-3>0 and 4*4-2>0
    assert 2*2-3>0 and 2*2-2>0 and 4*2-4>0
    N=9682;depth=19*(2*N-1)//8+1;c=149**depth
    assert depth==45988
    threshold=331969
    assert 2**(2*threshold-3*221274)*15**6>13**3*(345+7*threshold)**6
    assert 5**3*14<13**3
    assert c-1>=2**threshold and c>40*(1<<221234) and c>4640000
    assert 149**(19*(2*(N-1)-1)//8+1)-1<2**threshold
    assert 5290<2**13 and 23*221287<22*232000
    assert 149**3>10*(1+149**2) and 25*(10+9792)<17*10**5
    assert (149**38730+1).bit_length()==279599
    certificate={
        'status':'PASS','variables':265,'quadraticRows':237,'degree':4,'content':1,
        'ordinaryMonomialsForEveryPositiveParameter':3485,'symbolicTerms':3486,
        'sourceSha256':PIN,'systemSha256':sha256(system_raw).hexdigest(),
        'polynomialSha256':sha256(polynomial_raw).hexdigest(),
        'unchangedSourceRowsComparedExactly':unchanged,'changedFactorAndProductRowsReconstructed':changed,
        'newSharedFourthPowerRowsReconstructed':8,'newFifthPowerWeightRowsReconstructed':3,
        'completeValuationResidueCheck':True,'comparisonPrecision':3,'inputPrecision':1,
        'deepComparisonValuationStrictLowerBound':'17*nu/8',
        'heightFormula':'max(C,A^2+1);149^(4*N+2)+1 for N>=53',
        'definingThresholdN':N,'forcedIndexDepth':depth,'specifiedParameter':'149^19365',
        'specifiedCoefficientHeight':'149^38730+1','specifiedCoefficientHeightBinaryDigits':279599,
        'integerThresholdChecks':{'lucasResidual':True,'scalarHeight':True,
                                  'inputHeightAdditiveTerm':True,'realCompleteness':True,
                                  'previousNDoesNotMeetThisSufficientCriterion':True},
        'arithmeticScope':'Exact coefficients, residue classes and threshold inequalities are certified. The defining theorem additionally uses the stated normalized modular, elliptic, pole and simultaneous-prime premises and effective sum-height theorem.',
    }
    (folder/'independent-verification265-v19.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps(certificate,sort_keys=True))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=HERE)
    p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
    verify(a.source_root,a.output_root)
