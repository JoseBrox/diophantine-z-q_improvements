#!/usr/bin/env python3
"""Independent full table and positive local-squareclass audit for 474 variables."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
import json

from exact_arithmetic import read_terms, normalize, sos, sha

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data/system475"
PACKAGE = HERE / "data/system474"
PRIMES = (2, 3, 5, 7, 11, 13, 17)


def local_vector(n):
    bits = []
    for p in (2, 3, 17):
        unit, exponent = n, 0
        while unit % p == 0:
            unit //= p
            exponent += 1
        bits.append(exponent % 2)
        if p == 2:
            # Unit basis (-1,5): 1,7,5,3 have bit pairs 00,10,01,11.
            bits.extend({1: (0, 0), 7: (1, 0), 5: (0, 1), 3: (1, 1)}[unit % 8])
        else:
            legendre = pow(unit % p, (p-1)//2, p)
            assert legendre in (1, p-1)
            bits.append(int(legendre == p-1))
    return tuple(bits)


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
    assert sha(SOURCE / "residuals.json") == "d24e7aa7ab64bc02280dadf051c33b9078c3dc6ad411a5866ed2e62758239850"
    assert data["sourceSha256"] == cert["baselineSha256"] == sha(SOURCE / "residuals.json")
    assert len(parent["coordinates"]) == 475 and len(parent["residuals"]) == 444
    names = {c["name"]: c["id"] for c in parent["coordinates"]}
    rows = {r["name"]: r for r in parent["residuals"]}
    sign = names["correction.partial.2"]
    signrow = rows["correction.initialSign"]["id"]
    inputrow = rows["inputSquare.definition"]["id"]
    y = names["inputSquare.quadratic"]
    assert cert["deletedParentCoordinate"] == sign
    assert cert["deletedParentResidual"] == signrow
    assert cert["replacedInputResidual"] == inputrow
    assert cert["specialization"] == {str(sign): "1"}
    assert read_terms(rows["correction.initialSign"]["terms"]) == {((), 0): Q(1), ((sign, sign), 0): Q(-1)}
    assert read_terms(rows["inputSquare.definition"]["terms"]) == {((0, 0), 0): Q(1), ((y,), 0): Q(-1)}
    occurrences = [r["id"] for r in parent["residuals"] if any(sign in t["monomial"] for t in r["terms"])]
    assert cert["signOccurrences"] == occurrences == [signrow, rows["correction.partialProduct1"]["id"]]
    # Audit all seven branch equations as (s_i-s_{i-1})(s_i-p_i*s_{i-1})=0.
    chain = [names[f"correction.partial.{p}"] for p in PRIMES] + [names["correction.partial.sign"]]
    assert chain[0] == sign
    for i, p in enumerate(PRIMES, 1):
        left, right = chain[i-1], chain[i]
        expected = {((left, left), 0): Q(p), ((left, right), 0): Q(-p-1), ((right, right), 0): Q(1)}
        assert read_terms(rows[f"correction.partialProduct{i}"]["terms"]) == expected
    # Exactly 128 positive products represent the entire seven-dimensional
    # product Q_2^*/squares x Q_3^*/squares x Q_17^*/squares.
    classes = {}
    for mask in product((0, 1), repeat=7):
        c = 1
        for p, bit in zip(PRIMES, mask):
            c *= p**bit
        vector = local_vector(c)
        assert vector not in classes
        classes[vector] = c
    assert set(classes) == set(product((0, 1), repeat=7))
    assert max(classes.values()) == 510510
    kept = [c for c in parent["coordinates"] if c["id"] != sign]
    remap = {c["id"]: i for i, c in enumerate(kept)}
    assert cert["parentToNew"] == {str(k): a for k, a in remap.items()}
    expected_coordinates = [{"id": remap[c["id"]], "parentId": c["id"], "sourceId": c["sourceId"],
                             "name": "inputSquarePlus1200" if c["id"] == y else c["name"], "kind": c["kind"]} for c in kept]
    assert data["coordinates"] == poly["coordinates"] == expected_coordinates
    assert len(kept) == 474 and remap[0] == 0
    survivors = [r for r in parent["residuals"] if r["id"] != signrow]
    expected_rows = []
    for i, (old, new) in enumerate(zip(survivors, data["residuals"])):
        assert new["id"] == i and new["parentId"] == old["id"] and new["sourceId"] == old["sourceId"]
        assert new["name"] == ("shiftedInputSquare.definition" if old["id"] == inputrow else old["name"])
        p = defaultdict(Q)
        for (m, s), a in read_terms(old["terms"]).items():
            p[(tuple(remap[k] for k in m if k != sign), s)] += a
        if old["id"] == inputrow:
            p[((), 0)] += Q(1200)
        p = {k: a for k, a in p.items() if a}
        p, factor = normalize(p)
        assert factor == Q(cert["positivePrimitiveRowMultipliers"][str(old["id"])])
        assert read_terms(new["terms"]) == p
        assert max(len(m) for m, s in p) <= 2
        expected_rows.append(p)
    assert len(expected_rows) == len(data["residuals"]) == 443
    assert set(cert["positivePrimitiveRowMultipliers"]) == {str(r["id"]) for r in survivors}
    assert data["fixedParameter"] == poly["fixedParameter"] == parent["fixedParameter"] == {"name": "S", "value": "3^(2^26)", "coordinate": False}
    table = read_terms(poly["terms"])
    assert table == sos(expected_rows)
    assert max(len(m) for m, s in table) == 4
    assert {k for m, s in table for k in m} == set(range(474))
    assert table[((0, 0, 0, 0), 0)] == 1
    grouped = defaultdict(dict)
    for (m, s), a in table.items():
        assert a.denominator == 1 and 0 <= s <= 2
        grouped[m][s] = a.numerator
    u = remap[names["anchor.U"]]
    assert grouped[(u, u)] == {2: 64}
    others = [c for m, c in grouped.items() if m != (u, u)]
    assert max(abs(c.get(2, 0)) for c in others) == report["otherQuadraticSCoefficientsAtMost"] == 8
    lower = max(abs(c.get(0, 0)) + abs(c.get(1, 0)) for c in others)
    assert lower.bit_length() == report["lowerCoefficientEnvelopeBits"] == 1520 < 2**26
    assert len(grouped) == report["ordinaryMonomials"] == 27986
    assert len(table) == report["coefficientParameterTerms"] == 27993
    assert report["totalVariables"] == 474 and report["existentialWitnesses"] == 473
    assert report["quadraticResiduals"] == 443 and report["degree"] == 4
    assert report["coefficientContent"] == 1 and report["exactCoefficientHeight"] == "64*3^(2^27)"
    for name, digest in report["sha256"].items():
        assert sha(PACKAGE / name) == digest
    receipt = {"status": "PASS", "independence": "No producer imports; exact substitution and every coefficient are recomputed using independent checker arithmetic.",
               "totalVariables": 474, "existentialWitnesses": 473, "quadraticResiduals": 443,
               "degree": 4, "ordinaryMonomials": 27986, "coefficientParameterTerms": 27993,
               "coefficientContent": 1, "exactCoefficientHeight": "64*3^(2^27)",
               "localCorrectionClasses": {"primes": list(PRIMES), "places": [2, 3, 17],
                                          "vectors": {str(p): local_vector(p) for p in PRIMES},
                                          "distinctPositiveProductClasses": len(classes), "fullDimension": 7},
               "finiteChecks": ["sole occurrences of the deleted sign coordinate and exact sign specialization",
                                "all seven prime-choice equations and all 128 positive local squareclasses",
                                "exact shifted input equation X^2+1200-Y=0",
                                "every retained row and dense coordinate map",
                                "all 27993 coefficient-parameter terms, degree, active coordinates, content and exact height"],
               "arithmeticScope": "The source soundness/completeness proof is applied with beta=2*X^2+2403. This map is integral iff X is integral, is odd on integers, and makes all five scalar contact factors positive. Positive local corrections therefore suffice. This check does not independently reprove the inherited Diophantine arithmetic theorem.",
               "arithmeticProof": "../../../../papers/quartic/quartic_20261107_v7.pdf",
               "parentAuditSha256": sha(SOURCE / "independent-verification.json"),
               "sha256": {name: sha(PACKAGE / name) for name in
                          ("residuals.json", "polynomial.json", "transformation-certificate.json", "construction-report.json")}}
    (PACKAGE / "independent-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
