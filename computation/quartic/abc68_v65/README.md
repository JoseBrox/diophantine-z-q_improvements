# Complete 68-variable quartic

This directory specifies the primitive integer family in
`papers/quartic_existence/quartic_abc68_20261117_v65.tex`.
The fixed odd coefficient parameter satisfies `B >= 81`. A sufficiently large
defining value exists under ordinary rational abc and the arithmetic premises
stated in the paper; no numerical sufficient value is supplied.

## Exact specification

- `quadratic-family.json` lists all **68 coordinates** and **56 primitive integer quadrics**.
- `polynomial-family.json` is their complete sum-of-squares expansion: degree **4**, **1,078 coordinate monomials**, and **1,081 parameter-separated terms**.
- `basis-transformation.json` records the fixed invertible reference matrix and all constant-pivot row operations.
- `construction-report.json` records the coefficient census and arithmetic scope.

The input is coordinate one. Its fourth-power coefficient is one, so the
polynomial has integer content one for every integer parameter. The constant
coefficient is `B^2+1`; the largest fixed coefficient is 3,554. All other
parameter-dependent profiles are bounded by `B^2+1` for `B >= 81`, giving the
exact coefficient height in that range.

The translated-secant chart uses six field coordinates and one rational
half-trace output. Both reciprocal abscissas are already coordinates. The
imaginary component of the difference abscissa is a derived quadratic,
with no separate coordinate or defining row. All tangent fibers and all
finite two-torsion differences are covered. The additional difference `(0,0)`
has elliptic index zero, so the soundness proof includes it. Every old
nonzero-integer witness lifts, and the explicit zero-input witness retains
its original gap.

## Reproduction

```sh
python -B computation/quartic/abc68_v65/build.py --output /tmp/abc68-rebuilt
python -B computation/quartic/abc68_v65/check.py --tables /tmp/abc68-rebuilt --output /tmp/abc68-independent.json
python -B computation/quartic/abc68_v65/chart-check.py --output /tmp/abc68-chart.json
```

The independent checker reconstructs all literal equations without importing
the producer or an inherited coefficient table. It verifies row equivalence,
the entire expansion, every coefficient profile, the exact variable census,
and an algebraic zero-input fixture. That fixture has a rational parameter
outside the stated defining range and is only an identity check.

The chart checker supplies universal polynomial identities and exhaustive
comparisons with an independent elliptic group law over seven small odd
finite fields. These computations supplement the all-field proof; they do
not establish the retained global arithmetic premises.
