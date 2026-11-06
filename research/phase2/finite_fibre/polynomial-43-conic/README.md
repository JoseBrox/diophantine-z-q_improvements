# Preferred indexed polynomial in 43 variables

This package specifies an integer polynomial in **43 external variables**,
including the input, with **42 existential witnesses**. It compiles the frozen
source `source-43-conic.json.gz`, preserving its rational input projection.
Identifying that projection with the integers additionally uses the source
arithmetic proofs and cited inputs.

The representation is an exact **indexed determinant/coefficient/product
polynomial specification**. Its 6,224-node integer coefficient DAG, fixed
integer constants, and all finite index bounds are specified. Its twenty
formal algebra generators are eliminated by determinants, so they are not
quantified coordinates. The rank-sized matrices, the indexed elliptic
exclusion product, the final outer product, and the expanded coefficient
table are not materialized.

## Degree refinement

The source uses fixed nonzero square height scales and parametrizes each of
the ten first pole conics. Each conic has two finite charts; the exceptional
point with `e=1,p=0` is included, and no nonzero condition on the removed root
or its conic parameter is imposed. This leaves nine monic point quartics and
eleven quadratic choices: ten second pole roots and the Lucas root. The
maximum finite-algebra rank is **`2^29`**.

All remaining quadratics have explicit zero and nonzero cases, including a
repeated Lucas root. A finite separating-parameter range, explicit degree
cases, and a resultant select a simple root of a norm polynomial. Rational
eigenlines and trace-adjugate equations recover a rational source point. A
reciprocal substitution absorbs the final guards into one extra witness.

The independently verified bounds are

```text
degree <= 2^9566680
coefficient height <= 2^(2^86098389).
```

These are upper bounds for the literal specified polynomial, not expanded
coefficient statistics. The large exponents include the indexed fixed
elliptic exclusion product, whose coefficients are canonically specified by
exact binary multiplication over `Q(sqrt(2))`.

## Reproduction and independent verification

From the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-43-conic.json.gz --output research/phase2/finite_fibre/polynomial-43-conic
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-43-conic.json.gz research/phase2/finite_fibre/polynomial-43-conic/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
python3 research/phase2/finite_fibre/check_fixed_anchor_height.py
```

The independent checker imports no producer. It verifies the point quartics,
derivative guards, source rational-square clearings and their denominators,
all affine substitutions, quadratic exceptional cases, guard coverage,
canonical indexed-anchor clearing, variable inventories, finite ranges,
and all degree/coefficient bounds. The exact small interpreter exercises the
complete theorem on adversarial finite algebras. The general theorem and
height proof justify the unexpanded large operations.

Proofs are in `../finite_algebra_polynomial.tex`, `../source_shared.tex`,
`../coefficient_bounds.tex`, `../fixed_anchor_height.tex`, and
`../../new_polynomials/degree_refinements.tex`.

Specification SHA-256:
`fe155074230a7cba19b77415e7d1a360640f3664cea51efdfe347a0774b6895c`.

Uncompressed source SHA-256:
`bdad2cd825cfd5e342a3bae01132cbbbbee179db5d8c2dc31e17475572b73f85`.

The producer and independent verification receipts are included. No script
commits changes; the earlier source variants remain available separately.
