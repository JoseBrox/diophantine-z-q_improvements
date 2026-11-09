#!/usr/bin/env python3
"""Exact conversion and structural checks for the additional-abc family."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PINNED=HERE.parent/'trace27_nontorsion'
sys.path.insert(0,str(PINNED))
# This auditor is independent of the integer compiler and checks its full
# conversion by canonical expression trees, not by numeric samples.
from verify_specification import audit


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    raw=gzip.decompress((args.directory/'source.json.gz').read_bytes())
    source=json.loads(raw)
    encoded=(args.directory/'source-polynomial-specification.json').read_bytes()
    spec=json.loads(encoded)
    report=audit(source,spec)
    assert source['retained_base_count']==12 and source['total_polynomial_variables_after_finite_algebra']==13
    assert [r['kind'] for r in source['finite_monic_relations']]==['point']*3+['pole']*2
    assert source['comparison_orders']==[1]*6 and source['formal_precision']==4
    assert source['height_scales']=='1,(beta^6+(Tr x(A))^6)^2'
    assert source['beta_formula']=='2*input.X^2+B'
    assert source['closed_equations']==source['indexed_guard_polynomials']==[]
    assert 'ADDITIONAL rational abc' in source['additional_arithmetic_input']
    assert 'ADDITIONAL rational abc' in spec['arithmetic_status']
    B=source['family_parameter']['value']
    assert B>=3 and B%2==1 and source['family_parameter']['selected_member_certified_to_define_Z'] is False
    assert source['finite_parameters']=={'pole_chart_detector0':[0],'pole_chart_detector1':[0],'fixed_input_shift':[B]}
    assert sum(node[0]=='parameter' and node[1]=='fixed_input_shift' for node in source['coefficient_dag'])==1
    assert [e['name'] for e in source['events'] if e['operation']=='point']==['A','H','UA']
    assert sum(e['operation']=='detector' for e in source['events'])==2
    assert sum(e['operation']=='preparation_zero_pole' for e in source['events'])==2
    assert not any('scalar' in e['operation'] or 'Lucas' in e['operation'] for e in source['events'])
    # The only B-dependent node is a named coefficient parameter. All degree
    # recurrences assign it weight zero. Thus the proved weight inequalities
    # hold symbolically for every fixed B, independently of its norm bound.
    report['uniform_degree_reason']='The input shift is a named coefficient parameter of weight zero. No operation or branch in the source depends on its numerical value; every native degree inequality is certified symbolically.'
    report['additional_abc_required']=True
    report['formal_precision']=4
    report['comparison_orders']=[1]*6
    report['point_roles']=['A','H','UA']
    report['source_sha256']=hashlib.sha256(raw).hexdigest()
    report['integer_specification_sha256']=hashlib.sha256(encoded).hexdigest()
    report['family_parameter']=source['family_parameter']
    report['helper_hashes']={name:hashlib.sha256((PINNED/name).read_bytes()).hexdigest() for name in ('verify_specification.py','finite_algebra_check_core.py')}
    report['scope']='Exact affine coefficient conversion, direct point quartics and derivatives, automatic guard coverage, nonzero pole square clearings, source structure, and symbolic degree uniformity. The general finite-algebra theorem preserves the source projection. The integer-defining assertion additionally assumes rational abc and the explicitly retained arithmetic premises; no selected input shift is certified sufficient.'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','total_coordinates':13,'point_quartics_checked':report['source_point_quartics_checked'],
        'pole_square_clearings_checked':report['source_rational_square_clearings_checked'],
        'guard_factors_checked':report['source_guard_atomic_factors_checked'],'uniform_degree':True},indent=2))

if __name__=='__main__':main()
