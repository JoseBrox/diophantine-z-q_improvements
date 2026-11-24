#!/usr/bin/env python3
"""Exact finite checks for the bounded-odd-depth amplifier.
The checks verify arithmetic margins, not the additional OM hypothesis.
"""
from fractions import Fraction as Q

profiles = 0
for d in range(1, 81):
    s = 6*d-1
    assert s > 0 and s % 2 == (s+2) % 2 == 1
    for a in range(1, d+1, 2):
        low = -3*a
        assert s+2-6*a >= 1
        for w in range(low, low+12):
            for v0, v1 in ((low,w),(w,low)):
                r0,r1 = s*v0,(s+2)*v1
                assert r0 != r1
                nu = min(r0,r1)
                assert nu < 0 and nu % 2 == 1
                assert -nu >= 3*a*s
                assert (-nu)//2+1 > Q(3*a*s,2)
                profiles += 1

orders = 0
for k in range(3, 100):
    for mu in range(1, 128, 2):
        # Integer v satisfying v>(k-3/4)*mu.
        v = (4*k-3)*mu//4+1
        assert v >= k
        assert v >= (k-1)*mu+1
        orders += 1
for eta in map(Q,['1/1000','1/100','1/10','1/2','1','2']):
    k = max(3, 3//eta+1)
    assert Q(7,3*k) < Q(3,k) < eta

print('PASS:', profiles, 'component valuation profiles;', orders,
      'scalar precision inequalities; strict exponent margins.')
