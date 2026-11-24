#!/usr/bin/env python3
"""Independent field-polynomial interpretation and complete lift audit."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
rho = s.Symbol("rho")


def reduce_field(expression):
    return s.rem(s.Poly(s.expand(expression), rho), s.Poly(rho ** 2 - 2, rho)).as_expr().expand()


def components(expression):
    p = s.Poly(reduce_field(expression), rho)
    return [p.nth(0), p.nth(1)]


def element(prefix):
    return s.Symbol(prefix + "0") + rho * s.Symbol(prefix + "1")


def conjugate(expression):
    return reduce_field(expression.subs(rho, -rho))


def expression(row, names):
    return s.expand(sum(s.sympify(t["coefficient"]) * s.prod(s.Symbol(names[i - 1]) for i in t["monomial"])
                        for t in row["terms"]))


def proportional(actual, expected):
    actual, expected = s.expand(actual), s.expand(expected)
    symbols = sorted(actual.free_symbols | expected.free_symbols, key=str)
    a, b = s.Poly(actual, *symbols), s.Poly(expected, *symbols)
    assert a.monoms() == b.monoms(), (actual, expected)
    multiplier = s.cancel(a.coeffs()[0] / b.coeffs()[0])
    assert multiplier.is_Rational and multiplier != 0
    assert s.expand(actual - multiplier * expected) == 0
    return multiplier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    raw = (HERE / "scaled_point_abc_quadrics.json").read_bytes()
    new = json.loads(raw)
    cert = json.loads((HERE / "scaled_point_abc_certificate.json").read_bytes())
    oldraw = (ROOT / new["abc_scaled_point_predecessor"]).read_bytes()
    old = json.loads(oldraw)
    assert sha256(raw).hexdigest() == cert["table_sha256"]
    assert sha256(oldraw).hexdigest() == new["abc_scaled_point_predecessor_sha256"]
    assert old["variables"] == 674 and len(old["residuals"]) == 593
    assert new["variables"] == cert["variables"] == len(new["variable_names"]) == 645
    assert len(new["residuals"]) == cert["quadratic_rows"] == 564
    names, old_names = new["variable_names"], old["variable_names"]
    oldrows = {r["name"]: expression(r, old_names) for r in old["residuals"]}
    newrows = {r["name"]: expression(r, names) for r in new["residuals"]}
    z = s.Symbol
    S, F, SS, SR, sigma, SF = [element("abc_point_" + a) for a in ("S", "F", "S2", "SH", "sigma", "SF")]
    J = element("abc_numerator_J")
    E = element("abc_numerator_E")
    R, T, v = [z(f"int_b_{i}") + rho * z(f"int_b_{i + 1}") for i in (2, 4, 6)]
    u = reduce_field((rho - 1) * (v - (4 - 2 * rho) - R))
    w = reduce_field((rho - 1) * (v - (4 - 2 * rho) + T))
    Delta = 11 - 6 * rho
    expected_new, expected_old, replaced, dropped = {}, {}, set(), set()

    def put(target, name, field_expression):
        for i, c in enumerate(components(field_expression)):
            target[name + str(i)] = c

    roles = ["b", "g", "t", "m", "w", "s", "h", "c", "gamma", "j", "i", "power_delta", "power_alpha"]
    assert new["ordinary_integer_inputs"] == old["ordinary_integer_inputs"] == ["i_half" if q == "i" else q for q in roles]
    assert new["integer_blocks"] == old["integer_blocks"] == 13
    removed, private = [], []
    for role in roles:
        pre = "int_i_reciprocal" if role == "i" else "int_" + role
        field_old = lambda i: z(f"{pre}_{i}") + rho * z(f"{pre}_{i + 1}")
        sold, told, Fold, Gold, hold, dold = [field_old(i) for i in (9, 11, 13, 15, 17, 19)]
        trace, X2, X4, c, epsilon = [z(f"{pre}_{i}") for i in (8, 29, 30, 43, 44)]
        X = z("i_half" if role == "i" else role)
        piold = hold + sold + told
        expected_old[f"integer.{role}.pair.differenceReal"] = trace - components(hold * piold)[0]
        put(expected_old, f"integer.{role}.pair.firstProduct.", piold * Fold - dold * epsilon)
        put(expected_old, f"integer.{role}.pair.secondProduct.", Gold * hold - dold)
        put(expected_old, f"integer.{role}.pair.secant.", (sold - told) * hold - told ** 2 - Delta * (Fold + Gold * epsilon))
        put(expected_old, f"integer.{role}.pair.scale.", dold * (sold - told) - Delta * Fold * Gold - X4 * c)
        put(expected_old, f"integer.{role}.product.first.", u * Fold - X2 * E)
        L = element(f"abc_numerator_{role}_L")
        put(expected_old, f"integer.{role}.product.second.", v * conjugate(L) - w * Gold)
        P, Q = field_old(25), field_old(27)
        put(expected_old, f"integer.{role}.C", 2 * (sold - R) ** 2 - P - c * Q)
        replaced.update(f"integer.{role}.C{i}" for i in range(2))
        G, Z = [element(f"abc_scaled_pair_{role}_{a}") for a in ("G", "Z")]
        weight = z(f"abc_scaled_pair_{role}_weight")
        put(expected_new, f"abc.scaled_point.{role}.first.", (hold + told) * F + X * SF - G * hold)
        put(expected_new, f"abc.scaled_point.{role}.secant.", Delta * X2 * (F + G) - S * Z + told * hold + told ** 2)
        expected_new[f"abc.scaled_point.{role}.trace"] = trace - components(hold ** 2 + S * Z + hold * told)[0]
        put(expected_new, f"abc.scaled_point.{role}.scaled_chord.", Z - X * hold)
        expected_new[f"abc.scaled_point.{role}.weight"] = weight - c * X2
        put(expected_new, f"abc.scaled_point.{role}.reciprocal.", sigma * conjugate(L) - weight * G)
        put(expected_new, f"integer.{role}.C", 2 * (X2 * SS - 2 * X * SR + R ** 2) - P - c * Q)
        removed.extend(f"{pre}_{i}" for i in (9, 10, 13, 14, 15, 16, 19, 20))
        private.extend(f"abc_scaled_pair_{role}_{kind}{i}" for kind in ("G", "Z") for i in range(2))
        private.append(str(weight))
        # Every input-power equation and its actual source input remain unchanged.
        assert oldrows[f"integer.{role}.height.betaSquare"] == X ** 2 - X2
        assert oldrows[f"integer.{role}.height.betaFourth"] == X2 ** 2 - X4
        assert oldrows[f"integer.{role}.shared.unit"] == c * epsilon - 1
    put(expected_old, "abc.common_numerator.E", E - v * J)
    put(expected_new, "abc.point_common.numerator_product.", u * F - v * J)
    put(expected_new, "abc.point_common.S2.", SS - S ** 2)
    put(expected_new, "abc.point_common.SH.", SR - S * R)
    put(expected_new, "abc.point_common.curve.", F * SS + Delta * F ** 2 - 1)
    put(expected_new, "abc.point_common.sigma.", w * sigma - v)
    put(expected_new, "abc.point_common.SF.", SF - S * F)
    removed.extend(("abc_numerator_E0", "abc_numerator_E1"))
    dropped = set(expected_old) - replaced
    assert len(expected_old) == 197 and len(dropped) == 171 and len(replaced) == 26
    for name, p in expected_old.items():
        proportional(oldrows[name], p)
    for name, p in expected_new.items():
        multiplier = proportional(newrows[name], p)
        assert multiplier == s.Rational(new["abc_scaled_point_row_multipliers"][name])
    assert set(expected_new) == set(new["abc_scaled_point_added_rows"]) | replaced
    assert len(expected_new) == 168
    unchanged = set(oldrows) - set(expected_old)
    assert len(unchanged) == 396
    for name in unchanged:
        assert newrows[name] == oldrows[name], name
    assert set(newrows) == unchanged | set(expected_new)
    assert set(dropped) == set(new["abc_scaled_point_deleted_rows"])
    assert replaced == set(new["abc_scaled_point_changed_rows"])
    for variable in removed:
        actual = [name for name, p in oldrows.items() if z(variable) in p.free_symbols]
        assert actual == new["abc_scaled_point_occurrences"][variable]
        assert set(actual) <= set(expected_old)
    shared = [f"abc_point_{a}{i}" for a in ("S", "F", "S2", "SH", "sigma", "SF") for i in range(2)]
    assert set(removed) == set(new["abc_scaled_point_removed_coordinates"])
    assert set(names) == set(old_names).difference(removed) | set(private) | set(shared)

    # Universal certificate, independent of the serialized coordinate names.
    # Work in Q[rho]/(rho^2-2), with unrestricted symbolic field components.
    f, ss, tt, gg, hh, rr, jj, vv, ww, sig, ll, zz = [element("check_" + a) for a in ("f", "S", "T", "G", "H", "R", "J", "v", "w", "sigma", "L", "Z")]
    xx, cc, ee, weight = s.symbols("check_X check_c check_epsilon check_weight")
    A = (hh + xx * ss + tt) * f - gg * hh
    B = Delta * xx ** 2 * (f + gg) - (xx * ss - tt) * hh + tt ** 2
    C = f * ss ** 2 + Delta * f ** 2 - 1
    scale_row = gg * hh * (xx * ss - tt) - Delta * xx ** 2 * f * gg - xx ** 2
    assert reduce_field(scale_row - xx ** 2 * C + f * B + (xx * ss - tt) * A) == 0
    Cv = gg * tt ** 2 + Delta * xx ** 2 * gg ** 2 - xx ** 2
    assert reduce_field(Cv - xx ** 2 * C - (gg - f) * B + (xx * ss - tt) * A) == 0
    # The old first and second products and secant row are respectively
    # X^2*A, zero, and -B after the retained c*epsilon=1 is used.
    d_lift = cc * xx ** 2 * gg * hh
    assert reduce_field((hh + xx * ss + tt) * (xx ** 2 * f) - d_lift / cc - xx ** 2 * A) == 0
    assert reduce_field((cc * xx ** 2 * gg) * hh - d_lift) == 0
    old_secant = (xx * ss - tt) * hh - tt ** 2 - Delta * xx ** 2 * (f + gg)
    assert reduce_field(old_secant + B) == 0
    old_scale = d_lift * (xx * ss - tt) - Delta * xx ** 2 * f * cc * xx ** 2 * gg - xx ** 4 * cc
    assert reduce_field(old_scale - cc * xx ** 2 * scale_row) == 0
    assert reduce_field(hh * (hh + xx * ss + tt) - (hh ** 2 + ss * zz + hh * tt) - ss * (xx * hh - zz)) == 0
    # No division by X occurs in any lift. The reciprocal merge needs no
    # division even by the reference field elements in the soundness direction.
    target = vv * conjugate(ll) - ww * weight * gg
    combination = ww * (sig * conjugate(ll) - weight * gg) - (ww * sig - vv) * conjugate(ll)
    assert reduce_field(target - combination) == 0
    assert reduce_field((xx * ss - rr) ** 2 - (xx ** 2 * ss ** 2 - 2 * xx * ss * rr + rr ** 2)) == 0
    # The only denominator used above is c, already guarded by the unchanged
    # unit row. All actual old-coordinate reconstruction expressions are polynomial.
    parameters = [z(k) for k in new["parameters"]]
    used = set()
    for row in new["residuals"]:
        for t in row["terms"]:
            assert t["monomial"] == sorted(t["monomial"]) and len(t["monomial"]) <= 2
            used.update(t["monomial"])
            coef = s.sympify(t["coefficient"])
            assert coef.free_symbols <= set(parameters)
            assert s.Poly(coef, *parameters, domain=s.ZZ)
    assert used == set(range(1, 646))
    assert newrows["integer.b.height.betaSquare"] == z("b") ** 2 - z("int_b_29")
    assert new["source_coding_theorem"] == old["source_coding_theorem"]
    assert new["source_universality_hypothesis"] is None and new["unconditional_undecidability_claim"] is False
    assert new["abc_scaled_point_input_nonzero_guards_added"] == 0
    for k, value in cert.items():
        if k.startswith("abc_scaled_point_"):
            assert new[k] == value
    result = {"status": "PASS", "variables": 645, "quadratic_rows": 564, "degree": 4,
              "coordinates_saved": 29, "quadratic_rows_saved": 29,
              "old_row_interpretations_checked": 197, "new_or_changed_rows_checked": 168,
              "unchanged_rows_checked": 396, "integer_blocks_retained": 13,
              "removed_coordinates_occurrence_audited": 106,
              "universal_field_identities_checked": 9,
              "input_nonzero_guards_added": 0, "zero_input_fibers_soundness_preserved": True,
              "source_sha256": sha256(oldraw).hexdigest(), "table_sha256": sha256(raw).hexdigest(),
              "verification_scope": "Full source-row interpretations, new quadratic model, unchanged rows, occurrences, universal polynomial lift identities, coefficient domain, support, degree, counts and metadata. Arithmetic existence is inherited from the common physical numerator theorem; no numerical defining parameter or unconditional rational undecidability is certified."}
    if args.write_certificate:
        (HERE / "independent_verification.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
