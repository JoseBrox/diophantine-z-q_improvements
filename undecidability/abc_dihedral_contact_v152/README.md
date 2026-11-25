# v152: dihedral contact pencils and normalized derivative moments

**287 rational coordinates, 236 quadratic residuals (ordinary rational abc).** This improves the 290/239 v148 system under exactly its retained arithmetic premises. All twelve certified source integers, all 52 Jones rows, the point charts, harmonic selector, interpolated mean, and one BB-native pole are retained. The effective/ineffective qualifications of v148 are unchanged.

## 1. A split rational pencil with arbitrarily many groups

Put
\[
 A(t)=t^6-45t^4+135t^2-27,\qquad
 B(t)=6t(t^2-1)(t^2-9).
\]
Then \(A(t)+\sqrt{-3}B(t)=(t+\sqrt{-3})^6\) and \(A^2+3B^2=(t^2+3)^6\).
The rational transformations
\[
 R(t)=(3t-3)/(t+3),\qquad S(t)=-t
\]
generate a dihedral group of order twelve on the projective line. Indeed \(R(t)+\sqrt{-3}=(3+\sqrt{-3})(t+\sqrt{-3})/(t+3)\), and \((3+\sqrt{-3})^6\) is a nonzero rational. Its projective order is six (the argument of \(3+\sqrt{-3}\) is \(\pi/6\)); \(SRS=R^{-1}\). The ratio \(A^2/B^2\) is invariant under both.

For rational seed \(t_i\) outside the finite set of poles, zeros of \(AB\), and fixed points of nonidentity group elements, the orbit has twelve distinct finite rational elements. Set
\[
 \kappa_i=A(t_i)^2/B(t_i)^2,\quad
 G_i(t)=A(t)^2-\kappa_iB(t)^2.
\]
The polynomial is monic of degree twelve and its roots are exactly that orbit. All are nonzero, paired by sign. Arbitrarily many pairwise disjoint finite rational orbits can be chosen: at each step exclude the finitely many earlier orbit elements and exceptional points. Thus this is a pencil of split degree-twelve contact polynomials with only two shared basis forms.

For the twelve inputs choose the seeds
\[
 2,4,6,8,10,11,12,13,14,16,17,18 .
\]
The independent verifier enumerates all 144 roots exactly; each has absolute value at most 18, and there are no repetitions. The common shift 784 is larger than every radius. The roots of the two-slot products below, viewed as affine polynomials in \(z\), are all distinct because the positive center exceeds the radii. This avoids relying on a genericity argument for this particular compiler.

## 2. The cheaper center and the retained height margin

Retain the v115/v126 height tree and write its positive root as \(M=B_{\rm abc}+2(L^4+R_0^4)\), with positive odd integer \(B_{\rm abc}\) and rational \(L,R_0\). Replace \(a=M^{12}+784\) by
\[
 a=M^4+784,\quad x_-=M^4-z,\quad x_+=M^4+z,\quad t_x=a-z,\quad t_y=a+z.
\]
The letter \(R_0\) in the height-tree formula is only a scalar leaf, not the elliptic generator. For rational \(L,R_0\), if both vanish then \(M\) is an odd integer. Otherwise the valuation of the nonzero sum of fourth powers is \(4m\) when the two valuations differ, or \(4m+1\) when equal to \(m\); this follows from the fourth-power residue 1 modulo 16 of every dyadic unit. The case where exactly one leaf is zero has valuation divisible by four. Therefore \(v_2(M)=0\) or \(v_2(M)\le-2\). In the first case \(a\equiv1\bmod8\); in the second \(M^4\) dominates \(784=28^2\) by at least twelve valuation units. In either case \(a\) is a nonzero square in \(\mathbb Q_2\). This is a new use of the exact root of the height tree, not an assertion that \(M^4+784\) is a dyadic square for arbitrary rational \(M\).

For each group set \(F_i=G_i(t_x)G_i(t_y)\), \(F_*=\prod_i F_i\). Use the derivative in \(a\) with \(z\) held fixed, and define **rescaled** derivative coefficients
\[
 r_i=-\frac{\partial_a F_i}{24F_i},\quad r_*=\sum_i r_i=12c,\qquad uc=1.
\]
Thus \(u=-288F_*/\partial_a F_*\) whenever the guarded expressions are defined.

Apply the v63/v126 radical argument with degree twelve in place of eight. For clarity, the shifted polynomials in \(x_-\) or \(x_+\) have roots \(-784+\theta\), where \(\theta\) ranges over the 144 signed radii. Their corresponding shifts \(784-\theta\) are positive distinct rationals. Clear their fixed denominators and exclude the primes dividing denominators, leading coefficients, differences, sums, and 288, as well as the inherited fixed bad primes. These exclusions are independent of the tuple and \(B_{\rm abc}\).

Choose \(x\) to be the larger-height of \(x_-,x_+\), and \(y\) the other. Ordinary abc applied to a fixed split degree-\(d\) binary form gives simple-prime weight at least \((d-4-2\epsilon)h(x)-O(1)\); the weight of its multiple-prime support is at most \((2+\epsilon)h(x)+O(1)\) (the standard radical and total multiplicity subtraction in v63). Start with the simple primes of group \(i\) at \(x\). Discard denominator primes of \(M\), at cost \(h(M)\), and multiple primes of the entire opposite product, at cost \((2+\epsilon)h(y)+O(1)\). At a remaining prime with roots on both slots, their two simple factors have sum \(2M^4+d+d'\), where \(d,d'\) are fixed positive shifts. Cancellation of the simple derivative term requires divisibility of that sum by \(p^2\). The power-multiple lemma of [v63](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex) bounds the multiple support of the product of these distinct positive shifts at \(2M^4\) by \((2+\epsilon)h(M)+O(1)\), independent of the number of shifts and of the fixed exponent in its leading coefficient. All its nonvanishing hypotheses follow from positivity. Hence at each surviving prime \(v_p(u)=1\). Every normalized weight
\[
 \omega_i=r_i/c=12r_i/r_*
\]
is integral, at most two groups are active, their weights are units, and their residues sum to 12. This follows directly from the logarithmic derivative: each simple factor contributes a pole of order one, and at a two-slot collision the excluded multiple-sum condition prevents cancellation. Inactive groups have no pole. If both factors belong to the same group its sole normalized active weight is 12.

For \(\epsilon=1/100\) the retained radical per group now has logarithmic weight at least
\[
 (12-6-3\epsilon)\max(h(x_-),h(x_+))-(3+\epsilon)h(M)-O(1)
 \ \ge\ (893/100)h(M)-O(1).
\]
The last step uses \(x_-+x_+=2M^4\). The v126 pairwise denominator bound is unchanged: deleting all twelve input denominator primes costs at most \(6C h(M)+O(1)\), where \(C=(1001/997)^4\). The existing cost for nonzero-label factors is \(\sum_j\log(1+|m_j|)\).

Consequently the v148 local implication, with the same normalized weights, gives \(X_i\equiv\pm m_i\bmod p\) at all the retained primes of group \(i\). If \(X_i\ne\pm m_i\), the signed numerator product gives
\[
 (893/100-8C)h(M)
 \le \sum_j\log(1+|m_j|)+2\log(1+|m_i|)+O(1).
\]
The coefficient is strictly positive by integer cross multiplication. The retained positive-weight trace-height estimate bounds each \(m_j^2\) by \(O(h(M)+1)\), so \(h(M)\) would be bounded independently of \(B_{\rm abc}\), contradicting \(M\ge B_{\rm abc}\) for sufficiently large fixed odd \(B_{\rm abc}\). Thus each input is integral, as required by the unchanged source.

This argument generalizes to any fixed number of groups with distinct generic orbits in the same rational pencil. One can take a square offset larger than all radii and of 2-adic valuation four, and an even center exponent sufficiently large that the corresponding paired-height and discrepancy costs are dominated by \((12-6-3\epsilon)m/2-(3+\epsilon)\). For exponent \(m\ge4\) even, the height-tree valuation calculation ensures the same dyadic square property. Only the sufficient fixed parameter and the fixed exceptional set change. The proof does not require a new modular height theorem for an arbitrary contact set; it uses ordinary abc.

## 3. Exact quadratic derivative circuit

For each \(t=t_x,t_y\) store seven values
\[
 s=t^2,\quad Q=(s-1)(s-9),\quad
 A=sQ-35s^2+126s-27,\quad R=B(t)/A,\quad q=R^2,\quad
 \alpha=A'/A,\quad \beta=R B'/A .
\]
The last three identities can be imposed with the quadrics
\[
 AR=6tQ,\quad A\alpha=6t(Q-20s+36),\quad
 A\beta=6R(5Q+20s-36).
\]
Here \(t=a\pm z\) is an affine linear expression, so every displayed equation is quadratic. The first of these three rows forces \(A\ne0\): otherwise \(B=0\), contradicting \(A^2+3B^2=(t^2+3)^6>0\). In fact \(A\) has no rational zero, since a zero gives \(R_i^2\) a rational multiple of 3 via the real part of \((t+\sqrt{-3})^6\), or directly by the rational-root theorem on \(t^6-45t^4+135t^2-27\) (the only possible integer roots are \(\pm1,\pm3,\pm9,\pm27\), and none is a root). This verifies completeness of the division at all rational arguments.

Store \(P=q_xq_y\). A direct logarithmic differentiation of \(G_i=A^2-\kappa_i B^2\) gives, after clearing the normalized denominator,
\[
\begin{split}
0={}&12r_i(1-\kappa_i(q_x+q_y)+\kappa_i^2 P)
 +\alpha_x+\alpha_y\\
 &-\kappa_i(\alpha_x q_y+\alpha_y q_x+\beta_x+\beta_y)
 +\kappa_i^2(\beta_xq_y+\beta_yq_x).
\end{split}
\]
This is one quadric per group, even for arbitrarily many groups. A zero of \(F_i\) would be a single simple root, since the actual two-slot positions are disjoint. Its derivative in \(a\) would be nonzero. The displayed row would then contradict that nonzero derivative (multiply by \(A_x^2 A_y^2\)). Thus the divisor \(F_i\) is genuinely nonzero in every rational solution. The new sum row \(r_*=12c\), together with \(uc=1\), ensures that the actual total logarithmic derivative is nonzero.

## 4. Rescale before coupling the moments

Retain the notation of v148, but now \(L_\mu=\sum_i r_i X_i\), \(F=\sum_i r_i D_i\), \(r_*=\sum_i r_i\), and \(r_*\mu=L_\mu\). As before
\[
 J=12F/r_*,\qquad {\rm var}=12(\sum_i r_iX_i^2-\mu L_\mu)/r_*.
\]
With \(T=(s+s^{-1})^2\) the existing unit-test register, impose directly
\[
 r_* W=12\left(\sum_i r_i X_i^2-\mu L_\mu+F^2+T^2\right).
\]
Since \(r_*=12c\), this is exactly \(W={\rm var}+cJ^2+uT^2\). The two former product/quotient helpers \(G,L_u\) are unnecessary. Keep \(W^2\), \(Z=D^2+cW^2\), the physical pole parameter \(\alpha_{\rm pole}=u+Z^2\), and the native pole unchanged. The entire sequential local soundness proof of v148 applies: in particular private-integrality is proved before the opposite unit test, not assumed from it.

## 5. Completeness, including foreign primes

For a canonical integer tuple all the point, height-tree and center data are fixed before prime selection, exactly as in v125/v126. The enlarged finite rational contact list has 288 distinct positions and the required signs. The retained supplier allows arbitrary finite lists with cleared fixed denominators, simultaneous primary/opposite order compatibility, prescribed finite-place slope neighborhoods and a sufficiently large real slope. No new version of the prime-pattern assertion is used. Select the primes and carry out the existing interpolation and recurrence; a selected prime has one simple active factor, so \(v(u)=1\), one weight 12 modulo the prime, and the same local tests succeed.

At a nonselected prime outside the finite preparation set, the split-factor prime factorization gives \(F_*\) a unit if \(z\) is integral. The derivative is integral, so \(v(u)\le0\). If \(z\) is nonintegral and \(a\) a unit (include its fixed supports in preparation), the leading terms give \(v(u)=2v(z)\), which is even, because every \(G_i\) is monic, its roots sum to zero, and the characteristic is outside the fixed excluded set. Explicitly at real or local slope infinity,
\[
 \frac{\partial_a F_i}{F_i}
 =\sum_{\theta:G_i(\theta)=0}\frac{2(a-\theta)}{(a-\theta)^2-z^2}
 \sim -24a/z^2,\quad r_i\sim a/z^2,\quad c\sim a/z^2.
\]
Thus \(\omega_i\to1\) and all the former fixed-place limits for the normalized moments and selectors remain valid. The physical pole is still asymptotic to \(7c\). At 2 the new \(a\) is a square and at all prescribed places the slope can be chosen sufficiently large in absolute value; this recovers precisely the old BB-native prepared input. At foreign negative odd valuations of \(u\), the parity argument for \(\alpha_{\rm pole}=u+Z^2\) ensures that the normalizing factor is a unit. At even valuations the square factor preserves parity outside 7. Hence the full old completeness proof, including treatment of foreign point denominators, applies.

## 6. Census and verification

The compiler removes fourteen old contact registers, two center powers and two coupled-moment helpers. It adds fifteen shared contact registers, reuses the twelve derivative coefficients and keeps every other coordinate. Thus \(290-18+15=287\); it removes 33 rows and adds 30, giving 236. It compares all 206 retained named rows exactly, including all 52 source rows, and verifies full coordinate support and degree at most two. The full table and independent exact checks accompany this proof. This is a transfer improvement, not a new unconditional theorem that Z is Diophantine in Q.
