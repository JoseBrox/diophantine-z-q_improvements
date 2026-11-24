# The foreign-boundary obstruction for arbitrary coupled covers

This note complements the positive [all-prime charging cover](../../../papers/elliptic_divisibility/all_prime_foreign_charge_20261124/README.md).
It proves an obstruction for general algebraic covers, including
positive-dimensional coupled fibers, not merely fixed-field norm conics,
Kummer tests, or uncoupled BB poles.

The scope is a **uniform local rejection mechanism along the generic
foreign denominator boundary**, while retaining arbitrarily large
references for every integer input. It is not an impossibility theorem
for global coupled geometry, nor a lower bound on the variable count of
a Diophantine definition.

## 1. A quantitative obstruction for any bounded-degree exception locus

Let \(E/\mathbb Q\) be the project's rational carrier \(y^2=x^3-2x\)
with nontorsion \(P=(9/4,-21/8)\). Put \(q=\widehat h(P)>0\),
\(H=[h]P,U=[j]P\), and retain ordinary rational abc. The doubled-point
denominator estimate of the
[duplication-mass paper](../../../papers/elliptic_divisibility/duplication_mass_and_bounded_quotients_20261124/README.md)
gives simple mass \(qn^2+o(n^2)\) for \([n]P\).

Let \(B=\mathbb A^1_X\times E_H\times E_U\), with boundary divisor
\(D=\mathbb A^1_X\times E_H\times\{O_U\}\). Fix a proper closed algebraic
subset \(Z\subsetneq D\) defined over \(\mathbb Q\).
Suppose a proposed rational relation on \(X,H,U\), with *arbitrary*
existential auxiliary variables, has the following uniform local property:

> There is a fixed finite exceptional set \(S\) of rational primes.
> For every \(p\notin S\), every rational solution with \(X\)
> \(p\)-integral, \(U\) formal of depth exactly one, and \(H\)
> nonformal has reduction \((X,H,O)\) in the reduction of \(Z\).

This property includes a rejection of all simple foreign contacts off
a bounded-degree exceptional locus, not just at primes of some
specified Frobenius type. Then the relation **cannot** admit witnesses
for every sufficiently large integer \(m=X\) with \(U=[m]H\) and
arbitrarily large \(|h|\).

**Proof.** On the affine Weierstrass chart of the first elliptic
factor of \(D\), choose a nonzero polynomial \(F(X,x(H),y(H))\)
vanishing on \(Z\) in that chart. Its restriction to the generic
\(X\)-fiber is nonzero. This is possible because the affine chart is
a dense open of the integral \(D\). If the intersection is empty,
take \(F=1\). Enlarge \(S\) by fixed coefficient denominators and
bad primes. For all but finitely many integers \(m\), the rational
function \(F(m,x,y)\) on \(E\) is not identically zero: reduce
modulo the monic equation of \(y\), and inspect a nonzero coefficient
polynomial in \(m\). For each such fixed \(m\), it vanishes at only
finitely many \(H\), so may be assumed nonzero along the arbitrarily
large admissible references.

At every retained foreign simple prime, \(x(H),y(H)\) are integral
and \(X=m\) is integral. Thus \(p\) divides the reduced numerator of
\(F(m,H)\). Its height is at most \(C_F qh^2+O_m(1)\), with \(C_F\)
independent of \(m\): evaluate a fixed polynomial and use the height
upper bounds \(h(x(H))=2qh^2+O(1)\) and
\(h(y(H))\le3qh^2+O(1)\) from the fixed Weierstrass equation.
The full simple-prime mass of \(U=[mh]P\) is \(qm^2h^2+o(h^2)\)
for fixed \(m\); deleting all denominator primes of \(H\) loses at
most \(qh^2+O(1)\). Consequently
\[
 (m^2-1)qh^2-o(h^2)-O(1)
   \le\log|\operatorname{num}F(m,H)|
   \le C_F qh^2+O_m(1).
\]
Let \(|h|\to\infty\) for this fixed \(m\). We obtain \(m^2-1\le C_F\).
This excludes all sufficiently large fixed \(m\), as claimed.
The argument allows a finite menu of exception loci by taking a
finite union (or multiplying their nonzero functions). QED.

In particular an all-prime local condition of the form
\[
 U\ {\rm simple\ formal},\ H\ {\rm nonformal}
 \quad\Longrightarrow\quad F(X,H)\equiv0\pmod p
\]
cannot replace the inert-prime norm obstruction if \(F\) has fixed
degree and the true multiplication family is retained. The point
of the argument is the growth \(m^2h^2\), not the mere presence of a
primitive prime. It applies to *any* relation with that local
implication, regardless of how its equations or auxiliary variables
are obtained.

## 2. Consequence for proper smooth models of coupled covers

Let \(f:V\to B\) be a dominant morphism of varieties over \(\mathbb Q\),
with \(V\) a smooth variety admitting a smooth proper-over-\(B\)
compactification. It is enough to have such a compactification after
a resolution that is an isomorphism on the guarded open of witnesses.
For example this holds for a smooth locally closed witness stratum
by taking a projective compactification of its graph and resolving
outside that stratum in characteristic zero.

Take a log resolution of the inverse image of \(D\), again unchanged
over the open of witnesses away from \(D\). The resulting smooth
proper morphism will be denoted \(\bar f:\bar V\to B\). We assume the
guarded witnesses lift to it; the preceding construction ensures this
for a smooth stratum away from the boundary. The Cartier divisor
\(\bar f^*D\) now has simple normal crossings after base change to a
fixed algebraic closure. Consider its irreducible components
dominating \(D\). Denote their multiplicities by \(e_i\).

**Theorem.** If a fixed cover, or a finite menu of covers, admits
guarded rational witnesses on the true multiplication graphs
\(X=m,U=[m]H\), with arbitrarily large references for every sufficiently
large integer \(m\), it cannot have all its boundary-dominating
components of multiplicity at least two (in every branch of the menu).

**Proof.** Suppose all those multiplicities are at least two. Remove
from \(D\) the proper closed images of the components of
\(\bar f^*D\) which do not dominate \(D\). These images are closed by
properness. Also remove the locus where a chosen boundary
description fails to spread out; all data are algebraic of finite type.
The resulting open in \(D\) is nonempty. After spreading out the
proper map, smooth variety, boundary components and local SNC
equations over a ring of integers with finitely many primes inverted,
the local Cartier equation of \(\bar f^*D\) at any lift of a point
reducing in that open is a unit times a product of the local
equations of the components, with their positive integral
multiplicities. One may split the components over a finite extension
unramified outside a fixed finite set; at remaining places the
normalized valuations of integral local equations are nonnegative
integers. These assertions also follow directly by taking the local
normal-crossing parameter charts and using their finitely presented
étale neighborhoods. Alternatively use the standard transverse
specialization argument for fibrations with multiple fibers.

Now suppose a rational witness projects to a \(p\)-integral base point
with simple contact to \(D\), away from the removed locus. At a good
prime, properness extends that rational lift to an integral local
point (after the indicated unramified splitting if needed).
The valuation of a local defining parameter of \(D\) is exactly one.
The pullback equation expresses this valuation as
\(\sum_i e_i a_i\) with each \(a_i\) a nonnegative integer and at
least one positive. All \(e_i\ge2\), a contradiction.
Thus the reduction of every allowed foreign simple contact lies in
the fixed proper closed removed locus of \(D\). Section 1 applies.
For a finite menu use the union of the exceptional loci, or apply
the bound to every branch separately. QED.

Nondominant smooth strata cannot by themselves carry arbitrarily large
references for an unbounded set of \(m\). Their images lie in proper
closed subsets of \(B\); for fixed sufficiently large \(m\) a
bounded-degree closed subset of \(E^2\) cannot contain the multiplication
graph of degree growing quadratically in \(m\). This is the graph-degree
argument of the [earlier no-cap theorem](quotient_cap_pole_obstruction_20261124.md).
Such strata intersect each graph in finitely many points, so they may be
discarded when testing the arbitrarily-large-reference completeness
requirement. Any polynomial source admits a finite smooth
stratification of its witness variety in characteristic zero; the
theorem applies to the above proper models of its dominant smooth
strata. It does not assert that a rational point of an arbitrary
singular model lifts to an arbitrary resolution.

## 3. What a multiplicity-one component permits locally

Conversely, suppose a proper resolved cover has a component of
multiplicity one dominating \(D\).
At a general geometric point on this component, away from other
boundary components, the pullback of the parameter of \(D\) vanishes
to first order. The map of that component to \(D\) is dominant and
generically smooth in characteristic zero. At a general smooth point
where its differential is surjective onto the tangent space of \(D\),
the differential of the entire morphism is surjective onto the
tangent space of \(B\): the extra transverse parameter pulls back to
a local equation of the component times a unit. Hence the map is
smooth there by the Jacobian criterion.

Choose an algebraic closed point in this smooth open mapping into
\(D\) with \(H\ne O\), and outside any prescribed proper closed
subset of \(D\). Its coordinates and the local map are defined over
some number field. At infinitely many rational primes splitting
completely in that field, outside a fixed finite set, this smooth
point reduces to an \(\mathbb F_p\)-point and the reduced morphism
is smooth there. By the elementary smooth form of Hensel's lemma,
there are \(p\)-adic lifts of nearby base points having exactly
depth-one contact with \(D\). The first factor can remain nonformal.

This does not assert the existence of rational witnesses for those
base points, and does not place them in the cyclic-index family.
It establishes the generic geometric distinction: a multiplicity-one
component allows transverse contacts at appropriate split primes;
multiple fibers provide a Frobenius-independent obstruction but
would violate the required completeness here.

The local geometry is related to the arithmetic-surjectivity
criteria for fibrations studied by Loughran and Smeets,
*Fibrations with few rational points*, Geom. Funct. Anal. 26
(2016), 1449--1482, and Loughran, Skorobogatov and Smeets,
*Pseudo-split fibers and arithmetic surjectivity*, Ann. Sci. Éc.
Norm. Supér. 53 (2020), 1037--1070. We only use the elementary
smoothness and multiple-divisor arguments above, not their global
surjectivity theorems. In particular no pseudo-split criterion
for all modifications is asserted for the present source.

## 4. Necessary change of strategy

True integer multiples necessarily have simple foreign denominator
mass asymptotic to \(q(m^2-1)h^2\) for fixed \(m\) as \(|h|\to\infty\).
Thus all-prime **control** must allow this mass to pass through the
cover, not indiscriminately forbid it. The accompanying nine-coordinate
charging relation achieves precisely such a transfer into a free
rational witness, with sharp height cost \(3q(m^2-1)h^2\).

The obstruction here shows why simply replacing the constant
quadratic norm extension by a fixed-degree family with no
multiplicity-one component at the foreign boundary cannot work.
A viable next mechanism needs a nonlocal condition on the rational
lifts, an arithmetic bound on a moving witness with genuinely nonlinear
logarithmic-height budget, or a different completeness requirement
(not arbitrarily large references for each fixed input).

These conclusions concern specified local and height mechanisms.
They do not prohibit all-prime comparisons with new moving residue
conditions depending on auxiliary variables, nor a genuinely global
rational-point obstruction. No quotient cap or new numerical
defining-variable count is established.
