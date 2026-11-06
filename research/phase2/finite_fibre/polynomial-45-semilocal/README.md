# An explicit indexed polynomial in 45 variables

This package specifies an integer polynomial in **45 external variables**,
including the input, so there are **44 existential witnesses**. It compiles
the frozen normalized semilocal shared-point source
`source-45-semilocal.json.gz`. The arithmetic characterization of that source
is a separate dependency; the compiler proves equality of rational input
projections.

The representation is an exact **indexed determinant/coefficient/product
polynomial specification**. Its complete 6,174-node integer coefficient DAG
and all finite index bounds are materialized. **There is no indexed elliptic
exclusion product** in this variant. The 31 formal algebra generators are
eliminated by determinants and are not quantified coordinates. Matrices of
rank up to `2^40`, the final outer product, and the expanded monomial table
are not materialized.

The construction uses the same generic compiler as the 46-variable semilocal
package. The arithmetic scalar normalization removes one retained coordinate
and expands the finite scalar correction set to 16,384 values. Zero radicands,
repeated Lucas roots, and all degree drops are explicitly included.

The independently verified bounds are

```text
degree <= 2^302
coefficient height <= 2^(2^306).
```

Stronger unrounded integer bounds appear in the specification. These are
upper bounds for the literal indexed polynomial, not expansion statistics.

## Reproduce and audit

Run from the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-45-semilocal.json.gz --output research/phase2/finite_fibre/polynomial-45-semilocal
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-45-semilocal.json.gz research/phase2/finite_fibre/polynomial-45-semilocal/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
```

The independent checker validates exact affine conversions, all point
equations and derivative guards, all quadratic cases, denominator coverage,
monicity, triangularity, coordinate inventories, finite ranges, and the
degree/coefficient inequalities. It imports no producer. The small exact
interpreter executes the full determinant/trace construction on adversarial
small algebras.

Proofs are in `../finite_algebra_polynomial.tex`, `../source_shared.tex`,
`../coefficient_bounds.tex`, and
`../../new_polynomials/scalar_preparation_zero.tex`.

Specification SHA-256:
`9b13aa4d2faa7697828ef56302c7c7608b0e2a3ea177b57671b685e3e90c322c`.

Uncompressed source SHA-256:
`f39001418588f3b102f590393e3909c2e98f56a5cd9b4a6659a69d9cdf12809a`.

No script commits changes.
