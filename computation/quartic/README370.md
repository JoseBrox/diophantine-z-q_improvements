# A quartic in 370 variables

This directory specifies an integer quartic in **370 total variables** whose
rational input projection is the integers, under the arithmetic premises stated
in the accompanying paper. The effective height estimate is proved in the
companion paper on sums of elliptic abscissas.

Read [the paper](../../papers/quartic/quartic370_20261108_v10.pdf), or its
[LaTeX source](../../papers/quartic/quartic370_20261108_v10.tex).

The coefficient table specifies a family with fixed coefficient
`A = 80989^(2*N+1)`. Every integer `N >= 27464` is covered by the theorem.
In particular, `N = 27464`, hence `A = 80989^54929`, specifies one defining
polynomial completely. Neither `A` nor `N` is a polynomial variable.

| Quantity | Exact value |
| --- | ---: |
| Total variables, including the input | 370 |
| Quadratic equations | 342 |
| Degree of their sum of squares | 4 |
| Symbolic terms before grouping powers of the fixed coefficient | 5852 |
| Nonzero coordinate monomials, for every `N >= 27464` | 5837 |
| Integer content | 1 |
| Largest coefficient binary digits, at `N = 27464` | 1791357 |

## Reproduction

Only Python's standard library is required. Run these commands from this
directory:

```sh
python3 build_quartic370.py
python3 check_quartic370.py
```

The constructor starts from the exact compressed source in
`baseline389/quadratic-system389.json.gz`. Its uncompressed SHA-256 digest is
`f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394`.

The output directory `family370` contains:

- `quadratic-family370.json`: every coordinate and quadratic equation;
- `polynomial-family370.json`: every nonzero coefficient of the sum of squares;
- `construction-report370.json`: exact transformation and size information;
- `independent-verification370.json`: results of the independent checks.

The checker recovers the retained source rows by the inverse affine input
transformation, verifies the new scale equations and all root-coordinate
normalizations, and independently expands the sum of squares. It recovers all
50 equations of the third detector as a separate copy of the second detector
and verifies their full rational normalizations by exact polynomial identities. It also checks
the local congruences, fixed-prime avoidance and numerical separation
certificate. These finite checks establish the specified algebra and numerical
certificates. The arithmetic defining property follows from the paper and its
explicitly stated premises.

## Data format

Coordinates are consecutively numbered from 1 to 370; coordinate 1 is the
input. The separate `sourceId` field is a stable identifier inherited from the
source circuit. It is not a current coordinate number.

Each term has an integer `coefficient`, a nonnegative `parameterPower`, and a
sorted list `monomial` of coordinate numbers. Repeated numbers denote powers;
an empty list denotes a constant. Thus a term represents

`coefficient * A^parameterPower * product(coordinate[j] for j in monomial)`.

The equation table lists one polynomial to be set to zero per row. Its
`fixedParameter` object records the literal specialization. The quartic table
lists the complete sum of their squares. Coefficients are decimal strings so
that their exact integers survive JSON implementations with limited numeric
precision.

The abscissa sum is `S = S0 + S1*sqrt(2)`. Its three semantic scales are
`1`, `S0^2`, and `(S0+S1)^2`. The stored scale coordinates include affine
normalizations documented in the paper and independently checked in the code.
Equal scales are permitted.
