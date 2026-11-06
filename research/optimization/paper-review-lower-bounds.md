# Mathematical review of the assembled report

The reviewed sections are the definitions and reduction, exact quartics,
unconditional lower bounds, and number-field transfer results in
`diophantine_optimization.tex`. No substantive mathematical defect was found
in these sections.

The lower-bound proof correctly handles cubic cones, geometrically reducible
irreducible cubics, the curve quotient, and all archimedean embeddings of a
number field. Kollár's Theorem 2 was checked again in the primary paper:
<https://arxiv.org/pdf/math/0005146>. Its hypotheses and conclusion agree
with the stated application.

The exact decimal decomposition of the constant term `H0` was checked against
the independent 12,449-variable verification receipt and agrees. The proof
should explicitly mention that specialization of its table over `Z[M]`
cannot remove a monomial: every nonconstant coefficient is `a+b*M`, with
`|a|<2^3247<M`, while the only quadratic coefficient in `M` is the positive
constant term. This supplements the existing height and variable-dependence
arguments.

The published number-field references were checked at their primary sources:

- Koymans–Pagano, Theorem 1.2:
  <https://arxiv.org/html/2412.01768v3>.
- Alpöge–Bhargava–Ho–Shnidman, published Corollary 1.2:
  <https://link.springer.com/article/10.1007/s00222-025-01392-3>.

Both published statements establish Diophantine definability of the ordinary
subset `Z` in `O_K`. The linked ABHS arXiv v1 instead phrases its corollary in
terms of a Diophantine model. The report's attribution is correct for the
published version; specifying that version avoids a misleading comparison
with the older preprint wording.

Editorial and verification-scope suggestions sent to the assembling author:

- Replace the literal text `A model,+an` by `A model, an`.
- Replace `smaller exponent count` after the 12,449-variable result by
  `smaller variable count`.
- Unless separately recorded, do not say that deliberately corrupted maps
  and final output coefficients were tested: `negative-checks-12476.json`
  records seven pivot, row-operation, occurrence-list, patch and coefficient
  mutations. The positive checker does validate the entire map and output,
  but that is a distinct claim.

The proposed 853-variable producer was also reviewed independently. Its
primitive-element formula, reciprocal guard, homogenization induction and
renumbering are correct. `polynomial-853/producer-review.json` records the
additional exact inventory checks. The complete emitted-DAG equivalence
audit is a separate verifier, not claimed by this prose review.
