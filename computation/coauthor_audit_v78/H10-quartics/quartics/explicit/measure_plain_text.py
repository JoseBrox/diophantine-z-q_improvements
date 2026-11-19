#!/usr/bin/env python3
"""Write an integer polynomial in the repository's plain algebraic notation and measure it.

Input: a JSON file with an integer field "variables" and a list "terms"; each term has
"monomial", a list of one-based variable indices with repetition (for example [1, 1, 47]
is x1^2*x47), and "coefficient", a decimal integer string. A term may not carry a
nonzero "parameterPower": an explicit polynomial has no parameters.

The notation is defined in README.md beside this file. This program is the reference
implementation of that definition. It uses only the Python standard library.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter

LIMIT_BYTES = 100_000
INTEGER = re.compile(r"-?(0|[1-9][0-9]*)\Z")

# Coefficients may have many thousands of digits; lift the interpreter's conversion cap.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def load_terms(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    variables = data["variables"]
    if type(variables) is not int or variables < 1:
        raise ValueError("'variables' must be a positive integer")
    collected = Counter()
    for term in data["terms"]:
        if term.get("parameterPower", 0) != 0:
            raise ValueError("a term depends on a parameter; the polynomial is not explicit")
        coefficient = term["coefficient"]
        if type(coefficient) is not str or not INTEGER.match(coefficient):
            raise ValueError("coefficient is not a decimal integer string: %r" % (coefficient,))
        monomial = term["monomial"]
        if any(type(i) is not int or not 1 <= i <= variables for i in monomial):
            raise ValueError("variable index out of range in %r" % (monomial,))
        collected[tuple(sorted(monomial))] += int(coefficient)
    terms = {m: c for m, c in collected.items() if c != 0}
    if not terms:
        raise ValueError("the polynomial is zero")
    return variables, terms


def render(terms):
    pieces = []
    for monomial in sorted(terms):
        coefficient = terms[monomial]
        factors = []
        for index, power in sorted(Counter(monomial).items()):
            factors.append("x%d" % index if power == 1 else "x%d^%d" % (index, power))
        magnitude = str(abs(coefficient))
        if factors and magnitude == "1":
            body = "*".join(factors)
        else:
            body = "*".join([magnitude] + factors)
        sign = "-" if coefficient < 0 else ("+" if pieces else "")
        pieces.append(sign + body)
    return "".join(pieces)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("polynomial_json")
    parser.add_argument("--output", help="write the plain text here (no trailing newline)")
    parser.add_argument("--verify-text", help="require this file to equal the plain text byte for byte")
    parser.add_argument("--limit", type=int, default=LIMIT_BYTES,
                        help="size limit in bytes (default %d)" % LIMIT_BYTES)
    args = parser.parse_args(argv)
    variables, terms = load_terms(args.polynomial_json)
    text = render(terms).encode("ascii")
    used = {i for monomial in terms for i in monomial}
    report = {
        "variables_declared": variables,
        "variables_occurring": len(used),
        "monomials": len(terms),
        "degree": max(len(m) for m in terms),
        "largest_coefficient_digits": max(len(str(abs(c))) for c in terms.values()),
        "bytes": len(text),
        "sha256": hashlib.sha256(text).hexdigest(),
        "limit_bytes": args.limit,
        "within_limit": len(text) < args.limit,
    }
    if args.output:
        with open(args.output, "wb") as handle:
            handle.write(text)
    if args.verify_text:
        with open(args.verify_text, "rb") as handle:
            report["verify_text_matches"] = handle.read() == text
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    ok = report["within_limit"] and report.get("verify_text_matches", True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
