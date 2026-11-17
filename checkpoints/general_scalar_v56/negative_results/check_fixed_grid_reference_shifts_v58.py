#!/usr/bin/env python3
"""Exact coefficient classification for fixed reference shifts in the grid."""
from pathlib import Path
import json
import sympy as S

n, s, t, b, h, u = S.symbols('n s t b h u')
indices = [S.Integer(1), n, s, t, b, h, n*h, s*h, t*h, b*h]
alpha = S.symbols('alpha0:10')
beta = S.symbols('beta0:10')
m = sum(a*i for a, i in zip(alpha, indices))
mp = sum(a*i for a, i in zip(beta, indices))
equations = S.Poly(n*m-mp, n, s, t, b, h).coeffs()
matrix, rhs = S.linear_eq_to_matrix(equations, alpha+beta)
assert rhs == S.zeros(rhs.rows, 1)
assert matrix.rank() == 18
assert len(matrix.nullspace()) == 2
solution = list(S.linsolve((matrix, rhs), alpha+beta))[0]
free = S.symbols('a c')
substitution = dict(zip(alpha+beta, solution))
mm = S.expand(m.subs(substitution))
mmp = S.expand(mp.subs(substitution))
assert S.expand(mmp-n*mm) == 0
assert S.Poly(mm, n, s, t, b, h).monoms() == [
    (0, 0, 0, 0, 1), (0, 0, 0, 0, 0)]
assert set(mm.free_symbols)-{h} == {beta[1], beta[6]}
assert mm == beta[1]+beta[6]*h
assert mmp == beta[1]*n+beta[6]*n*h

a, bb, c, d = S.symbols('a bb c d')
H1, H2 = a+bb*h, c+d*h
U1, U2 = a*n+bb*u, c*n+d*u
assert S.expand(U1*H2-U2*H1-(a*d-bb*c)*(n*h-u)) == 0
assert S.expand(d*H1-bb*H2-(a*d-bb*c)) == 0
mm = S.symbols('m')
assert S.expand(u*(h-mm)-h*(u-mm*n)-mm*(n*h-u)) == 0

report = {
    'status': 'PASS',
    'indices': [str(i) for i in indices],
    'coefficient_matrix_rank': matrix.rank(),
    'solution_space_dimension': len(matrix.nullspace()),
    'reference_index': 'a+c*h',
    'paired_reference_index': 'a*n+c*n*h',
    'comparison_determinant_identity_checked': True,
    'fixed_gcd_obstruction_identity_checked': True,
    'adaptive_shift_residual_identity_checked': True,
    'retained_scope': ['fixed integer-linear group operations',
                      'infinitely many inputs',
                      'unbounded Lucas root index per input',
                      'infinitely many auxiliary indices per root tuple'],
    'new_arithmetic_couplings_excluded': False,
    'new_variable_bound_proved': False,
}
out = Path(__file__).with_name('fixed_grid_reference_shifts_v58_certificate.json')
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'coefficient_rank': matrix.rank(),
                  'reference_family_dimension': len(matrix.nullspace())}))
