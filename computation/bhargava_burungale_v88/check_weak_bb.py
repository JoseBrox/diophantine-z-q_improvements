"""Independently audit the nine extra guard removals and BB final receipts.

The source DAG, full point charts, native pole identity, denominator coverage,
and parent norm-factor bounds are first checked by check_full_auxiliary.py.
This file does not import either certificate producer. It then reconstructs
the three new proof stages and recomputes the determinant bounds directly.
The number-theoretic and positivity arguments are in the accompanying proof;
finite computation is not advertised as proving their quantified statements.
"""
from copy import deepcopy
from fractions import Fraction
from functools import cache
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ORDER = [
    'pre_character_root_ordinate', 'pre_character_auxiliary_abscissas',
    'point_separator_and_rational_character', 'post_character_root_abscissa',
    'retained_point_and_contact_units', 'positive_contact_sums',
    'odd_weight_normalizer', 'positive_balancing_atoms',
    'positive_product_atoms',
]


def audit(directory, cert=None):
    source = json.loads((directory / 'native.json').read_text())
    parent = json.loads((directory / 'polynomial.json').read_text())
    compact = json.loads((directory / 'compact.json').read_text())
    if cert is None:
        cert = json.loads((directory / 'strengthened.json').read_text())
    nodes = source['coefficient_dag']

    @cache
    def factors(i):
        op, *args = nodes[i]
        if op == 'int':
            return frozenset()
        if op == 'neg':
            return factors(args[0])
        if op == 'pow':
            return factors(args[0]) if args[1] else frozenset()
        if op == 'mul':
            return frozenset().union(*(factors(j) for j in args))
        return frozenset([i])

    # Arithmetic replay uses the independently checked native DAG, not the
    # lists of automatically nonzero factors proposed by the producer.
    from field_circuit import Circuit, Rational
    c = Circuit()
    for i, row in enumerate(nodes):
        assert c.node(*row) == i
    def rat(r):
        return Rational(c, r['numerator'], r['denominator'])
    contacts, = [e for e in source['events'] if e['operation'] == 'moving_contacts']
    p, q, u = map(rat, [contacts['p'], contacts['q'], contacts['u']])
    k = contacts['band']
    summands = [p*p+q**3, p**3+q**5, p+q**k, p**k+q]
    positive = frozenset().union(*(factors(a.n) for a in summands))
    assert len(positive) == 4
    assert factors(u.d) < positive
    normalizer = factors((1+u).n)
    assert len(normalizer) == 1
    stages = {
        'positive_contact_sums': sorted(positive),
        'odd_weight_normalizer': sorted(normalizer),
    }
    points = [e for e in source['events'] if e['operation'] == 'point_block']
    assert [p['name'] for p in points] == ['A', 'H', 'UA']
    root_ordinate = factors(source['finite_blocks'][0]['variable_nodes'][-1])
    def point_norm(p):
        h0, h1 = map(rat, p['h'])
        return factors((h0*h0-2*h1*h1).n)
    auxiliary_abscissas = frozenset().union(*(point_norm(p) for p in points[1:]))
    root_abscissa = point_norm(points[0])
    assert len(root_ordinate) == len(root_abscissa) == 1
    assert len(auxiliary_abscissas) == 2
    stages.update({'pre_character_root_ordinate':sorted(root_ordinate),
                   'pre_character_auxiliary_abscissas':sorted(auxiliary_abscissas),
                   'post_character_root_abscissa':sorted(root_abscissa)})
    assert cert['additional_automatic_guards'] == stages
    assert cert['recovery_order'] == ORDER
    auto = positive | normalizer | root_ordinate | auxiliary_abscissas | root_abscissa
    initial = set(compact['retained_norm_atoms'])
    assert len(auto) == 9 and auto <= initial
    retained = initial - auto
    assert cert['retained_norm_atoms'] == sorted(retained)

    # The contact lemma uses a monic even product with roots in [-1,0].
    theta = list(map(Fraction, contacts['theta']))
    assert len(theta) == 8 and len(set(theta)) == 8
    assert all(-1 <= t <= 0 for t in theta)
    assert k >= 2 and contacts['scale_power'] > 0
    # Nothing from the old compact proof stages or original norm separator
    # can be silently altered by this additional guard optimization.
    for key in ['positive_balancing_atoms', 'positive_product_atoms',
                'rank', 'variables', 'separator_degree',
                'suppressed_pole_node', 'native_source_sha256']:
        assert cert[key] == compact[key]
    assert auto.isdisjoint(compact['positive_balancing_atoms'])
    assert auto.isdisjoint(compact['positive_product_atoms'])

    rows = {row['node']: row for row in parent['subalgebra_norm_factors']}
    assert retained <= rows.keys()
    g = sum(rows[i]['scalar_norm_degree_bound'] for i in retained)
    gl = sum(rows[i]['scalar_norm_log2_l1_bound'] for i in retained)
    tower = parent['quadratic_tower']
    weights = [row['root_weight'] for row in tower]
    env = [row['envelope_degree'] for row in tower]
    separator = max(sum(weights), *(sum(weights[:i+1])+sum(env[i+1:])
                                  for i in range(len(tower)-1)))
    log_separator = tower[-1]['root_operator_log2_norm']
    for i in reversed(range(len(tower)-1)):
        log_separator = tower[i]['root_operator_log2_norm'] + 1 + max(
            log_separator, sum(2+row['envelope_log2_l1'] for row in tower[i+1:]))
    rank = math.prod(block['degree'] for block in source['finite_blocks'])
    variables = source['total_external_variables']
    determinant_degree = rank * (1 + g + separator)
    terms = math.comb(determinant_degree+variables, variables) - math.comb(
        determinant_degree-rank+variables-1, variables)
    l1 = rank * (1 + gl + log_separator)
    expected = {'rank': rank, 'variables': variables, 'guard_degree': g,
                'separator_degree': separator,
                'degree_bound': determinant_degree+1,
                'support_power': terms.bit_length(),
                'coefficient_log2_l1': l1,
                'coefficient_double_power': l1.bit_length()}
    for key, value in expected.items():
        assert cert[key] == value, (key, cert[key], value)
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=HERE.parents[1]/'diophantine')
    parser.add_argument('directories', nargs='*', type=Path,
                        default=[HERE/'full_flip_first', HERE/'full_strong_flip'])
    parser.add_argument('--report',type=Path)
    args = parser.parse_args()
    answers=[]
    sys.path.insert(0, str(args.repo.resolve()/'computation/few_variables/trace27_nontorsion'))
    subprocess.run([sys.executable, '-B', str(HERE/'check_weak_bb_full.py'),
                    '--repo', str(args.repo.resolve()),
                    *(str(d.resolve()) for d in args.directories)], check=True)
    for directory in args.directories:
        result = audit(directory)
        cert = json.loads((directory/'strengthened.json').read_text())
        # Three concrete corruption controls exercise the independent layer.
        mutations = []
        bad = deepcopy(cert); bad['degree_bound'] -= 1; mutations.append(bad)
        bad = deepcopy(cert); bad['retained_norm_atoms'].pop(); mutations.append(bad)
        bad = deepcopy(cert); bad['recovery_order'][1:3] = reversed(bad['recovery_order'][1:3]); mutations.append(bad)
        for bad in mutations:
            try:
                audit(directory, bad)
            except AssertionError:
                pass
            else:
                raise AssertionError('A corrupted receipt was accepted')
        answers.append({'directory':directory.name,'status':'PASS','corruption_controls_rejected':3,**result})
        print(directory.name, json.dumps(result, sort_keys=True), '3 corruption controls rejected')
    if args.report:
        args.report.write_text(json.dumps({'status':'PASS','new_producer_imported':False,'terminal_zero_roots_allowed':True,'routes':answers},indent=2)+'\n')


if __name__ == '__main__':
    main()
