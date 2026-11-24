# Shared comparison contacts and a three-label Pell amplifier (v131)

The two complete tables have **848 variables / 737 quadratic residuals** and **876 variables / 763 quadratic residuals**, respectively. They use two or three *comparison* poles in total, plus twelve scalar poles. They replace the independent comparison contact families by one family shared by all source inputs, with private numerator pairs. The twelve certified source integers and the 52 Jones source residuals are unchanged. There is no additional ordinary-rational-abc assumption. The two-contact threshold remains ineffective; the three-contact threshold has an explicit integer recipe below. The specified member is a new coefficient choice, not the earlier fixed scalar anchor.

The arithmetic inputs are precisely the indicated existing ones: the rank-one elliptic group, relative formal logarithm of order four, scalar extraction and simultaneous scalar preparation of v74/v82/v104, the original reflected contact-height bounds (v74 or v68), the positive trace-height theorem or effective unweighted torsion-sum theorem, the compatible Gaussian prime supplier with half-generator annihilation and real recurrence, and BB-native pole existence. These are not independently discharged here. In particular the theorem is not a claim of unconditional rational undecidability.

## 1. Point charts and the common scalar

Put \(K=\mathbb Q(\rho)\), \(\rho^2=2\), \(D=(3-\rho)^2\), \(E:y^2=x^3-Dx\), \(R_0=(1+\rho,2\rho)\), \(P_0=2R_0\). The retained group is \(\mathbb ZR_0+E[2](K)\). Use \(\nu([m]R_0+T)=m/2\). Let \(f(Q)=1/x(Q)\) and \(S_Q=y(Q)/x(Q)\).

Use the finite-pair chart of [v65](../../papers/quartic_existence/quartic_abc68_20261117_v65.tex), Proposition 2.1 (the unscaled \(\beta=1\) chart):
\[
 d_*=(\eta+s+t)F=\eta G,\quad D(F+G)=(s-t)\eta-t^2,\quad
 1=d_*(s-t)-DFG .
\]
It parametrizes distinct finite points \(U=(1/F,s/F),V=(1/G,t/G)\) of nonzero abscissa, including tangents and finite torsion differences. Their difference \(A\) is finite with
\[
 x(A)=\eta(\eta+s+t),\qquad y(A)=-(\eta+t)x(A)-Dd_* .
\]
Both reciprocal abscissas are nonzero. Use one such chart for \(H,H-P_0\), enforcing the two components of \(A=P_0\) by the displayed formulas; \(x(P_0)=57/8-7\rho/2,\ y(P_0)=-165/8+417\rho/32\). Write \(S=S_H,T_H=S_{H-P_0}\).

Use twelve private pairs \((U_i,V_i)\), with difference labels \(m_i=2\nu(A_i)\in\mathbb Z\), and three further pairs with finite differences \(A_a,A_t,A_m\), labels \(a,t,m\in\mathbb Z\). Set \(b=2m+1\). The scalar point is precisely \(A_a\); reconstruct its abscissa and ordinate, guard its ordinate by a field inverse and set \(Z y(A_a)=2S x(A_a)\). This is \(Z=2z(A_a)/z(H)\) wherever both parameters are defined, with \(z=-x/y\). The scalar equations below themselves exclude \(Z=0\), and hence \(S=0\). The scalar point is non-torsion.

For each distinguished source input \(X_i\), put
\[
 \beta_i=51X_i^2+2504,\quad r_i=\beta_i(\beta_i-1)(\beta_i-2401)(32\beta_i+343),\quad
 R_i=\frac{149 C^2r_i}{1+149^2r_i},\quad C=149^N .
\]
These are positive, with \(R_i>100\) for \(N\ge1\). Preserve the v82 physical scalar input
\[
 J_i=Z^2/R_i^5+f(H)^2/R_i^4,\quad
 \tau_i\operatorname{Tr}(Z^2/R_i^5)=\operatorname{Nm}(J_i),\quad
 d_i^{\rm pole}=(7/9)R_i(R_i+9792)\tau_i^2 .
\]
The factor \(7/9\) is exactly the BB migration of [v104](../quadratic_reduction_v104/bb_native_combined.tex). In the table, store common \(Z^2,f(H)^2\), and the three rational quantities
\[
 A_*=N_{K/\mathbb Q}(Z^2),\quad B_*=\operatorname{Tr}(Z^2\overline{f(H)^2}),\quad C_*=N_{K/\mathbb Q}(f(H)^2).
\]
Then the actual scalar equation is recovered from
\[
 \widehat\tau_i\operatorname{Tr}(Z^2)=A_*+B_*R_i+C_*R_i^2,\qquad
 \tau_iR_i^5=\widehat\tau_i .
\]
This is just expansion of the norm of \(Z^2+R_i f(H)^2\), with no auxiliary algebraic roots. Both real embeddings of \(J_i\) are positive, since \(f(H)\ne0\), so the trace denominator cannot vanish on a solution. In particular the scalar nonzero and local extraction arguments of [v82, section 2](../../papers/quartic/scalar_point163_179_20261120_v82.tex) apply to these actual physical points; they do not require the old scaled inverse-Vieta coordinate system. With the source exceptional primes, the retained scalar estimate of [v74](../../papers/quartic/quartic193_20261117_v74.tex) gives, for every \(i\),
\[
 |a|\ge149^{L_N},\qquad h(\beta_i)\le C_s149^{-L_N}|a|(1+\log|a|/3),\qquad
 L_N=\lfloor9(2N-1)/4\rfloor+1,\quad C_s=2^{330770}.
\]
For the specified route the effective scalar inequality of [v68](../../papers/quartic/quartic229_compact_20261117_v68.tex), with the same normalizer \(C=149^N\), is stronger than this displayed inequality. Thus this use in the specified route is effective and does not require an additional ineffective scalar constant.

All poles here and below use the seven-coordinate quadratic compilation of the elementary native equations \(e^2+dp^2=1,\ uv=e(1-d),\ u^2-v^2=dq^2\). The scalar input and the comparison input are represented by stored rational coordinates; \(p^2,q^2\) have two stored square helpers. The pole obstruction and the BB sufficient preparation \(0<d<1,\ v_2(d)\ge4,\ d\in7\mathbb Q_2^{\times2}\), square reduced denominator, are proved and cited in v104.

## 2. One global reflected contact family

Let \(\Theta_0=\{0,-1/2,-1,1/2399,-32/407\}\), and use precisely the old general reflected set \(\Theta_0\cup(2-\Theta_0)\) for two contacts, or the old specified set \(\Theta_0\cup(3/11-\Theta_0)\) for three. Put \(G(x)=\prod_{\theta\in\Theta}(x-\theta)\). The difference points in the fifteen non-reference pairs give the common aggregate
\[
 U+\rho V=\sum_{j=1}^{15} x(A_j)+15(3-\rho)+20 .
\]
There is no weighting by a variable scalar. Thus both embeddings are at least 20, since every finite point has \(x\ge -(3-\rho)\) in the corresponding embedding. For a free rational \(\lambda\), use \(t_0=\lambda,t_1=\lambda+U\), and, in the three-contact version, \(t_2=\lambda+U+10+V^2\). These have disjoint translated contact positions on every actual tuple, as all gaps exceed the contact diameter. Set
\[
 q_j=\frac{(t_j+3)^8}{G(t_j)},\quad c=\sum_j q_j,\quad u c=1 .
\]
The literal guard \(t_j+3\ne0\) and contact equation force \(q_j,G(t_j)\ne0\); guard \(1+q_j\ne0\) separately. Outside a fixed computable enlargement of the old exceptional set by denominator and difference primes (including those involving \(-3\)), the positive odd contact radical of \(t_j\) is precisely the product of primes at which \(q_j\) has negative odd valuation. This follows by reducing the ten distinct linear factors, with \(t_j+3\) a unit at a contact; nonintegral \(t_j\) gives even valuation. Use \(M_j\) for that product. The original v74 bound is \(h(t_j)\le H_2 M_j^{7/6}\), with fixed ineffective \(H_2\) (increase it by a fixed factor for the enlarged exceptional set). The v68 specified coarse bound is \(h(t_j)\le2^{304}M_j(22+\tfrac12\log M_j)^2\) before enlargement. In particular both routes have \(h(t_j)\le H M_j^{7/6}\), with \(H\) ineffective only in the first. Indeed \(e^{-x/12}(22+x/2)\le28\) for \(x\ge0\); if \(R\) is the product of the finitely many added exceptional primes, one may take \(H=2^{304}28^2 R^2\) in the specified route. No full-family modular estimate for a different reflected set has been substituted.

## 3. Shared local tests

For each pair \(P=(s,t,F,G,\eta,d_*)\) define the field element \(r_P=F+c\bar G\); also use it for the reference pair. Form the following factors, multiplying all of them to one \(W\in K\):
* Reference: \(1+c r_H^2\).
* Input \(i\): \(C_i=2\beta_i s_i-2S,\ E_i=2\beta_i\bar t_i-2\bar T_H\), and \(1+c r_i^2+c^2 C_i^4+c^4 E_i^8\), where \(r_i=r_{P_i}\) in this bullet (not the rational scalar polynomial).
* The three growth-label pairs: introduce field ratios \(L_j s_j=2S\), let \(E_j=L_j\bar t_j-2\bar T_H\), and use \(1+c r_{P_j}^2+c^{10}E_j^4\). The ratios are defined wherever the equations have a solution, because \(S\ne0\).
* Growth residual: put
\[
 \delta=L_t^2-(L_a^2-1)(L_a-1)^2(2L_m+1)^2-1,
\]
and use \(1+c^7\delta^2\).

Use the single shared rational error \(D_g\operatorname{Tr}W=\operatorname{Nm}(W-1)\). This equation forces \(\operatorname{Tr}W\ne0\): otherwise \(W=1\) from the field norm, contradicting the zero trace. For each \(j\) put
\[
 g_j=1+D_g^2+(c-q_j)^2/q_j,\quad \tau_j(1+q_j)=g_j,\quad d_j^{\rm pole}=7q_j\tau_j^2 .
\]
This is the old shared gauge principle, now with only two or three comparison poles for the entire tuple. No input-dependent common squareclass of different pole arguments is asserted.

Fix a consumed prime of contact \(j\), \(v_p(q_j)=-\mu\) with \(\mu>0\) odd, outside the enlarged fixed exceptional set. Write valuations in the two unramified slots with repetitions at an inert prime. Exactly as in the global-gauge lemma, the pole obstruction gives \(v_p(g_j)>-\mu/2\) (also if \(g_j=0\)). The two nonconstant terms in \(g_j\) have even and odd valuations respectively. A negative minimum cannot cancel. Thus \(v_p(D_g)>-\mu/4\), \(v_p(c-q_j)>-3\mu/4\), and \(v_p(c)=-\mu\). In every displayed factor of \(W\), the nonconstant terms have distinct nonzero residue classes of valuations: odd for \(c r_P^2\), \(2\bmod4\) for \(c^2 C_i^4,c^{10}E_j^4\), \(4\bmod8\) for \(c^4 E_i^8\). The residual-only factor has one odd term. Therefore each factor has nonpositive valuation and, if a unit, residue one. Zero terms have valuation \(+\infty\). If both slots of \(W\) have negative valuation, \(v_p(D_g)\le\max_w v_w(W)\); if either is a unit the same conclusion \(\max_w v_w(W)>-\mu/4\) follows immediately. All factors at a common successful slot have valuation \(>-\mu/4\); every nonconstant term has valuation \(>-\mu/4\).

In particular \(v(r_P)>3\mu/8\) for all pairs. The valuations of \(F,c\bar G\) have opposite parity, since good-prime reciprocal abscissa valuations are even. Both \(F,\bar G\) thus have positive valuation, proving the formal-group conditions for the reference and every pair. At this slot \(v(C_i)>7\mu/16\), \(v(E_i)>15\mu/32\), so both are positive. Dividing the cleared comparisons by their formal slopes raises the congruence precision by at least one. The two exact logarithm ratios, multiplied by \(h=\nu(H)\) and \(h-1\), give the integer labels \(2\nu(U_i),2\nu(V_i)\) up to errors of valuation at least four, by the retained relative order-four formal estimate. Consequently
\[
 h(2\beta_i)\equiv2\nu(U_i),\quad (h-1)(2\beta_i)\equiv2\nu(V_i)\pmod {p^2},
 \qquad 2\beta_i\equiv m_i\pmod {p^2}.
\]
This establishes local integrality as well: subtract the congruences; they were obtained by multiplying before assuming integrality. The reference and points are finite, so the formal slopes are nonzero at the slots used.

The growth-pair alternate error satisfies \(v(E_j)>39\mu/16\ge39/16\), hence \(v(E_j)\ge3\). Its ratio agrees with the primary ratio modulo \(p^4\); the same subtraction gives \(L_a\equiv a,L_t\equiv t,L_m\equiv m\pmod {p^4}\). Since \(v(\delta)>27\mu/8\), its valuation is at least four. Evaluating its integral polynomial on these locally integral ratios gives
\[
 M_j^4\mid\Delta=t^2-(a^2-1)(a-1)^2 b^2-1
 \quad\text{and}\quad
 M_j^2\mid J_i=|\operatorname{num}(2\beta_i-m_i)|
\]
when the indicated residual is nonzero, for every contact \(j\) and input \(i\). The first inequality uses \(7\mu/2-\mu/8=27\mu/8\); the input and growth error inequalities follow by the same division of the valuation bounds. The argument does not require arbitrary rational solutions to have disjoint prime radicals or independently selected references.

## 4. Global soundness and the effective parameter

Let \(B=\max(1,|a|,|t|,|b|,|m_1|,\ldots,|m_{12}|)\); in particular \(B\ge149^{L_N}\). The old positive unweighted trace-height theorem gives \(B^2\le K(1+h(U))\) with fixed ineffective \(K\) for the two-contact route; the added integral constant contributes only fixed height. All finite torsion strata are covered by that theorem. In the three-contact route the [effective torsion-sum theorem v62](../../papers/effective_sums/effective_torsion_sums_20261117_v62.tex) gives an explicit \(B^2\le K(1+h(U)+h(V))\). For example put \(r=15,A_r=(r-1)2^{r-1}\); one may take \(K=72(2A_r^2+r2^{r-1}+8)\). In fact if \(M\) is the maximum of 1 and the absolute integer difference labels, \(B\le3M\), \(h(x(A))\ge M^2/4-3\) for the maximal nonzero label by the retained duplication bound, and the local sum theorem gives the lower bound for the aggregate up to \(A_r\log M+B_r+h(3-\rho)\). Its proof is unaffected by replacing the integral translation \(+1\) by \(+20\): it only improves the archimedean bound. Use \(A_r\log M\le M^2/8+2A_r^2\), \(B_r\le r2^{r-1}\), \(h(3-\rho)<2\), and \(h(U+\rho V)\le h(U)+h(V)+2\). The stated \(K\) follows. The trace version has fixed constants independent of \(N\) because the aggregate is unweighted.

For either route let \(L=\max_j h(t_j)\). Height inequalities for the successive differences give \(h(U)\le2L+1\) and, in the three-contact case, \(h(V)\le L+3\). In particular \(B^2\le K(1+5L+10)\). Enlarge \(H,K\) to integers at least one and put \(C_B=100K(H+1)\).

If \(\Delta\ne0\), then \(|\Delta|\le10B^6\). From the contact divisibility,
\[
 L\le H(10B^6)^{7/24}\le10H B^{7/4},
 \qquad B^{1/4}\le C_B .
\]
A sufficiently large fixed \(N\) makes this impossible. Thus \(\Delta=0\).

The new amplifier is elementary: since \(b\) is odd, \(Y=(a-1)b\ne0\), and
\[
 t^2-(a^2-1)Y^2=1 .
\]
Write \(n\ge1\) for its absolute Pell index at \(A=|a|>100\). The fundamental positive unit for \(A^2-1\) is \(A+\sqrt{A^2-1}\) (the smallest positive Pell ordinate is one), and all nontrivial solutions have \((|t|,|Y|)=(X_n(A),Y_n(A))\). The recurrence gives \(Y_n(A)\equiv n\bmod (A-1)\), and \(Y_n(A)\equiv(-1)^{n-1}n\bmod(A+1)\). Since \(a-1\mid Y\), this implies \(n\ge|a-1|\ge A-1\). Also \(X_n(A)\ge A^n\), for example by the positive Pell recurrence. Hence \(\log B\ge(A-1)\log A\). This replaces the old homogeneous Lucas residual and does not invoke its growth theorem.

If some \(J_i\ne0\), its numerator is at most \(3B e^{h(\beta_i)}\), so \(L\le H(3B e^{h(\beta_i)})^{7/12}\) and
\[
 B^2\le C_B B^{7/12}e^{7h(\beta_i)/12},\qquad
 \log B\le h(\beta_i)+\log C_B.
\]
Choose once and for all any integer \(N\ge1\) satisfying the explicit sufficient recipe
\[
 149^{L_N}>\max(100,C_B^4,4C_B,8C_s).
\]
This choice is ineffective only where \(H,K\) are ineffective; it is computable in the specified route using the stated integer constants and the finite exceptional set. Then the scalar inequality gives \(h(\beta_i)\le A\log A/4\) (use \(1+\log A/3\le2\log A\) for \(A>100\)). This contradicts the Pell lower bound. Every \(2\beta_i=m_i\in\mathbb Z\). Because \(2\beta_i=102 X_i^2+5008\) and 102 is squarefree, reduced denominator comparison proves every \(X_i\in\mathbb Z\). The unchanged outer Jones theorem now gives soundness.

## 5. Simultaneous completeness

Fix an integer source witness. The twelve \(R_i\) are fixed. The finite union of the scalar preparation sets, the common reference and the single scalar point are prepared exactly by [v104, simultaneous scalar preparation](../quadratic_reduction_v104/bb_native_combined.tex), including at seven. This supplies the actual \(d_i^{\rm pole}\) with square reduced denominator, class seven and valuation at least four at two, and real values in \((0,1)\). It first fixes a positive scalar index \(a\in6\mathbb Z\) and \(A_a=[a]R_0\), and then restricts the reference to a progression retaining all of those open conditions. No other scalar point is chosen per input.

Take \(n=a-1\), \(t=X_n(a)\), \(b=Y_n(a)/(a-1)\). Then \(b\) is an odd integer, by the Pell recurrence modulo \(a-1\) and modulo two; \(b>1\) since \(a\ge6\). Put \(m=(b-1)/2\). This gives \(\Delta=0\) with all three difference labels nonzero. Fix the other difference points as \([t]R_0,[m]R_0\) and the input points \([2\beta_i]R_0\). The aggregate and all shifts are now fixed, before the comparison primes and final reference are chosen.

Use the disjoint translated contact positions of section 2 with the old Gaussian prime supplier, avoiding all fixed scalar preparation primes and the nonzero difference labels and coordinate exclusions, as well as all fixed contact differences and denominator data. At each selected prime, its own \(q_j\) has valuation \(-1\) and the others are integral; \(c\) has valuation \(-1\). Refine the common reference progression for \(H=[h]P_0\) so that \(H\) is formal at the primary slot and \(H-P_0\) formal at the opposite slot, with equal positive formal depths. The old compatibility and synchronization argument (v78, integer completeness; v65, half-generator annihilation) applies to this single list: the divided annihilator orders annihilate \(R_0\); the selected primes are prime to the order moduli by the short-interval argument; only the smaller of the two depths is raised by the extra prime-power congruences. The reference remains in the scalar preparation progression. For every fixed nonzero integer difference label \(k\), choose the actual numerator pair \([hk]R_0,[(h-1)k]R_0\). These are distinct and have the desired difference. Real and fixed-place neighborhoods avoid the finitely many poles and zeros of their point and ratio functions, by the same finite-index recurrence used in v65 and v104.

At a selected prime with common depth \(d\ge1\), all intended reciprocal abscissas have depth at least \(2d\); the raw cleared errors for input and growth comparisons have depth at least \(3d\), by the order-four relative estimate, with the growth ratio error at least \(4d\) before multiplication by the opposite formal slope. Thus the \(r_P\) have depth at least \(2d-1\), \(\delta\) has depth at least \(4d\), and every nonconstant term of every factor at the successful slot has positive valuation. All factors at the other slot are either unit of residue one or have poles by the valuation tags. Hence \(W\equiv1\) in the successful slot and \(v_p(D_g)>0\) by the norm/trace equation (the two cases are a unit other slot or a negative-valuation other slot). For the selected contact \(v_p(g_j)=0,\ v_p(d_j^{\rm pole})=1\).

For nonselected primes outside the prepared finite set, the linear-prime factorization for \(G(t_j)\) shows its valuation is even, since each linear factor has a selected-prime numerator and the common slope denominator appears ten times. The additional numerator \((t_j+3)^8\) has even valuation. Consequently \(q_j\), and thus the actual comparison pole input, have even valuation there, irrespective of newly appearing denominators of any point or detector. At fixed prepared finite places and real infinity, the old arbitrarily large slope and denominator preparation gives \(q_j\sim\lambda^{-2},\ c\sim(\#\text{contacts})\lambda^{-2}\). Point and error functions are bounded there. Then \(W\to1,\ D_g\to0,\ g_j\to1,\ \tau_j\to1\). In particular \(d_j^{\rm pole}\sim7\lambda^{-2}\), giving positive even valuation of arbitrarily large depth and class seven at two, nonnegative valuation at all fixed finite places, and real values in \((0,1)\). All nonzero guards used here hold for sufficiently large prepared slopes. These preparations cover the full rational denominator, not just selected contact primes. BB existence supplies each actual scalar and comparison pole independently. Filling the chart and helper equations then gives a rational zero of the literal table. This proves completeness for every integer source witness.

## 6. Coefficient tables and scope

The deterministic builder pins the v128 outer-table Git blob and preserves all 52 source rows on their original 76-variable support, including the two borrowed source square registers. The replacement tuple circuit supplies the needed squares. All field equations are expanded in the basis \(1,\rho\) by exact rational coefficient arithmetic and each row is cleared of constant denominators. All new coefficients are integers except for the fixed coefficient parameter \(C\) (substituted as \(149^N\)); \(C\) and the instance parameters are not variables.

In the detector compilation \(u=1/c\); \(u^j L=X^2\) stores \(c^j X^2\) by a quadratic equation using stored \(u^j\), including \(j=1,5,7\). The powers \(c^2 C_i^4,c^4 E_i^8,c^{10} E_j^4\) are the stated squares of such scaled registers, so there are no omitted higher-degree rows. A quadratic field product is stored at each step of the global product. The contact denominator has the eighth power of \(t_j+3\); all ten linear factors are multiplied by the stored quadratic chain. The independent degree/support/count replay is necessary for the numerical result, whereas the arguments above establish the intended projection under the stated premises.

The two and three contact tables improve the respective 884 and 1049 bounds; the specified coefficient threshold is computed by the given recipe, rather than claiming the old specified anchor still suffices. The ordinary-abc frontier has a separate proof. No deletion of a certified source integer or claim of global minimality is made. Run `node build.mjs` from this directory for an exact replay (`--write` to regenerate).
