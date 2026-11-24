#!/usr/bin/env python3
"""Compile the common numerator with directly scaled private point fields."""
from __future__ import annotations

from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "undecidability/odd_pell_quotient_v104/odd_quotient_abc_quadrics.json"
ROLES = ["b", "g", "t", "m", "w", "s", "h", "c", "gamma", "j", "i", "power_delta", "power_alpha"]
SHARED = [f"abc_point_{role}{i}" for role in ("S", "F", "S2", "SH", "sigma", "SF") for i in range(2)]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b, strict=True))


def mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scale(a, c):
    return tuple(c * x for x in a)


def bar(a):
    return a[0], -a[1]


def field(prefix):
    return tuple(sp.Symbol(f"{prefix}{i}") for i in range(2))


def expression(row, names):
    return sp.expand(sum(sp.sympify(t["coefficient"]) * sp.prod(sp.Symbol(names[i - 1]) for i in t["monomial"])
                         for t in row["terms"]))


def encode(name, expression, ids):
    expression = sp.expand(expression)
    symbols = sorted(expression.free_symbols, key=str)
    entries = sp.Poly(expression, *symbols).terms()
    denominator = lcm(*(int(c.q) for _, c in entries))
    content = gcd(*(abs(int(c * denominator)) for _, c in entries))
    multiplier = sp.Rational(denominator, content)
    terms = []
    for powers, coefficient in entries:
        monomial = sorted(ids[str(s)] for s, n in zip(symbols, powers, strict=True) for _ in range(n))
        assert len(monomial) <= 2
        terms.append({"coefficient": str(coefficient * multiplier), "monomial": monomial})
    return {"name": name, "terms": sorted(terms, key=lambda t: t["monomial"])}, str(multiplier)


def build_data(old):
    old_names = old["variable_names"]
    oldrows = {r["name"]: r for r in old["residuals"]}
    assert old["variables"] == 674 and len(oldrows) == 593
    assert old["ordinary_integer_inputs"] == ["i_half" if r == "i" else r for r in ROLES]
    prefixes = {r: "int_i_reciprocal" if r == "i" else f"int_{r}" for r in ROLES}
    removed = [f"{prefixes[r]}_{i}" for r in ROLES for i in (9, 10, 13, 14, 15, 16, 19, 20)]
    removed += ["abc_numerator_E0", "abc_numerator_E1"]
    private = {r: [f"abc_scaled_pair_{r}_{kind}{i}" for kind in ("G", "Z") for i in range(2)] +
                  [f"abc_scaled_pair_{r}_weight"] for r in ROLES}
    names = [n for n in old_names if n not in removed] + sum(private.values(), []) + SHARED
    ids = {n: i + 1 for i, n in enumerate(names)}
    z = sp.Symbol
    S, F, S2, SH, sigma, SF = [field(f"abc_point_{r}") for r in ("S", "F", "S2", "SH", "sigma", "SF")]
    J = field("abc_numerator_J")
    R, T, v = [(z(f"int_b_{i}"), z(f"int_b_{i + 1}")) for i in (2, 4, 6)]
    delta, kappa, a_inverse = (sp.Integer(11), sp.Integer(-6)), (sp.Integer(4), sp.Integer(-2)), (sp.Integer(-1), sp.Integer(1))
    u = mul(a_inverse, sub(sub(v, kappa), R))
    w = mul(a_inverse, sub(add(v, T), kappa))
    drop_rows = {"abc.common_numerator.E0", "abc.common_numerator.E1"}
    replacements, new_expressions, occurrences = {}, {}, {}

    def put_field(prefix, values):
        for i in range(2):
            new_expressions[prefix + str(i)] = values[i]

    for role in ROLES:
        prefix = prefixes[role]
        input_name = "i_half" if role == "i" else role
        X, X2 = z(input_name), z(prefix + "_29")
        c, epsilon, trace = z(prefix + "_43"), z(prefix + "_44"), z(prefix + "_8")
        T, H = [(z(prefix + f"_{i}"), z(prefix + f"_{i+1}")) for i in (11, 17)]
        G, Z = [field(f"abc_scaled_pair_{role}_{r}") for r in ("G", "Z")]
        weight = z(f"abc_scaled_pair_{role}_weight")
        L = field(f"abc_numerator_{role}_L")
        put_field(f"abc.scaled_point.{role}.first.", sub(add(mul(add(H, T), F), scale(SF, X)), mul(G, H)))
        put_field(f"abc.scaled_point.{role}.secant.", add(add(sub(scale(mul(delta, add(F, G)), X2), mul(S, Z)), mul(T, H)), mul(T, T)))
        new_expressions[f"abc.scaled_point.{role}.trace"] = trace - add(add(mul(H, H), mul(S, Z)), mul(H, T))[0]
        put_field(f"abc.scaled_point.{role}.scaled_chord.", sub(Z, scale(H, X)))
        new_expressions[f"abc.scaled_point.{role}.weight"] = weight - c * X2
        put_field(f"abc.scaled_point.{role}.reciprocal.", sub(mul(sigma, bar(L)), scale(G, weight)))
        old_C = [f"integer.{role}.C{i}" for i in range(2)]
        P = (z(prefix + "_25"), z(prefix + "_26"))
        Q = (z(prefix + "_27"), z(prefix + "_28"))
        c_square = add(sub(scale(S2, X2), scale(SH, 2 * X)), mul(R, R))
        c_rows = sub(scale(c_square, 2), add(P, scale(Q, c)))
        for name, row in zip(old_C, c_rows, strict=True):
            replacements[name] = row
        for name in oldrows:
            if name.startswith(f"integer.{role}.pair.") or name.startswith(f"integer.{role}.product.first.") or name.startswith(f"integer.{role}.product.second."):
                drop_rows.add(name)
    for name in removed:
        occurrences[name] = [r["name"] for r in old["residuals"]
                             if any(old_names[i - 1] == name for t in r["terms"] for i in t["monomial"])]
        assert set(occurrences[name]) <= drop_rows | set(replacements), (name, occurrences[name])
    put_field("abc.point_common.numerator_product.", sub(mul(u, F), mul(v, J)))
    put_field("abc.point_common.S2.", sub(S2, mul(S, S)))
    put_field("abc.point_common.SH.", sub(SH, mul(S, R)))
    put_field("abc.point_common.curve.", sub(add(mul(F, S2), mul(delta, mul(F, F))), (1, 0)))
    put_field("abc.point_common.sigma.", sub(mul(w, sigma), v))
    put_field("abc.point_common.SF.", sub(SF, mul(S, F)))
    rows, multipliers = [], {}
    for row in old["residuals"]:
        name = row["name"]
        if name in drop_rows:
            continue
        if name in replacements:
            newrow, multiplier = encode(name, replacements[name], ids)
            rows.append(newrow)
            multipliers[name] = multiplier
        else:
            rows.append({"name": name, "terms": [
                {"coefficient": t["coefficient"], "monomial": sorted(ids[old_names[i - 1]] for i in t["monomial"])}
                for t in row["terms"]]})
    for name, poly in new_expressions.items():
        newrow, multiplier = encode(name, poly, ids)
        rows.append(newrow)
        multipliers[name] = multiplier
    new = dict(old)
    new.update({
        "variables": len(names), "variable_names": names, "residuals": rows,
        "abc_scaled_point_proof": "undecidability/abc_scaled_point_v106/scaled_private_points.tex",
        "abc_scaled_point_removed_coordinates": removed,
        "abc_scaled_point_private_coordinates": private,
        "abc_scaled_point_shared_coordinates": SHARED,
        "abc_scaled_point_deleted_rows": sorted(drop_rows),
        "abc_scaled_point_changed_rows": list(replacements),
        "abc_scaled_point_added_rows": list(new_expressions),
        "abc_scaled_point_row_multipliers": multipliers,
        "abc_scaled_point_occurrences": occurrences,
        "abc_scaled_point_savings": {"coordinates": 29, "quadratic_rows": 29},
        "abc_scaled_point_reconstruction": "old s_i=X_i*S; old F_i=X_i^2*F; old G_i=weight_i*G_i; old h_i=retained H_i; old t_i=retained T_i; old d_i=weight_i*G_i*H_i; old E=v_H*J. The retained half-trace is Re(H_i^2+S*Z_i+H_i*T_i) with Z_i=X_i*H_i. No input division is used.",
        "abc_scaled_point_common_units": "Shared F(S^2+Delta*F)=1 implies F!=0. Existing reference chart implies u_H,w_H,v_H are units in Q(sqrt(2)), so sigma=v_H/w_H is defined. No extra unit coordinate.",
        "abc_scaled_point_arithmetic_completion": "Use the already proved common physical U and common reference H from v103, with private V_i=U-[n_i]R0. Set retained T_i=X_i*S_Vi, retained H_i=X_i*h_i, G_i=f(V_i), Z_i=X_i*H_i and weight_i=c_i*X_i^2.",
        "abc_scaled_point_zero_set_scope": "Every rational zero lifts directly to the complete v104 predecessor even when some X_i=0. Completeness is the same source-instance projection with reselected common numerator witnesses. The map is not asserted to factor through all v105 auxiliary fibers.",
        "abc_scaled_point_no_new_arithmetic_premise": True,
        "abc_scaled_point_input_nonzero_guards_added": 0,
        "abc_scaled_point_provenance": "Fresh reconstruction, not recovery of the unavailable earlier 649-coordinate artifact.",
        "unconditional_undecidability_claim": False,
    })
    assert len(removed) == 106 and sum(map(len, private.values())) + len(SHARED) == 77
    assert len(drop_rows) == 171 and len(replacements) == 26 and len(new_expressions) == 142
    assert len(names) == 645 and len(rows) == 564
    assert {i for row in rows for t in row["terms"] for i in t["monomial"]} == set(ids.values())
    return new


def main():
    source = PREDECESSOR.read_bytes()
    new = build_data(json.loads(source))
    new["abc_scaled_point_predecessor"] = str(PREDECESSOR.relative_to(ROOT))
    new["abc_scaled_point_predecessor_sha256"] = sha256(source).hexdigest()
    raw = (json.dumps(new, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (HERE / "scaled_point_abc_quadrics.json").write_bytes(raw)
    cert = {"variables": new["variables"], "quadratic_rows": len(new["residuals"]), "degree": 4,
            "table_sha256": sha256(raw).hexdigest(), "integer_blocks": new["integer_blocks"],
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "source_coding_theorem": new["source_coding_theorem"],
            "source_universality_hypothesis": None, "unconditional_undecidability_claim": False,
            **{k: v for k, v in new.items() if k.startswith("abc_scaled_point_")}}
    (HERE / "scaled_point_abc_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: cert[k] for k in ("variables", "quadratic_rows", "degree", "table_sha256")}))


if __name__ == "__main__":
    main()
