#!/usr/bin/env python3
"""Exact small-instance interpreter for the indexed determinant construction.

Standard library only. It materializes multiplication matrices, determinants,
trace-adjugate polynomials, every finite degree/selector case, and one complete
example polynomial. The source algebra of rank 2^508 is intentionally not
materialized. Tests target nilpotents, degree drops, bad separators, zero
radicals, nonrational residue fields, and closed trace conditions.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product, permutations
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Poly:
    def __init__(self, coefficients=()):
        if isinstance(coefficients, Poly):
            coefficients = coefficients.c
        elif isinstance(coefficients, (int, Fraction)):
            coefficients = [coefficients]
        values = [Fraction(c) for c in coefficients]
        while values and values[-1] == 0:
            values.pop()
        self.c = tuple(values)
    def __add__(self, other):
        other = Poly(other)
        return Poly([self[k]+other[k] for k in range(max(len(self.c), len(other.c)))])
    __radd__ = __add__
    def __neg__(self): return Poly([-c for c in self.c])
    def __sub__(self, other): return self+-Poly(other)
    def __rsub__(self, other): return Poly(other)+-self
    def __mul__(self, other):
        other = Poly(other)
        if not self.c or not other.c: return Poly()
        values = [Fraction(0)]*(len(self.c)+len(other.c)-1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c): values[i+j] += a*b
        return Poly(values)
    __rmul__ = __mul__
    def __pow__(self, exponent):
        out, base = Poly(1), self
        while exponent:
            if exponent & 1: out = out*base
            exponent >>= 1
            if exponent: base = base*base
        return out
    def __getitem__(self, index): return self.c[index] if index < len(self.c) else Fraction(0)
    def __eq__(self, other): return self.c == Poly(other).c
    @property
    def degree(self): return len(self.c)-1
    def derivative(self): return Poly([k*self[k] for k in range(1, len(self.c))])
    def at(self, value):
        out = Fraction(0)
        for c in reversed(self.c): out = out*value+c
        return out


def numeric_det(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    answer = Fraction(1)
    for k in range(len(a)):
        pivot = next((r for r in range(k, len(a)) if a[r][k]), None)
        if pivot is None: return Fraction(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]; answer = -answer
        p = a[k][k]; answer *= p
        for r in range(k+1, len(a)):
            q = a[r][k]/p
            for c in range(k+1, len(a)): a[r][c] -= q*a[k][c]
    return answer


def polynomial_det(matrix):
    n = len(matrix)
    require(n <= 6, "The exact demo interpreter deliberately caps matrices at dimension six")
    answer = Poly()
    for perm in permutations(range(n)):
        sign = -1 if sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n)) % 2 else 1
        term = Poly(sign)
        for row, col in enumerate(perm): term *= matrix[row][col]
        answer += term
    return answer


def numeric_adjugate(matrix):
    n = len(matrix)
    if n == 1: return [[Fraction(1)]]
    return [[(-1)**(i+j)*numeric_det([[matrix[r][c] for c in range(n) if c != i]
                                    for r in range(n) if r != j]) for j in range(n)] for i in range(n)]


def trace_polynomial(matrix, multiplier):
    answer = Poly()
    for column in range(len(matrix)):
        replaced = [[Poly(multiplier[i][j]) if j == column else matrix[i][j]
                     for j in range(len(matrix))] for i in range(len(matrix))]
        answer += polynomial_det(replaced)
    return answer


def resultant(f, g):
    n, m = f.degree, g.degree
    if n < 0 or m < 0: return Fraction(0)
    if n == 0: return f[0]**m
    if m == 0: return g[0]**n
    size = n+m
    rows = []
    for k in range(m): rows.append([Fraction(0)]*k+list(reversed(f.c))+[Fraction(0)]*(m-1-k))
    for k in range(n): rows.append([Fraction(0)]*k+list(reversed(g.c))+[Fraction(0)]*(n-1-k))
    require(all(len(r) == size for r in rows), "Wrong Sylvester dimensions")
    return numeric_det(rows)


def divisors(n):
    n = abs(n)
    result = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0: result.update((d, n//d))
    return result


def rational_roots(f):
    if f.degree <= 0: return set()
    scale = lcm(*(c.denominator for c in f.c))
    coeff = [int(c*scale) for c in f.c]
    divisor = gcd(*coeff)
    coeff = [c//divisor for c in coeff]
    require(coeff[0] != 0, "This interpreter uses H(0)=1")
    candidates = {Fraction(sign*a, b) for a in divisors(coeff[0])
                  for b in divisors(coeff[-1]) for sign in (-1, 1)}
    return {r for r in candidates if f.at(r) == 0}


class Algebra:
    """A finite monic triangular algebra over Q in a standard monomial basis."""
    def __init__(self, degrees, tails):
        self.degrees, self.tails = tuple(degrees), tails
        self.m = len(degrees)
        self.basis = list(product(*(range(d) for d in degrees)))
        self.position = {e: i for i, e in enumerate(self.basis)}
        self.n = len(self.basis)
        require(self.n <= 6, "Only small matrices are materialized")
        for i, tail in enumerate(tails):
            for e in tail:
                require(len(e) == self.m and e[i] < degrees[i] and not any(e[i+1:]), "Nontriangular relation")

    @lru_cache(None)
    def reduce_monomial(self, exponent):
        index = next((i for i in range(self.m-1, -1, -1) if exponent[i] >= self.degrees[i]), None)
        if index is None: return {exponent: Fraction(1)}
        out = Counter()
        for e, coefficient in self.tails[index].items():
            new = [a+b for a, b in zip(exponent, e)]; new[index] -= self.degrees[index]
            for monomial, scalar in self.reduce_monomial(tuple(new)).items(): out[monomial] -= coefficient*scalar
        return {e: Fraction(c) for e, c in out.items() if c}

    def normal(self, polynomial):
        out = Counter()
        for e, coefficient in polynomial.items():
            for monomial, scalar in self.reduce_monomial(e).items(): out[monomial] += coefficient*scalar
        return {e: Fraction(c) for e, c in out.items() if c}

    def constant(self, c): return {(0,)*self.m: Fraction(c)} if c else {}
    def variable(self, i):
        e = [0]*self.m; e[i] = 1
        return self.normal({tuple(e): 1})
    def add(self, *polynomials):
        out = Counter()
        for p in polynomials:
            for e, c in p.items(): out[e] += c
        return self.normal(dict(out))
    def scale(self, p, c): return self.normal({e: c*a for e, a in p.items()})
    def mul(self, *polynomials):
        out = self.constant(1)
        for p in polynomials:
            product_poly = Counter()
            for a, c in out.items():
                for b, d in p.items(): product_poly[tuple(i+j for i, j in zip(a, b))] += c*d
            out = self.normal(dict(product_poly))
        return out
    def matrix(self, p):
        matrix = [[Fraction(0)]*self.n for _ in range(self.n)]
        for column, e in enumerate(self.basis):
            value = self.mul(p, {e: 1})
            for monomial, c in value.items(): matrix[self.position[monomial]][column] = c
        return matrix
    @staticmethod
    def evaluate(p, point):
        answer = Fraction(0)
        for e, c in p.items():
            value = Fraction(c)
            for x, k in zip(point, e): value *= x**k
            answer += value
        return answer


def run_case(name, algebra, guard, equations, expected, expand_product=False):
    n, m = algebra.n, algebra.m
    variables = [algebra.variable(i) for i in range(m)]
    multiplier_matrices = [algebra.matrix(p) for p in equations+variables]
    recovered, squarefree_selectors, degree_drops = set(), 0, 0
    full_product = Poly(1)
    branch_count = 0
    for ell in range(m*n*(n+1)//2+1):
        lam = algebra.add(algebra.constant(1), *(algebra.scale(v, ell**(i+1)) for i, v in enumerate(variables)))
        M = algebra.matrix(algebra.mul(guard, lam))
        pencil = [[Poly([int(i == j), -M[i][j]]) for j in range(n)] for i in range(n)]
        H = polynomial_det(pencil)
        require(H[0] == 1, "Norm constant coefficient differs from one")
        traces = [trace_polynomial(pencil, ME) for ME in multiplier_matrices]
        # Independent numeric Gaussian/cofactor checks at enough exact points
        # to prove the degree-bounded determinant and trace identities.
        for v in range(n+1):
            numeric = [[p.at(v) for p in row] for row in pencil]
            require(H.at(v) == numeric_det(numeric), "Determinant identity failed")
            adj = numeric_adjugate(numeric)
            for trace, ME in zip(traces, multiplier_matrices):
                direct = sum(ME[i][j]*adj[j][i] for i in range(n) for j in range(n))
                require(trace.at(v) == direct, "Trace-adjugate identity failed")
        roots = rational_roots(H)
        for d in range(1, n+1):
            branch_count += 1
            Hd = Poly([H[k] for k in range(d+1)])
            ad = H[d]
            res = resultant(Hd, Hd.derivative()) if ad else Fraction(0)
            g, L = ad*res, ad**3*res
            psi = Poly([1]+[H[d-j]*ad**(2*j-1)*g**j for j in range(1, d+1)])
            reversed_traces = [Poly([trace[n-1-k]*L**k for k in range(n)]) for trace in traces[:len(equations)]]
            Q = psi**2+sum((H[k]**2 for k in range(d+1, n+1)), Fraction(0))
            for reversed_trace in reversed_traces: Q += reversed_trace**2
            if expand_product: full_product *= Q
            if not ad or not g:
                require(psi == 1, "A vanished base guard did not give reciprocal value one")
                continue
            if any(H[k] for k in range(d+1, n+1)): continue
            squarefree_selectors += 1
            degree_drops += int(d < n)
            for v in roots:
                U = 1/(L*v)
                require(psi.at(U) == 0, "Reciprocal root identity failed")
                if Q.at(U) != 0: continue
                J = -v*H.derivative().at(v)
                require(J != 0, "The reconstruction trace vanished")
                point = tuple(trace.at(v)/J for trace in traces[len(equations):])
                require(algebra.evaluate(guard, point) != 0 and all(algebra.evaluate(e, point) == 0 for e in equations),
                        "Trace reconstruction admitted an invalid point")
                for i, tail in enumerate(algebra.tails):
                    require(point[i]**algebra.degrees[i]+algebra.evaluate(tail, point) == 0,
                            "Reconstructed point violates a monic relation")
                recovered.add(point)
    require(recovered == set(expected), "Wrong projected rational point set in "+name)
    result = {"name": name, "rank": n, "generators": m, "finite_factors_checked": branch_count,
              "accepted_points": [[str(x) for x in p] for p in sorted(recovered)],
              "squarefree_selector_cases": squarefree_selectors, "accepted_degree_drop_cases": degree_drops}
    return result, full_product


def main():
    tests = []
    A = Algebra([2], [{(0,): -1}]); z = A.variable(0)
    result, example = run_case("closed condition on two rational roots", A, A.constant(1),
                              [A.add(z, A.constant(-1))], {(Fraction(1),)}, True)
    tests.append(result)
    A = Algebra([2], [{(0,): -2}])
    tests.append(run_case("nonrational quadratic field and bad constant separator", A, A.constant(1), [], set())[0])
    A = Algebra([3], [{(2,): -1}]); z = A.variable(0)
    tests.append(run_case("nilpotent component killed by guard", A, z, [], {(Fraction(1),)})[0])
    A = Algebra([2], [{}]); z = A.variable(0)
    tests.append(run_case("all nilpotent support excluded", A, z, [], set())[0])
    A = Algebra([1], [{}])
    tests.append(run_case("zero radical including zero quadratic coefficient", A, A.constant(1), [A.constant(0)],
                          {(Fraction(0),)})[0])
    tests.append(run_case("zero branch rejected by nonzero constant residual", A, A.constant(1), [A.constant(1)], set())[0])
    A = Algebra([2, 2], [{(0, 0): -1}, {(0, 0): -1}]); x, y = A.variable(0), A.variable(1)
    tests.append(run_case("four points with a colliding separator", A, A.constant(1), [A.add(x, A.scale(y, -1))],
                          {(Fraction(1), Fraction(1)), (Fraction(-1), Fraction(-1))})[0])
    A = Algebra([4], [{(2,): -4}]); z = A.variable(0)
    guard = A.scale(A.mul(z, z), 8)
    tests.append(run_case("point quartic with a double excluded zero root", A, guard, [],
                          {(Fraction(2),), (Fraction(-2),)})[0])
    require(all(c.denominator == 1 for c in example.c), "Example polynomial lost integer coefficients")
    here = Path(__file__).resolve().parent
    polynomial = {"definition": "The full indexed polynomial for A=Q[z]/(z^2-1), G=1, E=z-1, including every selector and degree case.",
                  "variable": "U", "coefficients_ascending": [int(c) for c in example.c], "degree": example.degree}
    raw = (json.dumps(polynomial, separators=(",", ":"))+"\n").encode()
    (here/"small-example-expanded-polynomial.json").write_bytes(raw)
    receipt = {"status": "passed", "exact_arithmetic": "fractions and integers; no probabilistic evaluations",
               "test_cases": tests, "total_factors_checked": sum(t["finite_factors_checked"] for t in tests),
               "example_polynomial_degree": example.degree,
               "example_polynomial_sha256": hashlib.sha256(raw).hexdigest(),
               "interpreter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "scope": "Actual matrix/determinant/resultant and full finite-case execution on eight adversarial small algebras. The rank-2^508 source algebra is not materialized."}
    (here/"small-algebra-verification.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k: receipt[k] for k in ("status", "total_factors_checked", "example_polynomial_degree", "example_polynomial_sha256")}, indent=2))


if __name__ == "__main__":
    main()
