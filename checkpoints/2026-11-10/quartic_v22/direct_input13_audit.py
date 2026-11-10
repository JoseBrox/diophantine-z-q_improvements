#!/usr/bin/env python3
"""Independent exact audit of the direct-input13 fourth-/sixth-power sources.

No direct-input producer or checker is imported. The audit imports only the
existing independent source-conversion and active-algebra checkers. It checks
the complete source against its audited predecessor by literal expression
identities under two specified substitutions, and checks the new substitutions
as polynomial identities with B treated as an indeterminate.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
from math import comb, prod
from pathlib import Path
import sys

sys.dont_write_bytecode = True
DEFAULT_REPO = Path('/workspace/scratch/191d4e871efa/repo')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_module(path, name):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class CanonicalExpressions:
    """Exact expression interning, using only commutativity of + and *."""
    def __init__(self):
        self.table = {}

    def intern(self, key):
        if key not in self.table:
            self.table[key] = len(self.table)
        return self.table[key]

    def read(self, nodes, replacements=None):
        replacements = replacements or {}
        ids = []
        for index, (operation, *args) in enumerate(nodes):
            if index in replacements:
                ids.append(replacements[index])
                continue
            if operation in ('int', 'variable', 'parameter'):
                key = (operation, *args)
            elif operation == 'pow':
                assert 0 <= args[0] < index
                key = (operation, ids[args[0]], args[1])
            elif operation == 'neg':
                assert 0 <= args[0] < index
                key = (operation, ids[args[0]])
            elif operation in ('add', 'mul'):
                assert all(0 <= a < index for a in args)
                key = (operation, *sorted(ids[a] for a in args))
            else:
                raise AssertionError(operation)
            ids.append(self.intern(key))
        return ids


def transform_rationals(value, ids):
    if isinstance(value, dict):
        if set(value) == {'numerator', 'denominator'}:
            return ('rational', ids[value['numerator']], ids[value['denominator']])
        return {k: transform_rationals(v, ids) for k, v in value.items()}
    if isinstance(value, list):
        return [transform_rationals(v, ids) for v in value]
    return value


def transform_relation(row, ids):
    out = transform_rationals(row, ids)
    for key in ('generator_node', 'derivative_guard'):
        if key in out:
            out[key] = ids[row[key]]
    for key in ('coefficient_nodes_ascending', 'automatic_nonzero_nodes'):
        if key in out:
            out[key] = [ids[v] for v in row[key]]
    return out


def exact_source_difference(previous, current):
    """Compare every source equation, guard and event, after two replacements."""
    assert previous['variables'] == current['variables']
    assert previous['finite_parameters'] == current['finite_parameters']
    assert previous['comparison_orders'] == current['comparison_orders'] == [1]*6
    assert previous['formal_precision'] == current['formal_precision'] == 4
    assert previous['closed_equations'] == current['closed_equations'] == []
    assert previous['indexed_guard_polynomials'] == current['indexed_guard_polynomials'] == []
    old_height = next(e for e in previous['events'] if e['operation'] == 'conditional_weak_abc_height_scales')
    new_height = next(e for e in current['events'] if e['operation'] == 'conditional_weak_abc_height_scales')
    old_target = previous['comparison_tests'][5][0]['numerator']
    new_target = current['comparison_tests'][5][0]['numerator']
    old_scale = old_height['sum_eighth_powers']['numerator']
    new_scale = new_height['sum_even_powers']['numerator']
    expressions = CanonicalExpressions()
    new_ids = expressions.read(current['coefficient_dag'])
    old_ids = expressions.read(previous['coefficient_dag'], {
        old_target: new_ids[new_target], old_scale: new_ids[new_scale]})
    assert transform_rationals(previous['comparison_tests'], old_ids) == transform_rationals(current['comparison_tests'], new_ids)
    assert [transform_relation(r, old_ids) for r in previous['finite_monic_relations']] == [transform_relation(r, new_ids) for r in current['finite_monic_relations']]
    assert set(old_ids[k] for k in previous['guard_numerators']) == set(new_ids[k] for k in current['guard_numerators'])
    assert [(old_ids[k], why) for k, why in previous['guard_descriptions']] == [(new_ids[k], why) for k, why in current['guard_descriptions']]
    assert len(previous['events']) == len(current['events']) == 11
    for old_event, new_event in zip(previous['events'], current['events']):
        assert old_event['operation'] == new_event['operation']
        if old_event['operation'] == 'conditional_weak_abc_height_scales':
            for key in ('beta', 'trace', 'scales'):
                assert transform_rationals(old_event[key], old_ids) == transform_rationals(new_event[key], new_ids)
        else:
            assert transform_rationals(old_event, old_ids) == transform_rationals(new_event, new_ids), old_event['operation']
    return {'exact_source_substitutions': ['real numerator of L−beta becomes real numerator of L−X',
                                           'beta^8+T^8 becomes beta^d+T^d'],
            'checked_relations': 5, 'checked_events': 11,
            'checked_guard_descriptions': len(current['guard_descriptions']),
            'all_other_point_test_pole_and_guard_expressions_identical': True}


def check_changed_formulas(source, algebra):
    """Exact sparse identities; no direct-input builder/checker is used."""
    nodes = source['coefficient_dag']
    names = {v['name']: v['index'] for v in source['variables']}
    event = next(e for e in source['events'] if e['operation'] == 'conditional_weak_abc_height_scales')
    expand = algebra.expander(nodes, variables={names['input.X']: 0, names['A.a0']: 1, names['A.a1']: 2}, parameters={'fixed_input_shift': 3})
    x, a, b, B = [{(i,): 1} for i in range(4)]
    beta = algebra.plus(algebra.times({(): 2}, algebra.power(x, 2)), B)
    trace = algebra.plus(algebra.times({(): 2}, algebra.power(a, 2)), algebra.times({(): 4}, algebra.power(b, 2)))
    d = source['scale_power']
    for key, expected in [('target', x), ('beta', beta), ('trace', trace),
                          ('sum_even_powers', algebra.plus(algebra.power(beta, d), algebra.power(trace, d)))]:
        assert expand(event[key]['numerator']) == expected
        assert expand(event[key]['denominator']) == {(): 1}
    test_event = next(e for e in source['events'] if e['operation'] == 'conditional_direct_target_tests')
    L = test_event['L']
    target = source['comparison_tests'][5]
    assert target[1] == L[1]
    assert target[0]['denominator'] == L[0]['denominator']
    target_expand = algebra.expander(nodes, atoms={L[0]['numerator']: 0, L[0]['denominator']: 1}, variables={names['input.X']: 2})
    assert target_expand(target[0]['numerator']) == {(0,): 1, (1,2): -1}
    assert event['scales'][1] == event['sum_even_powers']
    assert source['comparison_target'] == source['final_polynomial_multiplier'] == 'input.X'
    assert [e['name'] for e in source['events'] if e['operation'] == 'point'] == ['A', 'H', 'UA']
    assert [r['degree'] for r in source['finite_monic_relations']] == [4,4,4,2,2]
    assert [r['kind'] for r in source['finite_monic_relations']] == ['point']*3+['pole']*2
    assert source['retained_base_count'] == 12
    assert prod(r['degree'] for r in source['finite_monic_relations']) == 256
    # This is metadata/consistency, not a proof of abc or the global theorem.
    kappa = Fraction(16,15) if d == 4 else Fraction(121,100)
    assert source['weak_abc_exponent'] == {'numerator': kappa.numerator, 'denominator': kappa.denominator}
    absorption = 1/((8/kappa-6)*(d/kappa-3))
    assert 0 < absorption < 1
    assert absorption == (Fraction(8,9) if d == 4 else Fraction(14641,17538))
    return {'scale_power': d, 'changed_target_exactly_L_minus_X': True,
            'formal_B_checked': True, 'retained_n_point_role': 'A',
            'comparison_absorption_coefficient': str(absorption)}


def audit_variant(repo, variant_name, previous, conversion, algebra, active):
    directory = repo/'computation/few_variables/direct_input13_v22'/variant_name
    raw = gzip.decompress((directory/'certificate/source.json.gz').read_bytes())
    source = json.loads(raw)
    encoded = (directory/'certificate/source-polynomial-specification.json').read_bytes()
    spec = json.loads(encoded)
    receipt = json.loads((directory/'certificate/source-construction-certificate.json').read_text())
    assert receipt['source_sha256'] == sha(raw)
    assert receipt['integer_specification_sha256'] == sha(encoded)
    source_receipt = conversion.audit(source, spec)
    difference = exact_source_difference(previous, source)
    changed = check_changed_formulas(source, algebra)
    active.SOURCES[13] = directory/'certificate/source-polynomial-specification.json'
    active_receipt = active.check_directory(directory/'active13')
    final_raw = (directory/'definition-polynomial-specification.json').read_bytes()
    final = json.loads(final_raw)
    final_certificate = json.loads((directory/'definition-construction-certificate.json').read_text())
    base_raw = (directory/'active13/polynomial-specification.json').read_bytes()
    base = json.loads(base_raw)
    c = json.loads((directory/'active13/construction-certificate.json').read_text())
    assert final['format'] == 'integer-polynomial-times-input/v1'
    assert final['polynomial_recipe'] == {'base_name': 'Q_B', 'final_name': 'F_B', 'expression': 'input.X * Q_B', 'multiplier_variable_index': 0}
    assert final['base_specification'] == 'active13/polynomial-specification.json'
    assert final['base_specification_sha256'] == sha(base_raw)
    assert final_certificate['definition_specification_sha256'] == sha(final_raw)
    assert final['external_variables'] == base['external_variables']
    assert len(final['external_variables']) == final['total_variables'] == 13
    assert final['external_variables'][0] == {'index': 0, 'name': 'input.X', 'category': 'retained.input'}
    assert final['family_parameter'] == base['family_parameter'] == source['family_parameter']
    assert final['arithmetic_status'] == base['arithmetic_status']
    assert final['family_parameter']['value'] == 3
    assert not final['family_parameter']['selected_member_certified_to_define_Z']
    D = active_receipt['degree_bound']
    assert c['point_algebra_rank'] == 64 and c['rank'] == 256
    # Directly sum the separator-degree contributions from all factors.
    E = sum(2*256 if r < 64 else 256 for r in range(1,65))
    assert E == 32512
    # Count by each separator exponent; independent of the producer's
    # difference-of-binomial formula, including both endpoints.
    support = sum(comb(D-j+12,12) for j in range(E+1))
    assert support == comb(D+13,13)-comb(D-E+12,13)
    bounds = final['bounds']
    assert bounds['base_degree_bound'] == D
    assert bounds['degree_bound'] == D+1
    assert bounds['degree_bound_power_of_two_exponent'] == (D+1).bit_length() == 44
    assert bounds['separator_degree_bound'] == E
    assert int(bounds['ordinary_monomial_upper_bound']) == support
    assert bounds['ordinary_monomial_upper_bound_power_of_two_exponent'] == support.bit_length()
    assert bounds['coefficient_l1_norm_log2_bound'] == active_receipt['coefficient_l1_norm_log2_bound']
    assert bounds['coefficient_height_bound_double_power_of_two_exponent'] == c['coefficient_height_bound_double_power_of_two_exponent'] == 45
    for name, digest in source['source_helpers'].items():
        assert digest == sha((repo/'computation/few_variables/trace27_nontorsion'/name).read_bytes())
    assert source['source_builder_sha256'] == sha((directory.parent/'build_direct_input_source.py').read_bytes())
    return {'variant': variant_name, 'status': 'PASS',
            'source_sha256': sha(raw), 'integer_specification_sha256': sha(encoded),
            'active_specification_sha256': sha(base_raw), 'final_specification_sha256': sha(final_raw),
            'source_graph_audit': difference, 'changed_formula_audit': changed,
            'source_conversion': {k:v for k,v in source_receipt.items() if k.startswith('source_')},
            'active_bound_audit': active_receipt,
            'final_polynomial_is_exactly_X_times_Q': True,
            'input_zero_branch': 'For X=0 every auxiliary assignment is a zero; for X!=0 the old guarded-source projection is preserved exactly.',
            'degree_bound': D+1, 'strict_degree_power_exponent': 44,
            'separator_degree_bound': E, 'support_upper_bound': str(support),
            'strict_support_power_exponent': support.bit_length(),
            'coefficient_log2_l1_bound': bounds['coefficient_l1_norm_log2_bound'],
            'coefficient_height_double_power_exponent': 45,
            'coefficient_multiset_unchanged_by_final_factor': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=DEFAULT_REPO)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    pinned = args.repo/'computation/few_variables/trace27_nontorsion'
    sys.path.insert(0, str(pinned))
    conversion = load_module(pinned/'verify_specification.py', 'direct13_existing_conversion_checker')
    algebra = load_module(pinned/'finite_algebra_check_core.py', 'direct13_existing_sparse_algebra')
    active = load_module(args.repo/'computation/few_variables/active_elimination/check_active_specification.py', 'direct13_existing_active_checker')
    old_path = args.repo/'computation/few_variables/weak_abc13/certificate/source.json.gz'
    old_raw = gzip.decompress(old_path.read_bytes())
    previous = json.loads(old_raw)
    records = [audit_variant(args.repo, name, previous, conversion, algebra, active) for name in ('abc','weak')]
    report = {'status': 'PASS', 'predecessor_source_sha256': sha(old_raw), 'variants': records,
              'checker_sha256': sha(Path(__file__).read_bytes()),
              'existing_checker_hashes': {str(path.relative_to(args.repo)): sha(path.read_bytes()) for path in [pinned/'verify_specification.py', pinned/'finite_algebra_check_core.py', args.repo/'computation/few_variables/active_elimination/check_active_specification.py']},
              'scope': 'Exact source-expression equivalence under the two stated substitutions; exact new polynomial identities; complete affine finite-algebra conversion; independent operator inequalities and all 64 degree cases; exact final X-factor recipe and direct capped-separator support count. No numerical samples are used. The global arithmetic theorem, abc premises and ineffective sufficiency threshold are separate.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'variants': [{k:r[k] for k in ('variant','degree_bound','strict_degree_power_exponent','strict_support_power_exponent','coefficient_log2_l1_bound')} for r in records]}, indent=2))


if __name__ == '__main__':
    main()
