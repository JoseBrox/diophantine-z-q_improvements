# Preferred semilocal indexed polynomial in 45 variables

This package specifies an integer polynomial in **45 external variables**,
including the input, with **44 existential witnesses**. It compiles the frozen
source `source-45-conic-semilocal.json.gz`, preserving its rational input
projection. The source arithmetic characterization is a separate dependency.

The representation is an exact **indexed determinant/coefficient/product
polynomial specification**. Its complete 6,245-node integer coefficient DAG
and all finite index bounds are materialized. **There is no indexed elliptic
exclusion product** in this variant. Its 21 formal algebra generators are
eliminated by determinants and are not quantified coordinates. The
rank-sized matrices, final outer product, and expanded monomial table remain
unmaterialized.

## Degree refinement

Fixed nonzero square height scales remove eight finite component choices.
The first conic in each of the ten pole blocks is rationally parametrized,
including its exceptional `e=1,p=0` point. This removes ten finite quadratic
generators. The remaining algebra has nine point quartics and twelve
quadratic choices, with maximum rank **`2^30`**. Every zero-radicand and
repeated Lucas-root case is explicitly included.

A finite separating-parameter range and explicit degree/resultant cases
isolate a simple root of a guarded norm polynomial. Its rational eigenline
recovers the source coordinates, and trace-adjugate equations impose closed
conditions. A reciprocal substitution uses one additional witness to impose
the final nonzero guards.

The independently verified rounded bounds are

```text
degree <= 2^243
coefficient height <= 2^(2^246).
```

Stronger unrounded integer bounds appear in the specification. These are
upper bounds for the literal indexed polynomial, not expansion statistics.

## Reproduction and independent verification

From the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-45-conic-semilocal.json.gz --output research/phase2/finite_fibre/polynomial-45-conic-semilocal
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-45-conic-semilocal.json.gz research/phase2/finite_fibre/polynomial-45-conic-semilocal/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
```

The independent checker verifies point equations and derivatives, source
rational-square clearings and their denominator guards, affine conversions,
every quadratic case, denominator coverage, monicity, triangularity, all
finite ranges and coordinate inventories, and degree/coefficient bounds.
It imports no producer. The separate small interpreter executes the full
determinant/trace construction on adversarial finite algebras.

Proofs are in `../finite_algebra_polynomial.tex`, `../source_shared.tex`,
`../coefficient_bounds.tex`, and
`../../new_polynomials/degree_refinements.tex`.

Specification SHA-256:
`94aa7333869c254a3a82d591d83e219a144316874bd92d09b529f99c69b6b2a6`.

Uncompressed source SHA-256:
`cc3f38bc2f464551c0eb86c5724afc52903dda393618aca2de25d4b5217abdc5`.

The passing independent receipt is `verification.json`. No script commits
changes; the earlier source variants remain available separately.
