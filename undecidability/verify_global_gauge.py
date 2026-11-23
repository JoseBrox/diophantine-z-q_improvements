#!/usr/bin/env python3
"""Read-only exact audit of the global-contact quadratic checkpoints.

This checker independently reconstructs every retained or replacement row.
It also verifies the physical gate identities, the complete occurrence lists
for deleted/redefined registers, the field-chart identity, the product map,
the coordinate census, the degree, and the explicit conditional status.
Arithmetic hypotheses and U_em are not certified by a coefficient check.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import hashlib
import json
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "undecidability/code"))
from build_global_gauge import build


# Written independently as the first coordinate of each field pair. The
# products at128 and130 have their NEW meanings: products of common factors.
PAIRS = [15, 17, 19, 64, 150, 23, 33, 54, 102, 182, 184, 186,
         194, 35, 39, 43, 41, 46, 48, 50, 66, 68, 70, 72,
         213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 233, 235,
         201, 205, 610, 120, 122, 124, 128, 130]
theta = sp.Symbol("theta")


def field_components(expr):
    p = sp.Poly(sp.expand(expr), theta)
    reduced = sp.rem(p, sp.Poly(theta**2 - 2, theta)).as_expr().expand()
    return reduced.coeff(theta, 0), reduced.coeff(theta, 1)


def check_chart_identity():
    s, t, F, G, eta, d, D = sp.symbols("s t F G eta d D")
    r1 = d - F * (eta + s + t)
    r3 = D * (F + G) - (s - t) * eta + t**2
    r4 = d * (s - t) - D * F * G - 1
    assert sp.expand(r4 - (s - t) * r1 + F * r3
                     - (F*s**2 + D*F**2 - 1)) == 0
    # This is a polynomial identity; no private denominator or genericity
    # hypothesis is hidden in either direction of the chart replacement.


def check(m, coordinate_count, row_count, duplicate_count):
    folder = ROOT / "undecidability/coefficients/jones1980_global_gauge"
    path = folder / f"global_gauge_m{m}_quadrics.json"
    raw = path.read_bytes()
    new = json.loads(raw)
    cert = json.loads((folder / f"global_gauge_m{m}_certificate.json").read_bytes())
    rebuilt = build(m, ROOT)
    assert raw == (json.dumps(rebuilt, separators=(",", ":"), sort_keys=True) + "\n").encode()
    assert cert["table_sha256"] == hashlib.sha256(raw).hexdigest()
    for doc in (new, cert):
        assert doc["source_universality_hypothesis"] == "U_em"
        assert doc["source_universality_verified"] is False
        assert doc["unconditional_undecidability_claim"] is False
    assert cert["new_abc_assumption"] is False
    assert new["variables"] == cert["variables"] == coordinate_count
    assert len(new["residuals"]) == cert["quadratic_rows"] == row_count

    old_path = ROOT / f"undecidability/coefficients/jones1980_common_points/common_points_m{m}_quadrics.json"
    old_bytes = old_path.read_bytes()
    old = json.loads(old_bytes)
    assert new["global_gauge_predecessor_sha256"] == hashlib.sha256(old_bytes).hexdigest()
    assert cert["predecessor_sha256"] == hashlib.sha256(old_bytes).hexdigest()
    maps = json.loads((ROOT / f"computation/variable_reductions_v82/general/quartic{m}/maps.json").read_text())
    source = json.loads((ROOT / f"computation/variable_reductions_v82/general/source{m}.json").read_text())
    labels = {int(j): slot for j, slot in maps["source_labels"].items()}
    common_pairs = PAIRS + ([190] if m == 179 else [])
    common = sorted([j for start in common_pairs for j in (start, start+1)] + [400, 401, 402])
    assert len(common) == len(set(common)) == (91 if m == 163 else 93)
    assert sorted(new["global_shared_source_labels"]) == common
    assert all(maps["R_weights"][str(j)] == 0 for j in common if j < 400 or j > 402)
    assert maps["R_weights"]["190"] == (-1 if m == 163 else 0)
    assert maps["R_weights"]["191"] == (-1 if m == 163 else 0)
    for j in [300] + ([301] if m == 179 else []):
        assert maps["c_weights"][str(j)] == 2
        assert maps["R_weights"][str(j)] == 0
    for j in (201, 202, 203, 204, 205, 206, 209, 210):
        assert maps["c_weights"][str(j)] == maps["R_weights"][str(j)] == 0
    for j in (207, 208, 211, 212):
        assert maps["c_weights"][str(j)] == 1
        assert maps["R_weights"][str(j)] == 0

    oldnames = old["variable_names"]
    newnames = new["variable_names"]
    assert len(newnames) == len(set(newnames)) == coordinate_count
    blocks = old["ordinary_integer_inputs"] + ["i_reciprocal"]
    assert len(blocks) == 12
    rename = {f"int_{b}_{labels[j]}": f"int_b_{labels[j]}"
              for b in blocks if b != "b" for j in common}
    rename = {a: b for a, b in rename.items() if a in oldnames}

    def slot(b, j):
        if j == 620:
            return sp.Symbol(f"int_{b}_last_contact_weight")
        n = f"int_{b}_{labels[j]}"
        if n not in oldnames:
            n = f"int_b_{labels[j]}"
        return sp.Symbol(rename.get(n, n))

    def fp(b, j):
        return slot(b, j) + theta * slot(b, j+1)

    def oldexpr(row):
        return sp.expand(sum(sp.sympify(term["coefficient"])
                    * sp.prod(sp.Symbol(rename.get(oldnames[j-1], oldnames[j-1]))
                              for j in term["monomial"])
                    for term in row["terms"]))

    def newexpr(row):
        return sp.expand(sum(sp.sympify(term["coefficient"])
                    * sp.prod(sp.Symbol(newnames[j-1]) for j in term["monomial"])
                    for term in row["terms"]))

    c, ci, ci2 = (slot("b", j) for j in (400, 401, 402))
    weights = [slot(b, j) for b in blocks
               for j in ([300, 620] if m == 163 else [300, 301, 620])]
    gone = slot("i_reciprocal", 620)
    replacement = ci - sum(q for q in weights if q != gone)
    assert sp.expand(sum(weights).subs(gone, replacement) - ci) == 0
    assert len(weights) == new["global_contact_weights"] == (24 if m == 163 else 36)
    assert gone not in set(map(sp.Symbol, newnames))

    # Complete occurrence audit: the removed field appears only in the four
    # old pair equations, while each redefined product occurs only in its chain.
    pair_names = {f"new1.{stem}.{j}" for stem in ("d_piF", "sum", "d_Gh", "unit") for j in (0, 1)}
    product_names = {f"amplified.det0.product{k}.{j}.definition" for k in (1, 2, 3) for j in (0, 1)}
    for row in old["residuals"]:
        terms = {oldnames[j-1] for term in row["terms"] for j in term["monomial"]}
        for b in blocks:
            if terms & {f"int_{b}_{labels[j]}" for j in (211, 212)}:
                assert row["name"].split(".", 2)[2] in pair_names
            if terms & {f"int_{b}_{labels[j]}" for j in (128, 129, 130, 131)}:
                assert row["name"].split(".", 2)[2] in product_names
    removed_d = {f"int_{b}_{labels[j]}" for b in blocks for j in (211, 212)}
    assert set(new["global_input_chart_removed_coordinates"]) == removed_d
    assert not removed_d.intersection(newnames)

    # New last-contact equations, independently written in their exact stored
    # scales. Their physical provenance is checked immediately below.
    last = 1 if m == 163 else 2
    b_id, n_id, inv_id = (96, 95, 311) if m == 163 else (582, 581, 312)
    gate_names = {f"balanced.detector{last}.poleInput.definition",
                  f"shared.inverse{last}", f"shared.gate{last}"}

    def new_gate(b):
        q, pole, nr, inv, error = (slot(b, j) for j in (620, b_id, n_id, inv_id, 305))
        result = {
            f"balanced.detector{last}.poleInput.definition": 167281*pole*(ci2+q)-166464*nr**2,
            f"shared.inverse{last}": ci*ci2-inv*q,
        }
        if m == 163:
            result[f"shared.gate{last}"] = 2*nr*ci2-error**2-inv*ci+2*ci*ci2-ci2**2-ci2*q
        else:
            result[f"shared.gate{last}"] = 2*nr*ci-error**2-inv*c+2*ci-ci2-q
        return result

    pc = sp.Symbol("physical_c", nonzero=True)
    px = {j: sp.Symbol(f"X{j}") for j in labels}
    px[620] = sp.Symbol("X620")
    physical = {
        f"balanced.detector{last}.poleInput.definition": 167281*pc*px[b_id]*(1+px[620])-166464*pc**2*px[n_id]**2,
        f"shared.inverse{last}": pc-px[620]*px[inv_id],
        f"shared.gate{last}": 2*pc*px[n_id]-1-px[305]**2-pc*px[inv_id]+2*pc-px[620],
    }
    original = {row["name"]: row for row in source["rows"]}
    qlast = pc-px[300]-(px[301] if m == 179 else 0)
    cw = {int(j): w for j, w in maps["c_weights"].items()}
    cw[620] = 2
    back = {slot("b", j): px[j]*pc**(-cw[j]) for j in [620, b_id, n_id, inv_id, 305]}
    back.update({c: pc, ci: 1/pc, ci2: 1/pc**2})
    for name, expression in new_gate("b").items():
        hc, hr = maps["row_c_R_weights"][name]
        assert hr == maps["row_parameter_weights"][name] == 0
        assert sp.cancel(expression.xreplace(back)*pc**hc-physical[name]) == 0
        oldphysical = sum(sp.Rational(t["coefficient"])*pc**t["c_power"]
                          *sp.prod(px[j] for j in t["monomial"])
                          for t in original[name]["terms"])
        assert sp.expand(physical[name].subs(px[620], qlast)-oldphysical) == 0

    expected = {}
    for row in old["residuals"]:
        n = row["name"]
        if n.startswith("integer."):
            _, label, local = n.split(".", 2)
            b = "i_reciprocal" if label == "i" else label
            if local in pair_names | product_names:
                continue
            expected[n] = new_gate(b)[local] if local in gate_names else oldexpr(row)
        else:
            expected[n] = oldexpr(row)

    F = fp("b", 205)
    s = fp("b", 201)
    Fhat = sp.Symbol("common_input_F_over_c_real") + theta*sp.Symbol("common_input_F_over_c_imag")
    xU = sp.Symbol("common_input_x_real") + theta*sp.Symbol("common_input_x_imag")
    D = 11 - 6*theta
    common_eqs = {
        "global.common_input.scale": F-c*Fhat,
        "global.common_input.unit": F*xU-1,
        "global.common_input.curve": xU-s**2-D*F,
    }
    for b in blocks:
        t, G, eta = (fp(b, j) for j in (203, 207, 209))
        equations = {
            f"global.{b}.input_pair.product": Fhat*(eta+s+t)-eta*G,
            f"global.{b}.input_pair.sum": D*(F+c*G)-(s-t)*eta+t**2,
        }
        f0, f1, f2, f3, A, B, W = (fp(b, j) for j in (118, 120, 122, 124, 128, 130, 302))
        equations.update({
            f"global.{b}.factor_product1": f1*f2-A*ci2,
            f"global.{b}.factor_product2": A*f3-B*ci2,
            f"global.{b}.factor_product3": f0*B-W*ci2,
        })
        for name, expr in equations.items():
            for j, component in enumerate(field_components(expr)):
                expected[f"{name}.{j}"] = component
    for name, expr in common_eqs.items():
        for j, component in enumerate(field_components(expr)):
            expected[f"{name}.{j}"] = component
    expected = {n: sp.expand(e.subs(gone, replacement)) for n, e in expected.items()}

    rows = {row["name"]: row for row in new["residuals"]}
    duplicates = {d["name"]: d["identical_to"] for d in new["global_duplicate_rows_removed"]}
    assert len(rows) == row_count
    assert len(duplicates) == cert["duplicate_rows_removed"] == duplicate_count
    assert set(rows).isdisjoint(duplicates)
    assert set(rows) | set(duplicates) == set(expected)
    for name, expression in expected.items():
        retained = duplicates.get(name, name)
        assert retained in rows
        assert sp.expand(expression-newexpr(rows[retained])) == 0, (m, name)

    # The reordered product has exactly the old W, including its contact scale.
    c0, f0, f1, f2, f3 = sp.symbols("c0 f0 f1 f2 f3", nonzero=True)
    oldA = c0**2*f0*f1
    oldB = c0**2*oldA*f2
    oldW = c0**2*oldB*f3
    newA = c0**2*f1*f2
    newB = c0**2*newA*f3
    newW = c0**2*f0*newB
    assert sp.expand(oldW-newW) == 0

    used = {j for row in rows.values() for term in row["terms"] for j in term["monomial"]}
    assert used == set(range(1, coordinate_count+1))
    assert max(len(term["monomial"]) for row in rows.values() for term in row["terms"]) == 2
    parameters = set(map(sp.Symbol, new["parameters"]))
    for row in rows.values():
        for term in row["terms"]:
            a = sp.sympify(term["coefficient"])
            assert a.free_symbols <= parameters
            assert (sp.Poly(a, *sorted(a.free_symbols, key=str)).domain == sp.ZZ
                    if a.free_symbols else a.is_Integer)
    assert any(sp.expand(newexpr(row) - (c*ci-1)) == 0 for row in rows.values())
    # A sum of real squares of nonzero quadratic leading forms has degree4.
    assert cert["degree"] == 4
    assert coordinate_count == 251 + 12*(m-1) - len(common)*11 + 11 - 24 + 4
    assert row_count == len(old["residuals"]) - 42 - duplicate_count
    print(f"m={m}: PASS, {coordinate_count} coordinates, {row_count} quadrics, "
          f"{len(common)} common source coordinates; U_em remains unverified")


if __name__ == "__main__":
    check_chart_identity()
    check(163, 1185, 1095, 462)
    check(179, 1355, 1241, 528)
