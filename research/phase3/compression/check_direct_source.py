#!/usr/bin/env python3
"""Audit the phase3 source change and four frozen coefficient DAGs.

The AST comparison proves that the previous source formulas outside the
specified replacement are literally unchanged. Small polynomial identities
are checked by independent sparse Laurent-polynomial arithmetic. Rebuilding
the files is a reproducibility check, not an arithmetic projection theorem.
"""
from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import gzip
import hashlib
import json
from math import prod
from pathlib import Path

from build_direct_source import DirectBuilder

HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / 'phase2/new_polynomials/build_shared_source.py'
NEW = HERE / 'build_direct_source.py'
CASES = [
    ('source-41-direct.json.gz', 'finite', 2, 40, 19, 28,
     '540e8f30c51525eefc8cb8a46da4b2bb59da460d214977631f6e9c03488be974'),
    ('source-43-direct-semilocal.json.gz', 'semilocal', 2, 42, 20, 29,
     'f30f5113bdb1e09c7b79188a99d1ad9516fe6b79ba3208d9c5171674365baa95'),
    ('source-41-shift2402.json.gz', 'finite', 2402, 40, 19, 28,
     '18867094aa587a12fb87e1118259a5f24c392b5186e14d01f83ef7526801e953'),
    ('source-43-semilocal-shift2402.json.gz', 'semilocal', 2402, 42, 20, 29,
     '13019caa7b4003697ef143ca439878759e327c74d78ab10857c1e64b684a16b6'),
]


def dump(value):
    if isinstance(value, list):
        return [dump(x) for x in value]
    return ast.dump(value, include_attributes=False)


def methods(path):
    tree = ast.parse(path.read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    return {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}


class ReplaceConstants(ast.NodeTransformer):
    def __init__(self, mapping):
        self.mapping = mapping

    def visit_Constant(self, node):
        if type(node.value) is int and node.value in self.mapping:
            node.value = self.mapping[node.value]
        return node


def check_source_diff():
    old, new = methods(OLD), methods(NEW)
    assert set(old) == set(new)
    unchanged = sorted(set(old) - {'__init__', 'build'})
    assert all(dump(old[k]) == dump(new[k]) for k in unchanged)

    oi, ni = old['__init__'].body, new['__init__'].body
    assert len(oi) == len(ni) == 29
    assert ast.unparse(oi[16]).startswith("self.xi = self.c.variable('proxy.xi'")
    assert ast.unparse(oi[17]).startswith("self.zeta = self.c.variable('proxy.zeta'")
    assert isinstance(ni[0], ast.If)
    assert ast.unparse(ni[1]) == 'self.beta_shift = beta_shift'
    assert dump(oi[:16] + oi[18:]) == dump(ni[2:])

    ob, nb = deepcopy(old['build'].body), deepcopy(new['build'].body)
    assert len(ob) == 53 and len(nb) == 54
    assert ast.unparse(ob[5]) == 'beta = self.X * self.X + 2'
    assert ast.unparse(nb[5]) == 'beta = self.X * self.X + self.beta_shift'
    assert [ast.unparse(n).split(' = ')[0] for n in ob[6:13]] == [
        'a', 'b', 'tau', "self.relations[-1]['zero_discriminant_rule']",
        "self.relations[-1]['a']", "self.relations[-1]['b']", 'proxies']
    assert 'zip(L, proxies)' in ast.unparse(ob[24])
    assert ast.unparse(nb[17]) == 'tests.append(self.sub(L[0], self.field(beta)))'
    assert ast.unparse(nb[18]) == 'u, v, w = L[1:]'
    assert ast.unparse(nb[21]) == 'tests.append(direct_lucas)'
    assert ast.unparse(nb[23]) == 'assert len(tests) == len(orders) == 16'
    assert "'direct_Lucas_polynomial_test'" in ast.unparse(nb[24])
    assert ast.unparse(nb[50]) == "result['direct_Lucas_polynomial_test'] = True"
    assert ast.unparse(nb[51]) == "result['direct_Lucas_proof'] = 'direct_polynomial.tex'"
    assert ast.unparse(nb[52]).startswith('if self.beta_shift != 2:')

    # The only numerical metadata changes are 2 retained proxies and one
    # quadratic finite generator. All remaining mathematical code is identical.
    ob[43] = ReplaceConstants({46: 44}).visit(ob[43])
    ob[46] = ReplaceConstants({21: 20}).visit(ob[46])
    ob[47] = ReplaceConstants({21: 20}).visit(ob[47])
    assert dump(ob[:5] + ob[13:24] + ob[27:]) == dump(
        nb[:5] + nb[6:17] + nb[25:50] + nb[53:])
    assert not any(isinstance(n, ast.Attribute) and n.attr in ('xi', 'zeta')
                   for n in ast.walk(new['build']))
    assert not any(isinstance(n, ast.Name) and n.id in ('tau', 'proxies')
                   for n in ast.walk(new['build']))
    return new['build'], {
        'unchanged_methods': unchanged,
        'other_build_statements_AST_identical': True,
        'old_builder_sha256': hashlib.sha256(OLD.read_bytes()).hexdigest(),
        'new_builder_sha256': hashlib.sha256(NEW.read_bytes()).hexdigest(),
        'change_scope': ['remove retained xi,zeta and finite tau',
                        'replace three proxy comparisons by direct F at order64',
                        'change corresponding counts and descriptive metadata',
                        'make previously preferred refinement options defaults',
                        'optional beta=X^2+C, default C=2'],
    }


class Poly:
    """Small exact Laurent polynomials in six variables; no CAS dependency."""
    N = 6

    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            self.terms = dict(terms.terms)
        elif isinstance(terms, dict):
            self.terms = {tuple(k): Fraction(v) for k, v in terms.items() if v}
        else:
            self.terms = {(0,) * self.N: Fraction(terms)} if terms else {}

    @classmethod
    def variable(cls, index):
        exponent = [0] * cls.N
        exponent[index] = 1
        return cls({tuple(exponent): 1})

    def __add__(self, other):
        ans = dict(self.terms)
        for e, c in Poly(other).terms.items():
            ans[e] = ans.get(e, Fraction(0)) + c
        return Poly(ans)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        ans = {}
        for a, c in self.terms.items():
            for b, d in Poly(other).terms.items():
                e = tuple(x + y for x, y in zip(a, b))
                ans[e] = ans.get(e, Fraction(0)) + c * d
        return Poly(ans)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int)
        if n < 0:
            assert len(self.terms) == 1
            e, c = next(iter(self.terms.items()))
            return Poly({tuple(n * x for x in e): c ** n})
        result, x = Poly(1), self
        while n:
            if n & 1:
                result *= x
            x *= x
            n //= 2
        return result

    def __truediv__(self, other):
        return self * Poly(other) ** -1

    def __rtruediv__(self, other):
        return Poly(other) / self

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def record(self):
        return [{'exponents': list(e), 'coefficient': str(c)}
                for e, c in sorted(self.terms.items())]


class ExactQuadraticField:
    @staticmethod
    def field(a=0, b=0):
        return (Poly(a), Poly(b))

    @staticmethod
    def add(a, b):
        return a[0] + b[0], a[1] + b[1]

    @staticmethod
    def sub(a, b):
        return a[0] - b[0], a[1] - b[1]

    @staticmethod
    def mul(a, b):
        return a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]

    @classmethod
    def square(cls, a):
        return cls.mul(a, a)


def eval_expr(node, context):
    return eval(compile(ast.Expression(node), '<audited source expression>', 'eval'),
                {'__builtins__': {}, 'sorted': sorted, 'set': set}, context)


def check_polynomial_identities(build):
    a, b, c, d, e, f = [Poly.variable(i) for i in range(6)]
    context = {'self': ExactQuadraticField(),
               'u': (a, b), 'v': (c, d), 'w': (e, f)}
    context['u_minus_two'] = eval_expr(build.body[19].value, context)
    actual = eval_expr(build.body[20].value, context)

    # Independently expanded rational and sqrt2 components of F.
    K0, K1 = a*a - 2*a + 2*b*b, 2*a*b - 2*b
    M0, M1 = c*e + 2*d*f, c*f + d*e
    L0, L1 = a*a - 4*a + 4 + 2*b*b, 2*a*b - 4*b
    N0, N1 = e*e + 2*f*f, 2*e*f
    expected = (c*c + 2*d*d - K0*M0 - 2*K1*M1 + L0*N0 + 2*L1*N1 - 1,
                2*c*d - K0*M1 - K1*M0 + L0*N1 + L1*N0)
    assert actual == expected
    assert all(all(x >= 0 for x in exponent)
               for q in actual for exponent in q.terms)
    assert max(sum(e) for q in actual for e in q.terms) == 4

    loop = build.body[30]
    assert isinstance(loop, ast.For)
    assignments = {n.targets[0].id: n for n in loop.body
                   if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    A, delta, F, w0, w1, unused = [Poly.variable(i) for i in range(6)]
    weights = eval_expr(assignments['weights'].value,
                       {'A': A, 'delta': delta, 'F': F, 'orders': [1, 16, 64]})
    R = F / (A**5 * delta**6)
    for m in (1, 16, 64):
        expected_weight = R / (delta**(2*m+2) * R**(2*m))
        assert weights[m] == expected_weight
        assert weights[m] == Poly({(10*m-5, 10*m-8, 1-2*m, 0, 0, 0): 1})
    norm = w0*w0 - 2*w1*w1
    actual_B = eval_expr(assignments['B'].value,
                         {'F': F, 'norm': norm, 'A': A, 'delta': delta,
                          'W': [w0, w1]})
    expected_B = Poly({(-5, -6, 1, 2, 0, 0): Fraction(1, 4),
                       (-5, -6, 1, 0, 2, 0): -1,
                       (-5, -6, 1, -2, 4, 0): 1})
    assert actual_B == expected_B
    return {
        'direct_F_degree': 4,
        'direct_F_variables': ['u0', 'u1', 'v0', 'v1', 'w0', 'w1'],
        'direct_F_rational_component': actual[0].record(),
        'direct_F_sqrt2_component': actual[1].record(),
        'detector_weights_checked_orders': [1, 16, 64],
        'detector_weight_identity': 'R/(delta^(2*m+2)*R^(2*m))='
                                   'A^(10*m-5)*delta^(10*m-8)/F^(2*m-1)',
        'reciprocal_trace_pole_input_identity':
            'R/(Tr(W^-1))^2=F*(w0^2-2*w1^2)^2/(4*A^5*delta^6*w0^2)',
        'arithmetic': 'Exact independent sparse Laurent polynomials over Q',
    }


def check_case(name, anchor, shift, base, generators, rank_exp, digest):
    raw = gzip.decompress((HERE / name).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == digest
    obj = json.loads(raw)
    rebuilt = DirectBuilder(anchor=anchor, beta_shift=shift).build()
    assert raw == (json.dumps(rebuilt, separators=(',', ':')) + '\n').encode('ascii')
    nodes, variables = obj['coefficient_dag'], obj['variables']
    assert [v['index'] for v in variables] == list(range(len(variables)))
    assert all(v['category'].startswith('retained.') for v in variables[:base])
    assert all(v['category'].startswith('finite.') for v in variables[base:])
    assert len(variables) == base + generators
    assert not any('proxy' in v['name'] or v['category'] == 'finite.Lucas'
                   for v in variables)
    assert obj.get('beta_shift', 2) == shift
    assert ('beta_shift' in obj) == (shift != 2)
    deps = []
    for index, node in enumerate(nodes):
        op = node[0]
        if op == 'int':
            assert len(node) == 2 and isinstance(node[1], int)
            dependency = 0
        elif op == 'parameter':
            assert node[1] in obj['finite_parameters']
            dependency = 0
        elif op == 'variable':
            assert 0 <= node[1] < len(variables)
            dependency = 1 << node[1]
        else:
            assert op in ('add', 'mul', 'neg', 'pow')
            children = node[1:2] if op in ('neg', 'pow') else node[1:]
            assert all(isinstance(c, int) and 0 <= c < index for c in children)
            if op == 'pow':
                assert isinstance(node[2], int) and node[2] >= 0
            dependency = 0
            for child in children:
                dependency |= deps[child]
        deps.append(dependency)
    relations = obj['finite_monic_relations']
    assert len(relations) == generators
    assert [r['variable'] for r in relations] == list(range(base, len(variables)))
    for relation in relations:
        assert relation['monic'] is True
        coeffs = relation['coefficient_nodes_ascending']
        assert len(coeffs) == relation['degree']
        assert all(0 <= c < len(nodes) for c in coeffs)
        assert all(deps[c] >> relation['variable'] == 0 for c in coeffs)
        assert nodes[relation['generator_node']] == ['variable', relation['variable']]
    assert prod(r['degree'] for r in relations) == 2**rank_exp
    assert obj['monic_degree_product'] == {'base': 2, 'exponent': rank_exp}
    assert obj['retained_base_count'] == base
    assert obj['total_polynomial_variables_after_finite_algebra'] == base + 1
    assert all(0 <= g < len(nodes) for g in obj['guard_numerators'])
    assert not obj['closed_equations']
    assert obj['comparison_orders'] == [1]*10 + [16, 64, 64, 64] + [16, 64]
    assert len(obj['comparison_tests']) == 16
    events = [e for e in obj['events'] if e['operation'] == 'direct_Lucas_polynomial_test']
    assert len(events) == 1 and events[0]['order'] == 64
    assert events[0]['field_value'] == obj['comparison_tests'][-1]
    params = obj['finite_parameters']
    assert len(params['scalar_correction']) == len(set(params['scalar_correction'])) == 16384
    assert all(v != 0 for v in params['scalar_correction'])
    charts = [k for k in params if k.startswith('pole_chart_')]
    assert len(charts) == 10 and all(params[k] == [0, 1] for k in charts)
    assert not any(k.startswith('zero_component') for k in params)
    assert len(params) == 11
    assert all(obj[k] for k in ['pole_first_conics_parametrized',
                                'height_scales_without_case_parameters',
                                'scalar_contact_normalized',
                                'scalar_preparation_fixed_zero',
                                'direct_Lucas_polynomial_test'])
    return {'file': name, 'status': 'PASS', 'beta_shift': shift,
            'retained_base': base, 'finite_generators': generators,
            'finite_rank_power_of_two': rank_exp,
            'relation_degrees': dict(Counter(r['degree'] for r in relations)),
            'dag_nodes': len(nodes), 'guard_count': len(obj['guard_numerators']),
            'uncompressed_sha256': digest}


def main():
    build, diff = check_source_diff()
    identities = check_polynomial_identities(build)
    cases = [check_case(*case) for case in CASES]
    # Reject exactly the rational shifts excluded by the producer's condition.
    for invalid in (1, 0, 2401, 2400, 2397):
        try:
            DirectBuilder(beta_shift=invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(('accepted invalid shift', invalid))
    print(json.dumps({'status': 'PASS',
        'scope': 'Exact AST change review, independently expanded small polynomial '
                 'identities, frozen-byte reproducibility, integer DAG well-formedness, '
                 'triangular monicity, counts, finite parameters and guard references. '
                 'The arithmetic input projection and final finite-algebra compiler '
                 'are separately proved and checked.',
        'source_change': diff, 'polynomial_identities': identities,
        'sources': cases}, indent=2))


if __name__ == '__main__':
    main()
