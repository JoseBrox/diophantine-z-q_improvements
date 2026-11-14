# Smaller degrees and coefficient heights

The new constructions preserve the rational input projections of their specified sources. **All variable counts and all arithmetic hypotheses are unchanged.** The underlying prime-pattern, pole-realization and height audits are not declared complete by these algebraic results.

## Few-variable constructions

| Source | Total variables | Previous degree bound | New degree bound |
|---|---:|---:|---:|
| Inherited arithmetic premises |25|<2^85|**<2^78**|
| Fully specified, same premises |27|<2^87|**<2^80**|
| Weak abc, exponent 121/100 |13|<2^44|**<2^38**|
| Weak abc, exponent 16/15 |13|<2^44|**<2^38**|

The exact majorants and support bounds are in the [data record](../data/algebraic_improvements_20261113_v24.json). The [paper](../papers/finite_algebra/triangular_separation_20261113_v24.pdf) gives the full algebraic projection proof, all exceptional cases, and the coefficient algorithm. The [computation directory](../computation/few_variables/triangular_elimination_v24/README.md) contains the specifications and separate checkers.

The fully specified27 polynomial retains **L=20483** and now has coefficient height less than **2^(2^92)** instead of 2^(2^99), under its inherited premises. The other three stored numerical members remain algebraic fixtures with no certified defining parameter; their coefficient norms are not bounds for a numerically certified integer-defining member.

The construction separates the quadratic roots using coefficients that contain products of earlier radicands. This avoids a lower bound on every nonzero radicand. Separate point-root and radicand bounds, together with determinant truncation to the appropriate dimension, lower the degree without changing the arithmetic source.

## Quartic coefficient improvement

For the pinned 214-variable quartic, an invertible rescaling of six witness coordinates gives

    H(P_N) = max((5898050446009651968 *31581660^28)^2,
                 31581660^28 *149^(2N)).

For N>=57 this is **31581660^28 *149^(2N)**. It is strictly smaller than the old height 149^(4N+2)+1 for every N>=53. The new quartic has the same 214 variables,188 quadratic rows and 2919 coordinate monomials. The [paper](../papers/quartic/coefficient_balancing_20261113_v24.pdf) proves exact rational projection equivalence and the height formula. The [complete tables and checker](../computation/quartic/balanced214_v24/README.md) verify all coefficients.

This does not promote the214-variable arithmetic theorem to independently accepted status, nor does it supply an effective defining N. The coefficient thresholds 53 and 57 must not be confused with that ineffective threshold.

## Verification and remaining work

The new checks comprise four independent numerical bound reconstructions,13 exact finite-algebra examples, and all 188 source/transformed quadratic rows and 2919 quartic coefficient profiles. Deliberate coefficient, degree and projector errors are rejected. Both papers have complete TeX sources and inspected PDFs. The [audit continuation](audits/continuation_20261113_v24.md) states the exact source, review and execution limits.

No smaller variable count was proved in this continuation. The next mathematical targets are fewer elliptic point roles, fewer pole parameters, and a quadratic treatment of the rescaled contact equations that preserves all rational solutions.
