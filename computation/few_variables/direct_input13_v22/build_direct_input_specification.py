#!/usr/bin/env python3
"""Construct the exact final polynomial X times the guarded determinant."""
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
import build_active_specification as active


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('variant',type=Path)
    args=ap.parse_args()
    variant=args.variant
    source=variant/'certificate/source-polynomial-specification.json'
    sys.argv=[active.__file__,str(source),str(variant/'active13')]
    active.main()
    raw=(variant/'active13/polynomial-specification.json').read_bytes()
    base=json.loads(raw)
    receipt=json.loads((variant/'active13/construction-certificate.json').read_text())
    D=receipt['degree_bound'];E=(2*receipt['point_algebra_rank']-1)*receipt['rank']
    support=comb(D+13,13)-comb(D-E+12,13)
    output={
        'format':'integer-polynomial-times-input/v1',
        'base_specification':'active13/polynomial-specification.json',
        'base_specification_sha256':hashlib.sha256(raw).hexdigest(),
        'polynomial_recipe':{'base_name':'Q_B','final_name':'F_B',
            'expression':'input.X * Q_B','multiplier_variable_index':0},
        'external_variables':base['external_variables'],
        'total_variables':13,
        'family_parameter':base['family_parameter'],
        'arithmetic_status':base['arithmetic_status'],
        'projection':'The rational input projection is {0} union the guarded-source input projection.',
        'bounds':{'base_degree_bound':D,'degree_bound':D+1,
            'degree_bound_power_of_two_exponent':(D+1).bit_length(),
            'separator_degree_bound':E,
            'ordinary_monomial_upper_bound':str(support),
            'ordinary_monomial_upper_bound_power_of_two_exponent':support.bit_length(),
            'support_reason':'Multiplication by input.X shifts all monomials injectively; apply the capped-separator monomial count to Q_B.',
            'coefficient_l1_norm_log2_bound':receipt['coefficient_l1_norm_log2_bound'],
            'coefficient_height_bound_double_power_of_two_exponent':receipt['coefficient_height_bound_double_power_of_two_exponent'],
            'coefficient_reason':'Multiplication by a coordinate preserves the complete coefficient multiset.'},
        'expansion_status':'The determinant polynomial is specified by exact finite integer operations; no monomial expansion is materialized.'}
    target=variant/'definition-polynomial-specification.json'
    target.write_text(json.dumps(output,indent=2)+'\n')
    certificate={
        'status':'Exact finite polynomial specification',
        'definition_specification_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'base_specification_sha256':output['base_specification_sha256'],
        'total_variables':13,'outer_input_factor':True,
        **output['bounds'],
        'family_parameter':base['family_parameter']}
    (variant/'definition-construction-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({k:certificate[k] for k in ('total_variables','degree_bound',
          'degree_bound_power_of_two_exponent','ordinary_monomial_upper_bound_power_of_two_exponent',
          'coefficient_l1_norm_log2_bound')},indent=2))


if __name__=='__main__':main()
