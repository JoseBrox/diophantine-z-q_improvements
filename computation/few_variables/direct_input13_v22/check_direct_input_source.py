#!/usr/bin/env python3
"""Independent exact conversion and direct-input formula checks.

The source-to-integer conversion and the changed scale/target identities
are checked symbolically. Full rational formulas are additionally evaluated
over fifteen finite-field samples; these evaluations are bounded evidence.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import gzip
import hashlib
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
from finite_algebra_check_core import expander,plus,times,power


class QuadraticArithmetic:
    def __init__(self,p):self.p=p
    def q(self,x):
        x=F(x);return x.numerator*pow(x.denominator,-1,self.p)%self.p
    def f(self,a=0,b=0):return self.q(a),self.q(b)
    def add(self,a,b):return (a[0]+b[0])%self.p,(a[1]+b[1])%self.p
    def neg(self,a):return -a[0]%self.p,-a[1]%self.p
    def sub(self,a,b):return self.add(a,self.neg(b))
    def mul(self,a,b):return (a[0]*b[0]+2*a[1]*b[1])%self.p,(a[0]*b[1]+a[1]*b[0])%self.p
    def sq(self,a):return self.mul(a,a)
    def scale(self,a,c):return a[0]*c%self.p,a[1]*c%self.p
    def inv(self,a):
        z=pow((a[0]*a[0]-2*a[1]*a[1])%self.p,-1,self.p)
        return a[0]*z%self.p,-a[1]*z%self.p
    def div(self,a,b):return self.mul(a,self.inv(b))
    def conj(self,a):return a[0],-a[1]%self.p
    def difference(self,P,Q):
        m=self.div(self.add(P[1],Q[1]),self.sub(P[0],Q[0]))
        x=self.sub(self.sub(self.sq(m),P[0]),Q[0])
        y=self.sub(self.sub(self.mul(m,P[0]),P[1]),self.mul(m,x))
        return x,y
    def reciprocal(self,P):return self.inv(P[0])
    def parameter(self,P):return self.neg(self.div(P[0],P[1]))


def symbolic_new_formulas(source):
    nodes=source['coefficient_dag'];names={v['name']:v['index'] for v in source['variables']}
    event=next(e for e in source['events'] if e['operation']=='conditional_weak_abc_height_scales')
    d=source['scale_power']
    expand=expander(nodes,variables={names['input.X']:0,names['A.a0']:1,names['A.a1']:2},
                    parameters={'fixed_input_shift':3})
    x,a,b,B=[{(i,):1} for i in range(4)]
    beta=plus(power(x,2),B)
    trace=plus(times({():2},power(a,2)),times({():4},power(b,2)))
    for name,expected in [('target',x),('beta',beta),('trace',trace),
                          ('sum_even_powers',plus(power(beta,d),power(trace,d)))]:
        row=event[name]
        assert expand(row['denominator'])=={():1}
        assert expand(row['numerator'])==expected
    assert event['power']==d and event['scales'][1]==event['sum_even_powers']
    target=source['comparison_tests'][5]
    tests=next(e for e in source['events'] if e['operation']=='conditional_direct_target_tests')
    L=tests['L'];assert target[1]==L[1]
    assert target[0]['denominator']==L[0]['denominator']
    ex=expander(nodes,atoms={L[0]['numerator']:0,L[0]['denominator']:1},
                variables={names['input.X']:2})
    assert ex(target[0]['numerator'])=={(0,):1,(1,2):-1}
    assert tests['tests']==source['comparison_tests']
    return {'target_identity':'D6=L-X','scale_identity':f'(X^2+B)^{d}+(2A.a0^2+4A.a1^2)^{d}',
            'coefficient_shift_checked_as_formal_symbol':True}


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
    for name in ('A','H','UA'):
        h=arith.f(names[name+'.a0'],names[name+'.a1']);x=arith.sq(h)
        a,b=arith.sub(arith.sq(x),arith.f(11,-6))
        multiplier=arith.f(2*a+b,-a-b)
        ap,bp=arith.mul(arith.sq(multiplier),arith.f(a,b))
        Y=names[name+'.Y']
        j=arith.div(arith.f(Y*pow(2,-1,p),bp*pow(Y,-1,p)),multiplier)
        point=(x,arith.mul(h,j));points[name]=point
        event=next(e for e in source['events'] if e['operation']=='point' and e['name']==name)
        assert pair(event['output_x'])==x and pair(event['output_y'])==point[1]
    A,H,U=[points[name] for name in ('A','H','UA')]
    P=(arith.f(F(57,8),F(-7,2)),arith.f(F(-165,8),F(417,32)))
    V0=arith.difference(H,P);V1=arith.difference(U,A)
    L=arith.div(arith.parameter(U),arith.parameter(H))
    Lp=arith.conj(arith.div(arith.parameter(V1),arith.parameter(V0)))
    X=names['input.X'];B=source['family_parameter']['value'];beta=(X*X+B)%p
    tests=[arith.reciprocal(H),arith.reciprocal(U),arith.conj(arith.reciprocal(V0)),
           arith.conj(arith.reciprocal(V1)),arith.sub(L,Lp),arith.sub(L,arith.f(X))]
    assert [pair(D) for D in source['comparison_tests']]==tests
    d=source['scale_power'];trace=2*A[0][0]%p
    scales=[1,(pow(beta,d,p)+pow(trace,d,p))%p]
    contacts=[F(0),F(-1,2),F(-1,4),F(-2,5),F(-1),F(-1,3)]
    for r,event in enumerate(e for e in source['events'] if e['operation']=='detector'):
        t=scales[r]*names['slope.lambda']%p;delta=(t-1)%p
        poly=prod((t-arith.q(c))%p for c in contacts)%p
        weight=pow(delta,4,p)*pow(poly,-1,p)%p
        W=arith.f(1)
        for D in tests:W=arith.mul(W,arith.add(arith.f(1),arith.scale(arith.sq(D),weight)))
        assert q(event['scale'])==scales[r] and q(event['slope_argument'])==t
        assert q(event['F'])==poly and q(event['delta'])==delta
        assert q(event['weights']['1'])==weight and pair(event['product_components'])==W
        norm=(W[0]*W[0]-2*W[1]*W[1])%p
        pole=poly*norm*norm*pow(4*pow(delta,8,p)*W[0]*W[0]%p,-1,p)%p
        assert q(event['pole_input'])==pole
        tau=names[f'detector{r}.conic_parameter'];s=names[f'detector{r}.s']
        B0=17*pole%p;e=(tau*tau-B0)*pow(tau*tau+3*B0,-1,p)%p
        vv=B0*e*(B0-pole*pole)%p
        rad=(s*s-vv)*(s*s+3*vv)*pow(B0,-1,p)%p
        assert q(source['finite_monic_relations'][3+r]['original_square_input'])==rad
    return {'prime':p,'seed':seed,'point_charts':3,'local_tests':6,'complete_products':2,'pole_radicands':2}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    raw=gzip.decompress((args.directory/'source.json.gz').read_bytes());source=json.loads(raw)
    encoded=(args.directory/'source-polynomial-specification.json').read_bytes();spec=json.loads(encoded)
    report=audit(source,spec)
    assert source['retained_base_count']==12 and source['total_polynomial_variables_after_finite_algebra']==13
    assert [r['kind'] for r in source['finite_monic_relations']]==['point']*3+['pole']*2
    assert source['comparison_orders']==[1]*6 and source['formal_precision']==4
    d=source['scale_power'];assert d in (4,6)
    kappa=F(121,100) if d==6 else F(16,15)
    assert source['weak_abc_exponent']=={'numerator':kappa.numerator,'denominator':kappa.denominator}
    assert source['height_scales']==f'1,beta^{d}+(Tr x(A))^{d}'
    assert source['beta_formula']=='input.X^2+B'
    assert source['comparison_target']==source['final_polynomial_multiplier']=='input.X'
    assert source['closed_equations']==source['indexed_guard_polynomials']==[]
    premise=f'ADDITIONAL weak rational abc at exponent {kappa}'
    assert premise in source['additional_arithmetic_input'] and premise in spec['arithmetic_status']
    B=source['family_parameter']['value']
    assert B>=3 and B%2==1 and source['family_parameter']['selected_member_certified_to_define_Z'] is False
    assert source['finite_parameters']=={'pole_chart_detector0':[0],'pole_chart_detector1':[0],'fixed_input_shift':[B]}
    assert source['source_builder_sha256']==hashlib.sha256((HERE/'build_direct_input_source.py').read_bytes()).hexdigest()
    assert [e['name'] for e in source['events'] if e['operation']=='point']==['A','H','UA']
    assert sum(e['operation']=='detector' for e in source['events'])==2
    exact=symbolic_new_formulas(source)
    gamma=8/kappa-6;alpha=d/kappa-3;coefficient=2/(gamma*alpha)
    assert gamma>0 and alpha>0 and coefficient/2<1
    assert coefficient/2==(F(14641,17538) if d==6 else F(8,9))
    records=[];skipped=0
    for p in (1000003,1000033,1000037):
        for seed in range(5):
            try:records.append(finite_reconstruction(source,p,8713+seed))
            except ValueError:skipped+=1
    assert len(records)>=12
    report.update(status='PASS',total_coordinates=13,
        source_sha256=hashlib.sha256(raw).hexdigest(),integer_specification_sha256=hashlib.sha256(encoded).hexdigest(),
        scale_power=d,weak_abc_exponent=source['weak_abc_exponent'],
        absorption_coefficient=str(coefficient/2),exact_changed_formula_checks=exact,
        finite_field_formula_reconstructions=records,singular_samples_skipped=skipped,
        family_parameter=source['family_parameter'],
        uniform_degree_reason='The shift is a formal coefficient parameter of weight zero; no operation or branch depends on its numerical value.',
        scope='Exact source-to-integer conversion, three point quartics and derivatives, two square clearings, guard coverage, and changed input/scale identities with formal shift. Complete finite-field formula reconstruction is supplementary bounded evidence. The paper separately proves the projection under the stated arithmetic premises and additional weak abc hypothesis; no numerical defining shift is certified.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','total_coordinates':13,'scale_power':d,
        'point_quartics_checked':report['source_point_quartics_checked'],
        'pole_square_clearings_checked':report['source_rational_square_clearings_checked'],
        'guard_factors_checked':report['source_guard_atomic_factors_checked'],
        'finite_field_reconstructions':len(records),'absorption_coefficient':str(coefficient/2)},indent=2))


if __name__=='__main__':main()
