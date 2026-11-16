#!/usr/bin/env python3
"""Exact native input-one fixture with two enlarged admissible fixed levels.

This uses the unchanged conditional source detector and the original fixed
exceptional set. The levels are computed rational S-integers, not required
to be 17 times integer squares. Every whole-point-algebra character is
checked. This is one algebraic fixture for B=3, not uniform completeness or
a certificate that B=3 is beyond the defining family's ineffective bound.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
import argparse
import sympy as sp


@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def lift(z):
        return z if isinstance(z, K) else K(z)

    def __add__(self, z):
        z=K.lift(z)
        return K(self.a+z.a,self.b+z.b)

    __radd__=__add__

    def __neg__(self):
        return K(-self.a,-self.b)

    def __sub__(self,z):
        return self+-K.lift(z)

    def __rsub__(self,z):
        return K.lift(z)+-self

    def __mul__(self,z):
        z=K.lift(z)
        return K(self.a*z.a+2*self.b*z.b,self.a*z.b+self.b*z.a)

    __rmul__=__mul__

    def norm(self):
        return self.a*self.a-2*self.b*self.b

    def bar(self):
        return K(self.a,-self.b)

    def inverse(self):
        n=self.norm()
        assert n
        return K(self.a/n,-self.b/n)

    def __truediv__(self,z):
        return self*K.lift(z).inverse()

    def __rtruediv__(self,z):
        return K.lift(z)*self.inverse()

    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        ans=K(1);base=self
        while n:
            if n&1:ans=ans*base
            base=base*base;n//=2
        return ans

    def positive(self):
        # Exact sign at the embedding sqrt2>0.
        if not self.b:return self.a>0
        if self.a>=0 and self.b>=0:return True
        if self.a<=0 and self.b<=0:return False
        if self.a>0:return self.a*self.a>2*self.b*self.b
        return 2*self.b*self.b>self.a*self.a


D=K(11,-6)
rho=K(0,1)


def add_point(P,Q):
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u:
        if y==-v:return None
        assert y==v and y!=K()
        slope=(3*x*x-D)/(2*y)
    else:
        slope=(v-y)/(u-x)
    xx=slope*slope-x-u
    return xx,slope*(x-xx)-y


def minus_point(P):
    return P[0],-P[1]


def subtract_point(P,Q):
    return add_point(P,minus_point(Q))


def reciprocal(P):
    assert P is not None
    return 1/P[0]


def zcoord(P):
    assert P is not None
    return -P[0]/P[1]


def curve_check(P):
    assert P is not None
    x,y=P
    assert x!=K() and y!=K()
    assert y*y==x*x*x-D*x


def encode_q(q):
    return {"numerator":str(q.numerator),"denominator":str(q.denominator)}


def encode_k(q):
    return [encode_q(q.a),encode_q(q.b)]


def factor(n):
    return {int(p):int(e) for p,e in sp.factorint(abs(int(n))).items()}


def support(q):
    return set(factor(q.numerator))|set(factor(q.denominator))


def field_support(q):
    return support(q.a)|support(q.b)


def point_chart(half,point):
    h=(half[0]*half[0]+D)/(2*half[1])
    j=point[1]/h
    assert h*h==point[0] and j*j==h**4-D
    a,b=(h**4-D).a,(h**4-D).b
    c,d=2*a+b,-a-b
    multiplier=K(c,d)
    transformed=multiplier*j
    u,v=transformed.a,transformed.b
    aa,bb=(multiplier**2*(h**4-D)).a,(multiplier**2*(h**4-D)).b
    assert aa==u*u+2*v*v and bb==2*u*v
    assert u and v and multiplier.norm()
    roots=(K(2*u),K(-2*u),2*rho*v,-2*rho*v)
    signs=[]
    for Y in roots:
        assert Y**4-4*aa*Y**2+8*bb*bb==K()
        jplus=(Y/2+(bb/Y)*rho)/multiplier
        jminus=(Y/2-(bb/Y)*rho)/multiplier.bar()
        yp=h*jplus
        ym=h.bar()*jminus
        assert yp in (point[1],-point[1])
        assert ym in (point[1].bar(),-point[1].bar())
        signs.append((1 if yp==point[1] else -1,
                      1 if ym==point[1].bar() else -1))
    assert set(signs)==set(product((1,-1),repeat=2))
    return h,j,{"h":encode_k(h),"j":encode_k(j),
                "scalarRoots":[encode_k(Y) for Y in roots],
                "ordinateSignPairs":[list(s) for s in signs]}


def source_products(alpha,signs,P,H,input_label=1):
    # The same abstract K is used to evaluate all 64 geometric characters.
    # The second component of each pair is the conjugate-slot value; at
    # non-rational characters it need not be the conjugate of the first.
    ap,am,hp,hm,up,um=signs
    Aplus=(P[0],input_label*ap*P[1]);Aminus=(P[0].bar(),input_label*am*P[1].bar())
    Hplus=(H[0],hp*H[1]);Hminus=(H[0].bar(),hm*H[1].bar())
    Uplus=(H[0],input_label*up*H[1]);Uminus=(H[0].bar(),input_label*um*H[1].bar())
    Pminus=(P[0].bar(),P[1].bar())
    V0plus=subtract_point(Hplus,P)
    V0minus=subtract_point(Hminus,Pminus)
    V1plus=subtract_point(Uplus,Aplus)
    V1minus=subtract_point(Uminus,Aminus)
    assert all(Q is not None and Q[0]!=K() and Q[1]!=K()
               for Q in (V0plus,V0minus,V1plus,V1minus))
    Lplus=zcoord(Uplus)/zcoord(Hplus)
    Lminus=zcoord(Uminus)/zcoord(Hminus)
    L0plus=zcoord(V1plus)/zcoord(V0plus)
    L0minus=zcoord(V1minus)/zcoord(V0minus)
    tests_plus=(reciprocal(Hplus),reciprocal(Uplus),
                reciprocal(V0minus),reciprocal(V1minus),
                Lplus-L0minus,Lplus-input_label)
    tests_minus=(reciprocal(Hminus),reciprocal(Uminus),
                 reciprocal(V0plus),reciprocal(V1plus),
                 Lminus-L0plus,Lminus-input_label)
    values=[]
    for tests in (tests_plus,tests_minus):
        W=K(1)
        for test in tests:
            factor_value=1+alpha*test*test
            assert factor_value.positive() and factor_value.bar().positive()
            W*=factor_value
        values.append(W)
    return tuple(values)


def main(output=None):
    home=Path(__file__).resolve().parent
    B=3
    X=1
    power=4
    exception_bound=76176
    scale_numerator=10621537
    u=125012
    lam=F(256*u,scale_numerator)
    R0=(K(1,1),K(0,2))
    P=add_point(R0,R0)
    assert P==(K(F(57,8),F(-7,2)),K(F(-165,8),F(417,32)))
    H=add_point(P,P)
    curve_check(P);curve_check(H)
    root_h,root_j,root_chart=point_chart(R0,P)
    aux_h,aux_j,aux_chart=point_chart(P,H)
    trace=2*P[0].a
    a1=F((X*X+B)**power)+trace**power
    assert a1==F(scale_numerator,256)
    args=(lam,a1*lam)
    assert args[1]==u
    assert all(t>1 for t in args)
    # Denominators of the actual reciprocal tests are all S-supported.
    constant_denominators=set()
    for q in (reciprocal(H),reciprocal(P)):
        constant_denominators |= set(factor(q.a.denominator))
        constant_denominators |= set(factor(q.b.denominator))
    assert max(constant_denominators)<=exception_bound

    theta=(F(0),F(-1,2),F(-1,4),F(-2,5),F(-1),F(-1,3))
    blocks=[]
    for t in args:
        delta=t-1
        Fval=F(1)
        for contact in theta:Fval*=t-contact
        weight=Fval/(4*delta**8)
        alpha=delta**4/Fval
        # These certificates prove the level is integral with even
        # valuation outside the ORIGINAL S, without factoring its huge
        # numerator.
        alpha_den=factor(alpha.denominator)
        wnum=factor(weight.numerator)
        wden=factor(weight.denominator)
        assert max(alpha_den,default=1)<=exception_bound
        assert max(wden,default=1)<=exception_bound
        assert all(e%2==0 for p,e in wnum.items() if p>exception_bound)
        T=(1+alpha*reciprocal(H)**2)*(1+alpha*reciprocal(P).bar()**2)
        W=T*T
        a,c=W.a,W.b
        nw=W.norm()
        assert nw>0 and a>0 and c
        physical_b=weight*(nw/a)**2
        level=weight*nw
        complement=level*(level-physical_b)
        witness=2*weight*nw*c/a
        assert complement>0 and witness*witness==2*complement
        assert level>physical_b>0
        # All 64 character evaluations, not just the selected rational
        # character, have every detector guard and this complement guard.
        all_chars=[]
        for signs in product((1,-1),repeat=6):
            plus,minus=source_products(alpha,signs,P,H)
            assert (plus,minus)==source_products(alpha,signs,P,H,input_label=-1)
            zero=(plus+minus)/2
            nn=plus*minus
            assert zero!=K() and nn!=K()
            bchar=weight*(nn/zero)**2
            guard=level-bchar
            assert guard!=K()
            all_chars.append({"signs":list(signs),"guard":encode_k(guard)})
            if signs==(1,1,1,1,1,1):
                assert plus==W and minus==W.bar()
                assert bchar==K(physical_b)
        # Exact rational incidence in a general fixed level A:
        # A(A-b) has class2; no 17m² representation is asserted.
        blocks.append({
            "t":encode_q(t),"F":encode_q(Fval),"delta":encode_q(delta),
            "weight":encode_q(weight),"alpha":encode_q(alpha),
            "weightNumeratorFactors":wnum,"weightDenominatorFactors":wden,
            "alphaDenominatorFactors":alpha_den,
            "actualW":encode_k(W),"actualTraceInverse":encode_q(2*a/nw),
            "actualInput":encode_q(physical_b),
            "fixedLevel":encode_q(level),
            "complementSquareRootForClass2":encode_q(witness),
            "complement":encode_q(complement),
            "wholeCharacterGuardChecks":len(all_chars),
            "wholeCharacterGuardSha256":
                sha256(json.dumps(all_chars,sort_keys=True).encode()).hexdigest(),
            "wholeCharacterGuards":all_chars,
        })
    report={
        "status":"PASS_EXACT_NATIVE_TWO_BLOCK_FIXTURE",
        "input":X,"realizedInputs":[-1,1],"fixedB":B,"power":power,
        "negativeInputSignSymmetryChecked":True,
        "sourceSha256":sha256((home.parents[2]/"papers/conditional_few_variables/direct_input13_20261110_v22.tex").read_bytes()).hexdigest(),
        "source":"direct_input13_20261110_v22.tex, unchanged point and detector functions",
        "rootIndex":1,"referenceIndex":2,"numeratorIndex":2,
        "slope":encode_q(lam),"secondScale":encode_q(a1),
        "originalExceptionalSet":"all rational primes <=76176",
        "enlargedExceptionalSet":False,
        "class":2,
        "levelScope":"Two computed fixed positive rational levels, integral with even valuations outside the original exceptional set; they are not required to have class17.",
        "actualReciprocalDenominatorPrimes":sorted(constant_denominators),
        "rootChart":root_chart,"referenceAndNumeratorChart":aux_chart,
        "blocks":blocks,
        "limitations":[
            "Only the integer inputs -1 and 1 and the coefficient fixture B=3 are treated.",
            "The fixed levels have been chosen from this tuple, then frozen; uniform completeness for these same levels is unproved.",
            "This does not solve the narrower equation with levels17m².",
            "The original pole preparation conditions are not asserted; direct all-character guards and the generalized fixed-level local implication are used.",
            "No new defining-variable count or sufficient coefficient threshold is claimed.",
        ],
    }
    out=output or home/"fixture.json"
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":report["status"],"input":X,"B":B,
                      "slope":str(lam),"arguments":[str(t) for t in args],
                      "characterChecks":sum(b["wholeCharacterGuardChecks"] for b in blocks),
                      "reciprocalDenominatorPrimes":sorted(constant_denominators),
                      "receipt":str(out)}))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    main(parser.parse_args().output)
