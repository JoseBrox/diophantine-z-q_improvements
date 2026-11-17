# A constant-only alternative to the coherent weight change

This is a complete algebraic and arithmetic reduction of the same-count
Burungale transfer. It does not save variables. Independent audit pending.

## Scalar change

Both retained general scalars have the form

\[
\rho_L(X)=\frac{A_L r(X)}{(1+C_L r(X))^2},
\]

where `r` is an integer polynomial, positive on the real line and
integer-valued on integers. For the original scalar

\[
A_L=102^2\ell^L,\quad
r=\beta(\beta-1)(\beta-2401)(32\beta+343)(2\beta-1),\quad
C_L=17(\ell^{(L+1)/2}+1),
\]

with `beta=216X^4+450459`, `ell=76249`. For the aligned scalar,
use `r=R`, `A_L=102^2 ell^L M`, and
`C_L=102^2 M(ell^((L+1)/2)+1)` exactly as in its manuscript.

Set

\[
k=1+4\ell=304997=7\cdot11\cdot17\cdot233,
\qquad
\rho_L^*(X)=\frac{49 A_L r(X)}{(1+kC_Lr(X))^2}.
\]

Use `rho*` in every scalar and comparison-scale occurrence. Retain the
already established per-block physical weight

\[
u_j=\rho^*R_j,\qquad w_j=u_j/(1+u_j)^2.
\]

Thus the native square-criterion hypotheses are preserved, unlike a
return to unnormalized physical weights. No additional rational
coordinate or per-block expression is introduced by this scalar change.

## Properties valid for every rational input

The exact ratio is a rational square:

\[
\frac{\rho^*}{\rho}
=\left(7\frac{1+C_Lr}{1+kC_Lr}\right)^2.
\]

All denominators are nonzero for real inputs because `C_L r>0`.
Odd scalar valuation support is unchanged. Outside the fixed exceptional
set and away from `ell`, at a finite odd contact of `r` the two
denominators are units and the odd valuations themselves are unchanged.
At all other primes outside that set and `ell`, the scalar valuation is
even in both specifications.

At `ell`, the multiplier `k` is a unit and is congruent to one. If
`v_ell(r)>=0`, the existing exact residue certificate makes the old
denominator a unit, and the new denominator has the same residue. If
`v_ell(r)<0`, both denominators have valuation `v_ell(r)` because
`C_L` and `k` are units. Therefore the consumed-prime valuation is
unchanged for every rational input. In particular it is positive odd
and at least `L`.

The scalar's integrality-reflecting label is unchanged. The scalar
contact-height proof is unchanged, and its height estimate has the
same exponents with a different absolute constant. Indeed `k` and
`49` are fixed, while the numerator and denominator retain the same
degrees in `r`, `X`, and `ell^((L+1)/2)`. No new prime is added to the
global exceptional set: `7,11,17,233` were already in it. If the
original scalar is a norm from the detector field, so is the new one,
by the displayed square ratio.

For both scalars `C_L r>=1` on the real line. Since

\[
1+kt-7(1+t)=(k-7)t-6>0\qquad(t\ge1),
\]

one has `0<rho*<rho`. The original displayed estimates give
`rho<36/ell<1/56`; the aligned scalar has an even smaller bound.
Hence `0<rho*<1/56` for every real input.

## Integer-input preparation

For integer inputs, the displayed numerator is an integer and its
denominator is a square, so the reduced denominator is square. Since
`7 | k` and `r,C_L` are integers, the denominator is a 7-adic unit.
The numerator has a factor `49`, and all its remaining factors are
7-integral. Thus

\[
v_7(\rho^*)\ge2.
\]

At 2, both original and new denominators are units (`C_L` is even for
the original scalar; the aligned scalar also has its certified even
contact value). The square ratio has 2-adic valuation zero. Consequently
`rho*` is a 2-adic square and retains the old valuation, four or twelve.
At 3 and 17 the integer-input preparation remains valid: the scalar
numerator's old positive valuation is unchanged, the new denominator
is a unit because the contact value or its coefficient has positive
valuation, and the square class is unchanged. These are the original
local calculations with `C_L` replaced by an integer multiple.

Before choosing the scalar/reference roots, use the temporary finite
preparation set containing the supports of `rho*` and `1+rho*`.
This does not alter the global exceptional set or height constants.

The existing v53 preparation then gives both normalized actual pole
inputs

\[
b_j=4w_j/\operatorname{Tr}(W_j^{-1})^2
\]

with square reduced denominators. At 7, choose `R_j` close to one and
the trace close to two. Then `u_j` and `w_j` have valuation at least
two, so `v_7(b_j)>=2`. At 2, the same preparation gives
`b_j in Q_2^{*2}` and `v_2(b_j)=v_2(rho*)>=4`.

At the selected real character, choose `R_j<2` and both detector slots
in `[1,2)`. Then `w_j<u_j<2rho*`, the reciprocal trace exceeds one,
and

\[
0<b_j<8\rho^*<1/7.
\]

Therefore `d_j=7b_j` satisfies every intrinsic Burungale preparation
hypothesis. Other point-algebra characters remain real and have
positive nonzero `d_j`. The unguarded intrinsic polynomial and the
proved density avoid every terminal-radicand norm, also when some
conjugate value of `d_j` is one.

## Conclusion and scope

Replacing the scalar constants and the two old pole blocks as above
gives the same complete **25-variable** transfer as the coherent
`w7` construction. It works with either retained scalar and with either
v53 scalar orders or the corrected order-two precision source. It keeps
the original normalized physical weights, and therefore also remains
a legitimate source for the native 21-variable square-cover criterion.
No realization of that smaller cover, numerical sufficient `L`, or
new determinant degree bound is supplied by this constant change.
