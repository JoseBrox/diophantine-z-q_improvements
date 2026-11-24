#!/usr/bin/env python3
"""Exact no-row-change CM-pole audit of the twelve-predicate abc table."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TABLE = ROOT / "undecidability/abc_pell_integrality_v108/c_integrality_abc_quadrics.json"
TABLE_SHA = "4cacba002f7537c2c3732fadb00f7961dffc9bfc7fc91ef42740a903bc9b1eb7"


def expression(row, names):
    return s.expand(sum(s.sympify(t["coefficient"]) * s.prod(s.Symbol(names[i - 1]) for i in t["monomial"])
                        for t in row["terms"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    raw = TABLE.read_bytes()
    assert sha256(raw).hexdigest() == TABLE_SHA
    table = json.loads(raw)
    assert table["variables"] == 605 and len(table["residuals"]) == 528
    assert table["integer_blocks"] == 12
    names = table["variable_names"]
    rows = {r["name"]: expression(r, names) for r in table["residuals"]}
    roles = ["i" if x == "i_half" else x for x in table["ordinary_integer_inputs"]]
    assert len(roles) == 12 and "c" not in roles
    checked, maps = [], {}
    for role in roles:
        prefix = "int_i_reciprocal" if role == "i" else "int_" + role
        z = lambda i: s.Symbol(prefix + "_" + str(i))
        c, eps, tau, beta = z(43), z(44), z(33), z(34)
        es, us, vs, p, q, P, R = z(35), z(36), z(38), z(37), z(39), z(40), z(41)
        expected = {
            f"integer.{role}.detector0.pole.pSquare": p * p - c * P,
            f"integer.{role}.detector0.pole.qSquare": q * q - c * R,
            f"integer.{role}.detector0.pole.first": beta * P + es * es - eps * eps,
            f"integer.{role}.detector0.pole.factor": beta * es - es * eps + us * vs,
            f"integer.{role}.detector0.pole.second": beta * R - us * us + vs * vs,
            f"integer.{role}.shared.unit": c * eps - 1,
            f"integer.{role}.single.poleInput": beta - 7 * tau * tau,
        }
        for name, poly in expected.items():
            assert rows[name] == s.expand(poly), name
            checked.append(name)
        # No private auxiliary has an outside inverse or other hidden guard.
        private_names = {str(z(i)) for i in (34, 35, 36, 37, 38, 39, 40, 41)}
        actual = {name for name, poly in rows.items() if {str(x) for x in poly.free_symbols} & private_names}
        assert actual <= set(expected)
        maps[role] = {"chart_unit": str(c), "unit_inverse": str(eps), "normalizer": str(tau),
                      "physical_input": f"{c}*{beta}=7*{c}*{tau}^2",
                      "physical_e": f"{c}*{es}", "physical_u": f"{c}*{us}",
                      "physical_v": f"{c}*{vs}", "physical_p": str(p), "physical_q": str(q)}
    assert len(checked) == 84

    # Universal reconstruction, independent of the serialized variable names.
    c = s.Symbol("c", nonzero=True)
    b, e, u, v, p, q = s.symbols("b e u v p q")
    stored_first = (b / c) * (p * p / c) + (e / c) ** 2 - 1 / c ** 2
    stored_factor = (b / c) * (e / c) - (e / c) / c + (u / c) * (v / c)
    stored_second = (b / c) * (q * q / c) - (u / c) ** 2 + (v / c) ** 2
    assert s.cancel(c * c * stored_first - (e * e + b * p * p - 1)) == 0
    assert s.cancel(c * c * stored_factor - (u * v - e * (1 - b))) == 0
    assert s.cancel(c * c * stored_second - (b * q * q - u * u + v * v)) == 0
    # The stored chart divides solely by c; p,q,e,u,v may be zero.
    d, aa, bb, n, UU, VV = s.symbols("d aa bb n UU VV", nonzero=True)
    e0 = n / (d * aa ** 2)
    p0 = UU / (d ** 2 * aa ** 2)
    u0 = bb / aa
    v0 = e0 * (1 - d) / u0
    q0 = VV / (d ** 2 * aa * bb)
    curve1 = UU ** 2 - d ** 3 * aa ** 4 + d * n ** 2
    curve2 = VV ** 2 - d ** 3 * bb ** 4 + d * n ** 2 * (1 - d) ** 2
    assert s.cancel(e0 ** 2 + d * p0 ** 2 - 1 - curve1 / (d ** 3 * aa ** 4)) == 0
    assert s.cancel(e0 * (1 - d) - u0 * v0) == 0
    assert s.cancel(u0 ** 2 - v0 ** 2 - d * q0 ** 2 + curve2 / (d ** 3 * aa ** 2 * bb ** 2)) == 0
    # Prepared example from the two explicit BB points, and the allowed k=1 branch.
    d0, aa0, bb0, n0 = Q(112, 225), Q(15, 2), Q(29, 2), Q(21)
    UU0, VV0 = Q(196, 15), Q(247940, 3375)
    assert UU0 ** 2 == d0 ** 3 * aa0 ** 4 - d0 * n0 ** 2
    assert VV0 ** 2 == d0 ** 3 * bb0 ** 4 - d0 * n0 ** 2 * (1 - d0) ** 2
    fixture = (n0 / (d0 * aa0 ** 2), UU0 / (d0 ** 2 * aa0 ** 2), bb0 / aa0,
               (n0 / (d0 * aa0 ** 2)) * (1 - d0) / (bb0 / aa0), VV0 / (d0 ** 2 * aa0 * bb0))
    ee, pp, uu, vv, qq = fixture
    assert ee ** 2 + d0 * pp ** 2 == 1 and ee * (1 - d0) == uu * vv and uu ** 2 - vv ** 2 == d0 * qq ** 2
    dz, rz = Q(112, 841), Q(27, 29)
    assert 1 - dz == rz ** 2
    assert Q(1) ** 2 + dz * 0 ** 2 == 1 and 1 - dz == rz * rz and rz ** 2 - rz ** 2 == dz * 0 ** 2
    result = {
        "status": "PASS", "variables": 605, "quadratic_rows": 528,
        "table_sha256": TABLE_SHA, "table_modified": False,
        "pole_blocks": 12, "literal_rows_checked": 84,
        "physical_reconstruction_identities": 3, "two_point_recipe_identities": 3,
        "physical_input_scaling": "d=b=7*c*tau^2; no 7/9 rescaling",
        "prepared_two_point_fixture": {"b": str(d0), "e_p_u_v_q": [str(x) for x in fixture]},
        "zero_auxiliary_fixture": {"b": str(dz), "e": "1", "p": "0", "q": "0", "u": str(rz), "v": str(rz)},
        "chart_maps": maps, "checked_rows": checked,
        "old_non_cm_pole_realization_needed_for_this_table": False,
        "external_point_theorem": "Bhargava-Burungale, arXiv:2611.16130v2, Theorem 2.3, rational-point assertion",
        "preparation_source": "undecidability/abc_common_numerator_v103/common_numerator.tex, fixed-place and real preparation paragraph",
        "retained_nonpole_interfaces_and_jones_coding_required": True,
        "unconditional_rational_undecidability_claim": False,
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "README.md").read_bytes()).hexdigest(),
        "scope": "All twelve current pole blocks already are the CM pole equations. Exact row/coordinate audit and rational identities are checked; the cited BB theorem supplies prepared existence, and all non-pole arithmetic interfaces remain required.",
    }
    if args.write_certificate:
        (HERE / "certificate.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        assert result == json.loads((HERE / "certificate.json").read_text())
    print(json.dumps({k: result[k] for k in ("status", "variables", "quadratic_rows", "pole_blocks", "literal_rows_checked", "table_sha256", "table_modified")}))


if __name__ == "__main__":
    main()
