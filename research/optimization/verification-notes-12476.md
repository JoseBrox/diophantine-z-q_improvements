# Independent verification of the 12,476-variable quartic

The additional algebraic transformations pass an independently implemented
checker. The check proves equality of rational input projections with the
frozen 12,504-variable parent, conditional only on that parent's algebraic
certificate. The arithmetic theorem identifying the parent projection with
Z remains outside this check.

## Exact result

| Quantity | Independently computed value |
| --- | ---: |
| Total variables, including input | 12,476 |
| Rational witness variables | 12,475 |
| Total degree | 4 |
| Nonzero quadratic residuals | 11,911 |
| Nonzero expanded monomials | 130,481 |
| Maximum coefficient bit length | 3,247 |
| Maximum coefficient decimal digits | 978 |
| GCD of all expanded coefficients | 1 |
| Maximum terms in one residual | 19 |
| Residual weights | All 1 |
| Additional eliminations | 28 |
| Additional invertible row operations | 13 |
| Individually checked row patches | 1,588 |

The coefficient maximum H therefore satisfies 2^3246 <= H < 2^3247. Its
complete decimal value is in `verification-12476.json`. This is a reduction
in variables at the same degree, with a substantial increase in coefficient
height. No claim of minimality for the variable count is made.

The uncompressed expanded polynomial has SHA-256
`92222e9965d3155ab917c1cdc3f97dc9b05a8aeb0dfe09e53a8d32f605ec3cb9`.

## Why the transformations preserve the input projection

A row operation replaces R_i by a nonzero rational multiple of
`a R_i + b R_j`, keeps R_j unchanged, and has a nonzero rational constant a.
Its inverse recovers R_i from the two retained equations. Both implications
hold at every rational assignment, including when the resulting row is zero.

An elimination first verifies that its pivot row is a nonzero rational
multiple of `d V - N`, where d is a nonzero integer constant and N does not
involve V. Thus every solution has the uniquely determined value V=N/d.
Substitution in every other occurrence of V is reversible by assigning this
same value. Multiplying any resulting row by a nonzero rational constant
preserves its zero set. The input coordinate, numbered 0, is never eliminated.
No variable-dependent denominator is cancelled.

The final variable map is a bijection from all active old coordinates to the
listed compact coordinates and fixes input 0. Every final residual and every
positive weight is checked. Ordered-pair polynomial multiplication then
independently expands the complete sum of squares, and its exact bytes are
compared with both supplied monomial tables. Over Q a sum of positive-weight
squares is zero precisely when all residuals are zero.

## Reproduction and scope

From the repository root:

```sh
python3 research/optimization/verify_extra_operations.py
```

The checker uses only the Python standard library and imports no producer or
shared polynomial-arithmetic helper. It uses exact Fraction substitution and
coefficient-by-coefficient proportionality checks, independently of the
producer's denominator-clearing and primitive-normalization algorithms.
It rescans the complete residual system to find every occurrence at each
elimination. It imposes no coefficient-size bound as a proof assumption.

All frozen parent files are SHA-256 pinned. The candidate certificate must
contain an unchanged prefix consisting of the initial record and all 1,467
parent transformation records. The additional verifier starts from the
pinned parent residuals, so it does not repeat that prefix's algebraic
checks by default. The original full checker was already run separately in
the research session. To rerun that unchanged checker without modifying its
stored report, use:

```sh
python3 research/optimization/verify_extra_operations.py --check-parent
```

The default run, which produced the supplied receipt, checked the 41 added
operations and the complete final expansion. It did not rerun the parent's
full certificate. The receipt explicitly records that distinction.

Seven deliberate corruptions of actual added events were also tested and
rejected: zero denominator, input elimination, omitted occurrence, omitted
patch, changed substitution numerator, changed substituted coefficient, and
a singular row operation. Their outcomes are recorded separately in
`negative-checks-12476.json`.
