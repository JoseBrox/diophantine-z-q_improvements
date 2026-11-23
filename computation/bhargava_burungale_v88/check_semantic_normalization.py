"""Check the manuscript's ordered factor identities using the pinned circuit.

Run against the published balanced sources. No new producer is imported.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import math
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--work-root', type=Path, required=True)
parser.add_argument('--source', type=Path)
parser.add_argument('--report', type=Path,
                    default=HERE/'semantic_factor_identity.json')
args = parser.parse_args()
if args.source is None:
    args.source = args.work_root/'bb_general'
sys.path.insert(0, str(args.work_root/'diophantine/computation/few_variables/trace27_nontorsion'))
from field_circuit import Circuit, Rational

rows = []
for route in ('general25', 'explicit27'):
    source = json.loads((args.source/route/'native.json').read_text())
    circuit = Circuit()
    for index, node in enumerate(source['coefficient_dag']):
        assert circuit.node(*node) == index

    def rational(value):
        return Rational(circuit, value['numerator'], value['denominator'])

    def leaf(node):
        return Rational(circuit, node, circuit.one)

    def constant(node):
        operation, *values = circuit.nodes[node]
        if operation == 'int':
            return values[0]
        if operation == 'pow':
            return constant(values[0])**values[1]
        if operation == 'mul':
            return math.prod(map(constant, values))
        if operation == 'add':
            return sum(map(constant, values))
        if operation == 'neg':
            return -constant(values[0])
        raise AssertionError(('nonconstant residual', circuit.nodes[node]))

    def unit(value):
        assert constant(value.n) == constant(value.d)

    height = next(event for event in source['events']
                  if event['operation'] == 'combined_height_scales')
    beta = rational(height['beta'])
    A = beta*(beta-1)
    B = (beta-2401)*(32*beta+343)
    poles = [event for event in source['events']
             if event['operation'] == 'bb_product_pole']
    detectors = [event for event in source['events']
                 if event['operation'] == 'combined_detector']
    for index, (pole, detector) in enumerate(zip(poles, detectors, strict=True)):
        d = rational(pole['square_class'])
        argument = rational(detector['argument'])
        if index:
            unit(leaf(argument.d)/rational(height['scalar_denominator'])**2)
        else:
            assert argument.d == circuit.one
        product = circuit.rational(1)
        factors = []
        for contact in map(Fraction, detector['contacts']):
            difference = argument-contact
            unit(leaf(difference.d)/(contact.denominator*leaf(argument.d)))
            # The denominator is exactly b*D. Therefore the exact numerator
            # is b*N-a*D, without a hidden cancellation factor.
            factor = leaf(difference.n)
            factors.append(factor)
            product *= factor
        C = 4_879_476*((2*2399*407)**2 if index == 0 else 1)
        multiplier = A*(beta-2401) if index else A
        for factor in factors[:5 if index else 6]:
            multiplier *= factor
        old_d = d/multiplier**2
        unit(old_d*C*A*B*product)
        new_d = d
        new_t = rational(pole['square_multiplier'])
        original_input = rational(pole['input'])
        reconstructed = new_d*new_t**2
        assert (reconstructed.n, reconstructed.d) == (original_input.n, original_input.d)
        rows.append(dict(route=route, detector=index, constant=C,
                         factor_identity=True, input_identity=True,
                         normalized_degree_pair=[circuit.bounds[new_d.n][0],
                                                 circuit.bounds[new_d.d][0]]))

result = dict(status='PASS', new_producer_imported=False, rows=rows)
args.report.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
