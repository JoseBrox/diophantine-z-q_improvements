#!/usr/bin/env python3
"""Build the explicit 29-variable odd-product rational source.

There are 28 retained coordinates, nine quartic point roots, and four
quadratic pole roots. The finite-algebra compiler eliminates all thirteen
roots using one final rational coordinate. The semilocal anchor variant
retains two additional coordinates and gives 31 variables.

Arithmetic scope: the inherited group, height, pole, Lucas, and simultaneous
prime-pattern hypotheses, plus the proved odd-product height identity.
The indexed finite anchor is exact but is not expanded into monomials.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from math import isqrt
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
from field_circuit import Builder as FieldBuilder, Circuit, Rational


class OddProductBuilder(FieldBuilder):
    def __init__(self, *, anchor='finite', share_height=True,
                 normalize_scalar=True, parametrize_poles=True,
                 fixed_scales=True):
        assert share_height and normalize_scalar and parametrize_poles and fixed_scales
        self.fourfold_points = {}
        self.c = Circuit()
        self.D = self.field(11, -6)
        self.anchor_kind = anchor
        self.share_height = share_height
        self.normalize_scalar = normalize_scalar
        self.parametrize_poles = parametrize_poles
        self.fixed_scales = fixed_scales
        self.relations = []
        self.closed_equations = []
        self.events = []
        self.X = self.c.variable('input.X', 'retained.input')
        names = ['A', 'S', 'T', 'Z']
        if not share_height:
            names += ['J0']
        names += ['H', 'UA', 'US', 'UT', 'UZ']
        self.point_names = names
        self.abscissas = {
            name: tuple(self.c.variable(name + '.a' + str(k), 'retained.point')
                        for k in range(2)) for name in names
        }
        self.slope = self.c.variable('slope.lambda', 'retained.slope')
        self.pole_structural = [
            tuple(self.c.variable('detector%d.%s' % (r, k), 'retained.pole')
                  for k in (('conic_parameter', 's') if parametrize_poles
                            else ('e', 's'))) for r in range(3)
        ]
        scalar_e_name = 'conic_parameter' if parametrize_poles else 'e'
        self.scalar_structural = tuple(
            self.c.variable('scalar.' + k, 'retained.scalar_pole')
            for k in ((scalar_e_name, 's') if normalize_scalar
                      else ('t', scalar_e_name, 's')))
        self.anchor_structural = None
        if anchor == 'semilocal':
            self.anchor_structural = tuple(
                self.c.variable('anchor.' + k, 'retained.anchor')
                for k in ('v', 'w'))
        self.base_count = len(self.c.variables)
        self.correction_primes = ((2,3,11,17,37,67,71,5,19,23,349,661,5209)
                                  if normalize_scalar else (2,3,5,7,11,13,17))
        self.correction = self.c.parameter('scalar_correction',
            518513917206770054130 if normalize_scalar else 510510)
        self.zero_choices = [self.c.parameter('zero_component%d' % r, 1)
                             for r in range(0 if fixed_scales else 8)]
        self.conic_charts = {
            label: self.c.parameter('pole_chart_' + label, 1)
            for label in ([('detector%d' % r) for r in range(3)]+['scalar']
                          if parametrize_poles else [])}

    def rr(self, value):
        value = self.c.rational(value)
        return {'numerator': value.n, 'denominator': value.d}

    def finite_monic(self, name, coefficients, *, kind):
        """Coefficients are listed from degree0, with leading1 omitted."""
        coeffs = [self.c.rational(a) for a in coefficients]
        assert all(a.d == self.c.one for a in coeffs), name
        z = self.c.variable(name, 'finite.' + kind)
        variable = self.c.nodes[z.n][1]
        self.relations.append({
            'name': name, 'kind': kind, 'variable': variable,
            'generator_node': z.n, 'degree': len(coeffs),
            'coefficient_nodes_ascending': [a.n for a in coeffs],
            'monic': True,
        })
        return z

    def finite_square(self, name, value, *, kind):
        """For value=N/D use Z=D*q, so the monic relation is Z²=N*D."""
        value = self.c.rational(value)
        den = Rational(self.c, value.d, self.c.one)
        self.c.nonzero(den, name + '.denominator')
        radicand = Rational(self.c, self.c.mul(value.n, value.d), self.c.one)
        z = self.finite_monic(name, [-radicand, 0], kind=kind)
        self.relations[-1]['original_square_input'] = self.rr(value)
        self.relations[-1]['original_root'] = self.rr(z / den)
        self.relations[-1]['zero_stratum_rule'] = (
            'If radicand is zero use the linear relation Z=0; otherwise '
            'retain Z²=radicand and guard Z!=0. This is a finite case split.')
        return z / den

    def point(self, name):
        self.c.point_count += 1
        a = self.abscissas[name]
        A, B = self.sub(self.mul(self.square(a), a), self.mul(self.D, a))
        # Y=2*b0: Y^4-4*A*Y²+8*B² is monic over the integer DAG.
        Y = self.finite_monic(name + '.Y', [8*B*B, 0, -4*A, 0], kind='point')
        self.c.nonzero(Y, name + '.rational ordinate component')
        self.c.nonzero(A*A-2*B*B, name + '.halfpoint ordinate norm squared')
        derivative = 4*Y**3-8*A*Y
        self.c.nonzero(derivative, name + '.point generator derivative')
        self.relations[-1]['derivative_guard'] = derivative.n
        b = (Y/2, B/Y)
        twice = self.double({'x': a, 'y': b})
        if name in ('A', 'S', 'T', 'Z'):
            fourfold = self.double(twice)
            self.fourfold_points[name] = fourfold
            base = self.fixed_point()
            negative_base = {'x': base['x'], 'y': self.scale(base['y'], -1)}
            point = self.difference(fourfold, negative_base)
            chart = 'P+4R'
        else:
            point = twice
            chart = '2R'
        self.inv(point['x'])
        self.inv(point['y'])
        self.events.append({'operation': 'point', 'name': name, 'chart': chart,
                            'halfpoint_x': [self.rr(v) for v in a],
                            'halfpoint_y': [self.rr(v) for v in b],
                            'output_x': [self.rr(v) for v in point['x']],
                            'output_y': [self.rr(v) for v in point['y']]})
        return point

    def zero_pole(self, b, structural, label):
        self.c.pole_count += 1
        e, s = structural
        self.c.nonzero(b, label + '.nonzero input')
        B = 17*b
        if self.parametrize_poles:
            e = self.conic_parameter(B, e, label)
        h = e*(B-b*b)
        if not self.parametrize_poles:
            self.finite_square(label+'.p', B*(1-e)*(1+3*e), kind='pole')
        self.finite_square(label+'.q', (s*s-B*h)*(s*s+3*B*h)/B, kind='pole')
        self.events.append({'operation': 'preparation_zero_pole', 'label': label,
                            'input': self.rr(b), 'B': self.rr(B), 'h': self.rr(h)})

    def conic_parameter(self, B, t, label):
        sigma = self.conic_charts[label]
        denominator = t*t+3*B
        self.c.nonzero(denominator, label + '.conic chart denominator')
        e = (t*t+(4*sigma-1)*B)/denominator
        self.events.append({'operation': 'rational_pole_conic', 'label': label,
                            'B': self.rr(B), 'parameter': self.rr(t),
                            'chart': self.rr(sigma), 'e': self.rr(e),
                            'denominator': self.rr(denominator),
                            'reconstruct_p': '-4*B*t*(1-chart)/(t^2+3*B)',
                            'exceptional_point': 'chart=1 gives e=1,p=0; '
                                                 't=0 is always permitted.'})
        return e

    def scalar_pole(self, b):
        self.c.pole_count += 1
        if self.normalize_scalar:
            e, s = self.scalar_structural
            self.c.nonzero(b, 'scalar.nonzero pole input')
            B = 17*b
            if self.parametrize_poles:
                e = self.conic_parameter(B, e, 'scalar')
            h = e*(B-b*b)
            if not self.parametrize_poles:
                self.finite_square('scalar.p', B*(1-e)*(1+3*e), kind='scalar_pole')
            self.finite_square('scalar.q', (s*s-B*h)*(s*s+3*B*h)/B,
                               kind='scalar_pole')
            self.events.append({'operation': 'normalized_scalar_preparation_zero',
                                'input': self.rr(b), 'B': self.rr(B),
                                'h': self.rr(h)})
            return
        t, e, s = self.scalar_structural
        self.c.nonzero(b, 'scalar.nonzero pole input')
        U = b*(1-b*t*t)/(1+b*t*t)
        B = 17*b
        if self.parametrize_poles:
            e = self.conic_parameter(B, e, 'scalar')
        h = e*(B-U*U)
        if not self.parametrize_poles:
            self.finite_square('scalar.p', B*(1-e)*(1+3*e), kind='scalar_pole')
        self.finite_square('scalar.q', (s*s-B*h)*(s*s+3*B*h)/B,
                           kind='scalar_pole')
        self.events.append({'operation': 'original_scalar_pole',
                            'input': self.rr(b), 'U': self.rr(U),
                            'B': self.rr(B), 'h': self.rr(h)})

    def scalar_norm(self, r, tests):
        orders = [1, 1, 1, 1, 48, 48]
        assert len(tests) == len(orders)
        self.c.nonzero(r, 'scalar.contact')
        nodes = [1+tests[0]**2/r]
        # This is exactly the source constant-left tree, not a new product test.
        for exponent in sorted(set(orders[1:])):
            xs = [x for x, e in zip(tests[1:], orders[1:]) if e == exponent]
            power = r**exponent
            for i in range(0, len(xs), 2):
                a = xs[i]/power
                nodes.append(a if i+1 == len(xs)
                             else a*a+r*(xs[i+1]/power)**2)
        while len(nodes) > 1:
            nodes = [nodes[i] if i+1 == len(nodes)
                     else nodes[i]**2+r*nodes[i+1]**2
                     for i in range(0, len(nodes), 2)]
        W = nodes[0]
        self.c.nonzero(W, 'scalar.norm root')
        self.scalar_pole(self.correction*r*W*W)
        self.events.append({'operation': 'scalar_norm', 'r': self.rr(r),
                            'test_values': [self.rr(x) for x in tests],
                            'orders': orders, 'root': self.rr(W)})

    def fixed_point(self):
        return {'x': self.field(Fraction(57,8), Fraction(-7,2)),
                'y': self.field(Fraction(-165,8), Fraction(417,32))}

    def build(self):
        points = {name: self.point(name) for name in self.point_names}
        roots = [points[k] for k in ('A', 'S', 'T', 'Z')]
        H = points['H']
        Ui = [points[k] for k in ('UA', 'US', 'UT', 'UZ')]
        J0 = H if self.share_height else points['J0']
        beta = 2*self.X*self.X+3
        base = self.fixed_point()
        targets = [base]+roots
        source_points = [H]+Ui
        differences = [self.difference(p, q)
                       for p, q in zip(source_points, targets)]
        tests = [self.reciprocal(p) for p in source_points]
        tests += [self.conj(self.reciprocal(p)) for p in differences]
        denominator = self.logarithm(H, 64)
        alternate_denominator = self.logarithm(differences[0], 64)
        L, Lprime = [], []
        for i, precision in enumerate([16,64,64,64]):
            L.append(self.div(self.logarithm(Ui[i], precision), denominator))
            Lprime.append(self.conj(self.div(
                self.logarithm(differences[i+1], precision), alternate_denominator)))
        tests += [self.sub(u, v) for u, v in zip(L, Lprime)]
        tests.append(self.sub(L[0], self.field(beta)))
        u, v, w = L[1:]
        u_minus_two = self.sub(u, self.field(2))
        direct_lucas = self.sub(
            self.add(self.square(v), self.mul(self.square(u_minus_two), self.square(w))),
            self.add(self.mul(self.mul(u, u_minus_two), self.mul(v, w)), self.field(1)))
        tests.append(direct_lucas)
        orders = [1]*10+[16,64,64,64]+[16,64]
        assert len(tests) == len(orders) == 16
        self.events.append({'operation': 'direct_Lucas_polynomial_test',
                            'inputs': [[self.rr(a),self.rr(b)] for a,b in L[1:]],
                            'field_value': [self.rr(a) for a in direct_lucas],
                            'polynomial': 'v^2-u*(u-2)*v*w+(u-2)^2*w^2-1',
                            'order': 64})
        squared_tests = [self.square(test) for test in tests]
        product_x = self.field(1)
        for point in roots:
            product_x = self.mul(product_x, point['x'])
        C0, C1 = product_x
        scales = [self.c.rational(1), C0*C0, (1+C1*C1)**2]
        for index, scale in enumerate(scales):
            self.c.nonzero(scale, 'odd-product height scale'+str(index))
        self.events.append({'operation': 'odd_product_height_scales',
                            'root_names': ['A', 'S', 'T', 'Z'],
                            'product_components': [self.rr(x) for x in product_x],
                            'scales': [self.rr(x) for x in scales]})
        contacts = [Fraction(0), Fraction(-1,2), Fraction(-1),
                    Fraction(1,2399), Fraction(-32,407)]
        for r, A in enumerate(scales):
            t = A*self.slope
            delta = t-1
            self.c.nonzero(delta, 'detector%d.normalizer' % r)
            F = self.c.rational(1)
            for theta in contacts:
                factor = t-theta
                self.c.nonzero(factor, 'detector%d.contact%s' % (r, theta))
                F *= factor
            # Algebraically identical to the displayed normalized detector.
            weights = {m: A**(10*m-5)*delta**(10*m-8)/F**(2*m-1)
                       for m in sorted(set(orders))}
            W = self.field(1)
            for square, m in zip(squared_tests, orders):
                factor = self.add(self.field(1), self.scale(square, weights[m]))
                W = self.mul(W, factor)
            norm = W[0]*W[0]-2*W[1]*W[1]
            self.c.nonzero(norm, 'detector%d.product norm' % r)
            self.c.nonzero(W[0], 'detector%d.trace numerator' % r)
            B = F*norm*norm/(4*A**5*delta**6*W[0]*W[0])
            self.zero_pole(B, self.pole_structural[r], 'detector%d' % r)
            self.events.append({'operation': 'detector', 'index': r,
                                'scale': self.rr(A), 'slope_argument': self.rr(t),
                                'F': self.rr(F), 'delta': self.rr(delta),
                                'weights': {str(m): self.rr(w) for m,w in weights.items()},
                                'product_components': [self.rr(w) for w in W],
                                'pole_input': self.rr(B)})
        rbeta = self.c.rational(1)
        for factor in (beta,beta-1,beta-2401,32*beta+343,2*beta-1):
            rbeta *= factor
        if self.normalize_scalar:
            delta_beta = beta*beta+beta+23
            self.c.nonzero(delta_beta, 'scalar.quadratic normalizer')
            raw_contact = rbeta
            rbeta = Fraction(204**2,23**24)*rbeta/(delta_beta**4)
            self.events.append({'operation': 'normalized_scalar_contact',
                                'raw_contact': self.rr(raw_contact),
                                'quadratic_normalizer': self.rr(delta_beta),
                                'normalized_contact': self.rr(rbeta),
                                'fixed_square_root': '204/23^12'})
        scalar_point = self.fourfold_points['S']
        scalar_tests = list(self.reciprocal(J0)+self.reciprocal(scalar_point)+
                            self.div(self.parameter_at_identity(scalar_point),
                                     self.parameter_at_identity(J0)))
        self.events.append({'operation': 'shifted_scalar_and_anchor_point',
                            'point': 'S-P=4R_S',
                            'x': [self.rr(x) for x in scalar_point['x']],
                            'y': [self.rr(y) for y in scalar_point['y']]})
        self.scalar_norm(rbeta, scalar_tests)
        indexed_guards = []
        if self.anchor_kind == 'semilocal':
            v, w = self.anchor_structural
            f0, f1 = self.reciprocal(scalar_point)
            F = f0*f0+f0*f1-f1*f1
            constant = Rational(self.c, self.c.power(self.c.node('int',3), 4*2**24),
                                self.c.one)
            self.finite_square('anchor.u', 3*F*F-6*v*v+2*w*w-2*constant,
                               kind='anchor')
        else:
            indexed_guards.append({
                'name': 'finite size exclusion',
                'operation': 'indexed_product_of_cleared_rational_norms',
                'index_first': 1, 'index_last': {'base':2,'exponent':9566463},
                'variable_field_argument': [self.rr(x) for x in scalar_point['x']],
                'fixed_point': {'x':['57/8','-7/2'],'y':['-165/8','417/32']},
                'fixed_curve_D': [11,-6],
                'factor': 'Norm_K/Q(x(S-P)-x([index]P))',
                'clearing': 'Clear rational denominators factor by factor; all '
                            'variable denominators are separately guarded; fixed '
                            'point denominators are nonzero rational integers.',
                'fixed_multiple_algorithm': 'Repeated group addition, or standard '
                            'elliptic division polynomials with this fixed curve and point.',
                'status': 'Exact indexed finite polynomial, not expanded.'})
        corrections=[]
        primes=self.correction_primes
        for mask in range(1<<len(primes)):
            value=1
            for i,p in enumerate(primes):
                if mask>>i&1: value*=p
            corrections.extend((value,-value))
        count = 29+(2 if self.anchor_kind == 'semilocal' else 0)
        assert self.base_count+1 == count
        assert len(self.relations) == 13+(self.anchor_kind == 'semilocal')
        degree_power = 22+(self.anchor_kind == 'semilocal')
        result = {
            'format': 'shared-point-source-coefficient-dag/v1',
            'status': 'EXACT SOURCE SPECIFICATION; arithmetic inputs and independent '
                      'implementation review remain separate',
            'source_commit': '14e8f601fe0d9173d4a5f084aedc3e07066a7688',
            'additional_arithmetic_input': 'Inherited exponent-24 height and simultaneous prime-pattern hypotheses, including Sun arXiv:2610.20691v2 Theorem4.1; odd-product identity proved separately',
            'anchor_kind': self.anchor_kind, 'share_scalar_height_point': self.share_height,
            'retained_base_count': self.base_count,
            'total_polynomial_variables_after_finite_algebra': count,
            'variables': self.c.variables, 'coefficient_dag': self.c.nodes,
            'finite_monic_relations': self.relations,
            'finite_generator_count': len(self.relations),
            'monic_degree_product': {'base':2,'exponent':degree_power},
            'closed_equations': self.closed_equations,
            'guard_numerators': sorted(self.c.guards),
            'guard_descriptions': self.c.guard_descriptions,
            'indexed_guard_polynomials': indexed_guards,
            'finite_parameters': {'scalar_correction': corrections,
                **{'zero_component%d'%i:[0,1]
                   for i in range(0 if self.fixed_scales else 8)},
                **{'pole_chart_'+label:[0,1] for label in self.conic_charts}},
            'comparison_tests': [[self.rr(a),self.rr(b)] for a,b in tests],
            'comparison_orders': orders, 'events': self.events,
            'counts': dict(Counter(v['category'] for v in self.c.variables)),
            'semantics': 'Every coefficient DAG node is an integer polynomial '
                        'in the retained variables, previous finite generators, '
                        'and fixed finite parameters. Each source branch imposes '
                        'the monic relations, closed numerator equations, all '
                        'listed nonzero guards, and the indexed anchor guard '
                        'when present. Finite-case normalization of repeated '
                        'quadratic roots is still required by the finite-algebra '
                        'compiler; it introduces no quantified selector.'
        }
        if self.normalize_scalar:
            result['scalar_contact_normalized'] = True
            result['scalar_preparation_fixed_zero'] = True
            result['scalar_normalization_proof'] = 'scalar_preparation_zero.tex'
        if self.parametrize_poles:
            result['pole_first_conics_parametrized'] = True
        if self.fixed_scales:
            result['height_scales_without_case_parameters'] = True
        result['direct_Lucas_polynomial_test'] = True
        result['direct_Lucas_proof'] = 'direct_polynomial.tex'
        result['beta_formula'] = '2*input.X^2+3'
        result['odd_root_chart'] = 'P+4R for A,S,T,Z; 2R for H,UA,US,UT,UZ'
        result['comparison_targets'] = 'P,A,S,T,Z (direct targets)'
        result['height_point'] = 'S-P=4R_S'
        result['odd_product_height_proof'] = '../odd_product_construction.tex'
        result['arithmetic_profile'] = {'height_exponent': 24, 'height_log2_upper_bound': 4783227,
            'formal_orders': [16,64,64,64], 'scalar_order': 48,
            'new_asymmetric_depth_prime_separation_used': False}
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--anchor',choices=['finite','semilocal'],default='finite')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    obj=OddProductBuilder(anchor=args.anchor).build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(obj,separators=(',',':'))+'\n').encode('ascii')
    if args.output.suffix=='.gz':
        args.output.write_bytes(gzip.compress(raw,compresslevel=1,mtime=0))
    else:
        args.output.write_bytes(raw)
    print(json.dumps({k:obj[k] for k in ('anchor_kind','share_scalar_height_point',
        'retained_base_count','total_polynomial_variables_after_finite_algebra',
        'finite_generator_count','monic_degree_product','counts')},indent=2))
    print(json.dumps({'coefficient_nodes':len(obj['coefficient_dag']),
                      'uncompressed_bytes':len(raw),
                      'uncompressed_sha256':hashlib.sha256(raw).hexdigest()}))


if __name__=='__main__':
    main()
