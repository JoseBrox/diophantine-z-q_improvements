#!/usr/bin/env python3
"""Verify the monic finite-wrapper transfer and its numerical degree ledger.

The source universal equation is the published BDHMS Definition 5.3.
This checker verifies the new exact algebraic identities and dependence
conditions; the infinite arithmetic source theorems remain cited inputs.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "undecidability"
sys.path.insert(0, str(BASE / "code"))
from finite_algebra_encoder import degree_bound


def norm_identity():
    z, r1, r2, r3 = sp.symbols("z r1 r2 r3")
    a, b, c = sp.symbols("a b c")
    product = sp.Integer(1)
    for e1 in (-1, 1):
        for e2 in (-1, 1):
            for e3 in (-1, 1):
                product *= z + e1*r1 + e2*r2 + e3*r3
    raw = sp.Poly(sp.expand(product), r1, r2, r3)
    norm = sp.Integer(0)
    for exponents, coefficient in raw.terms():
        assert all(e % 2 == 0 for e in exponents)
        norm += coefficient * a**(exponents[0]//2) * b**(exponents[1]//2) * c**(exponents[2]//2)
    expression = ((z*z+c-a-b)**2+4*z*z*c-4*a*b)**2-16*z*z*c*(z*z+c-a-b)**2
    assert sp.expand(norm-expression) == 0
    polynomial = sp.Poly(expression, z)
    assert polynomial.degree() == 8 and polynomial.LC() == 1

    # The other arguments of the norm are independent of the source n.
    S, shift, n = sp.symbols("S shift n")
    source = sp.Poly(expression.subs(z, S*S*n+shift), n)
    assert source.degree() == 8 and sp.expand(source.LC()-S**16) == 0
    return {"radical_free_formula": "PASS", "monic_degree": 8,
            "source_degree_in_n": 8, "source_leading_coefficient": "S^16",
            "method": "Expanded eight-sign product, exact even-exponent reduction, symbolic polynomial comparison."}


def wrapper_identity():
    S, s, t, xi, m = sp.symbols("S s t xi m")
    relation = xi**2+S*xi+S*S*(s*s+t*t)-m
    recovered = S*S*(s*s+t*t+(xi/S)**2+xi/S)-m
    assert sp.cancel(recovered-relation) == 0
    completed = 4*m+S*S-(2*xi+S)**2-4*S*S*(s*s+t*t)
    assert sp.expand(completed+4*relation) == 0

    # The rank-sixteen basis uses a rank-eight companion matrix.
    coeff = sp.symbols("c0:8")
    M = sp.zeros(8)
    for j in range(7):
        M[j+1,j] = 1
    for j in range(8):
        M[j,7] = -coeff[j]
    O, I = sp.zeros(8), sp.eye(8)
    X = sp.BlockMatrix([[O, M-S*S*(s*s+t*t)*I], [I, -S*I]]).as_explicit()
    MM = sp.diag(M, M)
    assert all(sp.expand(e) == 0 for e in X*MM-MM*X)
    check = X*X+S*X+S*S*(s*s+t*t)*sp.eye(16)-MM
    assert all(sp.expand(e) == 0 for e in check)
    # A degree-eight monic in m composed with monic quadratic in xi
    # is monic of degree sixteen; use arbitrary coefficient symbols.
    monic = m**8+sum(coeff[j]*m**j for j in range(8))
    composite = sp.Poly(monic.subs(m, xi**2+S*xi+S*S*(s*s+t*t)), xi)
    assert composite.degree() == 16 and composite.LC() == 1
    return {"recovered_wrapper_identity": "PASS", "completed_square_identity": "PASS",
            "rank_multiplier": 16, "wrapper_separating_generators": ["xi"],
            "xi_multiplication_matrix_relation": "PASS",
            "monic_composite_degree": 16}


def source_dependencies(document):
    nodes = document["coefficient_dag"]
    inputs = {v["index"] for v in document["variables"] if v["category"] == "retained.input"}
    assert len(inputs) == 9
    terminal = {b["variable"] for b in document["finite_blocks"] if b["kind"] == "pole"}
    dependence = []
    for op, *args in nodes:
        if op == "variable":
            mask = (1 if args[0] in inputs else 0) | (2 if args[0] in terminal else 0)
        elif op in ("int", "parameter"):
            mask = 0
        elif op == "pow":
            mask = dependence[args[0]]
        elif op in ("add", "mul", "neg"):
            mask = 0
            for child in args:
                mask |= dependence[child]
        else:
            raise AssertionError(op)
        dependence.append(mask)
    points = [b for b in document["finite_blocks"] if b["kind"] == "point_block"]
    poles = [b for b in document["finite_blocks"] if b["kind"] == "pole"]
    for point in points:
        for name in ("A", "B"):
            f = point[name]
            assert nodes[f["denominator"]] == ["int", 1]
            assert dependence[f["numerator"]] == 0
    for pole in poles:
        assert pole["monic"] is True and pole["degree"] == 2
        coefficients = pole["coefficient_nodes_ascending"]
        assert len(coefficients) == 2 and nodes[coefficients[1]] == ["int", 0]
        assert all(not(dependence[j] & 2) for j in coefficients)
    assert all(not(dependence[j] & 2) for j in document["guard_numerators"])
    return {"input_count": len(inputs), "point_blocks": len(points),
            "point_coefficients_independent_of_all_inputs": True,
            "point_coefficient_denominators_equal_one": True,
            "pole_coefficients_and_guards_independent_of_terminal_roots": True}


def verify():
    report = json.loads((BASE / "certificates/common_numerator_transfers.json").read_text())
    assert report["status"] == "PASS"
    delta = 15616+233856*4+(233952*4+467712*4**2)*9**59
    assert delta < 2**211
    outputs = {}
    expected_variables = {"general25": 82, "explicit27": 100, "abc11": 52}
    expected_bits = {"general25": 650, "explicit27": 714, "abc11": 500}
    for route, old in report["routes"].items():
        path = BASE / "common_numerator_sources" / route / "common_source.json.gz"
        data = gzip.decompress(path.read_bytes())
        sha = hashlib.sha256(data).hexdigest()
        assert sha == old["joint_source_sha256"]
        document = json.loads(data)
        dependence = source_dependencies(document)
        dg = old["guard_multiplication_degree_bound"]
        dt = old["maximum_generator_multiplication_degree_bound"]
        assert dt >= 2
        assert old["gamma_multiplication_degree_bound"] == dg+dt
        r = 16*int(old["finite_algebra_rank"])
        ell = old["gamma_count"]+1  # xi also generates m.
        guard = dg*(2*delta+1)+delta
        theta = dt*(2*delta+1)
        assert theta >= 2*delta+2
        d = guard+theta
        assert d == (dg+dt)*(2*delta+1)+delta
        degree = degree_bound(r, ell, d)
        variables = old["variables"]-1
        assert variables == expected_variables[route]
        assert degree.bit_length() == expected_bits[route]
        assert degree < 2**expected_bits[route]
        outputs[route] = {
            "rational_variables": variables,
            "ordinary_coordinates_before_final_encoder": variables-1,
            "integer_predicates_retained": 9,
            "source_common_numerator_sha256": sha,
            "source_dependencies": dependence,
            "finite_algebra_rank_exponent_base2": r.bit_length()-1,
            "finite_algebra_rank": str(r),
            "guarded_separator_count": ell,
            "guard_multiplication_degree_upper_bound": str(guard),
            "maximum_generator_multiplication_degree_upper_bound": str(theta),
            "gamma_multiplication_degree_upper_bound": str(d),
            "final_polynomial_degree_upper_bound": str(degree),
            "final_degree_strictly_less_than_power2": expected_bits[route],
            "external_wrapper_degree_multiplier": 1,
            "abc_required": route == "abc11",
        }
    return {
        "status": "PASS",
        "norm_identity": norm_identity(),
        "wrapper_identity": wrapper_identity(),
        "source_degree_bound_delta": str(delta),
        "routes": outputs,
        "degree_formula": "2*r*(J+1)*(1+d*(1+2*J*(1+ell*(J+1)))), J=ell*(r+1)^2",
        "scope": "Exact new algebraic identities, actual point/terminal dependencies, and numerical ledgers; source universality and integer-predicate arithmetic remain the cited theorems and retained premises.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    options = parser.parse_args()
    result = verify()
    output = json.dumps(result, indent=2)+"\n"
    if options.report:
        options.report.parent.mkdir(parents=True, exist_ok=True)
        options.report.write_text(output)
    print(output, end="")
