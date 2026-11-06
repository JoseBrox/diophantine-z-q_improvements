# Targeted review of the assembled version-three paper

Reviewed `../diophantine_optimization_20261106_v3.tex`, specifically the
abstract, overview, system-combination section, lower-bound sections,
and optimization strategy. The unchanged mathematical proofs were not
rerun or rederived in this assembly review.

## Confirmed

- Preferred counts are consistently 41 and 43 for the indexed formulas,
  and 1315 and 1339 for the quartics. The previous 43/45 and 1367/1391
  constructions are explicitly retained as comparison constructions.
- The 41/43 degree bounds `2^9566673` and `2^236`, and the associated
  coefficient bounds, agree across the abstract, overview, theorem,
  and strategy section.
- The system-combination example correctly uses 1272/1296 residuals
  and exact norm-compiled degree 72 without additional coordinates.
- Total coordinates include the input; witnesses exclude it. System
  degree is total degree, including the input. The conic obstruction
  explicitly uses a different, stated measure: joint witness degree
  with unrestricted input degree.
- The claim about at most two quadratic equations in any ambient
  dimension is justified, including all number fields, nonzero guards,
  and finite unions. It is not overstated in the abstract.
- At least five total coordinates and at least three independent
  quadratic residuals are necessary for a quadratic definition. The
  detailed proof states the equation-count assertion after eliminating
  linear constraints. The abstract's weaker wording is also correct.
- Unrestricted lower bounds remain three total coordinates and degree
  four for one equation. A sign-changing quartic in three coordinates
  is not excluded. The remaining five-to-ten-coordinate quadratic
  range is not claimed to have a construction.
- The eighteen-dimensional point-module obstruction is consistently
  limited to preservation and separate decoding of the independent
  modules; it is not presented as a lower bound for all definitions.
- Arithmetic upper bounds retain their named source and prime-pattern
  assumptions. Lower bounds are unconditional. Division norms preserve
  the conjunction and do not establish arithmetic base-change claims.
- The strategy's numerical interface `k>12 deg(F)` agrees with the
  preceding direct-polynomial height calculation.

## Two small precision fixes requested

Both are in `systems_combination.tex`; no assembled file was edited.

1. In the coefficient-height part of the sum-of-squares proposition,
   add `P != 0` to the hypotheses of that sentence. The paper defines
   coefficient height only for nonzero polynomials, while the generic
   proposition otherwise permits every residual to be zero.
2. In the degree-72 example, say **a field-adapted reduced-norm
   construction** when discussing an arbitrary specified nonreal
   number field. The fixed supplied degree-36 form does not remain
   anisotropic over every extension; the later full construction
   already states the distinction correctly.

No other necessary count, hypothesis, or proof-integration correction
was found in the targeted sections.
