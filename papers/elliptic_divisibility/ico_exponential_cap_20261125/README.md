# A nonisotrivial genus-nine exponential cap from effective Mordell on ico curves

## Statement and status

We obtain an explicit **global upper-height constraint of the requested exponential scale**, using only one additional ordinary rational coordinate. It uses the effective Mordell theorem for nondegenerate ico models in Shijie Fan and Rafael von Känel, *Rational points and rational moduli spaces*, [arXiv:2501.17155v2](https://arxiv.org/html/2501.17155v2), Corollary 7.6 and the maps (8.3)--(8.4). We checked the applicability of the stated theorem and the explicit polynomial maps; its underlying modularity and effective-Shafarevich proof is retained as an additional external theorem, not independently audited in its entirety here.

We give two versions, on \(E:y^2=x^3-2x\) and \(P=(9/4,-21/8)\):

* An **eight-coordinate** extension of the seven-coordinate conic-charge source, with the proved bound
  \[
      \log(1+h_{\rm W}(s))\le240\widehat h(P)h^2+O(1).
  \]
* A **seven-coordinate** extension of the original six-coordinate quotient source, capping the existing square-abscissa coordinate of \(U\) directly and omitting the charge conic altogether. It gives the same quotient-size bound
  \[
      \log(1+|j/h|)\le120\widehat h(P)h^2+O(1).
  \]

Here \(H=[h]P,\ U=[j]P\), and \(h_{\rm W}\) is logarithmic Weil height. Under ordinary rational abc and the old cyclic-chart and BB premises, sufficiently high fixed comparison precision makes **every rational input in either enlarged relation an integer**. Actual complete witnesses for \(X=1,-1\) are proved, with arbitrarily large references. Zero can be added by a polynomial factor if desired.

**The missing step is completeness for all integer inputs.** Neither relation is recorded as a defining polynomial for \(\mathbb Z\). The new achievement is a fully specified, genuinely nonisotrivial higher-genus cap with a uniform bound of the right scale, not just fiberwise finiteness. The new upper bound has no dependence on a variable abc exponent or an unknown least rational point. Section 5 proves a substantial obstruction to low-genus multisection witnesses; the direct candidate in fact has only finitely many possible references for each sufficiently large fixed true multiplier.

## 1. The effective Mordell input and a two-coordinate chart

Let
\[
 \mathcal S=\{[Z_0:\cdots:Z_4]\in\mathbb P^4:
                           \sigma_2(Z)=\sigma_4(Z)=0\}.
\]
This is the icosahedral surface of Fan--von Känel. For a homogeneous integer polynomial \(f\) of positive degree, assume its five pure diagonal coefficients are all nonzero. Then \(\mathcal S\cap\{f=0\}\) is a nondegenerate ico model: it avoids all five coordinate points. Their Corollary 7.6 gives, for every rational point \(Z\) of this model,
\[
 \tag{1}
 h_{\mathbb P^4}(Z)\le c\,\nu_f^{24},\qquad
 \nu_f=\operatorname{rad}\!\left(\prod_{i=0}^4 a_i\right),
 \qquad c=10^{10^{12}},
\]
where \(a_i\) are its nonzero diagonal coefficients. This applies to the whole ico model, including all its components. In our application \(f\) is a nonzero hyperplane form and thus gives a curve. The degree and the non-diagonal coefficients do not enter \(\nu_f\); the requirement that \(f\) have **integer coefficients** is essential.

Use the explicit affine chart of their (8.3), with free plane coordinates \(w,t\):
\[
\begin{split}
 a_0&=(t-1)(wt+w-1),\\
 a_1&=w+t-w^2t-1,\\
 a_2&=w(1-t^2-w),\\
 a_3&=t-w+w^2-t^2,\\
 A&=\sum_{i=0}^3 a_i,\qquad T=\prod_{i=0}^3 a_i .
\end{split}
\]
To avoid notation collisions, these \(a_i\) are chart polynomials, not the coefficients of \(f\).
Set
\[
 Z_i=-A\prod_{l\ne i,\,0\le l\le3}a_l\quad(0\le i\le3),
                  \qquad Z_4=T .
\]
These polynomials are evaluated directly, not stored as ordinary coordinates.

Guard \(ATa_0(a_0+a_2)\ne0\). On this chart the \(Z_i\) form a nonzero projective vector on \(\mathcal S\). For completeness of the algebraic check, write \(e_k\) for elementary symmetric functions of \(a_0,\ldots,a_3\). The identity
\[
                    A e_2=e_3
\]
follows by expanding the displayed cubics. For normalized coordinates \(Z_i/T=-A/a_i,\ Z_4/T=1\), the equation \(\sigma_2=0\) is exactly this identity, while \(\sigma_4=0\) follows from \(A=\sum a_i\). These verify the surface equations independently of the external theorem.

Write \(R_i=\prod_{l\ne i,\,0\le l\le4}Z_l\).
The inverse map of (8.4) has coordinates
\[
 \rho_0=-(R_1+R_3)(R_0+R_1+R_2),\quad
 \rho_1=R_0(R_0+R_1+R_2+R_3),\quad
 \rho_2=R_0(R_0+R_2).
\]
On the guarded chart these are nonzero as a projective vector and
\((\rho_0:\rho_1:\rho_2)=(w:t:1)\).
In fact canceling the common factor in the three expressions reduces the two inverse identities to
\[
 -(a_1+a_3)(a_0+a_1+a_2)=w a_0(a_0+a_2),
 \qquad a_0 A=t a_0(a_0+a_2).
\]
The guard ensures \(\rho_2\ne0\). Hence the usual homogeneous-polynomial upper-height inequality gives
\[
 \tag{2}
 h_{\rm W}(w)\le h(w:t:1)\le8h_{\mathbb P^4}(Z)+\log6 .
\]
The degree eight and coefficient one-norm six follow directly from the inverse expressions.

It suffices to impose a single equation
\[
 \tag{3}
 Z_0+Z_1+Z_2+Z_3+\alpha Z_4=0,\qquad \alpha\ne0,
\]
with \(\alpha\) a fixed rational function of the input/reference base. For \(\alpha=b/a\) in lowest terms, \(a>0\), use the integer hyperplane form with coefficients \((a,a,a,a,b)\). Thus
\(\nu_f=\operatorname{rad}(ab)\). Combining (1),(2) gives
\[
 \tag{4}
 \log(1+h_{\rm W}(w))\le24\log\operatorname{rad}(ab)+O(1).
\]
In particular any fixed-degree choice of \(\alpha(X,H)\) gives an exponential height cap in \(h_{\rm W}(X)+qh^2\). Unlike the earlier five-contact upper-bound proposal, the arithmetic input here is the nondegenerate moduli curve, with its forbidden boundary of five projective coordinate points, not a scalar support bound on a fixed split polynomial in the charge.

## 2. A concrete varying coefficient and actual lifts

Put \(q=\widehat h(P)>0\), \(g=g_H\) with \(g^2=x(H)\). Thus
\[
                  h_{\rm W}(g)=qh^2+O(1).
\]
In the real rational chart \(|g|>1\), by \(y^2=x(x^2-2)\) and \(x=g^2>0\). Define the fixed rational function
\[
 \tag{5}
 \alpha_0(v)=
 \frac{-4(v^2+1)^4}
 {v(v-2)(v-1)(v+1)(v+3)(2v+1)(3v-1)}.
\]
The letter \(v\) in (5) is just an argument, not an old pole variable. At \(w=v,t=2\), the four chart polynomials become
\[
 3v-1,\quad -(v-1)(2v+1),\quad -v(v+3),\quad (v-2)(v+1),
\]
and \(A=-2(v^2+1)\). Consequently \(\alpha_0(v)=A\sum_i1/a_i\), which is precisely the coefficient making (3) vanish there. This is an exact identity, not an assumption about rational points on the new curve.

### Charge version

Append the original charge conic
\[
 r^2=1+(g_U/g_H^2)s^2,\qquad s\ne0
\]
to the six-coordinate source. In (3) choose
\[
        w=s,\qquad v_0=2g/(g-1),\qquad \alpha=\alpha_0(v_0).
\]
Retain only the extra ordinary plane coordinate \(t\). The coefficients depend on \(g\) alone. On true multiplication witnesses \(X=1\) or \(X=-1\), choose coherent signs \(g_U=g_H=g>1\), possible since the finite ordinate characters change sign with the chosen square roots. Then the conic parameter \(1\) gives
\[
     s=v_0=2g/(g-1),\qquad r=(g+1)/(g-1).
\]
Take \(t=2\). Since \(v_0>2\), every chart guard holds and (3) is satisfied. Thus every such old prepared witness for \(X=\pm1\) extends to the new cap. In particular there are arbitrarily large reference indices, as in the parent theorem.

A simplification of the coefficient gives
\[
 \tag{6}
 \alpha_0(2g/(g-1))
 =-\frac{(5g^2-2g+1)^4}
 {g(g-1)(g+1)(3g-1)(5g-3)(5g-1)(5g+1)}.
\]
For \(g=a/b\) reduced, \(b>0\), its homogeneous numerator and denominator before cancellation are
\[
 -(5a^2-2ab+b^2)^4,\qquad
 b\,a(a-b)(a+b)(3a-b)(5a-3b)(5a-b)(5a+b).
\]
Every prime of the reduced numerator or denominator divides the product of the quadratic \(5a^2-2ab+b^2\) and the eight displayed linear factors. Repeated prime powers of the numerator do not enlarge the radical. Hence
\[
 \log\nu_f\le10 h_{\rm W}(g)+O(1).
\]
Equation (4) proves exactly
\[
 \tag{7}
              \log(1+h_{\rm W}(s))\le240 qh^2+O(1).
\]
All constants are uniform in \(X,h,j,s,t\). This establishes the requested height inequality on every solution of the **additional proposed constraint**. It is the completeness of that constraint at general integer \(X\), not this bound, that remains open.

### Direct version, without a charge

The charge is no longer essential once a global height constraint is available. Instead apply (3) with
\[
                     w=g_U,\qquad\alpha=\alpha_0(g_H).
\]
The same radical argument applies, now homogenizing (5): for \(g=a/b\), the numerator is \(-4(a^2+b^2)^4\) and the denominator is a product of eight linear factors including \(b\). Thus again \(\log\nu_f\le10 h_{\rm W}(g_H)+O(1)\) and
\[
              \log(1+h_{\rm W}(g_U))\le240 qh^2+O(1).
\]
For \(X=\pm1\), choose \(g_U=g_H>0\) and \(t=2\); remove the finite set of reference fibers where (5) or the chart guard is undefined. This preserves arbitrarily-large-reference completeness. All calculations remain valid for arbitrary rational solutions satisfying the actual guards, not only for the positive-root witnesses.

Since \(h_{\rm W}(g_U)=qj^2+O(1)\), the direct version gives the quotient cap without any ordinary-abc denominator mass on \(U\) and without the conic. It uses one fewer ordinary coordinate than the charge version.

## 3. Fixed precision and soundness

In the charge version the lower bound of the one-conic theorem is
\[
 h_{\rm W}(s)\ge qj^2-qh^2-o(j^2)-O(1).
\]
Thus (7), or the direct bound on \(h_{\rm W}(g_U)\), gives
\[
 \tag{8} \log(1+|j/h|)\le120 qh^2+O(1).
\]
The six-coordinate parent source, using ordinary rational abc and the duplication mass continuation, gives \(h\mid j\), and for \(X\ne j/h\) gives
\[
 \log(1+|j/h|)\ge
 \left((N+3)(1-10/299)-1/1196-o(1)\right)qh^2-O(1).
\]
Fix \(N=130\), or any higher fixed precision. Then
\[
                  133(289/299)-1/1196
                  =153747/1196>120 .
\]
The little-oh is uniform in the input because it is the fixed denominator-sequence error. Increase the same fixed finite reference exclusion to make the strict coefficient gap dominate every fixed additive constant in the two inequalities. This excludes \(X\ne j/h\) on every solution of either cap relation. Therefore the input projection is contained in \(\mathbb Z\).

The additional prime-pattern or point-realization issue has not been used in soundness. In completeness the preceding section proved actual witnesses only for \(\pm1\); no claim is made that the ico curve contains the necessary point for an arbitrary other true multiplier.

The ordinary coordinate counts are:
* original quotient: six;
* with conic charge and the new plane coordinate: eight;
* with only the new plane coordinate and direct \(g_U\) cap: seven.

All \(\tau\)-chart and coefficient expressions are fixed rational functions. Clear their denominators in (3), guard all displayed factors, and adjoin the one extra conic root only in the charge version. The old finite-algebra encoder handles all point and pole characters and these guards in the same single coordinate. The finite algebra has rank eight for the direct version and at most sixteen for the charge version, as in the parent source plus the conic quadratic root. Thus the constructions give finite coefficient recipes for single integer polynomials, without expanding their determinants or claiming numerical degree bounds. The additional external theorem used in the new soundness is precisely (1). The sufficient reference cutoff remains ineffective.

## 4. The new family really has varying geometric moduli

We verify that (3) is not merely a twist of a fixed curve, nor a genus-one fiber hidden in a singular plane model. Consider the pencil on \(\mathcal S\) with parameter \(\alpha\) and restrict to \(Z_4=1\).
Write \(e_i\) for the elementary symmetric functions of \(Z_0,\ldots,Z_3\). The hyperplane and surface equations are
\[
                      e_1=-\alpha,\qquad e_2=\alpha,\qquad e_4=-e_3.
\]
Consequently the four coordinates are the ordered roots of
\[
        F_{\alpha,u}(z)=z^4+\alpha z^3+\alpha z^2-u(z+1),
                    \quad u=e_3.
\]
The rational function defining a single root is
\[
                  u=z^2(z^2+\alpha z+\alpha)/(z+1),
\]
of degree four (the numerator at \(z=-1\) is one).
Its pole at infinity has order three and its pole at \(-1\) is simple. Its discriminant polynomial in \(u\) is
\[
 \operatorname{disc}_z F=-u\,C_\alpha(u),
\]
where
\[
 \begin{split}
 C_\alpha(u)={}&27u^3+(-4\alpha^3+12\alpha^2-48\alpha+256)u^2\\
      &+(8\alpha^4-60\alpha^3+128\alpha^2)u
                     -4\alpha^5+16\alpha^4 .
 \end{split}
\]
The further discriminant identity is
\[
 \operatorname{disc}_u C_\alpha
       =-16\alpha^5(\alpha+4)^2(8\alpha^2-61\alpha+128)^3 .
\]
For generic \(\alpha\), \(C_\alpha(0)\ne0\) and the cubic discriminant is nonzero. Therefore there are four distinct finite simple branch values, with transposition monodromy, and one branch at infinity with 3-cycle monodromy. The degree-four covering has transitive monodromy; a transitive subgroup of \(S_4\) containing a transposition and a 3-cycle is \(S_4\). Indeed its order is divisible by 4 and 3, so the only proper possibility is an index-two subgroup \(A_4\), which has no transpositions.

The normalization of the ordered-root curve is therefore geometrically connected and its degree-24 Galois map to the \(u\)-line has genus nine, by
\[
       2g-2=24\left(-2+4(1-1/2)+(1-1/3)\right)=16.
\]
This gives the genus of the generic pencil fiber (the omitted chart points do not create further one-dimensional components: at \(Z_4=0\), the equations \(e_1=e_2=e_4=0\) give finitely many projective points). The guarded \(\tau,\rho\) chart is a birational chart on these curves by the inverse identities and the birational equivalence in the cited source.

To check varying moduli, consider the unordered four finite branch values \(u_1,\ldots,u_4\), one of which is zero. The affine invariant
\[
 I(\alpha)=\frac{\sum_i(u_i-\bar u)^4}
                     {(\sum_i(u_i-\bar u)^2)^2},\qquad
 \bar u=\tfrac14\sum_i u_i
\]
is a rational function of \(\alpha\) where the denominator is nonzero. Newton sums of \(-\operatorname{disc}_zF/27\) give
\[
 I(1)=11939/20449,\qquad I(2)=43753/69312 .
\]
These are unequal. The branch at infinity is distinguished by inertia order three, whereas the finite branches have inertia order two. Thus an isomorphism of the quotient branch data preserves infinity and can only change the four finite branch values by an affine transformation and permutation.

If the geometric curve type were constant on a nonempty open, the fixed genus-nine curve would have only finitely many \(S_4\) actions, because its automorphism group is finite. There would then be only finitely many quotient branch configurations up to isomorphism of the quotient line, contradicting the nonconstant invariant \(I(\alpha)\). Therefore the pencil is nonisotrivial. Both \(\alpha_0(g_H)\) and (6) are nonconstant rational functions on the reference curve, so both pulled-back families are nonisotrivial as well.

The checks here establish the geometric type of the generic fibers. The soundness bound (1) does not require every specialized fiber to be smooth or irreducible; nonzero diagonal coefficients suffice.

## 5. Why generic rational-function completeness cannot work for this pencil

There is an unconditional function-field obstruction to the most direct attempt to complete the new cap. In this section only the geometric constraint is considered; no conjectural arithmetic height or prime-distribution input is needed.

Pull back the reference chart to the fixed elliptic curve with generator \(R_0=(2,2)\), using
\[
 Q=[h]R_0,\quad H=[2]Q,\quad g_H=\pm f(Q),\quad
 f(Q)=\frac{x(Q)^2+2}{2y(Q)}.
\]
For true multipliers \(m\), take \(g_U=\pm f([m]Q)\). There are just four sign choices. The pullbacks are fixed maps of elliptic curves; on a geometric integral curve of witnesses each sign is constant. For rational witnesses with actual group labels, the half-point \([h]R_0\) is rational by construction. In the following theorem the half-point is included in the algebraic family for convenience; this introduces no ordinary variable into the cap construction itself.

The generic genus-nine cap curve over \(\mathbb C(E_Q)\) is fixed for each choice of reference sign in either version: its coefficient is a rational function of \(f(Q)\) alone, not of \(m\). It is nonisotrivial by Section 4. We use the function-field height inequality of Sheng-Li Tan, *Height inequality of algebraic points on curves over functional fields*, J. reine angew. Math. 461 (1995), 123--135, [DOI](https://doi.org/10.1515/crll.1995.461.123), Theorem A (or the standard characteristic-zero Vojta function-field height inequality). In the needed form, for a fixed nonisotrivial smooth projective curve of genus at least two over the function field \(K=\mathbb C(E_Q)\), there are fixed constants \(C_1,C_2\) such that every algebraic point \(R\) satisfies
\[
       h_{K_C}(R)\le C_1 d(R)+C_2,\qquad
       d(R)=\frac{2g(B_R)-2}{[K(R):K]},
\]
where \(B_R\) is the smooth projective curve of the finite function field extension \(K(R)\). These constants apply to arbitrary degree; one must not substitute a bounded-degree number-field height estimate here.

As the canonical divisor on the generic curve is ample, its height bounds the degree height of the rational map \(w\) by a fixed multiple and additive constant. In particular, if an algebraic witness curve \(\Gamma\) over \(\mathbb C\), with smooth normalization of genus one, maps nonconstantly to \(E_Q\) and carries the guarded ico data, then
\[
 \tag{9}
 \frac{\deg(w:\Gamma\to\mathbb P^1)}{\deg(\Gamma\to E_Q)}
                      \le C_3
\]
for a constant independent of \(\Gamma\). The height here is normalized function-field degree; if \(w\) is constant its degree is zero. To see the discriminant is zero, the extension generated by its ico coordinates is an intermediate field between \(\mathbb C(E_Q)\) and \(\mathbb C(\Gamma)\). Its smooth base curve receives a finite map from a genus-one curve and maps finitely to a genus-one curve. Riemann--Hurwitz forces its genus to be one. The height of \(w\) in the intermediate extension is its degree divided by the extension degree, equally computed on \(\Gamma\). This proves (9). Only the fixed generic cap curve is used, so no uniformity over varying \(\alpha\) beyond the already fixed family over \(K\) is assumed.

For the direct cap, \(w=g_U=\pm f([m]Q)\) on a true multiplication family. The function \(f\) has degree four, with four simple poles at \(E[2]\), so the left side of (9) equals \(4m^2\). It exceeds \(C_3\) for large \(|m|\).

For the charge cap, \(L_m=g_U/g_H^2=\pm f([m]Q)/f(Q)^2\).
The function \(f\) has four simple poles at \(E[2]\) and four simple zeros above \((0,0)\) under [2], as in the one-conic paper. Outside these eight points, every point of \(E[2|m|]\) is a simple pole of \(L_m\). Thus there are at least \(4m^2-8\) distinct simple poles on the reference curve. A nonconstant map from a smooth genus-one curve \(\Gamma\) to \(E_Q\) is étale, by Riemann--Hurwitz. At every preimage of these simple poles, the rational-function conic
\[
                         r^2=1+L_m w^2
\]
forces \(w\) to vanish: otherwise the right-hand side has negative odd order. It follows that the left side of (9) is at least \(4m^2-8\), again impossible for all sufficiently large \(|m|\).

This proves more than the absence of a rational section. For either explicit cap, fix any sufficiently large \(|m|\). Consider any algebraic curve of true-multiplication witnesses over a number field, with nonconstant reference and the indicated half-point and guards. If it carries infinitely many rational points, its smooth projective normalization must have genus at most one by Faltings. Since it maps nonconstantly to an elliptic curve, its genus must be one. We just excluded such a curve. The finitely many singularities of an algebraic curve do not affect this argument. The same conclusion holds for curves defined over a fixed algebraic extension and rational points over that extension.

There is a useful **stronger conclusion for the direct cap**. For fixed \(m\), its plane coordinate \(w=\pm f([m]Q)\) is fixed over the reference function field. Since the generic ico curve has a nonconstant coordinate \(w\), the possible plane coordinates \(t\) above this value form a finite algebraic set. Thus the true-multiplication locus in \((Q,t)\) has only finitely many irreducible components dominating the reference curve, all of dimension one. Components over finitely many fixed reference values are irrelevant to unbounded reference indices. Every actual rational half-point in the true family is represented by one of the finite sign branches. Consequently the preceding Faltings/function-field argument proves that **for every sufficiently large fixed \(|m|\), only finitely many distinct reference indices are possible on the direct cap**, even allowing arbitrary rational lifts \(t\). This rules out arbitrarily-large-reference completeness for this particular seven-coordinate candidate, but not the existence of one reference for each integer.

For the charge cap, \(w=s\) is not fixed by \(H,U\); the conic gives a generically finite cover of a curve fiber of the ico family over the reference. The resulting true-multiplication locus for fixed \(m\) can be a surface. Infinite rational references there would require rational points not contained in any fixed finite union of algebraic curves: otherwise the same Faltings argument would apply componentwise. In fact a dominant surface component is generically finite over the nonisotrivial genus-nine fibration over the elliptic reference curve, which is of general type by the standard canonical-dimension theorem for nonisotrivial fibrations of curves of genus at least two over a positive-genus base. Hence weak Bombieri--Lang, **if additionally assumed**, would rule out arbitrarily-large-reference completeness of this particular charge pencil for sufficiently large \(m\). We do not assume that conjecture or infer non-density of the rational points from ordinary rational abc.

Thus no rational-function parametrization or elliptic multisection can furnish the old arbitrarily-large-reference witnesses for these particular explicit pencils at all sufficiently large multipliers. A one-reference-per-input construction remains possible. The conclusion also does not exclude different coefficient families varying in the external input \(X\) as well as in \(H\); a uniform function-field comparison over those varying families would require a separate argument.

## 6. The important off-diagonal-coefficient freedom and its limit

The cited effective Mordell theorem is uniform in the non-diagonal coefficients of an **integer** homogeneous polynomial. This is useful: in a more general degree-\(d\) ico constraint one may let integer off-diagonal coefficients be very large while keeping the diagonal prime support small. It is therefore not necessary in principle to control the logarithmic heights of all the curve coefficients.

However it is invalid to replace these arbitrary integer coefficients by unconstrained rational existential variables and retain the same bound. For example, at any rational point \(Z\) of the surface with \(Z_0Z_1\ne0\), the quadric
\[
      \sum_{i=0}^4 Z_i^2 + b Z_0Z_1=0,\qquad
      b=-\frac{\sum_{i=0}^4 Z_i^2}{Z_0Z_1},
\]
has diagonal coefficients one before clearing denominators. The rational surface chart gives infinitely many such points of unbounded height, so a uniform fixed-\(\nu_f\) bound for these rational coefficients would be false. The actual integer homogeneous equation multiplies every diagonal coefficient by the reduced denominator of \(b\); its prime support enters \(\nu_f\). This is precisely the step that would be lost in a proposed free-coefficient realization.

A promising refinement of the cap is to permit one more moving off-diagonal parameter whose **denominator support**, rather than its magnitude, is controlled by the input/reference base. The two extra coordinates permitted in the original target leave room for such a parameter together with the plane coordinate. If the denominator support is contained in the primes of a fixed nonzero rational function of \(X,H\), then its logarithmic radical is \(O(h_{\rm W}(X)+qh^2+1)\). After integer normalization of the ico model the bound (1) still gives the required exponential scale, independently of the numerator size of the moving coefficient. The original input-height anchor bounds \(h_{\rm W}(X)\) by \(O(qh^2+1)\). We have not yet found an existential constraint with this controlled-denominator property and complete true integer witnesses. It cannot be assumed from a rational coefficient or from its squareclass alone.

## 7. Reproduction and status

The exact checker verifies the two surface identities, the inverse chart, the coefficient formulas, the radical-degree counts, the discriminant and the varying branch invariant, the precise comparison margin, and rational conic/ico fixtures from the actual elliptic sequence. It does not verify the modularity theorem (1), compute the old BB witnesses, or establish rational points for general multipliers.

This is a sound global cap with an explicit nonisotrivial higher-genus construction and actual complete witnesses on a small input set. It is not a complete new Diophantine definition. The next task is an arithmetic realization of sufficiently flexible nondegenerate ico fibers, ideally using the independence of their height bound from the magnitudes of integer off-diagonal coefficients. The generic rational-section and genus-one multisection obstruction shows that a mere rational parametrization of the current pencil will not achieve this.

No current defining-variable or quartic record is changed.


The [bounded-reference continuation](../bounded_reference_20261125/README.md) proves that the original quotient has complete true witnesses for every nonzero integer with signed reference index bounded by a fixed polynomial in the input magnitude. In particular a one-reference-per-input strategy is compatible with the old source, despite the finiteness obstruction for this particular direct cap. This does not prove the extra ico equation is solvable at one of those references. The [exact checker](../../../scripts/verify_ico_cap_20261125.py) passed all symbolic identities, 32 rational elliptic chart fixtures and 1000 Taylor-exponent checks. The underlying effective Mordell theorem and the missing all-integer completeness are not computationally certified.


**Off-diagonal continuation.** The [optimal interpolation theorem](../ico_boundary_interpolation_20261125/README.md) shows that arbitrary integer homogeneous forms cannot improve the diagonal radical beyond the intrinsic coordinate-point reduction radical of the actual ico point. Two mixed coefficients in a degree-fifteen form already achieve this optimum. The required boundary avoidance is locally possible at every prime above eleven for any fixed nonzero numerator coordinate different from one, but is not globally established. The [multiplication-graph boundary obstruction](../../../negative_results/papers/elliptic_divisibility/ico_multiplication_boundary_20261125.md) combines weak boundedness of the Hilbert moduli space with the marked-Belyi abc argument to exclude a finite menu of rational-function lifts on the reference curve for sufficiently large fixed multipliers and arbitrarily large references, even if the menu and its degrees vary with the multiplier. General arithmetic lifts at individual references remain open. Neither continuation establishes all-integer completeness of the cap.
