#!/usr/bin/env python3
"""Independent certificate audit for the nine-shift, terminal-root source.

The two imported checkers use independent iterative support and degree
traversals; neither imports the new producer's guard traversal. This script
also certifies retention of every syntactic rational denominator and allows
only the final quadratic root to vanish. Infinite arithmetic premises are
proved in the manuscript, not inferred from these finite checks.
"""
from pathlib import Path
from copy import deepcopy
import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
from build_source import make_source, parent_specification, specification, canonical, _compiler

def module(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

subcheck=module('derivative63_independent_subalgebra_check',HERE.parent/'subalgebra_norms_v30'/'check.py')
termcheck=module('derivative63_independent_terminal_check',HERE.parent/'terminal_root_v40'/'check.py')
termcheck.ROOT=ROOT
oldcheck=module('derivative63_independent_full_norm_check',HERE.parent/'unit_norm_v28'/'check.py')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=HERE/'specification_certificate.json')
    args=ap.parse_args()
    source=make_source(3)
    sourcefile=HERE/'specification/source.json'
    parentfile=HERE/'specification/subalgebra_parent.json'
    parent=json.loads(parentfile.read_text())
    final=json.loads((HERE/'specification/polynomial.json').read_text())
    assert canonical(source)==sourcefile.read_bytes()
    assert canonical(parent)==canonical(parent_specification(source))
    assert canonical(final)==canonical(specification(source,parentfile))
    records=[]
    scratch=HERE/'verification_tmp'
    scratch.mkdir(exist_ok=True)
    oldcache=scratch/'full_norm'
    (oldcache/'specifications').mkdir(parents=True,exist_ok=True)
    subcheck.OLD=oldcache
    try:
        for B in (3,5,81,101):
            native=make_source(B)
            pp=parent_specification(native)
            path=scratch/('parent_B%d.json'%B)
            path.write_text(json.dumps(pp,indent=2)+'\n')
            ss=specification(native,path)
            oldspec=_compiler.compile_specification(native)
            oldcheck.structural_check(native,oldspec)
            (oldcache/'specifications'/(native['name']+'.json')).write_text(json.dumps(oldspec))
            pa=subcheck.verify_spec(native,pp)
            ta=termcheck.verify_spec(native,pp,ss,path)
            assert ss['bounds']['degree_bound']==234157441
            assert ss['bounds']['full_rank']==128
            assert ss['bounds']['total_variables']==11
            assert ss['bounds']['support_strict_power_of_two']==264
            assert ss['bounds']['integer_content']==1
            records.append(dict(B=B,source_nodes=len(native['coefficient_dag']),
                source_guards=len(native['guard_numerators']),
                denominators=ta['source_denominators_checked'],
                omitted_nodes=ta['omitted_nodes'],degree_bound=ta['degree_bound'],
                coefficient_log2_l1_bound=ta['coefficient_log2_l1_bound'],
                norm_dimension_distribution=pa['norm_dimension_distribution']))
        rejected=0
        for mutation in ('degree','denominator'):
            bad=deepcopy(final)
            if mutation=='degree':bad['bounds']['degree_bound']-=1
            else:bad['subalgebra_norm_factors'].pop(0)
            try:termcheck.verify_spec(source,parent,bad,parentfile)
            except AssertionError:rejected+=1
            else:raise AssertionError('Corrupt '+mutation+' certificate accepted')
        assert rejected==2
        (oldcache/'specifications'/(source['name']+'.json')).write_text(json.dumps(_compiler.compile_specification(source)))
        subcheck.verify_spec(source,parent)
        termcheck.verify_spec(source,parent,final,parentfile)
    finally:
        shutil.rmtree(scratch)
    report=dict(status='PASS',scope=__doc__,source_sha256=hashlib.sha256(sourcefile.read_bytes()).hexdigest(),
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        degree_bound=234157441,degree_strict_power_of_two=28,support_strict_power_of_two=264,
        terminal_root_zero_allowed=True,all_preceding_radicands_units=True,
        optional_intrinsic_guards_removed=['s','eta+v^2','eta-v^2'],
        finite_rank=128,variables=11,integer_content=1,corruption_controls_rejected=rejected,
        fixtures=records)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','degree_bound','variables','corruption_controls_rejected')},indent=2))
if __name__=='__main__':main()
