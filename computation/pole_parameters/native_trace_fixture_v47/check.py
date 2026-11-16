#!/usr/bin/env python3
"""Independent SymPy number-field verification of the exact native fixture.

Does not import the producer or its Fraction-pair arithmetic.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import argparse
import sympy as s
from sympy.polys.domains import QQ


HERE=Path(__file__).resolve().parent
R=QQ.algebraic_field(s.sqrt(2))
r=R.from_sympy(s.sqrt(2))
one=R.one
zero=R.zero
D=R.convert(11)-6*r


def rat(z):
    return QQ(int(z["numerator"]),int(z["denominator"]))


def elt(z):
    return R.convert(rat(z[0]))+R.convert(rat(z[1]))*r


def bar(z):
    a=z.to_list()
    return R.convert(a[-1])-R.convert(a[0])*r if len(a)==2 else z


def rational(z):
    assert len(z.to_list())<=1
    return z.to_list()[0] if z else QQ.zero


def norm(z):
    return rational(z*bar(z))


def add(P,Q):
    x,y=P;u,v=Q
    if x==u:
        assert y==v and y
        m=(3*x*x-D)/(2*y)
    else:
        m=(v-y)/(u-x)
    xx=m*m-x-u
    return xx,m*(x-xx)-y


def subtract(P,Q):
    return add(P,(Q[0],-Q[1]))


def reciprocal(P):
    assert P[0] and P[1]
    return one/P[0]


def z(P):
    assert P[0] and P[1]
    return -P[0]/P[1]


def verify_factorization(integer,factors):
    answer=1
    for p,e in factors.items():
        p,e=int(p),int(e)
        assert e>0 and s.isprime(p)
        answer*=p**e
    assert answer==abs(int(integer))


def products(alpha,signs,P,H,input_label=1):
    ap,am,hp,hm,up,um=signs
    PA=(P[0],input_label*ap*P[1]); MA=(bar(P[0]),input_label*am*bar(P[1]))
    PH=(H[0],hp*H[1]); MH=(bar(H[0]),hm*bar(H[1]))
    PU=(H[0],input_label*up*H[1]); MU=(bar(H[0]),input_label*um*bar(H[1]))
    MP=(bar(P[0]),bar(P[1]))
    V0p=subtract(PH,P);V0m=subtract(MH,MP)
    V1p=subtract(PU,PA);V1m=subtract(MU,MA)
    for Q in (PA,PH,PU,V0p,V1p):
        assert Q[0] and Q[1]
        assert Q[1]**2==Q[0]**3-D*Q[0]
    for Q in (MA,MH,MU,V0m,V1m):
        assert Q[0] and Q[1]
        assert Q[1]**2==Q[0]**3-bar(D)*Q[0]
    lp=z(PU)/z(PH);lm=z(MU)/z(MH)
    l0p=z(V1p)/z(V0p);l0m=z(V1m)/z(V0m)
    Ds=((reciprocal(PH),reciprocal(PU),reciprocal(V0m),
         reciprocal(V1m),lp-l0m,lp-input_label*one),
        (reciprocal(MH),reciprocal(MU),reciprocal(V0p),
         reciprocal(V1p),lm-l0p,lm-input_label*one))
    ans=[]
    for tests in Ds:
        W=one
        for q in tests:
            factor=one+alpha*q*q
            assert factor
            W*=factor
        ans.append(W)
    return ans


def main(fixture=None,scaling=None,output=None):
    data_path=fixture or HERE/"fixture.json"
    data_bytes=data_path.read_bytes()
    data=json.loads(data_bytes)
    rescaling_bytes=(scaling or HERE/"scaling.json").read_bytes()
    rescaling=json.loads(rescaling_bytes)
    assert rescaling["fixtureSha256"]==sha256(data_bytes).hexdigest()
    assert data["realizedInputs"]==[-1,1]
    source_path=HERE.parents[2]/"papers/conditional_few_variables/direct_input13_20261110_v22.tex"
    assert data["sourceSha256"]==sha256(source_path.read_bytes()).hexdigest()
    assert data["input"]==1 and data["fixedB"]==3 and data["power"]==4
    assert data["enlargedExceptionalSet"] is False
    assert data["class"]==2
    R0=(one+r,2*r)
    P=add(R0,R0)
    H=add(P,P)
    assert P==(R.convert(QQ(57,8))-R.convert(QQ(7,2))*r,
               -R.convert(QQ(165,8))+R.convert(QQ(417,32))*r)
    for half,point,chart in (
        (R0,P,data["rootChart"]),
        (P,H,data["referenceAndNumeratorChart"]),
    ):
        h,j=elt(chart["h"]),elt(chart["j"])
        assert h==(half[0]**2+D)/(2*half[1])
        assert h*h==point[0] and h*j==point[1]
        assert j*j==h**4-D
        aa=h**4-D
        rep=aa.to_list()
        a,b=rep[-1],rep[0] if len(rep)==2 else QQ.zero
        cc,dd=2*a+b,-a-b
        multiplier=R.convert(cc)+R.convert(dd)*r
        transformed=multiplier*j
        reps=transformed.to_list()
        u,v=reps[-1],reps[0] if len(reps)==2 else QQ.zero
        assert u and v and multiplier
        bprime=2*u*v
        roots=[elt(x) for x in chart["scalarRoots"]]
        assert len(set(roots))==4
        actual_signs=[]
        for Y in roots:
            jp=(Y/2+R.convert(bprime)/Y*r)/multiplier
            jm=(Y/2-R.convert(bprime)/Y*r)/bar(multiplier)
            yp=h*jp;ym=bar(h)*jm
            assert yp in (point[1],-point[1])
            assert ym in (bar(point[1]),-bar(point[1]))
            actual_signs.append([1 if yp==point[1] else -1,
                                 1 if ym==bar(point[1]) else -1])
        assert actual_signs==chart["ordinateSignPairs"]
        assert {tuple(z) for z in actual_signs}==set(product((1,-1),repeat=2))
    lam=rat(data["slope"])
    scale=QQ(4)**4+QQ(57,4)**4
    assert scale==rat(data["secondScale"])
    assert lam==QQ(32003072,10621537)
    reciprocal_denominators=set()
    for point in (P,H):
        q=reciprocal(point)
        for c in q.to_list():
            for prime in s.factorint(int(c.denominator)):
                reciprocal_denominators.add(int(prime))
    assert reciprocal_denominators=={41,593,8273}
    assert sorted(reciprocal_denominators)==data["actualReciprocalDenominatorPrimes"]
    theta=(QQ.zero,QQ(-1,2),QQ(-1,4),QQ(-2,5),QQ(-1),QQ(-1,3))
    count=0
    for i,block in enumerate(data["blocks"]):
        t=rat(block["t"])
        assert t==(lam if i==0 else lam*scale)
        delta=t-1
        Fvalue=QQ.one
        for a in theta:Fvalue*=t-a
        w=Fvalue/(4*delta**8)
        alpha=delta**4/Fvalue
        assert Fvalue==rat(block["F"]) and delta==rat(block["delta"])
        assert w==rat(block["weight"]) and alpha==rat(block["alpha"])
        assert w>0 and alpha>0
        verify_factorization(w.numerator,block["weightNumeratorFactors"])
        verify_factorization(w.denominator,block["weightDenominatorFactors"])
        verify_factorization(alpha.denominator,block["alphaDenominatorFactors"])
        assert all(int(p)<=76176 for p in block["weightDenominatorFactors"])
        assert all(int(p)<=76176 for p in block["alphaDenominatorFactors"])
        assert all(int(e)%2==0 for p,e in block["weightNumeratorFactors"].items()
                   if int(p)>76176)
        T=(one+R.convert(alpha)*reciprocal(H)**2)*(
            one+R.convert(alpha)*bar(reciprocal(P))**2)
        W=T*T
        assert W==elt(block["actualW"])
        N=norm(W)
        W0=rational((W+bar(W))/2)
        W1=rational((W-bar(W))/(2*r))
        b=w*(N/W0)**2
        A=w*N
        q=2*w*N*W1/W0
        assert q and 0<b<A
        assert rat(block["actualInput"])==b
        assert rat(block["fixedLevel"])==A
        assert rat(block["complementSquareRootForClass2"])==q
        assert rat(block["actualTraceInverse"])==2*W0/N
        assert rat(block["complement"])==A*(A-b)
        assert q*q==2*A*(A-b)
        assert N==norm(T)**2
        new=rescaling["blocks"][i]
        c=int(new["classRepresentative"])
        k=int(new["denominatorClearer"])
        m=int(new["fixedPositiveIntegerM"])
        gamma=rat(new["fixedWeightCoefficient"])
        rr=rat(new["levelSquareRootOverClass"])
        assert c>0 and k>0 and m>0 and gamma>0
        verify_factorization(c,new["classRepresentativePrimeFactors"])
        verify_factorization(k,new["denominatorClearerPrimeFactors"])
        assert all(int(p)<=76176 and int(e)==1
                   for p,e in new["classRepresentativePrimeFactors"].items())
        assert all(int(p)<=76176
                   for p in new["denominatorClearerPrimeFactors"])
        assert rr*rr==A/c and k*rr==m
        assert gamma==QQ(17*k*k,c)
        assert gamma*A==17*m*m==int(new["level"])
        assert rat(new["actualRescaledWeight"])==gamma*w
        assert rat(new["actualRescaledInput"])==gamma*b
        VV=2*W0/N
        YY=-2*m*W1/N
        assert rat(new["actualTraceInverse"])==VV
        assert rat(new["normWitnessY"])==YY
        assert (m*VV)**2-2*YY**2==4*gamma*w/17
        assert gamma*w*N==17*m*m
        chars={tuple(c["signs"]):elt(c["guard"])
               for c in block["wholeCharacterGuards"]}
        assert len(chars)==64
        for signs in product((1,-1),repeat=6):
            wp,wm=products(R.convert(alpha),signs,P,H)
            assert (wp,wm)==tuple(products(R.convert(alpha),signs,P,H,input_label=-1))
            mid=(wp+wm)/2
            prod=wp*wm
            assert mid and prod
            bc=R.convert(w)*(prod/mid)**2
            guard=R.convert(A)-bc
            assert guard and guard==chars[signs]
            count+=1
        guard_hash=sha256(json.dumps(block["wholeCharacterGuards"],
                                    sort_keys=True).encode()).hexdigest()
        assert guard_hash==block["wholeCharacterGuardSha256"]
    assert count==128
    receipt={
        "status":"PASS_INDEPENDENT_NATIVE_FIXTURE",
        "method":"SymPy exact QQ(sqrt2) arithmetic; no producer import.",
        "dataSha256":sha256(data_bytes).hexdigest(),
        "fixedCoefficientIncidenceSha256":sha256(rescaling_bytes).hexdigest(),
        "actualSourceInputs":[-1,1],"fixedCoefficientFixture":3,
        "negativeInputSignSymmetryChecks":128,
        "wholeCharacterComplementGuards":count,
        "sourcePointCharts":3,
        "sourceFiniteCharacterCount":64,
        "coupledActualArguments":["32003072/10621537","125012"],
        "originalFixtureUsesUnchangedNativeDetectors":True,
        "fixedRescalingChangesOnlyPhysicalWeightAndInput":True,
        "originalExceptionalSetUnchanged":True,
        "fixedLevelAdmissibilityOutsideOriginalS":True,
        "commonComplementClass":2,
        "fixedSUnitCoefficientRescalingChecked":True,
        "actualStandardNormIncidencesAfterFixedRescaling":2,
        "scope":"One exact actual tuple at two enlarged admissible fixed rational levels; equivalently two standard17m² incidences after the certified fixed S-unit source rescalings. This does not solve the original unscaled incidence, uniform completeness, a sufficient B threshold, or a new defining-variable record.",
    }
    output=output or HERE/"verification.json"
    output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps(receipt,sort_keys=True))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture",type=Path)
    parser.add_argument("--scaling",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    main(args.fixture,args.scaling,args.output)
