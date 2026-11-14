#!/usr/bin/env python3
"""Exact lower-degree specifications using multiquadratic subalgebra norms.

The v28 arithmetic sources and their rational input projections are unchanged.
No production determinant is expanded. Each JSON file specifies finite integer
polynomial operations, exact source hashes, and proved degree/norm majorants.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Iterable

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / 'unit_norm_v28'
sys.path.insert(0, str(OLD))
from build_sources import make_source
_spec = importlib.util.spec_from_file_location('unit_norm_v28_builder', OLD / 'build.py')
_old = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_old)
NAMES = ('general25', 'explicit27', 'weak13', 'abc13')


def canonical(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


def ceil_log2(n: int) -> int:
    if n < 1:
        raise ValueError('A positive integer is required')
    return (n - 1).bit_length()


def binary_basis(vectors: Iterable[int]) -> tuple[int, ...]:
    """Canonical reduced basis, highest bit first, over F_2."""
    rows: dict[int, int] = {}
    for vector in vectors:
        if vector < 0:
            raise ValueError('Bit vectors must be nonnegative')
        v = vector
        for pivot in sorted(rows, reverse=True):
            if (v >> pivot) & 1:
                v ^= rows[pivot]
        if not v:
            continue
        pivot = v.bit_length() - 1
        for j in list(rows):
            if (rows[j] >> pivot) & 1:
                rows[j] ^= v
        rows[pivot] = v
    return tuple(rows[j] for j in sorted(rows, reverse=True))


def swap_conjugate_bits(vector: int, point_count: int) -> int:
    result = 0
    for i in range(point_count):
        result |= ((vector >> (2*i)) & 1) << (2*i+1)
        result |= ((vector >> (2*i+1)) & 1) << (2*i)
    return result


def compile_specification(source: dict) -> dict:
    old = _old.compile_specification(source)
    nodes = source['coefficient_dag']
    points = old['point_blocks']
    point_count = len(points)
    base_count = source['retained_base_count']
    point_variables: dict[int, tuple[int, tuple[int, ...]]] = {}
    for i, point in enumerate(points):
        xi, eta = 1 << (2*i), 1 << (2*i+1)
        for j, node in enumerate(point['variable_nodes']):
            index = nodes[node][1]
            point_variables[index] = ((xi, (xi ^ eta,)) if j < 2
                                      else (xi ^ eta, ()))

    @lru_cache(None)
    def affine_support(node: int) -> tuple[int, tuple[int, ...]]:
        op, *args = nodes[node]
        if op in ('int', 'parameter'):
            return 0, ()
        if op == 'variable':
            if args[0] < base_count:
                return 0, ()
            if args[0] not in point_variables:
                raise ValueError('A guard factor depends on a pole root')
            return point_variables[args[0]]
        if op == 'neg':
            return affine_support(args[0])
        if op == 'pow':
            if args[1] == 0:
                return 0, ()
            offset, directions = affine_support(args[0])
            return (offset if args[1] % 2 else 0), directions
        if op == 'mul':
            offset = 0
            directions = []
            for child in args:
                a, rows = affine_support(child)
                offset ^= a
                directions.extend(rows)
            return offset, binary_basis(directions)
        if op == 'add':
            offset, rows = affine_support(args[0])
            directions = list(rows)
            for child in args[1:]:
                a, rows = affine_support(child)
                directions.extend(rows)
                directions.append(offset ^ a)
            return offset, binary_basis(directions)
        raise ValueError('Unsupported circuit operation: ' + op)

    guards = []
    for factor in old['support_factor_bounds']:
        offset, directions = affine_support(factor['node'])
        space = binary_basis((offset, *directions))
        conjugate = binary_basis(swap_conjugate_bits(v, point_count) for v in space)
        if conjugate != space:
            raise ValueError('The subalgebra is not stable under Q(sqrt(2))/Q')
        rank = 1 << len(space)
        guards.append(dict(node=factor['node'], affine_offset=offset,
            affine_directions=list(directions), subspace_basis=list(space),
            subspace_dimension=len(space), subalgebra_rank=rank,
            element_degree_bound=factor['degree'],
            element_operator_log2_norm_bound=factor['log_norm'],
            scalar_norm_degree_bound=rank * factor['degree'],
            scalar_norm_log2_l1_bound=rank * factor['log_norm']))
    guard_degree = sum(g['scalar_norm_degree_bound'] for g in guards)
    guard_log = sum(g['scalar_norm_log2_l1_bound'] for g in guards)

    tower = []
    for i, point in enumerate(points):
        tower.extend([
            dict(kind='point_norm', point_index=i, name=point['name']+'.W',
                 square='A_i^2-2*B_i^2', degree=8, operator_log2_norm=11,
                 root_weight=4, root_operator_log2_norm=6),
            dict(kind='point_primitive', point_index=i, name=point['name']+'.z',
                 square='2*A_prime_i+2*(2*A_i^2-B_i^2)*W_i',
                 degree=12, operator_log2_norm=20,
                 root_weight=6, root_operator_log2_norm=12)])
    for i, pole in enumerate(old['quadratic_reductions']):
        tower.append(dict(kind='pole', pole_index=i, name=pole['name'],
            square='sign times the product of the listed odd_factor_nodes',
            degree=pole['degree_bound'],
            operator_log2_norm=pole['operator_log2_norm_bound'],
            root_weight=pole['root_weight'],
            root_operator_log2_norm=pole['root_log2_norm_bound']))
    r_log = ceil_log2(base_count+1)
    for record in tower:
        power = (record['degree']+3)//4
        exponent = (record['operator_log2_norm']+1)//2
        record.update(envelope_power=power, envelope_constant_exponent=exponent,
            envelope_degree=2*power, envelope_log2_l1=exponent+power*r_log)
    terms = []
    for i, record in enumerate(tower):
        degree = (record['envelope_degree']+record['root_weight']
                  +sum(r['degree'] for r in tower[:i])
                  +2*sum(r['envelope_degree'] for r in tower[i+1:]))
        log_norm = (1+record['envelope_log2_l1']+record['root_operator_log2_norm']
                    +sum(r['operator_log2_norm'] for r in tower[:i])
                    +sum(2+2*r['envelope_log2_l1'] for r in tower[i+1:]))
        terms.append(dict(index=i, degree=degree, operator_log2_norm=log_norm))
    omega_degree = max(t['degree'] for t in terms)
    omega_log = ceil_log2(len(tower))+max(t['operator_log2_norm'] for t in terms)
    n = old['bounds']['full_rank']
    degree_before_input = n*(guard_degree+omega_degree+1)
    degree = degree_before_input+int(source['multiply_by_input'])
    coefficient_log = n*(guard_log+omega_log+1)
    variables = base_count+1
    support_bound = (math.comb(degree_before_input+variables, variables)
                     -math.comb(degree_before_input-n+variables-1, variables))
    bounds = dict(total_variables=variables, point_blocks=point_count,
        pole_quadratics=len(old['quadratic_reductions']), full_rank=n,
        guard_factors=len(guards), scalar_guard_degree_bound=guard_degree,
        scalar_guard_log2_l1_bound=guard_log, separator_degree_bound=omega_degree,
        separator_operator_log2_norm_bound=omega_log,
        degree_before_input_factor=degree_before_input, degree_bound=degree,
        strict_degree_power_of_two=degree.bit_length(), separator_variable_degree_bound=n,
        coefficient_log2_l1_bound=coefficient_log,
        coefficient_height_double_power_exponent=coefficient_log.bit_length(),
        monomial_upper_bound=str(support_bound),
        support_strict_power_of_two=support_bound.bit_length(), integer_content=1)
    return dict(schema='subalgebra-norm-polynomial-specification/v30', name=source['name'],
        native_source_sha256=hashlib.sha256(canonical(source)).hexdigest(),
        native_source_generator='computation/few_variables/unit_norm_v28/build_sources.py',
        native_source_arguments=dict(name=source['name'], parameter=source['family_parameter']['value']),
        family_parameter=source['family_parameter'], external_variables=old['external_variables'],
        point_blocks=points, quadratic_reductions=old['quadratic_reductions'],
        guard_factorizations=old['guard_factorizations'],
        subalgebra_norm_factors=guards, quadratic_tower=tower,
        separator_term_bounds=terms, recipe=RECIPE, bounds=bounds,
        multiply_by_input=source['multiply_by_input'],
        arithmetic_scope='Exactly the v28 arithmetic source, assumptions, sufficient parameters and full-unit completeness theorem. No new arithmetic input.',
        coefficient_scope=old['norm_scope'])


RECIPE = {
 'point_algebra': 'The unchanged rank-four tables, tensor order and weights in v28.',
 'extension': 'Extend coefficients to Q(sqrt(2)); set xi_i=U_i/2+sqrt(2)*V_i/2 and eta_i=U_i/2-sqrt(2)*V_i/2.',
 'quadratic_equations': 'xi_i^2=A_i+sqrt(2)*B_i; eta_i^2=A_i-sqrt(2)*B_i; U_i=xi_i+eta_i; V_i=(xi_i-eta_i)/sqrt(2); W_i=xi_i*eta_i.',
 'subalgebra': 'For each listed guard factor f, use the span of square-exponent monomials whose bit vectors lie in subspace_basis. Order bit vectors numerically. Norm is the determinant of multiplication by f on this basis.',
 'integer_descent': 'Conjugation stability makes each subalgebra norm rational. Integrality of the point generators makes it an integer polynomial; no extra variable or choice of a square root of 2 is introduced.',
 'G': 'Product of the subalgebra norms, each factor once. G!=0 is equivalent to the former full scalar norm guard being nonzero at every rational retained tuple.',
 'quadratic_tower': 'In point order use W_i, z_i=(2*A_i+B_i)*U_i-2*(A_i+B_i)*V_i, followed by the square-extracted pole roots.',
 'A_prime_i': '6*A_i^3-9*A_i*B_i^2-4*B_i^3',
 'r': '1+sum of squares of every retained coordinate (the extra separating variable is not included).',
 'M_i': '2^(envelope_constant_exponent) * r^(envelope_power).',
 'Omega': 'Sum over i of 2*M_i*q_i * (product_{k<i} c_k) * (product_{k>i} 4*M_k^2), where q_i is the tower generator and q_i^2=c_i.',
 'P': 'det_A(I-Y*G*M_Omega) on the unchanged full finite algebra in the original v28 basis.',
 'final': 'X*P for the two conditional routes, and P otherwise.',
 'semantics': 'G=0 gives P=1 even on a nonreduced pole boundary. G!=0 gives exactly a rational character of the guarded v28 source. The inherited full-unit completeness theorem preserves every required integer input.',
 'degree_convention': 'Total degree in retained coordinates and Y. Fixed family parameters are coefficients, not quantified variables.'}


def build(directory: Path) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    constructions = []
    for name in NAMES:
        spec = compile_specification(make_source(name))
        (directory/(name+'.json')).write_text(json.dumps(spec, indent=2)+'\n')
        constructions.append(dict(name=name, family_parameter=spec['family_parameter'],
            **spec['bounds'], native_source_sha256=spec['native_source_sha256'],
            coefficient_scope=spec['coefficient_scope']))
    report = dict(schema='subalgebra-norm-degree-bounds/v30', constructions=constructions,
        scope='Upper bounds for finite integer-polynomial specifications, not expanded degrees or global minimum claims. Variable counts and arithmetic assumptions are unchanged.')
    (directory/'bounds.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'specifications')
    args = parser.parse_args()
    for record in build(args.output)['constructions']:
        print(record['name'], record['degree_bound'], '< 2^'+str(record['strict_degree_power_of_two']))
