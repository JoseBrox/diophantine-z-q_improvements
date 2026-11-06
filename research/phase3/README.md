# Direct Lucas constructions, small-variable limits, and number fields

## Current result and scope

The best construction supplied here has **41 total variables**, including
the input, and 40 existential witnesses. **A definition with 2–10 total
variables has not been obtained.** Two total variables are impossible;
the unrestricted cases of 3–10 variables remain unresolved here.

The interpretation of the new polynomials as definitions of the ordinary
subset `Z` of `Q` remains **conditional on the named arithmetic lemmas in
the pinned source and Sun, arXiv:2610.20691v2, Theorem 4.1**. The exact
algebraic checks do not certify those arithmetic inputs. No novelty,
optimality, or independent human-review claim is made.

Pinned revision: `28e87b1b62af0effd954605af7f70b2699dd5672`.
The released manuscript and the preceding complete paper are unchanged.
The working branch is `research/polynomial-optimization`. No commit, push,
or pull-request submission has been made.

The fresh, standalone paper is
**`diophantine_optimization_20261106_v3.tex`**. It contains all definitions,
proofs, dependencies, prior comparison constructions, and 38 bibliography
entries. It is organized by mathematical topic. Static TeX checks pass;
no rendered PDF is claimed.

## Preferred polynomials over the rationals

All variable counts include the input. Large degree figures are upper
bounds; the quartic degrees are exact.

| Package | Variables | Degree | Coefficient height |
|---|---:|---:|---:|
| `finite_fibre/polynomial-41` | 41 | at most `2^9566673` | at most `2^(2^86098382)` |
| `finite_fibre/polynomial-43-semilocal` | 43 | at most `2^236` | at most `2^(2^240)` |
| `quartic/quartic-direct-translated` | 1315 | 4 | exactly `64*3^(2^28)`, less than `2^429496736` |
| `quartic/quartic-direct-small-coefficients-1335` | 1335 | 4 | less than `2^1020` |

The 41- and 43-variable packages are exact indexed determinant and finite
product specifications. The enormous matrices and outer products are
not expanded. The preferred translated 1315-variable table has 29,021
ordinary coordinate monomials and coefficients expressed using the fixed
integer `s=3^(2^27)`. The preferred 1335-variable table has 29,050 ordinary
integer terms. All have passing independent-check receipts.

For comparison, the untransformed 1315-variable table has 28,991 encoded entries over
`Z[kappa]`, or 28,987 distinct monomials after collecting the coefficients
in the specified constant kappa. Kappa is not a variable. The 1339-variable
table has 29,061 ordinary integer terms. The intermediate 1338-variable
table is also retained. The distinction between encoded coefficient
entries and monomials after specializing a fixed constant is checked.

The final affine substitution acts only on three private anchor
witnesses and preserves literal polynomial projections over every
characteristic-zero field. The constant-chain eliminations remove its
last squaring coordinate and inline the first three known constants,
giving 1335 coordinates at the same coefficient-height bound. They
preserve residual systems over every field and the sum-of-squares
projection over every field having a real embedding.

Two more checked indexed packages use `beta=X^2+2402`, with the same
counts and recorded degree/height bounds. They repair the finite scalar
contact obstruction in fields having a real embedding. This is not an
arithmetic proof over those fields.

The improvement replaces three comparisons with rational Lucas proxies
by a direct test of

`F(U,V,W)=V^2-U(U-2)VW+(U-2)^2 W^2-1`

at approximate logarithmic ratios. Integral congruences transfer this
polynomial relation to the same integer residual used by the height
proof. Two retained proxies and one algebraic generator disappear. There
are sixteen tests rather than eighteen. The preferred finite source has
40 retained coordinates, nine quartic and ten quadratic generators, and
rank at most `2^28`. One final compiler witness gives 41 coordinates.

## Several equations and lower bounds

- Over `Q`, or any number field having a real embedding, the sum of
  squares combines finitely many equations without a new variable.
  Quadratic equations give one quartic.
- Over any specified number field, a division-norm form combines `r`
  equations of degree at most `D` into one of degree at most
  `D*ceil(sqrt(r))`, again without adding variables. Integer coefficients
  suffice for the combining form, chosen using the specified field.
- Thus finite systems and one equation have the same minimum variable
  count when the degree is unrestricted. Guards can cost an additional
  coordinate and are not silently ignored.
- At most two quadratic equations, in any number of coordinates, cannot
  have an infinite input projection contained in a number field's ring
  of integers. A quadratic defining system needs at least five total
  coordinates and three independent quadratic equations, after linear
  elimination. This does not rule out five through ten coordinates.
- Any finite system defining a ring of integers needs at least three
  total coordinates. A single defining polynomial needs degree at least
  four. The earlier nonnegative-polynomial and conic-specialization
  bounds remain in the complete paper.

## What blocks the proposed shortcuts

The specific cyclic elliptic group is geometrically dense in its
two-dimensional Weil restriction. Covering nine independent copies by
finite algebraic decoding therefore needs at least eighteen retained
parameters. This is a restriction on that decoding strategy, not a
universal eighteen-variable lower bound for integrality.

No arbitrary finite Boolean combination, even allowing negations, of
perfect-power denominator predicates applied to fixed rational functions
of the input can define `Z`. If it contains almost every integer, it also
contains infinitely many nonintegers converging to an integer. A separate
mod-two rank argument blocks aggregation by too few fixed monomials.

The literature review distinguishes integer pairing, conditional
polynomial injections on all rational pairs, rationally injective
elliptic surfaces, and an injection on a bounded set with a fixed finite
denominator-prime support. None supplies the required rational decoder
or a 2–10-variable construction here.

## Checks over number fields

The literal quartics, including all final transformations, accept
every input in every characteristic-zero field containing `i`. A generic
section is checked against the complete coefficient tables.

The unshifted indexed formulas equal **1 identically** at inputs satisfying
`X^2=2399`, `X^2=-1`, or `X^2=-2`; the guarded quadratic source systems
reject them as well. These inputs are algebraic integers. The shifted
packages are explicitly outside this counterexample's scope.

An explicit totally real quartic field contains a point outside the fixed
cyclic group that passes every finite elliptic anchor exclusion at fixed
height. This is a counterexample to an essential arithmetic inference,
not a full false-positive witness for the entire source.

The preferred norm repairs are explicit degree-72 determinant
specifications with the preferred 1315/1335 coordinates. Their coefficient
height bounds are respectively `2^7730941609` and `2^18757`. The fixed degree-36
norm is anisotropic over `Q`, `Q(i)`, and number fields of degree coprime
to 36; field-dependent choices give degree 72 for any specified number
field. These preserve the recorded quadratic systems, including their
arithmetic failures. They do not define the new ring of integers.

A fixed finite existential formula cannot define every number field's
ring of integers. The proof uses constructibility; it permits equations,
guards, and finite alternatives. The separate question of existence of a
different definition for each field remains unresolved in this work.

## Verification and reproduction

`verification-index.json` binds the checked source/specification/table
bytes to their independent receipts. It records four indexed packages,
five full quartic tables, seven norm specifications, two independent exact
point-depth checks, the field counterexamples, and paper consistency.

Run from the repository root:

```sh
python3 -E -B research/phase3/compression/check_direct_source.py
python3 -E -B research/phase3/number_fields/check_quartic_base_change_20261106_v1.py
python3 -E -B research/phase3/number_fields/check_contact_exclusions_20261106_v1.py
python3 -E -B research/phase3/number_fields/check_real_anchor_20261106_v1.py
python3 -E -B research/phase3/number_fields/verify_division_norm_specs_independent_20261106_v1.py
python3 -E -B research/phase3/assemble_phase3.py
python3 -E -B research/phase3/verification_index.py
python3 -E -B research/phase3/make_checkpoint.py
```

Detailed source-producer, generic compiler, and quartic commands appear
in the paper's reproducibility appendix. The generic finite-algebra and
quartic checkers in `research/phase2/` are reused without modification.
Neither the new independent norm checker nor the quartic checker imports
the corresponding producer.

## Next mathematical work

1. Independently settle the named source and Sun arithmetic dependencies.
2. Seek a simultaneous rational-solubility theorem allowing several pole
   witnesses or elliptic point choices to share parameters, or replace the
   height/Lucas mechanism with one needing fewer independent choices.
3. Improve the explicit height constant or find a less costly size
   condition at the same variable count.
4. For number fields, replace the fixed cyclic-group argument or prove
   the required existential isolation of the embedded rational field.

Reapplying the finite primitive-element compiler or using rational
pairing alone does not establish any of these missing assertions.
