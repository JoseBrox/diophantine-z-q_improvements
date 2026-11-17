# Primary-source audit for alternative variable compression

Date: 17 November 2026. This is a research checkpoint, not a new polynomial construction. The source sweep found no verified theorem lowering the established general25, fixed weak-abc13 or ordinary-abc11 counts.

## Existential rank

N. Daans, P. Dittmann and A. Fehm, Existential rank and essential dimension of diophantine sets, arXiv:2102.06941v5, Corollaries4.21 and5.11:
https://arxiv.org/pdf/2102.06941

For two Diophantine sets of positive existential rank over Q, their intersection has rank at most the sum of the ranks minus one. In characteristic zero, Theorem4.16 identifies essential fibre dimension with max(positive-existential rank minus one,0). The proof uses a transcendence basis and one primitive algebraic element.

The present two intrinsic pole blocks have two free parameters and one finite root each. Their conjunction already uses four free parameters and one shared encoder, the five witnesses furnished by the intersection estimate. Point roots are absorbed into that encoder too. No additional deletion follows from applying the theorem again. This is a comparison with this construction, not a theorem that its rank is minimal.

Remark8.23 bounds the universal one-input existential rank of Q by twelve times the existential rank of Z in Q, assuming the relevant Diophantine input. That bound does not lower the latter rank.

The root reopened and checked Corollary4.21 and the essential-dimension statement directly.

## Rational injections

H. Pasten, Bivariate polynomial injections and elliptic curves, arXiv:1811.02416, Theorem1.1 and Corollary1.2:
https://arxiv.org/pdf/1811.02416

This gives an unconditional regular-function injection V(Q) x V(Q) -> Q for a suitable affine open V in a positive-rank elliptic curve. The generic surface-to-line fiber is one-dimensional. Rational injectivity supplies neither finite algebraic recovery nor a lower-cost existential decoder; it cannot simply replace two retained point coordinates in the finite-algebra specification.

B. Poonen's polynomial injection Q^2 -> Q uses a nondensity hypothesis implied by Bombieri-Lang for surfaces. The alternative generalized-abc condition quoted there is a four-term form, not the ordinary rational abc premise used by the present eleven-variable construction. Neither assertion includes the missing decoder.

M. Hirvensalo, On injective multivariate polynomials over rational numbers, DOI10.1016/j.tcs.2026.116158, Theorem2:
https://doi.org/10.1016/j.tcs.2026.116158

The examined theorem's domain is Lambda_Pi=Z[1/Pi] intersect [0,1], for fixed finitely many odd primes Pi. It is not an injection theorem on all Q^2. The research reviewer checked that restricted domain; the root's attempted DOI reopening was blocked by the publisher redirect. This item is not used as an arithmetic input.

## Fixed local integrality

N. Daans, Universally defining Z in Q with 10 quantifiers, arXiv:2301.02107, Propositions4.2,4.8 and4.10:
https://arxiv.org/pdf/2301.02107

Proposition4.2 gives a three-quantifier existential integrality definition at a fixed finite prime set, with coefficients selected for that set by approximation. Proposition4.8 combines tests at that same fixed set. These statements do not uniformly consume the input-dependent collection of all relevant contact primes. The variable-quaternion family in Proposition4.10 uses six quantifiers. No reduction of the current free pole parameters follows.

## General Diophantine coding

B. Bhatt and B. Poonen, Diophantine sets, 3 July2026, Theorems3.4 and4.4:
https://math.mit.edu/~poonen/papers/diophantine.pdf

The affine replacement theorem gives an affine finitely presented scheme mapping surjectively on points of a finitely presented scheme over every base algebra. It provides no dimension or variable-count bound. The equivalence of formulations of Diophantine definability also supplies no coordinate reduction.

H. Pasten, Notes on the DPRM property for listable structures, arXiv:2012.14054:
https://arxiv.org/pdf/2012.14054

Its catalogue result gives bounded existential rank once the DPRM property holds, without the small numerical bound needed here.

## Direct recent arithmetic sources

A. Burungale, A Diophantine definition of Z in Q, arXiv:2611.16130v1:
https://arxiv.org/abs/2611.16130

A. Kozachinskiy, H. Pasten and X. Vidaux, arXiv:2611.17124v1:
https://arxiv.org/abs/2611.17124

The review found only the12November v1 submissions in their current version histories. Burungale does not give a numerical quartic variable count in the reviewed text, and its index-to-integer passage uses a recursive encoded relation. The other paper retains the same quadratic-field elliptic curve and states ordinary abc, Dickson and the relevant2-primary Tate-Shafarevich finiteness assumptions. No cheaper complete source was obtained from them.

## Upstream explicit quartic

The separately pinned upstream v19 release gives a reported explicit250-variable quartic. See external_candidates/upstream_explicit250_v19.md. It awaits coefficient reproduction and arithmetic audit before replacing the improvements repository's certified explicit record. It does not change the25/13/11 or ordinary-abc71 targets.

## Review scope

The research agent inspected the cited primary statements and their hypotheses. The root separately reopened the DDF theorem, Pasten and Bhatt-Poonen primary files, and the pinned upstream release description. No inference from an injection, an affine replacement or a nonquantitative rank bound to a numerical existential-coordinate saving is made.
