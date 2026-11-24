# Finite Kummer tests do not supply a quotient-size cap

## Scope

This extends the [geometric no-cap theorem for uncoupled prepared poles](quotient_cap_pole_obstruction_20261124.md) to arbitrary finitely many extra independent perfect-power tests on the same input and two elliptic points. It is an obstruction to a specified strategy, not a lower bound for general existential definitions, and does not settle the original nine-coordinate target.

Assume ordinary rational abc, and retain the setting of the earlier theorem: \(E/\mathbb Q\), a fixed nontorsion \(P\in E(\mathbb Q)\), the rational input \(X\), and \(H=[h]P,U=[j]P\). A finite menu of branches may use:

* rational-function equalities and nonzero guards on \((X,H,U)\);
* finitely many uncoupled prepared BB poles on rational functions of those same data;
* finitely many **Kummer tests**
  \[
     Z_i^{e_i}=f_i(X,H,U),\qquad e_i\ge2,
  \]
  with fixed positive integer exponents, rational-function right hand sides, and nonzero defined values;
* fixed real and finitely many finite-place open conditions on the base points and the Kummer roots.

The roots do not occur in other Kummer right hand sides or in the pole inputs. Rational-function guards involving the roots are allowed provided they are nonzero at the chosen witnesses (and are not additional equalities). No claim is made about arbitrary coupled covers or about covers with new transcendental parameters.

**Theorem.** If every sufficiently large positive integer \(m\) admits prepared solutions in this menu with \(X=m\), \(U=[m]H\), and arbitrarily large positive \(h\), there is one integer input \(m_0\) and one fixed reference \(H_0=[h_0]P\ne O\) for which the same source has prepared solutions with \(U=[M]H_0\) for arbitrarily large positive integers \(M\).

In particular finitely many independent square or higher-power tests, even if their roots are absorbed into a finite algebra at no free-coordinate cost, cannot repair the quotient-size-cap strategy under this completeness requirement. The Kummer part of the argument uses Faltings, not abc. The ordinary rational abc hypothesis is needed only for the old BB-pole part.

## 1. Multiplication graphs and Kummer ramification

Fix one nonzero function \(f\in\mathbb Q(X,E^2)\) and exponent \(e\ge2\). On the geometric generic \(X\)-fiber, suppose some irreducible divisor \(D\) in the zero or pole divisor of \(f\) dominates the first elliptic factor and has nonzero order \(r\) not divisible by \(e\). (Negative order means a pole.)

For all sufficiently large positive integer specializations \(X=m\), the specialized geometric components, their divisor multiplicities, projection degrees and geometric genera are uniformly bounded as in Section 3 of the preceding no-cap proof. The indicated component persists with multiplicity \(r\) and its first projection is still nonconstant. The same intersection argument applies to a zero divisor as to a pole divisor, with the sign of \(r\) unchanged.

More explicitly, on the normalization of the indicated specialized divisor, with projections \(a,b\) to \(E\), its intersections with the graph \(G_m:H\mapsto(H,[m]H)\) are the zero fiber of \(b-[m]a\). Its degree is at least
\[
 (m\sqrt{\deg a}-\sqrt{\deg b})^2
\]
for all sufficiently large \(m\); the total ramification of this map to \(E\) is bounded by the uniformly bounded genus. The preimages of singularities and intersections with other zero/pole components have uniformly bounded cardinality by projective degree and genus bounds. Their total intersection multiplicity is bounded by their cardinality plus the total ramification. It follows that there are not merely one but a number tending to infinity of **distinct** transverse intersections with the graph away from every other zero/pole component. At each such point the restricted rational function
\[
  f_m(H)=f(m,H,[m]H)
\]
has order exactly \(r\). The map from the graph to \(E\) is the first projection, an isomorphism, so these are distinct geometric points of its base \(E\). No denominator identically vanishes on the large graphs, since a divisor of uniformly bounded projective degree cannot contain them.

Let \(C\) be the normalization of the projective Kummer cover \(Z^e=f_m(H)\) over the geometric base. Every geometric irreducible component of \(C\) is ramified over each of the points just found: its inertia index there is \(e/\gcd(e,r)>1\). To see this even if the polynomial factors over the function field, work in the local field of the smooth base with algebraically closed residue field of characteristic zero. A unit has an \(e\)-th root in the completed local ring by Hensel, so the equation is locally the Kummer equation with radicand a uniformizer to order \(r\). Its extensions have this ramification index. Alternatively, after adjoining all roots of unity, the group acts transitively on the generic components, and the local inertia computation is identical on them.

The base has genus one. Riemann–Hurwitz for any such component gives \(2g(C_0)-2\) equal to a positive ramification sum. Thus every component has genus at least two; one transverse point already suffices for this conclusion. Choose a fixed number field containing the coefficients of all the components for this fixed \(m\). Faltings' finiteness theorem gives only finitely many rational points over that number field on each smooth projective component. The guarded affine Kummer points are on a smooth open of these normalizations, since the radicand is defined and nonzero. Therefore only finitely many \(H\in E(\mathbb Q)\) can have a rational Kummer lift at this fixed \(m\).

Consequently, in any branch admitting arbitrarily large references for an unbounded set of \(m\), all nonvertical geometric divisor orders of every \(f_i\) must be divisible by its \(e_i\). No hypothesis on the ranks of the covering curves is needed for this deduction.

## 2. Fixed-reference specialization becomes étale

By the uncoupled-pole theorem, in such a branch all nonvertical generic geometric **pole** orders of the BB scalar functions are even. Its equality constraints hold identically generically. These facts use the arithmetic lemma in that theorem for BB poles, and the bounded-degree multiplication graph argument for equalities. For Kummer right hand sides we have the stronger divisibility condition on all nonvertical zeros and poles from Section 1.

Choose a sufficiently large \(m_0\) from the branch's unbounded set of inputs avoiding the finitely many exceptional specializations. Choose one of its arbitrarily large prepared reference indices \(h_0\) so that \(H_0=[h_0]P\) avoids the finite vertical zero/pole fibers, projection branch values, images of singularities and intersections of distinct components for every rational function in question. These exclusions are legitimate for fixed \(m_0\); all the relevant divisors are now fixed, and a nontorsion cyclic group visits any finite set only finitely often.

With \(X=m_0\) and \(H=H_0\) fixed, every nonzero Kummer rational function of \(U\) on \(E\) has all geometric divisor orders divisible by its exponent. Its normalized projective Kummer cover is finite étale over \(E\) (it may be disconnected); the local computation above gives index one at every point. Take the fiber product of these finite étale covers, and its connected component through the chosen rational lifts at \(U_0=[m_0]H_0\). This component is smooth, projective, geometrically connected over \(\mathbb Q\), and of genus one. For the geometric connectedness assertion, the fiber product is normal, its geometric connected components are disjoint, and the rational point lies on a Galois-invariant unique geometric component. That component descends to \(\mathbb Q\).

Denote the resulting elliptic curve, using this rational point as its origin, by \(E'\). Its projection to \(E\), translated by \(-U_0\), is a nonconstant morphism of elliptic curves preserving the origins, hence an isogeny \(\varphi:E'\to E\). If \(d=\deg\varphi\), the dual isogeny satisfies \(\varphi\hat\varphi=[d]\). Thus \(Q'=\hat\varphi(H_0)\in E'(\mathbb Q)\) is nontorsion, and the points \([r]Q'\) project (in the original, untranslated projection) to
\[
 U_0+[dr]H_0=[m_0+dr]H_0.
\]
Their Kummer coordinates are rational wherever defined. No uniform bound on \(d\) or arithmetic computation of the isogeny is necessary.

## 3. Approximation preserves the actual pole preparations

Every BB scalar specialized at the fixed \(m_0,H_0\) has even geometric pole orders on \(E\). By the unconditional local divisor argument in the earlier no-cap theorem, its nonzero defined rational values have no negative odd valuations outside a fixed finite set of rational primes depending on these specializations. Include all these primes, the original finite-place conditions and the dyadic preparation in one finite set.

Take sufficiently small neighborhoods of the origin of \(E'\) at all these finite places, and in the real topology. The maps giving the base point and the Kummer roots are regular at that origin on the guarded open. All the original nonzero values, fixed-place open conditions, dyadic class and depth, and real intervals \(0<b_i<1\) persist after sufficiently shrinking the neighborhoods. In particular, the known prepared valuations at the finite excluded primes persist. Outside them the even-pole property already ensures square denominator. Nonzero guards involving Kummer roots also persist by continuity at the known rational point.

The compact real and local elliptic groups give arbitrarily large positive \(r\) for which \([r]Q'\) belongs to all these neighborhoods. One can first take an integer progression ensuring the prescribed formal neighborhoods at each of the finitely many finite places, and then use recurrence in the compact real cyclic closure of a multiple of \(Q'\). Finitely many additional algebraic guard poles or zeros on the component can be avoided, since they do not contain the chosen guarded point. The equality constraints on the base are identically satisfied as in the earlier theorem. Any fixed index congruences can be incorporated into the progression by a further fixed multiple.

For each such \(r\), all Kummer tests and guards hold and all the uncoupled BB inputs are actually prepared. Invoke the same prepared BB converse independently on those scalars. This yields the required rational solutions with \(M=m_0+dr\) unbounded. The argument works without a BB pole or without any Kummer tests as special cases.

For a finite menu, at every large integer \(m\) some branch has unbounded prepared reference indices. One branch has this property for an unbounded set of inputs. The preceding arguments require only this unbounded set, since the exceptional parameter sets are finite, and therefore prove the theorem for the menu.

## 4. Relevance to the nine-coordinate target

The extension rules out a potentially attractive low-cost repair: adding any fixed finite collection of independent algebraic power tests in the existing three base data, then absorbing their roots into the old finite-algebra encoder. If the tests have moving ramification in the numerator point, Faltings destroys the required infinite reference family for large integer inputs. If the ramification is absent, finite étale covers of elliptic curves preserve an infinite arithmetic progression of numerator indices.

A viable repair must go beyond this class: for example an independent free scalar entering a genuinely coupled cover, a higher-degree non-Kummer cover whose restrictions can have a special low-genus component, or a completeness mechanism with only finitely many admissible reference indices for each fixed integer input. No construction of such a cap is established here. In particular the conclusion is about unbounded quotient size at a fixed integer input; it is not a statement that all enlarged sources accept noninteger inputs.

The standard ingredients are the multiplication-graph intersection lemma already proved in the companion theorem, Riemann–Hurwitz, Faltings' theorem on rational points of curves of genus at least two, the group structure of a pointed genus-one curve, and duality of elliptic isogenies. All these apply in characteristic zero over fixed number fields; no uniform Faltings constant is used. For the uncoupled-pole part ordinary rational abc and the stated BB realization are retained.