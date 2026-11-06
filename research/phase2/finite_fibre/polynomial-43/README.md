# An explicit indexed polynomial in 43 variables

This package specifies an integer polynomial in **43 external variables**,
including the input, so there are **42 existential witnesses**. It compiles
the frozen normalized shared-point source `source-43.json.gz`. The source
arithmetic proof is a separate dependency; the compiler proves equality of
the rational input projections.

The representation is an exact **indexed determinant/coefficient/product
polynomial specification**. Its 6,153-node integer coefficient DAG and all
finite index bounds are materialized. The thirty formal finite-algebra
generators are eliminated by the determinant operations and are not
quantified coordinates. Matrices of rank up to `2^39`, the indexed elliptic
exclusion product, the final outer product, and the expanded monomial table
are not materialized.

The construction and proof are described in `../finite_algebra_polynomial.tex`,
`../source_shared.tex`, `../coefficient_bounds.tex`, and
`../fixed_anchor_height.tex`. The arithmetic scalar normalization removing
one base coordinate is proved in
`../../new_polynomials/scalar_preparation_zero.tex`. It changes the fixed
scalar correction set to 16,384 values; the generic compiler is unchanged.

The independently verified bounds are

```text
degree <= 2^9566740
coefficient height <= 2^(2^86098449).
```

These are upper bounds for the specified literal polynomial, not statistics
of an expanded coefficient table. Every zero-radicand and repeated Lucas-root
case is included. There is no unperformed exceptional-stratum computation.

## Reproduce and audit

Run from the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-43.json.gz --output research/phase2/finite_fibre/polynomial-43
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-43.json.gz research/phase2/finite_fibre/polynomial-43/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
python3 research/phase2/finite_fibre/check_fixed_anchor_height.py
```

The independent checker validates exact affine source conversions, point
derivative guards, quadratic exceptions, denominator coverage, the canonical
indexed-anchor factors, coordinate inventories, finite ranges, and all
degree/coefficient bounds. It imports no producer. The receipts state the
scope of what was actually checked.

Specification SHA-256:
`b11ad8157beaf36d3d58c1c5dafe60d9986be598f0ecfdd0ec823be982a9a49f`.

Uncompressed source SHA-256:
`528c3ad7938613141471630fea76e75f9dd5a76dc7cd9949597bef85cc3e2e7c`.

No script commits changes.
