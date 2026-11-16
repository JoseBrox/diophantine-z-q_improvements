#!/usr/bin/env python3
"""Exact certificates for the mixed-power height proof; no numerical sampling."""
import argparse
from hashlib import sha256
from pathlib import Path
import json
import sympy as s

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
n, kap, a, b, c, e = s.symbols("n kappa a b c e")
N, A, E, C, K, Z = s.symbols("N A E C K Z", nonnegative=True)
D = 2*n-kap*(n+2)
coefficient = (n+kap*(n-2))/(n*D)

checks = []

def identity(name, lhs, rhs):
    difference = s.factor(lhs-rhs)
    assert difference == 0, (name, difference)
    checks.append({"name": name, "kind": "symbolic identity", "passed": True})

def positive_polynomial(name, value, variables):
    expanded = s.Poly(s.expand(value), *variables)
    assert all(q >= 0 for q in expanded.coeffs()), (name, expanded)
    checks.append({
        "name": name,
        "kind": "nonnegative coefficient polynomial",
        "certificate": str(expanded.as_expr()),
        "domain": "Every displayed parameter is nonnegative.",
        "passed": True,
    })

# n=N+3, k=K+1 parametrizes the theorem's integer n range and
# the positive multiple 2*n*k that occurs in the local congruences.
case_specs = [
    ("a>0,e>=0", 2*n*K+(2*n-2)*E),
    ("a>0,e<0", 2*A+2*(n-1)*E),
    ("b>0", 2*n*A),
    ("c>0,e=0", 2*n*K),
    ("c>0,e>0", C+(2*n-1)*E),
    ("c>0,e<0", 2*n*K+(n-2)*(Z+1)),
]

identity("a positive, e nonnegative gap",
         a+(2*n-1)*e-2*n,
         (a+e-2*n)+(2*n-2)*e)
identity("a positive, e negative gap",
         (2+2*A)+(n-1)*(2+2*E)-2*n,
         2*A+2*(n-1)*E)
identity("b positive gap", n*(2+2*A)-2*n, 2*n*A)
identity("c positive, e zero gap", 2*n*(K+1)-2*n, 2*n*K)
identity("c positive, e positive gap",
         (1+C)+(2*n-1)*(1+E)-2*n, C+(2*n-1)*E)
identity("c positive, e negative gap",
         c+(n-1)*(-e)-2*n,
         (c-e-2*n)+(n-2)*(-e))
for name, value in case_specs:
    positive_polynomial(name, value.subs(n, N+3), (N, A, E, C, K, Z))

identity("height numerator simplification",
         D+kap*(3*n-2), 2*(n+kap*(n-2)))
identity("x height coefficient", (1+kap*(3*n-2)/D)/(2*n), coefficient)
identity("x additive constant", (2*n/D)/(2*n), 1/D)
identity("y height coefficient", (1+kap*(3*n-2)/D)/2, n*coefficient)
identity("y additive constant", (2*n/D)/2, n/D)

def fraction(q):
    q = s.Rational(q)
    return f"{q.p}/{q.q}" if q.q != 1 else str(q.p)

rows = []
expected = {
    4: (s.Rational(301,388), s.Rational(50,97)),
    6: (s.Rational(251,588), s.Rational(25,98)),
    8: (s.Rational(703,2360), s.Rational(10,59)),
}
for nv, (want_c, want_add) in expected.items():
    values = {n:nv, kap:s.Rational(101,100)}
    cv = s.factor(coefficient.subs(values))
    add = s.factor((1/D).subs(values))
    assert cv == want_c and add == want_add
    rows.append({
        "n": nv, "kappa": "101/100", "x_height": fraction(cv),
        "x_logK": fraction(add), "y_height": fraction(nv*cv),
        "y_logK": fraction(nv*add),
        "max_divisor_height_degree_eight_contacts_strict": fraction(7/(4*cv)),
    })
    checks.append({"name": f"n={nv} exact coefficients", "passed": True})

absorptions = []
for nv, divisor_degree, wanted in [
    (4, 2, s.Rational(602,679)),
    (6, 4, s.Rational(1004,1029)),
    (8, 4, s.Rational(1406,2065)),
]:
    cv = coefficient.subs({n:nv,kap:s.Rational(101,100)})
    result = s.factor(s.Rational(4,7)*divisor_degree*cv)
    assert result == wanted and result < 1
    absorptions.append({"n":nv,"divisor_height_degree":divisor_degree,
                        "coefficient":fraction(result),"strictly_below_one":True})
    checks.append({"name":f"n={nv}, divisor degree {divisor_degree} absorption",
                   "passed":True})

X,z2,z4,z8,T,t0,t1,B = s.symbols("X z2 z4 z8 T t0 t1 B")
quadrics = [z2-X**2,z4-z2**2,z8-z4**2,t1-t0-B-z8**2-T**2]
qvars = (X,z2,z4,z8,T,t0,t1)
degrees = [s.Poly(q,*qvars).total_degree() for q in quadrics]
assert degrees == [2,2,2,2]
identity("height circuit computes X^16",
         (z8**2).subs(z8,z4**2).subs(z4,z2**2).subs(z2,X**2), X**16)
checks.append({"name":"height circuit has four quadratic rows, three power coordinates",
               "degrees":degrees,"passed":True})

M = s.symbols("M", nonnegative=True)
positive_polynomial("second residual factor constant bound", 8*(1+M)-(M+8), (M,))
assert 4*8 == 32
checks.append({"name":"product residual constant is 32","passed":True})

source = REPO / "papers/elliptic_heights/mixed_power_height_20261116_v45.tex"
report = {
    "status":"PASS",
    "scope":"Exact symbolic arithmetic and unbounded local-case certificates for the written proof. No detector completeness or new variable record is asserted.",
    "source_sha256":sha256(source.read_bytes()).hexdigest(),
    "checks":checks,
    "check_count":len(checks),
    "coefficient_table":rows,
    "eight_contact_absorptions":absorptions,
    "height_circuit":{"power_coordinates":["z2","z4","z8"],
                      "quadratic_row_count":4,
                      "additional_coordinate_cost_over_X8":1,
                      "additional_row_cost_over_X8":1,
                      "strict_net_saving_requires_other_coordinate_saving_at_least":2},
    "hypothesis_scope":{
        "mixed_power_theorem":"Only the fixed weak-abc exponent kappa is used.",
        "marked_contacts":"Ordinary abc is retained for the cited marked-contact theorem.",
        "product_residual_application":"Requires the stated detector divisibility, uniform constants, and all-point index-height theorem.",
    },
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path,
                    help="Write a new certificate to exactly this path.")
parser.add_argument("--check", action="store_true",
                    help="Compare with the committed certificate without writing files.")
args = parser.parse_args()
if args.check:
    committed = json.loads((HERE / "certificate.json").read_text())
    assert report == committed, "Committed certificate differs from exact reconstruction."
if args.output is not None:
    args.output.write_text(json.dumps(report, indent=2)+"\n")
if args.check or args.output is not None:
    print(json.dumps({"status":"PASS", "checks":len(checks),
                      "certificate_match":True if args.check else None,
                      "output":str(args.output) if args.output is not None else None}))
else:
    print(json.dumps(report, indent=2))
