#!/usr/bin/env python3
"""Check the bounded-variable undecidability ledger and its exact certificates.

The infinite equivalences are proved in the accompanying TeX. This program
does not independently establish the imported arithmetic or universality
theorems, and its receipt states that limitation.
"""
from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    folder = ROOT / 'undecidability'
    result = subprocess.run(
        [sys.executable, '-B', str(folder/'verify_transfer_general_degree.py')],
        cwd=ROOT, capture_output=True, text=True, check=True)
    actual = json.loads(result.stdout)
    expected = json.loads((folder/'certificates/transfer_general_degree.json').read_text())
    assert actual == expected, 'General transfer certificate is stale'
    # Independently factor the published degree expression.
    nu, delta = 58, 4
    eta = 15616 + delta * (233856 + (233952+467712*delta)*(2*delta+1)**(nu+1))
    assert str(eta) == actual['eta_58_4']
    ledger = json.loads((folder/'results.json').read_text())
    old = json.loads((ROOT/'data/results_20261123_v88.json').read_text())
    routes = old['route_bounds']
    proved = [r for r in ledger['records'] if r['id'].startswith('mixed-nine-')]
    assert len(proved) == 3
    for record in proved:
        source = routes[record['integer_predicate_route']]
        m = source['variables']
        assert record['integer_predicate_total_variables'] == m
        assert record['integer_predicate_degree_upper_bound'] == source['degree_upper_bound']
        # Eight retained inputs, nine separate witness blocks, three wrapper coordinates.
        assert record['variables'] == 8 + 9*(m-1) + 3
        assert int(record['degree_upper_bound']) == max(2*eta, 4*source['degree_upper_bound'])
        assert record['defining_parameter_effective'] == source['sufficient_parameter_effective']
        assert record['retains_project_arithmetic_premises'] is True
        assert (folder/record['proof']).is_file()
        assert (ROOT/record['integer_predicate_path']).is_file()
    assert ledger['global_minimum_claimed'] is False
    assert ledger['inherited_arithmetic_premises_independently_proved'] is False
    for record in ledger['records']:
        if record['id'].startswith('quartic-transfer-'):
            assert record['status'] == 'historical_checkpoint_source_equivalence_unresolved'
            assert record['variables'] == 15*record['integer_predicate_total_variables']+94
            assert record['quadratic_rows'] == 61+15*record['integer_predicate_quadratic_rows']
    quartic_run = subprocess.run(
        [sys.executable, '-B', str(folder/'verify_jones1980.py')],
        cwd=ROOT, capture_output=True, text=True, check=True)
    quartic = json.loads(quartic_run.stdout)
    assert quartic['status'] == 'PASS'
    current_quartics = [r for r in ledger['records'] if r['id'].startswith('jones1980-quartic-')]
    assert len(current_quartics) == 3
    for record in current_quartics:
        m = record['integer_predicate_total_variables']
        checked = quartic['routes'][str(m)]
        assert record['variables'] == checked['variables'] == 12*m+239
        assert record['quadratic_rows'] == checked['quadratic_residuals']
        assert record['degree'] == 4 and record['integer_certificates'] == 12
        assert record['retains_project_arithmetic_premises'] is True
        assert record['status']=='exact_algebraic_checkpoint_undecidability_conditional_on_U_em'
        assert record['source_universality_hypothesis']=='U_em'
        assert record['source_universality_independently_verified'] is False
        assert record['instance_tail'] == 'x > 2*z for fixed positive integer z'
        assert (folder/record['proof']).is_file() and (folder/record['table']).is_file()
    joint_run = subprocess.run(
        [sys.executable, '-B', str(folder/'verify_joint_sources.py')],
        cwd=ROOT, capture_output=True, text=True, check=True)
    joint=json.loads(joint_run.stdout)
    assert joint==json.loads((folder/'certificates/shared_integer_transfers.json').read_text())
    joint_records=[r for r in ledger['records'] if r['id'].startswith('shared-integer-')]
    assert len(joint_records)==3
    for record in joint_records:
        route=record['integer_predicate_route'];checked=joint['routes'][route]
        assert record['variables']==checked['variables']
        assert record['tuple_coordinates']+2==record['variables']
        assert record['degree_upper_bound']==checked['mixed_transfer_degree_upper_bound']
        assert record['degree_strictly_less_than_power2']==checked['mixed_transfer_degree_strictly_less_than_power2']
        assert int(record['degree_upper_bound'])<2**record['degree_strictly_less_than_power2']
        assert record['separating_gamma_count']==checked['gamma_count']
        assert record['source_sha256']==checked['joint_source_sha256']
        assert record['retains_project_arithmetic_premises'] is True
        assert record['native_pole_converse_premise_required'] is False
        assert record['defining_parameter_effective']==(route=='explicit27')
        assert record['stored_source_is_certified_defining_member']==(route=='explicit27')
        assert (folder/record['proof']).is_file() and (folder/record['source_specification']).is_file()
    encoder_only=[r for r in ledger['records'] if r['id'].startswith('joint-encoder-only-')]
    assert len(encoder_only)==3
    for record in encoder_only:
        assert record['variables']==9*record['integer_predicate_total_variables']-6
        assert (folder/record['proof']).is_file()
    shared_run = subprocess.run(
        [sys.executable, '-B', str(folder/'verify_shared_reference.py')],
        cwd=ROOT, capture_output=True, text=True, check=True)
    shared=json.loads(shared_run.stdout)
    assert shared['status']=='PASS' and shared['unconditional_undecidability_claim'] is False
    shared_records=[r for r in ledger['records'] if r['id'].startswith('shared-quartic-')]
    assert len(shared_records)==3
    for record in shared_records:
        m=record['integer_predicate_total_variables'];checked=shared['routes'][str(m)]
        assert record['variables']==checked['variables']
        assert record['variables']==252+12*(m-1)-11*record['shared_reference_coordinates']
        assert record['quadratic_rows']==checked['quadratic_residuals']
        assert record['quadratic_rows']==220+12*record['integer_predicate_quadratic_rows']-11*record['shared_reference_rows']
        assert record['degree']==4 and record['retains_project_arithmetic_premises'] is True
        assert record['status']=='exact_algebraic_checkpoint_undecidability_conditional_on_U_em'
        assert record['source_universality_hypothesis']=='U_em'
        assert record['source_universality_independently_verified'] is False
        assert (folder/record['proof']).is_file() and (folder/record['table']).is_file()
    mt_run = subprocess.run(
        [sys.executable, '-B', str(folder/'code/mt_quadratic_system.py')],
        cwd=ROOT, capture_output=True, text=True, check=True)
    mt = json.loads(mt_run.stdout)
    assert mt == json.loads((folder/'certificates/mt_source_audit.json').read_text())
    assert (mt['reduced_variables'], mt['reduced_rows']) == (57,45)
    receipt = {
        'schema': 'zq-undecidability-verification/v89',
        'status': 'PASS',
        'proved_transfer_counts': {r['integer_predicate_route']:r['variables'] for r in proved},
        'source_ledger_consistent': True,
        'proved_joint_counts': {r['integer_predicate_route']:r['variables'] for r in joint_records},
        'joint_degree_strict_power2_bounds': {r['integer_predicate_route']:r['degree_strictly_less_than_power2'] for r in joint_records},
        'joint_source_reproduction':joint['status'],
        'independent_quartic_checkpoints': quartic['routes'],
        'shared_quartic_checkpoints':shared['routes'],
        'emended_source_universality':'U_em remains unverified',
        'printed_system_affine_checkpoint': {'variables':57,'quadratic_rows':45,'universality':'unresolved'},
        'degree_arithmetic_independently_factored': True,
        'historical_quartic_source_equivalence': 'unresolved',
        'scope': 'Exact ledger and certificate checks; infinite transfer proved in TeX; external arithmetic premises are not proved by computation; U_em remains unverified and quartic bounds are source-conditional checkpoints.'
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
