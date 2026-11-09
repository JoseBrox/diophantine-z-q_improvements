# Three next questions for number fields

The first test field should remain **K=Q(i)**. Its exact elliptic point
stability is certified, but no definition of Z[i] in Q(i), and no
counterexample to such a definition, has been established here.

## 1. Can an additional global constraint produce bounded denominators?

Find an explicit existentially defined set S in K and a fixed positive
integer M such that

**Z ⊆ S and M S ⊆ Z[i].**

Every witness must range over K. A bound depending on the input, or
integrality at only finitely many fixed primes, is insufficient. Success
would define Z[i] immediately by the proved finite-union and integral-basis
criterion.

The required new ingredient cannot consist solely of fixed rational
operations on stable elliptic coordinates. Corvaja–Zannier’s Theorem 1.1
proves that every finite union of rational-map images of points on fixed
abelian varieties misses infinitely many rational integers. Products of
abelian varieties and Mordell–Weil extend this obstruction to all fixed
finite sums, products, and ratios, including finite exceptional values.
Our degree-eleven slope condition therefore also fails integer
completeness. This closes that particular approach, rather than merely
leaving its completeness unproved.

Poonen’s 2026 integral-basis step directly supports the final transfer.
Its approximation-to-integrality arguments are useful models for a new
global constraint, but their existing integral witness domains cannot be
silently enlarged to K.

## 2. Can a finite algebraic correspondence escape that obstruction?

Test the following precise next class: a variety V with a generically
finite map to a power E^r, together with a rational function h on V.
Can h(V(K)) contain every rational integer while having uniformly
bounded denominators? Here the output may be algebraic, rather than a
fixed rational function, over the elliptic coordinates. Unrestricted
additional affine witnesses are a second possible departure.

For curves finite over E, Siegel’s theorem already prevents infinitely
many bounded-denominator values of a nonconstant h: after removing its
poles, such points are integral outside a fixed finite set. Thus the
first serious case has dimension at least two.

Corvaja–Zannier does not automatically cover these correspondences.
Faltings’s and Vojta’s integral-point and Mordell–Lang results can settle
special cases once the relevant variety, subgroup, and divisor hypotheses
are verified. Stronger general height assertions discussed in
Corvaja–Zannier §3 are explicitly conditional on Vojta’s conjectures.
They must not be substituted for proved completeness or nonexistence.

## 3. Is any infinite bounded-denominator rational subset Diophantine in Q(i)?

Seek either an example, or a theorem that every Diophantine
S ⊆ Q inside Q(i), with M S ⊆ Z for some fixed M, is finite.
The latter would be a genuine undefinability result. Combined with the
known integral-witness definition of Z in Z[i], it would imply that
Z[i] is not Diophantine in Q(i). Our dense rational set is consistent
with such an obstruction because its denominators are unbounded at
every prime.

This requires control of arbitrary existential varieties, beyond
abelian rational maps. Fehm’s and Kwon’s large-field theorems cannot
supply it: no number field is large. Mazur–Rubin–Shlapentokh’s
rank-stability transfer, and Poonen’s related 2026 work, concern
integral witnesses; they supply the integral-domain input, not this
whole-field obstruction or an existential definition over K.

## Primary references

- Corvaja–Zannier, appendix by Masser, [arXiv:2608.28255v1](https://arxiv.org/abs/2608.28255v1), Theorem 1.1 and §3.
- Poonen, [*Rank stability makes rings of integers diophantine*](https://math.mit.edu/~poonen/papers/h10_over_OK.pdf), 3 July 2026, §4.
- Mazur–Rubin–Shlapentokh, [arXiv:2208.09963v3](https://arxiv.org/abs/2208.09963v3), Theorem 1.1 and §14; 2024 corrigendum.
- Fehm, *J. Algebra* 323 (2010), 1738–1744; Kwon, [arXiv:2411.03212](https://arxiv.org/abs/2411.03212).

