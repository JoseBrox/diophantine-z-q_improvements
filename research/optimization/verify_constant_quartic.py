#!/usr/bin/env python3
"""Independent exact audit of the fixed-constant 12449-variable quartic.

No producer code is imported. The parent residual system is SHA-pinned. Its
16 deleted variables are solved uniquely, every occurrence is inspected, and
the complete new sum of squares is expanded independently over Z[M]. Here
M=3**(2**26) is a fixed integer, never an extra quantified variable.
"""

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PINS = {
    "residuals.json.gz": "77ee06488cf89df303372a19020626af1cae0e30e9bc869feba28c79942b3e75",
    "weights.json": "a7e96eefe561b570c18c822dd8c873cddd19c58c8f9ef3d826f33c4f75c8c27e",
    "variable-map.json": "61b4bf2264abd8b222ad94f01f044de861cc70baccc779f5ca874b106cc04ca7",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_row(row, variable_count, formal=False):
    answer = {}
    for entry in row:
        require(len(entry) == (3 if formal else 2), "Malformed polynomial term")
        if formal:
            coefficient, exponent, monomial = entry
        else:
            coefficient, monomial = entry
            exponent = 0
        require(type(coefficient) is int and coefficient != 0, "Invalid coefficient")
        require(type(exponent) is int and 0 <= exponent <= 2, "Invalid M exponent")
        require(type(monomial) is list and monomial == sorted(monomial), "Noncanonical monomial")
        require(all(type(v) is int and 0 <= v < variable_count for v in monomial), "Invalid variable")
        key = (exponent, tuple(monomial))
        require(key not in answer, "Repeated polynomial term")
        answer[key] = coefficient
    return answer


def verify(parent, candidate):
    raw_parent = {name: (parent/name).read_bytes() for name in PINS}
    for name, expected in PINS.items():
        require(sha(raw_parent[name]) == expected, "Parent hash mismatch: "+name)
    old_map = json.loads(raw_parent["variable-map.json"])
    require(len(old_map) == len(set(old_map)) == 12465 and old_map[0] == 0, "Invalid parent map")
    old_rows = [read_row(row, len(old_map)) for row in json.loads(gzip.decompress(raw_parent["residuals.json.gz"]))]
    require(json.loads(raw_parent["weights.json"]) == [1]*len(old_rows), "Parent weights are not all one")
    locate = {source: current for current, source in enumerate(old_map)}
    chain = [locate[source] for source in range(11,26)]
    anchor_r, anchor_D, anchor_u, anchor_v, anchor_w = [locate[source] for source in range(16794,16799)]

    # Establish the uniquely forced fixed powers, without expanding giant
    # integers. The first remaining chain value is modest enough to check
    # exactly. Each subsequent exponent is doubled by a monic square row.
    solved = {}
    removed_rows = set()
    forced_exponents = {}
    for k, variable in enumerate(chain+[anchor_D]):
        if k == 0:
            expected = {(0,()):3**1024, (0,(variable,)):-1}
            exponent = 1024
        else:
            previous = (chain+[anchor_D])[k-1]
            expected = {(0,(previous,previous)):-1, (0,(variable,)):1}
            exponent = 2*forced_exponents[previous]
        hits = [i for i,row in enumerate(old_rows) if row == expected]
        require(len(hits) == 1, "A unique constant defining row is missing")
        require(hits[0] not in removed_rows, "Duplicate defining row")
        removed_rows.add(hits[0]); forced_exponents[variable] = exponent
        solved[variable] = {"base":3,"exponent":exponent,"parent_row":hits[0]}
    require(forced_exponents[chain[-1]] == 2**24 and forced_exponents[anchor_D] == 2**25,
            "Wrong anchor power")

    expected_anchor = {(0,(anchor_u,anchor_u)):1,(0,(anchor_v,anchor_v)):6,
                       (0,(anchor_w,anchor_w)):-2,(0,(anchor_r,anchor_r)):-3,
                       (0,(anchor_D,anchor_D)):2}
    hits = [i for i,row in enumerate(old_rows) if row == expected_anchor]
    require(len(hits) == 1, "Packed anchor residual is missing")
    anchor_row = hits[0]
    deleted = set(solved)
    incidence = defaultdict(list)
    for i,row in enumerate(old_rows):
        for (_,monomial), coefficient in row.items():
            for v in deleted.intersection(monomial):
                incidence[v].append(i)
            if deleted.intersection(monomial) and i not in removed_rows:
                require(i == anchor_row and monomial == (anchor_D,anchor_D),
                        "Deleted variable has an unaccounted occurrence")
    require(0 not in deleted and len(deleted) == len(removed_rows) == 16,
            "Bad elimination inventory")

    active = sorted(set(range(len(old_map)))-deleted)
    remap = {v:i for i,v in enumerate(active)}
    derived = []
    for i,row in enumerate(old_rows):
        if i in removed_rows:
            continue
        result = {}
        for (e,monomial), coefficient in row.items():
            if monomial == (anchor_D,anchor_D):
                require(i == anchor_row and coefficient == 2, "Unexpected anchor square")
                key = (1,())  # D_anchor^2 = 3^(2^26) = M.
            else:
                key = (0,tuple(remap[v] for v in monomial))
            require(key not in result, "Unexpected substitution collision")
            result[key] = coefficient
        derived.append(result)

    raw_candidate = gzip.decompress(candidate.read_bytes())
    obj = json.loads(raw_candidate)
    require(obj["format"] == "integer-quartic-with-one-fixed-power-constant-v1", "Wrong format")
    require(obj["constant_M"] == {"base":3,"exponent":2**26,"is_a_variable":False}, "Wrong fixed constant")
    require(obj["parent"] == "quartic-anchor-packed-large", "Wrong parent identifier")
    require(obj["parent_residuals_sha256"] == PINS["residuals.json.gz"], "Wrong parent certificate hash")
    require(obj["variables"] == len(active) == 12449, "Wrong variable count")
    require(obj["variable_map_to_parent"] == active, "Wrong complete variable remap")
    require(obj["deleted_parent_variables"] == sorted(deleted), "Wrong deleted coordinates")
    require(obj["deleted_parent_rows"] == sorted(removed_rows), "Wrong deleted equations")
    require(obj["parent_anchor_row"] == anchor_row, "Wrong anchor row index")
    actual_rows = [read_row(row,len(active),True) for row in obj["residuals"]]
    require(actual_rows == derived, "Residual substitution differs")
    require(max(len(m) for row in derived for e,m in row) == 2, "Residuals are not quadratic")

    # Independent expansion uses unordered pairs and a factor of two for
    # off-diagonal terms, rather than the producer's ordered-pair expansion.
    expansion = Counter()
    for row in derived:
        terms = sorted(row.items())
        for i, ((e,m),a) in enumerate(terms):
            expansion[(2*e,tuple(sorted(m+m)))] += a*a
            for (f,n),b in terms[i+1:]:
                expansion[(e+f,tuple(sorted(m+n)))] += 2*a*b
    expansion = {key:c for key,c in expansion.items() if c}
    advertised = read_row(obj["coefficient_table"],len(active),True)
    require(advertised == expansion, "Expanded coefficient table differs")

    by_monomial = defaultdict(dict)
    for (e,m), c in expansion.items():
        by_monomial[m][e] = c
    require(set(v for m in by_monomial for v in m) == set(range(12449)), "An advertised variable is unused")
    require(max(map(len,by_monomial)) == 4, "Wrong formal degree")
    require(by_monomial[(remap[anchor_u],)*4] == {0:1}, "Primitive quartic coefficient missing")
    constant = by_monomial[()]
    require(set(constant) == {0,2} and constant[2] == 4 and constant[0] >= 0, "Wrong constant coefficient")
    require(all(e <= 1 or m == () for e,m in expansion), "Unexpected quadratic M coefficient")
    c0 = max(abs(c) for (e,m),c in expansion.items() if e == 0)
    c1 = max(abs(c) for (e,m),c in expansion.items() if e == 1)
    require(c0 < 2**3247 and c1 <= 24, "Coefficient dominance bounds fail")
    # M > 2^(2^26) > 2^3247. Thus a nonzero linear polynomial c0+c1*M
    # cannot vanish under these coefficient bounds. The only quadratic one
    # is the strictly positive constant 4*M^2+constant[0]. All other absolute
    # coefficients are < M+24*M=25*M < 4*M^2. This proves actual monomial
    # count, exact degree, and the stated exact maximum after specialization.
    require(2**26 > 3247 and 2**26 > 4, "Fixed-constant comparison failed")
    monomials = len(by_monomial)
    require(monomials == 130378 and len(derived) == 11892, "Wrong final inventory")

    return {
        "status":"PASS",
        "scope":"Exact unique constant elimination from the pinned parent, exhaustive incidence and remap, and full sum-of-squares expansion over Z[M]; M is then the fixed integer 3^(2^26).",
        "total_variables":len(active),"existential_witnesses":len(active)-1,
        "degree":4,"residuals":len(derived),"monomials_after_specialization":monomials,
        "formal_coefficient_entries":len(expansion),"variables_removed":len(deleted),
        "content_gcd":1,"max_abs_coefficient":{"power_term":{"coefficient":4,"base":3,"exponent":2**27},"addend":constant[0]},
        "coefficient_bit_bound":2**28+3,
        "maximum_constant_coefficient_bits":c0.bit_length(),"maximum_linear_M_coefficient":c1,
        "fixed_constant":{"base":3,"exponent":2**26,"is_a_variable":False},
        "forced_parent_constant_powers":solved,"removed_variable_incidence":dict(incidence),
        "parent_sha256":PINS,"uncompressed_candidate_sha256":sha(raw_candidate),
        "checker_sha256":sha(Path(__file__).read_bytes()),
        "not_checked":["Original source arithmetic theorem","Parent semantic anchor theorem (separate checked dependency)","Decimal expansion of the giant fixed constant","Global optimality"]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = REPO/"research/optimization"
    parser.add_argument("--parent",type=Path,default=root/"quartic-anchor-packed-large")
    parser.add_argument("--candidate",type=Path,default=root/"quartic-12449/polynomial-symbolic.json.gz")
    parser.add_argument("--receipt",type=Path,default=root/"quartic-12449/verification.json")
    args = parser.parse_args()
    receipt = verify(args.parent,args.candidate)
    args.receipt.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({k:receipt[k] for k in ("status","total_variables","degree","monomials_after_specialization","variables_removed","content_gcd")}))


if __name__ == "__main__":
    main()
