#!/usr/bin/env python3
"""Exact split-prime norm-height cancellation at the odd point [5]P.

Uses rational pairs for Q(sqrt(2)), two independent addition chains,
primitive minimal polynomials, and certified Hensel residues. Standard
library only; no numerical height approximation or factorization oracle.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

D=(F(11),F(-6))
P=((F(57,8),F(-7,2)),(F(-165,8),F(417,32)))


def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,n): return (a[0]*n,a[1]*n)


def inverse(a):
    norm=a[0]*a[0]-2*a[1]*a[1]
    assert norm
    return (a[0]/norm,-a[1]/norm)


def divide(a,b): return mul(a,inverse(b))


def point_add(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A; z,w=B
    if x==z:
        if y==neg(w):return None
        slope=divide(sub(scale(mul(x,x),3),D),scale(y,2))
    else:
        slope=divide(sub(w,y),sub(z,x))
    X=sub(sub(mul(slope,slope),x),z)
    Y=sub(mul(slope,sub(x,X)),y)
    return X,Y


def valuation_integer(n,p):
    assert n
    v=0
    while n%p==0:n//=p;v+=1
    return v


def serialize_pair(pair): return [str(x) for x in pair]


def main():
    P2=point_add(P,P)
    P4=point_add(P2,P2)
    Q=point_add(P,P4)
    assert Q==point_add(point_add(P2,P),P2)
    x,y=Q
    assert mul(y,y)==sub(mul(mul(x,x),x),mul(D,x))
    a,b=x
    assert b!=0
    den=lcm(a.denominator,b.denominator)
    an=int(a*den); bn=int(b*den)
    assert gcd(gcd(an,bn),den)==1
    norm_numerator=an*an-2*bn*bn
    norm_content=gcd(abs(norm_numerator),den*den)
    polynomial_content=gcd(norm_content,abs(2*an*den))
    assert norm_content//polynomial_content==137**2
    primitive=[norm_numerator//polynomial_content,
               -2*an*den//polynomial_content,
               den*den//polynomial_content]
    assert gcd(gcd(abs(primitive[0]),abs(primitive[1])),primitive[2])==1
    assert add(add(scale(mul(x,x),primitive[2]),scale(x,primitive[1])),
               (F(primitive[0]),F(0)))==(F(0),F(0))
    # Both conjugates exceed one, proved by a rational square comparison.
    assert a>1 and (a-1)**2>2*b*b

    prime, precision=137,8
    assert all(prime%d for d in range(2,12))
    modulus=prime**precision
    root=31
    for _ in range(8):
        root=(root-(root*root-2)*pow(2*root,-1,modulus))%modulus
    assert (root*root-2)%modulus==0 and root%prime==31
    vd=valuation_integer(den,prime)
    roots=(root,(-root)%modulus)
    vals=[]
    residues=[]
    for r in roots:
        residue=(an+bn*r)%modulus
        assert residue
        vnum=valuation_integer(residue,prime)
        assert vnum<precision
        vals.append(vnum-vd)
        residues.append(residue)
    assert sorted(vals)==[-2,2]
    result={
        "status":"PASS",
        "point":"[5]P",
        "point_x":serialize_pair(x),"point_y":serialize_pair(y),
        "two_independent_addition_chains_agree":True,
        "common_denominator":str(den),"numerator_components":[str(an),str(bn)],
        "primitive_minimal_polynomial_ascending":[str(c) for c in primitive],
        "both_real_abscissas_greater_than_one":True,
        "prime":prime,"sqrt2_residues_mod_prime":[31,106],
        "hensel_precision":precision,"hensel_roots":[str(r) for r in roots],
        "numerator_residues":[str(r) for r in residues],
        "denominator_prime_valuation":vd,"split_abscissa_valuations":vals,
        "exact_height_identity":"h(Norm(x([5]P))) = 2 h(x([5]P)) - 2 log(137)",
        "unbounded_defect_sequence":"n_r=5*137^r; split valuations are +/-2(r+1)",
        "scope":"All displayed finite identities and valuations are exact. The infinite sequence follows from the formal-group proof, not from numerical extrapolation.",
        "script_sha256":sha256(Path(__file__).read_bytes()).hexdigest()
    }
    here=Path(__file__).resolve().parent
    (here/'odd-norm-cancellation-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','point_x','split_abscissa_valuations','exact_height_identity')},indent=2))


if __name__=='__main__':main()
