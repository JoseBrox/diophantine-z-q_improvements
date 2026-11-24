#!/usr/bin/env python3
"""Compile the common-numerator reciprocal-product compression for abc."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "undecidability/pell_signed_branch_v101/signed_branch_abc_quadrics.json"
COMMON = [f"abc_numerator_{x}{i}" for x in ("J", "E", "K") for i in range(2)]


def compact(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def build_data(old):
    labels = old["ordinary_integer_inputs"]
    assert len(labels) == old["integer_blocks"] == 13
    names = old["variable_names"]
    oldrows = {r["name"]: r for r in old["residuals"]}
    prefixes = {x: "int_i_reciprocal" if x == "i" else "int_" + x for x in labels}
    removed = [f"{prefixes[x]}_{i}" for x in labels for i in (21, 22, 23, 24)]
    private = {x: [f"abc_numerator_{x}_L{i}" for i in range(2)] for x in labels}
    newnames = [x for x in names if x not in removed] + sum(private.values(), []) + COMMON
    ids = {x: i + 1 for i, x in enumerate(newnames)}

    def decode(row):
        return {tuple(names[i - 1] for i in t["monomial"]): t["coefficient"] for t in row["terms"]}

    def encode(name, p):
        p = {tuple(sorted(m)): c for m, c in p.items() if c}
        den = lcm(*(Fraction(c).denominator for c in p.values()))
        content = gcd(*(abs(int(Fraction(c) * den)) for c in p.values()))
        factor = Fraction(den, content)
        row = {"name": name, "terms": sorted([
            {"coefficient": str(Fraction(c) * factor), "monomial": sorted(ids[v] for v in m)}
            for m, c in p.items()], key=lambda t: t["monomial"])}
        assert all(len(t["monomial"]) <= 2 for t in row["terms"])
        return row, str(factor)

    changed, multipliers, occurrences = {}, {}, {}
    for x in labels:
        pre, L = prefixes[x], private[x]
        uv = [f"{pre}_{i}" for i in (21, 22, 23, 24)]
        b2, b4 = f"{pre}_29", f"{pre}_30"
        for v in uv:
            occurrences[v] = [r["name"] for r in old["residuals"]
                              if any(v == names[i - 1] for t in r["terms"] for i in t["monomial"])]
        for component in range(2):
            # The first row's old +/- fields have sum 2*X^2*J.
            # Precompute E=v*J once, so no cubic coefficient occurs.
            name = f"integer.{x}.product.first.{component}"
            p = {m: Fraction(c) for m, c in decode(oldrows[name]).items() if not set(m).intersection(uv)}
            p[tuple(sorted((b2, COMMON[2 + component])))] = -2 if component == 0 else 2
            changed[name], multipliers[name] = encode(name, p)

            # Their difference is 2*L; the common J contribution cancels.
            name = f"integer.{x}.product.second.{component}"
            replacements = {uv[0]: (L[0], 1), uv[1]: (L[1], 1),
                            uv[2]: (L[0], -1), uv[3]: (L[1], -1)}
            p = defaultdict(Fraction)
            for m, c in decode(oldrows[name]).items():
                mm, cc = [], Fraction(c)
                for v in m:
                    nv, sign = replacements.get(v, (v, 1))
                    mm.append(nv)
                    cc *= sign
                p[tuple(sorted(mm))] += cc
            changed[name], multipliers[name] = encode(name, p)

            # (X^2 J+L)(X^2 J-L)=X^4 K-L^2, K=J^2.
            name = f"integer.{x}.product{component}"
            p = {m: Fraction(c) for m, c in decode(oldrows[name]).items() if not set(m).intersection(uv)}
            p[tuple(sorted((b4, COMMON[4 + component])))] = 1
            if component == 0:
                p[(L[0], L[0])], p[(L[1], L[1])] = -1, -2
            else:
                p[(L[0], L[1])] = -2
            changed[name], multipliers[name] = encode(name, p)
        expected = {f"integer.{x}.product.{side}.{j}" for side in ("first", "second") for j in range(2)}
        expected |= {f"integer.{x}.product{j}" for j in range(2)}
        assert set(n for v in uv for n in occurrences[v]) == expected

    rows = []
    for row in old["residuals"]:
        if row["name"] in changed:
            rows.append(changed[row["name"]])
        else:
            rows.append({"name": row["name"], "terms": [
                {"coefficient": t["coefficient"], "monomial": sorted(ids[names[i - 1]] for i in t["monomial"])}
                for t in row["terms"]]})
    j0, j1, e0, e1, k0, k1 = COMMON
    v0, v1 = "int_b_6", "int_b_7"
    commonrows = {
        "abc.common_numerator.E0": {(e0,): 1, tuple(sorted((v0, j0))): -1, tuple(sorted((v1, j1))): -2},
        "abc.common_numerator.E1": {(e1,): 1, tuple(sorted((v0, j1))): -1, tuple(sorted((v1, j0))): -1},
        "abc.common_numerator.K0": {(k0,): 1, (j0, j0): -1, (j1, j1): -2},
        "abc.common_numerator.K1": {(k1,): 1, (j0, j1): -2},
    }
    rows.extend(encode(name, p)[0] for name, p in commonrows.items())
    new = dict(old)
    new.update({
        "variables": len(newnames), "variable_names": newnames, "residuals": rows,
        "abc_common_numerator_proof": "undecidability/abc_common_numerator_v103/common_numerator.tex",
        "abc_common_numerator_removed_coordinates": removed,
        "abc_common_numerator_private_coordinates": private,
        "abc_common_numerator_shared_coordinates": COMMON,
        "abc_common_numerator_changed_rows": list(changed),
        "abc_common_numerator_added_rows": list(commonrows),
        "abc_common_numerator_row_multipliers": multipliers,
        "abc_common_numerator_occurrences": occurrences,
        "abc_common_numerator_savings": {"coordinates": 2 * len(labels) - 6, "added_quadratic_rows": 4},
        "abc_common_numerator_reconstruction": "Old U_i=X_i^2*J+L_i and old V_i=X_i^2*J-L_i, with E=v_H*J and K=J^2; field basis 1,sqrt(2).",
        "abc_common_numerator_arithmetic_completion": "One physical numerator U=[j]R0 and V_i=U-[n_i]R0, by the inherited all-sign prime-order CRT and arbitrary prime-power refinement; current fixed dyadic contact translations are retained.",
        "abc_common_numerator_zero_set_scope": "Exact polynomial lift to the entire predecessor for every rational zero. Completeness is on the instance projection, by reselecting common-numerator elliptic witnesses for every nonzero integer tuple.",
        "abc_common_numerator_no_new_arithmetic_premise": True,
        "abc_common_numerator_retained_pole_interface": "The ordinary-abc 56-coordinate interface, including its existing pole realization, is unchanged.",
        "unconditional_undecidability_claim": False,
    })
    assert len(newnames) == old["variables"] - 20 == 675
    assert len(rows) == len(old["residuals"]) + 4 == 594
    assert {i for row in rows for t in row["terms"] for i in t["monomial"]} == set(ids.values())
    return new


def main():
    source = PREDECESSOR.read_bytes()
    new = build_data(json.loads(source))
    new["abc_common_numerator_predecessor"] = str(PREDECESSOR.relative_to(ROOT))
    new["abc_common_numerator_predecessor_sha256"] = sha256(source).hexdigest()
    raw = compact(new)
    (HERE / "common_numerator_abc_quadrics.json").write_bytes(raw)
    cert = {"variables": new["variables"], "quadratic_rows": len(new["residuals"]), "degree": 4,
            "table_sha256": sha256(raw).hexdigest(), "integer_blocks": new["integer_blocks"],
            "ordinary_integer_inputs": new["ordinary_integer_inputs"],
            "source_coding_theorem": new["source_coding_theorem"],
            "source_coding_theorem_independently_reproved": False,
            "source_universality_hypothesis": None, "unconditional_undecidability_claim": False,
            **{k: v for k, v in new.items() if k.startswith("abc_common_numerator_")}}
    (HERE / "common_numerator_abc_certificate.json").write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: cert[k] for k in ("variables", "quadratic_rows", "degree", "table_sha256")}))


if __name__ == "__main__":
    main()
