# Recursive odd-support union: one scalar pole for the tuple (v136)

**663 / 683 rational unknowns; 574 / 592 quadratic residuals** (general / specified). The v134 counts were 750 / 771. There is one scalar pole rather than twelve, plus the existing two / three comparison poles. The 52 named Jones source rows, twelve certified inputs and short-power congruences are unchanged.

Arithmetic inputs: the rank-one elliptic group, the **full-rational-domain** five-contact scalar height input H4.1 of [v68](../../papers/quartic/quartic229_compact_20261117_v68.tex), the corresponding reflected comparison height estimates, the weighted aggregate estimate of [v133](../weighted_private_v133/README.md), the inherited simultaneous prime/CRT and recurrence inputs, and the BB prepared realization of [v104](../quadratic_reduction_v104/bb_native_combined.tex). The new scalar proof uses H4.1 itself, not a height estimate restricted to the old quadratic scalar argument. These imported arithmetic premises are not independently proved here. No ordinary-rational-abc hypothesis is added. The general parameter is ineffective; the specified parameter can be chosen effectively under the quantitative premises.

## 1. A recursive normalization that protects odd prime support

For \(n=12\) (the argument works for any fixed finite \(n\)), fix \(N\ge1\), \(C=149^N\). Put
\[
 c_0=2504,\quad r(Y)=Y(Y-1)(Y-2401)(32Y+343),\quad
 P_*=r(c_0)=51948354689656,\qquad \phi(w)=w/(1+w)^2.
\]
For arbitrary rational inputs \(X_i\) define successively
\[
 S_0=5\cdot2^{20}149^{2N+1},\quad
 W_i=S_{i-1}X_i^2,\quad Y_i=c_0+\phi(W_i),\quad
 S_i=S_{i-1}r(Y_i)/P_*,
\]
\[
 T_*=2^{n+20}149^{N+1},\qquad R=T_*^2\phi(S_n).
\]
These are everywhere defined on rational inputs: \(S_i>0,\ W_i\ge0,\ Y_i\in[c_0,c_0+1/4]\). All factors of \(r\) are positive increasing on that interval. Endpoint evaluation gives \(1\le r(Y_i)/P_*<2\), so \(S_0\le S_n\le2^nS_0\). Since \(S_n\ge1\), \(R\ge T_*^2/(4S_n)\ge 2^{n+18}149/5>100\). These facts also exclude every spurious cleared-denominator branch of the recursion.

Take the scalar exceptional set \(S\) of v68, namely \(\{2,3,5,7,11,13,17,37,41,2399\}\), enlarged by 149 and all primes dividing \(P_*\). Let \(M_i\) be the five-contact positive odd radical of \(Y_i\) outside \(S\). **Claim:** for every rational tuple, every prime dividing any \(M_i\) has positive odd valuation on \(R\), and \(v_{149}(R)=4N+3\).

Proof. For \(w=u/v\ge0\) reduced with \(v>0\), the fraction \(\phi(w)=uv/(u+v)^2\) is reduced (including zero); \(\gcd(uv,u+v)=1\). Thus each \(Y_i\) has square reduced denominator. Its contact at infinity has no odd contribution. At a prime outside \(S\) dividing \(M_i\), \(Y_i\) is integral, the four finite contacts are distinct modulo that prime, and \(v_p(r(Y_i))>0\) is odd.

If \(v_p(S_{i-1})\) is odd (of either sign), then for nonzero \(X_i\), \(v_p(W_i)=v_p(S_{i-1})+2v_p(X_i)\) is odd and nonzero. At any nonzero valuation, \(v_p(\phi(w))=|v_p(w)|\). Consequently \(Y_i\equiv c_0\bmod p\); this also holds when \(X_i=0\). For \(p\nmid P_*\) the update factor \(r(Y_i)/P_*\) is a unit. Hence an old odd valuation is preserved **exactly**, including negative odd valuations. At a new contact prime of \(M_i\) the old valuation must be even, since the odd case just proved would make the contact factor a unit. The update makes it odd, and every subsequent update preserves it. The final \(\phi\) sends nonzero odd valuations to positive odd ones; the square multiplier is a unit outside \(S\). At 149, \(P_*\equiv75\bmod149\), and the seed has valuation \(2N+1\). The same persistence proof applies at every stage on all rational inputs. The final multiplier adds \(2N+2\). QED.

The detector changes the scalar arguments; it does not preserve each of the old individual local tests. Therefore it does not contradict the [v135 local merger obstruction](../scalar_merger_obstruction_v135/README.md). It replaces their global height role instead. In particular we do not assume disjoint supports of the original scalar inputs, or take the unmodified product of their pole arguments.

## 2. One scalar valuation extraction and all input heights

Use the physical scalar point and reference \(A_a,H\) of v131, \(f=1/x(H)\), \(Z=2z(A_a)/z(H)\), and the v82/v134 normalized equations
\[
 J=R^{-5}(Z^2+Rf^2),\quad
 \tau\operatorname{Tr}(Z^2/R^5)=\operatorname{Nm}J,\quad
 b_s=R(R+9792)\tau^2,\quad d_s=(7/9)b_s .
\]
The one native pole is at \(d_s\). The reduced chart of section 5 below recovers the physical ratio without a circular nonvanishing argument. At each odd positive \(\mu=v_p(R)\) outside \(S\), the [v82 scalar lemma](../../papers/quartic/scalar_point163_179_20261120_v82.tex), its formal isometry and torsion translation give \(v_p(a)>9\mu/4\). The calculation only uses the physical \(R,Z,f\), not the old formula for \(R\). It also applies at 149, which is away from \(2,7,9792\). Write \(A=|a|\), \(L=9N+7\). Section 1 gives
\[
 149^L M_i^3\mid A,\qquad A\ge149^L.
\]
In fact one may use the cube of the radical of the union of the \(M_i\), since distinct primes are counted once. The exponent at 149 is \(\lfloor9(4N+3)/4\rfloor+1=L\).

H4.1 and the H4.2 estimate of v68 give \(h(Y)\le 2^{238}M^3\) for the original scalar exceptional set and the corresponding radical: the source constant is less than \(2^{237}\), \(E(M)\le1+\log M\), and \((1+\log M)^2<2M\). This estimate applies on the full rational domain away from the contact locations, as in H4.1. The product of the added primes is at most \(149P_*\). Hence with \(H_s=2^{238}(149P_*)^3\) we have
\[
 h(Y_i)\le H_s M_i^3\le H_s149^{-L}A .
\]
This is a rational height bound, not a bound on real values.

For \(W_i=u/v\ge0\) reduced as above, \(h(\phi(W_i))=2\log(u+v)\ge2h(W_i)\). Therefore
\[
 2h(X_i)\le h(W_i)+h(S_{i-1})
 \le \tfrac12h(Y_i)+\tfrac12\log2505+h(S_{i-1}).
\]
The polynomial height inequality (the coefficient one-norm of \(r\) is less than \(2^{21}\)) gives
\[
 h(S_{i-1})\le h(S_0)+4\sum_{j<i}h(Y_j)+100(i-1),
 \qquad h(S_0)<12N+30.
\]
Here 100 bounds \(\log\|r\|_1+\log P_*\). Keep the original weighted comparison target \(\beta_i=51X_i^2+2504\), so \(h(\beta_i)\le2h(X_i)+\log2555\). With \(A\ge149^L\), for twelve inputs we obtain the explicit uniform joint estimate
\[
 h(\beta_i)\le D_N149^{-L}A,\qquad D_N=49H_s+12N+1300.
\]
The coefficient \(D_N149^{-L}\) tends to zero. This replaces the twelve private scalar estimates, independently of how many original input denominators are nontrivial.

## 3. Global soundness

All weighted private comparison charts and factors of v133/v134, all reference and growth labels, and the comparison contact arguments are unchanged physically. Put \(k_i=2\beta_i,\ w_i=k_i^2,\ H_w=\sum_i h(w_i)\). Write \(B\ge A\) for the maximum of one and the absolute integer difference labels, including \(a,t,b=2m+1\). By v133, with a fixed \(K\ge1\),
\[
 B^2\le K(1+h(U)+H_w)
\]
in the general route, with \(h(V)\) added in the specified route. The explicit \(K\) of v133 works in the three-contact case; the two-contact \(K\) is ineffective. Because \(H_w\le24(D_N+1)149^{-L}A\), choosing \(149^L>48K(D_N+1)\) absorbs \(KH_w\) into \(B^2/2\).

Replace \(K\) by \(2K\) in the v131 global argument. Let \(H\) be the comparison height constant, \(C_B=200K(H+1)\) as in that argument. The v133 local proof gives \(M_j^4\mid\Delta\) for nonzero growth residual \(\Delta\), and \(M_j^2\mid J_i\) for nonzero \(J_i=|\operatorname{num}(2\beta_i-m_i)|\); here \(M_j\) denotes the comparison radical, not the scalar-chain radical. If \(\Delta\ne0\), \(h(t_j)\le HM_j^{7/6}\) first implies \(B^{1/4}\le C_B\). Choose \(149^L>C_B^4\). Then \(\Delta=0\) forces \(t^2-(a^2-1)(a-1)^2 b^2=1\) with odd \(b\). The v131 elementary Pell argument gives \(\log B\ge(A-1)\log A\).

For any \(J_i\ne0\), v131's height calculation gives \(\log B\le h(\beta_i)+\log C_B\). It contradicts the Pell growth by the new estimate, for example with any integer \(N\ge1\) satisfying
\[
 149^{9N+7}>\max(100,C_B^4,4C_B,48K(D_N+1),4D_N).
\]
Indeed \(h(\beta_i)<A/4\), \(\log C_B<\log A\), and \(A>100\). This is an effective search for the specified route; the general constants are ineffective. All \(J_i=0\), so \(102X_i^2+5008\in\mathbb Z\). Since 102 is squarefree, reduced denominators force \(X_i\in\mathbb Z\), including the zero input case. The unchanged source rows now give the old integer-source implication.

## 4. Completeness and the essential dyadic class

Fix an integer source witness, including all twelve inputs. All \(S_i\) and \(R>100\) are now fixed before the elliptic scalar and reference choices. The initial \(S_0\) has \(v_2(S_0)=20\) and odd unit congruent to 1 modulo 8, **because the additional factor 5 cancels the class \(149\equiv5\bmod8\)**. This factor is essential. For integral \(X_i\), \(Y_i-c_0\in 2^{20}\mathbb Z_2\) whenever \(v_2(S_{i-1})=20\). As \(v_2(P_*)=3\), the update factor \(r(Y_i)/P_*\) is congruent to one modulo \(2^{17}\). By induction the depth and squareclass persist. Thus \(R\) is a 2-adic square of depth 84 (for \(n=12\)). The number \(9792=2^6\cdot153\) is also a 2-adic square; \(R+9792\) has its squareclass by depth. Consequently \(R(R+9792)\) is a square at 2, and the physical \(d_s\) has squareclass seven at 2.

For any rational \(R=u/v\) in lowest terms, \(R(R+9792)=u(u+9792v)/v^2\) has square reduced denominator. Its odd support is finite and positive. At its odd-support primes and the fixed primes \(2,3,7,17\), use the v82/v104 preparation: choose the reference sufficiently deep in both local slots, choose the exact positive index-ratio depths \(t_p=v_p(a/h)\) large enough, then \(a\in6\mathbb Z_{>0}\) with the prescribed congruences and real recurrence. The expansion for the actual scalar \(\tau\) gives \(v_p(\tau)=2t_p-5v_p(R)-v_p(2)\); its hypotheses are satisfied by first taking the reference depth sufficiently large, as in v82. Make the required depths large enough that \(d_s\) has no odd negative denominator valuations, is integral at 7, and has \(v_2(d_s)\ge4\). At other primes the parity of its denominator valuation is already even. The original compact real boxes \(|f^{(j)}|\le1,\ 1\le |Z^{(j)}|\le3\) give \(0<b_s\le24482500/R^4<1\). Thus \(0<d_s<1\), and BB gives a native witness by v104. The preparation depends only on the fixed integer tuple and the subsequent common scalar choices, just as before.

After fixing \(a\), preserve the real and finite open conditions on the reference progression. The Pell labels \(t=X_{a-1}(a)\), \(b=Y_{a-1}(a)/(a-1)\), \(m=(b-1)/2\) and all fixed difference points are chosen as in v131/v133. The aggregate and contact shifts are then fixed. Include all finite scalar preparation primes and the finitely many new fixed data among the comparison avoidances. The simultaneous comparison prime and synchronized reference argument of v131/v133 applies literally: the private target weights and cleared errors are unchanged. The comparison poles satisfy the same selected-prime valuations and fixed-place/real limits, hence the same BB preparation. Fix the final reference before choosing the native pole witnesses. The scalar open conditions persist and BB realization applies to every actual argument. Every row has rational witnesses.

## 5. Elliptic chart and literal quadratic tables

For the scalar pair write \(\pi=\eta+S+T\) in the old finite-pair chart. Since \(d_*=\eta G\), the point difference has \(x=\eta\pi,\ y=-\eta((\eta+T)\pi+DG)\), where \(D=(3-\sqrt2)^2\). Replace the field \(x,y,y^{-1}\) by one field register
\[
 l=-((\eta+T)\pi+DG),\qquad Zl=2S_H\pi .
\]
The common norm equation \(\mathcal C\operatorname{Tr}(Z^2)=\operatorname{Nm}(f^2)\) forces \(Z\ne0\). If \(\pi=0\), the finite-pair chart gives \(d_*=0,\eta=0\) because \(F,G\ne0\); hence \(l=-DG\ne0\), contradiction. Similarly \(\eta=0\) would force \(\pi=0\). The v82 scalar valuation calculation at 149, before identifying the physical ratio, gives positive valuation of \(f\) at some slot. Thus \(H\) is formal there and \(S_H\ne0\); the old 149 reference exclusions also hold. It follows that \(l\ne0\). Only now divide by \(\eta l\) to recover \(Z=2S_H x/y\). This is exactly the required formal-parameter ratio. The completeness chart lifts the old prepared nonzero-ordinate scalar point. Four rational coordinates and rows are eliminated. In addition, inline the eighth power of \(t_j+3\) as the square of its stored fourth power, saving one coordinate per contact.

The compiler uses stored \(X_i^2\) as before and \(k_i^2=4(51X_i^2+2504)^2\), \(W_i\), \((1+W_i)^2\), \(Y_i\), \(P_i=Y_i^2-76521Y_i/64\),
\[
 r(Y_i)=32P_i^2-\frac{5951086353}{128}P_i-\frac{455376332353657}{8192}Y_i,
 \qquad P_*S_i=S_{i-1}r(Y_i).
\]
The final normalizer row is \(R(1+S_n)^2=2^{64}149^2 C^2 S_n\), with the squared factor stored separately. The seed row is \(S_0=5\cdot2^{20}149C^2\). There is one v134 normalized physical scalar circuit and one native scalar pole. All weighted comparison rows and all 52 named Jones source rows retain their old monomials by name, apart from the explicitly changed scalar, chart and contact helper equations. The counts are exact builder outputs.

Run node build.mjs (or --write) in this directory. The builder pins the v128 source blob; exact execution checked both counts, full support, distinct row names and degree at most two. Independent named source-row comparison checks the 52 original rows. The companion independent rational-arithmetic fixture checks the endpoint bound, polynomial identity at test values, persistence at positive and negative odd depths, new-contact capture, square denominators, anchor depth, and the corrected dyadic class. These finite fixtures supplement the quantified proof. The sums of squares have exact degree four. No full CI, global minimality, independent proof of the arithmetic premises, or deletion of the short-power certificates is claimed.
