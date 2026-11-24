# Coupled curve-cap obstructions: unpointed genus one, torsion Jacobians, and constant moduli

## Result and exact scope

Continue the [seven-coordinate conic charge](../../../papers/elliptic_divisibility/one_conic_foreign_charge_20261124/README.md) on
\[
 E:y^2=x^3-2x,\quad P=(9/4,-21/8),\quad q=\widehat h(P)>0.
\]
Use \(H=[h]P,\ U=[j]P\), with \(h,j\ne0\), and \(g_H^2=x(H),g_U^2=x(U)\).
Write \(h_{\rm W}\) for logarithmic rational or absolute Weil height. The charge equation is
\[
 \tag{C} r^2=1+(g_U/g_H^2)s^2,\qquad s\ne0.
\]
We retain the cyclic chart, ordinary rational abc, and the published BB prepared-pole realization from the preceding constructions.

The target is a complete additional constraint implying
\[
 \tag{Cap}\log(1+h_{\rm W}(s))\le A qh^2+O(1)
\]
with a fixed \(A\). The intended complete witnesses have \(X=m\), \(U=[m]H\), for all nonzero integers \(m\). The previous
[standalone-cap note](standalone_charge_cap_20261124.md) excluded a finite algebraic projection to the charge and pointed rank-zero Weierstrass families. The present note removes the specified-origin requirement, treats genuinely coupled curves with \(U\) on the same fiber, and extends the linear-height obstruction to any genus with rank-zero Jacobian or with fixed geometric isomorphism type.

The conclusions are:

* A fixed smooth projective family of genus-zero or genus-one curves over the input/reference base cannot supply the cap and true-integer completeness, even when its rational functions include the numerator point \(U\) as well as the charge. This assertion concerns algebraic curve constraints on the points/charge, with the old BB input prepared on the known true witnesses, and with only the old BB realization needed on the varied witnesses. In particular, genus-one torsors without a specified rational origin do not escape the obstruction.
* For any fixed smooth projective curve family, on fibers of rank-zero rational Jacobian, the charge has a linear height bound over the base. No uniform torsion-order theorem is needed.
* Under ordinary rational abc, the same linear bound holds for all rational points on a fixed smooth projective family of genus at least two with constant geometric isomorphism type. This includes nontrivial families of twists with no globally specified rational isomorphism to a fixed curve.
* A nonisotrivial higher-genus family is not excluded. In particular, no assertion is made that its rational-point heights have a uniform exponential bound under ordinary rational abc, nor that it has suitable complete witnesses.

These are obstructions to classes of additional constraints. They are not a lower bound on all defining polynomials or a proof of nonexistence of the nine-coordinate goal.

## 1. The charge lower bound and base height

From (C), each foreign simple denominator prime of \(U\) outside the fixed bad set divides the reduced numerator of \(s\). Indeed at such a prime \(v_p(g_U)=-1\), \(v_p(g_H)\ge0\), so a negative valuation of \((g_U/g_H^2)s^2\) would be negative odd and cannot occur in the square on the right of (C).

The doubled-point mass theorem of the
[duplication continuation](../../../papers/elliptic_divisibility/duplication_mass_and_bounded_quotients_20261124/README.md) therefore gives, uniformly in the witnesses,
\[
 \tag{1}
 h_{\rm W}(s)\ge qj^2-qh^2-o(j^2)-O(1).
\]
The little-oh is for the fixed elliptic denominator sequence, as \(|j|\to\infty\). In particular
\[
 h_{\rm W}(s)\ge \tfrac12 qj^2-qh^2-O(1)
\]
for all nonzero labels after adjusting the constant.

For the input/reference base \(B\) use an open of \(\mathbb A^1\times E\), or the corresponding product with the fixed square-abscissa chart \(g_H,\eta_H\) (\(\eta_H^2=g_H^4-2\)). Any fixed affine or projective embedding on a specified open gives the base height bound
\[
 \tag{2}
 H_B(b)\ll 1+h_{\rm W}(X)+qh^2 .
\]
Here \(H_B\) denotes a **logarithmic** height, not an exponential height. For instance \(h_{\rm W}(x(H))=2qh^2+O(1)\) and \(h_{\rm W}(y(H))\le3qh^2+O(1)\); the finite square-root chart has the same bound. Include coefficients and finitely many fixed guard functions in this height estimate by the ordinary upper height inequality for fixed rational functions.

A uniform linear bound \(h_{\rm W}(s)\ll H_B(b)+1\) is incompatible with true witnesses for unbounded integer \(m\). In fact \(j=mh\) and (1),(2) would give
\[
 (\tfrac12 m^2-1-C)qh^2\le C(1+\log(1+|m|))+O(1).
\]
Since \(q>0\) and \(|h|\ge1\), this bounds \(|m|\) independently of the witnesses. No limiting choice of very large \(h\) is needed for this contradiction.

### Removal of algebraic exceptional loci

In the original quotient source, \(h_{\rm W}(X)\ll qh^2+1\). Thus a proper closed algebraic subset of the two-dimensional input/reference base cannot contain witnesses with unbounded **integer** \(X\). Here it is enough to work on the fixed reference chart, a curve with nonconstant map to \(E\).

Indeed, decompose a proper closed subset into finitely many curves and points. On an irreducible curve with \(X\) constant there is at most one input value. If the reference is constant, the input-height anchor bounds \(|X|\). Otherwise, on its smooth projective normalization the reference map to \(E\) is nonconstant, so the genus is at least one (Riemann--Hurwitz in characteristic zero), and \(X\) is a nonconstant rational function. Siegel's theorem on integral values of a nonconstant function on a positive-genus curve implies that there are only finitely many rational points on that curve with \(X\in\mathbb Z\). If the component is not geometrically irreducible over \(\mathbb Q\), apply the same assertion over a fixed field of definition of its geometric components, to the lifts of rational points away from their finite intersections and singular points. The normalization of a smooth rational point is rational over that fixed field. This gives the same finiteness. Zero-dimensional pieces cause no problem.

Equivalently, one can use the stronger arbitrarily-large-reference completeness in the original source: for every fixed sufficiently large \(m\), a proper closed subset of the base misses all but finitely many reference points, outside finitely many exceptional \(m\). The Siegel argument explains why even a one-reference-per-integer completeness reformulation cannot be confined to a fixed lower-dimensional algebraic base locus.

## 2. Uniform height lemma for torsion in a fixed abelian family

Let \(A\to B\) be an abelian scheme with a fixed relatively ample line bundle. After shrinking the integral base to a nonempty affine open, choose a symmetric relatively very ample bundle \(\mathcal L\), rigidified along the zero section. One can symmetrize an ample bundle by tensoring it with its pullback by \([-1]\), rigidify by a base pullback, and take a sufficiently high tensor power. Shrink again to trivialize the locally free direct image giving a projective embedding \(A\hookrightarrow\mathbb P^N_B\), with the embedding defined by \(\mathcal L\). Choose the power so that restrictions of ambient homogeneous forms of degree four generate the sections of \(\mathcal L^4\) on the generic fiber, and shrink so this holds throughout the open. Such a power exists by the usual eventual normal generation of sufficiently ample embeddings. Alternatively, the following comparison is the standard relative height-machine consequence of the cubical line-bundle identity.

The theorem of the cube for a symmetric rigidified bundle gives
\([2]^*\mathcal L\simeq\mathcal L^4\).
In this embedding, \([2]\) is therefore represented on \(A\) by homogeneous degree-four forms whose coefficients are fixed rational functions of the base, with no common zero on a fiber. The following uniform inequality holds for \(Q\in A_b(\overline{\mathbb Q})\) with \(b\) in the chosen open:
\[
 \tag{3}
 \left|h_{\mathbb P^N}([2]Q)-4h_{\mathbb P^N}(Q)\right|
       \le C(1+H_B(b)).
\]
For detail, the upper bound follows from evaluation of the degree-four forms. Over the generic base function field, no common projective zero on the embedded variety means that powers of each homogeneous coordinate belong to the homogeneous ideal generated by the multiplication forms and the defining ideal of \(A\). Choose such finitely many homogeneous identities over that function field and shrink the base so all coefficient denominators are nonzero. On actual points of \(A_b\) the defining ideal terms vanish. At each place, evaluating the remaining identities at a coordinate of maximal absolute value gives the lower estimate, with the logarithmic error bounded by the local coefficient sizes and the fixed degrees. Summing gives \(4h_{\mathbb P^N}(Q)-h_{\mathbb P^N}([2]Q)\le C(1+H_B(b))\). All coefficient heights are bounded by the base height; there is no fiber-dependent exponent or constant. The construction uses only finitely many fixed data. It may be applied after any further nonempty base restriction required in the statements below.

If \(Q\) is torsion, the sequence \([2]^nQ\) has a finite orbit for this fixed \(Q\). Iterating the lower estimate in (3) and dividing by \(4^n\) gives, on letting \(n\to\infty\),
\[
 \tag{4} h_{\mathbb P^N}(Q)\le (C/3)(1+H_B(b)).
\]
The finiteness of the orbit is enough; **no bound on its order** is used, and the constant is uniform in all torsion points and all base points on the open. This works in any fixed abelian dimension.

We will also use the elementary relative finite-map height lemma: for a projective family \(C\to B\) and a morphism \(f:C\to A\) finite onto its image (in particular, fiberwise nonconstant from integral projective curves), the fiberwise pullback of a relatively ample bundle is relatively ample. Comparing with any fixed projective embedding of \(C\), after choosing powers, gives
\[
 \tag{5}
 h_{\mathbb P^M}(Q_C)\ll h_{\mathbb P^N}(f(Q_C))+H_B(b)+1.
\]
For example, choose a power of the pullback ample bundle that is very ample and whose difference with the chosen embedding bundle is relatively generated by sections, after restriction to an affine open. The upper-height inequalities for those fixed sections give (5). Equivalently use homogeneous finite-map coefficient identities on the generic fiber and spread out as for (3). For a regular rational coordinate \(s\) on a guarded affine chart, its height is at most a fixed multiple of \(h_{\mathbb P^M}(Q_C)+H_B(b)+1\). If its defining rational expression is not everywhere defined, use its regular locus and finitely many charts on that locus. These estimates involve logarithmic heights, not the magnitudes of affine real coordinates.

## 3. Rank-zero Jacobians, without a chosen rational origin

Let \(C\to B\) be any fixed smooth projective family of geometrically connected curves of genus \(g\ge1\), with \(s\) a rational coordinate regular on the guarded open of witnesses. Choose a fixed relatively ample line bundle \(\mathcal M\) on \(C\), of degree \(d>0\) on each fiber. This is supplied, for example, by any fixed relative projective embedding. There is a canonical morphism to the relative Jacobian \(J=\operatorname{Pic}^0(C/B)\):
\[
       a:C\longrightarrow J,\qquad
       Q_C\longmapsto \mathcal O(d[Q_C])\otimes\mathcal M_b^{-1}.
       \tag{6}
\]
The relative diagonal gives this morphism over \(B\), with no rational section of \(C\to B\) required. After extending scalars on any fiber and choosing any point as temporary origin, (6) is the usual Abel--Jacobi map followed by multiplication by \(d\) and a translation. It is nonconstant on each fiber for \(g\ge1\); hence it is finite onto its image (proper and quasi-finite). In genus one its degree is \(d^2\).

If \(J_b(\mathbb Q)\) has rank zero, every rational point \(Q_C\in C_b(\mathbb Q)\) maps to rational torsion in \(J_b\). Apply (4) to the fixed abelian family \(J/B\), then (5), then the rational-coordinate height inequality. We obtain the **uniform linear bound**
\[
                  h_{\rm W}(s)\ll 1+H_B(b).
                  \tag{7}
\]
It holds on all rank-zero fibers on the fixed chosen base open, even if the fibers with rank zero form a nonconstructible set, and even if there is no known bounded-height rational point on those fibers.

This proves the stronger torsor obstruction. In particular there is no escape via a very large least rational point on a genus-one torsor whose Jacobian has rank zero: (6) is a finite map to the Jacobian's torsion points, and controls the rational point heights without choosing that least point as origin. The same proof rules out every rank-zero Jacobian strategy for higher genus within the stated fixed-family setting. It is stronger than an argument using Mazur's torsion-order theorem and does not require a uniform torsion bound for higher-dimensional abelian varieties.

By Section 1, such fibers cannot provide true witnesses for unbounded integer inputs, outside the algebraic exceptional loci. This statement applies even when the numerator point \(U\) and the charge are rational functions on the **same** curve fiber. No independence of the cap equation from \(U\) is assumed.

## 4. Positive-rank genus-one coupled fibers and the original BB pole

We now address genuinely coupled algebraic curve constraints, not just standalone conditions in \((X,H,s)\).

Fix a base point \(b=(X,H)\) with a known actual witness from the original height-anchored quotient source, including a **prepared** actual BB scalar. Let \(C_b\) be a smooth projective geometrically connected curve with a rational point \(Q_0\) giving that witness and the charge. Its guarded open carries the physical numerator point \(U\), its chart data, the charge \(s,r\) satisfying (C), and any other algebraic data of the proposed curve constraint. Suppose \(s\) is nonconstant. All regularity/nonzero conditions are imposed on a fixed open containing \(Q_0\). The original pole witnesses are not included as additional equations restricting this open: they are supplied by the old BB theorem once its actual input is prepared.

For fixed \(X,H\), the old scalar has the important form
\[
       e(Q_C)=\frac{112}{841}\bigl(1+L\,C(Q_C)^2\bigr),
       \qquad L=y(H)+u(X)^{-M_0}\ne0.
       \tag{8}
\]
Here \(C(Q_C)\) denotes the old rational detector error on the fiber, not the curve itself. The other adaptive or joint versions have the same form with a different fixed square multiplier. The rational number \(L\) is now fixed. Outside a finite set consisting of the support of \(L\), the multiplier and the fixed preparation primes, every negative valuation of \(1+LC^2\) is even. This follows from the parity of \(2v_p(C)\), even when \(C\) has newly introduced denominator primes. At those exceptional finite places, and really, the prepared value at \(Q_0\) is preserved on sufficiently small local neighborhoods: nonzero values preserve their valuations, the dyadic squareclass is locally constant away from zero, and the real inequalities \(0<e<1\) are open. All fixed guarded rational functions can also be kept defined and nonzero.

If \(C_b\) has genus zero, the rational point \(Q_0\) identifies it with \(\mathbb P^1\). Rational weak approximation gives infinitely many rational points in these finitely many local neighborhoods. If \(C_b\) has genus one and its rational Jacobian has positive rank, use \(Q_0\) as the origin **only for this fixed fiber**. Take a nontorsion rational point in its elliptic group. After a fixed integer multiplication into the finitely many small formal neighborhoods, real recurrence gives arbitrarily large multiples simultaneously in all the required neighborhoods of the origin. Translating back gives infinitely many rational points near \(Q_0\). A nonconstant rational function on a projective integral curve has finite fibers, so in either case the resulting values of \(s\) form an infinite set of rationals and have unbounded height. The BB realization supplies the terminal old pole witnesses at every one of these points, since (8) is prepared at every prime and really.

This contradicts (Cap) for the fixed \(b\). If instead \(U\) varies nonconstantly on the fiber, its infinitely many rational values have unbounded labels by the retained cyclic chart; then (1) already implies unbounded \(s\). In particular one cannot obtain a cap by making \(s\) constant but letting \(U\) range through a positive-rank elliptic fiber and retaining (C).

The argument extends to a rationally parametrized or abelian-subvariety curve inside a higher-dimensional fiber through a prepared witness, when the charge is nonconstant on it and the same finite-place openness holds. It does **not** automatically extend to further coupled prepared pole inputs with odd-order moving poles on the fiber. If there are other such inputs, one must separately establish their preservation; for an extra rational-function pole with only even geometric pole orders, the finite-exception argument of the
[earlier no-cap theorem](../pole_parameters/quotient_cap_pole_obstruction_20261124.md) suffices.

Combining Sections 3 and 4 proves the genus-zero/one exclusion. A genus-one fiber with a rational witness is either positive rank (unbounded charge by recurrence) or rank zero (linear height budget). If the charge is algebraically constant on generic curve fibers, it falls under the finite-projection obstruction of the previous note. For a fixed smooth geometrically connected family with a nonconstant generic charge, restrict to the nonempty base open where the charge is nonconstant on each fiber. A finite menu of such families is handled by taking the union of the fixed exceptional loci and the maximum of the linear height constants. Section 1 justifies ignoring those loci even in a one-reference-per-input reformulation. We only need one prepared true witness on any positive-rank fiber to contradict the cap; no generic Mordell--Weil section is needed.

## 5. Fixed geometric type in genus at least two: a uniform linear bound from rational abc

Let \(C\to B\) now be a fixed smooth projective geometrically connected curve family of genus \(g\ge2\), geometrically isotrivial: its generic geometric fiber is isomorphic to a single curve \(C_0\). If it has any rational base fiber on the smooth locus, take \(C_0\) to be that fiber over \(\mathbb Q\); otherwise there are no rational base witnesses on the locus under consideration. After shrinking \(B\), there is a finite étale surjective cover \(B'\to B\) on which the family is isomorphic to \(C_0\times B'\). Indeed a generic geometric isomorphism is defined over a finite extension of \(\mathbb Q(B)\); normalize and restrict to the finite étale open, then spread out this isomorphism and its inverse. Neither the extension nor the isomorphism depends on a witness after this fixed cover is chosen.

We prove, assuming ordinary rational abc only, that
\[
                    h_{\rm W}(s)\ll 1+H_B(b)                 \tag{9}
\]
for every rational point of \(C_b\) in the guarded locus on this open.

### 5.1 An automorphism-invariant Belyi map

The geometric automorphism group \(G=\operatorname{Aut}(C_{0,\overline{\mathbb Q}})\) is finite because \(g\ge2\). Choose a nonconstant function \(f\in\mathbb Q(C_0)\). The coefficients of the monic polynomial
\[
                    \prod_{\alpha\in G}(Z-f\circ\alpha)
\]
are invariant both under \(G\) (which permutes the factors) and under the absolute Galois group (which permutes the automorphisms, as \(f\) is rational). At least one coefficient is nonconstant, since otherwise \(f\) would be algebraic over \(\overline{\mathbb Q}\) and hence constant. Let \(F:C_0\to\mathbb P^1\) be this nonconstant rational function.

Apply the marked form of Belyi's theorem over \(\mathbb Q\) to the finite Galois-invariant set of branch values of \(F\): there is a rational map \(\beta:\mathbb P^1\to\mathbb P^1\) ramified only over \(0,1,\infty\) and sending that set into \(0,1,\infty\). Thus
\[
       \pi=\beta\circ F:C_0\longrightarrow\mathbb P^1
\]
is a Belyi map of a fixed degree \(D\), defined over \(\mathbb Q\) and invariant under all of \(G\). If \(\iota:C_b\to C_0\) is any geometric isomorphism, its Galois conjugates differ from it by postcomposition with elements of \(G\). Therefore \(\pi\circ\iota\) is rational over \(\mathbb Q\). For every rational witness \(Q_C\in C_b(\mathbb Q)\), the value
\[
               t=\pi(\widetilde Q),\qquad
               \widetilde Q=\iota(Q_C)
\]
is rational. This is essential: we will apply rational abc to \(t\), **not** abc over the varying splitting field of the twist.

Let \(D_0\) be the reduced divisor \(\pi^{-1}\{0,1,\infty\}\).
By Riemann--Hurwitz
\[
                     \deg D_0=D-2g+2<D .
\]
Choose fixed rational \(\rho\) with \(\deg D_0/D<\rho<1\).
The rational divisor \(\rho\pi^*[\infty]-D_0\) has positive degree, hence is ample after clearing its denominator. Its absolute Weil height is bounded below on \(C_0(\overline{\mathbb Q})\). Consequently
\[
                 h_{D_0}(\widetilde Q)\le \rho h_{\rm W}(t)+O(1).
                 \tag{10}
\]
All these heights are for the **fixed** curve \(C_0\) and fixed map \(\pi\), so the constant is uniform even over algebraic points in varying number fields.

### 5.2 Uniform bad-prime accounting for the twist

Use an affine base open, and a point \(b'\in B'_b\) over \(b\).
Because the cover is finite étale on this fixed open, its affine generators satisfy fixed monic polynomial equations with coefficients regular in the base coordinates. Consequently their absolute heights, and the height of \(b'\), are \(O(1+H_B(b))\). This follows from the usual root-height bound for algebraic roots of monic polynomials, or directly from the local Cauchy bound at every place. The degree of the residue extension of \(b'\) is bounded by the degree of the cover.

Let \(L\) be the compositum of that residue field and a fixed number field over which all points of \(D_0\) are defined. The isomorphism on the base cover supplies \(\widetilde Q\in C_0(L)\).
After spreading the fixed cover \(B'\to B\) out over a localization of \(\mathbb Z\), for every rational base point \(b\) the field \(L\) is unramified outside a set \(S_b\) of primes satisfying
\[
                       \sum_{p\in S_b}\log p\ll 1+H_B(b).
                       \tag{11}
\]
Here we may include the fixed bad primes of \(C_0,\pi,D_0\), of the fixed splitting field of \(D_0\), and the ramified primes of the cover model. To see the varying contribution, present the affine base open by coordinates, equations and finitely many inverses. Outside the numerator/denominator support of these finitely many nonzero coordinate/guard values, and a fixed finite set, the point extends over \(\mathbb Z_p\) on that model. The pullback of a finite étale model to \(\mathbb Z_p\) is finite étale, so each residue field factor over \(\mathbb Q_p\) is unramified. Each removed support has logarithmic weight bounded by twice the height of the corresponding rational value; fixed-degree evaluation bounds those heights by \(O(1+H_B(b))\). This proves (11), without a discriminant bound depending on the charge or on \(\widetilde Q\).

Suppose \(t\notin\{0,1,\infty\}\).
For a prime \(p\notin S_b\) counted by the rational truncated count \(N^{(1)}(t;0,1,\infty)\), the rational \(t\) reduces to a marked value at every place of \(L\) above \(p\). At good places of the fixed map \(\pi\) the integral point \(\widetilde Q\) reduces to \(D_0\); its full local intersection multiplicity with the effective reduced divisor is at least one. Since \(p\) is unramified in \(L\), the normalized weights of all its places over \(p\) sum to \(\log p\).
Thus the sum of the rational prime contributions outside \(S_b\) is at most the normalized full local counting contribution to \(h_{D_0}(\widetilde Q)\).

Choose fixed local Weil functions of this effective divisor which agree with the integral-model intersections at all good places. The remaining finite and archimedean local functions are bounded below by fixed local constants on the fixed projective curve, with the usual normalization by the field degree; only finitely many constants are nonzero. This can be obtained directly by using a projective embedding and local equations for the effective divisor (or the model/metric definition of its height). Hence removing those places costs a bounded additive constant, uniformly over all algebraic points. We obtain
\[
        N^{(1)}(t;0,1,\infty)
             \le h_{D_0}(\widetilde Q)+O(1+H_B(b))
             \le \rho h_{\rm W}(t)+O(1+H_B(b)).            \tag{12}
\]
The unramified exclusion in (11) is needed: without it the normalized sum of truncated extension-place weights need not equal the original rational-prime weight.

### 5.3 Ordinary rational abc with a fixed exponent

Choose once and for all an abc exponent \(\kappa>1\) such that \(\kappa\rho<1\). This is possible since \(\rho<1\) and the fixed map degree does not vary with the base point. Applying ordinary rational abc to the rational number \(t\) gives
\[
       h_{\rm W}(t)\le\kappa N^{(1)}(t;0,1,\infty)+C_\kappa .
\]
Together with (12) this gives
\[
                    h_{\rm W}(t)\ll 1+H_B(b).
\]
If \(t\in\{0,1,\infty\}\), the point \(\widetilde Q\) is in the fixed finite set \(D_0\), and its absolute height on \(C_0\) is bounded instead. Since the fixed map \(\pi\) is finite, a fixed projective coordinate height of \(\widetilde Q\) is \(O(1+h_{\rm W}(t))\) in the nonmarked case as well (the ample-degree comparison of (5) suffices).

Finally the charge coordinate on the family, transported by the fixed isomorphism over \(B'\), is a fixed rational function of \((b',\widetilde Q)\) on its regular guarded locus. The usual upper height inequality and \(h(b')\ll1+H_B(b)\) give (9). This proof applies to a curve fiber that simultaneously parametrizes \(U\) and \(s\); no assumption that the cap equation is independent of \(U\) is used.

The argument excludes every fixed geometrically isotrivial hyperbolic curve family as a complete cap strategy, under the ordinary rational abc already used in (1). It uses no uniform abc constant for number fields of growing discriminants, and no conjecture on rational point heights on nonisotrivial families.

References for the marked Belyi theorem and its height application: N. Elkies, *ABC implies Mordell*, IMRN 1991, no. 7, 99--109; M. van Frankenhuijsen, *The ABC conjecture implies Vojta's height inequality for curves*, J. Number Theory 95 (2002), 289--302, [publisher](https://www.sciencedirect.com/science/article/pii/S0022314X01927696). The marked form is also used in the project's [earlier geometric no-cap theorem](../pole_parameters/quotient_cap_pole_obstruction_20261124.md). We have supplied the extra twist-uniform bad-prime and height bookkeeping above; the usual fixed-curve effective Mordell assertion alone would not justify it.

## 6. Status and the surviving curve directions

For a fixed smooth proper algebraic family of curve constraints over \((X,H)\), with its charge regular on an actual guarded open, the following alternatives are now separated:

* Genus zero, or genus one with positive rank and a prepared rational lift: the original pole can be prepared again by local approximation, and the charge is unbounded on that fixed fiber.
* Genus one with rank zero, or higher genus with rank-zero Jacobian: the torsion-height argument gives a linear budget incompatible with unbounded true integer multipliers.
* Higher genus with fixed geometric type: under ordinary rational abc the invariant Belyi map gives the same incompatible linear budget.
* Higher genus with genuinely varying geometric moduli and positive-rank Jacobian: none of these arguments excludes it. A rational-point height upper bound of the required scale, together with actual integer completeness, still needs proof.
* Higher-dimensional families and additional coupled pole predicates whose rational realizations are not open along the fixed fibers may evade the curve arguments. No general impossibility is claimed.

Even in the remaining curve case, the proposed cap must have uniform constants across the base. Ordinary rational abc plus a Belyi map chosen independently for each nonisotrivial fiber does not by itself give those constants; the degree may grow, forcing the choice of abc exponent toward one without uniform control of its constant. The [ico cap](../../../papers/elliptic_divisibility/ico_exponential_cap_20261125/README.md) instead uses an external effective Mordell bound that is uniform in the needed coefficient support. No new defining-variable or quartic record is claimed here.
