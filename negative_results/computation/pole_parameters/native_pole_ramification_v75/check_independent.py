#!/usr/bin/env python3
"""Producer-free reconstruction of the physical norm counterexample.

Uses four-coordinate quadratic-algebra multiplication for the norm identities,
exact rational field pairs for the physical point, and a recursive DAG evaluator
at a different split prime for all 64 point characters. Imports no project code.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import isqrt, prod
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]


def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,c):return (c*x[0],c*x[1])
def norm(x):return x[0]**2-2*x[1]**2
def inv(x):
    n=norm(x);assert n
    return (x[0]/n,-x[1]/n)
def div(x,y):return mul(x,inv(y))
def power(x,n):
    answer=(F(1),F(0))
    for _ in range(n):answer=mul(answer,x)
    return answer


def point_sum(P,Q,D):
    if P==Q:
        slope=div(sub(scale(mul(P[0],P[0]),3),D),scale(P[1],2))
    else:
        slope=div(sub(Q[1],P[1]),sub(Q[0],P[0]))
    x=sub(sub(mul(slope,slope),P[0]),Q[0])
    y=sub(mul(slope,sub(P[0],x)),P[1])
    assert mul(y,y)==sub(power(x,3),mul(D,x))
    return x,y


def vp(value,p):
    value=F(value);assert value
    answer=0
    for integer,sign in ((abs(value.numerator),1),(value.denominator,-1)):
        while integer%p==0:
            answer+=sign;integer//=p
    return answer


def mod(value,p):
    value=F(value)
    return value.numerator*pow(value.denominator,-1,p)%p


def quadratic_algebra_product(x,y,u):
    # Basis r^i s^j, ordered 1,r,s,rs; r^2=2 and s^2=-u.
    out=[0,0,0,0]
    for i,xi in enumerate(x):
        for j,yj in enumerate(y):
            ri,si=i%2,i//2;rj,sj=j%2,j//2
            rr,ss=ri+rj,si+sj
            out[(rr%2)+2*(ss%2)]+=xi*yj*(2 if rr==2 else 1)*(-u if ss==2 else 1)
    return tuple(sp.expand(v) if isinstance(v,sp.Basic) else v for v in out)


def symbolic_norm_check():
    a,b,c,d,u=sp.symbols('a b c d u')
    Z=(a,b,c,d)
    Ws=quadratic_algebra_product(Z,(a,b,-c,-d),u)
    assert Ws[2:]==(0,0)
    T=quadratic_algebra_product(Z,(a,-b,c,-d),u)
    assert T[1]==T[3]==0
    left=quadratic_algebra_product(Ws,(Ws[0],-Ws[1],0,0),u)
    right=quadratic_algebra_product(T,(T[0],0,-T[2],0),u)
    assert all(sp.expand(x-y)==0 for x,y in zip(left,right))
    assert sp.expand(left[0]-(T[0]**2+u*T[2]**2))==0
    return True


def all_character_dag(P,R,g,a,z,u,W,V,b):
    path=REPO/'computation/few_variables/seven_contact11_v74/specification/source.json'
    source=json.loads(path.read_text())
    guards=[]
    for node,label in source['guard_descriptions']:
        guards.append(node)
        if label=='intrinsic.input':break
    else:raise AssertionError('Missing native pole boundary')
    guards=sorted(set(guards));assert len(guards)==30
    q=1000000009
    assert all(q%d for d in range(2,isqrt(q)+1))
    rt=int(sp.sqrt_mod(2,q));assert rt*rt%q==2
    names={v['name']:v['index'] for v in source['variables']}
    constant={'input.X':1,'A.a0':g[0],'A.a1':g[1],
              'H.a0':R[0][0],'H.a1':R[0][1],
              'UA.a0':R[0][0],'UA.a1':R[0][1],'contact.z':z}
    js={'A':div(P[1],g),'H':R[1],'UA':R[1]}
    count=0
    for mask in range(64):
        variables=[0]*len(names)
        for name,value in constant.items():variables[names[name]]=mod(value,q)
        for i,name in enumerate(('A','H','UA')):
            j0,j1=js[name]
            plus=mod(j0,q)+rt*mod(j1,q)
            minus=mod(j0,q)-rt*mod(j1,q)
            if (mask>>(2*i))&1:plus=-plus
            if (mask>>(2*i+1))&1:minus=-minus
            variables[names[name+'.U']]=(plus+minus)%q
            variables[names[name+'.V']]=(plus-minus)*pow(rt,-1,q)%q
            variables[names[name+'.W']]=plus*minus%q
        @lru_cache(None)
        def evaluate(node):
            op,*args=source['coefficient_dag'][node]
            if op=='int':value=args[0]
            elif op=='parameter':value=args[1]
            elif op=='variable':value=variables[args[0]]
            elif op=='neg':value=-evaluate(args[0])
            elif op=='add':value=sum(evaluate(k) for k in args)
            elif op=='mul':value=prod(evaluate(k) for k in args)
            elif op=='pow':value=pow(evaluate(args[0]),args[1],q)
            else:raise AssertionError(op)
            return value%q
        def rational(record):
            return evaluate(record['numerator'])*pow(evaluate(record['denominator']),-1,q)%q
        assert all(evaluate(node) for node in guards)
        count+=len(guards)
        if mask==0:
            contact=next(e for e in source['events'] if e['operation']=='moving_contact_height')
            detector=next(e for e in source['events'] if e['operation']=='balanced_actual_detector')
            assert rational(contact['A'])==mod(a,q)
            assert rational(contact['Z'])==mod(z*z,q)
            assert rational(contact['u'])==mod(u,q)
            assert [rational(t) for t in detector['product_components']]==[mod(W,q),0]
            assert rational(detector['trace'])==mod(V,q)
            assert rational(detector['b'])==mod(b,q)
    return {'source_sha256':sha256(path.read_bytes()).hexdigest(),
            'independent_reduction_prime':q,'sqrt2_mod_prime':rt,
            'characters':64,'distinct_guards':30,'nonzero_guard_values':count,
            'selected_character_scale_weight_product_trace_input_checked':True,
            'method':'Recursive DAG evaluation, distinct from producer, at a different split prime.'}


def main():
    report=json.loads((HERE/'certificate.json').read_text())
    saved=report['physical_norm_counterexample']
    assert symbolic_norm_check()
    p=100003;assert all(p%d for d in range(2,isqrt(p)+1))
    D=(F(11),F(-6));R=((F(1),F(1)),(F(0),F(2)))
    P=point_sum(R,R,D);R3=point_sum(R,P,D)
    assert [[str(q) for q in v] for v in P]==saved['P']
    assert [[str(q) for q in v] for v in R3]==saved['triple_R']
    assert all(norm(v) for point in (P,R,R3) for v in point)
    assert norm(sub(P[0],R[0]))
    g=(F(-1),F(7,4));assert mul(g,g)==P[0]
    a=(F(4)**4+F(57,4)**4)**8;z=a+8+p
    roots=(-7,-6,-4,1,3,5,8)
    factors=[(a+c)**2-z*z for c in roots]
    ff=prod(factors)
    derivative=sum(2*(a+c)*prod(factors[:i]+factors[i+1:]) for i,c in enumerate(roots))
    u=-14*ff/derivative
    assert str(a)==saved['scale_a'] and str(z)==saved['slope_z']
    assert str(u)==saved['physical_u'] and u>2*p
    assert {key:mod(value,p*p) for key,value in [('a',a),('z',z),('F',ff),('F_a',derivative)]}==saved['residues_mod_p_squared']
    assert mod(u/p,p)==14
    c=inv(R[0]);cb=(c[0],-c[1]);one=(F(1),F(0))
    tests=[c,c,cb,cb,(F(0),F(0)),(F(0),F(0))]
    actual=one
    for test in tests:
        square=mul(test,test)
        balanced=div(square,add(one,scale(square,u)))
        actual=mul(actual,add(one,scale(mul(balanced,balanced),1/u)))
    denominator=u*u*(u*u+6*u+1)**2
    numerator=denominator+2*u**3+12*u*u+34*u+1
    W=(numerator/denominator)**2
    assert actual==(W,F(0))
    w=u/(1+u)**2;V=2/W;b=4*w/V**2
    values={'F':ff,'F_a':derivative,'u':u,'w':w,'D_poly':denominator,
            'R_poly':numerator,'W':W,'V':V,'b':b,'eta_7b':7*b}
    assert {key:vp(value,p) for key,value in values.items()}==saved['valuations']
    dag=all_character_dag(P,R,g,a,z,u,W,V,b)
    assert dag['source_sha256']==saved['native_pre_pole_guards']['source_sha256']
    certificate={'schema':'native-pole-ramification-independent-check/v75','status':'PASS',
        'imports_project_producer_or_checker':False,'four_coordinate_norm_composition':True,
        'exact_point_duplication_and_tripling':True,'exact_physical_slope_and_derivative':True,
        'exact_actual_balanced_product':True,'fresh_prime_valuations':saved['valuations'],
        'all_character_guard_audit':dag,
        'real_guard_argument':'All point and quotient denominators are nonzero by all-character audit; u>0 and each real test square is nonnegative, so every balanced denominator is positive.',
        'scope':'Independent finite arithmetic and source-DAG verification. General valuation, ramification and abelian-family proofs require the mathematical review; external arithmetic premises are not audited.'}
    (HERE/'independent_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print('PASS: independent physical fixture, norm composition, and 1920 guard values at a second split prime.')


if __name__=='__main__':main()
