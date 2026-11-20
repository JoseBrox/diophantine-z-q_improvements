#!/usr/bin/env python3
"""Independent exact reconstruction; no imports from the producer package.

Run with PYTHONPATH=/workspace/scratch/7ac4dd889cf6/math-packages python.
The script only prints its findings; its input files remain unmodified.
"""
from fractions import Fraction as Q
from hashlib import sha256
from importlib.metadata import version
from itertools import product
from math import isqrt, prod
from pathlib import Path
import json

from sage.libs.pari import pari
import sympy as sp

PACKAGE = Path(__file__).resolve().parents[1] / 'package'


def valuation(q, p):
    q = Q(q)
    assert q
    a, b = abs(q.numerator), q.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v


def squareclass(q):
    q = Q(q)
    assert q
    # q and numerator*denominator differ by a rational square.
    n = q.numerator * q.denominator
    return (-1 if n < 0 else 1) * prod(
        int(p) for p, exponent in sp.factorint(abs(n)).items() if exponent % 2
    )


def subgroup(gens):
    return {squareclass(prod(g for g, bit in zip(gens, bits) if bit))
            for bits in product((0, 1), repeat=len(gens))}


def rat(x):
    return Q(str(x))


def main():
    beta, eta = 7 * 17, 5 * 10597
    N = beta * eta
    assert N == 6305215
    assert sp.isprime(17) and sp.isprime(10597)
    assert 213**2 + beta * 8**2 == eta

    # Reconstruct preparation without copying the published fractions.
    t = Q(19, 16)
    u = 17 * t**2
    r = t / (1 + u)
    w = u / (1 + u)**2
    d = beta * r**2
    V = Q(213, 8) * r
    H = V**2 + d
    e = 4*d/V**2
    assert d == 7*w
    assert H == eta*(r/8)**2
    assert d*H == N*(r**2/8)**2
    assert e == beta*Q(16, 213)**2
    assert 0 < w < Q(1, 4) and 0 < V < 2 and 0 < e < 1
    assert isqrt(d.denominator)**2 == d.denominator
    assert isqrt(e.denominator)**2 == e.denominator
    assert squareclass(d) == squareclass(e) == beta
    vals = {name: valuation(q, 2) for name, q in [('u',u),('d',d),('V',V),('e',e)]}
    assert vals == {'u':-8, 'd':8, 'V':1, 'e':8}
    assert valuation(u, 17) == 1
    assert int(sp.legendre_symbol(7,17)) == -1
    assert eta % 8 == 1 and beta % 8 == 7
    assert int(sp.legendre_symbol(eta,7)) == int(sp.legendre_symbol(eta,17)) == 1

    # Reconstruct all three maps algebraically rather than using producer code.
    ds, hs, ss = sp.symbols('d H s', nonzero=True)
    level = ds*hs
    covers = [ds*(ss**4-hs**2),
              ds*(ss**2-hs)*(ss**2-2*hs),
              ds*(ss**2+hs)*(ss**2+2*hs)]
    xs = [ds*ss**2, ds*ss**2-level, ds*ss**2+level]
    for x, cover in zip(xs, covers):
        assert sp.expand(ds**2*ss**2*cover - (x**3-level**2*x)) == 0

    E = pari.ellinit([0,0,0,-N*N,0])
    rank = E.ellrank()
    assert int(rank[0]) == int(rank[1]) == 1
    torsion = E.elltors()
    assert int(torsion[0]) == 4
    assert list(map(int, torsion[1])) == [2,2]
    R = pari([-2450**2, 4729026750])
    assert E.ellisoncurve(R) == 1
    xr, yr = map(rat, R)
    assert xr-N == -35*593**2
    assert xr+N == 35*93**2

    # Group-law reconstruction gives the four torsion classes and their R coset.
    # The resulting eight distinct classes have the full size 2^(rank+2).
    def kummer(P):
        if len(P) == 1:
            return (1,1)
        x = rat(P[0])
        if x == 0:
            return (-1, -N)
        if x == N:
            return (N, 2)
        return (squareclass(x), squareclass(x-N))

    T = [pari([0]), pari([0,0]), pari([N,0]), pari([-N,0])]
    points = T + [E.elladd(R, tp) for tp in T]
    image = {kummer(P) for P in points}
    assert len(image) == 8
    torsion_image = {kummer(P) for P in T}
    assert kummer(R) not in torsion_image
    G = subgroup([-1,2,35,N])
    assert len(G) == 16
    coordinate_classes = set()
    for a,b in image:
        coordinate_classes.update([a,b,squareclass(a*b)])
    for tp in T[1:]:
        xt = rat(tp[0])
        coordinate_classes.update(squareclass(xt+shift) for shift in [-N,0,N] if xt+shift)
    assert coordinate_classes <= G
    assert all(valuation(g,17)%2 == valuation(g,10597)%2 for g in G)
    # Check the WHOLE subgroup supported on {2,3,5,7}, with signs and N powers,
    # not just the sixteen-element menu displayed in the producer certificate.
    kappas = subgroup([-1,2,3,5,7])
    targets = {squareclass(beta*kappa*N**epsilon)
               for kappa in kappas for epsilon in (0,1)}
    assert len(kappas) == 32 and len(targets) == 64
    assert not (targets & G)
    assert all(valuation(g,17)%2 != valuation(g,10597)%2 for g in targets)

    # Independent exact specialization of the same PARI rank algorithm.
    Eisog = pari.ellinit([0,0,0,4*N*N,0])
    iso_rank = Eisog.ellrank()
    assert int(iso_rank[0]) == int(iso_rank[1]) == 1
    Xi, Yi = xr-N*N/xr, yr*(1+N*N/xr**2)
    assert Yi**2 == Xi**3 + 4*N*N*Xi

    # Parametrization used to audit weak approximation on the rational conic.
    # Intersect b=8+m(a-213), other than the base point, with a^2+119b^2=eta.
    m = sp.symbols('m')
    delta = -2*(213+beta*8*m)/(1+beta*m*m)
    aparam = 213+delta
    bparam = 8+m*delta
    assert sp.factor(aparam**2+beta*bparam**2-eta) == 0

    pins = {p.name:sha256(p.read_bytes()).hexdigest()
            for p in sorted(PACKAGE.iterdir()) if p.is_file()}
    print(json.dumps({
        'schema':'independent-genus-one-v82-review-v1',
        'status':'PASS exact reconstruction',
        'source_pins':pins,
        'runtime':{'PARI':str(pari('version()')),'passagemath-pari':version('passagemath-pari')},
        'curve_level':N,'ellrank':str(rank),'isogenous_ellrank':str(iso_rank),
        'torsion':str(torsion),'point':[str(xr),str(yr)],
        'Kummer_image':sorted(image),'coordinate_classes':sorted(coordinate_classes),
        'containing_subgroup':sorted(G),'excluded_target_class_count':len(targets),
        'prepared_tuple':{k:str(v) for k,v in locals().items() if k in ('t','u','r','w','d','V','H','e')},
        'two_adic_valuations':vals,'curve_maps_verified':3,
        'scope':['No producer code was imported or executed.',
                 'Universal local solubility and arbitrary depth are manually reviewed, not inferred from finite tests.',
                 'Rank bounds use PARI algebraic descent. The isogenous result is the same implementation on another curve.',
                 'No actual detector realization or ten-variable definition is established.']
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
