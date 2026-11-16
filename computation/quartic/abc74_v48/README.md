# The 74-variable quartic with integer reference coefficients

This package specifies the polynomial proved in
[papers/quartic_existence/quartic_abc74_20261116_v48.tex](../../../papers/quartic_existence/quartic_abc74_20261116_v48.tex).
All variable counts include the input.

For every fixed odd integer $B\ge81$, the table has 74 rational coordinates,
66 primitive integral quadratic rows, and their sum of squares has degree
exactly four, integer content one, and 1695 nonzero coordinate monomials.
Its exact coefficient height is

$$
H(Q_B)=\max\{30568,B^2+1\}.
$$

Under ordinary rational $abc$ and the arithmetic premises stated in the
paper, every sufficiently large fixed odd $B$ defines the integers over the
rationals. The sufficient threshold is ineffective; $B=81$ is only an
algebraic fixture. The height equals $B^2+1$ for odd $B\ge175$, which is a
coefficient crossover and not a sufficient defining threshold.

## Exact specification

- `quadratic-family.json` contains the coordinate order and all 66 rows.
- `polynomial-family.json` contains the collected integer quartic, with
  powers of the fixed parameter separated from coordinate monomials.
- `basis-transformation.json` specifies the unimodular reference-row matrix
  and the subsequent invertible elimination of fixed constant terms.
- `construction-report.json` records the exact counts and coefficient bounds.
- `build.py` reconstructs the reference quadrics, affine output substitutions,
  basis changes, complete source and quartic expansion.
- `check.py` independently reconstructs the specification using exact rational
  pairs, without importing the producer; its receipt is
  `independent-verification.json`.

The reference translator is $R_0=(1+\sqrt2,2\sqrt2)$, and $\beta=X$.
The complete seven-coordinate paired-point chart is retained. Every reference
exception, tangent pair, torsion branch, zero contact weight and zero input
is treated in the paper. No new nonzero coordinate is added.

## Reproduction

From the repository root, with Python 3.12 and SymPy 1.14.0:

```sh
python -B computation/quartic/abc74_v48/build.py --output /tmp/abc74-v48-rebuilt
python -B computation/quartic/abc74_v48/check.py
```

The producer uses the stored matrix directly; it does not rerun a lattice
search. The retained paired, contact and pole equations are authenticated
against the pinned `abc74_v46/quadratic-family.json` source. Their coordinate
substitutions and the single input-power change are checked exactly.
Computational verification certifies the identities and coefficients it
checks, without certifying the external arithmetic premises.
