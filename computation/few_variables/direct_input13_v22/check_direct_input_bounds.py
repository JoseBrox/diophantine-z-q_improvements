#!/usr/bin/env python3
"""Independent active-algebra bounds and the final input-factor identity."""
from __future__ import annotations
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'active_elimination'))
import check_active_specification as active


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('variant',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    variant=args.variant
    active.SOURCES[13]=variant/'certificate/source-polynomial-specification.json'
    inner=variant/'independent-active-bound-verification.json'
    sys.argv=[active.__file__,str(variant/'active13'),'--output',str(inner)]
    active.main()
    base_raw=(variant/'active13/polynomial-specification.json').read_bytes()
    base=json.loads(base_raw)
    receipt=json.loads((variant/'active13/construction-certificate.json').read_text())
    raw=(variant/'definition-polynomial-specification.json').read_bytes()
    final=json.loads(raw)
    assert final['format']=='integer-polynomial-times-input/v1'
    assert final['base_specification']=='active13/polynomial-specification.json'
    assert final['base_specification_sha256']==hashlib.sha256(base_raw).hexdigest()
    assert final['external_variables']==base['external_variables']
    assert final['external_variables'][0]['name']=='input.X'
    assert final['total_variables']==len(final['external_variables'])==13
    assert final['polynomial_recipe']=={'base_name':'Q_B','final_name':'F_B',
        'expression':'input.X * Q_B','multiplier_variable_index':0}
    assert final['family_parameter']==base['family_parameter']
    assert final['family_parameter']['selected_member_certified_to_define_Z'] is False
    assert final['arithmetic_status']==base['arithmetic_status']
    D=receipt['degree_bound'];E=127*256
    support=comb(D+13,13)-comb(D-E+12,13)
    bounds=final['bounds']
    assert bounds['base_degree_bound']==D and bounds['degree_bound']==D+1
    assert bounds['degree_bound_power_of_two_exponent']==(D+1).bit_length()
    assert bounds['separator_degree_bound']==E
    assert bounds['ordinary_monomial_upper_bound']==str(support)
    assert bounds['ordinary_monomial_upper_bound_power_of_two_exponent']==support.bit_length()
    assert bounds['coefficient_l1_norm_log2_bound']==receipt['coefficient_l1_norm_log2_bound']
    assert bounds['coefficient_height_bound_double_power_of_two_exponent']==receipt['coefficient_height_bound_double_power_of_two_exponent']
    # Multiplication by X is an injective shift on exponent tuples. It neither
    # changes coefficients nor introduces an auxiliary rational coordinate.
    report={'status':'PASS','total_variables':13,'all_degree_cases_checked':64,
        'base_degree_bound':D,'degree_bound':D+1,
        'strict_degree_power_of_two_exponent':(D+1).bit_length(),
        'ordinary_monomial_upper_bound':str(support),
        'strict_support_power_of_two_exponent':support.bit_length(),
        'coefficient_l1_norm_log2_bound':bounds['coefficient_l1_norm_log2_bound'],
        'outer_input_factor_checked':True,'coefficient_multiset_unchanged':True,
        'base_independent_report_sha256':hashlib.sha256(inner.read_bytes()).hexdigest(),
        'definition_specification_sha256':hashlib.sha256(raw).hexdigest(),
        'family_parameter':final['family_parameter'],
        'scope':'Independent exact source dependencies, companion-column inequalities and all64 finite-algebra degree cases, followed by the exact identity F_B=X*Q_B. The support count is an upper bound. Arithmetic hypotheses and ineffective defining thresholds are not certified by this algebraic calculation.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','total_variables','degree_bound',
        'strict_degree_power_of_two_exponent','strict_support_power_of_two_exponent')},indent=2))


if __name__=='__main__':main()
