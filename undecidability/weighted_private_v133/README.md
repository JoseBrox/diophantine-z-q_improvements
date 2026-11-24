# Weighted private point charts and reflected contact circuits (v133)

**774 / 795 rational unknowns, 663 / 682 quadratic residuals**, for the general / specified routes. The twelve source predicates, short Pell-power block, three growth labels and twelve scalar poles of v131 remain. There is no additional ordinary-rational-abc premise; every retained arithmetic and coding premise of v131 is still required. The coefficient threshold of the specified route is effective by the recipe below, not the previously fixed coefficient. This is a new source-instance projection equivalence, not a bijection on all auxiliary zeros.

## 1. Weighted private point chart

Use the notation of [v131](../shared_comparison_v131/README.md). For each source input X put beta=51 X^2+2504 and k=2 beta. Thus k>0 on *every* rational input, not only the desired integer fibers. Let (S,T,F,G,eta,d_*) be the actual finite-pair chart over K=Q(rho), rho^2=2, and D=(3-rho)^2. Store instead
\[
 (S',T',\eta')=k(S,T,\eta),\quad (F',G')=k^2(F,G),\quad d_*'=k^3d_* .
\]
The four field rows become
\[
 d_*'=(\eta'+S'+T')F'=\eta'G',\quad
 D(F'+G')=(S'-T')\eta'-T'^2,\quad
 k^4=d_*'(S'-T')-DF'G'.
\]
All are quadratic once k^2 is an affine expression in the stored normalizer register of Section 2. The inverse scaling recovers the complete old finite-pair chart, including finite torsion differences and tangents. Its stored abscissa contribution is now \(\eta'(\eta'+S'+T')=k^2x(A)\). No actual abscissa coordinate is added.

Replace the private cleared errors by the *linear* expressions
\[
 C_i=S_i'-2S_H,\qquad E_i=\overline{T_i'}-2\overline{T_{H-P_0}}.
\]
These are literally the original physical errors, so four rational error registers and their defining rows disappear per input. For its formal term use \(r_i'=F_i'+c\bar G_i'\), i.e. the scaled rather than physical reciprocal abscissas. The same factor \(1+c(r_i')^2+c^2C_i^4+c^4E_i^8\) is compiled by the existing quadratic square registers. The reference and three growth pairs are unchanged.

Here is the necessary additional local proof, since the formal tests are no longer identical on arbitrary rational inputs. At a consumed prime of odd depth mu, the v131 parity-factor and norm/trace argument remains valid: all its tagged valuations have the same residue classes. In a common successful slot, \(v(r_i')>3\mu/8\) and the two cleared errors have positive valuation. Reciprocal abscissas at a good prime have even valuation (from \(y^2=x^3-Dx\) with D a unit, considering positive and negative abscissa valuations separately). Multiplication by the rational square k^2 preserves this parity. Thus \(F_i'\) and \(c\bar G_i'\) have opposite parity and both have positive valuation. The unscaled reference factor gives the two formal reference points as before, in particular its slopes have negative valuation in their intended slots.

In either of the corresponding slots, write \(F=1/x\) and \(S=y/x\) for the unscaled private point. We have \(v(k^2F)>0\) and \(v(kS)=v(2S_H)<0\), using the appropriate reference slope for the opposite slot. If \(v(F)<0\), the identity \(S^2=1/F-DF\) gives \(v(kS)=v(k^2F)/2>0\), impossible. If \(v(F)=0\), then \(v(S)\ge0\) and \(v(k)>0\), again impossible. Hence \(v(F)>0\). The opposite argument with \(G,T\) is identical. This proves actual formal membership without presupposing local integrality of k. Dividing the positive-depth cleared errors by the physical formal slopes now gives the same precision at least two, and the retained relative order-four logarithm and subtraction give \(k\equiv m_i\bmod p^2\) as in v131, including local integrality of k. All growth-label estimates are unchanged. In particular \(M_j^2\mid|\operatorname{num}(2\beta_i-m_i)|\) for a nonzero error, and \(M_j^4\mid\Delta\) for a nonzero growth residual.

On the intended integer witness, k is fixed and nonzero before comparison prime selection. Exclude its prime divisors along with the already fixed finite avoidance data. All selected local valuations and precisions are then exactly as in v131. At fixed prepared places and real infinity the scaled point functions remain bounded, since the k are fixed. This change creates no new local realization premise.

## 2. Exact scalar normalizer circuit

The private normalizer polynomial is
\[
 r(\beta)=\beta(\beta-1)(\beta-2401)(32\beta+343)
 =32\beta^4-76521\beta^3-747054\beta^2+823543\beta.
\]
Set \(P=\beta^2-76521\beta/64\). Direct expansion gives
\[
 r=32P^2-\frac{5951086353}{128}P-\frac{455376332353657}{8192}\beta,
 \qquad k^2=4(P+76521\beta/64).
\]
The two former factor registers are replaced by this one register. The actual normalizer r and R, tau, and native scalar pole are unchanged; the k^4 in the new chart is the square of an affine expression. This saves one more rational coordinate and row per input. The displayed identity was independently expanded using exact rational symbolic arithmetic.

## 3. Weighted aggregate and its effective height inequality

Store
\[
 Z_{\rm agg}=U+\rho V
 =\sum_{i=1}^{12}k_i^2(x(A_i)+d)+
       \sum_{\ell\in\{a,t,m\}}(x(A_\ell)+d)+20,
 \qquad d=3-\rho.
\]
Both embeddings are at least 20. The two/three contact arguments of v131 remain \(\lambda,\lambda+U,\lambda+U+10+V^2\), using the appropriate subset. The aggregate row is quadratic by Section 1. Let \(w_i=k_i^2\) for the input points and \(w_i=1\) for the growth points; \(H_w=\sum_i h(w_i)\).

### Effective weighted extension of v62

For r finite points \(Q_i=[n_i]P+T_i\) in the setting of the [effective torsion-sum theorem](../../papers/effective_sums/effective_torsion_sums_20261117_v62.tex), put
\[
 Z=\sum_i w_i(x(Q_i)+d)+c_0,\quad w_i\in\mathbb Q_{>0},\quad c_0\in\mathbb Z_{>0},
 \quad M=\max(1,|n_1|,\ldots,|n_r|).
\]
Then
\[
 h(Z)\ge\max_i h(x(Q_i))-A_r\log M-B_r-h(d)-R_K
             -(2^{r-1}+1)H_w ,
\]
where \(A_r,B_r,R_K\) are exactly those of v62. Proof: take the positive integer \(L\) equal to the product of the reduced denominators of the weights, and \(W_i=Lw_i\in\mathbb Z_{>0}\). We have \(\log L,\log\max_iW_i\le H_w\). Apply the principal-part proof of v62 to \(LZ\). At a finite place, the weighted deep-subset numerator is the positive integer
\[
 C_J=\sum_{j\in J}W_j\prod_{a\in J\setminus\{j\}} n_a^2.
\]
The remainder is no worse than in v62, since all W_i are integral and the translation is integral. For a deep index i the local loss is at most \(v(C_J)+b_{\mathfrak p}\); for a shallow index it is at most \(b_{\mathfrak p}\), as in v62. Each numerator is bounded by \(\max W_i\,|J|M^{2(|J|-1)}\); there are at most \(2^{r-1}\) subsets containing i. Thus the new finite-place loss is at most \(2^{r-1}\log\max W_i\). At real places \(LZ=\sum W_i(x(Q_i)+d)+Lc_0\), so the original archimedean comparison holds since \(W_i\ge1\). Finally \(h(LZ)\le h(Z)+\log L\). This proves the asserted inequality, uniformly including every finite torsion fiber. No new effective height theorem is assumed.

Use this with r=15, P=R_0 and K=Q(rho), for which \(R_K=0\). The retained duplication bound is \(h(x(Q_i))\ge n_i^2/4-3\) for a nonzero index. As in v131, \(B\le3M\), \(A_r\log M\le M^2/8+2A_r^2\), \(B_r\le r2^{r-1}\), \(h(d)<2\), and \(h(Z_{\rm agg})\le h(U)+h(V)+2\). Hence
\[
 B^2\le K(1+h(U)+h(V)+H_w),\quad
 K=72(2A_r^2+r2^{r-1}+8+2^{r-1}+1)
\]
is an explicit sufficient constant for the specified three-contact route.

### Ineffective two-contact variant

The [positive weighted trace theorem v27](../../papers/trace_heights/weighted_trace_20261114_v27.tex) extends without change of external theorem to a fixed vector of rational weights: use the product of their projective parameter lines and the trace parameter line instead of the single r-line and trace line in that proof. At every actual tuple the weights are positive; the noncancellation lemma on translates uses only positivity of their values. The graph of the fixed multivariate weighted trace function, including the linear shift \(d\sum w_i+20\), is integral reduced; the same fixed abelian variety, subgroup, symmetric embedding, and section-surjectivity conditions apply. The Segre parameter height is \(\sum h(w_i)+h(U)\) up to a bounded term. Freeze all index-zero torsion coordinates as before. The same family theorem therefore supplies a fixed ineffective \(K\ge1\) with \(B^2\le K(1+h(U)+H_w)\). It is independent of the weights and scalar parameter N.

### Absorption and the unchanged amplifier

The twelve unmodified scalar poles give the original estimate \(A=|a|\ge149^{L_N}\) and \(h(\beta_i)\le C_s149^{-L_N}A(1+\log A/3)\) with \(C_s=2^{330770}\). Since \(h(k_i)\le h(\beta_i)+\log2\), \(h(w_i)=2h(k_i)\), and \(\log A\le\sqrt A\) for \(A\ge1\),
\[
 H_w\le56 C_s A^{3/2}.
\]
Choose N so \(149^{L_N}>(112 K C_s)^2\). Then \(KH_w<B^2/2\), and the respective aggregate bound reduces to the v131 bound with 2K in place of K. Enlarge N further by the v131 sufficient recipe with 2K, including its existing finite exceptional set. This is effective on the specified route; the general threshold remains ineffective. The original two/three-contact height inequalities, divisibility of the residuals, and Pell amplifier now apply verbatim. They prove that every source input is integral. The retained 52 Jones rows recover the coding instance.

For completeness fix the source integer tuple, prepare the common scalar and growth labels exactly as in v131, then fix the weighted aggregate and contact shifts. Positive weights and the translation keep the translated contact sets separated. The same simultaneous prime supplier and reference synchronization apply after the finite avoidance enlargement of Section 1. All contact, real and fixed-place BB preparations are unchanged; in particular no product of unrelated scalar squareclasses has been substituted for the twelve private scalar poles.

## 4. Reflected denominators and redundant guards

For either contact set let c_* be the reflection center (1 or 3/22). With \(T=(t-c_*)^2\),
\[
 G(t)=\prod_{\theta\in\Theta_0}(T-(\theta-c_*)^2).
\]
Evaluate this monic quintic from the three stored registers \(T,T^2,T^3\) and one denominator register, using
\(G=T^2(T^3+a_4T^2+a_3T)+a_2T^2+a_1T+a_0\).
All rows are quadratic, and this replaces the nine old product registers with four.

The literal gate equation \(q_j(g_j-1-E_g^2)=(c-q_j)^2\) and \(cu=1\) already imply \(q_j\ne0\). If \(t_j=-3\), the reflected polynomial is nonzero there in either set and the contact equation forces q_j=0, impossible. Therefore the separate inverse of \(t_j+3\) is redundant. The contact equation also excludes \(G(t_j)=0\). Delete the inverse of \(1+q_j\): at any consumed prime \(v(q_j)<0\), so \(1+q_j\ne0\) and the physical tau and obstruction have exactly their old interpretations. If \(q_j=-1\) globally, there are no consumed primes for this contact; the retained radical-one height bound still applies. This larger auxiliary fiber cannot evade the global argument, which uses only the prime-wise divisibility and the full-domain height bound. Completeness uses the same prepared large slopes, avoiding both old guard zeros. Thus seven coordinates and rows per contact disappear.

## 5. Census and reproducibility

The pinned v128 source is identical to v131: all 52 named Jones rows, all twelve integer inputs, borrowed source square registers, instance parameter conventions and short-power congruences are preserved. Sections 1–2 remove five coordinates/rows per input. Section 4 removes seven per contact. The two counts are \(848-60-14=774\), \(737-60-14=663\), and \(876-60-21=795\), \(763-60-21=682\). The builder and complete sparse coefficient tables are included. Run node build.mjs (or --write to regenerate). Exact execution checked every degree, full support, distinct row names and preservation of the 52 source rows independently by named monomial comparison. The sum of real squared quadratic leading forms cannot cancel, so the quartic degree is exactly four. This does not independently prove the retained arithmetic or Jones coding inputs; full repository CI has not been run.

The source certificate count is unchanged. No assertion of simultaneous scalar-pole sharing, short-power quotient elimination, or global minimality is made here.
