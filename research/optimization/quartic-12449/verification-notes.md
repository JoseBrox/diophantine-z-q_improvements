# Exact verification of the 12,449-variable quartic

The independent checker `../verify_constant_quartic.py` passes. It imports no
producer code. Starting from the SHA-pinned, separately verified 12,465-variable
parent, it checks the entire substitution and the complete expanded coefficient
table. Its receipt is `verification.json`.

Run from the repository root:

```sh
python3 research/optimization/verify_constant_quartic.py
```

## Why eliminating the 16 coordinates is exact

The 15 remaining power-chain coordinates are uniquely determined by an initial
linear equation setting the first to `3^1024` and 14 subsequent equations setting
each coordinate to the square of the preceding one. The final chain coordinate
is therefore `C = 3^(2^24)`. The additional anchor coordinate is uniquely fixed
by `D_anchor = C^2 = 3^(2^25)`.

The checker locates each of these defining equations uniquely. It scans every
monomial of every parent residual. Outside the 16 deleted defining equations,
the only occurrence of any deleted coordinate is `2*D_anchor^2` in the packed
anchor residual. Thus substituting the forced constants and deleting their
defining equations gives a bijection between rational solutions, with the
input coordinate preserved. No choice or nonzero hypothesis is needed.

Put `M = 3^(2^26)`. The remaining occurrence becomes `2*M`; the symbol `M`
denotes this fixed integer and consumes no variable. Every retained residual
is still quadratic in the 12,449 rational coordinates. The checker compares
all retained residuals and the full variable remap exactly.

## Complete expansion and specialization

The stored coefficient table is over `Z[M]`. The independent expansion uses
the square of each term and twice each product of distinct terms; this differs
from the producer's ordered-pair expansion. Every coefficient entry agrees.

There are 11,892 residuals, 130,380 nonzero entries indexed by a monomial and
a power of `M`, and 130,378 distinct monomials in the rational coordinates.
Specialization to the stated integer `M` preserves all these monomials. To
verify this without expanding millions of decimal digits, write each coefficient
as `c0+c1*M+c2*M^2`. The checker establishes:

- Every `|c0|` is less than `2^3247`, while `M > 2^(2^26) > 2^3247`.
- Every `|c1|` is at most 24.
- The only coefficient with `c2 != 0` is the constant coefficient, where
  `c2=4`, `c1=0`, and `c0` is nonnegative.

A nonzero linear coefficient with `c1 != 0` therefore cannot cancel after
specialization. The constant coefficient is positive. A private anchor fourth
power has coefficient exactly one, proving that the total degree is exactly
four and that the integer polynomial has content one.

Every nonconstant coefficient has absolute value less than
`M+24*M=25*M < 4*M^2`. Consequently the exact maximum absolute coefficient is

\[
4\cdot3^{2^{27}}+N,
\]

where

```text
N = 373684652355249371111055415460965317040747589616777785974770831188591770167322175457505857070439628239726443171972269170621942059432904883611120549682273.
```

The polynomial thus has 12,449 total variables, 12,448 existential witnesses,
exact degree four, and exactly 130,378 nonzero monomials. A valid upper bound
for the binary length of any coefficient is `2^28+3 = 268435459`.

## Dependencies and limits

The check proves exact equivalence to the pinned parent sum of squares. It does
not reprove the original arithmetic characterization of the integers, nor the
separate semantic anchor replacement used by that parent. It does not expand
the giant fixed power into decimal notation and makes no claim of global
optimality. The symbolic fixed-power notation is an exact finite specification
of integer coefficients, not an additional quantified parameter.
