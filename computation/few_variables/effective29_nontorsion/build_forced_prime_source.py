#!/usr/bin/env python3
"""Build the explicit 29-variable source with effective elliptic sum heights.

There are 28 retained coordinates, nine direct-chart quartic roots, and four
quadratic pole roots. The fixed coefficient exponent is L=137731. Under the
four inherited arithmetic inputs, the effective sum-height theorem and the
numerical cutoff prove that this particular source defines the integers.
The automatically invertible point-chart factors are recorded separately.
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


class PreferredBuilder(FieldBuilder):
    def __init__(self, *, anchor_exponent, anchor='forced_prime', share_height=True,
                 normalize_scalar=True, parametrize_poles=True,
                 fixed_scales=True):
        assert share_height and normalize_scalar and parametrize_poles and fixed_scales
        assert anchor == 'forced_prime'
        self.high_order, self.input_order = 39, 10
        self.high_precision, self.input_precision = 40, 12
        self.scalar_order, self.height_exponent = 20, 19
        self.forced_prime = 76249
        if type(anchor_exponent) is not int or anchor_exponent < 3 or anchor_exponent % 2 != 1:
            raise ValueError('anchor_exponent must be an odd integer L >= 3')
        self.forced_exponent = anchor_exponent
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
        self.base_count = len(self.c.variables)
        self.correction = self.c.rational(1)
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
        self.c.nonzero(z, name + '.nontorsion pole root')
        self.relations[-1]['original_square_input'] = self.rr(value)
        self.relations[-1]['original_root'] = self.rr(z / den)
        self.relations[-1]['zero_stratum_rule'] = (
            'The source guard Z!=0 excludes a zero radicand. '
            'Retain only Z²=radicand with nonzero Z.')
        return z / den

    def point(self, name):
        """Direct square-abscissa chart, with a uniformly nonzero root component.

        Put h=h0+h1*sqrt(2), j^2=A+B*sqrt(2)=h^4-D.
        For j=u+v*sqrt(2), the rational component of
        ((2*A+B)-(A+B)*sqrt(2))*j is 2*(u^3-2*v^3).
        It cannot vanish because 2 is not a rational cube.
        """
        self.c.point_count += 1
        h = self.abscissas[name]
        x = self.square(h)
        original_A, original_B = self.sub(self.square(x), self.D)
        multiplier = (2*original_A+original_B, -original_A-original_B)
        A, B = self.mul(self.square(multiplier), (original_A, original_B))
        Y = self.finite_monic(name + '.Y', [8*B*B, 0, -4*A, 0], kind='point')
        self.c.nonzero(Y, name + '.transformed j rational component')
        self.c.nonzero(A*A-2*B*B, name + '.transformed j norm squared')
        derivative = 4*Y**3-8*A*Y
        self.c.nonzero(derivative, name + '.point generator derivative')
        self.relations[-1]['derivative_guard'] = derivative.n
        transformed_j = (Y/2, B/Y)
        j = self.div(transformed_j, multiplier)
        point = {'x': x, 'y': self.mul(h, j)}
        automatic = [Y.n, (A*A-2*B*B).n, derivative.n,
                     (multiplier[0]**2-2*multiplier[1]**2).n]
        self.relations[-1]['automatic_nonzero_nodes'] = automatic
        self.relations[-1]['automatic_nonzero_proof'] = (
            'For every rational h0,h1, U+V*sqrt(2)=h^4-D is nonzero. '
            'The transformed component B=-4U^3+6UV^2+3V^3 is anisotropic '
            'over Q, and the quartic discriminant is '
            '2^15*B^2*(2U^2-V^2)^4*(U^2-2V^2)^2. Thus its roots, '
            'derivative, transformed norm, and multiplier norm are units '
            'in every algebraic fiber over the rational retained base.')
        self.inv(point['x'])
        self.inv(point['y'])
        if name == 'S':
            # This inherited dictionary slot stores S-P, now computed directly.
            self.fourfold_points[name] = self.difference(point, self.fixed_point())
        self.events.append({'operation': 'point', 'name': name,
                            'chart': 'x=h^2; y=h*j; j^2=h^4-D',
                            'square_root_x': [self.rr(v) for v in h],
                            'original_radicand': [self.rr(v) for v in (original_A, original_B)],
                            'multiplier': [self.rr(v) for v in multiplier],
                            'transformed_radicand': [self.rr(v) for v in (A, B)],
                            'transformed_j': [self.rr(v) for v in transformed_j],
                            'j': [self.rr(v) for v in j],
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
        orders = [1, 1, 1, 1, self.scalar_order, self.scalar_order]
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
        beta = 216*self.X**4+450459
        base = self.fixed_point()
        targets = [base]+roots
        source_points = [H]+Ui
        differences = [self.difference(p, q)
                       for p, q in zip(source_points, targets)]
        tests = [self.reciprocal(p) for p in source_points]
        tests += [self.conj(self.reciprocal(p)) for p in differences]
        denominator = self.logarithm(H, self.high_precision)
        alternate_denominator = self.logarithm(differences[0], self.high_precision)
        L, Lprime = [], []
        for i, precision in enumerate([self.input_precision]+[self.high_precision]*3):
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
        orders = [1]*10+[self.input_order]+[self.high_order]*3+[self.input_order,self.high_order]
        assert len(tests) == len(orders) == 16
        self.events.append({'operation': 'direct_Lucas_polynomial_test',
                            'inputs': [[self.rr(a),self.rr(b)] for a,b in L[1:]],
                            'field_value': [self.rr(a) for a in direct_lucas],
                            'polynomial': 'v^2-u*(u-2)*v*w+(u-2)^2*w^2-1',
                            'order': self.high_order})
        squared_tests = [self.square(test) for test in tests]
        sum_x = self.field(0)
        for point in roots:
            sum_x = self.add(sum_x, point['x'])
        scales = [self.c.rational(1), sum_x[0]**2, (sum_x[0]+sum_x[1])**2]
        for index, scale in enumerate(scales):
            self.c.nonzero(scale, 'effective-sum height scale'+str(index))
        self.events.append({'operation': 'effective_sum_height_scales',
                            'root_names': ['A', 'S', 'T', 'Z'],
                            'sum_components': [self.rr(x) for x in sum_x],
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
            raw_contact = rbeta
            prime_power = Rational(self.c, self.c.power(
                self.c.node('int', self.forced_prime), (self.forced_exponent+1)//2), self.c.one)
            contact_power = Rational(self.c, self.c.power(
                self.c.node('int', self.forced_prime), self.forced_exponent), self.c.one)
            delta_beta = 1+17*(prime_power+1)*rbeta
            self.c.nonzero(delta_beta, 'scalar.positive normalizer')
            rbeta = 102**2*contact_power*rbeta/(delta_beta**2)
            self.events.append({'operation': 'normalized_scalar_contact',
                                'raw_contact': self.rr(raw_contact),
                                'positive_normalizer': self.rr(delta_beta),
                                'normalized_contact': self.rr(rbeta),
                                'fixed_square_root': '102',
                                'forced_prime': self.forced_prime,
                                'forced_exponent': self.forced_exponent,
                                'formula': '102^2*ell^L*r/(1+17*(ell^((L+1)/2)+1)*r)^2',
                                'correction': 1})
        scalar_point = self.fourfold_points['S']
        scalar_tests = list(self.reciprocal(J0)+self.reciprocal(scalar_point)+
                            self.div(self.parameter_at_identity(scalar_point),
                                     self.parameter_at_identity(J0)))
        self.events.append({'operation': 'shifted_scalar_and_anchor_point',
                            'point': 'S-P (direct difference)',
                            'x': [self.rr(x) for x in scalar_point['x']],
                            'y': [self.rr(y) for y in scalar_point['y']]})
        self.scalar_norm(rbeta, scalar_tests)
        indexed_guards = []
        count = 29
        assert self.base_count+1 == count
        assert len(self.relations) == 13
        degree_power = 22
        result = {
            'format': 'shared-point-source-coefficient-dag/v1',
            'status': 'An explicitly specified defining polynomial, conditional on exactly the four inherited arithmetic inputs. The fixed exponent satisfies the proved numerical cutoff.',
            'source_commit': '14e8f601fe0d9173d4a5f084aedc3e07066a7688',
            'additional_arithmetic_input': 'The same four source inputs: elliptic group and height, contact-height exponent19, zero-preparation pole completeness, and the simultaneous Sun prime-pattern input. The new sum-height estimate is proved effectively from the retained elliptic height bound; no additional arithmetic hypothesis or ineffective constant is used.',
            'family_parameter': {'name': 'L', 'value': self.forced_exponent,
                'quantified': False, 'constraint': 'odd integer L>=3',
                'sufficient_threshold_exists': True,
                'effective_threshold_known': True,
                'effective_sufficient_threshold': 137731,
                'selected_member_certified_to_define_Z': self.forced_exponent >= 137731},
            'anchor_kind': self.anchor_kind, 'share_scalar_height_point': self.share_height,
            'retained_base_count': self.base_count,
            'total_polynomial_variables_after_finite_algebra': count,
            'variables': self.c.variables, 'coefficient_dag': self.c.nodes,
            'finite_monic_relations': self.relations,
            'finite_generator_count': len(self.relations),
            'monic_degree_product': {'base':2,'exponent':degree_power},
            'closed_equations': self.closed_equations,
            'guard_numerators': sorted(self.c.guards),
            'all_quadratic_roots_nonzero': True,
            'guard_descriptions': self.c.guard_descriptions,
            'indexed_guard_polynomials': indexed_guards,
            'finite_parameters': {**{'zero_component%d'%i:[0,1]
                   for i in range(0 if self.fixed_scales else 8)},
                **{'pole_chart_'+label:[0] for label in self.conic_charts}},
            'comparison_tests': [[self.rr(a),self.rr(b)] for a,b in tests],
            'comparison_orders': orders, 'events': self.events,
            'counts': dict(Counter(v['category'] for v in self.c.variables)),
            'semantics': 'Every coefficient DAG node is an integer polynomial '
                        'in the retained variables, previous finite generators, '
                        'and fixed finite parameters. Each source branch imposes '
                        'the monic relations, closed numerator equations, all '
                        'listed nonzero guards, and the indexed anchor guard '
                        'when present. Every quadratic generator is guarded '
                        'nonzero, so no zero-root stratum is retained. The '
                        'compiler introduces no quantified selector.'
        }
        if self.normalize_scalar:
            result['scalar_contact_normalized'] = True
            result['scalar_preparation_fixed_zero'] = True
            result['scalar_normalization_proof'] = 'Lemma lem:fixed-prime-completeness in the accompanying paper'
        if self.parametrize_poles:
            result['pole_first_conics_parametrized'] = True
        if self.fixed_scales:
            result['height_scales_without_case_parameters'] = True
        result['direct_Lucas_polynomial_test'] = True
        result['direct_Lucas_proof'] = 'Elementary Lucas growth lemma in the accompanying paper'
        result['beta_formula'] = '216*input.X^4+450459'
        result['point_chart'] = 'x=h^2; j^2=h^4-D; y=h*j; all nine nonzero ZP points, without a parity restriction'
        result['point_component_chart'] = 'jprime=((2*A+B)-(A+B)*sqrt(2))*j with j^2=A+B*sqrt(2); its rational component 2*(u^3-2*v^3) is nonzero because 2 is not a rational cube'
        result['comparison_targets'] = 'P,A,S,T,Z (direct targets)'
        result['height_point'] = 'S-P (direct difference)'
        result['effective_sum_height_proof'] = 'B^2 <= 2*h(sum_x) + 80; h(sum_x)<=h(S0)+h(S0+S1)+log(7)/2; three comparison scales give B^2 < 4*(H+log(3))*abs(N)^(19/k)+82'
        result['arithmetic_profile'] = {'height_exponent': self.height_exponent,
            'height_log2_upper_bound': 2093448,
            'formal_orders': [self.input_precision]+[self.high_precision]*3,
            'assigned_comparison_orders': [self.input_order]+[self.high_order]*3,
            'scalar_order': self.scalar_order, 'inherited_height_exponent': 19,
            'new_asymmetric_depth_prime_separation_used': False,
            'forced_prime': self.forced_prime, 'forced_exponent': self.forced_exponent,
            'minimum_forced_contact_valuation': self.forced_exponent,
            'minimum_scalar_index_valuation': (self.scalar_order-1)*self.forced_exponent+1}
        result['correction_free_input_map'] = True
        result['scalar_correction_fixed'] = 1
        result['profile_cutoff_proof'] = 'For L>=137731, 16*(19*L+1)>20*(2093448+6), so abs(a-1)>(64H)^20. The effective height estimate implies the inherited B^2-6<7H*abs(N)^(19/k), and its numerical soundness proof applies.'
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--anchor-exponent',type=int,default=137731,
        help='fixed odd integer L>=137731; default is the certified threshold')
    args=p.parse_args()
    if args.anchor_exponent < 137731:
        p.error('the explicit construction requires odd L>=137731')
    obj=PreferredBuilder(anchor_exponent=args.anchor_exponent).build()
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
