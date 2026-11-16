#!/usr/bin/env python3
"""Freeze S-unit coefficients turning the exact fixture into 17m² incidence."""
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json
import argparse
import sympy as sp


HERE=Path(__file__).resolve().parent


def decode(q):
    return F(int(q["numerator"]),int(q["denominator"]))


def encode(q):
    q=F(q)
    return {"numerator":str(q.numerator),"denominator":str(q.denominator)}


def sqrtq(q):
    assert q>0
    n,d=isqrt(q.numerator),isqrt(q.denominator)
    assert n*n==q.numerator and d*d==q.denominator
    return F(n,d)


def main(fixture=None,output=None):
    raw=(fixture or HERE/"fixture.json").read_bytes()
    original=json.loads(raw)
    blocks=[]
    for block in original["blocks"]:
        w=decode(block["weight"])
        a=decode(block["fixedLevel"])
        b=decode(block["actualInput"])
        V=decode(block["actualTraceInverse"])
        W0,W1=map(decode,block["actualW"])
        N=W0*W0-2*W1*W1
        classes={}
        for field,sgn in (("weightNumeratorFactors",1),("weightDenominatorFactors",-1)):
            for p,e in block[field].items():
                p=int(p);classes[p]=classes.get(p,0)+sgn*int(e)
        c=1
        for p,e in classes.items():
            if e%2:c*=p
        cf={int(p):int(e) for p,e in sp.factorint(c).items()}
        assert cf and all(p<=76176 and e==1 for p,e in cf.items())
        r=sqrtq(a/c)
        k=r.denominator
        kf={int(p):int(e) for p,e in sp.factorint(k).items()}
        assert all(p<=76176 for p in kf)
        m=r.numerator
        gamma=F(17*k*k,c)
        wn,bn=gamma*w,gamma*b
        Y=-2*m*W1/N
        assert gamma*a==17*m*m
        assert wn*N==17*m*m
        assert (m*V)**2-2*Y*Y==4*wn/17
        # Scaling is by a fixed S-unit. All outside-S detector valuations
        # and all guard zero sets are therefore unchanged.
        blocks.append({
            "classRepresentative":str(c),
            "classRepresentativePrimeFactors":cf,
            "levelSquareRootOverClass":encode(r),
            "denominatorClearer":str(k),
            "denominatorClearerPrimeFactors":kf,
            "fixedPositiveIntegerM":str(m),
            "fixedWeightCoefficient":encode(gamma),
            "actualRescaledWeight":encode(wn),
            "actualRescaledInput":encode(bn),
            "actualTraceInverse":encode(V),
            "normWitnessY":encode(Y),
            "level":str(17*m*m),
            "normIncidenceEquation":"(mV)^2-2Y^2=4w_rescaled/17",
            "allCharacterGuardRelation":"new(a-b)=gamma*old(a-b)",
        })
    report={
        "status":"PASS_EXACT_FIXED_COEFFICIENT_NATIVE_INCIDENCE",
        "fixtureSha256":sha256(raw).hexdigest(),
        "blocks":blocks,
        "originalExceptionalSet":"all rational primes <=76176",
        "outsideExceptionalSetCoefficientValuations":0,
        "sourceChange":"Each block's physical weight and input are multiplied by its displayed fixed positive rational S-unit coefficient; the actual point tuple, detector products, traces and coupled arguments are unchanged.",
        "limitations":[
            "This is a redesigned fixed-coefficient source, not a solution of the original unscaled17m² incidence problem.",
            "The coefficients are selected from this fixture once and then frozen; no input-dependent normalization is allowed.",
            "Only X=-1,1 and the algebraic coefficient fixture B=3 are realized.",
            "Local soundness at every consumed prime is preserved, but full completeness for the same fixed coefficients is unproved.",
            "No new defining-variable count is asserted."
        ],
    }
    out=output or HERE/"scaling.json"
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":report["status"],"blocks":2,
                      "mDecimalDigits":[len(b["fixedPositiveIntegerM"]) for b in blocks],
                      "receipt":str(out)}))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    main(args.fixture,args.output)
