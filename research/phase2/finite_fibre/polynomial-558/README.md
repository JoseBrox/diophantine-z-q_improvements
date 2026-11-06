# An explicit polynomial specification in 558 variables

This package completes the phase-one finite-fiber existence construction as
an **exact indexed determinant/coefficient/product polynomial specification**.
It has 558 external variables: the input, 556 other retained coordinates,
and one additional finite-algebra witness. Thus it has **557 existential
witnesses**.

Its 297 formal algebra generators are eliminated by determinants. They are
not quantified variables. The 101,637-node integer coefficient DAG is fully
materialized, as are all finite parameter bounds and the complete polynomial
recipe. The multiplication matrices can have rank `2^508`, so those matrices,
the enormous final product, and the expanded monomial list are not materialized.
The representation is more succinct than an ordinary arithmetic DAG listing
every gate, and is identified explicitly as such.

## Mathematical construction

The finite algebra consists of 211 monic point quartics and 86 algebraic
choices: the completed Lucas root, the anchor root, and 84 pole roots.
Every quadratic has an explicit zero case with a linear relation and a
nonzero case with a derivative guard. This covers repeated roots and the
exceptional zero pole inputs without relying on a generic-only argument.

For each finite branch, multiplication by
`G*(1 + ell*z_1 + ... + ell^297*z_297)` gives a matrix `M`. The polynomial
`H(V) = det(I - V*M)` sees only points where the guard is nonzero. At
those points the algebra is simple. A finite separating-parameter range
and explicit degree/resultant cases ensure that every accepted root is
simple. Its rational eigenline recovers a rational point of the algebra.
Trace-adjugate polynomials impose all remaining closed conditions.

A final reciprocal transformation incorporates the resultant and leading
coefficient guards into the one remaining witness. The product over all
finite choices is the specified polynomial. Every operation and every
index bound appears in `polynomial-specification.json` and the accompanying
proofs; no exceptional-stratum computation is left unspecified.

## Reproduction and verification

From the repository root:

```sh
python3 research/phase2/finite_fibre/build_558_specification.py
python3 research/phase2/finite_fibre/verify_558_specification.py
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
```

The independent checker imports no producer. It checks every source point
quartic, all 85 private quadratic extractions, the completed Lucas equation
and its zero case, all affine substitution identities, all coordinate and
finite-index inventories, monicity, triangularity, and the degree and
coefficient-norm inequalities. The exact small-instance interpreter executes
177 full selector/degree cases on eight adversarial examples and emits a
fully expanded degree-16 example polynomial.

The proof files are `../finite_algebra_polynomial.tex`, `../source_558.tex`,
and `../coefficient_bounds.tex`.

## Bounds and scope

The independently verified rounded bounds are

```text
degree <= 2^3122
coefficient height <= 2^(2^3127).
```

The specification records stronger unrounded integer bounds. These are
upper bounds for the literal indexed polynomial, not expansion statistics.
The source-to-polynomial transformation preserves the rational input
projection; identifying that projection with the integers still inherits
the arithmetic theorem of the pinned source repository.

Specification SHA-256:
`591b69dc16fc27a105dd051d7cebb8b10a0711655e4093f0be3194bd6312f320`.

The construction and verification receipts are included in this directory.
No commits are made by these scripts.
