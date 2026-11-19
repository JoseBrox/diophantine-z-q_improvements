#!/usr/bin/env python3
"""Reproduce the preferred 180-variable fixed member, without optimization.

Run build_enhanced.py and build_small_anchor.py first.  This producer applies
the published diagonal (245 on each contact-combination coordinate), writes
the five final artifacts, and uses only the Python standard library.  The
separate check_small_anchor.py does not import this producer.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd, prod
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "enhanced/180"
BASE = SOURCE / "anchor_plain"
FINAL = SOURCE / "anchor_scaled"


def read(path):
    return json.loads(path.read_text())


def compact_write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def expanded_terms(poly):
    return [
        {"monomial": list(monomial), "coefficient": str(coefficient)}
        for monomial, coefficient in sorted(poly.items())
    ]


def main():
    source = read(SOURCE / "quadrics.json")
    base = read(BASE / "quadrics.json")
    maps = read(BASE / "maps.json")
    anchor = read(BASE / "certificate.json")
    roles = {entry["source_id"]: entry["id"] for entry in source["coordinates"]}
    permutation = {int(i): j for i, j in maps["permutation"].items()}
    assert permutation[1] == 1

    # Physical contact triples are (root, root-square, combination).
    # Derive the published final coordinates, rather than assume their order.
    triples = [
        [permutation[roles[i]] for i in physical]
        for physical in [(74, 75, 76), (87, 88, 89), (574, 575, 576)]
    ]
    assert triples == [[79, 83, 134], [80, 84, 135], [82, 85, 137]]
    scales = {
        i: factor
        for triple in triples
        for i, factor in zip(triple, (1, 1, 245))
    }
    assert scales.get(1, 1) == 1

    rows = []
    for row in base["residuals"]:
        transformed = {
            tuple(term["monomial"]): int(term["coefficient"])
            * prod(scales.get(i, 1) for i in term["monomial"])
            for term in row["terms"]
        }
        divisor = gcd(*transformed.values())
        assert divisor > 0
        rows.append({m: a // divisor for m, a in transformed.items()})

    polynomial = defaultdict(int)
    for row in rows:
        for left, a in row.items():
            for right, b in row.items():
                polynomial[tuple(sorted(left + right))] += a * b
    polynomial = {m: a for m, a in polynomial.items() if a}
    height = max(map(abs, polynomial.values()))
    assert base["variables"] == 180 and len(rows) == 152
    assert max(map(len, polynomial)) == 4 and polynomial[(1, 1, 1, 1)] == 1
    assert len(polynomial) == 2850
    assert height == 16 * int(anchor["U"]) ** 2
    assert height == 206625078319751697390503348692624

    result = {
        **base,
        "residuals": [
            {**old, "terms": expanded_terms(row)}
            for old, row in zip(base["residuals"], rows)
        ],
    }
    FINAL.mkdir(parents=True, exist_ok=True)
    compact_write(FINAL / "quadrics.json", result)
    compact_write(
        FINAL / "polynomial.json",
        {"variables": 180, "inputCoordinate": 1, "terms": expanded_terms(polynomial)},
    )
    scaling = {
        "parent": "../anchor_plain",
        "scaling": {str(i): str(factor) for i, factor in scales.items()},
        "height": str(height),
        "height_bits": height.bit_length(),
        "monomials": len(polynomial),
        "r_scale": "1",
        "v_scale": "245",
    }
    (FINAL / "scaling.json").write_text(json.dumps(scaling, indent=2) + "\n")

    parts = []
    for monomial, coefficient in sorted(polynomial.items()):
        factors = [str(abs(coefficient))] if abs(coefficient) != 1 or not monomial else []
        factors.extend(
            "x" + str(i) + ("^" + str(exponent) if exponent > 1 else "")
            for i, exponent in sorted(Counter(monomial).items())
        )
        parts.append(("-" if coefficient < 0 else "+" if parts else "") + "*".join(factors))
    literal = "".join(parts)
    assert len(literal) == 59084
    literal_hash = sha256(literal.encode()).hexdigest()
    assert literal_hash == "5ee7330c9e2edd7d0f918fc692e7824089007ee0358e47079601e8aa9c8b4683"
    (FINAL / "quartic180.txt").write_text(literal)

    paths = [
        SOURCE / "quadrics.json",
        BASE / "maps.json",
        BASE / "certificate.json",
        FINAL / "scaling.json",
        FINAL / "quadrics.json",
        FINAL / "polynomial.json",
    ]
    left = 2**16 * (1 - Fraction(316 * 7, 10 * 12012))
    right = 350 * (53 + Fraction(158 * 7, 10))
    assert left > right and int(anchor["physical_anchor"]) ** 3 >= 2**316
    certificate = {
        "status": "PASS",
        "variables": 180,
        "quadrics": 152,
        "degree": 4,
        "monomials": len(polynomial),
        "height": str(height),
        "height_bits": height.bit_length(),
        "canonical_bytes": len(literal),
        "canonical_sha256": literal_hash,
        "anchor": anchor["physical_anchor"],
        "primes": anchor["primes"],
        "U": anchor["U"],
        "V": anchor["V"],
        "anchor_cube_at_least_2_power": 316,
        "delta_endpoint_left_over_2_300": str(left),
        "delta_endpoint_right_over_2_300": str(right),
        "strengthened_divisibilities": [
            "M_j^4 divides Delta",
            "M_j^3 divides nonzero input numerator",
        ],
        "arithmetic_scope": "Under the same effective source interfaces; sufficient fixed member certified by the strengthened endpoint proof",
        "input_hashes": {str(path.relative_to(HERE)): sha256(path.read_bytes()).hexdigest() for path in paths},
    }
    (FINAL / "certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({k: certificate[k] for k in ["variables", "degree", "monomials", "height_bits", "canonical_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
