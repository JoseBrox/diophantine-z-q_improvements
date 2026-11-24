# A geometric obstruction to quotient caps using only additional prepared poles

This is a new conditional obstruction, not an impossibility theorem for the nine-coordinate target. It concerns the particular strategy of adding finitely many BB pole tests whose input scalars are rational functions of the existing two elliptic points and external rational input, with no additional independent geometric witnesses entering those scalars.

## 1. Precise theorem

Assume ordinary rational abc. Let \(E/\mathbb Q\) be an elliptic curve and \(P\in E(\mathbb Q)\) a fixed nontorsion point. Write \(H=[h]P,\ U=[j]P\). Consider a finite menu of branches of the following form:

* Fixed rational functions \(b_i\in\mathbb Q(X,E\times E)^\times\).
* Fixed rational-function nonzero guards (including their denominator guards), and optionally rational-function equalities.
* Any fixed real or finite-place open conditions on \((X,H,U)\), including conditions imposed to prepare the poles.
* A separate prepared BB product pole for each \(b_i\), with no restrictions on its auxiliary variables except the defining pole equations and their usual nonzero-input requirements. In particular, those auxiliary variables do not enter other scalar functions or couple different poles.

A branch is *prepared* when its actual inputs \(b_i\) satisfy the conditions of the published sufficient realization theorem, namely square reduced denominator, \(0<b_i<1\), class seven over \(\mathbb Q_2\), and sufficient two-adic depth. Fixed square multipliers or finitely many prescribed constant factors in the scalar may be absorbed into \(b_i\). We allow a fixed finite excluded set of primes in the arithmetic discussion, but the prepared witnesses still satisfy the full square-denominator requirement.

Suppose that for every sufficiently large positive integer \(m\), there are prepared witnesses in the menu for
\[
 X=m,\quad H=[h]P,\quad U=[m]H
\]
with arbitrarily large positive \(h\). Then, for some integer input \(X=m_0\) and some fixed nonzero reference \(H_0=[h_0]P\), the same menu has prepared solutions with
\[
 U=[M]H_0
\]
for arbitrarily large integers \(M\). In particular no bound on \(|j/h|\) as a finite function of \(H\) and \(X\), much less a bound \(\log(1+|j/h|)\le C\widehat h(H)+O(1)\), can hold on all its solutions.

This result applies to adding any finite number of **uncoupled** prepared BB poles to the [six-coordinate quotient](../../../papers/elliptic_divisibility/height_anchored_quotient_20261124/README.md), using only rational functions of its existing \(X,H,U\). It also covers fixed isogeny-coset restrictions given by open congruence conditions on indices, since a fixed congruence progression is preserved by the final approximation. It does not rule out adding a new independent scalar inside a pole input, an independent point, a coupled pole witness, or an additional global algebraic cover that is not described by the above functions and open conditions. It is not a proof that every such extended source admits noninteger inputs.

## 2. Arithmetic lemma: every fixed geometric point receives simple contacts

**Lemma.** Assume ordinary abc over \(\mathbb Q\). Fix a nonzero rational function \(f\) on \(E/\mathbb Q\). If \(f\) has a geometric pole of odd order, then, for every sufficiently large \(|h|\), the rational value \(f([h]P)\), when defined, has negative odd valuation at some rational prime outside any prescribed fixed finite set.

**Proof.** Use the marked version of Belyi's theorem to choose a morphism \(\pi:E\to\mathbb P^1\), defined over \(\mathbb Q\), ramified only above \(0,1,\infty\), with all closed points of the zero and pole divisors of \(f\) included in the inverse image of these three points. This version is stated explicitly in P. Vojta, *Diophantine Approximation and Nevanlinna Theory*, Theorem 31.1, p. 219, [PDF](https://math.berkeley.edu/~vojta/cime/cime.pdf#page=107). Including all zeros is harmless and makes reduction arguments transparent.

Let \(d=\deg\pi\), and write \(D_1,\ldots,D_d\) for the distinct geometric points over the three contact values. There are exactly \(d\) points by Riemann--Hurwitz on the genus-one curve: the total ramification contribution is \(2d\), while the three fiber degrees sum to \(3d\). Extend to a fixed number field \(L\) containing all \(D_i\), and use absolute heights and local prime weights \(\log N\mathfrak p/[L:\mathbb Q]\). Exclude the finitely many bad and ramified primes, and those where different \(D_i\) or any zeros and poles of \(f\) have intersecting reductions. Over a good residue characteristic, the local intersection of the section \([h]P\) with \(D_i\) has multiplicity equal to the formal depth of \([h]P-D_i\) if this difference is formal, and zero otherwise.

Put \(q=\widehat h(P)>0\). For each fixed \(D_i\), the sum \(A_i(h)\) of full finite contact multiplicities with those normalized weights is at most
\[
 h(x([h]P-D_i))/2=qh^2+O(1+|h|).
\]
Indeed on a fixed Weierstrass model a formal point has abscissa valuation minus twice its depth, and the canonical height of \([h]P-D_i\) is a quadratic in \(h\) with leading term \(qh^2\). This holds for non-torsion as well as torsion \(D_i\). Finitely many values where a difference is the identity can be excluded. Let \(T_i(h)\) denote the corresponding truncated count, with each positive local multiplicity replaced by one.

The divisor of poles of \(\pi\) has degree \(d\); on \(E\) over \(L\), its class is linearly equivalent to \((d-1)[O]+[T]\) for a fixed point \(T\) (identify \(\operatorname{Pic}^0(E)\) with \(E\)). The height machine and the same quadratic estimate give
\[
 h(\pi([h]P))=d qh^2+O(1+|h|).
\]
Unlike the torsion-only case, a linear error in \(h\) may occur, but it is negligible here.

Apply ordinary rational abc to the rational value \(\pi([h]P)\). At the retained primes its truncated count for \(0,1,\infty\) is exactly \(\sum_iT_i(h)\), by the good model of the finite map and disjointness of the marked reductions. The prime weights from \(L\) sum to the original rational-prime weight. Exclusion of the fixed exceptional primes costs only a bounded amount in the truncated count. Thus
\[
 \sum_i T_i(h)\ge d qh^2-o(h^2).
\]
To see the indicated error, first fix an arbitrary weak exponent \(1+\epsilon\) from ordinary abc, take the liminf normalized by \(h^2\), then let \(\epsilon\downarrow0\). Since each \(T_i\le A_i\le qh^2+O(|h|+1)\), we obtain for every individual \(i\)
\[
 T_i(h)=qh^2+o(h^2),\qquad A_i(h)-T_i(h)=o(h^2).
\]
The truncated count at contacts of multiplicity at least two is bounded by their multiplicity surplus. Consequently the logarithmic weight of **simple** contacts with each \(D_i\) is \(qh^2+o(h^2)\). In particular there is such a simple contact with any chosen geometric odd-order pole of \(f\), for every sufficiently large \(|h|\).

At that prime of \(L\), the rational function \(f\) has valuation equal to its pole order with negative sign, because the contact multiplicity is one and the other zeros and poles do not reduce to that point. Since the underlying rational prime is unramified, this is also the normalized valuation of its rational value over \(\mathbb Q\). It is negative odd, as required. \(\square\)

This proof uses abc only for the rational number \(\pi([h]P)\), not abc over the extension splitting the marked points. It does not use a primitive-prime theorem or a uniform-in-\(f\) height bound. Each \(f\) here is fixed before letting \(|h|\to\infty\).

Conversely, if a rational function \(f\) on \(E\) has only even geometric pole orders, then all its defined nonzero rational values have no negative odd valuations outside a finite set depending on \(f\): spread out the split zero/pole divisors over the ring of integers of a fixed splitting field, discard ramification and collision primes, and use the same local intersection calculation. This converse is unconditional.

## 3. Geometric lemma: large multiplication graphs meet bounded-degree pole divisors transversely

Let \(b(X,H,U)\) be a nonzero rational function on \(\mathbb A^1\times E^2\) over \(\mathbb Q\). Work geometrically in characteristic zero. Call a divisor on \(E^2\) *vertical* if its projection to the first \(E\) factor is constant. Thus an irreducible nonvertical divisor dominates the first \(E\), and corresponds to a possible moving pole as a function of the second point \(U\) with \(H\) fixed.

**Lemma.** If the generic \(X\)-fiber of \(b\) has an odd-order geometric pole divisor which is nonvertical, then for every sufficiently large positive integer \(m\), the restricted function
\[
 b_m(H)=b(m,H,[m]H)
\]
has an odd-order geometric pole on \(E\).

**Proof.** Fix a projective embedding of \(E^2\) by a power of the product polarization. The zero and pole divisors of \(b\) on a generic \(X\)-fiber can be represented as components of two sections of one fixed line bundle, after clearing denominators. By spreading out the finitely many geometric irreducible components after a finite base extension of the \(X\)-line, there is a nonempty open subset of that line where their multiplicities, fiberwise geometric irreducibility, and degrees of the two projections remain constant, with all degrees uniformly bounded. This is the usual openness of geometric integrality for a flat proper family with geometrically integral generic fiber. One may discard finitely many parameter values to remove specialization collisions of distinct components and any cancellation in the numerator and denominator. In particular, for every sufficiently large \(m\) an odd-order nonvertical geometric component \(D_m\) persists. The degrees of all zero/pole components are uniformly bounded.

Normalize this integral curve \(D_m\) to \(C_m\). Let \(f,g:C_m\to E\) be its first and second projections. Then \(\deg f\ge1\), while \(\deg g\) is bounded independently of \(m\) (degree zero when it is constant). The geometric genera of the normalizations, the arithmetic genera of the integral curves and the number of their singular branches are uniformly bounded by their fixed projective degree bound. For example, the arithmetic genus of an integral projective curve of bounded degree is bounded by the plane projection genus bound, and the number of branches over singular points is bounded by twice the total delta invariant plus a harmless constant. The number of intersections with all other zero/pole components is uniformly bounded by projective Bézout, since these are distinct curves.

The intersection with the multiplication graph is described on \(C_m\) by the fiber over \(O\) of
\[
 \phi_m=g-[m]f:C_m\to E.
\]
Take an invariant nonzero holomorphic differential \(\omega\) on \(E(\mathbb C)\), normalized to have squared norm one, with norm defined by integrating \((i/2)\omega\wedge\bar\omega\). For a morphism to \(E\), the squared norm of its pullback equals its degree, by change of variables (zero for a constant). The group-law identity for invariant differentials gives
\[
 \phi_m^*\omega=g^*\omega-m f^*\omega.
\]
The triangle inequality yields, for all sufficiently large \(m\),
\[
 \deg\phi_m\ge (m\sqrt{\deg f}-\sqrt{\deg g})^2.
\]
Thus \(\phi_m\) is nonconstant and the degree tends to infinity at least quadratically, uniformly in the allowed components. This argument applies even if \(C_m\) varies with \(m\).

The total ramification of a nonconstant map \(C_m\to E\) is \(2g(C_m)-2\). In particular the excess multiplicity in the fiber \(\phi_m^{-1}(O)\) is uniformly bounded. Exclude the preimages of the singular points of \(D_m\) and of its intersections with any other zero or pole divisor. Their number is uniformly bounded by the preceding degree/genus bounds, and their total fiber multiplicity is at most their number plus the total ramification. Since the full fiber degree grows quadratically, there is a point remaining in the fiber of multiplicity exactly one. At its smooth image in \(D_m\), the multiplication graph meets \(D_m\) transversely. Indeed the graph is defined locally by \(g-[m]f=O\) in the ambient product, and its pullback to the smooth divisor has intersection multiplicity one; the local intersection number is symmetric on the smooth surface.

At this intersection the rational function \(b(m,\cdot,\cdot)\) has exactly the given odd pole order along \(D_m\), with no other divisor through the point. Restricting to the graph gives a pole of precisely that odd order. All graphs for large \(m\) are outside the cases where the restriction is identically zero or undefined, since a divisor of bounded projective degree cannot contain the graph of unbounded degree. This proves the lemma. \(\square\)

This uses characteristic-zero complex analysis only for the elementary degree estimate of a morphism to an elliptic curve. There is no inference from a dimension count alone. Uniform control of tangencies is essential: a nonempty intersection of a graph and a pole divisor would not suffice if every multiplicity were even.

## 4. Proof of the obstruction theorem

First suppose there is just one branch. For every sufficiently large integer \(m\) it has arbitrarily large prepared reference indices with \(X=m,U=[m]H\). If any scalar \(b_i\) had an odd nonvertical pole component on its generic \(X\)-fiber, Section 3 would give an odd pole on the restricted function \(b_i(m,H,[m]H)\) for every sufficiently large \(m\). Fix one such \(m\). Section 2 shows that for all sufficiently large \(|h|\), this scalar at \([h]P\) has a negative odd valuation outside any fixed excluded set, contradicting square reduced denominator. Hence every nonvertical generic geometric pole component of every scalar has **even order**.

Optional rational-function equality constraints cannot be nontrivial generically in a complete branch. Indeed for a fixed specialization \(X=m\) a nonzero equality expression on \(E^2\) has zero divisor of bounded degree; for large \(m\) it cannot vanish identically on the multiplication graph. Its zeros on that graph are then finite, precluding arbitrarily large \(h\). If an expression is identically zero on \(E^2\) for infinitely many \(m\), it is identically zero over \(\mathbb Q(X)\). This also permits omission of finitely many exceptional specializations.

Choose a sufficiently large integer \(m_0\) outside all the finite exceptional sets in these arguments. For a fixed generic \(X=m_0\), specializing the first elliptic point to \(H_0\) away from a finite set makes each scalar a rational function in \(U\) whose geometric poles all have even order. To verify this last assertion, omit the finitely many vertical pole/zero fibers, the branch points of projection to the first factor on the nonvertical components, the images of singularities, and the intersections of distinct components. At the remaining \(H_0\), each nonvertical component restricts transversely to the fiber, preserving its multiplicity; even multiplicities would in fact suffice even without transversality. This finite exclusion is compatible with choosing a prepared witness \(H_0=[h_0]P\) from the arbitrarily large reference indices.

Now fix this \(X=m_0\), this \(H_0\), and the known prepared value \(U_0=[m_0]H_0\). By the unconditional converse of Section 2, every defined nonzero value of every scalar \(b_i(m_0,H_0,U)\) has no negative odd valuation outside a fixed finite set of primes. This set depends on \(m_0,H_0\), which have now been fixed, not on the varying \(U\). Include the original finite preparation places and 2 in it. At each of these primes take a sufficiently small neighborhood of \(U_0\) so the nonzero scalar values preserve their valuations, and preserve their two-adic squareclasses when required. At the real place shrink a neighborhood of \(U_0\) so every \(0<b_i<1\) and all other open guards persist. These are valid local neighborhoods by continuity at defined, nonzero scalar values. Remove the finite zeros/poles of nonzero algebraic guards as necessary; none is identically zero since the prepared witness satisfies them.

There are arbitrarily large positive integers \(M\) with \([M]H_0\) simultaneously in these neighborhoods. Indeed at each finite place a sufficiently small formal subgroup has finite index in the compact elliptic group; choose a common fixed multiple of the necessary moduli so that the resulting progression of indices \(M\equiv m_0\) preserves all finite neighborhoods and any fixed congruence conditions. In the real compact cyclic closure, multiply the step further by its component-group order so the progression is dense in the component of \(U_0\); equivalently use the ordinary recurrence of a nontorsion point in its real cyclic closure. There are arbitrarily large such \(M\), and finitely many exceptional algebraic point fibers can be avoided. All equalities in this branch are identically satisfied by the preceding argument. All actual scalar values are again prepared at every prime and really. The BB theorem then supplies the independent pole witnesses. Thus \(j/h_0=M\) is unbounded for fixed \(X,H_0\), proving the assertion.

For a finite menu, at every large \(m\) one branch contains prepared solutions with arbitrarily large \(|h|\), since a finite union of bounded index sets is bounded. At least one branch does so for an unbounded set of integers \(m\). Apply the preceding argument to that branch using only this unbounded set. Every exceptional parameter set used above is finite, so there is a suitable \(m_0\) in it. The conclusion follows.

## 5. Implications for the requested cap

This theorem separates a local improvement from the genuinely new geometry required. Adding more finite-precision ratio tests, replacing the scalar rational function, or adding independently realized BB poles without new free data entering their inputs cannot yield a complete quotient-size cap of the desired type. The conclusion holds even with arbitrarily high fixed degrees and arbitrarily many such pole tests, under the stated integer completeness with arbitrarily large references. It does not use the six-coordinate source's particular false-positive examples.

For the remaining nine-coordinate target, a plausible next approach must involve an independent parameter or point entering the new scalar, a nontrivial finite cover or coupling not reducible to the displayed rational-function conditions, a different arithmetic predicate with a global (rather than square-denominator) soundness mechanism, or a source whose integer completeness does not require arbitrarily large reference indices for each fixed integer. None of these alternatives is established here.

No new numerical defining-polynomial bound, unconditional obstruction, or lower bound on arbitrary existential definitions of \(\mathbb Z\) is claimed. The marked Belyi theorem and ordinary rational abc are essential to the arithmetic part; the multiplication-graph argument is geometric and unconditional.