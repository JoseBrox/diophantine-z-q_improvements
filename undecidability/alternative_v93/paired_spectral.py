#!/usr/bin/env python3
"""One-coordinate guarded-character encoder using squared spectral differences.

This is an exact coefficient recipe. Large source matrices remain specified by
their published multiplication tables and coefficient DAGs; only the small
verification examples are materialized. The general proof is in
../papers/paired_spectral_encoder.tex.
"""
from __future__ import annotations

import sympy as sp


def degree_bound(n, ell, d):
    """Uniform total-degree upper bound; n is rank, ell is gamma count."""
    assert n >= 1 and ell >= 1 and d >= 0
    J = ell * n * (n + 1) // 2
    return 2 * n * (J + 1) * (1 + d * (1 + (4 + 6 * ell) * J))


def specification(matrices):
    """Matrices must be multiplication by g,g*theta_1,...,g*theta_m."""
    matrices = tuple(sp.Matrix(a) for a in matrices)
    assert matrices
    n = matrices[0].rows
    assert n >= 1 and all(a.shape == (n, n) for a in matrices)
    assert all(a*b == b*a for a in matrices for b in matrices)
    ell, N = len(matrices), n + 1
    J = ell * n * N // 2
    spectral = sp.Dummy('spectral')
    paired = sp.Dummy('paired')
    psi = sp.Poly(1, paired)
    individual = []
    for a in matrices:
        aug = sp.diag(a, sp.zeros(1))
        difference = (sp.kronecker_product(aug, sp.eye(N))
                      - sp.kronecker_product(sp.eye(N), aug))
        char = sp.Poly.from_list(difference.charpoly().all_coeffs(),
                                gens=spectral)
        reduced = {}
        for (exponent,), coefficient in char.terms():
            assert exponent >= N
            assert (exponent-N) % 2 == 0
            reduced[((exponent-N)//2,)] = coefficient
        q = sp.Poly.from_dict(reduced, paired)
        assert q.degree() == n*N//2 and q.LC() == 1
        assert sp.expand(char.as_expr()
                         - spectral**N*q.as_expr().subs(paired, spectral**2)) == 0
        psi *= q
        individual.append(q)
    assert psi.degree() == J and psi.LC() == 1
    coefficients = tuple(psi.all_coeffs())
    # Unlike the old encoder this envelope uses matrix entries only.
    R = sp.expand(2+N+sum(x*x for a in matrices for x in a))
    B = N*R
    return dict(matrices=matrices, n=n, ell=ell, N=N, J=J,
                coefficients=coefficients, paired_polynomial=psi,
                individual_paired_polynomials=individual, R=R, B=B)


def element_matrix(spec, s):
    assert 0 <= s <= spec['J']
    Delta = spec['coefficients'][s]**2
    if Delta == 0:
        return sp.zeros(spec['n'])
    K = (1+Delta)*(2*spec['B'])**(spec['J']-1)
    C = Delta+(4*spec['ell']*spec['B']+2)*K
    matrix = sp.zeros(spec['n'])
    for i, a in enumerate(spec['matrices']):
        matrix += Delta*C**(i+1)*Delta**(spec['ell']-1-i)*a
    return matrix


def determinant(spec, s, U):
    matrix = element_matrix(spec, s)
    return sp.Poly((sp.eye(spec['n'])-U*matrix).det(method='domain-ge'), U)


def factor(spec, s, U):
    return (determinant(spec, s, U).as_expr()**2
            + sum(a*a for a in spec['coefficients'][s+1:]))


def polynomial(spec, U):
    """Unexpanded product specifying every coefficient by integer operations."""
    return sp.Mul(*(factor(spec, s, U) for s in range(spec['J']+1)),
                  evaluate=False)
