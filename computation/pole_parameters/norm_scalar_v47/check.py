#!/usr/bin/env python3
"""Exact certificate for the v47 norm-compatible scalar replacement.

Standard-library arithmetic only. The source transfer and conic Hasse principle are proved in the accompanying
manuscript. The input map has degree eight.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import isqrt, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
n = 116576341082536192
D = 5951086353
d = 10657
ell = 76249
K = 25481059893697
H = 279986328
contacts = [Q(0), Q(1), Q(2401), Q(-343, 32)]
roots = [5951086353, 5960872849, 17757117551, 5845158349]


def prime(a):
    return a > 1 and all(a % t for t in range(2, isqrt(a) + 1))


def val(a, p):
    assert a
    if isinstance(a, Q):
        return val(a.numerator, p) - val(a.denominator, p)
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def r4(a):
    return a*(a-1)*(a-2401)*(32*a+343)


def clean(a):
    return {i: Q(c) for i, c in a.items() if c}


def add(a, b):
    out = dict(a)
    for i, c in b.items():
        out[i] = out.get(i, Q(0)) + c
    return clean(out)


def scale(a, c):
    return clean({i: c*x for i, x in a.items()})


def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] = out.get(i+j, Q(0)) + x*y
    return clean(out)


def pairmul(a, b):
    return (add(mul(a[0], b[0]), scale(mul(a[1], b[1]), d)),
            add(mul(a[0], b[1]), mul(a[1], b[0])))


def pairnorm(a):
    return add(mul(a[0], a[0]), scale(mul(a[1], a[1]), -d))


assert prime(d) and d <= 76176 and prime(ell) and ell > 76176
assert d % 8 == 1
assert all(pow(d, (p-1)//2, p) == 1 for p in (3, 17, ell))
assert H == 2**3 * 3**3 * 17 * ell
assert all(D*D+n*t == a*a for t, a in zip(contacts, roots))

norm_constants = [
    {"norm": 2, "rational_numerator": 147, "irrational_numerator": 1, "denominator": 74},
    {"norm": 17, "rational_numerator": 143, "irrational_numerator": 1, "denominator": 24},
    {"norm": ell, "rational_numerator": 1075327, "irrational_numerator": 3900, "denominator": 3611},
]
for c0 in norm_constants:
    assert c0["rational_numerator"]**2-d*c0["irrational_numerator"]**2 == c0["norm"]*c0["denominator"]**2

# Check the abstract polynomial norm identity in Z before composition.
beta_z = {2: Q(d, n), 0: Q(-D*D, n)}
lhs = {0: Q(32)}
gamma = ({0: Q(4*147, 74*n*n)}, {0: Q(4, 74*n*n)})
for theta, a in zip(contacts, roots):
    lhs = mul(lhs, add(beta_z, {0: -theta}))
    gamma = pairmul(gamma, ({0: Q(a)}, {1: Q(1)}))
assert lhs == pairnorm(gamma)

assert (d*K*K-D*D) % n == 0
A = d*n*H*H
B = 2*d*H*K
C = (d*K*K-D*D)//n
assert (A, B, C) == (
    97391047218196174706960881179098628096,
    152061501652330028986565424,
    59355302528062,
)
assert A > 0 and B > 0 and C > 2401

n_factors = {2: 8, 11: 1, 13: 1, 101: 1, 757: 1, 7013: 1, 5939: 1}
assert all(prime(p) for p in n_factors)
assert prod(p**e for p, e in n_factors.items()) == n
A_factors = dict(n_factors)
for p, e in {d: 1, 2: 6, 3: 6, 17: 2, ell: 2}.items():
    A_factors[p] = A_factors.get(p, 0)+e
assert prod(p**e for p, e in A_factors.items()) == A
# The degree-eight map beta=A U^2+B U+C, U=1+binom(X,4).
U = {4: Q(1,24), 3: Q(-1,4), 2: Q(11,24), 1: Q(-1,4), 0: Q(1)}
beta8 = add(add(scale(mul(U,U),A),scale(U,B)),{0:Q(C)})
assert max(beta8)==8 and all(c.denominator==1 for c in beta8.values())
assert A % 576 == 0 and B % 24 == 0
assert scale(U,24)==add(mul({2:Q(1),1:Q(-3),0:Q(1)},
                            {2:Q(1),1:Q(-3),0:Q(1)}),{0:Q(23)})
Z = add(scale(U,n*H),{0:Q(K)})
assert all(c.denominator==1 for c in Z.values())
assert add(scale(mul(Z,Z),Q(d,n)),{0:Q(-D*D,n)})==beta8
# At v_p(X)=-e, v_p(U)=-4e-v_p(24); the falling factors
# all have the same negative order. These coefficient inequalities
# prove dominance uniformly, not only for finitely many denominators.
integer_test = []
for p, va in sorted(A_factors.items()):
    vb, shift = val(B,p), val(24,p)
    first_lead, first_middle = va-2*(4+shift), vb-(4+shift)
    if p==2:
        assert (va,vb,shift,val(C,2))==(14,4,3,1)
        assert first_middle==-3 and first_middle<min(first_lead,val(C,2))
        assert va-vb-(8+shift)<0 and va-2*(8+shift)<0
        cases=[{"input_denominator_order":1,"winning_term":"B*U","beta_valuation":"-3"},
               {"input_denominator_order":">=2","winning_term":"A*U^2","beta_valuation":"8-8e"}]
    else:
        assert first_lead < first_middle and first_lead < 0
        cases=[{"input_denominator_order":">=1","winning_term":"A*U^2",
                "beta_valuation":f"{va-2*shift}-8e"}]
    assert p<=76176 or p==ell
    integer_test.append({"p":p,"v_A":va,"v_B":vb,"v_24":shift,"cases":cases})
# For every prime not dividing A: p is neither2 nor3, the leading
# order is -8e and is strictly lower than all other orders.

M0 = r4(C)
eta = 34
A0 = 102*eta*M0
assert M0 == 397180638679647074411201284065117677360619724674885081954
assert M0 % ell and A0 % ell
assert (1+A0*M0) % ell
assert (val(A, ell), val(B, ell), val(C, ell)) == (2, 1, 0)
assert C % ell == 10968 and M0 % ell == 19666

local_preparation = []
factors_C = [C, C-1, C-2401, 32*C+343]
for p, required_increment in ((2, 3), (3, 1), (17, 1)):
    delta_val = min(val(A, p), val(B, p))
    factor_vals = [val(f, p) for f in factors_C]
    increments = [delta_val+val(a, p)-v
                  for a, v in zip((1, 1, 1, 32), factor_vals)]
    assert min(increments) >= required_increment
    assert val(A0, p) >= 1
    assert (ell % 8 == 1) if p == 2 else pow(ell, (p-1)//2, p) == 1
    rho_val = 2*val(eta, p)+2*val(M0, p)
    assert rho_val == {2: 4, 3: 8, 17: 2}[p]
    local_preparation.append({"p": p, "min_v_beta_minus_C": delta_val,
                              "contact_valuations_at_C": factor_vals,
                              "min_relative_contact_precision": min(increments),
                              "rho_valuation_for_every_integer_X": rho_val,
                              "rho_is_local_square": True})

# Recover the osculating-curve identity independently by coefficient arithmetic.
qpoly = {2: Q(-80791, 3584), 1: Q(76832, 3584), 0: Q(8605184, 3584)}
hpoly = add(mul({2: Q(1), 0: Q(-2401)}, {2: Q(1), 0: Q(-2401)}),
            scale(mul(mul({1: Q(1)}, {1: Q(1), 0: Q(-1)}),
                      {1: Q(-1), 0: Q(2401)}), Q(-343, 8)))
diff = add(mul(qpoly, qpoly), scale(hpoly, -1))
assert set(diff) == {3, 4}
parameter = -diff[3]/diff[4]
assert parameter == Q(153664, 77207)
assert 4*parameter*(parameter-1)*(2401-parameter)/(parameter**2-2401)**2 == Q(n, D*D)

source_names = [
    "papers/finite_algebra/unit_norm_20261114_v28.tex",
    "papers/few_variables25/few_variables25_merged_20261110_v19.tex",
    "papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex",
    "papers/pole_parameters/finite_complement_classes_20261116_v46.tex",
]
source_hashes = {name: sha256((REPO/name).read_bytes()).hexdigest() for name in source_names}
text = (REPO/source_names[0]).read_text()
assert "a_1=1+\\rho T^2" in text
dependency = (REPO/source_names[2]).read_text()
assert "at every prime dividing the avoidance modulus the residue is $i$" in dependency

certificate = {
    "schema": "norm-compatible-scalar/v47",
    "status": "PASS",
    "scope": "Exact scalar identities and arithmetic certificate; full source transfer proved in accompanying note",
    "count": "Same 25 total coordinates; no smaller defining-polynomial count proved",
    "unresolved": "Prescribed native reciprocal traces on the two globally soluble norm conics",
    "norm_field": {"d": d, "prime": True, "supported_on_original_S": True},
    "norm_constants": norm_constants,
    "four_contact_certificate": {"n": n, "D": D, "square_numerators": roots,
                                 "abstract_polynomial_norm_identity": True,
                                 "osculating_parameter": str(parameter)},
    "input_polynomial": {"degree": 8, "A": A, "B": B, "C": C,
                         "U": "1+X*(X-1)*(X-2)*(X-3)/24",
                         "coefficients_ascending": [int(beta8.get(i,0)) for i in range(9)],
                         "K": K, "H": H},
    "integrality_reflection": integer_test,
    "scalar_constants": {"M0": M0, "eta": eta, "A0": A0, "ell": ell},
    "ell_certificate": {"C_mod_ell": C % ell, "M0_mod_ell": M0 % ell,
                         "A0_mod_ell": A0 % ell,
                         "denominator_mod_ell_at_integral_input": (1+A0*M0) % ell,
                         "v_rho_when_vX_nonnegative": "L",
                         "v_rho_when_vX_minus_e": "L-8+32e"},
    "local_preparation": local_preparation,
    "new_exceptional_primes": "Original S union prime divisors of M0; ell excluded",
    "source_sha256": source_hashes,
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path)
args=parser.parse_args()
encoded=json.dumps(certificate,indent=2)+"\n"
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(encoded)
else:
    assert (HERE/"certificate.json").read_text()==encoded, "Committed certificate differs"
print(json.dumps({"status":"PASS","input_degree":8,"norm_field_d":d,
                  "prepared_valuations":[4,8,2],
                  "ell_denominator_residue":(1+A0*M0)%ell,
                  "count_reduction":False},indent=2))
