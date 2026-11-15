#!/usr/bin/env python3
"""Smaller guards when only the final quadratic root may vanish.

The v30 integral algebra and separator are unchanged. This producer changes
the scalar guard and permits a zero ordinate at the final pole only.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = HERE.parent / 'subalgebra_norms_v30'
sys.path.insert(0, str(HERE.parent / 'unit_norm_v28'))
from build_sources import make_source

NAMES = ('general25', 'explicit27', 'weak13', 'abc13')


def compile_specification(source, parent, parent_path):
    nodes = source['coefficient_dag']
    poles = [block for block in source['finite_blocks'] if block['kind'] == 'pole']
    pole_nodes = {block['generator_node'] for block in poles}
    terminal = poles[-1]['generator_node']

    @lru_cache(None)
    def factors(index):
        op, *args = nodes[index]
        if op == 'int' and abs(args[0]) == 1:
            return frozenset()
        if op == 'neg':
            return factors(args[0])
        if op == 'pow':
            return factors(args[0]) if args[1] else frozenset()
        if op == 'mul':
            return frozenset().union(*(factors(child) for child in args))
        return frozenset((index,))

    support = set()
    for guard in source['guard_numerators']:
        if guard != terminal:
            support.update(factors(guard) - pole_nodes)
    for pole in poles[:-1]:
        support.update(factors(pole['coefficient_nodes_ascending'][0]))
    support = {node for node in support if nodes[node][0] != 'int'}
    old_factors = parent['subalgebra_norm_factors']
    assert support <= {factor['node'] for factor in old_factors}
    kept = [deepcopy(factor) for factor in old_factors if factor['node'] in support]
    omitted = [deepcopy(factor) for factor in old_factors if factor['node'] not in support]
    result = deepcopy(parent)
    result['schema'] = 'terminal-quadratic-root-polynomial-specification/v40'
    result['parent_specification'] = {
        'path': str(parent_path.relative_to(ROOT)),
        'sha256': hashlib.sha256(parent_path.read_bytes()).hexdigest(),
    }
    result['terminal_root_policy'] = {
        'name': poles[-1]['name'],
        'native_generator_node': terminal,
        'suppressed_source_guard_nodes': [terminal],
        'zero_terminal_root_allowed': True,
        'preceding_radicands_required_units': True,
        'terminal_square_multiplier_independently_required_nonzero': False,
    }
    result['guard_factorizations'] = [row for row in result['guard_factorizations']
                                     if row['node'] != terminal]
    result['subalgebra_norm_factors'] = kept
    result['omitted_support_factors'] = omitted
    bounds = result['bounds']
    bounds['guard_factors'] = len(kept)
    bounds['scalar_guard_degree_bound'] = sum(f['scalar_norm_degree_bound'] for f in kept)
    bounds['scalar_guard_log2_l1_bound'] = sum(f['scalar_norm_log2_l1_bound'] for f in kept)
    rank = bounds['full_rank']
    before = rank*(bounds['scalar_guard_degree_bound']+bounds['separator_degree_bound']+1)
    degree = before+int(source['multiply_by_input'])
    log_height = rank*(bounds['scalar_guard_log2_l1_bound']+
                      bounds['separator_operator_log2_norm_bound']+1)
    variables = bounds['total_variables']
    support_bound = (math.comb(before+variables, variables)
                     -math.comb(before-rank+variables-1, variables))
    bounds.update(degree_before_input_factor=before, degree_bound=degree,
                  strict_degree_power_of_two=degree.bit_length(),
                  coefficient_log2_l1_bound=log_height,
                  coefficient_height_double_power_exponent=log_height.bit_length(),
                  monomial_upper_bound=str(support_bound),
                  support_strict_power_of_two=support_bound.bit_length())
    result['recipe']['G'] = ('Product of the listed subalgebra norms. All native guards except '
                            'the terminal pole ordinate are retained, and every preceding '
                            'quadratic radicand remains a unit. The final radicand may vanish.')
    result['recipe']['semantics'] = ('G=0 gives P=1. On G!=0 the unchanged Omega is nonzero '
                                    'and separates the geometric characters of the possibly '
                                    'nonreduced terminal quadratic extension. A rational '
                                    'eigenvalue selects a unique Galois-fixed rational character. '
                                    'This enlarges the permitted retained tuples; the integer '
                                    'input projection and sufficient fixed parameters are unchanged.')
    result['arithmetic_scope'] = ('The final pole ordinate is allowed to be zero; its elementary '
                                  'negative-odd-valuation obstruction still applies. All previous '
                                  'full-unit completeness witnesses remain allowed. The inherited '
                                  'arithmetic premises and sufficient parameter values are unchanged. '
                                  'No equality of every retained-coordinate projection is claimed.')
    return result


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    constructions = []
    for name in NAMES:
        parent_path = PARENT / 'specifications' / (name+'.json')
        parent = json.loads(parent_path.read_text())
        spec = compile_specification(make_source(name), parent, parent_path)
        (output/(name+'.json')).write_text(json.dumps(spec, indent=2)+'\n')
        constructions.append({'name': name, 'family_parameter': spec['family_parameter'],
                              'removed_factor_nodes': [f['node'] for f in spec['omitted_support_factors']],
                              **spec['bounds'], 'coefficient_scope': spec['coefficient_scope']})
    report = {'schema': 'terminal-root-degree-bounds/v40', 'constructions': constructions,
              'scope': 'Exact majorants for finite unexpanded specifications. Variable counts '
                       'are unchanged. Fixed sufficient defining parameters are inherited.'}
    (output/'bounds.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'specifications')
    args = parser.parse_args()
    for record in build(args.output)['constructions']:
        print(record['name'], record['degree_bound'],
              '< 2^'+str(record['strict_degree_power_of_two']))
