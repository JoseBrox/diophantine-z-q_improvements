#!/usr/bin/env python3
"""Producer-free integer convolution for the alignment threshold."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def multiply(left, right):
    out = [0]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] += a*b
    return out


def main():
    # Coefficients in ascending powers of s. This equality, together
    # with 0<s<1, is the complete positive-factor certificate.
    product = multiply([1, 0, -1], [3, 0, 6, 0, 4, 0, 2])
    target = [3, 0, 3, 0, -2, 0, -2, 0, -2]
    assert product == target
    roots = [Q(2), Q(3, 2), Q(1), Q(4799, 2399), Q(782, 407),
             Q(4), Q(7, 2), Q(3), Q(9597, 2399), Q(1596, 407)]
    assert len(set(roots)) == 10 and min(roots) > 0
    fixtures = []
    for slope, scale in [(Q(7), Q(1, 100)), (Q(10), Q(1, 80)),
                          (Q(100), Q(1, 56))]:
        assert slope > max(roots) and 0 < scale < Q(2, 3)
        # Only the scalar identities are tested; these are not actual
        # elliptic fixtures. The theorem imposes the separate physical
        # root relation rho*T^2=4/lambda.
        ratio = (slope+1)/(slope+6)
        value = Q(1)
        for theta in roots:
            value *= (slope-theta)/(slope+1)
        u0 = scale*value
        u1 = u0*ratio**10
        w0, w1 = u0/(1+u0)**2, u1/(1+u1)**2
        assert w1/w0 == (ratio**5*(1+u0)/(1+u1))**2
        assert (slope+6)**2*u1/((slope+1)**2*u0) == ratio**8 < 1
        normalized = (slope+6)**2*w1/((slope+1)**2*w0)
        assert normalized == (ratio**4*(1+u0)/(1+u1))**2 < 1
        threshold = (1+ratio**2)/(ratio**4*(1+ratio**2+ratio**4))
        assert threshold > Q(2, 3) > u0
        fixtures.append({'lambda': str(slope), 'rho': str(scale),
                         's': str(ratio), 'strict_ratios_verified': True})
    result = {'status': 'PASS', 'method': 'integer convolution and exact Fraction arithmetic',
              'threshold_numerator_coefficients_ascending': product,
              'positive_factor_coefficients_ascending': [3, 0, 6, 0, 4, 0, 2],
              'scalar_fixtures': fixtures, 'fixtures_are_actual_elliptic_witnesses': False,
              'actual_realization_claimed': False,
              'certificate_sha256': sha256((HERE/'certificate.json').read_bytes()).hexdigest()}
    (HERE/'independent_certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
