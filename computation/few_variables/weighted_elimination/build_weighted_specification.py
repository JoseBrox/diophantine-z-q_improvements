#!/usr/bin/env python3
"""Specify the direct-scaled finite-algebra polynomial and certify its bounds.

The input is an already verified guarded monic finite-algebra specification.
No global arithmetic assertion is inferred by this algebraic compiler.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def ceil_log2(n: int) -> int:
    assert n > 0
    return (n - 1).bit_length()


def certify(spec: dict) -> dict:
    assert spec['closed_equations'] == []
    assert spec['indexed_guard_polynomials'] == []
    assert all(len(values) == 1 for values in spec['source_finite_parameters'].values())
    nodes = spec['coefficient_dag']
    relations = spec['monic_relations']
    weights: list[int] = []
    norm_logs: list[int] = []
    cache: dict[int, tuple[int,int]] = {}

    def bound(k: int) -> tuple[int,int]:
        if k in cache:
            return cache[k]
        op, *a = nodes[k]
        if op == 'int':
            out = (0, ceil_log2(max(1, abs(a[0]))))
        elif op == 'variable':
            out = (1, 0)
        elif op == 'parameter':
            out = (0, ceil_log2(max(1, a[1])))
        elif op == 'algebra_generator':
            i = a[0]
            assert i < len(weights), 'A relation is not triangular.'
            out = (weights[i], norm_logs[i])
        elif op == 'neg':
            out = bound(a[0])
        elif op == 'pow':
            u, v = bound(a[0])
            out = (a[1]*u, a[1]*v)
        elif op == 'mul':
            bs = [bound(i) for i in a]
            out = (sum(u for u,v in bs), sum(v for u,v in bs))
        elif op == 'add':
            bs = [bound(i) for i in a]
            out = (max(u for u,v in bs), max(v for u,v in bs)+ceil_log2(len(bs)))
        else:
            raise ValueError(op)
        cache[k] = out
        return out

    n = 1
    for i, rel in enumerate(relations):
        assert rel['generator'] == i
        e = rel['maximum_degree']
        assert e in (2, 4)
        n *= e
        coeffs = [(k, node) for k,node in enumerate(rel['coefficient_nodes_ascending'])
                  if nodes[node] != ['int',0]]
        weights.append(max([1]+[(bound(node)[0]+e-k-1)//(e-k) for k,node in coeffs]))
        norm_logs.append(max([0]+[(bound(node)[1]+e-k-1)//(e-k) for k,node in coeffs])
                         +ceil_log2(max(1,len(coeffs))))
    assert n & (n-1) == 0
    rank_log = n.bit_length()-1
    m = len(relations)
    maximum_selector = m*n*(n+1)//2
    guard_weight, guard_log = bound(spec['materialized_guard_node'])
    lambda_log = ceil_log2(m+1)+max((i+1)*ceil_log2(maximum_selector)+v
                                  for i,v in enumerate(norm_logs))
    w = guard_weight+max(weights)
    beta = guard_log+lambda_log
    old = spec['bounds']
    assert weights == old['generator_weights']
    assert norm_logs == old['generator_operator_log2_norm_bounds']
    assert guard_weight == old['materialized_guard_weight']
    assert guard_log == old['materialized_guard_operator_log2_norm_bound']
    assert beta == old['operator_log2_norm_bound']
    assert n == old['maximum_rank']
    # C(n) = 2 sum_{d=1}^{n-1} max(d^3+d,n)+(n^3+n).
    lo, hi = 0, n
    while hi-lo > 1:
        mid = (hi+lo)//2
        if mid**3+mid < n:
            lo = mid
        else:
            hi = mid
    t = lo
    C = (n**4+3*n*n)//2+2*t*n-t*t*(t+1)*(t+1)//2-t*(t+1)
    selectors = maximum_selector+1
    b = beta+rank_log
    degree = selectors*(w*C+n*n)
    norm_bound = selectors*(b*C+(rank_log+1)*(2*n**3+4*n-2))
    return {
        'method':'direct_scaled_characteristic_polynomials_with_weighted_principal_minors',
        'total_variables':spec['total_external_variables'],
        'retained_base_variables':spec['retained_base_variables'],
        'generator_count':m,
        'rank':n,
        'rank_power_of_two_exponent':rank_log,
        'generator_weights':weights,
        'generator_operator_log2_norm_bounds':norm_logs,
        'guard_weight':guard_weight,
        'guard_operator_log2_norm_bound':guard_log,
        'multiplication_element_weight':w,
        'multiplication_operator_log2_norm_bound':beta,
        'characteristic_coefficient_log2_norm_per_index':b,
        'selector_count':selectors,
        'degree_cases':n,
        'exact_factor_count':selectors*n,
        'small_degree_case_cutoff':t,
        'summed_case_weight':C,
        'degree_bound':degree,
        'degree_bound_power_of_two_exponent':ceil_log2(degree),
        'coefficient_l1_norm_log2_bound':norm_bound,
        'coefficient_height_bound_double_power_of_two_exponent':ceil_log2(norm_bound),
        'degree_bound_formula':'S*(w*C(n)+n^2)',
        'norm_bound_formula':'S*((beta+log2(n))*C(n)+(log2(n)+1)*(2*n^3+4*n-2))',
        'C_formula':'2*sum_{d=1}^{n-1}max(d^3+d,n)+(n^3+n)',
        'semantic_scope':'Same rational base projection as the supplied guarded finite algebra. Global arithmetic hypotheses are unchanged.',
        'expanded_polynomial':'Not materialized; all coefficient operations and finite index ranges are specified exactly.'
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    old = json.loads(raw)
    certificate = certify(old)
    new = dict(old)
    new['format'] = 'integer-polynomial-indexed-finite-algebra/direct-scaled-v1'
    new['source_specification_sha256'] = hashlib.sha256(raw).hexdigest()
    new['polynomial_recipe'] = {
        'theorem':'Direct-scaled elimination theorem in weighted_finite_algebra_20261109_v12.tex',
        'lambda':f"1+sum_{{i=1}}^{certificate['generator_count']} selector^i*z_i",
        'H':'det(I-V*M_{G*lambda})=sum_{k=0}^{n} a_k*V^k; a_0=1',
        'H_d':'sum_{k=0}^{d} a_k*V^k',
        'g_d':'Res_V(H_d, derivative_V(H_d)), Sylvester degrees d and d-1',
        'Q_d_for_d_less_than_n':'H_d(g_d*U)^2+sum_{k=d+1}^{n} a_k^2',
        'Q_n':'H_n(g_n*U)',
        'product':'Product of Q_d over selector=0,...,m*n*(n+1)/2 and d=1,...,n',
        'source_parameters':'Use the unique listed value of each source_finite_parameter',
        'only_external_variables':'external_variables; formal algebra generators and V are eliminated by finite matrix/coefficient operations'
    }
    new['bounds'] = certificate
    args.output.mkdir(parents=True,exist_ok=True)
    out = args.output/'polynomial-specification.json'
    out.write_text(json.dumps(new,indent=2)+'\n')
    certificate['input_specification_sha256'] = hashlib.sha256(raw).hexdigest()
    certificate['output_specification_sha256'] = hashlib.sha256(out.read_bytes()).hexdigest()
    certificate['family_parameter'] = old['family_parameter']
    certificate['arithmetic_status'] = old['arithmetic_status']
    (args.output/'construction-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps(certificate,indent=2))

if __name__ == '__main__':
    main()
