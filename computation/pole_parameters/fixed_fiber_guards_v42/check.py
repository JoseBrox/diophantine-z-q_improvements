#!/usr/bin/env python3
"""Exact checks for scalar pole classes and fixed-fiber guard avoidance.

The universal density and independent-index preparation assertions are proved
in the companion paper.  This checker audits actual source dependencies,
checks the square extraction independently, and verifies exact elliptic maps,
odd multiples, torsion diagnostics, and the half-point chart identity.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json
import sys
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0,str(REPO/'computation/few_variables/unit_norm_v28'))
from build_sources import make_source


def valuation(value,p):
    value=F(value)
    assert value
    def vp(a):
        a=abs(a);v=0
        while a%p==0: a//=p;v+=1
        return v
    return vp(value.numerator)-vp(value.denominator)


def rational_sqrt(value):
    value=F(value)
    assert value>=0
    a,b=isqrt(value.numerator),isqrt(value.denominator)
    assert a*a==value.numerator and b*b==value.denominator
    return F(a,b)


def source_audits():
    reports=[]
    for name in ('general25','explicit27','weak13','abc13'):
        source=make_source(name)
        nodes=source['coefficient_dag'];variables=source['variables']
        roots={'A'} if name in ('weak13','abc13') else {'A','S','T','Z'}
        auxiliary={'H','UA'} if name in ('weak13','abc13') else {'H','UA','US','UT','UZ'}
        allowed={v['index'] for v in variables if v['name'] in ('input.X','slope.lambda')
                 or v['category']=='retained.point' and v['name'].split('.')[0] in roots}
        dependencies=[]
        for op,*args in nodes:
            if op=='variable': result={args[0]}
            elif op in ('int','parameter'): result=set()
            elif op in ('pow','neg'): result=dependencies[args[0]].copy()
            elif op in ('add','mul'): result=set().union(*(dependencies[j] for j in args))
            else: raise AssertionError(op)
            dependencies.append(result)
        def deps(r):
            return dependencies[r['numerator']] | dependencies[r['denominator']]
        # Independent multiplicative normal form, treating sums as named atoms.
        # Constant factors are exact rational numbers, not formal integer nodes.
        cache={}
        def factors(i):
            if i in cache:return cache[i]
            op,*args=nodes[i]
            if op=='int': result=(F(args[0]),{})
            elif op in ('add','variable','parameter'): result=(F(1),{i:1})
            elif op=='neg':
                c,ff=factors(args[0]);result=(-c,ff.copy())
            elif op=='pow':
                c,ff=factors(args[0]);result=(c**args[1],{k:v*args[1] for k,v in ff.items()})
            elif op=='mul':
                cc=F(1);ff=Counter()
                for child in args:
                    c,f=factors(child);cc*=c;ff.update(f)
                result=(cc,dict(ff))
            else:raise AssertionError(op)
            cache[i]=result;return result
        def rational_factors(r):
            a,aa=factors(r['numerator']);b,bb=factors(r['denominator'])
            ff=Counter(aa);ff.subtract(bb)
            return a/b,{k:v for k,v in ff.items() if v}
        pole_rows=[]
        for event in source['events']:
            if event['operation']=='rescaled_zero_pole':
                support=deps(event['square_class'])
                assert support<=allowed
                assert not any(variables[i]['category'].startswith('finite.') for i in support)
                bc,bf=rational_factors(event['input'])
                dc,df=rational_factors(event['square_class'])
                tc,tf=rational_factors(event['square_multiplier'])
                ff=Counter(df)
                for k,v in tf.items():ff[k]+=2*v
                assert bc==dc*tc*tc and bf=={k:v for k,v in ff.items() if v}
                actual_roles={variables[i]['name'].split('.')[0] for i in deps(event['input'])}
                assert auxiliary<=actual_roles
                pole_rows.append({'pole':event['label'],
                    'd_dependencies':[variables[i]['name'] for i in sorted(support)],
                    'b_equals_d_times_t_squared':True,
                    'no_auxiliary_point_or_finite_character_dependency':True})
            if event['operation'] in ('combined_height_scales','conditional_weak_abc_height_scales'):
                for scale in event['scales']: assert deps(scale)<=allowed
        blocks=source['finite_blocks']
        assert {block['kind'] for block in blocks}=={'point_block','pole'}
        assert {block['name'] for block in blocks if block['kind']=='point_block'}==roots|auxiliary
        assert all(block['degree']==4 for block in blocks if block['kind']=='point_block')
        assert all(block['degree']==2 for block in blocks if block['kind']=='pole')
        reports.append({'source':name,'fixed_root_roles':sorted(roots),
            'independently_variable_auxiliary_roles':sorted(auxiliary),'poles':pole_rows,
            'finite_equations':'point blocks and pole quadratics only; differences are rationally recovered'})
    return reports


def add(P,Q,n):
    if P is None:return Q
    if Q is None:return P
    x,y=P;xx,yy=Q
    if x==xx:
        if y==-yy:return None
        slope=(3*x*x+4*n*x-3*n*n)/(2*y)
    else:slope=(yy-y)/(xx-x)
    xxx=slope*slope-2*n-x-xx
    return xxx,-y+slope*(x-xxx)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'verification.json')
    args=parser.parse_args()
    x,y,DE,D,A,s,q,tau=sp.symbols('x y DE D A s q tau')
    # Clear the denominator of the square-abscissa duplication identity.
    dup=(3*x*x-DE)**2-8*x*y*y-(x*x+DE)**2
    assert sp.expand(dup-8*x*(x**3-DE*x-y*y))==0
    image=(D*s*q)**2-(D*s*s)*(D*s*s-D*A)*(D*s*s+3*D*A)
    assert sp.expand(image-D*D*s*s*(q*q-D*(s*s-A)*(s*s+3*A)))==0
    e=(tau*tau-D)/(tau*tau+3*D)
    assert sp.factor(D*(1-e)*(1+3*e)-(-4*D*tau/(tau*tau+3*D))**2)==0

    # The exceptional rational-square twist has exactly these eight torsion
    # points; it is not needed for prepared inputs, whose twist has odd v17.
    torsion=[None,(F(0),F(0)),(F(1),F(0)),(F(-3),F(0)),
             (F(3),F(6)),(F(3),F(-6)),(F(-1),F(2)),(F(-1),F(-2))]
    for P in torsion:
        if P is not None:assert P[1]**2==P[0]*(P[0]-1)*(P[0]+3)
    assert all(add(P,Q,F(1)) in torsion for P in torsion for Q in torsion)
    counts={}
    for p in (5,7):
        counts[p]=1+sum(sum(yy*yy%p==xx*(xx-1)*(xx+3)%p for yy in range(p)) for xx in range(p))
        assert counts[p]==8
    division3=[(3*z**4+8*z**3-18*z*z-9)%5 for z in range(5)]
    assert division3==[1,4,1,3,3]

    # Explicit prepared inputs with square C give nonzero witnesses at any
    # nonzero tau. They exercise both signs of the nonsquare elliptic twist.
    examples=[]
    for d,r in ((F(1),F(6,101)),(F(409),F(6,1001))):
        t=34*r/(1+17*d*r*r)
        bb=d*t*t;CC=17*(17-bb);DD=17*d
        ss=17*(1-17*d*r*r)/(1+17*d*r*r)
        assert ss*ss==CC and 0<bb<17
        assert isqrt(bb.denominator)**2==bb.denominator
        assert [valuation(bb,p) for p in (2,3,17)]==[4,2,2]
        for tt in (F(1),F(17),F(2,3)):
            ee=(tt*tt-DD)/(tt*tt+3*DD);AA=ee*CC;nn=DD*AA
            pp=-4*DD*tt/(tt*tt+3*DD);qq=CC*pp
            assert qq and qq*qq==DD*(ss*ss-AA)*(ss*ss+3*AA)
            assert valuation(ee,17)==0
            assert valuation(nn,17)==valuation(DD,17)+2
            assert valuation(nn,17)%2==1
            P=(DD*ss*ss,DD*ss*qq)
            two=add(P,P,nn);current=P;abscissas=[]
            for odd in (1,3,5,7):
                assert current is not None
                xx,yy=current
                assert yy and yy*yy==xx*(xx-nn)*(xx+3*nn)
                sr=rational_sqrt(xx/DD);qr=yy/(DD*sr)
                assert qr and qr*qr==DD*(sr*sr-AA)*(sr*sr+3*AA)
                abscissas.append(xx)
                current=add(current,two,nn)
            assert len(set(abscissas))==4
            examples.append({'d':str(d),'b':str(bb),'tau':str(tt),'n_sign':1 if nn>0 else -1,
                'v17_n':valuation(nn,17),'verified_odd_multiples':[1,3,5,7]})

    # A positive value at just one character would not suffice. In Q×Q the
    # element (1,-1/51) has a positive selected character but its denominator
    # tau²+51d vanishes at the other character when tau=1.
    assert 1+51*F(1)==52 and 1+51*F(-1,51)==0
    report={'status':'PASS',
        'scope':'fixed-fiber guard avoidance and independent auxiliary-index preparation; no common rational tau existence theorem or variable saving',
        'symbolic_identities':['duplication square abscissa','pole-to-elliptic map','first conic chart'],
        'native_source_audits':source_audits(),
        'prepared_fixed_fiber_examples':examples,
        'square_twist_torsion_control':{'point_count_F5':counts[5],'point_count_F7':counts[7],
            'rational_torsion_points':8,'positive_non_two_torsion_abscissa':3,
            'normalized_three_division_values_mod5':division3},
        'non_scalar_guard_countercontrol':{'algebra':'Q×Q','d':['1','-1/51'],'tau':'1',
            'denominators':['52','0'],'selected_character_positive':True},
        'proof_dependencies':[
            'v14 nonsquare-twist torsion and x-squareclass lemmas',
            'v19/v28 retained source completeness and point-stage unit preparation',
            'finite-place continuity and recurrence in compact real cyclic closures'],
        'source_builder_sha256':sha256((REPO/'computation/few_variables/unit_norm_v28/build_sources.py').read_bytes()).hexdigest(),
        'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','native_sources':4,'prepared_fixed_fiber_examples':len(examples),
                      'certificate':str(args.output)},indent=2))


if __name__=='__main__':main()
