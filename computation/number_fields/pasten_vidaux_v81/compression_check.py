#!/usr/bin/env python3
"""Read-only independent finite checks for the ten-coordinate field selector.

No producer or other project checker is imported.  Exact SymPy arithmetic checks
source clearing identities, a complete rank-64 split algebra, and a rank-4
nonsplit triangular intrinsic-pole specialization.  These finite fixtures do not
expand or evaluate the full defining polynomial or prove its arithmetic inputs.
The default command compares compression_certificate.json without writing files;
--report PATH explicitly writes a newly computed certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from math import comb, factorial, isqrt, prod
from pathlib import Path

import sympy as sp


def coefficient_strings(poly: sp.Poly) -> list[str]:
    return [str(c) for c in poly.all_coeffs()]


def digest_integer(value: int) -> str:
    return hashlib.sha256(str(int(value)).encode()).hexdigest()


def source_clearing() -> dict:
    t, lam, ell, beta, emm, mu, a, c, v, s = sp.symbols(
        't Lambda L Beta M mu A C v s')
    p, q = t**3 - 2, t**3 - 3
    g, lr, br = p / q, lam / ell, beta / emm
    a1 = (lam*q - p*ell)**2 * (p+q)**2
    b1 = ell**2 * q * p**3
    a2 = (beta-t*emm)**2 * (ell+lam)**6 * lam
    # Lambda^2 is scalar in the point algebra, so Lambda^4=S^2.
    b2 = emm**2 * ell**3 * lam**4
    assert sp.cancel(a1 / b1 - (lr-g)**2*(1+g)**2/g**3) == 0
    assert sp.cancel(a2 / b2 - (br-t)**2*((1+lr)**2/lr)**3) == 0

    d = a / c
    intrinsic = d*(d+v*v)**2*s**4 - d*(d-v*v)**2*(1-d)**2
    cleared = a*c**3*(a+c*v*v)**2*s**4 - a*c*(a-c*v*v)**2*(c-a)**2
    assert sp.cancel(c**6*intrinsic-cleared) == 0
    assert sp.expand(cleared).subs(c, 0) == 0

    # Check the rationalized quotient of the odd elliptic map y U(x)/V(x).
    y1, y2, f1, f2, u1, u2, v1, v2 = sp.symbols('y1 y2 F1 F2 U1 U2 V1 V2')
    numerator = y1*y2*u1*v2
    denominator = f2*u2*v1
    difference = sp.together(numerator/denominator-(y1*u1/v1)/(y2*u2/v2))
    difference_num = sp.fraction(difference)[0]
    assert sp.rem(sp.Poly(difference_num, y2), sp.Poly(y2**2-f2, y2)).is_zero
    square = sp.rem(sp.Poly(numerator**2, y1), sp.Poly(y1**2-f1, y1)).as_expr()
    square = sp.rem(sp.Poly(square, y2), sp.Poly(y2**2-f2, y2)).as_expr()
    assert sp.expand(square-f1*f2*u1**2*v2**2) == 0
    return {
        'elliptic_ratio_rationalization': 'Lambda/L, Lambda=y1*y2*U1*V2, L=F2*U2*V1',
        'Lambda_square_scalar': 'F1*F2*U1^2*V2^2',
        'first_input_A1_over_B1_verified': True,
        'second_input_A2_over_B2_verified': True,
        'terminal_monic_clearing_verified': 'R=C^6*P_(A/C)(v,s); z=C^3*Y',
        'terminal_cleared_polynomial_total_degree': sp.Poly(cleared, a,c,v,s).total_degree(),
        'terminal_cleared_polynomial_terms': len(sp.Poly(cleared, a,c,v,s).terms()),
        'clearing_requires_nonzero_C': True,
        'C_zero_cleared_radicand_is_zero': True,
    }


def binary_generator_matrices(count: int, squares: list[int]) -> list[sp.Matrix]:
    rank = 1 << count
    result = []
    for i, square in enumerate(squares):
        matrix = sp.zeros(rank)
        for column in range(rank):
            matrix[column ^ (1 << i), column] = square if column & (1 << i) else 1
        result.append(matrix)
    return result


def power_basis(matrix: sp.Matrix) -> sp.Matrix:
    column = sp.eye(matrix.rows)[:, 0]
    columns = []
    for _ in range(matrix.rows):
        columns.append(column)
        column = matrix * column
    return sp.Matrix.hstack(*columns)


def rank64_split_fixture() -> dict:
    # The algebra Q[r1,...,r6]/(ri^2-1) has all 64 independent sign characters.
    # It is an exact algebra fixture, not a claim about an actual elliptic tuple.
    rank = 64
    generators = binary_generator_matrices(6, [1]*6)
    identity = sp.eye(rank)
    for i, matrix in enumerate(generators):
        assert matrix*matrix == identity
        for earlier in generators[:i]:
            assert matrix*earlier == earlier*matrix

    good_j = 2
    good = sum((good_j**i*matrix for i,matrix in enumerate(generators)), sp.zeros(rank))
    values = [63-2*mask for mask in range(rank)]
    evaluation = sp.Matrix([
        [(-1)**((character & monomial).bit_count()) for monomial in range(rank)]
        for character in range(rank)
    ])
    assert evaluation*evaluation == rank*identity
    assert evaluation*good == sp.diag(*values)*evaluation

    z = sp.symbols('Z')
    characteristic = sp.Poly(good.charpoly(z).as_expr(), z)
    independently_factored = sp.Poly(sp.prod(z-value for value in values), z)
    assert characteristic == independently_factored
    basis = power_basis(good)
    delta = int(basis.det(method='domain-ge'))
    # det(Vandermonde)/det(Hadamard): 2^(2016-192)*product(k!,1<=k<=63).
    independent_delta = 2**1824 * prod(factorial(k) for k in range(1,64))
    assert delta == independent_delta != 0

    bad = sum(generators, sp.zeros(rank))  # j=1, also in the finite selector menu
    bad_basis = power_basis(bad)
    assert bad_basis.rank() == 7
    assert bad_basis.det(method='domain-ge') == 0

    # Actual 64x64 determinant, with nonzero guard value G=3 and Z=2/3.
    # This sample distinguishes -I from the wrong +I convention.
    guard = sp.Integer(3)
    sample = sp.Rational(2,3)
    sample_matrix = guard*(sample*identity-good)-identity
    sample_det = int(sample_matrix.det(method='domain-ge'))
    expected_det = prod(int(guard*(sample-value)-1) for value in values)
    assert sample_det == expected_det != 0
    assert (guard*(sample*identity-good)+identity).det(method='domain-ge') == 0

    root = sp.Rational(values[0]) + 1/guard
    assert (guard*(root*identity-good)-identity).det(method='domain-ge') == 0
    # A zero primitive eigenvalue must be permitted by the shifted encoder.
    zero_eigenvalue = good-values[0]*identity
    assert power_basis(zero_eigenvalue).det(method='domain-ge') == delta
    assert (guard*((1/guard)*identity-zero_eigenvalue)-identity).det(method='domain-ge') == 0
    wrong_reciprocal = int((zero_eigenvalue-identity).det(method='domain-ge'))
    assert wrong_reciprocal == prod(2*k+1 for k in range(64)) != 0

    # Both a failed source guard and a failed primitive determinant force G=0.
    assert (-identity).det(method='domain-ge') == 1
    return {
        'algebra': 'Q[r1,...,r6]/(r1^2-1,...,r6^2-1)',
        'rank': rank,
        'all_generator_relations_and_commutators_verified': True,
        'all_64_sign_characters_verified_by_evaluation_matrix': True,
        'primitive_menu_index': good_j,
        'primitive_eigenvalues': values,
        'characteristic_coefficients_descending': coefficient_strings(characteristic),
        'power_basis_determinant': '2^1824 * product(k!, k=1,...,63)',
        'power_basis_determinant_bits': delta.bit_length(),
        'power_basis_determinant_decimal_sha256': digest_integer(delta),
        'bad_menu_index': 1,
        'bad_power_basis_rank': 7,
        'bad_power_basis_determinant': 0,
        'shifted_encoder_exact_nonroot_determinant_sha256': digest_integer(sample_det),
        'shifted_encoder_exact_root': str(root),
        'zero_primitive_eigenvalue_encoder_root': '1/3',
        'wrong_reciprocal_encoder_nonzero_determinant': 'product(2*k+1, k=0,...,63)',
        'wrong_plus_I_encoder_detected': True,
        'zero_combined_guard_determinant': 1,
        'fixture_scope': 'Exact rank-64 algebra and encoder checks, not an arithmetic source witness.',
    }


def triangular_nonsplit_fixture() -> dict:
    # Retain one initial quadratic root r^2=2, and use an actual cleared
    # intrinsic-pole radicand at A=1+r,C=3,v=s=1.
    r, z, guard = sp.symbols('r Z G')
    a, c = 1+r, sp.Integer(3)
    cleared = a*c**3*(a+c)**2-a*c*(a-c)**2*(c-a)**2
    reduced = sp.rem(sp.Poly(cleared,r), sp.Poly(r*r-2,r)).as_expr()
    assert reduced == 1002+642*r
    norm = 1002**2-2*642**2
    assert norm == 179676 and isqrt(norm)**2 != norm

    mr = sp.Matrix([[0,2,0,0],[1,0,0,0],[0,0,0,2],[0,0,1,0]])
    mq = sp.Matrix([[0,0,1002,1284],[0,0,642,1002],[1,0,0,0],[0,1,0,0]])
    identity = sp.eye(4)
    assert mr*mr == 2*identity
    assert mq*mq == 1002*identity+642*mr
    assert mr*mq == mq*mr
    dmatrix = (identity+mr)/3
    ymatrix = mq/27
    intrinsic_matrix = dmatrix*(dmatrix+identity)**2-dmatrix*(dmatrix-identity)**2*(identity-dmatrix)**2
    assert ymatrix*ymatrix == intrinsic_matrix

    alpha = mr+mq
    basis = power_basis(alpha)
    delta = int(basis.det())
    assert delta == -408164
    characteristic = sp.Poly(alpha.charpoly(z).as_expr(),z)
    assert characteristic.as_expr() == z**4-2008*z**2-5136*z+175672
    assert characteristic.is_irreducible
    inverse = basis.inv()
    rpoly = sp.Poly(sum(inverse[i,1]*z**i for i in range(4)),z)
    qpoly = sp.Poly(sum(inverse[i,2]*z**i for i in range(4)),z)
    assert sp.rem(rpoly*rpoly-2,characteristic).is_zero
    assert sp.rem(qpoly*qpoly-(1002+642*rpoly),characteristic).is_zero
    assert sp.rem(rpoly+qpoly-sp.Poly(z,z),characteristic).is_zero
    # Thus every root of characteristic in any characteristic-zero field
    # reconstructs an actual character of the triangular algebra.
    encoded = sp.expand((guard*(z*identity-alpha)-identity).det())
    expected = sp.expand(guard**4*characteristic.as_expr().subs(z,z-1/guard))
    assert sp.cancel(encoded-expected) == 0
    assert encoded.subs(guard,0) == 1
    assert sp.Poly(encoded,z).LC() == guard**4

    # A root of the unguarded characteristic polynomial is insufficient
    # without a primitive element: r alone sees only Q(sqrt(2)).
    nonprimitive = power_basis(mr)
    assert nonprimitive.rank()==2 and nonprimitive.det()==0
    assert sp.Poly(mr.charpoly(z).as_expr(),z) == sp.Poly((z*z-2)**2,z)
    return {
        'algebra': 'Q[r,q]/(r^2-2,q^2-(1002+642*r))',
        'basis': ['1','r','q','r*q'],
        'intrinsic_specialization': {'A':'1+r','C':3,'v':1,'s':1,'Y':'q/27'},
        'radicand_norm_to_Q': norm,
        'radicand_norm_is_not_a_square': True,
        'normalized_intrinsic_equation_verified_in_algebra': True,
        'primitive_element': 'r+q',
        'primitive_determinant': delta,
        'irreducible_characteristic_coefficients_descending': coefficient_strings(characteristic),
        'recovered_r_coefficients_descending': coefficient_strings(rpoly),
        'recovered_q_coefficients_descending': coefficient_strings(qpoly),
        'all_reconstructed_source_relations_verified_mod_characteristic': True,
        'shifted_encoder_identity': 'det(G*(Z*I-M_alpha)-I)=G^4*f(Z-1/G)',
        'zero_guard_value': 1,
        'nonprimitive_example': {
            'element':'r','power_basis_rank':2,'power_basis_determinant':0,
            'characteristic':'(Z^2-2)^2',
            'obstruction':'It has a root in Q(sqrt(2)), but the full algebra has no character there because the q-radicand has nonsquare norm.'
        },
    }


def report() -> dict:
    rank, generators = 64, 6
    pair_count = comb(rank,2)
    bad_bound = (generators-1)*pair_count
    menu_size = bad_bound+1
    assert pair_count == 2016 and bad_bound == 10080 and menu_size == 10081
    assert 1+4+2*2+1 == 10 and 2**generators == rank
    result = {
        'schema':'pasten-vidaux-v81-compression-v1',
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'arithmetic':'Exact integer and rational SymPy arithmetic; no producer imports.',
        'source_clearing':source_clearing(),
        'separator_census':{
            'initial_point_roots':4,'terminal_pole_roots':2,'algebra_rank':rank,
            'maximum_pair_difference_degree':5,'unordered_character_pairs':pair_count,
            'maximum_bad_integer_separator_indices':bad_bound,
            'separator_menu':'j=1,...,10081','separator_menu_size':menu_size,
            'multiplier_pairs':16**2,'determinant_factors_in_complete_product':16**2*menu_size,
            'coordinates':{'input':1,'elliptic_abscissas':4,'pole_parameters':4,'encoder':1,'total':10},
        },
        'rank64_split_fixture':rank64_split_fixture(),
        'triangular_nonsplit_fixture':triangular_nonsplit_fixture(),
        'universal_proof_obligations_reviewed_separately':[
            'The six monic quadratic equations give a free rank-64 algebra over the nine-coordinate base.',
            'Nonzero source guards make the algebra etale, and the pair-collision degree bound gives a primitive separator in the finite menu.',
            'A nonzero power-basis determinant identifies the algebra with K[T]/(its characteristic polynomial), so each K-root gives an actual K-character.',
            'At a zero combined guard each determinant factor is det(-I_64)=1; otherwise the root is alpha=Z-1/G.',
            'For every prime, either G vanishes identically modulo that prime and the factor is 1, or its leading Z^64 coefficient G^64 is nonzero; hence primitive integer content.',
        ],
        'not_computationally_certified':[
            'The complete high-degree product, its expanded coefficients, degree or coefficient height.',
            'An actual elliptic/pole arithmetic source witness for the rank-64 split fixture.',
            'The stable-positive-rank hypothesis, Burungale theorem, all-place approximation or prepared pole-density theorem.',
            'The global rationality-descent proof or an effective finite-exception correction.',
            'Any reduction below eleven coordinates for defining Z over Q.',
        ],
    }
    return json.loads(json.dumps(result,sort_keys=True))


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,help='explicitly write a newly computed certificate')
    args=parser.parse_args()
    result=report()
    serialized=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.report:
        args.report.write_text(serialized)
    else:
        path=Path(__file__).with_name('compression_certificate.json')
        assert path.exists(), 'compression certificate is missing'
        assert json.loads(path.read_text())==result, 'compression certificate differs'
    print('PASS: scalar clearing, rank-64 separator and guarded encoder, triangular nonsplit reconstruction, and 10-coordinate census')
    print('Full polynomial expansion and arithmetic/global existence claims remain outside this finite checker.')


if __name__=='__main__':
    main()
