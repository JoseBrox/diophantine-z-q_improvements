#!/usr/bin/env python3
"""Independent constants supporting the v47 scalar source-transfer audit.

This checker does not import the scalar producer/checker.  The mathematical
source-transfer argument is in the accompanying norm-compatible-scalar manuscript.
"""
from fractions import Fraction as Q
import hashlib
import json
import argparse
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
n = 116576341082536192
D = 5951086353
d = 10657
ell = 76249
aa = [5951086353, 5960872849, 17757117551, 5845158349]
theta = [Q(0), Q(1), Q(2401), Q(-343, 32)]
K = 25481059893697
H = 279986328
A = 97391047218196174706960881179098628096
B = 152061501652330028986565424
C = 59355302528062
M = 397180638679647074411201284065117677360619724674885081954
eta = 34
A0 = 102 * eta * M

def val(z, p):
    z = Q(z)
    if z == 0:
        raise ValueError("valuation at zero")
    ans = 0
    num, den = abs(z.numerator), z.denominator
    while num % p == 0:
        ans += 1
        num //= p
    while den % p == 0:
        ans -= 1
        den //= p
    return ans

def r4(t):
    return t * (t - 1) * (t - 2401) * (32 * t + 343)

assert s.isprime(d) and s.isprime(ell)
assert d < 76176 < ell
assert all(Q(a * a) == D * D + n * th for a, th in zip(aa, theta))
assert H == 2**3 * 3**3 * 17 * ell
assert d * n * H * H == A
assert 2 * d * H * K == B
assert Q(d * K * K - D * D, n) == C
assert C > 2401 and min(A, B) > 0
assert r4(C) == M
assert M % ell != 0 and (1 + A0 * M) % ell != 0
assert all((C - th) % ell != 0 for th in theta)
assert [val(A, ell), val(B, ell), val(C, ell)] == [2, 1, 0]

X,Z = s.symbols("X Z")
U = 1+X*(X-1)*(X-2)*(X-3)/24
beta = s.Poly(s.expand(A*U**2+B*U+C),X)
assert beta.degree()==8 and all(z.q==1 for z in beta.all_coeffs())
assert s.expand(24*U-(X*X-3*X+1)**2-23)==0
assert s.expand((d*(n*H*U+K)**2-D**2)/n-beta.as_expr())==0
assert beta.eval(0)==A+B+C != C
# The norm anchor is at Z=K, not at X=0 after the binomial shift.
abstract_beta=(d*Z*Z-D*D)/n
norm_product=s.prod(a*a-d*Z*Z for a in aa)
assert s.expand(r4(abstract_beta)-s.Rational(32,n**4)*norm_product)==0
assert s.Rational(32,n**4)*norm_product.subs(Z,K)==M
integrality = []
for p in s.factorint(A):
    p = int(p)
    va,vb,shift = val(A,p),val(B,p),val(24,p)
    if p==2:
        assert (va,vb,shift,val(C,p))==(14,4,3,1)
        assert va-2*(4+shift)==0 and vb-4-shift==-3
        assert va-vb-(8+shift)<0 and va-2*(8+shift)<0
        case="B U wins at e=1; A U^2 wins for e>=2"
    else:
        assert va-2*(4+shift)<min(vb-4-shift,0)
        case="A U^2 wins for every e>=1"
    assert p<=76176 or p==ell
    integrality.append({"prime":p,"vA":va,"vB":vb,"v24":shift,"case":case})
assert val(A,ell)==2 and val(B,ell)==1
certificate=json.loads((HERE/"certificate.json").read_text())
assert certificate["input_polynomial"]["degree"]==8
assert certificate["input_polynomial"]["coefficients_ascending"]==[int(beta.nth(i)) for i in range(9)]

local = []
for p, expected in [(2, 4), (3, 8), (17, 2)]:
    vc = [val(x, p) for x in [C, C-1, C-2401, 32*C+343]]
    precision = min(val(A,p), val(B,p))
    relative = min(precision - z for z in vc[:3])
    relative = min(relative, precision + val(32,p) - vc[3])
    assert relative >= (3 if p == 2 else 1)
    assert val(eta**2 * M**2, p) == expected
    assert A0 % p == 0
    assert (ell % 8 == 1 if p == 2 else s.legendre_symbol(ell, p) == 1)
    local.append({"prime": p, "relative_precision": relative,
                  "rho_valuation": expected})

for x, y, z, norm in [(147,1,74,2),(143,1,24,17),(1075327,3900,3611,ell)]:
    assert x*x - d*y*y == norm*z*z
assert d % 8 == 1
for p in [3,17,ell]:
    assert s.legendre_symbol(d,p) == 1

paths = [
    "papers/few_variables25/few_variables25_merged_20261110_v19.tex",
    "papers/finite_algebra/unit_norm_20261114_v28.tex",
    "papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex",
]
source_hashes = {p: hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in paths}
receipt = {
    "status": "PASS_INDEPENDENT_SOURCE_TRANSFER_AUDIT",
    "scope": "Exact constants plus separate mathematical transfer audit under retained source premises",
    "five_height_contacts": ["infinity", "0", "1", "2401", "-343/32"],
    "deleted_auxiliary_factor": "2 beta - 1 is not one of the five required contacts",
    "integrality_reflection": integrality,
    "input_degree": 8,
    "binomial_substitution_checked": True,
    "fixed_norm_anchor_at_Z_equals_K_checked": True,
    "all_negative_beta_valuations_even_outside_original_S": True,
    "consumed_ell_remains_nonexceptional": True,
    "local_preparation": local,
    "uniform_height_bound": "h(rho) <= 12 h(beta) + 2 L log(ell) + O(1)",
    "source_exponents_unchanged": ["7/9", "7/18", "7/6", "35/18"],
    "count": "25 total variables under the same retained premises; no numerical degree bound",
    "no_prescribed_trace_realization_claim": True,
    "source_sha256": source_hashes,
    "main_certificate_sha256":hashlib.sha256((HERE/"certificate.json").read_bytes()).hexdigest(),
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path)
args=parser.parse_args()
encoded=json.dumps(receipt,indent=2)+"\n"
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(encoded)
print(encoded,end="")
