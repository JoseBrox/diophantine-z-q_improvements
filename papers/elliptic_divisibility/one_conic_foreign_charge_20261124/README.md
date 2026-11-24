# One-conic foreign-prime charges: seven coordinates and exact height costs

This is a lower-coordinate alternative to the
[nine-coordinate BB charging cover](../all_prime_foreign_charge_20261124/README.md).
A norm from a fixed quadratic number field is not needed at all.
Two elementary rational conics give complementary types of
all-prime control. Both are globally parametrizable on every
guarded base tuple. Consequently they transfer denominator mass
into new rational witnesses, but by themselves impose no cap on
the hidden quotient. Their use leaves two ordinary coordinates
available within the nine-coordinate target.

## 1. Setup

Use the six-coordinate height-anchored quotient on
\[
 E:y^2=x^3-2x,\quad R_0=(2,2),\quad P=[2]R_0=(9/4,-21/8).
\]
The fixed point \(P\) is nontorsion, and the retained cyclic chart
represents \(H=[h]P,\ U=[j]P\) with nonzero integer indices. Let
\(q=\widehat h(P)\). Write \(g_H^2=x(H),\ g_U^2=x(U)\)
for the nonzero rational square-root coordinates already present
in that chart. Either sign is allowed. At any good prime,
if \(U\) is formal of positive depth \(a\) then \(v_p(g_U)=-a\);
if \(H\) is nonformal then \(v_p(g_H)\ge0\).

Retain the old comparison equations and all their guards.
For quantitative denominator mass and the height bound on \(X\),
we use the ordinary rational abc results of the
[duplication-mass paper](../duplication_mass_and_bounded_quotients_20261124/README.md).
The conic identities and local implications themselves do not
require abc or a further BB realization.

## 2. A single numerator charge at every odd foreign depth

Set
\[
 L=\frac{g_U}{g_H^2}\ne0
\]
and adjoin the conic
\[
 \tag{1} r^2=1+L s^2,\qquad s\ne0.
\]
Retain \(s\) as one ordinary rational coordinate and adjoin \(r\)
as a finite root. Clear the denominator by the existing
numerator-denominator square-root convention. With the same
selected-character encoder this uses **seven total coordinates**,
not nine. There is no second BB pole.

If \(p\) is a foreign prime where \(U\) has odd positive formal
depth \(a\), put \(b=v_p(g_H)\ge0\). Then
\[
 v_p(L)=-a-2b
\]
is negative odd. If \(v_p(L)+2v_p(s)<0\), the two summands on
the right of (1) have unequal valuations, and its value has
negative odd valuation. It cannot be a square. Equality of the
two valuations with zero is impossible by parity. Therefore
\[
 \tag{2} v_p(s)>a/2+b .
\]
This holds at every such prime, independently of its splitting
in every fixed number field. At a foreign simple denominator
prime \(v_p(s)\ge1+b\ge1\). The argument works at 2 as well
whenever the stated formal-depth and integral-model valuations hold.
No condition at an arbitrary even formal depth is inferred.

For completeness, (1) has the exact rational parametrization
\[
 \tag{3}
 s=\frac{2t}{1-Lt^2},\qquad
 r=\frac{1+Lt^2}{1-Lt^2}.
\]
For any guarded rational \(H,U\), choose any nonzero rational
\(t\) with \(Lt^2\ne1\). This supplies an actual rational conic
point. No simultaneous rank, inert-prime or local-to-global
assertion is used. In particular every old witness, true or false,
extends to this seven-coordinate relation. The denominator
\(g_H^2\) is already guarded, so no extra nonzero coordinate is
needed.

Under ordinary abc, let \(F_1(H,U)\) be the product of all
foreign exponent-one denominator primes outside a fixed set.
The full simple-prime mass estimate gives
\[
 \log F_1(H,U)\ge qj^2-qh^2-o(j^2)-O(1).
\]
Equation (2) implies
\[
 \tag{4}h(s)\ge qj^2-qh^2-o(j^2)-O(1).
\]
For \(j=mh\) with fixed integer \(m\ne0\) this is a lower
bound \((m^2-1)qh^2-o(h^2)\).
Thus this cheap conic has the same crucial quadratic charging
effect as the nine-coordinate BB variant.

As in the earlier note, a complete new relation on the charge
with \(\log(1+h(s))\le A qh^2+O(1)\) and fixed \(A\)
would give a quotient cap of coefficient \(A/2\).
After increasing the old fixed precision, the original input-height
and discrepancy argument would force integrality.
This is now a precise target using at most two further ordinary
coordinates. The new conic alone is not that relation.

## 3. Literally all depths: a two-register denominator charge

If control at every positive formal depth, including even depths,
is wanted, use instead the radius
\[
 R=\frac{g_U}{g_H}\ne0
\]
and the coupled conic
\[
 \tag{5} s^2+r^2=R^2 .
\]
Again retain one ordinary variable \(s\), and \(r\) is finite.
The rational solutions with both coordinates nonzero include
\(s=3R/5,\ r=4R/5\).

At **every** foreign denominator prime of positive depth \(a\),
including even \(a\), we have \(v_p(R)=-a-v_p(g_H)\le-a\).
The ultrametric inequality in (5) gives
\[
 \tag{6} \min\{v_p(s),v_p(r)\}\le-a-v_p(g_H)\le-a.
\]
Cancellation between the two squares can only increase the
valuation of their sum; it cannot invalidate (6).
Thus the full foreign denominator power divides the product
of the reduced denominators of the two witness coordinates.
This works at split and nonsplit primes alike, without any
parity hypothesis. In logarithmic heights it gives
\[
 \tag{7} h(s)+h(r)\ge
   \sum_{\substack{p\ {\rm foreign}}} a_p(U)\log p
   \ \ge\ qj^2-qh^2-o(j^2)-O(1).
\]
The last inequality can use only the simple primes, and is
therefore uniform in both indices.

This is a literal all-depth transfer, but the bound needed to
finish the definition must concern **both** conic coordinates
(including the finite root), unlike (1) which places the
numerator charge in a single chosen coordinate. Neither conic
forbids the foreign primes of actual integer multiples.
For \(\log(1+h(s)+h(r))\) an upper cap with fixed coefficient
would suffice in the same way.

The local charge mechanisms have different advantages: (1)
puts every odd foreign contact into one nonzero numerator; (5)
charges every depth but the height may be shared by two
coordinates. These are alternative seven-coordinate extensions,
not two simultaneous requirements. Both admit all previous
nonintegral counterexamples.

## 4. Exact height costs of explicit global witnesses

The size of the conic witnesses on the true multiplication
graphs can be estimated without a uniform rational-point theorem.

Let
\[
 f(Q)=\frac{x(Q)^2+2}{2y(Q)} .
\]
The duplication formula gives \(f(Q)^2=x([2]Q)\).
Its poles are the four geometric two-torsion points \(E[2]\),
each of order one. Indeed this follows from the Laurent
expansion at \(O\), and from the simple zeros of the ordinate
at the other three two-torsion points. Its zeros are the four
points mapping to \((0,0)\) under [2], each simple:
\(x^2+2=0\) and the ordinate is nonzero at these points.
Denote this four-element set by \(Z_f\).
It consists of exact four-torsion points.
In the true family take the coherent square roots
\[
 Q=[h]R_0,\quad g_H=f(Q),\quad g_U=f([m]Q).
\]
A sign change in either root leaves every height estimate unchanged.

The rational function \(L=f([m]Q)/f(Q)^2\) has the following
geometric pole degrees for \(m\ne0\):
\[
 \deg(L)=
 \begin{cases}
   4m^2,&m\text{ odd},\\
   4m^2+4,&m\text{ even}.
 \end{cases}
\]
To count them, the numerator has a simple pole at every point
of \(E[2m]\) (write \(E[2|m|]\) for negative \(m\)).
At each of the four points in \(E[2]\), the denominator has a
pole of order two, so no pole of the ratio remains.
For odd \(m\), the numerator is a simple zero at every point of
\(Z_f\); the denominator is a double zero there, leaving four
simple poles not counted by \(E[2m]\).
For even \(m\), the numerator is a simple pole at each point of
\(Z_f\), already counted in \(E[2m]\); the denominator double
zero raises each of these four pole orders by two.
All other numerator poles survive unchanged. This proves the
degree formulas, including \(m=\pm1\).

The analogous radius function \(R=f([m]Q)/f(Q)\) has degrees
\(4m^2-4\) for odd \(m\), and \(4m^2\) for even \(m\).
Here the four denominator poles cancel the four numerator poles
at \(E[2]\); for odd \(m\) the four zeros at \(Z_f\) also cancel,
while for even \(m\) they add one to the four existing pole orders.
When \(m=\pm1\) this radius is constant, agreeing with degree zero.

All these divisors are torsion supported. For a fixed rational
function on \(E\) with pole divisor of degree \(d\) supported on
torsion, the corresponding height is \(d\widehat h(Q)+O(1)\):
the pole divisor differs from \(d[O]\) by a torsion class
in \(\operatorname{Pic}^0(E)\), hence becomes linearly equivalent
after a fixed multiple. Height functoriality and the bounded
height difference for linearly equivalent divisors prove the claim.
Since \(\widehat h(Q)=qh^2/4\), we get for fixed \(m\)
\[
 h(L)=
 \begin{cases}
  m^2 qh^2+O_m(1),&m\ {\rm odd},\\
  (m^2+1)qh^2+O_m(1),&m\ {\rm even},
 \end{cases}
\]
\[
 h(R)=
 \begin{cases}
  (m^2-1)qh^2+O_m(1),&m\ {\rm odd},\\
  m^2 qh^2+O_m(1),&m\ {\rm even}.
 \end{cases}
\]
These formulas are valid for nonzero \(h\); nontorsion multiples
do not meet the zeros or poles supported on torsion.

For (1), choose \(t=1\) in (3) whenever \(L\ne1\), and \(t=2\)
if \(L=1\). This gives \(h(s)\le h(L)+O(1)\) uniformly.
The fractional linear map for \(t=1\) is invertible, giving
equality up to a bounded error. Thus the achievable numerator-charge
height has a precise upper budget with coefficient \(m^2\) or
\(m^2+1\), and the necessary lower budget from (4) has coefficient
\(m^2-1\). We do not claim the exact minimal height of (1).
For (5) the explicit Pythagorean solution has
\(\max(h(s),h(r))=h(R)+O(1)\), giving the displayed exact
upper cost; if a zero coordinate is allowed, the solution
\((R,0)\) has total height exactly \(h(R)\).

In particular the missing upper constraint need not force
a tiny charge: logarithmic height genuinely of order \(m^2h^2\)
is compatible with all-prime control and explicit integer witnesses.

## 5. Limits of obvious ways to close the cap

The polynomial-height estimate of the original modular premise
would be attractive if one could force five-contact odd support
of a rational function of the charge into the prime support of
the reference and other fixed-degree expressions in \(X,H\).
But ordinary abc gives a **linear** bound on that charge height
from such an inclusion, as proved in the
[nine-coordinate charging note, Section 5](../all_prime_foreign_charge_20261124/README.md).
This contradicts (4) for all sufficiently large fixed \(m\)
and arbitrarily large \(h\).

Also, imposing a second conic of the form (1) with \(s\)
replaced by \(s+F(X,H)\) forces every foreign simple prime
to divide the numerator of the fixed-degree function \(F\).
The [foreign-boundary obstruction](../../../negative_results/papers/pole_parameters/foreign_boundary_cover_obstruction_20261124.md)
excludes completeness for such a nonzero \(F\).
Choosing an identically zero \(F\) gives no new test.

The generic multiplicity-one boundary components of these
rational conic covers explain why all-prime charging is possible
without rejecting true multiplication graphs.
The next task is a genuinely nonlinear global constraint on
the one moving charge, not a second all-prime rejection with
a bounded-degree exception locus.

## Verification and status

The [standard-library checker](../../../scripts/verify_foreign_charge_20261124.py) tests the exact conic parametrization,
odd-depth numerator inequalities, all-depth denominator
inequalities, explicit rational elliptic fixtures, and the
torsion-divisor degree census. No conjectural mass or rank input
is certified by finite checks. Both variants are complete
extensions of the old six-coordinate relation and hence **not**
definitions of the integers. No new unrestricted-degree or
quartic defining-polynomial record is claimed.

The executed checker passed 32,000 synthetic conic valuation profiles, 163 exact odd-depth and 184 exact all-depth foreign-prime conic fixtures, and the torsion-grid degree census for 24 multipliers. The same script checks the older BB charge. Run from the repository root with `python -B scripts/verify_foreign_charge_20261124.py`.
