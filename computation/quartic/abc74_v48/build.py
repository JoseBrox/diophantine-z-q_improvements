#!/usr/bin/env python3
"""Reconstruct the complete 74-variable quartic and its exact coefficients.

The ten reference rows come from the literal five field quadrics. The stored
integer matrix, not a lattice-reduction search, specifies their chosen basis.
Every subsequent basis operation is an explicit rationally invertible row map.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd, lcm
import argparse
import json
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PARENT=ROOT/'computation/quartic/abc74_v46/quadratic-family.json'
PARENT_SHA='44499a87b0188f64d7e6d2c01046883a19326c40fa9956dcf31a1eb6e7a142dc'
RHO=s.sqrt(2)
XS=s.symbols('u0 u1 w0 w1 h0 h1 A0 A1 B0 B1')
REF_IDS=[3,4,5,6,7,8,23,24,25,26]

def primitive(p):
    p={k:Q(v) for k,v in p.items() if v}
    den=lcm(*(v.denominator for v in p.values()))
    content=gcd(*(int(den*v) for v in p.values()))
    sign=1 if p[min(p)]>0 else -1
    return {k:sign*int(den*v)//content for k,v in p.items()}

def components(expr):
    out=[{},{}]
    for powers,coefficient in s.Poly(s.expand(expr),*XS,extension=RHO).terms():
        coefficient=s.expand(coefficient)
        cs=[coefficient.subs(RHO,0),coefficient.coeff(RHO)]
        monomial=tuple(i for i,n in zip(REF_IDS,powers) for _ in range(n))
        for part,c in enumerate(cs):
            assert c.is_Rational
            if c:out[part][(0,monomial)]=Q(int(s.numer(c)),int(s.denom(c)))
    return out

def serialize(p):
    return [dict(parameterPower=j,monomial=list(m),coefficient=str(c))
            for (j,m),c in sorted(p.items())]

def multiply(p,q):
    r=defaultdict(Q)
    for (j,m),a in p.items():
        for (k,n),b in q.items():r[j+k,tuple(sorted(m+n))]+=a*b
    return {m:c for m,c in r.items() if c}

def substitute(p,replacements):
    out=defaultdict(Q)
    for (j,m),c in p.items():
        term={(j,()):Q(c)}
        for i in m:term=multiply(term,replacements.get(i,{(0,(i,)):Q(1)}))
        for key,z in term.items():out[key]+=z
    return {m:c for m,c in out.items() if c}

def build(output):
    raw=PARENT.read_bytes()
    assert sha256(raw).hexdigest()==PARENT_SHA,'Pinned complete source changed'
    parent=json.loads(raw)
    basis=json.loads((HERE/'basis-transformation.json').read_text())
    u,w,h,A,B=(XS[i]+RHO*XS[i+1] for i in (0,2,4,6,8))
    a=1+RHO;c=4-2*RHO;delta=-23+17*RHO
    assert s.expand(a*(a-c*c))==11-6*RHO
    v=a*(u+w)+2*c+delta*h
    S=v-c-a*u;T=a*w-v+c
    field_rows=[
        a*u*w-1,
        delta*h*h+a*h*(u+w)+2*c*h-1,
        a*A*(v+delta*w)+2*c*h*u+h-u,
        a*B*(v+delta*u)+2*c*h*w+h-w,
        a*a*(delta*delta*A*B-(1+4*c*w)*A-(1+4*c*u)*B)
            +1-2*(2*a+c*c)*h*h,
    ]
    reference=[primitive(p) for q in field_rows for p in components(q)]
    matrix=s.Matrix([[int(z) for z in row] for row in basis['referenceMatrix']])
    assert matrix.shape==(10,10) and matrix.det() in (-1,1)
    changed_reference=[]
    for coeffs in matrix.tolist():
        p=defaultdict(Q)
        for coeff,row in zip(coeffs,reference):
            for monomial,z in row.items():p[monomial]+=int(coeff)*z
        changed_reference.append(primitive(p))
    rows=[dict(id=i+1,name=f'common.unitGraph.{i+1}',terms=serialize(p))
          for i,p in enumerate(changed_reference)]
    replacements=dict(zip([3,4,5,6],components(S)+components(T)))
    replacement_count=0
    for original in parent['residuals']:
        if original['name'].startswith('common.primitive.'):continue
        p={(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient'])
           for t in original['terms']}
        if original['name']=='height.betaSquare':
            assert p=={(0,(1,1)):Q(1),(0,(36,)):Q(-4)}
            p[0,(36,)]=Q(-1)
            replacement_count+=1
        p=primitive(substitute(p,replacements))
        rows.append(dict(id=len(rows)+1,name=original['name'],terms=serialize(p)))
    assert replacement_count==1 and len(rows)==66
    before=[{(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient'])
             for t in row['terms']} for row in rows]
    assert before[0][0,()]==1 and basis['constantPivotRow']==1
    transformations=[]
    for i,p in enumerate(before):
        coefficient=p.get((0,()),0) if i else 0
        q=p.copy()
        if i:
            for m,z in before[0].items():q[m]=q.get(m,0)-coefficient*z
        q={m:z for m,z in q.items() if z}
        content=gcd(*q.values());sign=1 if q[min(q)]>0 else -1
        transformations.append(dict(row=i+1,pivotMultiple=coefficient,
                                    primitiveDivisor=content,sign=sign))
        rows[i]['terms']=serialize(primitive(q))
    assert transformations==basis['constantTransformation']
    expanded=defaultdict(int)
    for row in rows:
        p={(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient'])
           for t in row['terms']}
        assert max(len(m) for _,m in p)<=2
        for m,z in multiply(p,p).items():
            assert z.denominator==1
            expanded[m]+=int(z)
    expanded={m:z for m,z in expanded.items() if z}
    assert max(len(m) for _,m in expanded)==4
    assert expanded[0,(1,1,1,1)]==1 and gcd(*expanded.values())==1
    assert {i for _,m in expanded for i in m}==set(range(1,75))
    profiles=defaultdict(dict)
    for (j,m),z in expanded.items():profiles[m][j]=z
    assert profiles[()]=={0:1,2:1}
    fixed=max(abs(q[0]) for q in profiles.values() if set(q)=={0})
    assert fixed==30568 and len(profiles)==1695
    for q in profiles.values():
        if 1 in q:
            assert abs(q[1])<=2 and q[1]*q.get(0,0)>=0
            assert 81**2+1>=abs(q[1]*81+q.get(0,0))
        elif 2 in q:assert q=={0:1,2:1}
    coordinates=json.loads(json.dumps(parent['coordinates']))
    for item in coordinates:
        for old,new in [('common.S.','common.u.'),('common.T.','common.w.'),('common.f.','common.inverseChord.')]:
            if item['name'].startswith(old):item['name']=item['name'].replace(old,new)
    system=dict(format='integer-quadratic-family-unit-reference74-v48',variables=74,
                inputCoordinate=1,fixedParameter=parent['fixedParameter'],coordinates=coordinates,
                residuals=rows,parentQuadraticSha256=PARENT_SHA,
                coordinateConvention='Reference translator R0; beta=X. The reference coordinates are u,w,h=1/v,F_H,G_H. The paired chart and native pole inputs are complete. The stored row transformations preserve the full rational zero set.')
    polynomial=dict(format='integer-quartic-family-unit-reference74-v48',variables=74,degree=4,
                    inputCoordinate=1,fixedParameter=parent['fixedParameter'],coordinates=coordinates,
                    terms=serialize(expanded))
    report=dict(status='EXACT_CONDITIONAL_SPECIFICATION',variables=74,quadraticRows=66,degree=4,
                integerContentForEveryIntegerB=1,ordinaryMonomialsForEveryBAtLeast81=len(profiles),
                parameterSeparatedTerms=len(expanded),constantCoefficient='B^2+1',largestFixedCoefficient=str(fixed),
                exactHeight='max(30568,B^2+1)',translator='R0=(1+sqrt(2),2sqrt(2))',inputMap='beta=X',
                parentQuadraticSha256=PARENT_SHA,referenceRows=10,nonreferenceRows=56,
                parameterThresholdEffective=False,heightScale='B+X^8+T^2',heightAbsorption='602/679',
                localResidual='X*(m-X), m the integer index relative to R0',extraCoordinates=0,extraGuards=0,
                scope='Defining quartic under ordinary rational abc and the stated retained elliptic-group, simultaneous-prime, trace-height and simultaneous congruent-twist premises. B>=81 is fixed odd and sufficiently large; no numerical sufficient threshold is asserted.')
    output.mkdir(parents=True,exist_ok=True)
    for name,obj in [('quadratic-family.json',system),('polynomial-family.json',polynomial),('construction-report.json',report)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE)
    build(parser.parse_args().output)
