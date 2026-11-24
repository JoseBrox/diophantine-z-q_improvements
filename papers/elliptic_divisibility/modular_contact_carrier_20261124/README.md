# Odd elliptic denominator support from the original modular-height premise

## Result and scope

This note derives a denominator statement from the actual original modular
premise, with **no additional abc assumption**. It does not establish the
simple-denominator mass (SD) or the weaker power-growth hypothesis (OM) on
the original carrier.

Use exactly the rational five-contact estimate of
[v19](../../contact_heights/multiplicity_and_contact_heights_20261110_v19.tex):
for a reduced rational \(t=u/v\), \(v>0\), outside the contacts, let \(M_5(t)\)
be the product of primes greater than \(76176\) occurring to a positive odd
power in at least one of
\[
 v,\ u,\ u-v,\ u-2401v,\ 32u+343v.
\]
The retained full normalized modular realization gives
\[
 h(t)\le C_2 M_5(t)^2(1+\log M_5(t))^2,\qquad C_2<2^{221231}.
\]
We use this precise statement, not an abc estimate or a logarithmic
radical bound.

Consider the elliptic curve and point
\[
 E_*:Y^2=(X-33614)(X-14)(X+3136),\qquad
 P_*=(0,38416).
\]
For a nonzero integer \(n\) and a good prime \(p>76176\), let
\(a_p(n)=\max(0,-v_p(X([n]P_*))/2)\) be the formal denominator depth,
where \(v_p(p)=1\). Define
\[
 R_{\mathrm{odd}}(n)=
 \prod_{\substack{p>76176\\a_p(n)>0,\ a_p(n)\ {\rm odd}}}p .
\]
Then, uniformly for integers \(|c|\ge2\),
\[
 \tag{1}
 \log R_{\mathrm{odd}}(c-1)+\log R_{\mathrm{odd}}(c+1)
 \ge \log|c|-\log(1+\log|c|)-O(1).
\]
In particular the original premise implies infinitely many good rational
primes at which the initial denominator depth of \(P_*\), at its rank
of apparition, is odd.

This is a logarithmic mass lower bound on two adjacent indices of a
different, explicit curve. It does not imply power growth in \(|c|\),
does not bound those odd depths by a fixed constant, and does not
establish exponent-one mass.

## 1. Exact cancellation of four contact valuations

The quartic
\[
 w^2=2t(t-1)(t-2401)(32t+343)
\]
has two rational points at infinity. On its smooth projective model
the change of coordinates
\[
 X=33614/t,\qquad Y=4802w/t^2
\]
gives the stated model \(E_*\). Indeed, first put \(x=1/t\),
\(y=w/t^2\), so that
\[
 y^2=2(1-x)(1-2401x)(32+343x).
\]
The leading coefficient is \(1647086=49\cdot33614=343\cdot4802\).
Scaling gives the cubic
\[
 X^3-30492X^2-104986812X+1475789056.
\]
The points at infinity of the quartic correspond to \(P_*\) and
\(-P_*\), since the leading quartic coefficient is \(64\).
All bad primes of the integral cubic are in \(\{2,3,5,7\}\), as follows
from its three root differences and the discriminant formula.

Direct duplication gives
\[
 X([2]P_*)=\frac{5951086353}{3136},\qquad
 Y([2]P_*)=\frac{455376332353657}{175616}.
\]
The point \([2]P_*\) has formal depth 3 at 2, since the numerator of
the abscissa is odd and \(v_2(3136)=6\). The formal logarithm is
injective in this disk (depth greater than \(1/(2-1)\)); thus \(P_*\)
is nontorsion. Write \(q_*=\widehat h(P_*)>0\).

For \(Q=[c]P_*\) with \(|c|\ge2\), the rational function
\(t(Q)=33614/X(Q)\) has no exceptional contact value. Its finite
branch contacts are the images of two-torsion points, and its poles
are \(\pm P_*\). None can be attained by this nontorsion point \(Q\).
The function \(t\) has pole divisor \([P_*]+[-P_*]\), linearly
equivalent to \(2[O]\). Equivalently, it is a fixed invertible
fractional linear transform of the abscissa. Hence
\[
 h(t([c]P_*))=2q_*c^2+O(1).
\]

Let \(p>76176\). The five contacts are distinct in \(\mathbb P^1(\mathbb F_p)\).
If \(t=u/v\) is \(p\)-integral, at most one of the four finite
homogeneous linear contact forms is divisible by \(p\).
The quartic square identity, after multiplication by \(v^4\), forces
that valuation to be even. If \(v_p(t)<0\), each of the four finite
homogeneous linear forms is a unit, and the only contribution to
\(M_5(t)\) is from the denominator \(v\), precisely when its valuation
is odd. Thus
\[
 M_5(t(Q))=\prod_{\substack{p>76176\\v_p(t(Q))<0\ {\rm odd}}}p.
\]

At any such prime, \(33614\) and \(38416\) are units, and the two
points \(P_*\) and \(-P_*\) have distinct reductions. The abscissa
has a simple zero at each of them. Therefore if \(Q\) reduces to
\(\pm P_*\), the valuation of \(t(Q)\) is the negative formal depth
of \(Q\mp P_*\). This follows by translating to \(O\) and expanding
the abscissa in the formal parameter: the first derivative at the
translated zero is a unit because its ordinate is a unit and the
residue characteristic is odd. Conversely negative valuation of \(t\)
implies that \(Q\) reduces to one of these two points. Consequently
\[
 \tag{2}
 M_5(t([c]P_*))=
 R_{\mathrm{odd}}(c-1)R_{\mathrm{odd}}(c+1).
\]
The two supports on the right are disjoint: a common good prime would
make \([2]P_*\) reduce to \(O\), whereas the two reductions of
\(\pm P_*\) are distinct.

Combining (2) with the retained v19 inequality yields
\[
 2q_*c^2-O(1)\le C_2 M_5(t)^2(1+\log M_5(t))^2 .
\]
For sufficiently large \(|c|\), taking logarithms gives
\(\log M_5(t)+\log(1+\log M_5(t))\ge\log|c|-O(1)\).
If \(\log M_5(t)\ge\log|c|\), (1) is immediate; otherwise substitute
\(\log|c|\) in the second term to obtain (1). Enlarge the constant
for the finitely many smaller indices.

## 2. Infinitely many odd initial depths, without abc

For a good prime \(p>76176\), let \(r_p\) be the order of
\(P_*\bmod p\). Full rational two-torsion implies
\(4\mid\#E_*(\mathbb F_p)\). By Hasse's bound, for \(p>7\) the only
possible positive multiple of \(p\) in that interval is \(p\)
itself, which is odd. Therefore \(p\nmid r_p\).

When \(r_p\mid n\), the isometric formal logarithm at the odd good
prime gives the exact identity
\[
 a_p(n)=a_p(r_p)+v_p(n/r_p)=a_p(r_p)+v_p(n).
\]
Otherwise \(a_p(n)=0\). There is no multiplicity-one hypothesis here.

Now take the unbounded integer sequence
\[
 c_k+s_k\sqrt2=(3+2\sqrt2)^k,\qquad k\ge1.
\]
It satisfies \((c_k-1)(c_k+1)=2s_k^2\).
The factors on the left have gcd dividing 2. At every odd prime,
both \(v_p(c_k-1)\) and \(v_p(c_k+1)\) are therefore even (one is zero).
Every prime counted on the right of (2) for \(c=c_k\) has
\(a_p(r_p)\) odd, by the preceding formal-depth identity.
The product of these primes grows unboundedly by (1). It cannot
be supported on a fixed finite set, which proves the assertion.

This argument proves odd initial depth, not non-Wieferich depth one.
It does not require or assert that \(E_*(\mathbb Q)\) has rank one.
The retained modular realization is the only nonstandard arithmetic
premise used in the mass argument.

## 3. Why this cancellation cannot simply be moved to the original carrier

There are five ways to choose four of the five marked contacts
\(\{\infty,0,1,2401,-343/32\}\).
Each double cover of the line branched at those four points has genus
one. Its geometric \(j\)-invariant is determined by a cross-ratio
\(\lambda\) through \(256(1-\lambda+\lambda^2)^3/
(\lambda^2(1-\lambda)^2)\). The complete list, with the omitted
contact as label, is

| Omitted contact | Cross-ratio | \(j\) |
|---|---:|---:|
| \(-343/32\) | \(2401\) | \(191342053882402567201/129708022500\) |
| \(2401\) | \(-343/32\) | \(2179252305146449/66177562500\) |
| \(1\) | \(-1/224\) | \(128031684631201/9922500\) |
| \(0\) | \(-5/1024\) | \(1169975873419524361/108425318400\) |
| \(\infty\) | \(35/32\) | \(1439069689/44100\) |

Every invariant is rational and nonintegral, so none of these curves
has complex multiplication (a CM \(j\)-invariant is an algebraic integer).
In particular none is geometrically isogenous to the original
\(j=1728\) elliptic carrier.

More generally let \(A\) be any abelian variety whose geometric
simple factors are isogenous to the original carrier, for example
its Weil restriction from \(\mathbb Q(\sqrt2)\), or products of
such restrictions. There cannot be a nonconstant rational function
\(t\) on \(A\) with a rational function \(w\) satisfying an exact
square identity giving one of these four-contact double covers.
Otherwise the two functions give a nonconstant rational map
from \(A\) to the smooth genus-one curve. Over the algebraic
closure, a rational map from an abelian variety to an abelian
variety extends to a morphism; after translating, it is a
homomorphism. A nonconstant map would therefore make that
non-CM elliptic curve an isogeny quotient of \(A\), contradicting
the CM simple-factor condition.

This is an obstruction to the specific exact four-contact-square
cancellation method, not to all uses of the modular hypothesis.
In particular it does not prohibit cancellation only at selected
primes, more complicated algebraic covers, or a carrier which is
not geometrically isogenous to the original.

## 4. Remaining gap

Equation (1) gives only
\(\log R_{\mathrm{odd}}(c-1)+\log R_{\mathrm{odd}}(c+1)\gg\log|c|\).
The [bounded-odd-depth amplifier](../sublinear_odd_mass_amplifier_20261124/README.md)
needs a positive fixed power of \(|c|\), on bounded odd depths, on
the original carrier. No choice of fixed scalar precision changes
a logarithm into a positive power in its exponent comparison.
Moreover the auxiliary curve is not isogenous to that carrier.

Thus the original hypotheses yield the concrete weaker arithmetic
result above, but the requested mass estimate is still open.
No variable-count or quartic improvement is claimed in this note.

The accompanying exact checker verifies the birational identity,
duplication, discriminant support, all five cross-ratios and
nonintegral invariants, and the Pell valuation mechanism on finite
fixtures. The asymptotic claims follow from the proof and the
retained modular inequality, not from the fixtures.
