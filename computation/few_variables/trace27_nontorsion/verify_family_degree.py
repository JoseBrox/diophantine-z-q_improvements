#!/usr/bin/env python3
"""Prove the degree bound uniformly in the fixed odd coefficient exponent.

Replace ell**L and ell**((L+1)//2) by independent coefficient symbols.
They have degree zero in the 27 quantified/input coordinates. No value is
substituted for these symbols in the degree calculation. The temporary
parameter bound 1 is only a grammar placeholder: all coefficient-norm
bounds from that temporary compilation are discarded. The independent
audit below computes ONLY degrees and finite-product cardinalities.
"""
from pathlib import Path
import argparse
from math import comb, prod
import hashlib
import json
import sys
sys.dont_write_bytecode = True

from build_forced_prime_source import PreferredBuilder
from compile_source import compile_source


def independent_degree_audit(spec):
    nodes = spec['coefficient_dag']
    relations = spec['monic_relations']
    weights, memo = [], {}
    allowed_parameters = set(spec['source_finite_parameters']) | {
        'coefficient.ell_L', 'coefficient.ell_half'}

    def degree(i):
        if i in memo:
            return memo[i]
        op, *a = nodes[i]
        if op == 'int': value = 0
        elif op == 'parameter':
            assert a[0] in allowed_parameters
            value = 0
        elif op == 'variable': value = 1
        elif op == 'algebra_generator':
            assert a[0] < len(weights)
            value = weights[a[0]]
        elif op == 'neg': value = degree(a[0])
        elif op == 'pow': value = a[1]*degree(a[0])
        elif op == 'mul': value = sum(degree(j) for j in a)
        elif op == 'add': value = max(degree(j) for j in a)
        else: raise ValueError(op)
        memo[i] = value
        return value

    for relation in relations:
        d = relation['maximum_degree']
        weights.append(max([1]+[
            (degree(node)+d-j-1)//(d-j)
            for j,node in enumerate(relation['coefficient_nodes_ascending'])
            if nodes[node] != ['int',0]]))
    p = sum(r['kind']=='point' for r in relations)
    q = len(relations)-p
    m = p+q
    rank = 4**p*2**q
    basis = sum((r['maximum_degree']-1)*weights[r['generator']]
                for r in relations)
    guard = degree(spec['materialized_guard_node'])
    residuals = [r['numerator'] for r in spec['closed_equations']]
    residual = max([0]+[degree(i) for i in residuals])
    alpha = guard+max(weights)+basis
    determinant = rank*alpha
    adjugate_trace = (rank-1)*alpha+residual+basis
    reciprocal_scale = (2*rank+2)*determinant
    branch = 2*max(determinant,rank*(reciprocal_scale+1),
                   adjugate_trace+(rank-1)*(reciprocal_scale+1))
    charts = prod(len(v) for v in spec['source_finite_parameters'].values())
    factors = charts*rank*(1+m*rank*(rank+1)//2)
    total = branch*factors
    actual = spec['bounds']
    assert weights == actual['generator_weights']
    assert basis == actual['maximum_basis_weight']
    assert guard == actual['materialized_guard_weight']
    assert alpha == actual['operator_entry_degree']
    assert factors == actual['exact_number_of_final_factors']
    assert total == actual['degree_bound']
    assert total < 2**154
    return {'status':'passed','total_variables':27,
        'coefficient_symbols':['coefficient.ell_L','coefficient.ell_half'],
        'coefficient_symbols_are_quantified':False,
        'coefficient_symbols_have_degree_zero':True,
        'no_coefficient_value_substituted_in_degree_calculation':True,
        'generator_weights':weights,'maximum_rank':rank,
        'source_chart_cases':charts,'exact_number_of_final_factors':factors,
        'degree_bound':total,'degree_bound_power_of_two_exponent':154,
        'valid_for':'Every integer specialization of both coefficient symbols, hence every fixed odd L>=3.',
        'coefficient_height_bound_for_eventually_valid_member':None,
        'scope':'Uniform degree bound only. Existence of a sufficiently large valid L is mathematical and ineffective.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    builder = PreferredBuilder(anchor_exponent=137731)
    circuit = builder.c
    original_power = circuit.power
    symbols = {137731:'coefficient.ell_L',68866:'coefficient.ell_half'}

    def coefficient_power(node, exponent):
        if circuit.nodes[node]==['int',76249] and exponent in symbols:
            return circuit.node('parameter',symbols[exponent],1)
        return original_power(node,exponent)

    circuit.power = coefficient_power
    source = builder.build()
    spec = compile_source(source,'formal-coefficient-degree-envelope')
    assert spec['source_finite_parameters'] == source['finite_parameters']
    report = independent_degree_audit(spec)
    report['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['formal_coefficient_dag_sha256'] = hashlib.sha256(
        json.dumps(spec['coefficient_dag'],separators=(',',':')).encode()).hexdigest()
    output = args.output or Path(__file__).with_name('degree-family-verification.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
