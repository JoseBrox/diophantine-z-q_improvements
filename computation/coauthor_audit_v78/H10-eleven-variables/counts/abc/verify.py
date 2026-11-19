"""Arithmetic identities and independent checks of both guarded determinant specifications."""
import argparse
from fractions import Fraction as Fr
from hashlib import sha256
import importlib.util
import json
from math import prod
from pathlib import Path
import random
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def valuation(n,p):
    if not n:
        raise ValueError("Exact zero has infinite valuation")
    if n%p:
        return 0
    count=0
    while n%p==0:
        count+=1
        n//=p
    return count

def valuation_checks(k):
    tested=0
    for p in (2,3,5,7,11,19):
        for j in range(k):
            for left_unit,right_unit in ((1,1),(1,-1),(1,p-1),(1,p*p-1),(2*p+1,3*p+1)):
                for flip in (False,True):
                    g,h=p*left_unit,p**j*right_unit
                    if flip:
                        g,h=h,g
                    linear=g+h
                    f=g*h
                    q=(linear**3+g*g*h*h)*(linear**2+g*g*h)*(g**k+h)*(g+h**k)
                    assert q and 1+q*f
                    vu=5*valuation(f,p)+2*valuation(1+q*f,p)-valuation(q,p)
                    expected=5 if j==0 else (4*j-1 if j>1 else (3 if linear and valuation(linear,p)==1 else 1))
                    assert vu==expected,(k,p,g,h,expected,vu)
                    tested+=1
    return tested

def dag_values(nodes,variables,p):
    out=[]
    for op,*args in nodes:
        if op=="int": v=args[0]
        elif op=="parameter": v=args[1]
        elif op=="variable": v=variables[args[0]]
        elif op=="neg": v=-out[args[0]]
        elif op=="add": v=sum(out[i] for i in args)
        elif op=="mul": v=prod(out[i] for i in args)
        elif op=="pow": v=pow(out[args[0]],args[1],p)
        else: raise ValueError(op)
        out.append(v%p)
    return out

def contact_checks(source, kappa):
    event=next(e for e in source["events"] if e["operation"]=="weak_abc_collision_resolvent")
    d,m,k=(event[i] for i in ("d","m","K"))
    gamma=8/kappa-6
    alpha=d/kappa-3
    compact="normalization" in event
    margin=(gamma-Fr(6,k))*m/2-int(not compact)-1/(2*alpha)
    assert margin>0
    assert event["shifts"]==[0,15,20,24,30,60]
    assert set(event["shifts"])=={-60*t for t in (0,-Fr(1,2),-Fr(1,4),-Fr(2,5),-1,-Fr(1,3))}
    rng=random.Random(111)
    successes=0
    for p in (101,137,241,659,1009):
        for _ in range(10):
            variables=[rng.randrange(1,p) for _ in source["variables"]]
            values=dag_values(source["coefficient_dag"],variables,p)
            def get(key):
                e=event[key]
                return values[e["numerator"]]*pow(values[e["denominator"]],-1,p)%p
            beta=(variables[0]**2+source["fixed_parameters"]["fixed_input_shift"])%p
            # The square-abscissa chart stores h=h0+h1 sqrt(2), x(A)=h^2.
            trace=2*(variables[1]**2+2*variables[2]**2)%p
            scale=(pow(beta,d,p)+pow(trace,d,p))%p
            a=pow(scale,m,p)
            x,y=(a-variables[7])%p,(a+variables[7])%p
            g,h=(prod(t+c for c in event["shifts"])%p for t in (x,y))
            f=g*h%p
            l=(g+h)%p
            n=(l**3+f**2)%p
            den=(l**2+g*f)%p
            q=n*den*(pow(g,k,p)+h)*(g+pow(h,k,p))%p
            want=dict(beta=beta,T=trace,M=scale,a=a,x=x,y=y,g=g,h=h,L=l,F=f,N=n,D=den,Q=q)
            assert all(get(key)==v for key,v in want.items())
            r=(1+pow(scale,3*m*(k+11),p)*f)%p if compact else 1
            if compact: assert get("normalization")==r
            if q and r:
                assert get("u")==pow(f,5,p)*pow(1+q*f,2,p)*pow(q*r*r,-1,p)%p
                successes+=1
    if compact:
        for t in range(1,40):
            e=6*m*t
            qv=-(k+6)*e
            fv=1-e
            raw=5*fv+2*min(0,qv+fv)-qv
            normalized=raw-2*min(0,fv-3*m*(k+11)*t)
            assert normalized==5
    return dict(margin=str(margin),direct_dag_evaluations=successes,
                valuation_fixtures=valuation_checks(k))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,default=HERE.parents[1]/"source")
    args=parser.parse_args()
    root=args.repo.resolve()/"computation/few_variables"
    v63=load("native63_audit",root/"derivative11_v63/build_source.py")
    v28=load("original28_check",root/"unit_norm_v28/check.py")
    v30=load("independent30_check",root/"subalgebra_norms_v30/check.py")
    v40=load("independent40_check",root/"terminal_root_v40/check.py")
    records={}
    for flavor in ("weak","strong","weak-compact","strong-compact"):
        kappa=Fr(121,100) if flavor.startswith("weak") else Fr(16,15)
        folder=HERE/flavor
        source=json.loads((folder/"source.json").read_text())
        parent_path=folder/"subalgebra_parent.json"
        parent=json.loads(parent_path.read_text())
        result=json.loads((folder/"polynomial.json").read_text())
        cert=json.loads((folder/"certificate.json").read_text())
        for filename,digest in cert["hashes"].items():
            assert sha256((folder/filename).read_bytes()).hexdigest()==digest
        with tempfile.TemporaryDirectory() as temp:
            v30.OLD=Path(temp)
            cache=Path(temp)/"specifications"
            cache.mkdir()
            base=v63._compiler.compile_specification(source)
            v28.structural_check(source,base)
            (cache/(source["name"]+".json")).write_text(json.dumps(base))
            v30.verify_spec(source,parent)
            v40.ROOT=folder
            report=v40.verify_spec(source,parent,result,parent_path)
        assert result["bounds"]["integer_content"]==1
        assert result["bounds"]["total_variables"]==11 and result["bounds"]["full_rank"]==128
        records[flavor]=dict(**contact_checks(source,kappa),
            checked_source_denominators=report["source_denominators_checked"],
            degree_bound=report["degree_bound"],content=1,finite_rank=128,variables=11)
    print(json.dumps(records,indent=2))

if __name__=="__main__":
    main()
