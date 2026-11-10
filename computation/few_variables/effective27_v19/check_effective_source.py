#!/usr/bin/env python3
"""Independent coefficient conversion and formula reconstruction for effective27.

The affine source conversion, point quartics, guard coverage and square
clearings are checked as exact symbolic identities by the existing auditor.
Every new rational expression is also independently reconstructed over
several finite fields, without importing the producer or its field code.
These finite-field reconstructions are explicitly finite evidence; the
unrestricted arithmetic projection is the separate mathematical theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
import json
from math import prod,isqrt
from pathlib import Path
import random
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PINNED=HERE.parent/'trace27_nontorsion'
sys.path.insert(0,str(PINNED))
from verify_specification import audit


class QuadraticArithmetic:
    def __init__(self,p):self.p=p
    def q(self,x):
        x=F(x)
        return x.numerator*pow(x.denominator,-1,self.p)%self.p
    def f(self,a=0,b=0):return self.q(a),self.q(b)
    def add(self,a,b):return (a[0]+b[0])%self.p,(a[1]+b[1])%self.p
    def neg(self,a):return -a[0]%self.p,-a[1]%self.p
    def sub(self,a,b):return self.add(a,self.neg(b))
    def mul(self,a,b):return (a[0]*b[0]+2*a[1]*b[1])%self.p,(a[0]*b[1]+a[1]*b[0])%self.p
    def sq(self,a):return self.mul(a,a)
    def scale(self,a,c):return a[0]*c%self.p,a[1]*c%self.p
    def inv(self,a):
        n=(a[0]*a[0]-2*a[1]*a[1])%self.p
        t=pow(n,-1,self.p)
        return a[0]*t%self.p,-a[1]*t%self.p
    def div(self,a,b):return self.mul(a,self.inv(b))
    def conj(self,a):return a[0],-a[1]%self.p
    def difference(self,P,Q):
        m=self.div(self.add(P[1],Q[1]),self.sub(P[0],Q[0]))
        x=self.sub(self.sub(self.sq(m),P[0]),Q[0])
        y=self.sub(self.sub(self.mul(m,P[0]),P[1]),self.mul(m,x))
        return x,y
    def fpoint(self,P):return self.inv(P[0])
    def zpoint(self,P):return self.neg(self.div(P[0],P[1]))
    def logpoint(self,P):
        # Direct sum, independently of the producer's Horner scheme.
        w=self.mul(self.f(11,-6),self.sq(self.fpoint(P)))
        power=self.f(1);total=self.f();c=F(1)
        for j in range(1):
            if j==1:c=F(-2,5)
            elif j>=2:c*=F(4*j-5,4*j+1)
            total=self.add(total,self.scale(power,self.q(c)))
            power=self.mul(power,w)
        return self.mul(self.zpoint(P),total)


def finite_reconstruction(source,p,seed):
    assert all(p%d for d in range(2,isqrt(p)+1))
    rng=random.Random(seed);arith=QuadraticArithmetic(p)
    variables=[rng.randrange(1,p) for _ in source['variables']]
    vals=[]
    for op,*a in source['coefficient_dag']:
        if op=='int':v=a[0]%p
        elif op=='variable':v=variables[a[0]]
        elif op=='parameter':v=source['finite_parameters'][a[0]][0]%p
        elif op=='neg':v=-vals[a[0]]%p
        elif op=='add':v=sum(vals[i] for i in a)%p
        elif op=='mul':v=prod(vals[i] for i in a)%p
        elif op=='pow':v=pow(vals[a[0]],a[1],p)
        else:raise AssertionError(op)
        vals.append(v)
    def q(row):return vals[row['numerator']]*pow(vals[row['denominator']],-1,p)%p
    def pair(rows):return tuple(q(row) for row in rows)
    names={v['name']:variables[v['index']] for v in source['variables']}
    points={}
    for name in ('A','S','T','Z','H','UA','US','UT','UZ'):
        h=arith.f(names[name+'.a0'],names[name+'.a1']);x=arith.sq(h)
        a,b=arith.sub(arith.sq(x),arith.f(11,-6))
        multiplier=arith.f(2*a+b,-a-b)
        ap,bp=arith.mul(arith.sq(multiplier),arith.f(a,b))
        Y=names[name+'.Y']
        j=arith.div(arith.f(Y*pow(2,-1,p),bp*pow(Y,-1,p)),multiplier)
        point=(x,arith.mul(h,j));points[name]=point
        event=next(e for e in source['events'] if e['operation']=='point' and e['name']==name)
        assert pair(event['output_x'])==x and pair(event['output_y'])==point[1]
    H=points['H'];Ui=[points[k] for k in ('UA','US','UT','UZ')]
    roots=[points[k] for k in ('A','S','T','Z')]
    P=(arith.f(F(57,8),F(-7,2)),arith.f(F(-165,8),F(417,32)))
    V=[arith.difference(a,b) for a,b in zip([H]+Ui,[P]+roots)]
    L=[arith.div(arith.logpoint(Q),arith.logpoint(H)) for Q in Ui]
    Lp=[arith.conj(arith.div(arith.logpoint(Q),arith.logpoint(V[0]))) for Q in V[1:]]
    beta=(216*pow(names['input.X'],4,p)+450459)%p
    tests=[arith.fpoint(Q) for Q in [H]+Ui]+[arith.conj(arith.fpoint(Q)) for Q in V]
    tests += [arith.sub(a,b) for a,b in zip(L,Lp)]+[arith.sub(L[0],arith.f(beta))]
    a,t,b=L[1:];am2=arith.sub(a,arith.f(2))
    lucas=arith.sub(arith.add(arith.sq(t),arith.mul(arith.sq(am2),arith.sq(b))),
                     arith.add(arith.mul(arith.mul(a,am2),arith.mul(t,b)),arith.f(1)))
    tests.append(lucas)
    assert [pair(D) for D in source['comparison_tests']]==tests
    SmP=arith.difference(points['S'],P)
    scalar=list(arith.fpoint(H)+arith.fpoint(SmP)+arith.div(arith.zpoint(SmP),arith.zpoint(H)))
    assert [q(D) for D in source['scalar_tests']]==scalar
    raw=prod((beta,beta-1,beta-2401,32*beta+343,2*beta-1))%p
    exponent=source['family_parameter']['value'];ell=76249
    den=(1+17*(pow(ell,(exponent+1)//2,p)+1)*raw)%p
    z=102**2*pow(ell,exponent,p)*raw*pow(den,-2,p)%p
    assert q(source['scalar_contact'])==z
    aggregate=[sum(Q[0][k] for Q in roots)%p for k in range(2)]
    scales=[1,pow(1+z*aggregate[0]**2,2,p),
            pow(1+z*(aggregate[0]+aggregate[1])**2,2,p)]
    assert [q(a) for a in source['aggregate_sum_components']]==aggregate
    assert [q(a) for a in source['height_scales']]==scales
    base=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    all_contacts=[[c+j for j in js for c in base] for js in ((2,4),(6,8),(10,12))]
    phi_events=[e for e in source['events'] if e['operation']=='linear_scalar_normalization']
    for event in phi_events:
        numerator=q(event['coefficient'])*q(event['input'])%p
        assert q(event['output'])==numerator*pow(1+numerator,-1,p)%p
        assert q(event['denominator'])==(1+numerator)%p
    for r,event in enumerate(e for e in source['events'] if e['operation']=='combined_detector'):
        u=scales[r]*names['slope.lambda']%p;delta=(u+r+1)%p
        R=prod((u-arith.q(c))%p for c in all_contacts[r])*pow(delta,-10,p)%p
        combined=z*R%p;W=arith.f(1)
        orders=[1]*10+[3]*6
        for j,(D,order) in enumerate(zip(tests,orders)):
            value=arith.scale(D,pow(delta*pow(combined,order,p)%p,-1,p))
            expected_weight=combined*pow(delta*delta*pow(combined,2*order,p)%p,-1,p)%p
            assert q(event['comparison_weights'][j])==expected_weight
            W=arith.mul(W,arith.add(arith.f(1),arith.scale(arith.sq(value),combined)))
        for D in scalar:
            phi=R*D*pow(1+R*D,-1,p)%p
            E=arith.f(pow(R,3,p)*phi)
            value=arith.scale(E,pow(combined,-3,p))
            W=arith.mul(W,arith.add(arith.f(1),arith.scale(arith.sq(value),combined)))
        assert pair(event['product_components'])==W
        norm=(W[0]**2-2*W[1]**2)%p
        pole=combined*norm*norm*pow(W[0],-2,p)%p
        assert q(event['pole_input'])==pole
        tau=names[f'detector{r}.conic_parameter'];s=names[f'detector{r}.s']
        B=17*pole%p;e=(tau*tau-B)*pow(tau*tau+3*B,-1,p)%p
        vv=B*e*(B-pole*pole)%p
        rad=(s*s-vv)*(s*s+3*vv)*pow(B,-1,p)%p
        rel=source['finite_monic_relations'][9+r]
        assert q(rel['original_square_input'])==rad
    return {'prime':p,'seed':seed,'point_charts':9,'comparison_tests':16,
            'scalar_components':6,'linear_scalar_normalizations':len(phi_events),'complete_products':3,'pole_radicands':3}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    raw=gzip.decompress((args.directory/'source.json.gz').read_bytes());source=json.loads(raw)
    encoded=(args.directory/'source-polynomial-specification.json').read_bytes();spec=json.loads(encoded)
    report=audit(source,spec)
    assert source['retained_base_count']==26 and source['total_polynomial_variables_after_finite_algebra']==27
    assert [r['kind'] for r in source['finite_monic_relations']]==['point']*9+['pole']*3
    assert source['comparison_orders']==[1]*10+[3]*6 and source['scalar_orders']==[3]*6
    assert source['comparison_normalization']=='none'
    assert source['scalar_normalization']=='R*D/(1+R*D)'
    assert source['scalar_switch_exponent']==source['scalar_norm_denominator_exponent']==3
    assert source['common_index_divisible_by_selected_primes'] is True
    builder=(HERE/'build_effective_source.py').read_bytes()
    assert source['source_builder_sha256']==hashlib.sha256(builder).hexdigest()
    assert source['formal_precision']==4
    assert source['family_parameter']['effective_threshold_known'] is True
    assert source['family_parameter']['certified_sufficient_lower_bound']==125001
    assert source['family_parameter']['selected_member_certified_to_define_Z']==(source['family_parameter']['value']>=125001)
    slope=next(v['index'] for v in source['variables'] if v['name']=='slope.lambda')
    slope_node=source['coefficient_dag'].index(['variable',slope])
    assert slope_node in source['guard_numerators']
    assert all('retained.scalar_pole'!=v['category'] for v in source['variables'])
    assert source['closed_equations']==source['indexed_guard_polynomials']==[]
    assert source['finite_parameters']=={'pole_chart_detector0':[0],'pole_chart_detector1':[0],'pole_chart_detector2':[0]}
    records=[];skipped=0
    for p in (1000003,1000033,1000037):
        for seed in range(5):
            try:records.append(finite_reconstruction(source,p,5713+seed))
            except ValueError:skipped+=1
    assert len(records)>=12
    report.update(status='PASS',total_coordinates=27,
        source_sha256=hashlib.sha256(raw).hexdigest(),integer_specification_sha256=hashlib.sha256(encoded).hexdigest(),
        finite_field_formula_reconstructions=records,singular_finite_field_samples_skipped=skipped,
        explicit_nonzero_slope_guard=True,family_parameter=source['family_parameter'],
        comparison_orders=[1]*10+[3]*6,comparison_normalization='none',
        scalar_normalization='linear',scalar_denominator_exponent=3,
        scope='Exact symbolic source-to-integer conversion, point quartics and derivatives, automatic guard coverage and monic pole-square clearings. Independent finite-field reconstruction of every new rational expression is finite evidence, not a proof of a universal identity. The projection theorem and its certified sufficient exponent are supplied by the mathematical paper.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','total_coordinates':27,'exact_point_quartics':report['source_point_quartics_checked'],
                      'exact_square_clearings':report['source_rational_square_clearings_checked'],
                      'exact_guard_factors':report['source_guard_atomic_factors_checked'],
                      'independent_finite_field_formula_reconstructions':len(records)},indent=2))


if __name__=='__main__':main()
