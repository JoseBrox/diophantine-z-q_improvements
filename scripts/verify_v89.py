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
    receipt = {
        'schema': 'zq-undecidability-verification/v89',
        'status': 'PASS',
        'proved_transfer_counts': {r['integer_predicate_route']:r['variables'] for r in proved},
        'source_ledger_consistent': True,
        'degree_arithmetic_independently_factored': True,
        'historical_quartic_source_equivalence': 'unresolved',
        'scope': 'Exact ledger and certificate checks; infinite transfer proved in TeX; external arithmetic premises and classical universality not reproved by this program.'
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
