# Inverse reference functions and reciprocal squares

The complete proof is
[inverse_reference_squares_20261116_v48.tex](../../../papers/elliptic_charts/inverse_reference_squares_20261116_v48.tex).

The five field coordinates are `u,w,h,A,B`. The first three present the
complete four-point complement on the elliptic reference curve. The other
two are exactly the squared reciprocal abscissas. The five quadratic
equations include both exceptional fibers of the linear graph rows;
their fifth equation determines the otherwise unconstrained square.
There is no additional guard or coordinate.

The parameter assumptions are
`a*c*delta*Delta != 0`, with `delta=a-c²` and
`Delta=(a+delta)²-4*a*c²`, in characteristic zero.
Both project translators `R0` and `2R0` satisfy them. The theorem does not
require the translator's abscissa to be a square.

## Reproduction

From the repository root, using Python 3.12 and SymPy 1.14.0:

```sh
python -B computation/elliptic_charts/inverse_reference_squares_v48/check.py
python -B computation/elliptic_charts/inverse_reference_squares_v48/independent-check.py
```

Both programs accept `--output PATH`, allowing checks in temporary files.

- `check.py` proves the generic identities by exact Laurent normal forms,
  verifies the polynomial recovery from the ratio outputs, and certifies
  the nonzero field constants for both translators.
- `independent-check.py` imports no producer code and uses only Python's
  standard library. It exhausts all admissible constant pairs and complete
  graph fibers over six finite fields, including both exceptional fiber
  types. It checks 10,840 reference points and polynomial inverses.

The two distributed JSON files record the exact outputs. The finite-field
checks supplement the all-field proof; they are not an argument by sampling
for characteristic zero. This package by itself asserts no smaller complete
defining polynomial and uses no elliptic-rank or arithmetic-realization premise.
