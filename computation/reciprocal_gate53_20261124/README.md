# Reciprocal linear gate: a 53-variable ordinary-abc quartic

**Theorem.** Under exactly the arithmetic premises of the [54-coordinate asymmetric-contact construction](../asymmetric_contact54_20261124/README.md), including ordinary rational abc, the accompanying 43 integral quadrics have sum of squares of exact degree four and rational input projection \(\mathbb Z\) for every sufficiently large positive fixed integer \(B\equiv1\pmod8\). The 53 coordinates include the input. The sufficient cutoff remains ineffective.

The contact scalar, height, elliptic reference and translated-secant charts, signed detector and BB pole theorem are unchanged. The new normalizer is linear instead of quadratic in the stored scaled detector value. Its reciprocal chart excludes the zero-input degeneration of the physical pole without a new inverse coordinate. Completeness at foreign primes uses an extra valuation identity for the **actual multiplication family**, proved below; it does not follow from the old arbitrary-witness normalizer lemma.

## 1. Physical reciprocal pole and gate

Use all the physical notation of [v81](../../papers/quartic_existence/paired_contact56_20261119_v81.tex) and the asymmetric-contact successor:
\[
 u=1/c,\quad W=1+c C^4+c^2J^2-c^3\bar I^{\,4}-c^4\bar K'^{\,2},
 \quad D\operatorname{Tr}W=\operatorname{Nm}(W-1),\quad D_s=uD.
\]
The trace of \(W\) is nonzero by the old norm argument, so \(D\) is determined. Put
\[
 A=u+D_s=u(1+D).
\]
Here \(A\) is only a linear expression, not a new coordinate (it is unrelated to the contact polynomial value called \(A\) in the parent). Replace the old three normalizer rows by the reciprocal gate
\[
 (t-1)A=1,\qquad b=7c/t^2
\]
where the latter formula is for \(t\ne0\). In the actual polynomial system we do **not** assume \(t\ne0\) or use its inverse. Instead replace the physical native pole equations by
\[
 \tag{1}
 e^2+7c p'^2=1,\qquad U'V'=e(t^2-7c),\qquad U'^2-V'^2=7c q^2 .
\]
If \(t\ne0\), these equations are exactly equivalent to the parent native equations for \(b=7c/t^2\): recover \(p=tp'\), \(u_0=U'/t\), \(v_0=V'/t\), with \(e,q\) unchanged. Conversely these substitutions in reverse recover (1) from every native solution. There are no additional coordinate restrictions.

## 2. Soundness at consumed primes, including the zero fiber of the reciprocal chart

The unchanged asymmetric-contact estimate gives
\[
 \log r^+_{\rm odd,S}(u)\ge (23/20)h(M)-O(1),
 \quad M=B+8(X^8+T_{\rm sc}^2)\ge B .
\]
Consequently there is at least one retained prime with \(\mu=v_p(u)>0\) odd on every admissible contact fiber for sufficiently large \(B\). Take any such prime, in particular \(p\ne2,7\).

We first show that the polynomial system itself excludes \(t=0\) on these fibers. If \(t=0\), the first equation of (1) has terms of opposite valuation parity because \(v_p(7c)=-\mu\) is negative odd. As their sum is 1, they are both integral, \(e\) is a unit, and the middle equation \(U'V'=-7ce\) gives \(v_p(U')+v_p(V')=-\mu\). Both factors are nonzero and their valuations differ. Hence the valuation of \(U'^2-V'^2\) is finite even, while that of \(7cq^2\) is odd if \(q\ne0\), and infinite otherwise. Both contradict the last equation of (1). This excludes the degenerate fiber without a nonzero assumption on a native pole witness.

Now \(t\ne0\), so the physical pole is valid. The native negative-odd obstruction gives \(v_p(b)=-\mu-2v_p(t)>0\), or \(v_p(t)<-\mu/2\). The exact gate forces \(A\ne0\) and \(v_p(A)=-v_p(t)>\mu/2\), since \(t-1\) has the same negative valuation as \(t\). Subtracting \(u\) gives \(v_p(D_s)>\mu/2\) and therefore
\[
 v_p(D)>-\mu/2.
\]
This is stronger than the parent's \(-3\mu/4\) lower bound. The unchanged norm/trace inequality consequently provides a slot with \(v(W)>-3\mu/4\), and the four different valuation classes modulo four of the signed detector terms force all four raw tests to be positive there. This is the v81 extraction lemma, including zero tests and inert primes. It gives local integrality of \(X\) and \(p\mid\operatorname{num}(X(m-X))\) whenever \(X\ne0,m\). The unchanged strict height margin \(23/20-1002/997>0\) of the 54-coordinate proof then forces \(X=0\) or \(X=m\in\mathbb Z\) for sufficiently large fixed \(B\). Neither the new gate nor this argument assumes the true multiplication relation on arbitrary solutions.

## 3. A valuation identity for the actual multiplication family

In this section the residue characteristic is odd, the curve \(y^2=x^3-\Delta x\) has good reduction, \(\Delta\) is a unit, and valuations on the unramified local field are normalized by \(v(p)=1\). Let \(Q\) be a non-torsion point of finite nonzero abscissa, let \(n\ne0\) be an ordinary integer, and put \(V=[n]Q\). Define
\[
 f(R)=1/x(R),\quad s(R)=y(R)/x(R),\quad
 K_Q=n^2 f(Q)f(V),\quad I_Q=n s(V)-s(Q).
\]
If \(v(K_Q)=-2k\) with \(k>0\) odd, then
\[
 \tag{2}v(I_Q)=-k.
\]

To prove (2), classify \(Q\) by its abscissa. If \(v(x(Q))<0\), \(Q\) is in the first formal subgroup and so is \(V\); both reciprocal abscissas have positive valuation and \(v(K_Q)\ge0\). If \(v(x(Q))>0\), \(Q\) reduces to the two-torsion point \(T=(0,0)\). Translation by \(T\) has abscissa \(-\Delta/x(Q)\), so \(Q+T\) is formal, of some integer depth \(a\ge1\), and \(v(f(Q))=-2a\). At these good odd unramified places the formal logarithm is an isometry; \([n](Q+T)\) has depth \(a+v_p(n)\). For even \(n\) the point \(V\) itself is formal and \(v(K_Q)=4v_p(n)\ge0\); for odd \(n\), \(V+T\) is formal and \(v(K_Q)=-4a\), divisible by four. Neither gives the assumed negative valuation congruent to two modulo four.

It follows that \(v(x(Q))=0\), so \(v(f(Q))=0\) and \(s(Q)\) is integral. The assumed valuation implies \(v(x(V))=2(k+v_p(n))>0\). The curve equation and unit \(\Delta\) give \(v(y(V))=k+v_p(n)\), hence \(v(ns(V))=-k<0\). Subtracting the integral \(s(Q)\) proves (2). This covers all three possibilities for the abscissa; no conjectural distribution of local reduction types is used.

In the parent complete witness family for \(X=n\ne0\), \(U=[n]H\), \(V=[n](H-R_0)\), so its second raw product and error \(K',I\) are precisely \(K_Q,I_Q\) for \(Q=H-R_0\). The identity also holds at the conjugate slot.

**Consequence.** At every good odd rational prime with \(v_p(c)=k>0\) odd, in this true family, every local slot in which \(W\) is integral satisfies \(W\equiv1\) modulo the prime. Indeed the nonconstant terms have distinct classes modulo four, using the even valuations of \(J,K'\). Hence if any one has negative valuation the unique negative minimum makes \(W\) nonintegral. The first, second and third terms cannot have valuation zero. If the last has valuation zero then \(v(\bar K')=-2k\). By (2), \(v(\bar I)=-k\), so the third term has valuation \(3k-4k=-k<0\), a contradiction to integrality. Thus every nonconstant term is positive at an integral slot. In the parent's \(X=0\) complete fiber the same conclusion holds because every raw test is zero and \(W=1\).

Use the identity
\[
 1+D=\frac{\operatorname{Nm}W+1}{\operatorname{Tr}W}.
\]
If both slots are integral then both reduce to 1, so the ratio is a unit at an odd prime. If one is a pole and the other integral, the latter is a unit and both numerator and denominator have the same negative valuation, so the ratio is a unit. If both are poles of valuations \(w_1,w_2<0\), the numerator has valuation \(w_1+w_2\), while the denominator has valuation at least \(\min(w_1,w_2)\); thus \(v_p(1+D)\le\max(w_1,w_2)<0\). The inert case is the same computation with repeated valuations. In all cases \(1+D\ne0\) and \(v_p(1+D)\le0\). Therefore for this complete family, at any **negative odd valuation of \(u\)** outside the fixed good-prime exceptions,
\[
 v_p(A)=v_p(u)+v_p(1+D)<0,\qquad t=1+A^{-1}\equiv1\bmod p,\qquad v_p(b)=-v_p(u)>0 .
\]
This is the needed replacement for the old normalizer's stronger arbitrary-witness assertion. Only completeness uses it.

## 4. Ordered completeness at every prime

Fix the integer input and choose exactly the same multiplication family and asymmetric-contact prime pattern as in the 54-coordinate theorem. All constants, the fixed height \(M\), the finite avoidance set and the point neighborhoods are prepared in the same order. In particular at each freshly selected contact prime \(v_p(u)=1\), the successful-slot raw tests have the old positive depths and the opposite reciprocal products are units; hence \(v_p(D)>0\) by the parent calculation. This gives \(v_p(A)=1\), \(v_p(t)=-1\) and \(v_p(b)=1\). At least one such prime exists in every constructed witness, including the parent zero-input fiber, where \(D=0\). Thus \(A\) and \(t\) are globally nonzero.

At the fixed finite places and positive real infinity in the slope the old estimates \(W-1=O(c)\), \(D=O(c^2)\), \(c\to0\) are unchanged. They now give \(A=c^{-1}(1+O(c^2))\), \(t=1+O(c)\), \(b\sim7c\). All fixed exceptional primes, including 2 and 7, may be prepared by sufficiently deep slope denominators. The unchanged dyadic squareclass of \(c\), the real positivity and smallness, and the seven-adic positive valuation give all BB preparation conditions there. At any remaining prime outside seven of even valuation of \(u\), the valuation of \(b=7c/t^2\) is even; negative odd valuations of \(u\) are covered by Section 3, and positive odd valuations of \(u\) occur only at the selected primes by the parent's full prime factorization. Hence the actual \(b\) has square reduced denominator and is prepared: \(0<b<1\), \(b\in7\mathbb Q_2^{\times2}\), \(v_2(b)\ge4\).

Apply the same published class-seven BB-native pole realization to this actual scalar. Use the inverse substitution of Section 1 to supply (1), without changing the already chosen point and contact values. This proves complete rational witnesses for every integer, including zero. No global rational-point realization beyond the parent theorem is introduced.

## 5. Complete coefficient table and exact census

Retain the old coordinates \(x_1,\ldots,x_{53}\) from the 54-coordinate table, deleting \(x_{54}\) (the old \(\alpha\)). The stored meanings of \(x_{33},x_{34}\) become \(t,k_s=ut^2\); the pole coordinates \(x_{35},x_{36},x_{38}\) are \(e_s,U_s,V_s\) with \(e=ce_s,U'=cU_s,V'=cV_s\). Store \(x_{37}=p'\), \(x_{39}=q\), \(x_{40}=P_s\), \(x_{41}=Q_s\) with \(p'^2=cP_s,q^2=cQ_s\). The two old square rows and the old unit \(cu=1\) are retained. The other three native rows and the new gate/input rows are
\[
\begin{aligned}
 e_s^2+7P_s&=u^2,\\
 U_sV_s&=e_s(k_s-7),\\
 U_s^2-V_s^2&=7Q_s,\\
 (t-1)(u+D_s)&=1,\\
 ck_s&=t^2 .
\end{aligned}
\]
Multiply the first three rows by \(c^2\) and use the two square rows and the unit to recover (1) exactly. The pole input row is valid even at \(t=0\); that fiber was excluded arithmetically above. Thus these are literal integral quadrics with no hidden divisions. All other rows of the parent are unchanged, including the height equation and all eight asymmetric contact rows.

The exact table has **53 coordinates and 43 quadratic residuals**. Their sum of squares has **791 coordinate monomials** and 795 parameter-separated terms. All variables occur, the coefficient of \(X^4\) is one, and therefore the degree is exactly four and the content is one. The literal \(B=1\) algebraic fixture has 11,193 ASCII bytes and coefficient height 5,531,402,752. It is not claimed to define the integers; sufficiently large \(B\equiv1\pmod8\) is required.

Run the accompanying verifier against the pinned parent from the repository root. It checks every unchanged row, the five replacement quadrics, full expansion, support, content, fixture size and finite local profiles. The valuation and height arguments are the mathematical proof, not conclusions inferred from finite tests. The original reference/multiplication charts are credited in the parent papers; the reciprocal gate and true-multiplication negative-odd preparation proof are the new deductions.