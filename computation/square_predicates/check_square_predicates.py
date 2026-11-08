#!/usr/bin/env python3
"""Exact identities and complete coefficient data for quadratic square tests.

Python 3.10+; standard library only. The degree lower bound is proved in the
paper using Hilbert irreducibility and discrete valuations. This program
verifies the algebraic identities, coefficient tables, a resultant, and the
finite group calculation that accompany that proof.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import math


class Poly:
    names = ('u', 'v', 'U', 'V', 'T', 'd', 'k', 'r')
    n = len(names)

    def __init__(self, terms=0):
        if isinstance(terms, (int, Fraction)):
            terms = {(0,) * self.n: Fraction(terms)}
        self.terms = {m: Fraction(c) for m, c in terms.items() if c}

    @classmethod
    def var(cls, name, exponent=1):
        m = [0] * cls.n
        m[cls.names.index(name)] = exponent
        return cls({tuple(m): 1})

    @classmethod
    def coerce(cls, other):
        return other if isinstance(other, cls) else cls(other)

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in self.coerce(other).terms.items():
            out[m] = out.get(m, 0) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        out = {}
        for m, a in self.terms.items():
            for n, b in self.coerce(other).terms.items():
                e = tuple(x + y for x, y in zip(m, n))
                out[e] = out.get(e, 0) + a * b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        out, base = Poly(1), self
        while n:
            if n & 1:
                out *= base
            n >>= 1
            if n:
                base *= base
        return out

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def substitute(self, mapping):
        out = Poly(0)
        for m, c in self.terms.items():
            term = Poly(c)
            for name, exponent in zip(self.names, m):
                if exponent:
                    assert exponent >= 0
                    term *= mapping.get(name, self.var(name)) ** exponent
            out += term
        return out

    def degree(self, names=None):
        ids = list(range(self.n)) if names is None else [self.names.index(s) for s in names]
        return max((sum(m[i] for i in ids) for m in self.terms), default=-1)

    def height(self):
        assert all(c.denominator == 1 for c in self.terms.values())
        return max(abs(c.numerator) for c in self.terms.values())

    def evaluate(self, mapping):
        out = Fraction(0)
        for m, c in self.terms.items():
            for name, exponent in zip(self.names, m):
                if exponent:
                    c *= Fraction(mapping[name]) ** exponent
            out += c
        return out


def determinant(matrix):
    """Leibniz determinant using subset dynamic programming; no divisions."""
    n = len(matrix)
    partial = {0: Poly(1)}
    for row in range(n):
        new = {}
        for mask, value in partial.items():
            for col in range(n):
                if mask & (1 << col):
                    continue
                sign = -1 if (mask >> (col + 1)).bit_count() % 2 else 1
                target = mask | (1 << col)
                new[target] = new.get(target, Poly(0)) + sign * value * matrix[row][col]
        partial = new
    return partial[(1 << n) - 1]


def coefficient_table(poly, variables):
    selected = [Poly.names.index(s) for s in variables]
    assert all(all(e == 0 for i, e in enumerate(m) if i not in selected) for m in poly.terms)
    return [{'exponents': [m[i] for i in selected], 'coefficient': str(c.numerator)}
            for m, c in sorted(poly.terms.items(), reverse=True)]


def group_check():
    # Permutations of x,-x,y,-y induced by independent signs and interchange.
    perms = []
    for swap, sx, sy in product((0, 1), repeat=3):
        a, b = ((2, 0) if swap else (0, 2))
        perms.append((a + sx, a + (1 - sx), b + sy, b + (1 - sy)))
    perms = sorted(set(perms))
    identity = (0, 1, 2, 3)
    interchange = (2, 3, 0, 1)
    compose = lambda a, b: tuple(a[b[i]] for i in range(4))
    assert len(perms) == 8
    assert all(compose(a, b) in perms for a in perms for b in perms)
    overgroups = []
    for mask in range(1 << 8):
        subset = {perms[i] for i in range(8) if mask & (1 << i)}
        if identity not in subset or interchange not in subset:
            continue
        if all(compose(a, b) in subset for a in subset for b in subset):
            overgroups.append(sorted(subset))
    assert sorted(map(len, overgroups)) == [2, 4, 8]
    return {'group_order': 8, 'stabilizer_order': 2,
            'overgroup_orders': sorted(map(len, overgroups)),
            'unique_proper_intermediate_field_degree': 2}


def main():
    u, v, U, V, T, d, k, r = [Poly.var(s) for s in Poly.names]
    di = Poly.var('d', -1)
    q = Fraction
    A = 3 * U**3 - 2 * U**2 * V - 3 * U * V**2
    B = -2 * U**3 + U**2 * V + 2 * U * V**2 + V**3
    a, b = U + V, -U
    multiplier_norm = -U**2 + 2 * U * V + V**2
    assert a**2 - 2 * b**2 == multiplier_norm
    assert (a**2 + 2 * b**2) * U + 4 * a * b * V == A
    assert (a**2 + 2 * b**2) * V + 2 * a * b * U == B
    assert A**2 - 2 * B**2 == multiplier_norm**2 * (U**2 - 2 * V**2)
    source = {'U': u**2 + 2 * v**2, 'V': 2 * u * v}
    root_real = u**3 + 2 * u * v**2 - 4 * v**3
    root_imag = -u**3 + u**2 * v + 2 * v**3
    assert a.substitute(source) * u + 2 * b.substitute(source) * v == root_real
    assert a.substitute(source) * v + b.substitute(source) * u == root_imag
    G = 2 * T**4 - 2 * A * T**2 + B**2
    expanded = (4 * U**6 - 4 * U**5 * V - 7 * U**4 * V**2
                + 6 * U**2 * V**4 + 4 * U * V**5 + V**6
                - 6 * U**3 * T**2 + 4 * U**2 * V * T**2
                + 6 * U * V**2 * T**2 + 2 * T**4)
    assert G == expanded
    assert G.substitute(dict(source, T=root_real)) == 0
    # Rational reconstruction: clearing 2*T^2 in the real square component.
    assert 2 * T**4 + B**2 - 2 * A * T**2 == G
    assert 2 * root_imag**2 + root_real**2 == A.substitute(source)
    projective_residues = [int(B.evaluate({'U':x,'V':1})) % 3 for x in range(3)]
    projective_residues.append(int(B.evaluate({'U':1,'V':0})) % 3)
    assert projective_residues == [1, 2, 2, 1]

    P10 = (2 - 2 * U * T**2 + V**2 * T**4) * (V**2 + (U - 2 * T**2)**2)
    expanded10 = (2 * V**2 + 2 * U**2 - 8 * U * T**2 + 8 * T**4
                  - 2 * U * V**2 * T**2 - 2 * U**3 * T**2 + 8 * U**2 * T**4
                  - 8 * U * T**6 + V**4 * T**4 + U**2 * V**2 * T**4
                  - 4 * U * V**2 * T**6 + 4 * V**2 * T**8)
    assert P10 == expanded10
    Q4 = (U - u**2 - 2 * v**2)**2 + (V - 2 * u * v)**2
    assert Q4 == U**2 + V**2 + u**4 + 4 * v**4 + 8 * u**2 * v**2 - 2 * U * u**2 - 4 * U * v**2 - 4 * V * u * v
    assert (G.degree(), G.degree(('T',)), G.height(), len(G.terms)) == (6, 4, 7, 10)
    assert (P10.degree(), P10.degree(('T',)), P10.height(), len(P10.terms)) == (10, 8, 8, 12)
    assert (Q4.degree(), Q4.height(), len(Q4.terms)) == (4, 8, 8)
    assert math.gcd(*(abs(c.numerator) for c in G.terms.values())) == 1

    # Independent Sylvester determinant for the complete sextic's T-discriminant.
    f, fp = [Poly(2), Poly(0), -2*A, Poly(0), B**2], [Poly(8), Poly(0), -4*A, Poly(0)]
    sylvester = [[Poly(0) for _ in range(7)] for _ in range(7)]
    for i in range(3):
        sylvester[i][i:i+5] = f
    for i in range(4):
        sylvester[i+3][i:i+4] = fp
    discriminant = q(1, 2) * determinant(sylvester)
    assert discriminant == 512 * B**2 * multiplier_norm**4 * (U**2 - 2 * V**2)**2

    # General quadratic field identities, verified over Q[d,d^-1,k,u,v,U,V].
    ag = U + q(1, 2)*k*di*V
    bg = -k*di**2*U - q(1, 2)*V
    Ag = (ag**2+d*bg**2)*U + 2*d*ag*bg*V
    Bg = (ag**2+d*bg**2)*V + 2*ag*bg*U
    assert 4*d**2*Bg == -8*k*U**3 + 6*k*d*U*V**2 + (k**2+d**3)*V**3
    assert ag**2-d*bg**2 == q(1, 4)*(d**3-k**2)*di**3*(4*U**2-d*V**2)
    assert Ag**2-d*Bg**2 == (ag**2-d*bg**2)**2*(U**2-d*V**2)
    assert k*r**6-(k**2+d**3)*r**3+k*d**3 == (r**3-k)*(k*r**3-d**3)

    examples = [(0,0,0), (q(1,4),0,q(1,8)), (2,0,-4), (3,2,-1)]
    for x,y,t in examples:
        assert G.evaluate({'U':x,'V':y,'T':t}) == 0
    tables = {
        'format': 'quadratic-square-predicates/v1',
        'base_field': 'Q', 'extension': 'Q(sqrt(2))',
        'sextic': {'variables':['U','V','T'], 'total_degree':6, 'degree_in_T':4,
                   'coefficient_height':7, 'content':1, 'terms':coefficient_table(G,['U','V','T'])},
        'degree10': {'variables':['U','V','T'], 'total_degree':10, 'degree_in_T':8,
                    'coefficient_height':8, 'terms':coefficient_table(P10,['U','V','T'])},
        'quartic_two_auxiliaries': {'variables':['U','V','u','v'], 'total_degree':4,
                                  'coefficient_height':8, 'terms':coefficient_table(Q4,['U','V','u','v'])},
    }
    root=Path(__file__).resolve().parent
    table_path=root/'square-predicate-polynomials.json'
    table_path.write_text(json.dumps(tables,indent=2)+'\n')
    report={'status':'PASS','arithmetic':'exact sparse rational polynomial arithmetic',
            'identities':['complete sextic expansion','complete degree10 expansion',
                          'two-auxiliary quartic expansion','cubic coordinate transformation',
                          'general multiplier and norm identities','general irreducibility cubic identity',
                          'seven-by-seven Sylvester determinant for the sextic discriminant'],
            'finite_group_check':group_check(),
            'cubic_nonzero_residues_at_P1_F3':projective_residues,
            'examples':[{'U':str(x),'V':str(y),'T':str(t)} for x,y,t in examples],
            'proof_boundary':'Square-test completeness, irreducibility, and degree optimality are proved in the paper. The lower bound uses Hilbert irreducibility; these computations do not replace that theorem.',
            'polynomial_data_sha256':hashlib.sha256(table_path.read_bytes()).hexdigest(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (root/'square-predicate-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
