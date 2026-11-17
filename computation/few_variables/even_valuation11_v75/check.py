#!/usr/bin/env python3
"""Exact arithmetic and independently traversed even-valuation circuit audit."""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import argparse,ast,hashlib,json,shutil,sys

sys.dont_write_bytecode=True
from build_source import HERE,REPO,old,load,patch_compiler,make_source,check_dependencies
basecheck=load('even_valuation_independent_full_aux',REPO/'computation/few_variables/full_auxiliary11_v71/check.py')

def height_certificate(contacts):
    shifts=((-7,-6,-4,1,3,5,8) if contacts==7 else (-10,-8,-5,1,2,3,4,6,7))
    assert len(set(shifts))==contacts and sum(shifts)==0
    assert all(x+y!=0 for x in shifts for y in shifts)
    assert max(abs(x-y) for x in shifts for y in shifts)<76176
    assert max(abs(x+y) for x in shifts for y in shifts)<76176
    kappa=F(1001,1000);epsilon=F(1,100)
    alpha=4/kappa-3
    power=16 if contacts==7 else 8
    Q=(2*kappa-1)/(power-kappa*(power//2+2))
    gamma=(contacts-6-3*epsilon)/2;C=2+epsilon
    margin=gamma-Q*(C+1/(2*alpha))
    assert alpha==F(997,1001) and C==F(201,100)
    assert margin==(F(38695561,597203000) if contacts==7 else F(44272779,198801800))
    assert margin>0
    return dict(shifts=list(shifts),scale_exponent=power//2,signed_argument_exponent=power,
        kappa=str(kappa),epsilon=str(epsilon),alpha=str(alpha),Q=str(Q),
        gamma=str(gamma),C=str(C),strict_absorption_margin=str(margin),
        old_exceptional_set_suffices=True)

def adapted_native():
    native=basecheck.adapted_native_checker()
    path=REPO/'computation/few_variables/derivative11_v63/check_native.py'
    raw=path.read_text();node=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='audit')
    text='\n'.join(raw.splitlines()[node.lineno-1:node.end_lineno])+'\n'
    replacements={
        "chart={name:(ksqrt(point[0]),point[1]/ksqrt(point[0])) for name,point in points.items()}":
          "chart={name:((ksqrt(point[0]),point[1]/ksqrt(point[0])) if name=='A' else point) for name,point in points.items()}",
        """        assert hh**2 == points[name][0]
        assert jj**2 == hh**4-D
        assert hh*jj == points[name][1]""":
        """        if name=='A':
            assert hh**2 == points[name][0]
            assert jj**2 == hh**4-D
            assert hh*jj == points[name][1]
        else:
            assert hh == points[name][0]
            assert jj**2 == hh**3-D*hh
            assert jj == points[name][1]""",
        'a=M**4':"a=M**(8 if source['contact_count']==7 else 4)",
        'shifts=(-10,-8,-5,1,2,3,4,6,7)':"shifts=((-7,-6,-4,1,3,5,8) if source['contact_count']==7 else (-10,-8,-5,1,2,3,4,6,7))",
        'u=-18*pow(log_derivative,-1,p)%p':'u=-2*len(shifts)*pow(log_derivative,-1,p)%p',
        'transformed=[[c*c*pow(1+u*c*c,-1,p)%p for c in C] for C in tests]':
            'transformed=[([c*pow(1+u*c,-1,p)%p for c in C] if i<4 else [c*c*pow(1+u*c*c,-1,p)%p for c in C]) for i,C in enumerate(tests)]',
    }
    for before,after in replacements.items():
        assert text.count(before)==1,before;text=text.replace(before,after)
    exec(compile(text,__file__,'exec'),native.__dict__)
    return native

def even_valuation_certificate():
    import sympy as sp
    x,y,lam,a,b=sp.symbols('x y lam a b')
    assert sp.expand((11-6*sp.sqrt(2))*(11+6*sp.sqrt(2)))==49
    assert sp.cancel((1/x)/(1+lam/x)-1/(x+lam))==0
    assert sp.cancel((a*a/b)/(1+lam*a*a/b)-a*a/(b+lam*a*a))==0
    cases=[]
    for nu in range(-19,20,2):
        for val in range(-20,21,2):
            assert nu+val!=0
            vD=val-min(0,nu+val)
            assert vD==max(val,-nu)
            if nu>0:assert (vD>0)==(val>0)
            else:assert 2*vD-nu>=-3*nu>0
            cases.append((nu,val,vD))
    return dict(norm_curve_coefficient=49,excluded_primes=[2,7],
        positive_abscissa_valuation_relation='2*v(y)=v(x)',
        negative_abscissa_valuation_relation='2*v(y)=3*v(x)',
        normalized_odd_valuation_cases_checked=len(cases),
        direct_balancing_identities=True,
        global_square_of_abscissa_assumed=False)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--specification',type=Path,default=HERE/'specification')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    pins=check_dependencies()
    algebra=basecheck.universal_point_algebra()
    pointbounds=basecheck.norm_and_degree_bounds()
    patch_compiler()
    output=args.specification.resolve()
    source=json.loads((output/'source.json').read_text())
    assert source==make_source(source['family_parameter']['value'],source['contact_count'])
    height=height_certificate(source['contact_count'])
    parity=even_valuation_certificate()
    event=next(e for e in source['events'] if e['operation']=='moving_contact_height')
    assert event['shifts']==height['shifts']
    parent_path=output/'subalgebra_parent.json'
    parent=json.loads(parent_path.read_text());final=json.loads((output/'polynomial.json').read_text())
    subcheck,adjustments=basecheck.adapted_spec_checker()
    olddir=output/'independent_old_cache';(olddir/'specifications').mkdir(parents=True,exist_ok=True)
    oldspec=old._subalgebra._old.compile_specification(source)
    (olddir/'specifications'/(source['name']+'.json')).write_text(json.dumps(oldspec))
    subcheck.OLD=olddir
    pa=subcheck.verify_spec(source,parent);shutil.rmtree(olddir)
    term=load('even_valuation_independent_terminal',REPO/'computation/few_variables/terminal_root_v40/check.py')
    term.ROOT=output
    ta=term.verify_spec(source,parent,final,parent_path)
    controls=0
    for mutation in ['degree','guard']:
        bad=deepcopy(final)
        if mutation=='degree':bad['bounds']['degree_bound']-=1
        else:bad['subalgebra_norm_factors'].pop(0)
        try:term.verify_spec(source,parent,bad,parent_path)
        except AssertionError:controls+=1
        else:raise AssertionError('Corruption accepted: '+mutation)
    native=adapted_native();records=[]
    for p in [1000000007,1000000009]:
        for n,h in [(1,F(1,2)),(2,F(3,2)),(3,F(5,2))]:
            r=native.audit(source,p,n,h)
            r['auxiliary_index']=str(r['auxiliary_index'])
            r['actual_indices']={k:str(v) for k,v in r['actual_indices'].items()}
            records.append(r)
    report=dict(status='PASS',scope=__doc__,height=height,even_valuation=parity,
        source_sha256=hashlib.sha256((output/'source.json').read_bytes()).hexdigest(),
        universal_point_algebra=algebra,point_operator_bounds=pointbounds,
        checker_adjustments=adjustments,pinned_dependencies=pins,
        bounds=final['bounds'],subalgebra_audit=pa,terminal_audit=ta,
        corruption_controls_rejected=controls,native_records=records,
        characters=sum(r['characters_checked'] for r in records),
        nine_coordinate_completeness_claimed=False)
    target=args.output or output/'independent_certificate.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','height','even_valuation','characters','corruption_controls_rejected']},indent=2))

if __name__=='__main__':main()
