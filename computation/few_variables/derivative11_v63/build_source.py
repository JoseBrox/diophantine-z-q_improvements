#!/usr/bin/env python3
"""Complete nine-shift native integer circuit for the ordinary-abc eleven-variable family.

The stored B=3 member is an algebraic fixture, not a certified defining shift.
Finite point blocks and the one-coordinate determinant recipe are inherited
unchanged from the checked v28 compiler. The new arithmetic source is explicit
below; its infinite existence assertions are proved in the companion paper.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE/'unit_norm_v28'))
from build_sources import OptimizedArithmetic
from build_direct_input_source import DirectInputABCBuilder
from field_circuit import Circuit

_spec = importlib.util.spec_from_file_location('derivative_v28_compiler', BASE/'unit_norm_v28'/'build.py')
_compiler = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_compiler)
canonical = _compiler.canonical


class Derivative11(OptimizedArithmetic, DirectInputABCBuilder):
    def __init__(self, shift=3):
        if type(shift) is not int or shift < 3 or shift % 2 != 1:
            raise ValueError('B must be a fixed odd integer at least three')
        self.shift = shift
        self.c = Circuit()
        self.D = self.field(11, -6)
        self.relations, self.closed_equations, self.events = [], [], []
        self.fourfold_points = {}
        self.X = self.c.variable('input.X', 'retained.input')
        self.point_names = ['A', 'H', 'UA']
        self.abscissas = {name: tuple(self.c.variable(name+'.a'+str(j), 'retained.point')
                                      for j in range(2)) for name in self.point_names}
        self.z = self.c.variable('contact.z', 'retained.slope')
        self.v = self.c.variable('pole.v', 'retained.pole')
        self.s = self.c.variable('pole.s', 'retained.pole')
        self.base_count = len(self.c.variables)

    def build(self):
        points = {name: self.point(name) for name in self.point_names}
        A, H, U = [points[name] for name in self.point_names]
        HminusP = self.difference(H, self.fixed_point())
        UminusA = self.difference(U, A)
        r = self.div(self.parameter_at_identity(U), self.parameter_at_identity(H))
        rp = self.conj(self.div(self.parameter_at_identity(UminusA),
                               self.parameter_at_identity(HminusP)))
        tests = [self.reciprocal(H), self.reciprocal(U),
                 self.conj(self.reciprocal(HminusP)),
                 self.conj(self.reciprocal(UminusA)),
                 self.sub(r, rp), self.sub(r, self.field(self.X))]
        beta = self.X**2 + self.c.parameter('fixed_input_shift', self.shift)
        trace = 2*A['x'][0]
        M = beta**4 + trace**4
        aa, zz = M**4, self.z**2
        t = aa**2-zz
        shifts = [-10,-8,-5,1,2,3,4,6,7]
        G, half_derivative = self.c.rational(1), self.c.rational(0)
        for shift in shifts:
            factor = (aa+shift)**2-zz
            half_derivative, G = (half_derivative*factor+G*(aa+shift), G*factor)
        GA = 2*half_derivative
        primitive_denominator = half_derivative
        u = -9*G/primitive_denominator
        for value, label in [(M,'height.M'), (t,'height.nonzero signed argument'),
                             (G,'contact.G'), (primitive_denominator,'contact.H'),
                             (u,'contact.u'), (1+u,'contact.one_plus_u')]:
            self.c.nonzero(value, label)
        w = u/(1+u)**2
        transformed = []
        W = self.field(1)
        for i, C in enumerate(tests):
            C2 = self.square(C)
            denominator = self.add(self.field(1), self.scale(C2, u))
            self.c.nonzero(self.norm(denominator), 'balanced%d.denominator norm'%i)
            Di = self.div(C2, denominator)
            transformed.append(Di)
            W = self.mul(W, self.add(self.field(1), self.scale(self.square(Di), 1/u)))
        norm = self.norm(W)
        self.c.nonzero(norm, 'detector.product norm')
        self.c.nonzero(W[0], 'detector.trace numerator')
        V = 2*W[0]/norm
        b = w*norm**2/W[0]**2
        eta = 7*b
        self.c.nonzero(eta, 'intrinsic.input')
        radicand = eta*(eta+self.v**2)**2*self.s**4 - eta*(eta-self.v**2)**2*(1-eta)**2
        self.finite_square('intrinsic.Y', radicand, kind='pole')
        self.events.extend([
            dict(operation='moving_contact_height', beta=self.rr(beta), trace=self.rr(trace),
                 M=self.rr(M), A=self.rr(aa), Z=self.rr(zz), t=self.rr(t),
                 G=self.rr(G), G_A=self.rr(GA), H=self.rr(primitive_denominator),
                 u=self.rr(u), w=self.rr(w), shifts=shifts),
            dict(operation='balanced_actual_detector',
                 original_tests=[[self.rr(x) for x in C] for C in tests],
                 transformed_tests=[[self.rr(x) for x in C] for C in transformed],
                 product_components=[self.rr(x) for x in W],
                 product_norm=self.rr(norm), trace=self.rr(V), b=self.rr(b), eta=self.rr(eta)),
            dict(operation='intrinsic_pole', input=self.rr(eta), v=self.rr(self.v),
                 s=self.rr(self.s), radicand=self.rr(radicand))])
        assert self.base_count == 10
        assert [r['kind'] for r in self.relations] == ['point_block']*3+['pole']
        return dict(format='point-block-guarded-source/v63', name='ordinary_abc11',
            retained_base_count=10, total_external_variables=11,
            variables=self.c.variables, coefficient_dag=self.c.nodes,
            finite_blocks=self.relations, guard_numerators=sorted(self.c.guards),
            guard_descriptions=self.c.guard_descriptions, events=self.events,
            fixed_parameters={'fixed_input_shift':self.shift},
            family_parameter=dict(name='B', value=self.shift, quantified=False,
                sufficient_threshold_exists=True, effective_threshold_known=False,
                selected_member_certified_to_define_Z=False),
            multiply_by_input=True,
            proof='papers/conditional_few_variables/derivative_detector11_20261117_v63.tex',
            arithmetic_status='Ordinary rational abc and the precisely retained elliptic, prime-pattern, trace-height and intrinsic-pole inputs; no independent audit of all external foundations is claimed.')


def make_source(shift=3):
    return Derivative11(shift).build()


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_subalgebra = load_module('derivative_v63_subalgebra', BASE/'subalgebra_norms_v30'/'build.py')
_terminal = load_module('derivative_v63_terminal', BASE/'terminal_root_v40'/'build.py')
_terminal.ROOT = HERE.parents[2]


def parent_specification(source):
    result = _subalgebra.compile_specification(source)
    result['native_source_generator'] = 'computation/few_variables/derivative11_v63/build_source.py'
    result['arithmetic_scope'] = source['arithmetic_status']
    result['coefficient_scope'] = 'Coefficient norm bound only for the stored algebraic fixture; no sufficient defining shift is numerically specified.'
    return result


def specification(source, parent_path):
    parent = parent_specification(source)
    result = _terminal.compile_specification(source, parent, parent_path)
    result['arithmetic_scope'] = source['arithmetic_status'] + ' The intrinsic pole implication permits zero ordinate. All preceding point radicands and source denominators remain units.'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--shift', '--parameter', dest='shift', type=int, default=3)
    ap.add_argument('--name', default='ordinary_abc11', choices=['ordinary_abc11'])
    ap.add_argument('--output', type=Path, default=HERE/'specification')
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = make_source(args.shift)
    parent_path = args.output/'subalgebra_parent.json'
    parent_path.write_text(json.dumps(parent_specification(source), indent=2)+'\n')
    spec = specification(source, parent_path)
    (args.output/'source.json').write_bytes(canonical(source))
    (args.output/'polynomial.json').write_text(json.dumps(spec, indent=2)+'\n')
    report = dict(status='PASS', native_source_sha256=hashlib.sha256(canonical(source)).hexdigest(),
                  native_nodes=len(source['coefficient_dag']),
                  guard_count=len(source['guard_numerators']), bounds=spec['bounds'],
                  family_parameter=source['family_parameter'])
    (args.output/'construction.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','native_nodes','guard_count','bounds')},indent=2))


if __name__ == '__main__':
    main()
