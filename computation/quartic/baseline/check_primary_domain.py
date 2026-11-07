#!/usr/bin/env python3
"""Independent complete audit of the 475-variable quartic.

No producer modules are imported.  The finite coefficient certificate is
separated from the arithmetic parity theorem, whose hypotheses are recorded.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product as cartesian_product
import json

from exact_arithmetic import read_terms, normalize, sos, sha, valuation
from exact_arithmetic import add, product, fm

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data/system485"
PACKAGE = HERE / "data/system475"


def equivalent(p, q):
    p = normalize(p)[0]
    q = normalize(q)[0]
    return p == q or p == {k: -a for k, a in q.items()}


def main():
    parent = json.loads((SOURCE / "residuals.json").read_text())
    parent_receipt = json.loads((SOURCE / "independent-verification.json").read_text())
    data = json.loads((PACKAGE / "residuals.json").read_text())
    poly = json.loads((PACKAGE / "polynomial.json").read_text())
    cert = json.loads((PACKAGE / "transformation-certificate.json").read_text())
    report = json.loads((PACKAGE / "construction-report.json").read_text())
    assert parent_receipt["status"] == "PASS"
    for name, digest in parent_receipt["sha256"].items():
        assert sha(SOURCE / name) == digest
    assert sha(SOURCE / "residuals.json") == "41ffbca6450dcbfae53fe982709dff923e1a80ce43963a26be1f5283861374bb"
    assert cert["baselineSha256"] == data["sourceSha256"] == sha(SOURCE / "residuals.json")
    assert len(parent["coordinates"]) == 485 and len(parent["residuals"]) == 454
    assert data["fixedParameter"] == poly["fixedParameter"] == parent["fixedParameter"] == {
        "name": "S", "value": "3^(2^26)", "coordinate": False}
    names = {c["name"]: c["id"] for c in parent["coordinates"]}
    rows = {r["name"]: (r["id"], read_terms(r["terms"])) for r in parent["residuals"]}
    removed = {names[f"V{i}.dxInverse.{j}"] for i in range(5) for j in (0, 1)}
    removed_rows = {rows[f"V{i}.dxInverse.definition.{j}"][0] for i in range(5) for j in (0, 1)}
    assert len(removed) == len(removed_rows) == 10
    assert set(cert["deletedParentCoordinates"]) == removed
    assert set(cert["deletedParentResiduals"]) == removed_rows
    occurrences = {}
    for v in removed:
        occurrences[v] = {r["id"] for r in parent["residuals"]
                          if any(v in term["monomial"] for term in r["terms"])}
        assert len(occurrences[v]) == 2 and occurrences[v] <= removed_rows
    for row in parent["residuals"]:
        if row["id"] not in removed_rows:
            assert not any(removed.intersection(t["monomial"]) for t in row["terms"])

    # Identify the omitted equations as inverse equations for the actual
    # abscissa differences, including the source compiler's coordinate scales.
    compiled_path = HERE / "source/blocked/compiled/compiled-ir.json"
    compiled = json.loads(compiled_path.read_text())
    raw_to_parent = {c["sourceId"]: c["id"] for c in parent["coordinates"]}
    def value(name):
        return {(tuple(raw_to_parent[v] for v in m), s): a
                for (m, s), a in read_terms(compiled["values"][name]["terms"]).items()}
    v = lambda coordinate: {((coordinate,), 0): Q(1)}
    one = {((), 0): Q(1)}
    point_names = ("H", "UA", "US", "UT", "UZ")
    root_names = (None, "A", "S", "T", "Z")
    for i, (primary, root) in enumerate(zip(point_names, root_names)):
        xx = [value(primary + f".x.{j}") for j in (0, 1)]
        xq = [{((), 0): Q(57, 8)}, {((), 0): Q(-7, 2)}] if i == 0 else [value(root + f".x.{j}") for j in (0, 1)]
        difference = [add((1, xx[j]), (-1, xq[j])) for j in (0, 1)]
        inverse = [v(names[f"V{i}.dxInverse.{j}"]) for j in (0, 1)]
        inv_eq = fm(difference, inverse)
        inv_eq[0] = add((1, inv_eq[0]), (-1, one))
        for j in (0, 1):
            assert equivalent(rows[f"V{i}.dxInverse.definition.{j}"][1], inv_eq[j])
        ff = [value(f"U{i}.f.{j}") for j in (0, 1)]
        assert ff == [v(names[f"U{i}.f.{j}"]) for j in (0, 1)]
        f_eq = fm(xx, ff)
        f_eq[0] = add((1, f_eq[0]), (-1, one))
        for j in (0, 1):
            assert equivalent(rows[f"U{i}.f.definition.{j}"][1], f_eq[j])

    # The scalar difference guard is deliberately retained, not inferred from
    # the primary parity argument.
    scalar_guard = {names[f"scalar.shiftedS.dxInverse.{j}"] for j in (0, 1)}
    assert scalar_guard.isdisjoint(removed)
    assert scalar_guard == set(cert["retainedScalarDifferenceGuard"])
    assert all(rows[f"scalar.shiftedS.dxInverse.definition.{j}"][0] not in removed_rows
               for j in (0, 1))

    product_ids = [names[f"heightProduct.sixTimes4096C{j}"] for j in (0, 1)]
    real_f = [names[f"U{i}.f.0"] for i in range(5)]
    scales = {k: Q(6) for k in product_ids} | {k: Q(32) for k in real_f}
    assert cert["oldCoordinateEqualsMultiplierTimesNew"] == {str(k): str(a) for k, a in scales.items()}
    renamed = {v: f"heightProduct.4096C{j}" for j, v in enumerate(product_ids)}
    renamed.update({v: f"U{i}.fRealOver32" for i, v in enumerate(real_f)})
    g = names["anchor.mergedPhysicalA"]
    renamed[g] = "anchor.parityAndEvenPrimaryValue"
    assert cert["changedParentCoordinateNames"] == {str(k): a for k, a in renamed.items()}
    f0, f1 = [names[f"Sscalar.f.{j}"] for j in (0, 1)]
    b0, b1 = product_ids
    old_anchor = {((f0, f0), 0): Q(6), ((f0, f1), 0): Q(6), ((f1, f1), 0): Q(-6),
                  ((g,), 0): Q(-6), ((b0, b0), 1): Q(1), ((b0, b1), 1): Q(1), ((b1, b1), 1): Q(-1)}
    replaced_row, actual_old_anchor = rows["anchor.mergedPhysicalA.definition"]
    assert cert["replacedParentResidual"] == replaced_row
    assert actual_old_anchor == old_anchor
    new_anchor = {((f0, f0), 0): Q(1), ((f0, f1), 0): Q(1), ((f1, f1), 0): Q(-1),
                  ((g,), 0): Q(-1), ((b0, b0), 1): Q(1), ((b0, b1), 1): Q(1), ((b1, b1), 1): Q(-1)}
    for k in real_f:
        new_anchor[((k, k), 1)] = Q(2)
    # The rescalings encode exactly T=sum(a_i^2)/512: 32^2/512=2.
    assert Q(32**2, 512) == 2
    assert Q(6 * 4096, 6) == 4096
    kept = [c for c in parent["coordinates"] if c["id"] not in removed]
    remap = {c["id"]: i for i, c in enumerate(kept)}
    assert cert["parentToNew"] == {str(k): a for k, a in remap.items()}
    expected_coordinates = [{"id": remap[c["id"]], "parentId": c["id"], "sourceId": c["sourceId"],
                             "name": renamed.get(c["id"], c["name"]), "kind": c["kind"]} for c in kept]
    assert data["coordinates"] == poly["coordinates"] == expected_coordinates
    assert len(kept) == 475 and remap[0] == 0
    survivors = [r for r in parent["residuals"] if r["id"] not in removed_rows]
    assert len(survivors) == len(data["residuals"]) == 444
    expected_rows = []
    for i, (old, new) in enumerate(zip(survivors, data["residuals"])):
        rid = old["id"]
        assert new["id"] == i and new["parentId"] == rid and new["sourceId"] == old["sourceId"]
        assert new["name"] == ("anchor.parityAndEvenPrimaryValue.definition" if rid == replaced_row else old["name"])
        if rid == replaced_row:
            p = new_anchor
        else:
            p = {}
            for (m, s), coefficient in read_terms(old["terms"]).items():
                for k in m:
                    coefficient *= scales.get(k, 1)
                p[(m, s)] = coefficient
        p = {(tuple(remap[k] for k in m), s): a for (m, s), a in p.items()}
        p, factor = normalize(p)
        assert factor == Q(cert["positivePrimitiveRowMultipliers"][str(rid)])
        assert p == read_terms(new["terms"])
        assert max(len(m) for m, s in p) <= 2
        expected_rows.append(p)
    assert set(cert["positivePrimitiveRowMultipliers"]) == {str(r["id"]) for r in survivors}

    # Independent all-coefficient expansion, using unordered pairs rather than
    # the producer's ordered-pair multiplication implementation.
    table = read_terms(poly["terms"])
    assert table == sos(expected_rows)
    assert max(len(m) for m, s in table) == 4
    assert {k for m, s in table for k in m} == set(range(475))
    assert table[((0, 0, 0, 0), 0)] == 1
    grouped = defaultdict(dict)
    for (m, s), a in table.items():
        assert a.denominator == 1 and 0 <= s <= 2
        grouped[m][s] = a.numerator
    anchor_u = remap[names["anchor.U"]]
    assert grouped[(anchor_u, anchor_u)] == {2: 64}
    others = [c for m, c in grouped.items() if m != (anchor_u, anchor_u)]
    second = max(abs(c.get(2, 0)) for c in others)
    lower = max(abs(c.get(0, 0)) + abs(c.get(1, 0)) for c in others)
    assert second == report["otherQuadraticSCoefficientsAtMost"] == 8
    assert lower.bit_length() == report["lowerCoefficientEnvelopeBits"] == 1520
    assert lower.bit_length() < 2**26
    assert len(grouped) == report["ordinaryMonomials"] == 27987
    assert len(table) == report["coefficientParameterTerms"] == 27994
    assert report["totalVariables"] == 475 and report["existentialWitnesses"] == 474
    assert report["quadraticResiduals"] == 444 and report["degree"] == 4
    assert report["coefficientContent"] == 1 and report["exactCoefficientHeight"] == "64*3^(2^27)"
    for name, digest in report["sha256"].items():
        assert sha(PACKAGE / name) == digest

    # Finite local identities used in the written proof.  They do not replace
    # the formal-group valuation theorem or the inherited index identification.
    assert {a*a % 8 for a in (1, 3, 5, 7)} == {1}
    assert {(4*a)**2 % 16 for a in range(4)} == {0}
    parity_cases = []
    for mask in cartesian_product((0, 1), repeat=5):
        k = sum(mask)
        if k:
            expected = valuation(k, 2) - 3
            assert expected in (-3, -2, -1)
            assert all(valuation(k + 8*j, 2) - 3 == expected for j in range(8))
        else:
            expected = ">=1"
        parity_cases.append({"oddIndices": k, "valuationOfT": expected})
    for p in (2, 3):
        assert [(a, b) for a in range(p) for b in range(p)
                if (a*a+a*b-b*b) % p == 0] == [(0, 0)]
    receipt = {
        "status": "PASS",
        "independence": "No producer modules are imported. Uses only independently written sparse arithmetic and the frozen 485 audit receipt.",
        "totalVariables": 475, "existentialWitnesses": 474, "quadraticResiduals": 444,
        "degree": 4, "ordinaryMonomials": 27987, "coefficientParameterTerms": 27994,
        "coefficientContent": 1, "exactCoefficientHeight": "64*3^(2^27)",
        "heightProof": "The unique dominant coefficient is 64*S^2. Every other coefficient has |c2|<=8 and |c0|+|c1|<2^1520<S, so its absolute value is less than 9*S^2. The input fourth-power coefficient is 1.",
        "finiteChecks": ["all ten omitted inverse equations equal actual abscissa-difference inverse equations",
                         "all removed inverse coordinates occur only in their own two equations",
                         "all five primary real inverse-abscissa coordinates have the claimed semantic scale",
                         "the scalar subtraction inverse and its two defining equations remain",
                         "literal old and new merged anchor assignments",
                         "all seven invertible rational rescalings and every retained row",
                         "complete dense coordinate map and all primitive row multipliers",
                         "all 27994 coefficient-parameter terms, degree, active coordinates, content and exact height",
                         "all 32 five-index parity patterns and anisotropy of the binary form modulo 2 and 3"],
        "projectionScope": "Exact equivalence to the parent source restricted to even primary indices, under the separately proved parity-anchor theorem and inherited elliptic index identification. Input projection is unchanged because the original completeness construction chooses h divisible by 64 and U_i=[h*n_i]P. It is not claimed that every old auxiliary solution has even primary indices.",
        "arithmeticProof": "../../../../papers/quartic/quartic_20261107_v7.pdf",
        "parentAuditSha256": sha(SOURCE / "independent-verification.json"),
        "sha256": {name: sha(PACKAGE / name) for name in
                   ("residuals.json", "polynomial.json", "transformation-certificate.json", "construction-report.json")}}
    (PACKAGE / "independent-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
