# Explicit quartic in 229 coordinates

This package specifies a primitive integer quartic with 229 rational
coordinates, including the distinguished input. It uses 207 quadratic
squares and has exactly 3,312 monomials.

The fixed coefficient parameter is $C=149^N$. Its exact coefficient height
for every integer $N\ge1$ is

```math
\max\{9063965991649194484576286065455625302,149^{2N+2}\}.
```

At $N=15$ the height is exactly $149^{32}$, a 232-bit integer. The complete
arithmetic defining theorem and sufficient threshold are proved in the
accompanying manuscript. The finite checker below certifies the equations
and coefficients independently of that arithmetic argument.

## Construction

The construction starts with the certified 195-coordinate system. It copies
34 local coordinates and all 31 equations of its second detector. Both
components of the elliptic abscissa sum already have quadratic recovery
formulas, so the third detector needs no additional recovery coordinate.
The two shifts are

```math
t_1-t_0=13+S_0/2,\qquad
t_2-t_1=17+(S_0-S_1)/2,
```

where $S_0+S_1\sqrt2$ is the four-point abscissa sum. They are at least
7 and 9 for all finite points in the source domain, including torsion
points.

Each detector uses reflection center $3/11$ and the stored square
$r=(22t-3)^2$. The ten contacts have diameter $25/11$, so all three
translated contact sets are disjoint. All auxiliary squares, pole
realizations and three inverse guards are included in the count.

## Files and verification

`quadratic.json` specifies every quadratic equation; `polynomial.json`
specifies the full quartic expansion. `graft.json` gives the coordinate
and row copies, and `contact-change.json` records the new contact
coefficients. `PROVENANCE.json` identifies the precise sources and
attribution.

Rebuild and independently verify with:

```sh
python -B build.py
python -B check.py
```

The producer reconstructs the family directly from `source/quadratic195.json`
using `build_base.py`. No intermediate quartic table is required.
The checker uses only the Python standard library and does not import
either producer. It verifies the source digest, every retained and copied
row, both field components, all twelve contact equations in physical
coordinates, contact factorization and separation, all three guards,
the complete sum-of-squares expansion, exact content and degree, and
the uniform coefficient support and height.

The literal fixed polynomial is [`quartic229-N15.txt`](quartic229-N15.txt).
It contains all 3,312 integer-coefficient terms without a parameter.
Reproduce and check it with `build_literal.py` and `check_literal.py`.
`check_arithmetic.py --output arithmetic_certificate.json` certifies the
finite support and numerical inequalities used in the sufficient threshold.
The complete mathematical proof is
[`quartic229_20261117_v62.tex`](../../../papers/quartic/quartic229_20261117_v62.tex).
