#!/usr/bin/env python3
"""Independent exact checks of the final 1315, 1338, and 1335 quartic changes.

No producer is imported. Every residual, every expanded coefficient, the
coordinate maps, exact heights, and explicit Q(i) sections are checked.
The fixed symbol S is not evaluated as an enormous integer.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PARENTS = {
    "quartic-direct": "dbd50fdd3484df9aa27b0133406f644689f9bff776c34bf2fdad64494270a5ff",
    "quartic-direct-small-coefficients": "9486590b47c79aa4e37bf185dc278e2010567c3d98023785b6eb7bd6eeaa72e0",
}
OUTPUTS = {
    "quartic-direct-translated": "54175d125631269040f8a207b7863f7f8f9331db92bb9d9e95bbf12cc15c1a10",
    "quartic-direct-small-coefficients-1338": "69a280afdd6a98f6b13ac3b9455baf36b92cc3bd203d7664860269004baab0a8",
    "quartic-direct-small-coefficients-1335": "047ebb380d58179785ebe2d2e12c34e02594c01dab07afe242a80aa7455fd2b4",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load(name, expected):
    path = HERE / name / "polynomial.json.gz"
    raw = gzip.decompress(path.read_bytes())
    require(sha256(raw).hexdigest() == expected, "Changed artifact: " + name)
    return json.loads(raw)


def clean(poly):
    return {k: v for k, v in poly.items() if v}


def read(rows):
    result = {}
    for monomial, exponent, coefficient in rows:
        require(monomial == sorted(monomial) and type(exponent) is int and exponent >= 0
                and type(coefficient) is int and coefficient != 0, "Malformed sparse term")
        key = tuple(monomial), exponent
        require(key not in result, "Duplicate sparse term")
        result[key] = Fraction(coefficient)
    return result


def add(*polys):
    out = defaultdict(Fraction)
    for poly in polys:
        for key, value in poly.items(): out[key] += value
    return clean(out)


def scale(poly, scalar):
    return clean({key: scalar * value for key, value in poly.items()})


def multiply(a, b):
    out = defaultdict(Fraction)
    for (ma, ea), ca in a.items():
        for (mb, eb), cb in b.items():
            out[tuple(sorted(ma + mb)), ea + eb] += ca * cb
    return clean(out)


def variable(i):
    return {((i,), 0): Fraction(1)}


S = {((), 1): Fraction(1)}


def substitute(poly, mapping, coefficient_power=1):
    out = defaultdict(Fraction)
    for (monomial, exponent), coefficient in poly.items():
        term = {((), coefficient_power * exponent): coefficient}
        for i in monomial:
            term = multiply(term, mapping.get(i, variable(i)))
            if not term: break
        for key, value in term.items(): out[key] += value
    return clean(out)


def sum_of_squares(rows):
    out = defaultdict(Fraction)
    for row in rows:
        poly = read(row["terms"])
        for key, value in multiply(poly, poly).items(): out[key] += value
    return clean(out)


def basic_statistics(source, total, residual_count):
    require(len(source["variables"]) == total and len(source["residuals"]) == residual_count,
            "Wrong coordinate or residual count")
    require([v["index"] for v in source["variables"]] == list(range(total)), "Wrong coordinate enumeration")
    rows = [read(row["terms"]) for row in source["residuals"]]
    require(all(len(m) <= 2 for row in rows for m, e in row), "Residual degree exceeds two")
    poly = read(source["expanded_polynomial"])
    require(poly == sum_of_squares(source["residuals"]), "Full square expansion differs")
    require(max(len(m) for m, e in poly) == 4 and poly[((0, 0, 0, 0), 0)] == 1,
            "Exact degree or primitive coefficient fails")
    require({v for m, e in poly for v in m} == set(range(total)), "Unused or out-of-range coordinate")
    require(len({m for m, e in poly}) == len(poly), "Different fixed-symbol powers overlap")
    require(all(c.denominator == 1 for c in poly.values()), "Noninteger expanded coefficient")
    report = source["report"]
    require(report["total_variables"] == total and report["existential_witnesses"] == total - 1
            and report["quadratic_residuals"] == residual_count and report["total_degree"] == 4
            and report["encoded_coefficient_entries"] == len(poly)
            and report["distinct_variable_monomials"] == len(poly), "Incorrect output statistics")
    return poly


def gaussian_section(poly, total, pair, private_constants=None):
    keep = {0, *pair}
    mapping = {i: {} for i in range(total) if i not in keep}
    mapping.update(private_constants or {})
    restricted = substitute(poly, mapping)
    expected = {((0, 0, 0, 0), 0): Fraction(1), ((pair[0], pair[0]), 0): Fraction(1),
                ((pair[1], pair[1]), 0): Fraction(1)}
    constants = {k: v for k, v in restricted.items() if not k[0]}
    require(restricted == add(expected, constants), "Q(i) section has extra terms")
    return {"free_coordinate_pair": list(pair),
            "constant_terms": [[e, int(c)] for (m, e), c in sorted(constants.items())],
            "restriction": "X0^4+C(S)+a^2+b^2",
            "section": "Let A=X0^4+C(S); take a=(A-1)/2 and b=i*(A+1)/2."}


def translation():
    old = load("quartic-direct", PARENTS["quartic-direct"])
    new = load("quartic-direct-translated", OUTPUTS["quartic-direct-translated"])
    require(old["fixed_constants"] == {"K": "3^(2^28)"}
            and new["fixed_constants"] == {"S": "3^(2^27)"}, "Wrong fixed constants")
    for i in (55, 56, 57):
        uses = [r for r, row in enumerate(old["residuals"]) if any(i in m for m, e, c in row["terms"])]
        require(uses == [46], "Private coordinate occurs in another residual")
    require([r for r, row in enumerate(old["residuals"]) if any(e for m, e, c in row["terms"])] == [46],
            "Fixed kappa occurs in another residual")
    forward = {
        55: add(S, scale(variable(55), Fraction(1, 4)), scale(variable(56), Fraction(-3, 4)), scale(variable(57), Fraction(3, 4))),
        56: add(scale(S, Fraction(1, 2)), scale(variable(56), Fraction(1, 4))),
        57: add(scale(S, Fraction(3, 2)), scale(variable(57), Fraction(1, 4))),
    }
    inverse = {
        55: add(scale(variable(55), 4), scale(variable(56), 12), scale(variable(57), -12), scale(S, 8)),
        56: add(scale(variable(56), 4), scale(S, -2)),
        57: add(scale(variable(57), 4), scale(S, -6)),
    }
    for i in forward:
        require(substitute(forward[i], inverse) == variable(i)
                and substitute(inverse[i], forward) == variable(i), "Affine maps are not inverse")
    require(len(old["residuals"]) == len(new["residuals"]), "Translation changes row count")
    for i, (a, b) in enumerate(zip(old["residuals"], new["residuals"])):
        require(substitute(read(a["terms"]), forward, 2) == read(b["terms"]), "Wrong translated residual " + str(i))
    poly = basic_statistics(new, 1315, 1272)
    require(substitute(read(old["expanded_polynomial"]), forward, 2) == poly, "Full affine polynomial identity fails")
    powers = defaultdict(list)
    for (m, e), c in poly.items(): powers[e].append((m, int(c)))
    require(set(powers) == {0, 1, 2} and powers[2] == [((55, 55), 64)], "Wrong leading fixed-symbol coefficient")
    max_linear = max(abs(c) for m, c in powers[1])
    max_constant = max(abs(c) for m, c in powers[0])
    require(max_linear == 288 and max_constant < 2 ** 1020, "Coefficient-height component bound fails")
    # S>=9 makes 64*S^2 exceed 288*S; 64*S^2>2^(6+2^28) exceeds every constant coefficient.
    require(2 ** 27 >= 2 and 64 * 9 > max_linear and 6 + 2 ** 28 >= max_constant.bit_length(),
            "Exact height dominance fails")
    height_exponent = (6 * 5 + 8 * 2 ** 28 + 4) // 5
    require(3 ** 5 < 2 ** 8 and height_exponent == 429496736, "Binary height bound fails")
    section = gaussian_section(poly, 1315, (72, 73), {55: scale(S, 8), 56: scale(S, -2), 57: scale(S, -6)})
    return {"artifact": "quartic-direct-translated", "sha256": OUTPUTS["quartic-direct-translated"],
            "parent_sha256": PARENTS["quartic-direct"], "total_variables": 1315,
            "residuals_checked": 1272, "expanded_coefficients_checked": len(poly), "exact_degree": 4,
            "exact_primitive_height": "64*3^(2^28)", "strict_height_bound": "2^429496736",
            "affine_maps_inverse": True, "full_polynomial_substitution_identity": True,
            "field_scope": "Literal polynomial projection and conjunction preserved over every characteristic-zero field.",
            "Q_i_universal_section": section}


def elimination():
    old = load("quartic-direct-small-coefficients", PARENTS["quartic-direct-small-coefficients"])
    new = load("quartic-direct-small-coefficients-1338", OUTPUTS["quartic-direct-small-coefficients-1338"])
    require(old["fixed_constants"] == new["fixed_constants"] == {}, "Unexpected coefficient symbol")
    uses = [r for r, row in enumerate(old["residuals"]) if any(81 in m for m, e, c in row["terms"])]
    require(uses == [69, 70], "Eliminated coordinate has unrecorded occurrences")
    require(read(old["residuals"][69]["terms"]) == {((80, 80), 0): 1, ((81,), 0): -1}, "Wrong pivot equation")
    mapping = {i: variable(i - 1) for i in range(82, 1339)}
    mapping[81] = {((80, 80), 0): Fraction(1)}
    require(substitute(read(old["residuals"][69]["terms"]), mapping) == {}, "Pivot is not eliminated")
    retained = [row for i, row in enumerate(old["residuals"]) if i != 69]
    for i, (a, b) in enumerate(zip(retained, new["residuals"])):
        require(substitute(read(a["terms"]), mapping) == read(b["terms"]), "Wrong eliminated residual " + str(i))
    for i, record in enumerate(new["variables"]):
        j = i if i < 81 else i + 1
        require(record["name"] == old["variables"][j]["name"] and record["index"] == i,
                "Wrong variable renumbering")
    poly = basic_statistics(new, 1338, 1295)
    require(substitute(read(old["expanded_polynomial"]), mapping) == poly, "Full graph-substitution identity fails")
    require(all(e == 0 for m, e in poly), "Output is not an ordinary integer polynomial")
    height = max(abs(int(c)) for c in poly.values())
    require(height < 2 ** 1020 and str(height) == new["report"]["exact_primitive_coefficient_height"], "Exact height differs")
    section = gaussian_section(poly, 1338, (95, 96))
    return {"artifact": "quartic-direct-small-coefficients-1338", "sha256": OUTPUTS["quartic-direct-small-coefficients-1338"],
            "parent_sha256": PARENTS["quartic-direct-small-coefficients"], "total_variables": 1338,
            "residuals_checked": 1295, "expanded_coefficients_checked": len(poly), "exact_degree": 4,
            "exact_primitive_height": height, "strict_height_bound": "2^1020",
            "all_pivot_occurrences_checked": uses, "full_graph_substitution_identity": True,
            "field_scope": "Conjunction preserved over every characteristic-zero field. Literal SOS projection equivalence follows over formally real fields; arbitrary nonreal-field equivalence is not asserted.",
            "Q_i_universal_section": section}


def initial_constants():
    old = load("quartic-direct-small-coefficients-1338", OUTPUTS["quartic-direct-small-coefficients-1338"])
    new = load("quartic-direct-small-coefficients-1335", OUTPUTS["quartic-direct-small-coefficients-1335"])
    require(old["fixed_constants"] == new["fixed_constants"] == {}, "Unexpected fixed symbol")
    expected_pivots = [
        {((), 0): Fraction(3 ** 32), ((58,), 0): Fraction(-1)},
        {((58, 58), 0): Fraction(1), ((59,), 0): Fraction(-1)},
        {((59, 59), 0): Fraction(1), ((60,), 0): Fraction(-1)},
    ]
    for r, expected in zip((46, 47, 48), expected_pivots):
        require(read(old["residuals"][r]["terms"]) == expected, "Wrong initial constant equation")
    for coordinate, rows in ((58, [46, 47]), (59, [47, 48]), (60, [48, 49])):
        uses = [r for r, row in enumerate(old["residuals"]) if any(coordinate in m for m, e, c in row["terms"])]
        require(uses == rows, "Unrecorded constant-coordinate occurrence")
    mapping = {i: variable(i - 3) for i in range(61, 1338)}
    mapping.update({58: {((), 0): Fraction(3 ** 32)}, 59: {((), 0): Fraction(3 ** 64)},
                    60: {((), 0): Fraction(3 ** 128)}})
    for r in (46, 47, 48):
        require(substitute(read(old["residuals"][r]["terms"]), mapping) == {}, "A constant pivot survives")
    retained = [row for i, row in enumerate(old["residuals"]) if i not in (46, 47, 48)]
    require(len(retained) == len(new["residuals"]), "Wrong number of retained constant-substitution rows")
    for i, (a, b) in enumerate(zip(retained, new["residuals"])):
        require(substitute(read(a["terms"]), mapping) == read(b["terms"]), "Wrong constant-substituted residual " + str(i))
    for i, record in enumerate(new["variables"]):
        j = i if i < 58 else i + 3
        require(record["name"] == old["variables"][j]["name"] and record["index"] == i,
                "Wrong constant-elimination renumbering")
    require(read(new["residuals"][46]["terms"]) == {((), 0): Fraction(3 ** 256), ((58,), 0): Fraction(-1)},
            "First retained chain equation differs")
    poly = basic_statistics(new, 1335, 1292)
    require(substitute(read(old["expanded_polynomial"]), mapping) == poly, "Full constant-substitution identity fails")
    require(all(e == 0 for m, e in poly), "1335 polynomial has a coefficient symbol")
    height = max(abs(int(c)) for c in poly.values())
    old_height = max(abs(int(c)) for c in read(old["expanded_polynomial"]).values())
    require(height == old_height < 2 ** 1020 and str(height) == new["report"]["exact_primitive_coefficient_height"],
            "Claimed unchanged exact coefficient height fails")
    require((3 ** 512).bit_length() == 812, "Wrong new squared-constant bit length")
    section = gaussian_section(poly, 1335, (92, 93))
    return {"artifact": "quartic-direct-small-coefficients-1335", "sha256": OUTPUTS["quartic-direct-small-coefficients-1335"],
            "parent_sha256": OUTPUTS["quartic-direct-small-coefficients-1338"], "total_variables": 1335,
            "residuals_checked": 1292, "expanded_coefficients_checked": len(poly), "exact_degree": 4,
            "exact_primitive_height": height, "strict_height_bound": "2^1020", "height_unchanged": True,
            "deleted_coordinates": [58, 59, 60], "deleted_rows": [46, 47, 48],
            "substituted_constants": ["3^32", "3^64", "3^128"], "new_squared_constant_bits": 812,
            "full_polynomial_substitution_identity": True,
            "field_scope": "Conjunction preserved over every characteristic-zero field. Literal SOS projection equivalence follows over formally real fields; arbitrary nonreal-field equivalence is not asserted.",
            "Q_i_universal_section": section}


def main():
    receipt = {"status": "PASS", "checker": Path(__file__).name,
               "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "imports_producer": False, "randomized_checks": False,
               "scope": "Exact transformations, complete sparse coefficient tables, coordinate counts, heights, and explicit Q(i) sections; no independent arithmetic proof of the parent Z-definition.",
               "results": [translation(), elimination(), initial_constants()]}
    path = HERE / "final-transforms-independent-verification.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    print("PASS: translated1315, eliminated1338, and constant-eliminated1335; all residuals and coefficients checked.")
    for row in receipt["results"]:
        print(row["artifact"], row["expanded_coefficients_checked"], "coefficients; H <", row["strict_height_bound"])
    print("Receipt:", path.relative_to(REPO))


if __name__ == "__main__":
    main()
