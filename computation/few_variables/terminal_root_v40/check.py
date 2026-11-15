#!/usr/bin/env python3
"""Independent checks of terminal-root guards, bounds and nonreduced examples.

The new producer is not imported. The unchanged v30 specification is checked
by its separate checker; the permitted deletions and new bounds are rebuilt
here from the native circuit and a different iterative factor traversal.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = HERE.parent/'subalgebra_norms_v30'
sys.path.insert(0, str(HERE.parent/'unit_norm_v28'))
from build_sources import make_source
module_spec = importlib.util.spec_from_file_location('terminal_parent_independent_checker', PARENT/'check.py')
parent_checker = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(parent_checker)
NAMES = ('general25', 'explicit27', 'weak13', 'abc13')


def require(value, message):
    if not value:
        raise AssertionError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def verify_spec(source, parent, spec, parent_path):
    require(spec['schema']=='terminal-quadratic-root-polynomial-specification/v40', 'Schema')
    require(spec['parent_specification']=={'path': str(parent_path.relative_to(ROOT)),
                                          'sha256': digest(parent_path.read_bytes())}, 'Parent pin')
    changed = {'schema', 'parent_specification', 'terminal_root_policy', 'guard_factorizations',
               'subalgebra_norm_factors', 'omitted_support_factors', 'bounds', 'recipe', 'arithmetic_scope'}
    for key in set(parent)-changed:
        require(spec[key]==parent[key], 'Unchanged source field: '+key)
    nodes = source['coefficient_dag']
    poles = [block for block in source['finite_blocks'] if block['kind']=='pole']
    pole_nodes = {block['generator_node'] for block in poles}
    terminal = poles[-1]['generator_node']
    policy = {'name': poles[-1]['name'], 'native_generator_node': terminal,
              'suppressed_source_guard_nodes': [terminal], 'zero_terminal_root_allowed': True,
              'preceding_radicands_required_units': True,
              'terminal_square_multiplier_independently_required_nonzero': False}
    require(spec['terminal_root_policy']==policy, 'Exactly one final root relaxed')
    require(terminal in source['guard_numerators'], 'Terminal guard exists')
    # Iterative factor sets, independent of the producer's recursive traversal.
    factors = []
    for index, (op, *args) in enumerate(nodes):
        if op=='int' and abs(args[0])==1:
            value = set()
        elif op=='neg':
            value = factors[args[0]].copy()
        elif op=='pow':
            value = factors[args[0]].copy() if args[1] else set()
        elif op=='mul':
            value = set()
            for child in args:
                value.update(factors[child])
        else:
            value = {index}
        factors.append(value)
    support = set()
    native_guards = set(source['guard_numerators'])-{terminal}
    for guard in native_guards:
        support.update(factors[guard]-pole_nodes)
    for block in poles[:-1]:
        support.update(factors[block['coefficient_nodes_ascending'][0]])
    support = {node for node in support if nodes[node][0]!='int'}
    require(spec['guard_factorizations']==[row for row in parent['guard_factorizations']
                                          if row['node'] in native_guards], 'Every remaining guard')
    keep = [row for row in parent['subalgebra_norm_factors'] if row['node'] in support]
    omit = [row for row in parent['subalgebra_norm_factors'] if row['node'] not in support]
    require(spec['subalgebra_norm_factors']==keep, 'Exact reduced support')
    require(spec['omitted_support_factors']==omit, 'Exact deletion receipt')
    require({row['node'] for row in keep}==support, 'Complete support coverage')
    # Check every source rational denominator, including the final pole's.
    denominators = 0
    def visit(value):
        nonlocal denominators
        if isinstance(value, dict):
            if {'numerator', 'denominator'} <= value.keys():
                denominators += 1
                require(all(nodes[node][0]=='int' or node in support
                            for node in factors[value['denominator']]), 'A denominator was dropped')
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(source['events'])
    visit(source['finite_blocks'])
    expected = deepcopy(parent['bounds'])
    g = sum(row['scalar_norm_degree_bound'] for row in keep)
    h = sum(row['scalar_norm_log2_l1_bound'] for row in keep)
    n = expected['full_rank']
    before = n*(g+expected['separator_degree_bound']+1)
    degree = before+int(source['multiply_by_input'])
    coefficient = n*(h+expected['separator_operator_log2_norm_bound']+1)
    count = expected['total_variables']
    monomials = math.comb(before+count, count)-math.comb(before-n+count-1, count)
    expected.update(guard_factors=len(keep), scalar_guard_degree_bound=g,
                    scalar_guard_log2_l1_bound=h, degree_before_input_factor=before,
                    degree_bound=degree, strict_degree_power_of_two=degree.bit_length(),
                    coefficient_log2_l1_bound=coefficient,
                    coefficient_height_double_power_exponent=coefficient.bit_length(),
                    monomial_upper_bound=str(monomials), support_strict_power_of_two=monomials.bit_length())
    require(spec['bounds']==expected, 'Independent complete bound dictionary')
    require(degree<parent['bounds']['degree_bound'], 'Strict degree improvement')
    for key in set(parent['recipe'])-{'G', 'semantics'}:
        require(spec['recipe'][key]==parent['recipe'][key], 'Unchanged determinant recipe')
    return {'name': source['name'], 'source_sha256': digest(canonical(source)),
            'source_denominators_checked': denominators,
            'omitted_nodes': [row['node'] for row in omit],
            'degree_bound': degree, 'coefficient_log2_l1_bound': coefficient,
            'specification_sha256': digest(canonical(spec))}


def square_roots_rational(value):
    value = Fraction(value)
    if value < 0:
        return []
    a, b = math.isqrt(value.numerator), math.isqrt(value.denominator)
    if a*a != value.numerator or b*b != value.denominator:
        return []
    root = sp.Rational(a, b)
    return [root] if not root else [root, -root]


def algebra_examples():
    Y = sp.Symbol('Y')
    cases = [(1, 0, 0), (1, 1, 1), (1, -1, 1), (1, 2, 1),
             (2, 0, 0), (2, 1, 1), (-1, 0, 0),
             (sp.Rational(1, 10000), 1, 0)]
    results = []
    for d, c0, c1 in cases:
        d, c0, c1 = map(sp.Rational, (d, c0, c1))
        Mt = sp.Matrix([[0,d,0,0], [1,0,0,0], [0,0,0,d], [0,0,1,0]])
        Mq = sp.Matrix([[0,0,c0,c1*d], [0,0,c1,c0], [1,0,0,0], [0,1,0,0]])
        require(Mt*Mt==d*sp.eye(4), 'First quadratic relation')
        require(Mq*Mq==c0*sp.eye(4)+c1*Mt, 'Last quadratic relation')
        require(Mt*Mq==Mq*Mt, 'Commutative finite algebra')
        # M1=M2=10 bounds every generator in all selected cases.
        Momega = 8000*Mt+20*d*Mq
        poly = sp.Poly((sp.eye(4)-Y*Momega).det(), Y)
        actual = poly.ground_roots()
        expected = set()
        zero_terminal_characters = 0
        for t in square_roots_rational(d):
            for q in square_roots_rational(c0+c1*t):
                omega = 8000*t+20*d*q
                require(omega != 0, 'Nonzero separator at every rational character')
                expected.add(1/omega)
                zero_terminal_characters += int(q==0)
        require(set(actual)==expected, 'Rational roots exactly recover rational characters')
        if zero_terminal_characters:
            require(any(multiplicity==2 for multiplicity in actual.values()),
                    'Nonreduced terminal example has a repeated rational eigenvalue')
        results.append({'d': str(d), 'c0': str(c0), 'c1': str(c1),
                        'rational_roots': {str(root): multiplicity for root, multiplicity in actual.items()},
                        'zero_terminal_rational_characters': zero_terminal_characters,
                        'determinant': str(poly.as_expr())})
    # A zero nonterminal radicand is deliberately outside the theorem.
    Mt = sp.Matrix([[0,0,0,0], [1,0,0,0], [0,0,0,0], [0,0,1,0]])
    require((sp.eye(4)-8000*Y*Mt).det()==1, 'Nonterminal-zero counterexample')
    # Here t=0,q=+/-1 are two rational characters; the same formula loses both.
    return {'examples': results, 'nonterminal_zero_rejected': True}


def main(output, specifications):
    results, controls = [], 0
    for name in NAMES:
        source = make_source(name)
        parent_path = PARENT/'specifications'/(name+'.json')
        parent = json.loads(parent_path.read_text())
        parent_checker.verify_spec(source, parent)
        spec = json.loads((specifications/(name+'.json')).read_text())
        results.append(verify_spec(source, parent, spec, parent_path))
        mutations = []
        bad = deepcopy(spec);bad['bounds']['degree_bound'] -= 1;mutations.append(bad)
        bad = deepcopy(spec);bad['subalgebra_norm_factors'].pop(0);mutations.append(bad)
        bad = deepcopy(spec);bad['terminal_root_policy']['suppressed_source_guard_nodes']=[];mutations.append(bad)
        bad = deepcopy(spec);bad['terminal_root_policy']['preceding_radicands_required_units']=False;mutations.append(bad)
        bad = deepcopy(spec);bad['quadratic_tower'][-1]['envelope_power'] -= 1;mutations.append(bad)
        for bad in mutations:
            try:
                verify_spec(source, parent, bad, parent_path)
            except AssertionError:
                controls += 1
            else:
                raise AssertionError('A deliberate corruption was accepted')
    report = {'schema': 'terminal-root-verification/v40', 'constructions': results,
              'corruption_controls_rejected': controls, 'finite_algebra': algebra_examples(),
              'scope': 'Independent finite reconstruction, denominator coverage and majorants; '
                       'small exact finite-algebra examples include nonreduced fibers. '
                       'The geometric-character descent and arithmetic soundness are proved '
                       'in the companion paper. No external arithmetic premise is certified.'}
    output.write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--specifications', type=Path, default=HERE/'specifications')
    parser.add_argument('--output', type=Path, default=HERE/'verification.json')
    args = parser.parse_args()
    report = main(args.output, args.specifications)
    print(json.dumps({'status': 'passed', 'constructions': len(report['constructions']),
                      'corruption_controls_rejected': report['corruption_controls_rejected'],
                      'finite_algebra_examples': len(report['finite_algebra']['examples']),
                      'verification_sha256': digest(args.output.read_bytes())}, sort_keys=True))
