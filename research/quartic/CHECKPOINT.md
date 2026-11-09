# Quartic research checkpoint — 9 November 2026

## Candidate reduction, exact construction pending

The three-detector quartic can apparently be reduced from 351 to 348 total coordinates without changing the required local orders 1, 10, 40, the root/logarithm charts, the height argument, or the explicit scalar parameter.

At every consumed contact prime, delta=t-1 is a unit and q=q_1=1/(R delta^4) has odd valuation -v_p(R). Replace the old weights

  q_m = R^(1-2m) delta^(-2m-2)

by

  q'_m = q^(2m-1) = q_m delta^(-6(m-1)).

Their contact valuations are identical. Thus the distinct-valuation proof and all prescribed orders remain valid. At infinity all q'_m tend to zero faster; the factors and trace tend to 1 and 2. At fixed prepared finite primes, force delta to have nonpositive valuation by a fixed congruence on the prime-pattern denominator; then the new weight differs from the old by an integral factor, preserving all smallness requirements. This requires only the already assumed finite congruence freedom and has to be stated carefully in the proof.

For the existing five factor lists, the weight circuit already needs q^2, q^4, q^8, (q'_10)^2. Replace the four old toric auxiliary weights a,b,c,d by only three:

  q3=q*q2, q16=q8*q8, q76=q38*q38,
  q19=q16*q3, q38=q19*q19, q79=q76*q3.

q19 replaces q10 and q79 replaces q40. All rows are quadratic. Save one coordinate per detector: 351 -> 348; rows 323 -> 320. The same change in the two-detector six-factor circuit needs an extra q8 and saves no coordinate there, retaining 301.

This is a conditional projection improvement, inheriting exactly the previous arithmetic premises. No unconditional claim is made.

## Explored classes giving no improvement

`search_assignments.py` formulates a finite binary optimization for 16 tests assigned to at most seven valuation classes. It allows mixed orders in factors, all necessary repeated field squares, and new scalar weight squares. Starting from the original weight circuit, it recovers the costs of the existing 301/351 constructions. `assignment2.json` and `assignment3.json` record the solver outputs. This is computational evidence for that finite search class only, not a general lower bound.

A scan finds no purely linear residual and no coordinate occurring only linearly in the 301/351 quadratic systems, so straightforward elimination of a quadratic output used only linearly cannot remove a variable.

A fixed anisotropic binary norm would pair tests efficiently at chosen inert primes, but soundness must cover arbitrary contact primes. Such a norm splits at infinitely many of them. Without a new uniform contact restriction this is not a valid replacement.

## Stronger toric simplification — supersedes 348 candidate

A quadratic division identity reduces the weight circuit further. Put c=q^(-3), imposed by

  c*q4=q,  q4=q2^2, q2=q^2.

Then retain/add q8=q4^2 and impose

  c*q19=q8^2, q38=q19^2, c*q79=q38^2.

At every consumed contact prime q is nonzero, so c is nonzero and these equations force precisely q19=q^19 and q79=q^79. Completeness chooses these values on the nonzero domain. This replaces four old toric coordinates a,b,c,d by one c; in the two-detector circuit q8 must also be added.

Therefore the expected totals are:

* 301 -> 297, 275 -> 271 quadratic rows (two detectors; save two per detector).
* 351 -> 342, 323 -> 314 quadratic rows (three detectors; save three per detector).

The 348 construction and coefficients exist locally as an intermediate check, but 297/342 should be the delivered results once fully verified.
