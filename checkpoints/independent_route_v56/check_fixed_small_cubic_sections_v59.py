#!/usr/bin/env python3
"""Check nodal specialization and contact obstructions using stdlib only."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def add(R, S):
    if R is None:
        return S
    if S is None:
        return R
    x, y = R
    u, v = S
    if x == u and y == -v:
        return None
    slope = ((3*x*x-8*x+4)/(2*y) if R == S
             else (v-y)/(u-x))
    z = slope*slope+4-x-u
    return (z, -y+slope*(x-z))


def factors(n):
    n = abs(n)
    assert n != 0
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


P = (F(4), F(4))
T = (F(0), F(0))
R = None
a, b = 1, 0
rows = []
for m in range(1, 65):
    a, b = 3*a+4*b, 2*a+3*b
    R = add(R, P)
    assert a*a-2*b*b == 1
    expected = (F(2*(a+1), a-1), F(8*b, (a-1)**2))
    assert R == expected
    x, y = R
    assert y*y == x*(x-2)**2
    v = x-2
    vt = add(R, T)[0]-2
    assert v == F(4, a-1)
    assert vt == -F(4, a+1)
    assert vt < 0
    if m >= 2:
        assert 0 < v <= F(1, 4)
        assert v != 1 and v != 2
    if m <= 8:
        row = {"m": m, "a_m": a, "b_m": b,
               "V_m_at_0": str(v), "V_m_plus_T_at_0": str(vt)}
        if m >= 2:
            row["untranslated_exceptional_primes"] = sorted(set(
                factors(2)+factors(a-1)+factors(a-3)+factors(a-5)))
        row["translated_exceptional_primes"] = sorted(set(
            factors(2)+factors(a+1)+factors(a+3)+factors(a+5)))
        rows.append(row)

finite_field_cases = 0
for p in (73, 97, 193, 241, 313, 337):
    roots2 = [u for u in range(p) if u*u % p == 2]
    roots3 = [u for u in range(p) if u*u % p == 3]
    assert roots2 and roots3
    for s2 in roots2:
        for s3 in roots3:
            r = (3+2*s2) % p
            s6 = s2*s3 % p
            for m in range(1, p):
                rm = pow(r, m, p)
                if rm == 1:
                    continue
                v = 8*rm*pow((rm-1)**2, -1, p) % p
                assert (v == 2) == (rm in (r, pow(r, -1, p)))
                assert (v == 1) == (rm in ((5+2*s6) % p, (5-2*s6) % p))
                finite_field_cases += 1

certificate = {
    "status": "PASS",
    "arithmetic": "standard-library exact rational arithmetic",
    "direct_nodal_group_law_multiples_checked": 64,
    "finite_field_contact_equivalences_checked": finite_field_cases,
    "first_multiples": rows,
    "scope": {
        "fixed_finite_section_menus_excluded_in_prepared_large_slope_tail": True,
        "fixed_finite_section_menus_excluded_outside_finite_contact_primes": True,
        "varying_indices_excluded": False,
        "individual_rational_witnesses_excluded": False,
        "all_rational_sections_classified": False,
        "new_defining_variable_bound_proved": False,
    },
}
(HERE / "fixed_small_cubic_sections_v59_certificate.json").write_text(
    json.dumps(certificate, indent=2)+"\n")
print(json.dumps(certificate, indent=2))
