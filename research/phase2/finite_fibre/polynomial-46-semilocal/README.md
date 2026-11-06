# An explicit indexed polynomial in 46 variables

`polynomial-specification.json` defines an integer polynomial in **46 external
variables**, comprising the input, 44 further retained coordinates, and one
finite-algebra witness. It therefore has **45 existential witnesses**. Its
rational input projection equals that of the frozen shared-point semilocal
source `../../new_polynomials/source-46-semilocal.json.gz`. Identifying that
projection with the integers additionally uses the source arithmetic proof
and its cited inputs.

This is a complete **indexed determinant/coefficient/product polynomial
specification**. The full 6,166-node integer coefficient DAG is materialized.
There is no indexed elliptic exclusion product in this variant. All finite
ranges and every algebraic operation are explicit. Its 31 formal algebra
generators are eliminated by determinants; they are not quantified variables.
The rank-sized matrices, outer products, and expanded monomial table remain
unmaterialized. This representation is more succinct than an ordinary
arithmetic circuit listing every gate.

## Construction

The finite algebra has nine monic point quartics and 22 quadratic choices:
the completed Lucas root, eighteen coordinate pole roots, two scalar pole
roots, and the semilocal anchor root. Each quadratic has a zero case with a
linear relation and a closed residual, and a nonzero case with a derivative
guard. Repeated Lucas roots and zero radicands are therefore included. The
maximum free rank is `2^40`.

Multiplication by `G*(1 + ell*z_1 + ... + ell^31*z_31)` gives the norm
polynomial `H(V) = det(I - V*M)`. Explicit finite separating-parameter and
degree/resultant cases provide a simple root. Its rational eigenline recovers
a rational point of the finite algebra. Trace-adjugate equations impose the
closed residuals, and a reciprocal transformation absorbs the leading-
coefficient and resultant guards into the one additional witness. The final
product of sums of squares is the specified integer polynomial.

## Reproduction and independent verification

Run from the repository root:

```sh
python3 research/phase2/finite_fibre/compile_shared_source.py research/phase2/new_polynomials/source-46-semilocal.json.gz --output research/phase2/finite_fibre/polynomial-46-semilocal
python3 research/phase2/finite_fibre/verify_shared_specification.py research/phase2/new_polynomials/source-46-semilocal.json.gz research/phase2/finite_fibre/polynomial-46-semilocal/polynomial-specification.json
python3 research/phase2/finite_fibre/small_algebra_interpreter.py
```

The independent checker imports no producer. It verifies exact affine source
substitutions, the point equations and derivative guards, all quadratic
exceptional cases, denominator coverage, coordinate and finite-index
inventories, monicity, triangularity, and the degree/coefficient inequalities.
The separate exact small interpreter executes the full determinant and trace
construction on examples designed to test collisions, nilpotents, degree
drops, and zero quadratic cases.

## Bounds and identifiers

The independently verified rounded upper bounds are

```text
degree <= 2^296
coefficient height <= 2^(2^300).
```

Stronger unrounded integer bounds are in the specification. These are upper
bounds for the literal indexed polynomial, not expansion statistics. The
passing receipt is `verification.json`.

Specification SHA-256:
`dbfbe2a9ebe01fac2c7941b46273e0bd095e8818148288e21bc6385e788ac45a`.

Uncompressed source SHA-256:
`d4f95f2ebd7d769bb9459b32d1c3a9937b6c8f92837f265f22cf2c17d02fbc2d`.

Proofs are in `../finite_algebra_polynomial.tex`, `../source_shared.tex`, and
`../coefficient_bounds.tex`. The arithmetic characterization of the source
remains a separate dependency. No script commits changes.
