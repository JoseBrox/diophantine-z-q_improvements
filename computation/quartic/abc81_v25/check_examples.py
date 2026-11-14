#!/usr/bin/env python3
"""Exact Q(sqrt(2)) checks of the reciprocal point correspondence.

Finite examples supplement, but do not replace, the universal polynomial
identities and group-law proof. Only Python's standard library is used.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import json

@dataclass(frozen=True)
class K:
    a:Q=Q(0)
    b:Q=Q(0)
    def __post_init__(self):
        object.__setattr__(self,'a',Q(self.a));object.__setattr__(self,'b',Q(self.b))
    @staticmethod
    def coerce(x):return x if isinstance(x,K) else K(x)
    def __add__(self,x):
        x=K.coerce(x);return K(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,x):return self+-K.coerce(x)
    def __rsub__(self,x):return K.coerce(x)+-self
    def __mul__(self,x):
        x=K.coerce(x);return K(self.a*x.a+2*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def inv(self):
        n=self.a*self.a-2*self.b*self.b
        if not n:raise ZeroDivisionError('zero field element')
        return K(self.a/n,-self.b/n)
    def __truediv__(self,x):return self*K.coerce(x).inv()
    def __rtruediv__(self,x):return K.coerce(x)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        y=K(1);x=self
        while n:
            if n&1:y=y*x
            x=x*x;n//=2
        return y
    def __bool__(self):return bool(self.a or self.b)
    def conjugate(self):return K(self.a,-self.b)

D=K(11,-6);d=K(3,-1);ZERO=K();ONE=K(1)
def oncurve(P):return P is None or P[1]**2==P[0]**3-D*P[0]
def neg(P):return None if P is None else (P[0],-P[1])
def add(P,Qp):
    if P is None:return Qp
    if Qp is None:return P
    x,y=P;X,Y=Qp
    if x==X:
        if y+Y==ZERO:return None
        t=(3*x*x-D)/(2*y)
    else:t=(Y-y)/(X-x)
    Xn=t*t-x-X;return Xn,t*(x-Xn)-y

def multiply(n,P):
    if n<0:return multiply(-n,neg(P))
    R=None
    while n:
        if n&1:R=add(R,P)
        P=add(P,P);n//=2
    return R

def reciprocal(P):
    if P is None:return ZERO,ZERO
    x,y=P
    if not x:raise ValueError('The point (0,0) is outside this affine chart.')
    return ONE/x,-y/(x*x)

def run():
    R0=(K(1,1),K(0,2));P=(K(Q(57,8),Q(-7,2)),K(Q(-165,8),Q(417,32)))
    assert oncurve(R0) and add(R0,R0)==P
    torsion=[None,(ZERO,ZERO),(d,ZERO),(-d,ZERO)]
    points=[]
    for m in range(-3,4):
        for i,T in enumerate(torsion):
            U=add(multiply(m,R0),T)
            assert oncurve(U)
            if U==(ZERO,ZERO):continue
            points.append((m,i,U))
    assert len(points)==27 and len({str(p) for _,_,p in points})==27
    H=multiply(5,R0);Hm=add(H,neg(P));SH=H[1]/H[0];TH=Hm[1]/Hm[0]
    count=tangents=identities=torsiondiff=half=ratio_checks=0
    for m,i,U in points:
        for n,j,V in points:
            if U==V:continue
            f,h=reciprocal(U);g,k=reciprocal(V)
            if f==g:
                assert h and k==-h
                s=(ONE-3*D*f*f)/(2*h);tangents+=1
            else:s=(h+k)/(f-g)
            assert h*h==f-D*f**3 and k*k==g-D*g**3
            assert s*(f-g)==h+k
            assert s*(h-k)==ONE-D*(f*f+f*g+g*g)
            c=s*s+D*(f+g);y=D*h-s*(D*f+c)
            A=add(U,neg(V));assert A is not None and A==(c,y)
            assert oncurve(A)
            if U is None or V is None:identities+=1
            if m==n:torsiondiff+=1
            if (m-n)%2:half+=1
            for W,F,J,S in [(U,f,h,SH),(V,g,k,TH)]:
                if W is not None and not W[1]:continue
                z=ZERO if W is None else -W[0]/W[1]
                L=-z*S
                assert J*L+F*S==ZERO
                assert (ONE-D*F*F)*L+J*S==ZERO
                ratio_checks+=1
            count+=1
    assert count==702 and tangents>0 and identities>0 and torsiondiff>0 and half>0
    report=dict(schema='abc81-exact-elliptic-examples/v1',status='PASS',field='Q(sqrt(2))',basePointMultiples=list(range(-3,4)),torsionTranslates=4,pointsInChart=27,orderedPointPairs=count,tangentPairs=tangents,identityPairs=identities,torsionDifferences=torsiondiff,halfIntegralDifferences=half,regularRatioChecks=ratio_checks,arithmetic='Exact rational arithmetic in the specified quadratic field.',scope='Bounded examples only. Universal correspondence and arithmetic projection require the written proofs; no complete defining witness is constructed here.')
    (Path(__file__).resolve().parent/'elliptic-example-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
