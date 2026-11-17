# Independent mathematical review

**Status: PASS.** Reviewed on 17 November 2026 by `/root/nine_realization`. No material gap was found in the two stated counterexamples or in their stated scope. The producer and manuscript were not modified.

## What was checked

The separate `check_independent.py` imports neither the producer nor a computer algebra system. It reconstructs both native products by arithmetic in pairs representing `Q(sqrt(2))`, checks every recorded rational invariant, verifies all claimed valuations and local square classes, checks the reduced denominators as exact integer squares, and verifies the real inequalities. It also checks the two curve maps by sparse polynomial coefficient arithmetic after clearing denominators.

For the first obstruction, the identity

\[
\Delta(q,V)=(q^2+1)^2+4(V-1)q(q^2-1)
\]

works for every local scalar, including those with poles. At the prime `100003`, the denominator `q^2+1` is a unit for integral `q`. For `e=v_p(q)<0`, the relative correction has valuation `v_p(V-1)-e>0`. Thus the multiplier is always a nonzero local square, whereas the exact fixture makes `C` a nonsquare unit. The universal quantifier is proved by this argument, rather than inferred from a finite search.

For the second obstruction, the prime is inert in `Q(sqrt(2))`. The integer congruence for `u` gives `v_p(w)=-4`; the chosen field element `h` has valuation three and `v_p(Tr(h^2))=7`. Consequently the first term in the expansion of `Tr((1+wh^2)^-1)` has valuation three, whereas subsequent terms have valuation at least four. This gives `v_p(2-V)=3` and `v_p(C)=-1`. Since `-1` is a nonsquare modulo the prime, `1+r^2` always has even valuation for every `r` in the local field. Taking `r=wV^2c^2` proves exclusion for every scalar `c`.

The denominator proof is valid globally: `b=u` times a rational square. At an odd prime dividing the positive integer `u`, the integral field element `h` makes both native slots units congruent to one, so the valuation of `b` is positive. At every other odd prime, its valuation is even. The explicit two-adic preparation deals with the remaining prime. Both exact reduced denominators were also independently tested as integer squares.

The stated strengthening of preparation at an arbitrary fixed finite set away from the fresh prime is compatible with the constructions. Increasing the required finite-place divisibility and then choosing a sufficiently large positive representative of the specified residue classes preserves the fresh-prime obstruction. The resulting real bounds and local closeness follow from the displayed formulas. This does not create an actual elliptic-source lift.

## Curve calculations

The quartic-to-cubic transformation and the subsequent two-isogeny are exact, and the converse of the first transformation correctly retains an abscissa square-class condition. Positive rank of the final congruent-number curve alone would not settle that condition.

There is an independent short discriminant calculation for the first family. Divide the quartic by `q^2` and put `t=q-1/q`. The resulting quadratic is

\[
t^2+4(V-1)t+4.
\]

For its roots `t_1,t_2`, one has

\[
(t_1-t_2)^2=16V(V-2),\qquad
(t_1^2+4)(t_2^2+4)=64(V-1)^2.
\]

The quartic discriminant is their product with the first expression squared, namely `16384 V^2(V-2)^2(V-1)^2`. On `1<V<2`, its roots are simple and none is `q=2`. Pulling back by `q=2+wc^2` therefore gives eight simple roots, hence genus three. The second quartic has nonzero constant and leading terms and no repeated root, hence genus one.

## Scope

These are exact prepared **abstract native products**. The manuscript explicitly leaves their elliptic test tuples and physical contact lifts unproved. The results exclude completeness of the proposed scalar replacements on the stated abstract class; they do not exclude other actual witnesses, do not disprove either target realization theorem, and do not give a lower bound on defining variables. That distinction is consistently maintained.

File hashes and a machine-readable review record are in `independent_review.json`.
