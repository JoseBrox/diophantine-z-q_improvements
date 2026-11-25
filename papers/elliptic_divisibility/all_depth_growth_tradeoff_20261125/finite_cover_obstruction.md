# Obstruction to cofinal bounded-charge finite covers

This note restricts the deficit-charge target in [README.md](README.md)
and the double-quotient height-cap problem in
[double_quotient.md](double_quotient.md). Neither result is a general
impossibility theorem for Diophantine definitions.

## 1. A cofinal finite-cover obstruction for the deficit charge

Let \(K\) be a fixed number field, \(E/K\) a fixed elliptic curve
in a fixed integral Weierstrass model, and \(P\in E(K)\) nontorsion.
Write \(Q=[c]P\), \(T=[j]P\), and use the deficit \(D(c,j)\) from
the main note with the analogous maximum over the places above p
in K. Exclude a fixed finite set containing bad and ramified primes
and 2. The full denominator asymptotic used there is valid over K.

Suppose a proposed auxiliary predicate is a fixed finite menu of
algebraic systems over K, with a charge \(s\in\mathbb Q\).
After Q and s have been fixed, the remaining auxiliary choices are
finite algebraic choices over the variable point T on E. In particular,
they form finite-type covers of open subsets of E with a uniform
degree bound \(d_{\max}\) on their nonconstant curve components.
All remaining auxiliary values may lie in K, and every such K-valued
lift satisfying the equations and guards is an accepted tuple (the charge
s itself is still rational). A restriction that certain remaining
K-valued auxiliary coordinates must be rational, not merely K-valued,
is not covered by this argument unless it is already encoded by the
algebraic cover. The guards are algebraic nonvanishing conditions. This includes
successive monic finite-root equations with a fixed number of roots
and fixed degrees, possibly followed by additional polynomial equalities.

Assume every accepted tuple satisfies
\[
 D(c,j)\le C_D(1+h(s)).
\]
Suppose, for arbitrarily large c in absolute value, the predicate has
infinitely many distinct accepted T with
\(h(s)\le M(c)=o(c^2)\). This is impossible.

Indeed, for each fixed such Q, Northcott's elementary finiteness for
rationals of bounded height makes the menu of possible charges finite.
Some fixed charge and some curve component then have infinitely many
K-points above distinct T. Normalize and complete that component.
Its nonconstant map to E implies genus at least one by
Riemann--Hurwitz; by Faltings' theorem its genus cannot exceed one.
Components not geometrically irreducible over K contribute only
finitely many K-points off the common intersections of distinct
Galois conjugates, so one can use a geometrically integral component
defined over K. A K-point makes its smooth projective normalization
an elliptic curve. The map to E is an isogeny followed by translation.
Let \(d\le d_{\max}\) be its degree, and let \([j_0]P\) be an accepted
value. Composing with the dual isogeny shows that the image contains
\[
 [j_0+dt]P,\qquad t\in\mathbb Z,
\]
apart from finitely many exceptions arising from the deleted points
or nonvanishing guards. For every such image point there is a K-valued
lift to the selected component. When the original equations are over Q,
apply the argument over Q to get rational lifts.

Take all rational primes supporting Q's formal denominators outside
S and not dividing d. By the Chinese remainder theorem choose t so
that \(p\nmid j=j_0+dt\) at every such prime. The finitely many
deleted image points and j=0 can be avoided in that progression.
At a place of maximal depth a of Q, if T is formal then
\(b=a+v_p(j)-v_p(c)\le a\) by the formal logarithm.
If T is not formal then \(b=0\). In either case
\(\delta_p\ge a\). Hence
\[
 D(c,j)\ \ge\ \sum_{p\notin S,\ p\nmid d}a_p\log p
            \ \ge\ q c^2-o(c^2).
\]
The second estimate is uniform in the selected component because the
primes dividing \(d\) belong to a fixed finite set of primes at most
\(d_{\max}\); their mass is \(O(1+\log|c|)\).
This contradicts the bounded charge inequality for large c.

In particular, the canonical choice s=0 cannot work in this class of
cofinal finite-cover constructions. Even a varying charge satisfying
the modular bound \(h(s)=O(|c|^{3/k}+\log|c|+1)\) is ruled out for
k>=3 if cofinality in T is demanded for each fixed Q.

**Scope:** this is about finite algebraic covers over the *curve E*
in the variable T, not general rational-component equations in both
T and its conjugate. On the quadratic carrier, conjugate-coupled
equations can instead give covers of the two-dimensional Weil
restriction. The genus-one argument does not apply to those surfaces.
The argument also does not exclude selecting a single T (or finitely
many T) for each fixed Q, or using additional ordinary auxiliary
variables. Extra imposed local conditions not encoded by the stated
algebraic system are not covered either. In particular the original
conditional 17/19 count is not promoted to a record; a successful
deficit charge would need to escape this obstruction.

## 2. Double-quotient graphs are not algebraic curves

Over Q, or over a real number field K on the project carriers with
geometric j-invariant 1728, the K-endomorphism ring of E is Z.
Fix any nonzero integer m. Consider the points
\[
 ([h]P,[h+m h(h-1)]P)\in E^2(K),\qquad h\in\mathbb Z.
\]
Any infinite subset of these points is Zariski dense in \(E^2\).

For otherwise a curve component contains infinitely many points,
and its normalization maps nonconstantly to the first E. By the
same genus and Faltings argument, it is an elliptic curve over K.
The first projection is an isogeny after choosing an origin, and
the second is a homomorphism up to translation. Composing the
second homomorphism with the dual of the first produces an
endomorphism of E, hence multiplication by a fixed integer k.
Thus on the component there is an identity
\[
 [d]U=[k]H+C
\]
for a positive integer d and a fixed point C. On the indicated
points this would make the quadratic polynomial
\(d(h+m h(h-1))-kh\) constant on infinitely many integer h, since
P is nontorsion. Its quadratic coefficient dm is nonzero, a
contradiction.

This is a geometric obstruction even for one fixed true nonzero
double quotient m, not a dimension count for moving input m.
It rules out eliminating the numerator point by a finite-degree
algebraic reconstruction from H at fixed m with infinitely many
allowed references. It leaves open genuinely two-dimensional
coupled constraints and noncofinal completeness mechanisms.

The arithmetic finiteness input in both arguments is Faltings'
theorem on rational points of curves of genus at least two over a
number field. The remaining facts are standard Riemann--Hurwitz,
the homomorphism-plus-translation description of maps of elliptic
curves, and dual isogenies. The local denominator identities were
checked separately in verify.js; the arguments above are proofs,
not empirical extrapolations.
