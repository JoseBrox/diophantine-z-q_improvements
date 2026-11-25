# Exact off-diagonal interpolation on the ico surface

This is a continuation of the [exponential ico cap](../ico_exponential_cap_20261125/README.md). The new result identifies precisely what the independence of the effective Mordell bound from integer off-diagonal coefficients buys. It gives an exact two-coefficient interpolation, of fixed degree fifteen, with optimal diagonal prime support. It does **not** establish general completeness of the cap.

## 1. Pointwise minimal diagonal prime support

Let
\[
 \mathcal S=\{\sigma_2=\sigma_4=0\}\subset\mathbb P^4_{\mathbb Q}
\]
be the ico surface of Fan and von Känel, *Rational points and rational moduli spaces*, [arXiv:2501.17155v2](https://arxiv.org/html/2501.17155v2), equations (7.3), (7.5), Lemma 7.8 and Corollary 7.6. Here \(\sigma_i\) are the elementary symmetric polynomials in the five projective coordinates. The surface is integral, and its five coordinate points are precisely the degeneracy locus in their compactification. Write \(M\) for the complement of the five points.

For a point \(Z\in M(\mathbb Q)\), choose a primitive integral coordinate vector \(z=(z_0,\ldots,z_4)\), unique up to sign. Define its **boundary radical**
\[
 B(Z)=\prod_{\substack{p\text{ prime}\\
             \overline Z\text{ a coordinate point in }\mathbb P^4(\mathbb F_p)}}p.
\]
This is intrinsic: \(p\mid B(Z)\) means exactly one of the primitive coordinates is a \(p\)-adic unit. The set is finite because \(Z\) is not itself a coordinate point. We use the word boundary for this five-point reduction locus, not for an arbitrary choice of affine chart.

For any integer homogeneous form \(F\) with all five diagonal coefficients \(a_i\ne0\), if \(F(Z)=0\), then
\[
                       B(Z)\mid\operatorname{rad}\prod_{i=0}^4 a_i.
                       \tag{1}
\]
Indeed at a boundary prime with unique unit \(z_i\), every term but the \(i\)-th pure diagonal term is zero modulo \(p\). Thus \(p\mid a_i\). The degree of \(F\), the sizes of its coefficients and the number of its mixed monomials are irrelevant. The same necessary inclusion applies to a tuple of homogeneous forms when its nondegeneracy condition is that at least one diagonal coefficient at each coordinate point be nonzero.

**Proposition.** Conversely, for every \(Z\in M(\mathbb Q)\) there is an integer homogeneous form of degree fifteen of the shape
\[
 F=d\,\sigma_1^{15}+a\,\sigma_3^5+b\,\sigma_5^3,
 \qquad d>0,\quad a,b\in\mathbb Z,
 \tag{2}
\]
vanishing at \(Z\), with
\[
                    \operatorname{rad}(d)=B(Z).
                    \tag{3}
\]
The five diagonal coefficients are all \(d\). Thus the least possible diagonal radical, allowing arbitrary integer off-diagonal coefficients and arbitrary degree, is exactly \(B(Z)\). Degree fifteen and two freely chosen off-diagonal coefficients already attain this minimum.

**Proof.** Over any field, if \(\sigma_2(z)=\sigma_4(z)=0\), the characteristic polynomial with roots \(z_i\) is
\[
 \prod_{i=0}^4(T-z_i)
       =T^5-\sigma_1 T^4-\sigma_3 T^2-\sigma_5.
\]
If also \(\sigma_3=\sigma_5=0\), it equals \(T^4(T-\sigma_1)\). Since \(z\) is a nonzero vector, its multiset of coordinates consists of four zeros and the nonzero \(\sigma_1\). Conversely such a vector has \(\sigma_3=\sigma_5=0\). This argument works in every characteristic, including 2, 3 and 5.

Set \(A=\sigma_3(z)^5,\ C=\sigma_5(z)^3\), and \(D=\sigma_1(z)^{15}\). The integers \(A,C\) cannot both be zero because \(Z\in M\). The positive gcd \(G=\gcd(A,C)\) has prime support exactly \(B(Z)\), by the characteristic polynomial identity and the primitivity of \(z\). At every prime dividing \(G\), \(\sigma_1(z)\) is a unit. Hence \(\gcd(G,D)=1\), including the case \(D=0\), when necessarily \(G=1\).

By the extended Euclidean algorithm take integers \(a,b\) with \(aA+bC=-G D\). Then (2) holds with \(d=G\), and (3) follows. Furthermore, for the particular form (2) with any nonzero integer \(d\), the same equality implies \(G\mid d\); the common diagonal multiplier \(G\) is the least positive possible in this pencil. Since \(\sigma_3^5,\sigma_5^3\) have no pure diagonal monomials, (2) is nondegenerate. Its section of the integral surface is a curve, since the polynomial does not vanish identically (it is nonzero at each coordinate point). This verifies the hypotheses of Corollary 7.6, including the integer coefficient condition. QED.

### Height consequence without an initially specified curve

The cited effective Mordell theorem, applied to (2) with the actual computed integer coefficients, gives
\[
                 h_{\mathbb P^4}(Z)\le c B(Z)^{24},
                 \qquad c=10^{10^{12}}.                  \tag{4}
\]
This is an intrinsic form of their point height bound. No curve equation needs to be chosen before the point: the theorem is uniform in the mixed coefficients and degree, so the pointwise interpolation is legitimate. One could also use the integral moduli interpretation of \(M\) directly. The interpolation gives an elementary proof of the exact optimum for this use of Corollary 7.6.

In particular, for the guarded plane chart \(Z=Z(w,t)\) from the previous note, its inverse has degree eight, and
\[
                \log(1+h_{\rm W}(w))\le24\log B(Z)+O(1).
                \tag{5}
\]
The additive constant is absolute for this fixed chart. We do not claim an improvement to the exponent 24 of the cited theorem.

## 2. Two localized integer coefficients: an exact converse

For any finite rational-prime set \(S\), put \(R_S=\mathbb Z[S^{-1}]\). The following are equivalent for any \(Z\in M(\mathbb Q)\):

* its boundary radical is supported in \(S\);
* there exist \(a,b\in R_S\) with
\[
                  \sigma_1(Z)^{15}
                   +a\,\sigma_3(Z)^5+b\,\sigma_5(Z)^3=0.
                  \tag{6}
\]

All terms in (6) are homogeneous of degree fifteen, so any representative of the projective point can be used. If (6) holds, clearing a common denominator supported in \(S\) gives an integer form (2) with common diagonal \(d\) supported in \(S\); (1) gives necessity. Conversely, if \(B(Z)\) is supported in \(S\), the gcd \(G\) of the previous proof is a unit in \(R_S\), and that proof divided by \(G\) gives (6).

This is genuinely a two-coefficient interpolation, not a generic high-dimensional linear system. Neither coefficient needs any magnitude bound, and its denominator may have arbitrarily large powers of the permitted primes. In particular the old suggestion of choosing a variable integer form has a precise, degree-fixed reduction: it suffices to realize the plane chart with a controlled boundary radical.

### Application to the target count

Take \(w=g_U\), where \(g_U^2=x(U)\) is already one of the ordinary coordinates of the six-coordinate height-anchored quotient. Let \(t\) be the second plane coordinate. Let \(S\) be any prime set depending on the input/reference data with
\[
               \sum_{p\in S}\log p\le C_0 qh^2+O(1),
               \quad q=\widehat h(P),\ H=[h]P.
\]
For example this numerical budget holds for the support of finitely many fixed nonzero rational functions of the base \((X,H)\), using the original input-height anchor and canonical-height comparison.

If \(a,b\) in (6) are actually \(S\)-integers, (5) gives
\[
       \log(1+h_{\rm W}(g_U))\le24 C_0 qh^2+O(1),
       \qquad
       \log(1+|j/h|)\le12 C_0 qh^2+O(1).
\]
Here \(U=[j]P\), and the last implication uses \(h_{\rm W}(g_U)=qj^2+O(1)\). The six-coordinate discrepancy theorem then gives integrality of \(X\) at sufficiently high fixed comparison precision.

The number of ordinary coordinates in the **mixed-domain** system is nine: the old six, \(t\), and \(a,b\). This is *not* a nine-rational-coordinate polynomial definition: membership in \(R_S\) has not been enforced by rational polynomial equations, and actual true witnesses for all \(X=m\) with the required boundary budget have not been produced. If one uses the charge conic instead of \(g_U\), the corresponding mixed-domain count is ten. The direct cap is preferable.

There are therefore two logically distinct gaps:
(i) a boundary-avoiding plane lift for the true multipliers;
(ii) a low-coordinate existential certificate of the controlled coefficient denominator support (or an alternative algebraic constraint implying the same support). Even if either gap is solved, the other may remain. A bare equation (6) over unrestricted rationals has solutions on every nonboundary point, so it cannot impose any cap.

## 3. Exact local geometry of the existing plane chart

The explicit chart from (8.3) of the cited paper, in the notation of the previous note, has the factorization
\[
\begin{array}{ll}
 a_0=(t-1)(wt+w-1),&
 a_1=-(w-1)((w+1)t-1),\\
 a_2=-w(t^2+w-1),&
 a_3=-(t-w)(t+w-1),\\
 A=\sum a_i=-t(t+w^2-1).&
\end{array}
\]
The normalized projective coordinates are \((-A/a_0:\cdots:-A/a_3:1)\). All denominators are guarded.

For primes where \(w\) is integral and \(w(w-1)(w^2+w-1)\) is a unit, the five polynomials \(a_0,a_1,a_2,a_3,A\), considered as polynomials in \(t\), are pairwise coprime modulo \(p\). In fact the pairwise resultants are, up to signs, the following expressions (entries indexed in the order \(0,1,2,3,A\)):
\[
\begin{array}{c|cccc}
 &1&2&3&A\\\hline
0&w(w-1)^2Q&w^3(w-1)Q&w(w-1)^3Q&w^2(w-1)^2Q\\
1& &w^2(w-1)^2Q&w^2(w-1)^2Q&w(w-1)^2Q\\
2& & &w^3(w-1)Q&w^3(w-1)^2Q\\
3& & & &w^2(w-1)^2Q
\end{array}
\qquad Q=w^2+w-1 .
\]
In particular, if \(t\) is also integral at such a prime, its residue gives a boundary reduction if and only if one of these five polynomials vanishes. Indeed at most one vanishes. If a unique \(a_i\) vanishes, the \(i\)-th projective coordinate is a pole and the other normalized coordinates are integral. If only \(A\) vanishes, all four normalized coordinates vanish and the fifth is one. If none vanishes, all five normalized coordinates are units. This is an exact local criterion, with no assumption about splitting of \(p\) in a number field.

### New flexibility at simple foreign poles of \(w\)

Let \(v_p(w)=-1\). The previous choice \(t=2\) makes the reduction a boundary point at every such prime outside \(2,3\). In contrast take \(t=c/w\) where \(c\) is a \(p\)-adic unit and \(c-1\) is a unit. Then
\[
 v(a_0)=v(a_1)=v(A)=-1,\qquad v(a_2)=v(a_3)=-2.
\]
Indeed \(t\) has valuation one, and the leading terms of \(a_0,a_1,A\) are respectively \(-w,(1-c)w,-cw\), with nonzero unit factors. Thus the normalized coordinates \(Z_0,Z_1,Z_4\) are units, and \(Z_2,Z_3\) have positive valuation. The reduction is not a coordinate point. The same computation works for every pole depth \(v(w)=-a<0\), with valuations \(-a,-2a\) in place of \(-1,-2\). In particular \(t=2/w\) clears this entire class of boundary primes simultaneously outside 2.

This does **not** give a global solution. It transfers the dangerous primes to other contact factors. For example at \(t=2/w\), direct simplification gives
\[
 a_0=(2-w)(w+1)/w,\quad
 a_1=-(w-1)(w+2)/w,\quad
 a_2=-(w^3-w^2+4)/w,\quad
 a_3=(w^2-2)(w^2-w+2)/w^2,\quad
 A=-2(w^3-w+2)/w^2 .
\]
Consequently the ordinary-abc fixed-curve contact mechanism creates new boundary primes. Section 4 makes this obstruction precise even if arbitrary integer mixed coefficients and unbounded degrees are allowed. The local change nevertheless shows that direct rejection of all numerator-point denominator primes is not necessary for an ico cap: some of those primes can pass through a three-unit reduction.

### No local obstruction at any sufficiently large prime

In fact every \(w\in\mathbb Q\setminus\{0,1\}\) admits a nonboundary guarded lift over \(\mathbb Q_p\) at every \(p>11\). We give explicit choices in all valuation regimes. The guard \(a_0+a_2\ne0\) follows from \(A=t(a_0+a_2)\ne0\).

* If \(v_p(w)=-k<0\), take \(t=2/w\). The preceding computation gives valuations \((-k,-k,-2k,-2k,-k)\) for \((a_0,a_1,a_2,a_3,A)\).
* If \(v_p(w)=k>0\), take \(t=2w\). The valuations are \((0,0,k,k,k)\): the leading terms of \(a_2,a_3,A\) are \(w,w,2w\), respectively. Thus \(Z_2,Z_3,Z_4\) are units and the first two normalized coordinates have positive valuation.
* If \(v_p(w-1)=k>0\), take \(t=2w-1\). Writing \(w=1+\delta\), the leading terms of \(a_0,a_1,a_3\) are \(2\delta,-\delta,-\delta\), while \(a_2,A\) are units. The valuations are \((k,k,0,k,0)\). Hence the projective reduction has exactly the three nonzero coordinates \(0,1,3\).
* Otherwise \(w\) and \(w-1\) are units. The five polynomials \(a_0,a_1,a_2,a_3,A\) are nonzero modulo \(p\), of degrees at most \(2,1,2,2,2\), respectively, even when \(w^2+w-1=0\bmod p\). There are at most nine forbidden residues of \(t\). Since \(p>11\), choose any other residue. All five values are units.

These choices prove the existence of an open \(p\)-adic neighborhood of good lifts at every \(p>11\); the valuation patterns also prove all the local guards. Thus ordinary weak approximation gives rational plane lifts avoiding the boundary at any **prescribed finite set** of primes greater than 11, while retaining any compatible nonempty real guarded open condition. The exceptional small primes can be placed in the allowed support once and for all. This is not a solution of the global support problem. New boundary primes at unprescribed places are not controlled by weak approximation.

For example, at fixed \(w\) and a fixed finite allowed set \(S\), (4) and the inverse chart imply that there are only finitely many rational \(t\) whose boundary radical is supported in \(S\). Local flexibility at every prime therefore must not be interpreted as a global weak-approximation theorem for the desired \(S\)-integral lifts.

## 4. Fixed rational graph obstruction (also for one reference per input)

Fix any rational function \(t=T(w)\) over \(\mathbb Q\) such that the guarded plane chart is defined generically. The induced nonconstant map
\(\mathbb P^1\to\mathcal S\) extends across its finitely many rational-function poles as a morphism (the source is a smooth complete curve, the target projective). It must meet at least one of the coordinate points.

One way to justify this last assertion is Corollary 7.1(ii) of Fan--von Känel: the image of a nonconstant map from the projective line would be a nondegenerate curve if it missed the coordinate points; its normalization has genus zero by Riemann--Hurwitz, a contradiction. Equivalently, the fixed map avoiding those points would yield infinitely many points of bounded boundary radical by good reduction, contradicting (4) and finite fibers. The inverse chart ensures the map is nonconstant.

Pull the map back along \(w=f(Q)\) on the fixed elliptic curve
\[
 E:y^2=x^3-2x,\quad R_0=(2,2),\quad
 f(Q)=\frac{x(Q)^2+2}{2y(Q)}.
\]
It is still a nonconstant morphism, after extension over its removable projective base points, and still meets the boundary, since \(f:E\to\mathbb P^1\) is surjective. Fix one geometric boundary preimage \(D\) on this elliptic curve.

Assume ordinary rational abc. By the marked-Belyi contact lemma from the [quotient-cap pole obstruction](../../../negative_results/papers/pole_parameters/quotient_cap_pole_obstruction_20261124.md), the simple contact weight of \([j]R_0\) with this fixed \(D\) is
\[
                 \widehat h(R_0)j^2+o(j^2).
\]
The lemma uses the normalized finite-place weights of a fixed splitting field of the Belyi contacts; it applies to arbitrary geometric points, not just rational or torsion points. Away from a fixed finite set, these contacts give coordinate-point reductions of the image. Their normalized weight is at most the logarithmic weight of the rational boundary-prime product, since the image point is rational. Hence for the chart lift of \(g_U=\pm f([j]R_0)\) with fixed graph \(T\),
\[
                \log B(Z)\ge(q/4)j^2-o(j^2),
                \qquad q=\widehat h([2]R_0).
                \tag{7}
\]
The sign of the square root can be absorbed into the fixed map; a finite menu of fixed maps satisfies the same lower bound after taking a maximum of their fixed error thresholds. All constants in (7) are independent of the reference \(H\).

Now a budget \(\log B(Z)\le C_0 qh^2+O(1)\), combined with the true multiplication \(j=mh\), implies for sufficiently large \(|j|\) that \(m^2/8\le C_0+O(1)/(qh^2)\). Thus unbounded true integer multipliers are impossible, **even if only one reference per input is required**. The same conclusion follows for every integer polynomial form with bounded diagonal radical by (1), regardless of degree or off-diagonal freedom.

In particular both fixed choices \(t=2\) and \(t=2/w\) fail as general completeness constructions. This proof concerns a fixed rational graph (or a fixed finite menu), not a choice of \(t\) made by arbitrary arithmetic on each individual witness. For rational graphs on the reference curve allowed to vary with \(m\), the [companion moduli-boundary theorem](../../../negative_results/papers/elliptic_divisibility/ico_multiplication_boundary_20261125.md) gives a separate stronger obstruction to arbitrarily-large-reference completeness.

## 5. Status

The central positive result is the exact optimal interpolation (2)-(6). It removes all unnecessary restrictions on the degree and the magnitude of integer mixed coefficients. The mixed-domain nine-coordinate candidate is now explicit. But the arithmetic issue is intrinsic boundary avoidance, not linear algebra over the coefficients. A genuine completion requires a varying arithmetic lift, rather than a fixed rational graph of the existing numerator coordinate, and an existential way to enforce its boundary support. Neither is established here.

The [exact SymPy and rational-arithmetic checker](../../../scripts/verify_ico_interpolation_20261125.py) verifies the gcd identity on finite fields, the integer interpolation on exact rational chart fixtures, the resultant table and the pole-redirection formulas. It does not prove ordinary abc, the external effective Mordell theorem or the missing global realization.

The executed checker passed 277,082 projective finite-field points (1,135 on the ico surface), 2,890 local lifts, 1,090 rational chart interpolation fixtures, 32 elliptic interpolation fixtures, and all ten exact resultants and pole-redirection identities. The initial recursive Euclidean algorithm exceeded Python's recursion limit on a large exact fixture; it was replaced by the iterative Euclidean algorithm, and the complete check then passed. The elliptic fixtures do not include the original BB preparation or prove all-integer completeness.


**Coefficient-budget continuation.** The [eight-coordinate rational cap](../ico_coefficient_anchor_20261125/README.md) eliminates the second coefficient and replaces both localized-integer predicates by a shared quantitative height certificate. This is sufficient for soundness but is not literal prescribed-support membership, and the simultaneous coefficient-dependent reference preparation remains open. The same continuation reduces fixed-reference lift existence to a two-term S-unit equation plus exact boundary filtering. The [generalized-Szpiro obstruction](../../../negative_results/papers/elliptic_divisibility/ico_szpiro_obstruction_20261125.md) applies to arbitrary arithmetic lifts at individually chosen references, not merely rational graphs. Under that separate conjecture no fixed logarithmic boundary budget can be complete for unbounded true multipliers. Ordinary rational abc alone gives a necessary mass of decomposable good reductions, but not the full obstruction. The [exact checker](../../../scripts/verify_ico_coefficient_anchor_20261125.py) passed 2,240 interpolation and symmetry fixtures, 51,468 local contact fixtures, 125 adaptive-anchor fixtures and ten Thomae multidegrees.
