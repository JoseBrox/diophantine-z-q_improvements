# Priorities for reducing the total coordinate count

The verified baseline remains 27 total coordinates for the existence family and 29 for the explicit construction. Improving the finite-root compiler changes degree and coefficients; it does not remove retained rational coordinates. None of the proposals below has a complete projection proof or a new certified count.

## 1. Prove a complete pole certificate with one retained parameter

This is the most isolated reduction problem, and it can be tested independently of the elliptic-index argument. For a prepared input b, put B=17b and V=B(B-b²). Fixing the allowed degenerate value e=-1/3 leaves the quartic

    B q² = (s²+V/3)(s²-V).

Only s would remain a free rational parameter; q is a finite algebraic choice. The same reduction could be applied independently to the comparison and scalar poles.

**Next lemma needed.** For every b satisfying exactly the current preparation hypotheses, the displayed quartic has an affine rational point with q nonzero, under the inherited arithmetic inputs. A useful first investigation is exact local solubility and 2-descent in explicit prepared families, for example b=(204/M)² with M>50 and gcd(M,102)=1. A certified counterexample would decisively reject this specialization and direct attention to another fixed rational curve inside the pole surface.

**Proved restriction.** The existing simultaneous-realization theorem chooses a fresh twist; it does not supply this fixed specialization. Sharing a nondegenerate e instead forces equal squareclasses of the pole inputs. Sharing the chart parameter tau avoids that particular obstruction, but requires a separate simultaneous rational-point theorem. These are distinct questions. Pole savings alone cannot reach the under-ten target while retaining all nine elliptic points.

## 2. Eliminate the separate input point through a new scalar local certificate

The input label and its auxiliary multiple occupy two elliptic-point roles. Identifying that label with the scalar label would remove both roles, provided completeness survives. The new uniformly bounded scalar normalization resolves the real approximation issue: S-P need no longer lie in a specially chosen real neighborhood. Its constants and exceptional primes are independent of L, and its fixed-prime index forcing remains valid.

The remaining obstacle is arithmetic. Setting a=κ(X), with κ integrality-reflecting and κ(X)-1 highly divisible by the input contacts, does not make [a-1]P formal: the varying reduction orders must also divide a-1.

**Next lemma needed.** Construct a replacement scalar certificate whose soundness still gives the required contact divisibilities and fixed-prime index depth, but whose completeness for the prescribed index uses those integer divisibilities without assuming formal-group membership of [a-1]P at every contact prime. Alternatively, encode the required annihilating multiples through a correspondence that introduces fewer free coordinates than the two removed point roles. The finite-place condition must be proved for every integer input, not checked on examples.

**Proved restriction.** Merely making κ(X)-1 a larger power of the contact product does not remove the reduction-order factors. The index is also not recoverable by a finite algebraic extension of the point coordinates: its graph with [n]P is Zariski dense. If the replacement local certificate cannot overcome this obstruction, this identification should be abandoned rather than assigned an optimistic count.

## 3. Replace the paired-place integer-label mechanism

A credible route below ten ultimately needs a much smaller collection of point roles. A rational rank-one elliptic curve would use fewer rational coordinates per point, but it needs a different local mechanism. A concrete starting point is divisibility of its integer indices, using elliptic divisibility sequences together with the existing pole obstruction.

**Next lemma needed.** On a fixed, explicitly verified rank-one curve over Q, construct a Diophantine relation on nonzero multiples Q=[n]P and R=[m]P that detects n|m, using a small fixed number of unrestricted rational parameters and finite roots, with a complete local-to-global proof. This would permit testing an integer-label construction based on divisibility instead of the present conjugate formal-logarithm comparison. Denominator divisibility and divisibility of indices must be proved equivalent in the stated range; small indices, torsion, and bad primes need explicit treatment.

**Proved restrictions.** On a rational curve, the current requirements that H be formal at one split place and H-P at the other force P itself to reduce to the identity. Two rational curves linked by an algebraic curve of common-index pairs yield an isogeny relation, which prevents infinitely many coprime-order reductions. Neither substitution repairs the existing mechanism.

There is also a stronger restriction on the output map. Corvaja–Zannier, *Rational and integral values of rational functions at rational points*, [arXiv:2608.28255v1, Theorem 1.1](https://arxiv.org/html/2608.28255v1), prove that a finite union of rational images of finitely generated subgroups of semiabelian varieties misses infinitely many rational integers. Consequently fixed rational functions on finitely many powers of E(K) cannot cover all integers. This does not exclude unrestricted affine parameters or genuine algebraic correspondences; a replacement construction must make substantive use of such additional structure.

The effective one-scalar height problem remains valuable for making the smaller existing construction explicit, but it should run separately: by itself it does not remove a retained coordinate.
