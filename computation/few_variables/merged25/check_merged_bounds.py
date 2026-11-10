#!/usr/bin/env python3
"""Independent active-algebra bounds and symbolic uniformity for merged25.

The bound checker literally sums all 262144 cases. For uniformity, the
two powers of the fixed prime are replaced by independent coefficient
symbols of degree zero; no coefficient values are substituted in that
calculation. Coefficient-norm bounds for the formal envelope are discarded.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out)
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    checker=module('independent_active_checker',HERE.parent/'active_elimination/check_active_specification.py')
    checker.SOURCES[25]=HERE/'certificate/source-polynomial-specification.json'
    actual=checker.check_directory(HERE/'active25')
    # Producer modules are used only to make the symbolic coefficient envelope;
    # its graph/degree bounds are then checked independently below.
    source_module=module('merged_source_for_formal_envelope',HERE/'build_merged_source.py')
    bound_module=module('active_bound_envelope',HERE.parent/'active_elimination/build_active_specification.py')
    builder=source_module.MergedBuilder(1001)
    original_power=builder.c.power
    symbols={1001:'coefficient.ell_L',501:'coefficient.ell_half'}
    def symbolic_power(node,exponent):
        if builder.c.nodes[node]==['int',76249] and exponent in symbols:
            return builder.c.node('parameter',symbols[exponent],1)
        return original_power(node,exponent)
    builder.c.power=symbolic_power
    source=builder.build()
    source['finite_parameters'].update({name:[1] for name in symbols.values()})
    formal=source_module.compile_source(source,'formal-coefficient-envelope-no-value-substituted')
    bound=bound_module.certify(formal)
    graph=checker.inspect_graph(formal,bound)
    assert all(any(node[:2]==['parameter',name] for node in formal['coefficient_dag'])
               for name in symbols.values())
    assert bound['degree_bound']==actual['degree_bound']
    actual_certificate=json.loads((HERE/'active25/construction-certificate.json').read_text())
    assert bound['generator_weights']==actual_certificate['generator_weights']
    assert bound['guard_weight']==actual_certificate['guard_weight']
    D=actual['degree_bound'];n=25;b=bound['point_algebra_rank'];rank=bound['rank']
    E=(2*b-1)*rank
    support=comb(D+n,n)-comb(D-E+n-1,n)
    report={
        'status':'PASS','total_variables':25,'degree_bound':D,
        'degree_bound_power_of_two_exponent':D.bit_length(),
        'literal_active_case_verification':actual,
        'formal_coefficient_graph_verification':graph,
        'coefficient_symbols':list(symbols.values()),
        'coefficient_symbols_are_quantified':False,
        'coefficient_symbols_have_degree_zero':True,
        'no_coefficient_value_substituted_in_uniform_degree_calculation':True,
        'uniform_in_fixed_odd_exponent':True,
        'formal_coefficient_norm_bounds_discarded':True,
        'last_variable_degree_majorant':E,
        'support_upper_bound':str(support),
        'support_upper_bound_power_of_two_exponent':support.bit_length(),
        'exact_monomial_count':None,
        'support_formula':'binom(D+25,25)-binom(D-E+24,25)',
        'scope':'Independent degree recurrences and a literal sum of all active-algebra factors. The finite coefficient specification is unexpanded, and its monomial count is an upper bound only. The eventual defining exponent is ineffective.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','total_variables','degree_bound',
        'degree_bound_power_of_two_exponent','support_upper_bound_power_of_two_exponent',
        'uniform_in_fixed_odd_exponent')},indent=2))


if __name__=='__main__':main()
