#!/usr/bin/env python3
"""Render the published quartic coefficient tables as compact expanded ASCII.

Coefficient sources are immutable historical records. No Busy Beaver value is
evaluated: the symbolic BB(t) output remains expanded only in the variables.

python -B computation/expanded_text_v84/build.py
python -B computation/expanded_text_v84/build.py --output /tmp/expanded-v84
"""
from __future__ import annotations
from collections import OrderedDict
from itertools import groupby
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "quartic163-N1.txt": ("computation/variable_reductions_v82/general/quartic163/polynomial.json", 149, False),
    "quartic179.txt": ("computation/variable_reductions_v82/general/quartic179/polynomial.json", 1, False),
    "quartic56-B3.txt": ("computation/variable_reductions_v81/abc/quartic56/polynomial.json", 3, False),
    "quartic163-BB_t-symbolic.txt": ("computation/variable_reductions_v82/general/quartic163/polynomial.json", None, True),
}

def monomial_text(indices: list[int]) -> str:
    parts = []
    for index, block in groupby(indices):
        exponent = len(list(block))
        variable = f"x{index}"
        parts.append(variable + (f"^{exponent}" if exponent > 1 else ""))
    return "*".join(parts)

def render(source: Path, parameter: int | None, symbolic: bool) -> tuple[str, int]:
    spec = json.loads(source.read_text(encoding="utf-8"))
    coefficients: OrderedDict[tuple[int, ...], int | tuple[int, int]] = OrderedDict()
    for row in spec["terms"]:
        key = tuple(row["monomial"])
        base, power = int(row["coefficient"]), int(row["parameterPower"])
        if symbolic:
            assert key not in coefficients, "symbolic profile requires unique monomials"
            coefficients[key] = (base, power)
        else:
            assert parameter is not None
            coefficients[key] = int(coefficients.get(key, 0)) + base * parameter**power

    out = []
    for key in sorted(coefficients):
        raw = coefficients[key]
        if symbolic:
            coeff, power = raw
        else:
            coeff, power = int(raw), 0
        if coeff == 0:
            continue
        negative = coeff < 0
        abs_coeff = abs(coeff)
        mon = monomial_text(list(key))
        if not symbolic and mon and abs_coeff == 1:
            leader = ""
        elif symbolic and not power and mon and abs_coeff == 1:
            leader = ""
        else:
            leader = str(abs_coeff)
        if symbolic and power:
            leader += ("*" if leader else "") + f"149^({power}*BB(t))"
        term = leader + ("*" if leader and mon else "") + mon
        out.append(("-" if negative else "+" if out else "") + term)
    result = "".join(out)
    assert result.isascii() and result and "\n" not in result
    return result, len(out)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None,
                        help="write generated files in this directory (default: read-only)")
    args = parser.parse_args()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
    for name, (path, value, symbolic) in SOURCES.items():
        content, terms = render(ROOT/path, value, symbolic)
        if args.output:
            (args.output/name).write_bytes(content.encode("ascii"))
        print(f"{name}: {len(content)} bytes = {len(content)/1000:.3f} kB; {terms} monomials")
if __name__ == "__main__":
    main()
