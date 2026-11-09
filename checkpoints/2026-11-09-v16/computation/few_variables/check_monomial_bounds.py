#!/usr/bin/env python3
"""Certify support upper bounds without expanding the determinant polynomials."""
from pathlib import Path
import hashlib
import json
from math import comb

ROOT = Path(__file__).resolve().parent


def support_bound(total_degree, variables, last_variable_degree):
    """Count lattice points |alpha|<=D with alpha[-1]<=E exactly."""
    D, n, E = total_degree, variables, min(total_degree, last_variable_degree)
    return comb(D+n, n) - (comb(D-E+n-1, n) if E < D else 0)


def main():
    # Compare the closed formula with direct enumeration of the last exponent.
    for D in range(15):
        for n in range(1, 7):
            for E in range(D+3):
                assert support_bound(D, n, E) == sum(
                    comb(D-e+n-1, n-1) for e in range(min(D, E)+1))
    entries = []
    for label, folder in (
        ('inherited27', ROOT/'active_elimination/active27'),
        ('explicit29', ROOT/'active_elimination/active29'),
        ('weak_abc13', ROOT/'weak_abc13/active13'),
    ):
        source = folder/'construction-certificate.json'
        c = json.loads(source.read_text())
        n, D = c['total_variables'], c['degree_bound']
        b, rank = c['point_algebra_rank'], c['rank']
        assert c['exact_factor_count'] == b
        assert c['retained_base_variables'] == n-1
        # One determinant factor and b-1 squared determinant factors.
        # Every determinant is rank-by-rank and affine in U.
        E = (2*b-1)*rank
        M = support_bound(D, n, E)
        assert M < 2**M.bit_length()
        entries.append({
            'construction': label,
            'total_variables': n,
            'total_degree_majorant': str(D),
            'last_variable_degree_majorant': str(E),
            'exact_monomial_count': None,
            'exact_count_status': 'not computed; polynomial is not expanded',
            'support_upper_bound': str(M),
            'support_upper_bound_power_of_two_exponent': M.bit_length(),
            'power_of_two_inequality': 'strict',
            'formula': 'binom(D+n,n)-binom(D-E+n-1,n)',
            'uniform_in_fixed_coefficient_parameter': True,
            'source_certificate': str(source.relative_to(ROOT)),
            'source_certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        })
    result = {
        'status': 'PASS',
        'meaning': 'Certified upper bounds on ordinary coordinate monomials, not exact counts.',
        'derivation': (
            'Each H_r=det(I-U M_beta_r) has U-degree at most rank. '
            'The final product has one H_b and b-1 factors H_r^2+tail, '
            'so U-degree is at most (2b-1)*rank. Stars and bars with the '
            'U-exponent truncated gives the displayed exact lattice-point count.'
        ),
        'constructions': entries,
    }
    out = ROOT/'monomial-bound-certificate.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    for entry in entries:
        print(entry['construction']+': monomials < 2^'+str(
            entry['support_upper_bound_power_of_two_exponent'])+'; exact count not computed')


if __name__ == '__main__':
    main()
