#!/usr/bin/env python3
"""Independent spectrum/edge-case checks and exact new degree ledgers.

Source arithmetic is not checked here. The check establishes the finite
identities and arithmetic listed in its report; the universal equivalence is
proved in the companion manuscript. Existing source certificates are pinned
and their degree-entry ledgers are replayed from the complete source DAGs.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT/'undecidability'))
from paired_spectral import specification, element_matrix, determinant, degree_bound
from verify_joint_sources import operator_degree_ledger


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_spectra(spec, spectra):
    """Independent unordered-pair product, retaining all multiplicities."""
    Z = spec['paired_polynomial'].gens[0]
    expected = sp.Integer(1)
    for values in spectra:
        assert len(values) == spec['n']
        values = list(values)+[sp.Integer(0)]
        for i in range(len(values)):
            for j in range(i+1, len(values)):
                expected *= Z-(values[i]-values[j])**2
    assert sp.Poly(sp.expand(expected), Z) == spec['paired_polynomial']


def last_stratum(spec):
    coefficients = spec['coefficients']
    assert all(not c.free_symbols for c in coefficients)
    s = max(i for i, c in enumerate(coefficients) if c != 0)
    for j in range(spec['J']+1):
        if j < s:
            assert sum(c*c for c in coefficients[j+1:]) > 0
        elif j > s:
            assert element_matrix(spec, j) == sp.zeros(spec['n'])
    return s


def check_examples():
    U = sp.Symbol('U')
    out = []
    for radicand in (-2, 0, 1, 2, 4):
        t = sp.Matrix([[0, radicand], [1, 0]])
        spec = specification([sp.eye(2), t])
        a = sp.sqrt(radicand)
        check_spectra(spec, [[1, 1], [a, -a]])
        s = last_stratum(spec)
        beta, H = element_matrix(spec, s), determinant(spec, s, U)
        if radicand == 0:
            lam = beta[0, 0]
            assert lam != 0 and H == sp.Poly((1-U*lam)**2, U)
            rational = True
        else:
            disc = int(sp.discriminant(H.as_expr(), U))
            rational = radicand > 0 and math.isqrt(radicand)**2 == radicand
            assert (disc >= 0 and math.isqrt(max(disc, 0))**2 == disc) == rational
        out.append(dict(algebra=f'Q[t]/(t^2-({radicand}))', guard='1',
                        rational_character=rational, J=spec['J'], stratum=s,
                        checks='unordered spectral pairs; all strata; exact discriminant or nilpotent determinant'))

    # Independent nilpotents: this algebra is not monogenic.
    e, f = sp.zeros(4), sp.zeros(4)
    e[1, 0] = e[3, 2] = 1
    f[2, 0] = f[3, 1] = 1
    assert e*e == f*f == sp.zeros(4) and e*f == f*e
    spec = specification([sp.eye(4), e, f])
    check_spectra(spec, [[1]*4, [0]*4, [0]*4])
    s = last_stratum(spec)
    beta, H = element_matrix(spec, s), determinant(spec, s, U)
    lam = beta[0, 0]
    assert lam != 0 and H == sp.Poly((1-U*lam)**4, U)
    out.append(dict(algebra='Q[e,f]/(e^2,f^2)', guard='1', rational_character=True,
                    nonmonogenic=True, nonreduced=True, J=spec['J'], stratum=s,
                    checks='unordered spectral pairs; all strata; exact fourth-power determinant'))

    t = sp.Matrix([[0, 0], [1, 0]])
    spec = specification([t, t*t])
    check_spectra(spec, [[0, 0], [0, 0]])
    s = last_stratum(spec)
    assert s == 0 and determinant(spec, s, U).as_expr() == 1
    out.append(dict(algebra='Q[t]/(t^2)', guard='t', rational_character=False,
                    all_characters_excluded=True, J=spec['J'], stratum=s))

    # A denominator may vanish on excluded characters and at nilpotents.
    t = sp.Matrix([[0,1,0,0], [1,0,0,0], [0,0,0,1], [0,0,1,0]])
    v = sp.Matrix([[0,0,2,2], [0,0,2,2], [1,0,0,0], [0,1,0,0]])
    g = t+sp.eye(4)
    assert t*t == sp.eye(4) and v*v == 2*g and t*v == v*t
    spec = specification([g, g*t, g*v])
    check_spectra(spec, [[2,2,0,0], [2,2,0,0], [4,-4,0,0]])
    s = last_stratum(spec)
    beta, H = element_matrix(spec, s), determinant(spec, s, U)
    lambdas = []
    for sign in (-1, 1):
        character = sp.Matrix([[1, 1, 2*sign, 2*sign]])
        lam = (character*beta[:, 0])[0]
        assert lam != 0 and H.eval(1/lam) == 0
        lambdas.append(lam)
    assert lambdas[0] != lambdas[1]
    assert H == sp.Poly((1-U*lambdas[0])*(1-U*lambdas[1]), U)
    out.append(dict(algebra='Q[t,v]/(t^2-1,v^2-2(t+1))', guard='t+1',
                    permitted_rational_characters=2, excluded_nonreduced_part=True,
                    J=spec['J'], stratum=s, checks='selected-character denominator and exact quadratic determinant'))

    # Polynomial, not merely numerical, divisibility by the diagonal factor.
    a = sp.Symbol('a')
    t = sp.Matrix([[0, a], [1, 0]])
    spec = specification([sp.eye(2), t])
    z = spec['paired_polynomial'].gens[0]
    # There are 3 pair factors per matrix: first z*(z-1)^2;
    # second (z-4a)*(z-a)^2. Their product has degree six.
    expected = z*(z-1)**2*(z-a)**2*(z-4*a)
    assert spec['paired_polynomial'] == sp.Poly(expected, z)
    assert all(sp.Poly(c, a).degree() <= 2*j for j, c in enumerate(spec['coefficients']) if c != 0)
    out.append(dict(algebra='Q[a][t]/(t^2-a)', symbolic=True,
                    checks='exact mandatory diagonal quotient; even-power substitution; coefficient degree bounds'))
    return out


def independent_bound(n, ell, d):
    J = ell * (n*(n+1)//2)
    delta_degree = 4*J*d
    spectral_envelope_degree = 2*d
    K_degree = delta_degree+(J-1)*spectral_envelope_degree
    C_degree = max(delta_degree, K_degree+spectral_envelope_degree)
    matrix_degree = max(delta_degree+(i+1)*C_degree+(ell-1-i)*delta_degree+d
                        for i in range(ell))
    factor_degree = max(2*n*(1+matrix_degree), 4*J*d)
    D = (J+1)*factor_degree
    assert D == degree_bound(n, ell, d)
    return J, D


def ledgers():
    result = {}
    eta = 15616+233856*4+(233952*4+467712*16)*9**59
    wrapper_path = ROOT/'undecidability/certificates/finite_wrapper_transfer.json'
    wrapper = json.loads(wrapper_path.read_text())
    assert int(wrapper['source_degree_bound_delta']) == eta
    common = json.loads((ROOT/'undecidability/certificates/common_numerator_transfers.json').read_text())
    for family in ('finite_wrapper', 'common_numerator', 'shared_integer'):
        source = ROOT/f'undecidability/certificates/{family}_transfers.json'
        if family == 'finite_wrapper':
            source, data = wrapper_path, wrapper
        else:
            data = json.loads(source.read_text())
        rows = {}
        for route, record in data['routes'].items():
            n = int(record['finite_algebra_rank'])
            if family == 'finite_wrapper':
                ell = record['guarded_separator_count']
                d = int(record['gamma_multiplication_degree_upper_bound'])
                N = record['rational_variables']
                old = record['final_degree_strictly_less_than_power2']
                parent = common['routes'][route]
                assert n == 16*int(parent['finite_algebra_rank'])
                assert ell == parent['gamma_count']+1
                assert d == parent['gamma_multiplication_degree_bound']*(2*eta+1)+eta
                assert record['source_common_numerator_sha256'] == parent['joint_source_sha256']
            else:
                ell, d = record['gamma_count'], record['gamma_multiplication_degree_bound']
                N = record['variables']
                old = record['mixed_transfer_degree_strictly_less_than_power2']
                folder = ('common_numerator_sources' if family == 'common_numerator'
                          else 'joint_sources')
                filename = ('common_source.json.gz' if family == 'common_numerator'
                            else 'joint_source.json.gz')
                blob = gzip.decompress((ROOT/'undecidability'/folder/route/filename).read_bytes())
                assert hashlib.sha256(blob).hexdigest() == record['joint_source_sha256']
                replay = operator_degree_ledger(json.loads(blob))
                for key in ('finite_algebra_rank', 'gamma_count', 'gamma_multiplication_degree_bound'):
                    assert replay[key] == record[key]
            J, D = independent_bound(n, ell, d)
            final = D if family == 'finite_wrapper' else max(4*D, 2*eta)
            rows[route] = dict(variables=N, algebra_rank=str(n), gamma_count=ell,
                gamma_matrix_degree_bound=str(d), paired_difference_degree=str(J),
                encoder_degree_bound=str(D), final_degree_bound=str(final),
                old_degree_strict_power2=old, final_degree_strict_power2=final.bit_length(),
                source_degree_floor_applied=(family != 'finite_wrapper' and final == 2*eta),
                ordinary_rational_abc_required=(route == 'abc11'),
                retained_source_arithmetic_premises=True)
        result[family] = dict(source=str(source.relative_to(ROOT)), source_sha256=digest(source), routes=rows)
    # Pin and preserve the superior specialized single-input encoders.
    source = ROOT/'data/results_20261123_v88.json'
    old_single = json.loads(source.read_text())['route_bounds']
    route_names = ('general25','explicit27','ordinary_abc11','weak_abc11','strong_weak_abc11')
    assert set(route_names) == set(old_single)
    old_bounds = [old_single[r]['degree_upper_bound'] for r in route_names]
    assert old_bounds == [48318382080,183368679424,3261569,16460929,9808001]
    # Even d=1 already gives a larger generic bound for these ranks.
    # A nonconstant actual matrix system necessarily has d>=1 and ell>=1.
    generic_lower_envelopes = [degree_bound(old_single[r]['rank'],1,1) for r in route_names]
    assert all(a > b for a,b in zip(generic_lower_envelopes,old_bounds))
    result['single_input_scope'] = dict(source=str(source.relative_to(ROOT)), source_sha256=digest(source),
        route_names=list(route_names), variables=[old_single[r]['variables'] for r in route_names],
        specialized_degree_bounds=old_bounds,
        generic_degree_formula_even_at_d1_ell1=[str(D) for D in generic_lower_envelopes],
        change='None. The universal encoder does not replace their stronger specialized source encoders.')
    return result


def verify():
    examples = check_examples()
    records = ledgers()
    assert [records['finite_wrapper']['routes'][r]['final_degree_strict_power2']
            for r in ('general25','explicit27','abc11')] == [532,578,425]
    assert [records['common_numerator']['routes'][r]['final_degree_strict_power2']
            for r in ('general25','explicit27','abc11')] == [302,349,212]
    return dict(status='PASS', schema='paired-spectral-encoder/v1',
        coefficient_recipe='paired_spectral.py and ../papers/paired_spectral_encoder.tex',
        degree_formula='2*n*(J+1)*(1+d*(1+(4+6*ell)*J)), J=ell*n*(n+1)/2',
        finite_examples=examples, degree_ledgers=records,
        scope='Exact small-algebra identities, coefficient-stratum checks, pinned source-DAG degree replay and numerical ledgers. General equivalence is proved in the manuscript; source arithmetic is retained and no variable reduction is claimed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    output = json.dumps(verify(), indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output)
    print(output, end='')
