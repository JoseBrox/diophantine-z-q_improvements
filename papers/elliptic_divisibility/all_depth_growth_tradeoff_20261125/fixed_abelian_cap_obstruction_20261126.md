# Fixed-abelian-variety obstruction to the mixed-scale double-quotient cap

## Scope and result

This strengthens the finite-cover obstruction in
[finite_cover_obstruction.md](finite_cover_obstruction.md) and the
genus-one fiber obstruction in
[mixed_scale_cap_20261126.md](mixed_scale_cap_20261126.md).
It applies even to auxiliary constraints with several abelian
coordinates, including ramified finite covers of the base realized
inside products of fixed abelian varieties.

There is **no** construction enforcing the desired cap in this note.
The result is a restriction on one class of approaches, not on
arbitrary ramified covers or defining polynomials.

## 1. Statement

Use \(E/\mathbb Q:y^2=x^3-2x\), \(P=(9/4,-21/8)\) as in the
double-quotient source. Put
\[
 H=[h]P,\quad U=[j]P,\quad |h|\ge2,\quad j\ne0,\quad
 h\mid j,\quad h-1\mid j-1,\quad
 m'=\frac{j-h}{h(h-1)}.
\]
Fix any nonzero integer input \(X=m\).

Consider a finite menu of auxiliary varieties
\[
 V_i\subset E^2\times A_i
\]
over \(\mathbb Q\), where each \(A_i\) is an abelian variety fixed
once \(X=m\) is fixed. Assume the predicate accepts rational points
of the indicated Zariski opens in \(V_i\), subject to the two index
divisibilities, the nonzero conditions just displayed, and possibly
finitely many open local conditions. Other rational data, including
any charges, must be regular or rational functions of these auxiliary
points on the guarded opens. The local open conditions may depend
on the fixed reference.

Suppose the predicate claims a finite upper bound on \(|m'|\)
for each fixed pair \(X,H\). This includes the mixed-scale height
cap through the previously proved double-quotient inequality.
Then it cannot supply canonical witnesses
\[
      j=h+mh(h-1)
\]
for infinitely many distinct \(h\).

The conclusion uses Faltings' Mordell--Lang theorem for finitely
generated subgroups of a fixed abelian variety, and Poincare complete
reducibility. It does not require an effective height theorem.

## 2. Proof

For fixed nonzero \(m\), any infinite subset of the canonical pairs
\(([h]P,[h+mh(h-1)]P)\) is Zariski dense in \(E^2\), as proved
in Section 2 of finite_cover_obstruction.md. One way to see this is
Mordell--Lang: a proper abelian translate containing infinitely many
of these pairs would impose a nonzero linear relation on the two
indices, whereas \(h+mh(h-1)\) is genuinely quadratic. The direct
proof in that note also works using Faltings on curves.

Take rational witnesses for infinitely many distinct \(h\). Some
menu entry contains infinitely many. Replace that entry by its
closure in \(E^2\times A_i\). By Mordell--Weil its ambient group
of rational points is finitely generated. By Mordell--Lang the
rational points in the closure are contained in a finite union of
abelian translates contained in the closure. This can be taken
as a union of translates defined over \(\mathbb Q\) with rational
basepoints: the components of the Zariski closure of the rational
points are defined over \(\mathbb Q\), and a component that contains
a rational point is a translate by that point. Discard components
not meeting the guarded open.

The density result implies some translate \(Q+B\) contains infinitely
many canonical witnesses and projects dominantly onto \(E^2\).
Since the projection is a translation of a homomorphism on \(B\),
it is surjective. Denote this homomorphism by \(\pi:B\to E^2\).

Fix an actual accepted canonical lift \(Q_0\) on this translate,
with \(H_0=[h_0]P\) and \(U_0=[j_0]P\). Choose a homomorphism
\(\iota:E^2\to B\) defined over \(\mathbb Q\) with
\(\pi\iota=[d]\) for some positive integer \(d\).
Such a quasi-section follows from Poincare complete reducibility
over \(\mathbb Q\): an abelian complement to the connected kernel
gives an isogeny onto \(E^2\), and an inverse up to multiplication
gives \(\iota\).

The rational points
\[
 Q_t=Q_0+\iota(O,[t]P),\qquad t\in\mathbb Z,
\]
lie in \(Q+B\) and have the *same reference*
\(H_0\), with second point \([j_0+dt]P\). Restrict \(t\)
to multiples of \(|h_0(h_0-1)|\); both exact index divisibilities
then persist. The guarded open contains \(Q_0\). The orbit just
defined is on an elliptic curve translate through \(Q_0\), so
algebraic guard failures exclude at most finitely many orbit points.
The additional finitely many local open conditions, if present,
can all be preserved along infinitely many multiples: first use
the finite local group quotients to impose suitable congruences,
then compact real recurrence (or recurrence in the product of the
local compact groups) to return to a neighborhood of \(Q_0\).
The finitely many exceptional orbit points and \(j=0\) are avoidable.

On these accepted points \(X,H\) stay fixed and
\[
 m'=m+\frac{dt}{h_0(h_0-1)}
\]
is unbounded. This contradicts the cap. The same argument works over
a fixed number field with its Mordell--Weil group, provided the
index graph density and rational-lift convention are retained.

## 3. Consequences for ramification

For example suppose a coupled cap is an irreducible algebraic
surface \(V\) in \(E^2\times A\), with a dominant generically finite
projection to \(E^2\), and infinitely many canonical lifts for
a fixed nonzero \(X=m\). Mordell--Lang and the preceding density
argument give a two-dimensional abelian translate contained in
\(V\) with dominant projection. By dimension and irreducibility
it is all of the projective closure of \(V\). Its map to \(E^2\)
is an isogeny followed by translation, hence etale in characteristic
zero. Thus a genuinely ramified cover in this restricted class
cannot even provide the required infinite canonical lifts. This
argument assumes a closed projective realization of the stated
kind; it is not a claim about arbitrary rational maps from
nonabelian surfaces.

In particular switching from one fixed auxiliary elliptic curve
to any finite number of fixed elliptic curves is insufficient.
The arithmetic auxiliaries must escape a fixed abelian ambient
group, or the completeness requirement must be weakened to a
noncofinal construction. Allowing the auxiliary abelian variety
to vary with \(H,U\) is not excluded. Neither are higher-genus
covers of \(E^2\) not embeddable in an abelian variety, or
predicates using additional genuinely nonalgebraic selection.

The conclusion cannot be extended to a predicate whose remaining
BB witnesses have not been included in the algebraic constraints:
the varied points need not satisfy a separately required
foreign-prime preparation condition. The theorem applies to the
cap itself, or to a system for which every necessary acceptance
condition has the stated algebraic/open form.

## 4. Rational-section special case

Even without a fixed abelian ambient space for the auxiliaries,
a finite menu of rational-function sections over \(E^2\) at
fixed \(X=m\) cannot solve the cap problem by matching infinitely
many canonical pairs. Density makes the defining polynomial
identities of one matching section hold identically on the base;
its nonvanishing guards hold on a nonempty open. Fix a canonical
reference for which the section is defined at an accepted point.
The vertical elliptic fiber then meets this open, and all but
finitely many points \([j_0+dt]P\) with the requisite divisibilities
give rational lifts. Finite open local conditions are preserved
by the same recurrence argument. Thus the quotient again becomes
unbounded.

This excludes a large class of elementary constructions that
try to produce ramified witnesses by explicit rational formulas
in the two points. It does not exclude a genuinely arithmetic
(nonrational-section) choice of a lift at each canonical pair,
and it does not prove a height cap or a new variable bound.
