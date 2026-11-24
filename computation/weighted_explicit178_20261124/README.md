# An explicitly specified 178-variable defining quartic

**Theorem.** Under precisely the arithmetic hypotheses of the fixed 179-variable BB-native defining quartic, the complete integer coefficient table here defines Z in Q in **178 total variables**, including the input, as the sum of 150 quadratic squares. There is no new ineffective parameter. The previous fixed anchor \(A_{\rm a}=A_0B_{\rm a}^4\) is unchanged. The proof is an effective weighted abscissa-sum estimate, not an invocation of the ineffective weighted trace theorem.

The underlying point charts, local extraction, scalar preparation, numerical modular bounds and prime supplier are those in [v82](../../papers/quartic/scalar_point163_179_20261120_v82.tex) and the [BB-native replacement](../../papers/quartic/bb_native_quartics_20261124.tex). In particular we retain their stated arithmetic premises; we are not claiming their complete independent proof. The present weighted estimate extends the elementary finite-place argument of [v62](../../papers/effective_sums/effective_torsion_sums_20261117_v62.tex), and removes the reciprocal register that v82 needed to retain its effective unweighted height argument.

## 1. Effective positive rational weights, including torsion

Let \(K=\mathbb Q(\sqrt2)\), \(d=3-\sqrt2\), \(E:y^2=x^3-d^2x\). Retain the v62 notation \(Q_i=[m_i]R_0+T_i\ne O\), \(T_i\in E[2](K)\), \(1\le i\le r\), and \(M=\max(1,|m_i|)\). Let \(w_i\ge1\) be arbitrary rational weights. Write \(w_i=a_i/b\) with a common positive integer denominator and positive integer numerators, and put \(A=\max(b,a_1,\ldots,a_r)\). Define
\[
 Z_w=1+\sum_i w_i(x(Q_i)+d).
\]
Then
\[
 h(Z_w)\ge\max_i h(x(Q_i))-
 2^{r-1}\log A-(r-1)2^{r-1}\log M-
 \sum_{j=1}^r\binom{r-1}{j-1}\log j-h(d).
\tag{1}
\]

Proof: use the normalized absolute heights of v62. At every finite place of this K the v62 formal logarithm is injective on the first formal subgroup. If Q_i is formal, \(m_i\ne0\) and \(x(Q_i)=(m_i L_v)^{-2}+\epsilon_i\) with integral error and common \(L_v\ne0\). A finite nonformal point has integral abscissa, including finite torsion. Let J be the indices of the formal points, and fix i in J. The principal part of \(bZ_w\) is
\[
 (m_i L_v)^{-2}\frac{C_J}{\prod_{j\in J\setminus\{i\}}m_j^2},
 \qquad C_J=\sum_{j\in J}a_j\prod_{k\in J\setminus\{j\}}m_k^2>0.
\]
All other terms, including the translation \(\sum a_jd+b\), are integral. The local height loss relative to x(Q_i) is at most \(v(C_J)\), by the same comparison of the principal part with the integral error as in v62. Dividing by the positive integer b can only increase finite-place height. At a place where Q_i is nonformal there is no positive loss. Sum over the at most \(2^{r-1}\) subsets containing i and use \(C_J\le |J| A M^{2(|J|-1)}\). This proves the finite-place part. At both real embeddings, \(x(Q_j)\ge-d\); hence \(Z_w\ge1\), and every nonnegative abscissa is bounded by \(Z_w\), since its weight is at least one. The absolute value of a negative abscissa is bounded by d. The archimedean loss is at most h(d). This proves (1) without a new logarithmic or height hypothesis.

In particular put \(w=(1,R,1,1)\), where the scalar normalizer \(R=A_{\rm a}r/(1+25r)>100\) is the v82 fixed one. Take b and a to be the reduced denominator and numerator of R; then \(\log A=h(R)\). Use the same individual lower bounds \(h(x(Q_i))\ge m_i^2/4-3\) from v62, under its retained canonical-height and duplication premises, for nonzero m_i. The weaker constant six is sufficient. Put \(B=\max(1,|m_1|/2,|m_2|,|m_3|,|2m_4+1|)\), exactly the v82 label size. At r=4 the subset coefficients are 8,24 and \(\log864\). As in v62,
\[
 24\log M-M^2/8\le12\log96-12<43,\quad
 6+43+\log864+\tfrac12\log7<57.
\]
Therefore \(M^2<8h(Z_w)+64h(R)+456\), including the all-zero index case, and \(B^2\le5M^2+5\) gives
\[
 B^2<40h(Z_w)+320h(R)+2285.
\tag{2}
\]

## 2. The two effective aggregate equations

Write \(S_0+\sqrt2 S_1=x(Q_1)+R x(Q_2)+x(Q_3)+x(Q_4)\). Use the same three reflected contact arguments as the fixed v82 member, with
\[
 t_1-t_0=13+S_0/2,\qquad t_2-t_1=17+(S_0-S_1)/2.
\]
The exact identity is now
\[
 Z_w=-(2+2\sqrt2)t_0+(2+4\sqrt2)t_1-2\sqrt2 t_2-13+4\sqrt2+(R-1)d.
\]
At every finite place its coefficients are integral; at each real embedding the sum of the absolute values of its five affine coefficients is less than 64. Thus \(h(Z_w)\le\sum_{j=0}^2 h(t_j)+h(R)+\log64\). In particular (2) gives the explicit bound
\[
 B^2<40\sum_j h(t_j)+360h(R)+2500.
\tag{3}
\]

## 3. The original fixed anchor still suffices

Retain every scalar and comparison extraction in v82/BB-native unchanged. In particular, writing \(\beta=51X^2+2504\) and \(a=m_2\), the exact original anchor computation gives \(|a|\ge2^{960}\) and \(h(\beta)<|a|/2\) for every rational zero. The rational map for R gives
\[
 h(R)\le4h(\beta)+\log1801500+\log A_{\rm a}<4h(\beta)+300.
\]
Indeed \(A_{\rm a}<2^{375}\), and the denominator row sum 26 is smaller than \(A_{\rm a}\); use \(\log2<7/10\) and \(1801500<2^{21}\). Hence
\[
 360h(R)+2500<720|a|+110500<B^2/2,
\]
using \(B\ge|a|\ge2^{960}\). It follows from (3) that
\[
 B^2/2<40\sum_j h(t_j).
\tag{4}
\]
All constants are effective; no enlargement of the old anchor is necessary.

If the integer Lucas residual \(\Delta\ne0\), put \(J=a\Delta\ne0\). The v82 local argument gives \(M_j^3\mid J\) and \(|J|\le14B^5\); both assertions are unaffected by the new aggregate shifts. Retain the explicit reflected-contact estimates of v68:
\[
 h(t_j)\le\log33+\mathcal C M_j\sqrt{E(M_j)}
                 (\log J_*+\tfrac12\log M_j),\quad
 \mathcal C<2^{300},\quad J_*<2^{75},\quad
 E(M)<(21/10)M^{1/6006}.
\]
The additive \(240\log33\) in (4) is absorbed by two more units of \(\mathcal C\sqrt{21/10}\,|J|^{1/3+1/36036}(\log J_*+\log|J|/6)\): indeed \(\mathcal C>2^{68}\), \(J_*>2\). Thus
\[
 B^2<242\mathcal C\sqrt{21/10}\,|J|^{1/3+1/36036}
                 (\log J_*+\tfrac16\log|J|).
\]
The exact rational estimates in v82, with the constant doubled, give for \(s=\log B\)
\[
 e^{(1/3-5/36036)s}<1000\,2^{300}(54+5s/6).
\]
The quotient of the exponential by its linear factor is increasing on \(s\ge0\). At \(s=960\log2\), the left divided by \(2^{300}\) exceeds \(2^{20}(2723/3003)>614000\), while the right divided by \(2^{300}\) is strictly less than \(1000(54+800\cdot7/10)=614000\). Contradiction. Hence \(\Delta=0\).

For a nonzero input residual \(J_X=|\operatorname{num}(\beta-n)|\), use \(M_j\mid J_X\), \(J_X\le4B e^{h(\beta)}\), and the original weaker contact bound
\[
 h(t_j)\le K M_j(22+\tfrac12\log M_j)^2,\qquad K=2^{304}.
\]
Equation (4) gives \(e^s<960K e^{h(\beta)}(23+(s+h(\beta))/2)^2\). Taking logarithms and using \(\log(1+x)\le x\) yields
\[
 s<\frac{23}{22}\log(960\cdot529 K)+\frac{12}{11}h(\beta)
 <240+|a|.
\]
The last estimate uses \(960\cdot529<2^{19}\), \(\log2<7/10\), and \(h(\beta)<|a|/2\). The unchanged Lucas descent gives \(s\ge(|a|-6)\log(|a|-3)>240+|a|\). This contradiction proves \(\beta=n\in\frac12\mathbb Z\), so in lowest terms the denominator of X has square dividing 102; hence X is an integer.

## 4. Ordered completeness

Retain the v82 choice of the scalar reference progression and the nonzero scalar label a, then the Lucas labels and four finite difference points. The new R-weighted sum is fixed before choosing the comparison primes. For these integer witnesses Q2 is a nonzero doubled point and has abscissa greater than d at each real embedding; all other abscissas are at least -d. Thus the new weighted sum is greater than \((R-3)d>0\) at both embeddings. Its first rational component and the difference of its two rational components are positive (the latter is a positive weighted combination of the two embeddings). The successive shifts exceed 13 and 17, so the three translated reflected contact lists remain disjoint. The unchanged prime selection, synchronization and real/local preparation apply to these fixed shifts, with the same finite avoidance. All scalar and comparison BB-native pole arguments therefore have their previously proved rational realizations. Fill the same physical point and detector coordinates, using the weighted shifts. This is completeness for every integer input; no additional arithmetic supplier is needed.

## 5. Literal quadratic transformation and guards

Use the old 179-coordinate numbering in this section. Remove x91=R^-1 and its unit row. In the two aggregate rows replace respectively \(x_{91}x_{114}\) by \(x_{114}\) and \(x_{91}x_{115}\) by \(x_{115}\), the two components of \(R x(Q_2)\). These are exactly the weighted aggregate identities of section 2. Use the scalar pole gauge of the v82 physical equations rather than their former R^-1-scaled version: multiply each old stored scalar pole coordinate with label in {11,12,13,14,81,82,83,84,85} by R. These coordinates occur only in the seven scalar pole rows. All five homogeneous native/square rows are unchanged after division by the common square factor. The two remaining rows become
\[
 x_{81}x_{88}=x_{89}^2,\qquad x_{81}x_{82}=x_{89}+9792x_{90}.
\]
Here \(x_{90}=R,\ x_{89}=R^2\). All other rows are literally retained, with indices above 91 shifted down by one.

Before using the new chart's inverse gauge, the unchanged \(c c^{-1}=1\) row gives \(x_{162}\ne0\) in old numbering. The input-square and scalar pair equations recover \(x_{37}=cX^2,\ x_{77}=c(51X^2+2501)^2/4\). The four-contact product row then gives \(x_{78}R=c^2 r(X)>0\); the last inequality follows from \(\beta\ge2504\), since all four factors of r are positive. The forced-normalizer row gives \(A_{\rm a}x_{78}=25x_{78}R+c^2\). Substitution yields \(R=A_{\rm a}r/(1+25r)>100\). In particular the deleted reciprocal is recoverable and no R=0 branch is introduced. Dividing the nine scaled pole coordinates by R restores their exact old physical meanings. This lift recovers all predecessor equations except the intentionally changed aggregate constraints, whose arithmetic was proved above. Conversely the physical ordered witnesses give the new table. Every row is still of degree at most two, and the coefficient of X^4 in the sum of squares is one.

The complete table, expanded integer polynomial and plain-text file accompany this proof. The independent checker verifies the pin, all row maps and occurrences, the scalar polynomial identity before division by R, the two height endpoint inequalities, the coefficient expansion, and primitive content. It does not infer the retained arithmetic theorems from numerical tests.
