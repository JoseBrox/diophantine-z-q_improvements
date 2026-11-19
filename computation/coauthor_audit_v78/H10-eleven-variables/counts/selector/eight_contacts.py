"""Exact eight-contact certificate. Runs with Python's standard library."""
from fractions import Fraction
from itertools import combinations
from math import prod


def polynomial(roots):
    """Ascending coefficients of the product of (X - root)."""
    out = [1]
    for root in roots:
        old, out = out, [0] * (len(out) + 1)
        for i, coefficient in enumerate(old):
            out[i] -= root * coefficient
            out[i+1] += coefficient
    return out


def prime_support(n):
    primes = set()
    p = 2
    while p*p <= n:
        if n % p == 0:
            primes.add(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        primes.add(n)
    return primes


roots_b = [-4, -20, -20, -20, 5, 5]
roots_c = [4, 20, 20, 20, -5, -5]
b, c = map(polynomial, (roots_b, roots_c))
assert [a - z for a, z in zip(b,c)] == [0, 0, 0, 0, 0, 108, 0]
resultant = abs(prod(x-y for x in roots_b for y in roots_c))
assert resultant > 0
source_finite = sorted(set(roots_b+roots_c+[0]))
# If t=r/s=1/(U-21), the inverse sends (r,s) to (21r+s,r).
# The integer 2x2 matrix has determinant -1.
assert 21*0-1*1 == -1
forms = [(1,0)] + [(21-a,1) for a in source_finite]
assert set(forms) == {(1,0), (21,1), (17,1), (25,1), (16,1), (26,1), (1,1), (41,1)}
positions = sorted(Fraction(-y,x) for x,y in forms)
assert len(set(positions)) == 8 and positions[0] == -1 and positions[-1] == 0
determinants = [abs(a*d-b*c) for (a,b),(c,d) in combinations(forms,2)]
assert min(determinants) > 0
bad = prime_support(108*resultant*prod(determinants)*prod(a for a,_ in forms))
print('B ascending coefficients:', b)
print('C ascending coefficients:', c)
print('Difference coefficients:', [x-y for x,y in zip(b,c)])
print('Homogeneous resultant of B,C in absolute value:',resultant)
print('Eight finite contact positions:', ', '.join(map(str, positions)))
print('A sufficient fixed excluded prime set for the contact lemma:', sorted(bad))
