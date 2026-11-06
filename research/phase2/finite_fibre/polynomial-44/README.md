# An explicit indexed polynomial in 44 variables

`polynomial-specification.json` defines an integer polynomial in **44 external
variables**, comprising the input, 42 further retained coordinates, and one
finite-algebra witness. It therefore has **43 existential witnesses**. Its
rational input projection equals that of the frozen shared-point source
`../../new_polynomials/source-44.json.gz`. Identifying that source projection
with the integers additionally uses its arithmetic proof and cited inputs.

This is a complete **indexed determinant/coefficient/product polynomial
specification**. Its 6,145-node integer coefficient DAG is materialized, and
every finite index range is explicit. Its thirty formal algebra generators
are eliminated by determinants; they are not quantified variables. The
multiplication matrices, the enormous products, and the expanded monomial
table are not materialized. This is a more succinct representation than an
arithmetic circuit listing every gate.

## Construction

The guarded triangular algebra has nine monic point quartics and 21 quadratic
choices. Each quadratic has a zero case with a linear relation and a closed
residual, and a nonzero case with a derivative guard. This includes the
repeated Lucas-root case. The maximum algebra rank is `2^39`.

For each finite source branch and quadratic mask, the norm polynomial
`det(I - V*M_{G*lambda})` encodes guarded points. A fully specified finite
separating-parameter range and explicit degree/resultant cases select simple
roots. Their rational eigenlines recover rational algebra points, while
trace-adjugate equations impose all closed conditions. A reciprocal
transformation absorbs the leading-coefficient and resultant guards into the
one additional witness. Taking the finite product of the resulting sums of
squares gives the specified integer polynomial.

This variant includes an indexed fixed elliptic exclusion product for
`1 <= n <= 2^9566463`. Its coefficients are defined canonically by exact
binary multiplication of the fixed point over `Q(sqrt(2))`, followed by a
primitive common-denominator triple. The exact integer factor and the rule
for an identity multiple are in the specification. These fixed constants
introduce no quantified variables. The proof bounds all their coefficients
without computing the enormous product.

## Reproduction and independent verification

Run from the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-44.json.gz --output research/phase2/finite_fibre/polynomial-44
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-44.json.gz research/phase2/finite_fibre/polynomial-44/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
python3 research/phase2/finite_fibre/check_fixed_anchor_height.py
```

The independent checker imports no producer. It checks the exact affine
source substitutions, all nine point equations and derivative guards, all
quadratic exceptional cases, denominator coverage, the canonical fixed-anchor
clearing, coordinate inventories, finite ranges, monicity, triangularity,
and every recorded degree and coefficient-norm inequality. The exact small
interpreter executes the complete theorem on adversarial small algebras.
The separate anchor check compares binary multiplication with repeated
addition on the first 24 multiples; the general coefficient bound is proved
separately.

## Bounds and identifiers

The verified upper bounds for the literal indexed polynomial are

```text
degree <= 2^9566734
coefficient height <= 2^(2^86098443).
```

These are rigorous upper bounds, not expanded-polynomial statistics.
`construction-report.json` records the producer and source identifiers;
`verification.json` records the passing independent audit.

Specification SHA-256:
`2697e3872e5a98d4a0534fd919c28bec255bad1372af3a94e8703116ebb36811`.

Uncompressed source SHA-256:
`0a19cf62a878cef3a0b59c169661f9453d76d270cd7f78003d2522c20baee230`.

Proofs are in `../finite_algebra_polynomial.tex`, `../source_shared.tex`,
`../coefficient_bounds.tex`, and `../fixed_anchor_height.tex`. The compiler
preserves the supplied source; it does not independently establish all the
arithmetic results used by that source. No script commits changes.
