> **Erratum (v140):** The changed auxiliary parameter invalidates the reuse of the v101 exclusion of s=0. Use the [guarded repair v140](../independent_prefix_guarded_v140/README.md). Historical tables are retained.

# Independent prefix integrality and a packed power congruence (v138)

**657 / 677 variables, 568 / 586 quadratic residuals.** This alternative to v137 has six extra rational coordinates, but removes the dependency of prefix integrality on the two old short-power quotients. The long power chain is not restored. The number of certified source integers is still twelve: two new ones replace the two old ones. The smaller v137 counts remain preferred. All arithmetic and coding premises of v137 are retained.

## 1. Geometric-prefix certificate

Use the source notation of [v97](../pell_power_v97/pell_power_replacement.pdf), [v98](../pell_signed_q_v98/signed_q_and_absorbed_bound.pdf), [v101](../pell_signed_branch_v101/signed_branch_projection.pdf), and [v106](../pell_integrality_replacement_v106/pell_integrality_replacement.pdf). In particular \(L=5^{60}\), \(M=q^{32}\), and \(T=b^5-1\). Delete the old certified integers \(\delta,\alpha_*\) and their congruences. Certify instead two integers \(G,J\), with the first equation
\[
q=1+TG.
\]
All other outer Jones rows, including the strengthened closeness bound
\[
k^2-4(c-kY)^2-C_*^2>0,
\]
are retained. The new Pell equations are given below. This equation proves \(q\in\mathbb Z\) and gives
\[
\lambda=(q^4-1)/T=G(q^3+q^2+q+1)\in\mathbb Z
\]
as soon as \(b>1\). The positive-source inequalities force \(b>1\) on the same cofinite instance range as v101. No Pell index argument or power congruence is used to recover these integers.

The signed prefix argument of v98/v101 uses integrality of \(q\) and \(q\equiv\pm1\bmod T\) at this stage, and hence applies to the stronger congruence just obtained. In particular \(Q=|q|\ge b^5-2\), the integral binomial prefix is recovered, and \(r\ge M\ge b^{128}\) with \(r>L\) on the retained range. The half-trace argument of v106/v108 applies to this integral prefix (including \(3\mid a\)) before any classification of the first Pell pair. It proves that \(c,d\) are integers. Apply the signed binomial argument of v101 with its retained certificates and strengthened closeness. This recovers \(b=2^\ell,\ell>0\), \(|bw|=2^{2r+1}\), and \(M\mid\binom{2r}{r}\). Its growth estimates, with \(U=|w|M\), \(S_1=|s|\), give
\[
U\ge4^r,\quad S_1>U^{r-2},\quad |a|<S_1^2,\quad S_1>L+6r+2,\quad b<Q\le U^{1/32},
\qquad |C_*|<|c|=Y_{2r+1}(|a|)<S_1^{6r}.
\]
Here \(Y_n\) denotes the usual Pell ordinate polynomial. All these deductions precede recovery of \(q=b^L\). In particular \(s\) need not be positive on an arbitrary solution.

## 2. A new parameter and a single CRT certificate

Define
\[
 A=b/2+(b^2-1)qs,\quad m=2bA-b^2-1,\quad
 V=(2A-1)/(b-1)=1+2(b+1)qs,\quad C_q=2b^2s(q^2-1).
\]
These are integers after the preceding binomial argument, because \(b\) is even. Before that argument, the same rational polynomial equations are well-defined, and are not used to infer integrality of the prefix. The explicit identity \(m=2b(b^2-1)qs-1\) gives \(m\equiv-1\bmod b\), and
\[
 m\equiv-(b-1)^2\bmod |A-1|,\qquad
 (b-1)V=2(A-1)+1.
\]
Consequently \(-mV^2\equiv1\bmod |A-1|\). In particular the two moduli \(m,A-1\) are coprime. The new equations are
\[
 C_*=C_q+m[J(A-1)-V^2(L-C_q)],\qquad
 D_*^2-(A^2-1)C_*^2=1.
\]
They give \(C_*\equiv L\bmod |A-1|\) and \(C_*\equiv C_q\bmod |m|\), using only the one certified integer \(J\). The rational \(D_*\) is integral since its square is an integer.

## 3. Exact power recovery, including the signed branches

The bounds of section 1 imply
\[
 |A|>S_1,\quad |A-1|>L+6r,\quad |m|>S_1.
\]
For example use \(|A|\ge (b^2-1)QS_1-b/2\) and the explicit expression for \(m\); these estimates also hold for negative \(q\) or \(s\). In particular \(|A|\ge2\). Integral Pell classification gives \(C_*=\varepsilon Y_\nu(A)\), \(\varepsilon\in\{1,-1\}\), \(\nu\ge0\), where \(Y_0=0,Y_1=1,Y_{n+1}=2AY_n-Y_{n-1}\). The zeroth index is excluded by \(C_*\equiv L\bmod|A-1|\). The bound on \(|C_*|\) and \(|Y_\nu(A)|\ge |A|^{\nu-1}\) show \(\nu\le6r\). Since \(Y_\nu(A)\equiv\nu\bmod |A-1|\), we have \(\varepsilon\nu\equiv L\bmod |A-1|\). Both \(L+\nu\) and \(|L-\nu|\) are smaller than \(|A-1|\); hence \(\varepsilon=1,\nu=L\).

Put \(K=b^L\). The recurrence modulo \(|m|\), using \(2A\equiv b+b^{-1}\), proves
\[
 (b^2-1)Y_L(A)\equiv b(K-K^{-1})\pmod{|m|}.
\]
Indeed multiply the ordinate recurrence by \(b-b^{-1}\) and compare with the recurrence for \(b^n-b^{-n}\). The calculation is valid without division by \(b^2-1\); \(b\) is a unit. Also \(2bs(b^2-1)q=m+1\), so the second packed congruence gives
\[
 (b^2-1)q C_*\equiv (b^2-1)q C_q\equiv b(q^2-1)\pmod{|m|}.
\]
Combining and multiplying by the unit \(K/b\) yields
\[
 (q-K)(qK+1)\equiv0\pmod{|m|}.
\]
No primality of the modulus or factorwise cancellation is used. The integer product has magnitude at most
\[
 (Q+K)(QK+1)\le4(QK)^2\le4U^{(L+1)/16}<U^{r-2}<S_1<|m|.
\]
Here \(b,Q\le U^{1/32}\), \(r>L\), and the retained lower bounds on \(r,U\) give the strict inequality. Thus the product vanishes in \(\mathbb Z\). Since \(K\ge2\) and \(q\) is integral, \(qK=-1\) is impossible. Necessarily \(q=K=b^L\). No sign assumption on \(D_*\) was needed. The old corrected Jones source soundness now applies.

## 4. Completeness

Choose the positive canonical corrected-source witnesses, with \(q=b^L\) and \(s,w>0\). Then \(G=(q-1)/(b^5-1)\) is a positive integer since \(5\mid L\). Construct \(A,m,V,C_q\) as above and set \(C_*=Y_L(A),D_*=X_L(A)\). The first congruence follows from the Pell recurrence modulo \(A-1\). The second follows from the recurrence modulo \(m\): at \(q=K\), multiplying its identity by \(q\) yields \((b^2-1)q(C_*-C_q)=0\bmod m\). Since \(2bs(b^2-1)q=m+1\), the multiplier is a unit. Coprimality then gives an integral \(J\) in the displayed CRT equation. The canonical \(J\) is positive: \(A>s>L\), \(A>b,q\), \(0<m<2A^2\), \(0<V<2A\), \(0<C_q<2A^5\). Thus the absolute value of the CRT base \(C_q-mV^2(L-C_q)\) is at most \(26A^9\), strictly smaller than \(Y_L(A)\ge A^{L-1}\). Since \(m(A-1)>0\), \(J>0\). This also checks the shifted-target nonzero guards of v137.

The strengthened closeness bound remains satisfiable. Indeed \(A\le2q^3s\), while the canonical source Pell parameter \(p=2wr^2s^2M^3>4A^2\). Hence
\[
 C_*^2<(2A)^{2L-2}<p^{L-1}<p^r<k
\]
for the canonical \(k=Y_{r+1}(p)\). As in v98 the old integral positive margin \(\eta=k^2-4(c-kY)^2\) is at least \(k\), so \(\eta-C_*^2\) is a positive integer. The same three triangular-number witnesses represent the positive margin. All remaining rational witnesses follow from the v137 tuple certificate applied to the new integral tuple, with its other source witnesses unchanged.

## 5. Exact compilation

The two certified source coordinates are renamed to power_geom and power_crt. Replace four old power rows by ten quadratic rows. Add precisely six helpers for \(qs,V,V^2,b^2s,C_q\), and the bracket in the packed congruence. Reuse the existing \(b^2,q^2,b^5\). All other residuals (558 / 576 respectively) are literally unchanged under the index-preserving renaming. Both complete sparse tables have full support and quadratic residual degree. They retain one scalar pole and two/three comparison poles.

Run node build.mjs to verify byte-for-byte replay from the pinned v137 tables, or node build.mjs --write to regenerate. Run python3 verify_prefix.py for small-index exact arithmetic fixtures of the CRT and recurrence identities, including signed inputs. The theoretical proofs above use the actual \(L=5^{60}\); finite fixtures do not replace them. No reduction in the number of integer certificates, no independent proof of the retained arithmetic premises, and no full CI run is claimed.
