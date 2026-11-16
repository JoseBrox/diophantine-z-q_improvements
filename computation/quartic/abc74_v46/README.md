# The 74-variable quartic

This package specifies the family proved in
[`quartic_abc74_20261116_v46.tex`](../../../papers/quartic_existence/quartic_abc74_20261116_v46.tex).
The input is included in the 74 rational coordinates. Each polynomial is a
sum of 64 primitive integral quadratic squares, has degree four and integer
content one, and has 1190 coordinate monomials. Separating powers of the
fixed coefficient parameter `B` gives 1192 terms. Its exact coefficient
height is

```text
max(20828275368498373068800, B^2 + 275933278576697091).
```

The defining assertion uses ordinary rational `abc` and the retained
elliptic-group, simultaneous-prime, trace-height and congruent-number pole
inputs stated in the paper. The coefficient `B` is a sufficiently large
fixed odd integer; its sufficient threshold remains ineffective. The value
`B = 81` is an algebraic fixture, not a certified defining member.

## Construction

The complete point and ratio chart is rescaled by `beta = X/2`. Two scalar
coordinates store `beta^2` and `beta^4`; the additive argument scale is
`B + beta^8 + T^2`. Each detector tests weighted products of a reference and
a numerator reciprocal abscissa. Its quadratic factor equations use the
physical weight directly, and its pole equations use the native pole input.
No stored weight square or additional nonzero witness is needed.

The source coefficient table is
`computation/quartic/abc76_v44/quadratic-family.json`, pinned by SHA-256
`5f03efc8629210d3da25f7b2fad6428ea4f8f288d806bd32f26a87954bc012e8`.
The producer preserves 36 named rows, replaces 27 named rows, removes three
rows and introduces one height row. This is a new arithmetic construction;
equality of its complete rational zero set with the parent family's zero
set is not asserted.

## Contents

- `quadratic-family.json`: all 74 coordinates and all 64 quadratic rows.
- `polynomial-family.json`: the full expanded quartic coefficient table.
- `construction-report.json`: counts, coefficient height and source binding.
- `build.py`: exact sparse producer using Python's standard library and the
  existing standard-library polynomial helpers in the pinned source package.
- `check.py`: independent reconstruction and verification.
- `independent-verification.json`: the expected verification receipt.

## Reproduction

From the repository root, run the independent checker:

```bash
python computation/quartic/abc74_v46/check.py
```

To regenerate the coefficient tables in a separate directory:

```bash
python computation/quartic/abc74_v46/build.py --output /tmp/abc74-tables
```

Calling the producer without `--output` replaces this package's three
generated table/report files. The exact finite computation verifies the
coefficient specification. The manuscript supplies the geometric,
valuation, height and completeness arguments, including the zero-input
stratum and the half-generator choice for odd integer inputs.
