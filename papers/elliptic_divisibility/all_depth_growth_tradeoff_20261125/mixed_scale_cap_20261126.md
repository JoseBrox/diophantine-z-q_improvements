# Mixed-scale double-quotient cap and the unramified-fiber obstruction

This is a continuation of [double_quotient.md](double_quotient.md).
No defining-polynomial count is claimed. We work on its rational carrier
\(E:y^2=x^3-2x\), \(P=(9/4,-21/8)\), \(q=\widehat h(P)>0\).
The same height arguments apply to the quadratic carrier with the appropriate
absolute heights. Write \(H=[h]P,\ U=[j]P,\ H_*=\widehat h(H)=qh^2\)
and assume \(|h|\ge2,\ j\ne0,\ h\mid j,\ h-1\mid j-1\).
Then \(m=(j-h)/(h(h-1))\) is integral. Let \(A=h(s)+h(r)\)
be the sum of logarithmic heights of the two conic charge coordinates
\(s^2+r^2=(g_U/g_H)^2\), where \(g_V^2=x(V)\).
The already proved full-depth estimate is
\[
\log(1+|m|)\le C+\tfrac12\log(1+A/h^4).
\tag{1}
\]
Here \(h(\cdot)\) denotes logarithmic Weil height, not the reference index.

## 1. A mixed-scale cap with exactly quadratic reference-height dependence

An alternative target to \(A\ll(1+H_*)^{2+\epsilon}\) is
\[
 A\le C_0(1+|X|)^2(1+H_*)^2,
\tag{2}
\]
where \(X\) is the rational input and \(C_0\) is fixed independently
of \(h,j,X\). It does not imply or follow uniformly from the older cap.
However, it has a uniformly compatible choice of \(C_0\) for *all*
canonical integer tuples \(m=X,\ j=h+Xh(h-1)\) with the indicated
nonvanishing conditions, not just eventually in \(h\) for each fixed \(X\).

Indeed \(|j|\le |h|+|X||h||h-1|\le (1+\tfrac32|X|)h^2\).
For \(R=g_U/g_H\) take \(s=3R/5,\ r=4R/5\).
The canonical-height comparison and elementary height inequalities give
\(A\le2q(j^2+h^2)+O(1)\), with an absolute additive constant on this fixed
curve. Consequently these witnesses satisfy (2) for a fixed \(C_0\).
There is no cofinal-existence assertion for any *additional* predicates.

By (1) and boundedness of \((1+qh^2)^2/h^4\) for \(|h|\ge2\),
(2) implies
\[
 \log(1+|m|)\le \log(1+|X|)+O(1)\le h(X)+O(1).
\tag{3}
\]
More generally, \(A\ll(1+|X|)^r(1+H_*)^{2+\epsilon}\) for fixed
\(r,\epsilon\ge0\) gives
\[
 \log(1+|m|)\le (r/2)h(X)+(\epsilon/2)\log(1+H_*)+O(1).
\]
If an eventual double-quotient comparison source simultaneously proves
\(h(X)\le\kappa H_*+O(1)\) and, for \(m\ne X\),
\(\log(1+|m|)\ge bH_*-O(1)\), then the strict inequality
\(b>r\kappa/2\) suffices for equality \(m=X\) after a fixed finite
reference exclusion. For (2) the required inequality is simply \(b>\kappa\).
Both comparison estimates must be established for the actual double-quotient
source; the single-quotient discrepancy theorem cannot be transferred
without proof. This is an implication and a numerical compatibility result,
not a Diophantine enforcement of (2).

## 2. Why a fixed unramified fiber cannot be a cap

Consider any proposed cap predicate over the fixed base \(X,H\), whose
remaining auxiliary equations (including the charge witnesses, if used)
form a curve mapping nonconstantly and finitely on an open subset to
the variable elliptic point \(U\). Suppose there is an accepted rational
point on a component whose smooth projective normalization is a
geometrically integral curve of genus one. Assume that all rational lifts
satisfying the indicated algebraic guards and finitely many open local
conditions are accepted; in particular no additional coupled predicate
with unproved completeness may be silently imposed. Then this component
cannot enforce any finite upper bound on \(|m|\) for this fixed \(X,H\).

For the proof one can take the accepted smooth rational point as origin
on the normalization, with image \(U_0=[j_0]P\). The map to \(E\) is
an isogeny of degree \(d>0\) followed by translation by \(U_0\).
Composing with its dual gives rational lifts of all
\[
 U_t=U_0+[dt]P,\qquad t\in\mathbf Z .
\]
Only finitely many of these lifts can land at deleted points or zeros of
nonidentically-zero algebraic guards. Restrict \(t\) to multiples of
\(|h(h-1)|\) to preserve both index divisibilities. Impose any further
finite congruences on \(t\) so that the lifts stay in the original open
neighborhoods at the finitely many relevant nonarchimedean places.
At the real place, recurrence in the compact group of real points
gives infinitely many such multiples returning arbitrarily near the
original point. More explicitly, use a common multiple to put the
generating point in the appropriate open subgroups at finite places,
then take recurrent multiples of that point in the real compact group.
The resulting indices \(j=j_0+dt\) are unbounded since \(P\) is
nontorsion. Thus \(m\) is unbounded with \(H,X\) fixed.

This applies in particular to a nonconstant finite cover extending to an
unramified finite cover of the projective \(U\)-curve, by Riemann--Hurwitz.
The result is valid over a number field with the same acceptance convention
and local recurrence (using the product of its archimedean groups).
It does not apply when extra restrictions on rationality of some
coordinates are not captured by the curve over that field.

Therefore a finite-cover cap using this acceptance convention must avoid
such genus-one fibers at its accepted witnesses. A genus-zero component
cannot dominate \(E\). On the other hand genus at least two, which permits
finite rational fibers by Faltings, leaves the substantive problem of
uniform height and canonical completeness open. The existing fixed-m
Zariski-density obstruction in
[finite_cover_obstruction.md](finite_cover_obstruction.md) also rules out
a nontrivial equality cutting out a curve in \(E^2\) that contains
infinitely many canonical double-quotient pairs for fixed nonzero \(m\).
These are restrictions on approaches, not a no-go theorem for arbitrary
Diophantine caps.
