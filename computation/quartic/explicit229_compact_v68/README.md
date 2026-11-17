# Explicit 229-variable quartic with coefficient height 149^30

The fully expanded polynomial [quartic229-N15.txt](quartic229-N15.txt)
occupies **74,007 bytes** in Elliot Glazer's repository's prescribed
plain algebraic notation. It has 229 variables including input `x1`,
degree four, 3,312 nonzero monomials, integer content one, and exact
coefficient height

```math
149^{30}=156887395160328947946897503379992916684449577190738324732588533001.
```

This is a 217-bit integer. The input projection is exactly the integers
under the same arithmetic premises as the pinned 229-variable source
at `N=15`. The coordinate change adds no arithmetic hypothesis, variable,
equation, or excluded locus.

## Construction

Let `Q_j` be row `j` of the included source table, specialized at
`C=149^15`. The integer lists `a_i` and `b_j` in
[transformation.json](transformation.json) specify

```math
R_j(y)=149^{b_j}Q_j(149^{a_1}y_1,\ldots,149^{a_{229}}y_{229}),
\qquad P(y)=\sum_{j=1}^{207}R_j(y)^2.
```

All 207 transformed rows have integer coefficients and content one.
Because every scaling factor is a nonzero rational number and `a_1=0`,
the map is a bijection on rational witnesses that fixes the input.
The inverse is `y_i=149^(-a_i)x_i`. A rational sum of squares vanishes
exactly when every row vanishes. Consequently the source's complete
soundness and integer-witness proof transfers at the same fixed `N=15`.

[quadratic.json](quadratic.json) lists all transformed quadrics;
[polynomial.json](polynomial.json) gives every expanded integer
coefficient. The literal text contains the complete expanded polynomial
itself, without a parameter, abbreviation, factorization, header, or
trailing newline. Neither the coordinate names nor their order changes.

## Exact comparison

| Quantity | Source at N=15 | This polynomial |
|---|---:|---:|
| Variables, including input | 229 | 229 |
| Quadratic rows | 207 | 207 |
| Degree | 4 | 4 |
| Nonzero monomials | 3,312 | 3,312 |
| Coefficient height | 149^32 | 149^30 |
| Coefficient height in bits | 232 | 217 |
| Decimal coefficient digits, counting every coefficient | 95,953 | 21,633 |
| Bytes in the prescribed canonical notation | 148,701 | 74,007 |

The source's previously formatted multiline text has 162,438 bytes.
The canonical source size above removes its header and whitespace and
omits unit coefficients as required by the upstream notation. The
74,694-byte canonical saving comes from changing coefficients;
the monomial support and coordinate order are identical. The coefficient
height decreases by a factor of 22,201.

The 74,007-byte artifact is strictly below both 100,000 and 102,400 bytes,
with 25,993 bytes to spare under the strict decimal convention. No
minimality claim is made for the transformation, height, or text size.

## Reproduction

Run from this directory:

```sh
python -B build.py
python -B check.py --output certificate.json
python -B upstream/measure_plain_text.py polynomial.json --verify-text quartic229-N15.txt
```

The builder and `check.py` need only the Python standard library. The builder uses the fixed
integer exponent lists; no optimization software is required.

The separate checker does not import the builder or optimizer. It
authenticates the source, reconstructs every transformed coefficient
using exact rational arithmetic, verifies integrality and primitive
content of every quadratic row, independently expands all squares,
parses the full literal expression, and compares every coefficient.
It verifies all 229 occurring variables, input preservation, degree,
content, unchanged monomial support, coefficient height and file size.
It rejects a scaled input, a changed coefficient, a trailing newline,
a leading positive sign, and abbreviated coefficient syntax.

The unchanged upstream measuring program is included with its source
URL and SHA-256 in `transformation.json`. It independently confirms
the canonical byte-for-byte representation and the strict bound;
its output is [official_measurement.json](official_measurement.json).
The exact text SHA-256 is

```text
45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975
```

The second checker, `check_independent.py`, uses SymPy sparse polynomial rings
and a separate literal parser. It also checks the inverse coordinate map,
the manuscript exponent tables, and the retained arithmetic body. From the
repository root, `python -B scripts/verify_v68.py` reproduces the builder,
both certificates and the official measurement. SymPy is needed for this
combined check.

## Scope and upstream policy

The mathematical transformation preserves the complete source proof,
including its retained arithmetic premises. Finite coefficient checks
do not independently establish those premises.

The upstream [explicit-record rule](https://github.com/elliotglazer/diophantine-z-q/blob/970ec6bf338dc47fad151132a4122fd5c899e348/docs/explicit-record/README.md)
specifies `x1,...,xn`, literal decimal coefficients, and strict size
below 100,000 bytes. The included artifact follows that rule exactly.
Its [release policy](https://github.com/elliotglazer/diophantine-z-q/blob/970ec6bf338dc47fad151132a4122fd5c899e348/docs/release-policy.md)
additionally requires a complete current manuscript, matching PDF and
the stated independent acceptance before promotion as an official
upstream record. This package does not claim that upstream publication
or acceptance has occurred.

The source table is pinned to commit
`7501669160c1662a742ddd54baed364a47c82ddc` of
`JoseBrox/diophantine-z-q_improvements`, path
`computation/quartic/explicit229_v62/quadratic.json`.
Its source proof is
`papers/quartic/quartic229_20261117_v62.tex`.
