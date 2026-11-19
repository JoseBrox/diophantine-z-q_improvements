"""Independent finite checks of the specialized three-scale L=117 construction."""
from fractions import Fraction
from itertools import combinations
from math import prod
from pathlib import Path
import importlib.util
import inspect
import json
import sys

from check_L53 import prime_support, support, factors
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
P=167
L=117
BASE={2,3,5,7,11,13,17,37,41,2399}
UNIT=BASE|{19,23,457,4799}
def ab(b):return b*(b-1)*(b-2401),(32*b+343)*(b+24)
def prime_checks():
    assert prime_support(P)=={P}
    for x in range(P):
        a,b=ab(102*x*x+2957)
        assert a*b*(b+(102*2)**2*a)%P
    for x in range(8):
        z=102*x*x+2957;a,b=ab(z)
        n=a*b
        while n%4==0:n//=4
        assert n%2 and (P*n)%8==1 and a%2==0 and b%2
    for p in (3,17):
        for x in range(p):
            a,b=ab(102*x*x+2957)
            assert pow(P*a*b, (p-1)//2,p)==1
    # The rational beta=fraction(102X^2+2957) recognizes integrality.
    assert prime_support(102)=={2,3,17} and 102==2*3*17
    contacts=[Fraction(0),Fraction(1),Fraction(2401),Fraction(-343,32),Fraction(-24)]
    G=UNIT|support(factors(contacts))
    J=prod(G); Euler=prod(Fraction(p+1,p) for p in G)
    Cstar=Fraction(74712001,10**6)*2**68*3**16*5**16*7**4
    assert P not in G and 2*Cstar*J**2*Euler*J.bit_length()<2**342
    assert P**(2*L+1)-1>=2**1735 and P**(2*L+1)>120*2**342
    # Each displayed norm constant is < exp(128) since it is < 2^128.
    A=1+2402+2401
    B=sum((32,32*24+343,343*24))
    assert max(102**2*4*102**2*P*A*B,(A+B)**2*(4*102**2)**2*P**2)<2**128
    return sorted(G)

def load(name,path):
    obj=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(obj);sys.modules[name]=mod;obj.loader.exec_module(mod)
    return mod

def audit():
    f=PROJECT/'fewvars/check_positive.py'
    sys.argv=[str(f),'--output',str(HERE/'compact117'),'--repo',str(PROJECT/'source')]
    check=load('compact_replay',f)
    source=json.loads((HERE/'compact117/explicit27/native.json').read_bytes())
    node=check.Circuit()
    for i,entry in enumerate(source['coefficient_dag']):assert node.node(*entry)==i
    def R(i):return check.Rational(node,i,node.one)
    def src(x):return check.Rational(node,x['numerator'],x['denominator'])
    def equals(a,b):assert (a.n,a.d)==(b.n,b.d)
    event=lambda t:next(e for e in source['events'] if e['operation']==t)
    x=R(node.node('variable',0));power=lambda j:R(node.power(node.node('int',P),j))
    beta=102*x**2+2957
    a,b=ab(beta);raw=node.rational(1)
    for f0 in (beta,beta-1,beta-2401,32*beta+343,beta+24):raw*=f0
    T=(102*(power((L+1)//2)+2))**2;den=b+T*a
    rho=102**2*power(L)*T*raw/den**2
    hh=event('combined_height_scales')
    for val,tag in [(beta,'beta'),(raw,'raw_scalar_contact'),(den,'scalar_denominator'),(rho,'scalar_contact')]:
        equals(val,src(hh[tag]))
    pts=[e for e in source['events'] if e['operation']=='point_block']
    rootnames=('A','S','T','Z'); roots=[next(e for e in pts if e['name']==s) for s in rootnames]
    assert len(pts)==9 and all((e.get('chart')=='full_auxiliary')==(e['name'] not in rootnames) for e in pts)
    uv=[sum((src(e['x'][j]) for e in roots),node.rational(0)) for j in (0,1)]
    for v,p in zip(uv,hh['aggregate_components'],strict=True):equals(v,src(p))
    scales=[node.rational(1),(1+rho*uv[0]**2)**2,(1+rho*(uv[0]+uv[1])**2)**2]
    for v,p in zip(scales,hh['scales'],strict=True):equals(v,src(p))
    tests=event('comparison_and_scalar_tests')
    assert tests['comparison_powers']==[1]*10+[2]*6
    equals(src(tests['comparison'][14][0]),src(tests['L'][0][0])-beta)
    succeeds=[e for e in source['events'] if e['operation']=='combined_detector']
    sv=next(v for v in source['variables'] if 'slope' in v['name']);lam=R(node.node('variable',sv['index']))
    theta=[Fraction(0),Fraction(-1,2),Fraction(-1),Fraction(1,2399),Fraction(-32,407)]
    for j,e in enumerate(succeeds):
        arg=scales[j]*lam
        delta=arg-(-j-1)
        contacts=[s+y for s in (4*j+2,4*j+4) for y in theta]
        assert e['contacts']==list(map(str,contacts))
        ff=node.rational(1)
        for y in contacts:ff*=arg-y
        rf=ff/delta**10;q=rho*rf
        for v,tag in [(scales[j],'scale'),(arg,'argument'),(delta,'delta'),(ff,'F'),(rf,'contact_function'),(q,'combined_coefficient')]:
            equals(v,src(e[tag]))
        for order,w in zip(tests['comparison_orders'],e['comparison_weights'],strict=True):
            equals(q/(delta**2*q**(2*order)),src(w))
        for order,w,rawv,out in zip(tests['scalar_orders'],e['scalar_weights'],tests['scalar'],e['normalized_scalar'],strict=True):
            equals(q/q**(2*order),src(w))
            rv=rf*src(rawv)
            equals(rf**order*(rv/(1+rv)),src(out[0]));equals(node.rational(0),src(out[1]))
    # Compare all unchanged point roles, field/scalar tests and log ratios against
    # the independent upstream arithmetic on these same five enlarged charts.
    m=load('compact_reference_chart',check.BASE/'even_valuation25_v75/build_source.py')
    old=__import__('build_sources')
    class Reference(old.Explicit27):
        point=m.FullAuxiliary25.point
    baseline=Reference(L).build()
    new_sign=check.signatures(source['coefficient_dag']);old_sign=check.signatures(baseline['coefficient_dag'])
    def norm(v,sign):
        if isinstance(v,list):return [norm(z,sign) for z in v]
        if isinstance(v,dict):
            if set(v)=={'numerator','denominator'}:return [sign[v['numerator']],sign[v['denominator']]]
            return {k:norm(y,sign) for k,y in v.items()}
        return v
    oldtests=next(e for e in baseline['events'] if e['operation']=='comparison_and_scalar_tests')
    for key in ('scalar','L','Lprime','comparison_orders','scalar_orders'):
        assert norm(oldtests[key],old_sign)==norm(tests[key],new_sign)
    for i in range(16):
        if i!=14:assert norm(oldtests['comparison'][i],old_sign)==norm(tests['comparison'][i],new_sign)
    assert norm(oldtests['comparison'][14][1],old_sign)==norm(tests['comparison'][14][1],new_sign)
    assert norm([e for e in baseline['events'] if e['operation']=='point_block'],old_sign)==norm(pts,new_sign)
    # Reuse v75 five-full-chart and factor semantics; three poles and the actual
    # rank are read from the specification by the full independent verifier.
    check.ancestor=lambda route:source
    code=inspect.getsource(check.audit)
    assert code.count('directory=args.output/route')==1
    exec(compile(code.replace('directory=args.output/route','directory=args.output/"explicit27"'),
                 'three-pole-independent-audit','exec'),check.__dict__)
    out=check.audit('general25');print('Independent full three-scale certificate',out[1:])
    print('Scalar radical exceptional set',prime_checks())

if __name__=='__main__':audit()
