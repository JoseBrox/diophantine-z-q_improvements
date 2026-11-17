#!/usr/bin/env python3
"""Independently authenticate the retained scalar-interface minor and examples."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import sympy as sp


def determinant(matrix, p):
    a = [[int(v) % p for v in row] for row in matrix]
    n = len(a)
    value = 1
    for j in range(n):
        selected = next((i for i in range(j, n) if a[i][j]), None)
        assert selected is not None
        if selected != j:
            a[j], a[selected] = a[selected], a[j]
            value = -value
        pivot = a[j][j]
        value = value * pivot % p
        inverse = pow(pivot, -1, p)
        for i in range(j+1, n):
            factor = a[i][j]*inverse % p
            if factor:
                a[i][j:] = [(x-factor*y) % p for x, y in zip(a[i][j:], a[j][j:])]
    return value % p


def rank(matrix, p):
    a = [[int(v) % p for v in row] for row in matrix]
    j = 0
    for column in range(len(a[0])):
        k = next((i for i in range(j, len(a)) if a[i][column]), None)
        if k is None:
            continue
        a[j], a[k] = a[k], a[j]
        inverse = pow(a[j][column], -1, p)
        a[j] = [v*inverse % p for v in a[j]]
        for i in range(j+1, len(a)):
            factor = a[i][column]
            a[i] = [(x-factor*y) % p for x, y in zip(a[i], a[j])]
        j += 1
        if j == len(a):
            break
    return j


def main(certificate, output):
    raw = certificate.read_bytes()
    j = json.loads(raw)
    data = j['one_component_quadratic_interface']
    p, rho = data['prime'], data['rho']
    assert p == 1009 and rho*rho % p == 2
    monomials = [()] + [(i,) for i in range(21)] + [
        (i, k) for i in range(21) for k in range(i, 21)]
    rows = []
    for point in data['evaluation_points']:
        slot_values = []
        for sign in (1, -1):
            F, G, s, t, h, d, S, Z, F2, G2 = [
                (point[2*i]+sign*rho*point[2*i+1]) % p for i in range(10)]
            D = (11-6*sign*rho) % p
            assert all(x % p for x in (F, G, F-G, s, t, d, S, Z))
            assert (s*s*F+D*F*F-1) % p == 0
            assert (t*t*G+D*G*G-1) % p == 0
            assert (d-(h+s+t)*F) % p == (d-h*G) % p == 0
            assert (D*(F+G)-(s-t)*h+t*t) % p == 0
            assert (1-d*(s-t)+D*F*G) % p == 0
            q = (h+s-pow(d, -1, p)) % p
            assert q and (Z*q+2*S) % p == 0
            assert (F2-F*F) % p == (G2-G*G) % p == 0
            slot_values.append(Z*d % p)
        assert (2*point[20]-sum(slot_values)) % p == 0
        rows.append([1 if not m else point[m[0]] if len(m) == 1
                     else point[m[0]]*point[m[1]] % p for m in monomials])
    assert len(rows) == 236
    minor = [[row[c] for c in data['selected_columns']] for row in rows]
    det = determinant(minor, p)
    assert det == data['nonzero_minor_determinant_mod_prime'] == 514

    x = sp.symbols('x0:21')
    pair = lambda i: (x[2*i], x[2*i+1])
    add = lambda a, b: (a[0]+b[0], a[1]+b[1])
    neg = lambda a: (-a[0], -a[1])
    mul = lambda a, b: (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    F, G, s, t, h, d, S, Z, F2, G2 = [pair(i) for i in range(10)]
    pp = add(add(h, s), t)
    pairs = [add(d, neg(mul(pp, F))), add(d, neg(mul(h, G))),
             add(add(mul((11, -6), add(F, G)), neg(mul(add(s, neg(t)), h))), mul(t, t)),
             add(add((1, 0), neg(mul(d, add(s, neg(t))))), mul((11, -6), mul(F, G))),
             add(F2, neg(mul(F, F))), add(G2, neg(mul(G, G))),
             add(mul(F, d), neg(mul(pp, F2))), add(mul(G, d), neg(mul(h, G2)))]
    relations = [sp.Poly(v, *x) for pair0 in pairs for v in pair0] + [
        sp.Poly(x[20]-mul(Z, d)[0], *x)]
    terms = [sp.Integer(1) if not m else x[m[0]] if len(m) == 1
             else x[m[0]]*x[m[1]] for m in monomials]
    coefficients = [[int(f.coeff_monomial(m)) for m in terms] for f in relations]
    assert rank(coefficients, p) == 17
    assert all(sum(a*b for a, b in zip(row, c)) % p == 0 for row in rows for c in coefficients)
    false = [sp.Rational(v) for v in j['nontorsion_false_point']['coordinates']]
    substitution = dict(zip(x, false))
    assert all(f.as_expr().subs(substitution) == 0 for f in relations)
    residual = add(add(mul(mul(Z, d), add(h, s)), neg(Z)), mul((2, 0), mul(S, d)))
    residual = [sp.cancel(v.subs(substitution)) for v in residual]
    assert residual == [sp.Rational(-72, 41), sp.Rational(120, 41)]
    report = dict(status='PASS', checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        source_certificate_sha256=sha256(raw).hexdigest(),
        method='No producer imported; both split elliptic slots and quotient guards checked, minor reconstructed directly, coefficient identities independently expanded symbolically.',
        exact_graph_points=236, minor_size=236, prime=p, determinant=det,
        known_relation_rank=17, identity_dimension=17,
        false_scalar_residual=[str(v) for v in residual],
        scope='Finite exact arithmetic and stated interface only; characteristic-zero and density arguments require the separate proof review.')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    main(args.certificate, args.output)
