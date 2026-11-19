"""Independent exact checks for the ancillary eleven-variable audit.

No attachment checker is imported. The Hasse descent enumerates all primitive
pairs, not the attachment's two projective charts. The rank certificate uses
a different unit mesh, a shorter cutoff, Machin's exact arctangent bound for
pi, and direct Legendre-symbol point counts. Its analytic input is the
standard sign-minus L-derivative formula, not a numerical rank heuristic.
"""
from fractions import Fraction as Q
from itertools import product
import json
from math import isqrt, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent


def diagonal_descent():
    support = (2, 3, 7, 17, 59)
    classes = sorted({sign*prod(p for p, bit in zip(support, bits) if bit)
                      for sign in (-1, 1) for bits in product((0, 1), repeat=5)})
    remaining = [(k, 7*k if k % 7 else k//7) for k in classes]
    assert len(remaining) == 64
    output = []
    for p, e, count in [(2, 8, 32), (3, 3, 16), (7, 2, 4), (41, 1, 0)]:
        m = p**e
        squares = {y*y % m for y in range(m)}
        # Full enumeration is intentionally independent of chart reduction.
        values = set()
        primitive_count = 0
        for a in range(m):
            for b in range(m):
                if a % p == b % p == 0:
                    continue
                primitive_count += 1
                r, s = a*a, b*b
                plus = 83521*r*r - 18785*r*s + 19824*s*s
                minus = 83521*r*r + 83521*r*s - 19824*s*s
                values.add((plus % m, minus % m))
        assert primitive_count == m*m - (m//p)**2
        remaining = [(k, j) for k, j in remaining if any(
            k*u % m in squares and j*v % m in squares for u, v in values)]
        assert len(remaining) == count
        output.append({'modulus': m, 'primitive_pairs_checked': primitive_count,
                       'surviving_classes': remaining})
    assert output[-2]['surviving_classes'] == [(-826, -118), (-413, -59), (7, 1), (14, 2)]
    return output


def finite_local_fibers():
    import sympy as sp
    D, x, h = sp.symbols('D x h')
    f = sp.expand(D*((D+x*x)**2*x**4 - (D-x*x)**2*h*h))
    df = sp.diff(f, x)
    witnesses = []
    for p in (5, 13, 17, 29):
        residues = {y*y % p: y for y in range(p)}
        for d in range(1, p):
            if pow(d, (p-1)//2, p) != p-1:
                continue
            for h0 in (1-d, -d):
                fp = sp.Poly(f.subs({D:d, h:h0}), x)
                dfp = sp.Poly(df.subs({D:d, h:h0}), x)
                found = []
                for x0 in range(p):
                    value = int(fp.eval(x0)) % p
                    if value in residues and (value or int(dfp.eval(x0)) % p):
                        found.append((x0, residues[value]))
                assert found
                witnesses.append({'p':p, 'D':d, 'h':h0 % p, 'point':found[0]})
    assert len(witnesses) == 60
    return witnesses


def atanh_pi_bounds():
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239).
    def atan_interval(x, terms):
        partial = sum(((-1)**j*x**(2*j+1)/Q(2*j+1)
                       for j in range(terms)), Q(0))
        next_term = (-1)**terms*x**(2*terms+1)/Q(2*terms+1)
        return min(partial, partial+next_term), max(partial, partial+next_term)
    a, b = atan_interval(Q(1,5), 18)
    c, d = atan_interval(Q(1,239), 6)
    return 16*a-4*d, 16*b-4*c


def ceil_div(a, b):
    return -((-a)//b)


def rank_one_derivative():
    N, cutoff, scale = 791, 7000, 10**30
    pi_lo, pi_hi = atanh_pi_bounds()
    rt_scale = 10**20
    root_floor = isqrt(2*rt_scale**2)
    c_lo = pi_lo*rt_scale/(2*N*(root_floor+1))
    c_hi = pi_hi*rt_scale/(2*N*root_floor)
    assert 0 < c_lo < c_hi < 1
    def exp_polynomial(t, degree):
        a = Q(1); answer = a
        for j in range(1, degree+1):
            a *= -t/j
            answer += a
        return answer
    exp_lo = exp_polynomial(c_hi, 7)
    exp_hi = exp_polynomial(c_lo, 6)
    qlo = (scale*exp_lo).numerator // (scale*exp_lo).denominator
    qhi = ceil_div((scale*exp_hi).numerator, (scale*exp_hi).denominator)
    assert 0 < qlo < qhi < scale
    powers_lo = [scale]; powers_hi = [scale]
    for n in range(1, cutoff+2):
        powers_lo.append(powers_lo[-1]*qlo//scale)
        powers_hi.append(ceil_div(powers_hi[-1]*qhi, scale))
    # Bounds for E1(c*n)=integral_n^infinity exp(-c*t)/t dt.
    # Unit-mesh left and right endpoint sums bound this decreasing integrand.
    lower = [0]*(cutoff+1)
    upper = [0]*(cutoff+1)
    tail_mesh = ceil_div(powers_hi[cutoff+1]*scale,
                         (cutoff+1)*(scale-qhi))
    lo_sum, hi_sum = 0, tail_mesh
    for n in reversed(range(1, cutoff+1)):
        lower[n] = lo_sum
        hi_sum += ceil_div(powers_hi[n], n)
        upper[n] = hi_sum
        lo_sum += powers_lo[n]//n
    smallest = list(range(cutoff+1))
    for p in range(2, isqrt(cutoff)+1):
        if smallest[p] == p:
            for n in range(p*p, cutoff+1, p):
                if smallest[n] == n:
                    smallest[n] = p
    coefficients_prime = {}
    for p in range(2, cutoff+1):
        if smallest[p] != p:
            continue
        if 2*N % p == 0:
            coefficients_prime[p] = 0
            continue
        # Direct point count by Euler's criterion, with no CM p mod 4 shortcut.
        count = 1
        for x in range(p):
            f = (x*x*x-N*N*x) % p
            count += 1 if f == 0 else 2 if pow(f, (p-1)//2, p) == 1 else 0
        coefficients_prime[p] = p+1-count
    coefficients = [0]*(cutoff+1)
    coefficients[1] = 1
    for n in range(2, cutoff+1):
        remaining, value = n, 1
        while remaining > 1:
            p = smallest[remaining]
            exponent = 0
            while remaining % p == 0:
                remaining //= p
                exponent += 1
            if 2*N % p == 0:
                value = 0
                break
            previous, current = 1, coefficients_prime[p]
            for e in range(2, exponent+1):
                previous, current = current, coefficients_prime[p]*current-p*previous
            value *= current
        coefficients[n] = value
        assert abs(value) <= 2*n
    lower_scaled, upper_scaled = 0, 0
    for n in range(1, cutoff+1):
        a = 2*coefficients[n]
        lo, hi = (lower[n], upper[n]) if a >= 0 else (upper[n], lower[n])
        lower_scaled += a*lo//n
        upper_scaled += ceil_div(a*hi, n)
    # Absolute omitted L' tail: |a_n|<=2n and E1(cn)<=exp(-cn)/(cn).
    tail = 4*Q(powers_hi[cutoff+1])*scale/(c_lo*(cutoff+1)*(scale-qhi))
    tail_scaled = ceil_div(tail.numerator, tail.denominator)
    lower_scaled -= tail_scaled
    upper_scaled += tail_scaled
    assert lower_scaled > 0
    assert Q(6) < Q(lower_scaled,scale) < Q(upper_scaled,scale) < Q(10)
    G = (-784, -2940)
    assert G[1]**2 == G[0]**3-N*N*G[0]
    assert N == 7*113 and N % 8 == 7
    assert coefficients_prime[3] == 0 and coefficients_prime[19] == 0
    assert 3+1-coefficients_prime[3] == 4
    assert 19+1-coefficients_prime[19] == 20
    return {'curve': [0,0,0,-N*N,0], 'conductor':32*N*N,
            'root_number':-1, 'cutoff':cutoff, 'mesh':1,
            'scale':scale, 'lower_scaled':lower_scaled,
            'upper_scaled':upper_scaled, 'explicit_point':G,
            'logical_conclusion':'analytic rank 1; algebraic rank 1 by Gross-Zagier-Kolyvagin'}


def normalization_and_trace_identities():
    import sympy as sp
    d, t, v, s, x, D = sp.symbols('d t v s x D')
    eta = d*t*t
    old = eta*((eta+(t*v)**2)**2*s**4-(eta-(t*v)**2)**2*(1-eta)**2)
    new = d*((d+v*v)**2*s**4-(d-v*v)**2*(1-eta)**2)
    assert sp.expand(old-t**6*new) == 0
    x2 = (x*x+D)**2/(4*x*(x*x-D))
    assert sp.cancel(4*x2-x-D*(3*x*x+D)/(x*(x*x-D))) == 0
    return {'intrinsic_rescaling':'eta=d*t^2; old_v=t*v; old_Y=t^3*Y',
            'duplication_difference':'4*x(2Q)-x(Q)=D*(3*x(Q)^2+D)/(x(Q)*(x(Q)^2-D))'}


if __name__ == '__main__':
    result = {'diagonal_hasse_descent':diagonal_descent(),
              'finite_local_fiber_witnesses':finite_local_fibers(),
              'rank791':rank_one_derivative(),
              'identities':normalization_and_trace_identities()}
    target = HERE/'ancillary_independent_certificate.json'
    target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('Full primitive-pair descent:', [len(row['surviving_classes']) for row in result['diagonal_hasse_descent']])
    print('Smooth finite-field witnesses:', len(result['finite_local_fiber_witnesses']))
    print('Independent unit-mesh derivative interval:', result['rank791'])
    print('Exact pole normalization and duplication identities passed')
