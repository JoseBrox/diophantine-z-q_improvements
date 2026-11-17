#!/usr/bin/env python3
"""Exact arithmetic and independently traversed seven-contact circuit audit."""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import argparse,ast,hashlib,json,shutil,sys

sys.dont_write_bytecode=True
from build_source import HERE,REPO,old,load,patch_compiler,make_source,check_dependencies
basecheck=load('seven_contact_independent_full_aux',REPO/'computation/few_variables/full_auxiliary11_v71/check.py')

def height_certificate():
    shifts=(-7,-6,-4,1,3,5,8)
    assert len(set(shifts))==7 and sum(shifts)==0
    assert all(x+y!=0 for x in shifts for y in shifts)
    assert max(abs(x-y) for x in shifts for y in shifts)<76176
    assert max(abs(x+y) for x in shifts for y in shifts)<76176
    kappa=F(1001,1000);epsilon=F(1,100)
    alpha=4/kappa-3
    Q=(2*kappa-1)/(16-10*kappa)
    gamma=(7-6-3*epsilon)/2;C=2+epsilon
    margin=gamma-Q*(C+1/(2*alpha))
    assert (alpha,Q,gamma,C,margin)==(F(997,1001),F(501,2995),F(97,200),F(201,100),F(38695561,597203000))
    assert margin>0
    return dict(shifts=list(shifts),scale_exponent=8,signed_argument_exponent=16,
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
        'a=M**4':'a=M**8',
        'shifts=(-10,-8,-5,1,2,3,4,6,7)':'shifts=(-7,-6,-4,1,3,5,8)',
        'u=-18*pow(log_derivative,-1,p)%p':'u=-14*pow(log_derivative,-1,p)%p',
    }
    for before,after in replacements.items():
        assert text.count(before)==1,before;text=text.replace(before,after)
    exec(compile(text,__file__,'exec'),native.__dict__)
    return native

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--specification',type=Path,default=HERE/'specification')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    pins=check_dependencies();height=height_certificate()
    algebra=basecheck.universal_point_algebra()
    pointbounds=basecheck.norm_and_degree_bounds()
    patch_compiler()
    output=args.specification.resolve()
    source=json.loads((output/'source.json').read_text())
    assert source==make_source(source['family_parameter']['value'])
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
    term=load('seven_contact_independent_terminal',REPO/'computation/few_variables/terminal_root_v40/check.py')
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
    report=dict(status='PASS',scope=__doc__,height=height,
        source_sha256=hashlib.sha256((output/'source.json').read_bytes()).hexdigest(),
        universal_point_algebra=algebra,point_operator_bounds=pointbounds,
        checker_adjustments=adjustments,pinned_dependencies=pins,
        bounds=final['bounds'],subalgebra_audit=pa,terminal_audit=ta,
        corruption_controls_rejected=controls,native_records=records,
        characters=sum(r['characters_checked'] for r in records),
        nine_coordinate_completeness_claimed=False)
    target=args.output or output/'independent_certificate.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','height','characters','corruption_controls_rejected']},indent=2))

if __name__=='__main__':main()
