#!/usr/bin/env python3
"""Replay common-numerator, finite-wrapper and combined-quadratic reductions.

This gate certifies finite identities and bookkeeping. Infinite arithmetic
premises and the explicitly unresolved U_em source are not proved by it.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'undecidability'


def run(name, parse_json=True):
    result=subprocess.run([sys.executable,'-B',str(F/name)],cwd=ROOT,
                          text=True,capture_output=True,check=True)
    return json.loads(result.stdout) if parse_json else result.stdout


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    common=run('verify_common_numerator.py')
    wrapper=run('verify_finite_wrapper.py')
    compiler=run('verify_finite_wrapper_compiler.py')
    assert common==json.loads((F/'certificates/common_numerator_transfers.json').read_text())
    assert wrapper==json.loads((F/'certificates/finite_wrapper_transfer.json').read_text())
    assert compiler==json.loads((F/'certificates/finite_wrapper_compiler.json').read_text())
    assert common['status']==wrapper['status']==compiler['status']=='PASS'
    reciprocal_output=run('verify_reciprocal_reference.py',False)
    points_output=run('verify_common_points.py',False)
    assert reciprocal_output.count('PASS')==points_output.count('PASS')==2

    ledger=json.loads((F/'results.json').read_text())
    assert ledger['global_minimum_claimed'] is False
    assert ledger['inherited_arithmetic_premises_independently_proved'] is False
    records={r['id']:r for r in ledger['records']}
    assert len(records)==len(ledger['records'])
    for route,old_count,new_count,tuple_count in [
        ('general25',83,82,81),('explicit27',101,100,99),('abc11',53,52,51)]:
        c=common['routes'][route]
        w=wrapper['routes'][route]
        r=records['common-numerator-'+route]
        t=records['finite-wrapper-'+route]
        assert r['variables']==c['variables']==old_count
        assert r['tuple_coordinates']==c['tuple_coordinates']==tuple_count
        assert r['variables']==r['tuple_coordinates']+2
        assert t['variables']==w['rational_variables']==new_count==old_count-1
        assert t['ordinary_coordinates_before_final_encoder']+1==new_count
        assert t['integer_inputs_retained']==w['integer_predicates_retained']==9
        assert t['additional_finite_algebra_rank']==16
        assert t['wrapper_separating_generators']==['xi']
        assert t['source_equation_absorbed'] is True
        assert t['positivity_coordinates_remaining']==2
        compiled=compiler['routes'][route]
        assert compiled['rational_unknowns']==new_count
        assert compiled['integer_predicates_retained']==9
        assert compiled['input_polynomial_claimed_universal'] is False
        assert compiled['exact_homogenization_nodes_replayed']==c['coefficient_nodes']
        assert compiled['exact_tower_dependency_checks']['all_coefficients_depend_only_on_preceding_stages'] is True
        assert t['source_sha256']==r['source_sha256']==c['joint_source_sha256']==w['source_common_numerator_sha256']
        assert t['finite_algebra_rank_exponent_base2']==r['finite_algebra_rank_exponent_base2']+4
        assert t['separating_gamma_count']==r['separating_gamma_count']+1
        for record,degree,ceiling in [
            (r,c['mixed_transfer_degree_upper_bound'],c['mixed_transfer_degree_strictly_less_than_power2']),
            (t,w['final_polynomial_degree_upper_bound'],w['final_degree_strictly_less_than_power2'])]:
            assert record['degree_restriction']=='unrestricted'
            assert record['degree_upper_bound']==degree
            assert record['degree_strictly_less_than_power2']==ceiling
            assert int(degree)<2**ceiling
            assert record['retains_project_arithmetic_premises'] is True
            assert record['native_pole_converse_premise_required'] is False
            assert record['defining_parameter_effective']==(route=='explicit27')
            assert record['stored_source_is_certified_defining_member']==(route=='explicit27')
            assert record['additional_height_hypothesis']==('ordinary_rational_abc' if route=='abc11' else None)
            assert (F/record['proof']).is_file()
            assert (F/record['proof']).with_suffix('.pdf').is_file()
            assert (F/record['source_specification']).is_file()

    quartics={}
    for m in [163,179]:
        for prefix in ['reciprocal-quartic-','common-point-quartic-']:
            r=records[prefix+str(m)]
            c=json.loads((F/r['certificate']).read_text())
            table_path=F/r['table'];table=json.loads(table_path.read_text())
            assert r['variables']==c['variables']==table['variables']
            assert r['quadratic_rows']==c['quadratic_residuals']==len(table['residuals'])
            assert r['table_sha256']==c['table_sha256']==hashlib.sha256(table_path.read_bytes()).hexdigest()
            assert r['degree']==4==c['sum_of_squares_degree']
            assert r['source_universality_hypothesis']=='U_em'
            assert r['source_universality_independently_verified'] is False
            assert r['status']=='exact_algebraic_checkpoint_undecidability_conditional_on_U_em'
            assert r['retains_project_arithmetic_premises'] is True
            assert c['unconditional_undecidability_claim'] is False
            assert r['additional_height_hypothesis'] is None
            assert (F/r['proof']).is_file()
            assert (F/r['proof']).with_suffix('.pdf').is_file()
            if prefix=='common-point-quartic-':
                s={163:54,179:50}[m];q={163:24,179:20}[m]
                assert r['common_physical_coordinates']==c['common_point_shared_coordinates']==s
                assert r['variables']==251+12*(m-1)-11*s
                assert r['quadratic_rows']==219+12*{163:137,179:151}[m]-11*q
                assert r['common_input_numerator'] is True
            else:
                assert r['variables']==251+12*(m-1)-110
            quartics[r['id']]={'variables':r['variables'],'quadratic_rows':r['quadratic_rows'],'source_universality':'U_em remains unverified'}

    receipt={
        'schema':'zq-undecidability-verification/v90',
        'status':'PASS',
        'common_numerator_counts':{r:common['routes'][r]['variables'] for r in common['routes']},
        'finite_wrapper_counts':{r:wrapper['routes'][r]['rational_variables'] for r in wrapper['routes']},
        'common_numerator_degree_strict_power2':{r:common['routes'][r]['mixed_transfer_degree_strictly_less_than_power2'] for r in common['routes']},
        'finite_wrapper_degree_strict_power2':{r:wrapper['routes'][r]['final_degree_strictly_less_than_power2'] for r in wrapper['routes']},
        'all_nine_integer_certificates_retained':True,
        'finite_wrapper_coefficient_compiler':'PASS; exact DAG replay, explicitly nonuniversal fixtures, supplementary modular diagnostics',
        'quartic_checkpoints':quartics,
        'no_global_minimum_claimed':True,
        'scope':'Exact source circuits, identities, tables, hashes, counts and degree bounds; infinite equivalences are proved in the manuscripts under retained arithmetic premises. U_em is unresolved.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
