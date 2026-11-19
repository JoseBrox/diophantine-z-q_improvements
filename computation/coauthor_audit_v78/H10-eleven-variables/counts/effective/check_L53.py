"""Finite integer checks in the L=53 soundness proof for the three-scale 27-family."""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, prod
from pathlib import Path
import json
def prime_support(z):
    n=abs(z)
    assert n>0
    d=2;result=set()
    while d*d<=n:
        if n%d==0:
            result.add(d)
            while not n%d:n//=d
        d=3 if d==2 else d+2
    if n>1:result.add(n)
    return result
def support(values):
    ret=set()
    for val in values:ret|=prime_support(val.numerator)|prime_support(val.denominator)
    return ret
def factors(vals):return [a-b for a,b in combinations(vals,2)]
def main():
    base={2,3,5,7,11,13,17,37,41,2399}
    theta=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    contacts=[[shift+u for shift in (4*j+2,4*j+4) for u in theta] for j in range(3)]
    poles=[v+[F(-1-j)] for j,v in enumerate(contacts)]
    common=base|support(poles[0])
    for a,b,c in product(*poles):
        common|=prime_support(gcd((a-b).numerator,(a-c).numerator))
    scalar=common|support(factors([F(0),F(1),F(2401),F(-343,32),F(1,2)]))
    ell=76249
    assert ell not in scalar and ell not in set().union(*(support(factors(y)) for y in poles))
    assert prime_support(ell)=={ell}
    for x in range(ell):
        b=216*x**4+450459
        assert b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)%ell
    cstar=F(74712001,10**6)*2**68*3**16*5**16*7**4
    J=prod(scalar); Es=prod(F(p+1,p) for p in scalar)
    assert 2*cstar*J*J*Es*J.bit_length()<2**342
    outputs=[]
    for j in range(3):
        G=common|support(factors(poles[j]))
        K=prod(base)**2;E=prod(F(p+1,p)**2 for p in base)
        for p in G-base:
            exp=1+int(any((a-b).numerator%p==0 for a in contacts[j][:5] for b in contacts[j][5:]))
            K*=p**exp
            E*=F(p+1,p)**exp
        assert K<2**398 and cstar*K*E<2**550
        outputs.append(dict(exceptional=sorted(G),J_bits=prod(G).bit_length(),joint_coefficient=K))
    A=ell**107; T=1735
    assert A-1>=2**T and A>=120*2**342
    assert 2**(T-3*551)*12**6>9**3*(2400+7*T)**6
    assert 200**2<2**16 and 200*(551+3+16)<199*574
    assert A>10**6
    result=dict(L=53,ell=ell,common_exceptional=sorted(common),scalar_exceptional=sorted(scalar),scalar_coefficient_power=342,contact_coefficient_power=551,contact_log_shift=199,comparison_data=outputs,forced_lower_bound_bits=T)
    p=Path(__file__).with_name('L53.json');p.write_text(json.dumps(result,indent=2)+'\n');print('PASS: scalar and three comparison prime sets, four modular constants, L=53 quantitative contradictions.')
if __name__=='__main__':main()
