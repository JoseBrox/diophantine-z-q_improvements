# Independent audit: arbitrary contact amplification

Reviewed source:
`../independent_route_v56/amplified_index_pole_v59.tex`.

## Verdict and scope

The arithmetic theorem, completeness for every integer index ratio,
and whole-character detector guards pass. The result is conditional
on weak rational abc(4/3), with the cyclic point subgroup and fixed
exceptional-index restriction stated in the manuscript. It does not
identify an external rational input with the quotient, and no complete
defining-polynomial compiler or variable bound is claimed.

## Formal logarithm

For t=−x/y, the curve gives
x=(1+sqrt(1+4d²t⁴))/(2t²). Direct differentiation gives
dx/(2y)=dt/sqrt(1+4d²t⁴). Expanding the binomial series and integrating
produces exactly

`sum_{r>=0} (-1)^r binom(2r,r) d^(2r) t^(4r+1)/(4r+1)`.

The truncation Lambda_T is an odd polynomial beginning with t.
For p>T+1 and every r≥T+1, r−1−v_p(r)≥T. At depth e≥1 this
gives v_p(t^r/r)≥(T+1)e. The full logarithm and its truncation
have valuation e, so the relative tail error has valuation at least
Te. Applying log([m]H)=m log(H), with integer m and the standard
formal-group valuation inequality, proves the stated quotient error
uniformly in m, including p dividing m.

## Exact valuation threshold

Set k=8T−7. At a simple denominator prime of H, v_p(u)=k.
Every detector factor has nonpositive valuation. If v_p(D2)≤k/4,
then v_p(b)≤4v_p(D2)−k<0; the right side is an odd integer.
The intrinsic pole equation excludes this. Therefore
v_p(C2)>k/8=T−7/8, and integrality of the valuation gives
v_p(C2)≥T. The logarithm approximation then gives v_p(X−m)≥T.

For true input X=m, at positive odd denominator depth e,
the two tests have valuations at least2Te andTe. The first W-factor
is a unit; the second has valuation at least min(0,(4T−k)e).
Thus v_p(b)≥min(k,8T−k)e=min(8T−7,7)e>0.
Negative odd u-valuations are handled automatically by the balanced
transform, and even valuations give even b-valuations. This includes
all primes outside the fixed preparation set.

At2 the fixed initial point can be chosen sufficiently deep to
dominate the finitely many truncation coefficient denominators and
the fixed threshold2k. This choice works uniformly in integer m.
The previous local-square preparation gives v2(u)=4k and v2(b)=2+4k.
At7 the fact that−1 is nonsquare prevents cancellation in
1+u C_i²; hence W≡1 and v7(b)=2k. Real u>50 bounds the balanced
tests independently of their values and gives0<b<1/7.

## Whole-character guards and finite subgroup covers

At the chosen rational abscissa roots q_H,q_U, the finite roots
l_H²=q_H⁴−d² and l_U²=q_U⁴−d² are real and nonzero. Their image
point characters are H or−H and U or−U. Since Lambda_T is odd,
Lambda_T(ζ(−H))=−Lambda_T(ζ(H)); the added logarithm guard is
therefore nonzero on every image character whenever it is nonzero
on the selected one. All other test values are real. The common
positive weight u is independent of the ordinate signs, so every
balanced denominator, every W-factor and b are strictly positive
at every image character. A nonzero odd polynomial composed with
the nonconstant function ζ has only finitely many zeros on E, so
the logarithm guard removes only finitely many actual index choices.

For a rank-one congruent curve and an appropriate fixed even L,
the subgroup restriction to ZP=[L]E(Q) is realized by the finite
isogeny cover [L]R=H, and similarly for U. The cover is finite and
étale in characteristic zero. Adding its coordinate functions gives
a finite algebraic extension rather than another free point
coordinate. Some preimage characters can be nonreal; this does not
alter the real image coordinates H±,U± or the detector values just
audited. Rational characters of the cover impose the desired
rational preimage condition. A complete one-encoder polynomial
specification must still choose and verify that finite algebra and
its guards; the current manuscript correctly makes no such full
compiler claim.

For each nonzero image value eta, the intrinsic radicand is a
nonzero polynomial in the two pole parameters. Its other-character
norm factors are likewise nonzero polynomials. The retained
intrinsic density theorem avoids their finite union of zero sets,
along with the rational division guards. No new free parameter is
needed for these exclusions.

The remaining growth inequality in the manuscript follows exactly
by multiplying the simple denominator support by the fixed exponent
T. Its existential encoding remains open; the proof does not infer
it from real inequalities or finite congruences.
