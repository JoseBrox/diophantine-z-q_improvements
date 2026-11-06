#!/usr/bin/env python3
"""An exact 853-variable polynomial circuit, with no existential gate nodes.

Drop pole denominator guards implied over Q by their two cleared conics.
Combine the private scaled anchor and the Pell quadratic in one primitive
element, then use its reciprocal to enforce all remaining guards. The
855 and 854 producers and packages are left unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from build_compact_polynomial import Rational
from build_compact_854 import RecordingBuilder, children, coefficients_in_private_variable, dependence, prune


class PoleRecordingBuilder(RecordingBuilder):
    def __init__(self):
        super().__init__()
        self.poles = []

    def parity(self, b, label):
        self.poles.append((b, label))
        return super().parity(b, label)


def homogenized_substitution(c, count, variable, P, Q):
    """For each old H, output Q^d H(P/Q), with d its syntactic tau-degree.

    New outer nodes are deliberately raw arithmetic operations, so an
    independent reader can check this inductive polynomial certificate
    without expanding a large polynomial or importing the producer.
    """
    depends = dependence(c.nodes[:count], variable)
    images, degrees = [], []

    def qpower(exponent):
        return c.one if exponent == 0 else Q if exponent == 1 else c.node("pow", Q, exponent)

    for index in range(count):
        if not depends[index]:
            image, degree = index, 0
        else:
            op, *a = c.nodes[index]
            if op == "variable":
                assert a == [variable]
                image, degree = P, 1
            elif op == "neg":
                image, degree = c.node("neg", images[a[0]]), degrees[a[0]]
            elif op == "mul":
                image = c.node("mul", *(images[k] for k in a))
                degree = sum(degrees[k] for k in a)
            elif op == "pow":
                image = c.node("pow", images[a[0]], a[1])
                degree = degrees[a[0]]*a[1]
            elif op == "add":
                degree = max(degrees[k] for k in a)
                terms = [images[k] if degrees[k] == degree else
                         c.node("mul", images[k], qpower(degree-degrees[k])) for k in a]
                image = c.node("add", *terms)
            else:
                raise ValueError(op)
        images.append(image); degrees.append(degree)
    return images, degrees


def build():
    producer = PoleRecordingBuilder()
    parent = producer.build()
    c = producer.c
    parent_bytes = (json.dumps(parent, separators=(",", ":")) + "\n").encode()
    parent_count = len(c.nodes)
    by_name = {v["name"]: v["index"] for v in c.variables}
    u_index = by_name["anchor.u"]
    tau_index = by_name["proxy.t"]
    inverse_index = by_name["common denominator inverse"]
    private_indices = [by_name["anchor."+name] for name in ("u", "v", "w")]
    assert inverse_index == 854

    def variable(name):
        return Rational(c, c.node("variable", by_name[name]), c.one)

    old_anchor = next(r for r in c.equations if r["label"] == "packed semilocal anchor")
    old_pell = next(r for r in c.equations if r["label"] == "Lucas relation")
    other_rows = [r for r in c.equations if r is not old_anchor and r is not old_pell]
    assert len(other_rows) == 295

    removed_guards, pole_certificate = set(), []
    for b, label in producer.poles:
        t = variable(label+".t")
        delta = 1+b*t*t
        assert delta.n in c.guards and delta.n < parent_count
        removed_guards.add(delta.n)
        pole_certificate.append({
            "label": label,
            "argument_numerator_in_parent": b.n,
            "argument_denominator_in_parent": b.d,
            "removed_guard_in_parent": delta.n,
            "private_variable_indices_in_parent": [by_name[label+"."+name]
                                                   for name in ("t", "e", "p", "q", "s")],
        })
    assert len(removed_guards) == 42
    retained_guards = c.guards-removed_guards
    assert len(retained_guards) == 1639
    guard_factors = {a for guard in retained_guards for a in c.factors(guard)
                     if c.nodes[a][0] != "int"}
    assert len(guard_factors) == 1560
    G = c.from_factors({a: 1 for a in guard_factors})
    omitted_factors = {a for guard in removed_guards for a in c.factors(guard)
                       if c.nodes[a][0] != "int"}
    for row in c.equations:
        assert all(c.nodes[a][0] == "int" or a in guard_factors | omitted_factors
                   for a in c.factors(row["denominator"]))
    for b, label in producer.poles:
        assert all(c.nodes[a][0] == "int" or a in guard_factors for a in c.factors(b.d))
    for idx in [tau_index, *private_indices]:
        dep = dependence(c.nodes, idx)
        assert not dep[G] and not any(dep[g] for g in retained_guards)
    for idx in private_indices:
        dep = dependence(c.nodes, idx)
        assert not dep[old_anchor["denominator"]]
        assert not any(dep[row[key]] for row in other_rows+[old_pell]
                       for key in ("numerator", "denominator"))

    coeffs = coefficients_in_private_variable(c, old_anchor["numerator"], u_index)
    assert set(coeffs) <= {0, 2}
    N, B = coeffs[0], old_anchor["denominator"]
    assert c.factors(coeffs[2]) == c.factors(B)
    bf = c.factors(B)
    assert all(e % 2 == 0 for e in bf.values())
    S = c.from_factors({a: e//2 for a, e in bf.items()})
    assert all(c.nodes[a][0] == "int" or a in guard_factors for a in bf)
    f0, f1 = producer.anchor_arguments
    r = f0*f0+f0*f1-f1*f1
    assert c.factors(c.power(r.d, 2)) == bf
    C4 = c.power(c.node("int", 3), 2**26)

    s, z = variable("proxy.s"), variable("proxy.z")
    a = s*(s-2)*z
    b0 = (s-2)**2*z*z-1
    discriminant = a*a-4*b0
    assert a.d == b0.d == discriminant.d == c.one
    A, Delta = a.n, discriminant.n
    U = c.node("variable", u_index)
    two, four = c.node("int", 2), c.node("int", 4)
    plus = c.node("add", N, Delta)
    minus = c.node("add", N, c.node("neg", Delta))
    G2, G4 = c.node("pow", G, 2), c.node("pow", G, 4)
    U2, U4 = c.node("pow", U, 2), c.node("pow", U, 4)
    P = c.node("add", c.one, c.node("mul", two, A, G, U),
               c.node("mul", plus, G2, U2))
    Q = c.node("mul", four, G, U)
    psi = c.node("add", c.one, c.node("mul", two, minus, G2, U2),
                 c.node("mul", c.node("pow", plus, 2), G4, U4))
    dep = dependence(c.nodes, tau_index)
    assert not any(dep[k] for k in (N, B, G, A, Delta, P, Q, psi))

    images, degrees = homogenized_substitution(c, parent_count, tau_index, P, Q)
    rows = [{"label": row["label"], "numerator": images[row["numerator"]],
             "parent_numerator": row["numerator"], "parent_denominator": row["denominator"],
             "homogenizing_exponent": degrees[row["numerator"]]} for row in other_rows]
    final = c.node("add", *(c.node("pow", row["numerator"], 2) for row in rows),
                   c.node("pow", psi, 2))
    evidence = {
        "original_anchor_numerator": old_anchor["numerator"],
        "original_anchor_denominator": B,
        "anchor_A_numerator": N,
        "anchor_A_denominator": B,
        "anchor_u_squared_coefficient": coeffs[2],
        "anchor_denominator_square_root": S,
        "anchor_r_numerator": r.n,
        "anchor_r_denominator": r.d,
        "anchor_C_fourth_power": C4,
        "guard_product": G,
        "reciprocal_variable_node": U,
        "pell_linear_coefficient": A,
        "pell_constant_coefficient": b0.n,
        "pell_discriminant": Delta,
        "tau_numerator": P,
        "tau_denominator": Q,
        "psi": psi,
    }
    roots = [final, *retained_guards, *evidence.values(), *(r["numerator"] for r in rows)]
    nodes, renumber = prune(c.nodes, roots)
    deleted_variables = {tau_index, inverse_index}
    parent_variable_indices = [v["index"] for v in c.variables if v["index"] not in deleted_variables]
    variable_map = {old: new for new, old in enumerate(parent_variable_indices)}
    assert len(variable_map) == 853
    for node in nodes:
        if node[0] == "variable":
            assert node[1] in variable_map
            node[1] = variable_map[node[1]]
    variables = [dict(c.variables[old], index=new) for new, old in enumerate(parent_variable_indices)]
    variables[variable_map[u_index]]["name"] = "anchor.reciprocal_U"
    degree, bits = c.bounds[final]
    branches = parent["report"]["finite_branches"]
    report = {
        "total_variables": 853,
        "existential_witnesses": 852,
        "categories": dict(Counter(v["category"] for v in variables)),
        "point_charts": c.point_count,
        "pole_blocks": c.pole_count,
        "residuals_per_branch": len(rows)+1,
        "retained_nonzero_guards": len(retained_guards),
        "removed_redundant_pole_guards": len(removed_guards),
        "distinct_guard_factors": len(guard_factors),
        "template_nodes": len(nodes),
        "finite_branches": branches,
        "branch_degree_upper_bound": degree,
        "branch_coefficient_log2_upper_bound": bits,
        "degree_upper_bound": degree*branches,
        "coefficient_log2_upper_bound": bits*branches,
        "maximum_pell_substitution_exponent": max(row["homogenizing_exponent"] for row in rows),
        "bounds_are_upper_bounds_not_exact_expansion_statistics": True,
        "parent_855_circuit_sha256": hashlib.sha256(parent_bytes).hexdigest(),
        "scope": "Exact integer-polynomial circuit specification combining the private anchor and Pell quadratic after removing pole guards implied over Q. Arithmetic characterization inherits the source theorem; no global minimality claimed.",
    }
    return {
        "format": parent["format"],
        "source_commit": parent["source_commit"],
        "semantics": parent["semantics"],
        "variables": variables,
        "parent_variable_indices": parent_variable_indices,
        "nodes": nodes,
        "template_output": renumber[final],
        "finite_parameters": parent["finite_parameters"],
        "transformed_equations": [row | {"numerator": renumber[row["numerator"]]} for row in rows],
        "nonzero_numerators": sorted(renumber[g] for g in retained_guards),
        "guard_product_node": renumber[G],
        "removed_guard_nodes_in_parent": sorted(removed_guards),
        "pole_guard_certificate": pole_certificate,
        "quadratic_combination_certificate": {key: renumber[value] for key, value in evidence.items()} | {
            "private_anchor_variable_indices": [variable_map[i] for i in private_indices],
            "removed_pell_variable_index_in_parent": tau_index,
            "original_pell_numerator_in_parent": old_pell["numerator"],
        },
        "report": report,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    obj = build()
    raw = (json.dumps(obj, separators=(",", ":")) + "\n").encode()
    (args.output/"polynomial-circuit.json").write_bytes(raw)
    report = obj["report"] | {
        "circuit_sha256": hashlib.sha256(raw).hexdigest(),
        "circuit_bytes": len(raw),
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parent_producer_sha256": hashlib.sha256(Path(__file__).with_name("build_compact_polynomial.py").read_bytes()).hexdigest(),
    }
    (args.output/"construction-report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
