# One pole for a height-anchored elliptic quotient, and the exact remaining obstruction

## Result

Retain ordinary rational abc, the rational rank-one chart and exponent-one primitive divisor mass of [v82](../prepared_eds_divisibility_20261120_v82.tex), and the published prepared class-seven BB pole theorem of [v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex). Put
\[
E:y^2=x^3-2x,\qquad P=(9/4,-21/8),\qquad q=\widehat h(P)>0.
\]
For any fixed integer \(N\ge1\), the following **six-coordinate** polynomial relation has distinguished rational input \(X\), represents points \(H=[h]P,U=[j]P\) with \(h,j\ne0\), and satisfies, on every solution after a fixed finite reference-index exclusion:

1. \(h\mid j\). Write \(m=j/h\in\mathbb Z\).
2. \(h(X)\le q h^2/1196+O(1)\), with constants independent of all witnesses. Here \(h(X)\) denotes logarithmic rational height, whereas the index \(h\) is an integer.
3. Either \(X=m\), or
\[
\log(1+|m|)\ \ge\
\left(\frac{N+2}{7}-\frac1{1196}\right)q h^2-O(1).
\]
4. For every nonzero integer \(X=m\), witnesses with \(U=[m]H\) exist with arbitrarily large positive reference index \(h\).

These conclusions do not require the simultaneous tailored-prime supplier or the original quadratic-field carrier. The two former tasks of input-height anchoring and quotient comparison use one actual prepared pole. The rational point chart and primitive-prime theorem are as in v82.

**This is not a definition of the integers.** Section 6 proves that this very predicate accepts every rational input integral at the fixed preparation primes 2,7,29 (and in particular nonintegral inputs). An additional quotient-size bound is genuinely necessary; higher fixed precision, more fixed input contacts, or a larger fixed reference cutoff do not cure this construction. The current defining-polynomial variable bounds are unchanged.

## 1. Source functions and guards

Use ten distinct integer contacts \(\theta_\ell=\ell\), \(1\le\ell\le10\), and write
\[
 t=X^2+100,\qquad g(t)=\prod_{\ell=1}^{10}(t-\ell),\qquad u=g(t)>1.
\]
The constants here are a choice of this construction, not additional variables. Write \(v_p\) for the normalized rational valuation, with \(v_p(0)=+\infty\). Let \(K_0=100\), \(M_0=401\). Define the joint reference scalar
\[
 L=y(H)+u^{-M_0}.
\]
At an odd good prime, a point in the formal group of depth \(a=v_p(z(H))>0\), where \(z=-x/y\), has \(v_p(x(H))=-2a,\ v_p(y(H))=-3a\). Otherwise its affine coordinates are integral; for a nonformal point put \(a=0\). All point charts are the nonzero square-abscissa charts of v82.

For each of \(V=H,U\) put
\[
 Z_V=\frac{L^2}{x(V)^4},\qquad \chi_V=\frac1{1+Z_V}.
\]
Use a finite truncation of the formal logarithm,
\[
 \ell_R(z)=\sum_{r=0}^R
 \frac{(-1)^r\binom{2r}{r}2^r}{4r+1}z^{4r+1},
 \qquad R=N+4.
\]
The series follows by expanding the invariant differential
\(dz/\sqrt{1+8z^4}\) for the stated curve; compare the original carrier formula in [v111](../../../undecidability/direct_index_transfer_v111/README.md). At odd good primes, for a formal point of depth \(a\ge1\),
\[
 \ell_R(z)/\log_E(z)\in 1+p^{(N+4)a}\mathbb Z_p .
\]
Indeed, for every omitted index \(r\ge R+1\), its relative valuation is at least \(4ra-v_p(4r+1)\ge2ra\), since \(3^{2r}>4r+1\). The full logarithm is an isometry there. At two the denominators \(4r+1\) are odd and the same bound holds on sufficiently deep formal disks. Only sufficiently deep fixed-place witnesses are needed at the bad prime.

Define
\[
 F=\frac{\ell_R(z(U))/\ell_R(z(H))-X}{z(H)^N},
 \qquad T=\frac{F^2}{L^{-1}+F^2},\qquad
 C=1-\chi_H\chi_U(1-T).
\]
The actual pole input is
\[
 b=1+LC^2,\qquad e=\frac{112}{841}b.
\]
Require the BB product-pole equation
\[
 Y^2=(1-e)(v^4-e^2)(s^4-e^2)
\]
and all indicated divisions and \(e\) nonzero. In particular guard \(L,\ell_R(z(H)),z(H)\). The terminal root \(Y\) may be zero. All fixed exceptional primes in the primitive divisor and height results, the coefficient denominator primes of the logarithm, and \(2,7,29\) can be excluded in soundness; their set is independent of \(X,H,U\).

The local BB obstruction excludes negative odd valuations of \(e\), at every prime, even at zero terminal roots and zero pole parameters.

## 2. The single scalar forces a height-dominating reference

At every prime where \(v_p(L)\) is odd, each \(\chi_V\) is integral: the valuation of \(Z_V\) is \(2v_p(L)-4v_p(x(V))\), nonzero modulo 4. It is congruent to 1 if that valuation is positive, and to 0 if negative. Also \(T\) is integral and Boolean modulo \(p\), because the two summands of \(L^{-1}+F^2\) have different valuation parity (including \(F=0\)). Hence \(C\) is integral at such primes.

If \(v_p(L)<0\) is odd, the pole forces
\[
 v_p(C)>-\frac{v_p(L)}2
\]
outside the fixed scaling primes. For if \(C\ne0\) and the inequality fails, \(LC^2\) has negative odd valuation; adding 1 preserves it. For \(C=0\) the assertion holds with infinite valuation.

Consider a positive odd contact of \(u=g(t)\) outside the fixed exceptions, with \(\nu=v_p(u)>0\). If the depth \(a\) of \(H\) were less than \(K_0=100\), then
\[
 v_p(y(H))\ge-3a>-401\nu,
 \qquad v_p(L)=-401\nu.
\]
Moreover \(v_p(Z_H)\le-802\nu+8a<0\), so \(\chi_H\equiv0\pmod p\). Since all other factors of \(1-C\) are integral, \(C\equiv1\pmod p\), a contradiction to the pole. Thus **every positive odd contact of \(u\) forces \(a\ge100\)**, not just formality.

Let \(B_h\) be the positive reduced denominator of the square root of \(x([h]P)\), so \(x([h]P)=A_h^2/B_h^2\) with coprime integers \(A_h,B_h\). Let \(M(u)\) denote the product of all the positive odd contact primes of \(u\) outside the fixed exceptional set. The preceding implication gives
\[
 \log M(u)\le \frac{\log B_h}{100}
             \le\frac{q h^2}{100}+O(1).
\]
Under ordinary abc, the standard fixed split-polynomial simple/odd contact estimate used in v63 gives, at degree ten and \(\epsilon=1/100\),
\[
 \log M(u)\ge(10-4-2\epsilon)h(t)-O(1)
            =\frac{299}{50}h(t)-O(1).
\]
This is the finite-contact estimate for rational arguments, including nonintegral arguments. One way to obtain it is the truncated reduced-divisor inequality for the ten distinct finite roots, followed by \(2N^{(1)}\le N+N_{\rm odd}^{(1)}\) and \(N\le10h(t)+O(1)\). Equivalently the simple-prime estimate in v63 implies this bound. Fixed exclusions change only the additive constant. Thus
\[
 h(t)\le qh^2/598+O(1).
\]
For \(X=A/B\) reduced, \(X^2+100\) is reduced with denominator \(B^2\) and numerator \(A^2+100B^2\). Hence \(2h(X)\le h(t)\). Also \(h(u)\le10h(t)+O(1)\). In particular
\[
 h(X)\le qh^2/1196+O(1),\qquad
 2h(u)\le(10/299)qh^2+O(1).
\]
This is the new height-dominating relation. No height of \(U\) or its quotient index has been assumed.

## 3. The same pole gives exact divisibility and amplified congruences

The primitive-divisor mass theorem of v82, under ordinary abc, gives at least
\[
 \log Q_h\ge qh^2/5
\]
for sufficiently large \(|h|\), where \(Q_h\) is the product of exponent-one primitive denominator primes of \(H=[h]P\). The fixed bad primes may be removed at an additive constant cost. Remove also every prime where \(v_p(u)\ne0\); the sum of their logarithms is at most \(2h(u)\). For sufficiently large \(|h|\), the remaining product \(R_h\) therefore satisfies
\[
 \log R_h\ge(1/5-10/299)qh^2-O(1)
              \ge qh^2/7.
\]
The strict inequality \(1/5-10/299>1/7\) is essential. Enforce a fixed finite exclusion of the finitely many small nonzero reference indices, exactly as in v82, by a nonzero polynomial in the square abscissa of \(H\). The cutoff is ineffective.

At every prime of \(R_h\), \(H\) has formal depth one and \(u\) is a unit. Thus \(v_p(L)=-3\) and \(v_p(Z_H)=2\), giving \(\chi_H\equiv1\bmod p\). The pole forces \(v_p(C)\ge2\); the Boolean identities imply \(\chi_U\equiv1\), \(T\equiv0\bmod p\). In particular \(U\) is formal at this prime (an integral abscissa would give \(v_p(Z_U)\le-6\)). The reduction order of \(P\) is \(|h|\) by primitivity, so \(h\mid j\). Existence of one such prime suffices; the height estimate gives many.

Now \(m=j/h\) is an integer. At each of the remaining primes the actual formal logarithm ratio equals \(m\). The ratio of the truncated logarithms differs from \(m\) by an element of \(p^{N+4}\mathbb Z_p\), using the relative estimate and the integrality of \(m\). The condition \(T\equiv0\) forces \(2v_p(F)>3\), or \(v_p(F)\ge2\). Consequently
\[
 v_p(X-m)\ge N+2 .
\]
This also implies \(X\) is integral at these primes. If \(X\ne m\), their powers divide its nonzero reduced numerator:
\[
 (N+2)\log R_h\le\log|\operatorname{num}(X-m)|
                   \le h(X)+\log(1+|m|).
\]
Substituting the two established height inequalities proves the exponential lower bound in the theorem. The precision \(N\) is any fixed positive integer; increasing it only changes polynomial degree and fixed exceptions.

## 4. Ordered integer completeness and denominator parity

Fix an integer \(m=X\ne0\). Choose \(H\) sufficiently deep in the formal groups at every prime in the finite support of \(u\) and at all fixed preparation primes. Then set \(U=[m]H\). These choices are possible by taking \(h\) divisible by a suitable fixed modulus (for this input). At two, seven and 29 require large depth at the outset. Choose the real value of \(H\) in a compact arc around \(-P\) with \(0<y(H)<3\), shrinking it if necessary to avoid the finite zero set of \(\ell_R(z(H))\). This zero set is finite since \(\ell_R\) is nonzero and \(z\) nonconstant. Real recurrence in the identity component gives arbitrarily large \(h\) satisfying both requirements. All guards can be met on this arc: \(u>1,L>0,x(H)x(U)\ne0\), \(L^{-1}+F^2>0\), and the other denominators are positive or explicitly guarded.

At a formal prime of \(H\), with depth \(a>0\), true multiplication gives depth of \(U\) at least \(a\). At a prime dividing \(u\), the initial depth was chosen so that \(y(H)\) dominates \(u^{-M_0}\); elsewhere the same domination is automatic. Hence \(v_p(L)=-3a\) and \(v_p(Z_H),v_p(Z_U)\ge2a\). At a good odd prime the truncated logarithm ratio differs from \(m\) by a value of valuation at least \((N+4)a\). At bad/fixed primes the sufficiently deep initial choices give the same assertion. Thus \(v_p(F)\ge4a\), \(v_p(T)\ge5a\), and \(v_p(C)\ge2a\), proving \(v_p(b-1)\ge a\). In particular \(b\) is a unit at every formal prime. The same argument covers a zero error.

At any other prime \(H\) is nonformal. Since all primes of \(u\) were among the formal primes of \(H\), \(L\) is integral there. If \(v_p(L)\) is even, a negative valuation of \(b=1+LC^2\) is even. If \(v_p(L)\) is odd, the previously proved parity rules make \(C\) integral, so \(b\) is integral. This proves that the actual \(b\) has square reduced denominator, including every foreign prime of the actual point data. At seven \(b\) is a unit; at 29 the scaling has even valuation \(-2\). At two \(b\equiv1\bmod8\), and therefore \(e\in7\mathbb Q_2^{\times2}\) with \(v_2(e)=4\).

Really \(0<L<4\), \(0<\chi_V<1\), \(0\le T<1\), so \(0<C<1\) and \(1<b<5\). Hence \(0<e<560/841<1\). The actual input \(e\) is prepared, and the BB theorem supplies \(v,s,Y\) without further point or prime choices. This is the desired ordered completeness.

## 5. Six-coordinate coefficient recipe

Use the two square-abscissa charts \(H=(g_H^2,g_H\eta_H)\), \(U=(g_U^2,g_U\eta_U)\) with \(\eta_H^2=g_H^4-2,\eta_U^2=g_U^4-2\). Retain \(X,g_H,g_U,v,s\) and one finite encoder coordinate. Compute the displayed rational functions by numerator-denominator pairs, impose their nonzero selected-character guards and the finite reference cutoff. For the terminal square radicand \(A/B\) adjoin the monic root \(Y_*^2=AB\) and recover \(Y=Y_*/B\) at the selected character. The finite free algebra has rank eight. Apply the [selected-character determinant](../../../undecidability/papers/joint_finite_algebra_encoder.tex) to all guards and generators and clear fixed rational denominators. This is a finite exact coefficient prescription with six total ordinary coordinates. It does not require all geometric characters to satisfy the guards, and zero terminal roots are allowed. There is no numerical degree ceiling or effective sufficient reference cutoff claimed.

## 6. Explicit obstruction to interpreting the new predicate as an integer definition

The exponential lower bound is a genuine restriction on incorrect quotients, but is not a contradiction. In fact let \(X\) be any rational number integral at \(2,7,29\). There are accepted tuples for this \(X\) with arbitrarily large positive \(h\).

Fix \(X,t,u\). At every prime of the support of \(u\), every fixed preparation prime and every denominator prime of \(X\), choose \(H\) sufficiently deep. At denominator primes of \(X\) prescribe the formal depth to be **even**. This is possible simultaneously: after entering sufficiently deep formal subgroups, for every such fixed prime the depth of \([r]H_0\) equals the original depth plus \(v_p(r)\), by the isometric formal logarithm. Prescribe \(v_p(r)\) to be sufficiently large with the required parity, using ordinary integer CRT, and impose deep neighborhoods at all other fixed places. In particular this is a nonempty congruence progression on indices. At each of those primes the depth can be made sufficient for \(y(H)\) to dominate \(u^{-M_0}\).

Choose \(H\) in the same real arc as Section 4, avoiding the finitely many excluded indices and zeros. **Now fix \(H\)**. Its actual formal-prime set is finite, including any foreign denominator primes. At each such prime where \(a=v_p(z(H))\) is odd and \(X\) is integral, choose an integer \(m\) satisfying \(v_p(m-X)\ge(N+4)a\); at the fixed preparation primes impose this even if \(a\) is even. These finitely many ordinary rational-prime congruences are independent by CRT. Choose a nonzero integer \(m\) in the resulting progression, and set \(U=[m]H\).

At every formal prime of odd depth the same calculation as Section 4 gives \(v_p(F)\ge4a\) and \(v_p(b-1)\ge a\), because the truncated logarithm ratio approximates \(m\) and \(m\) approximates \(X\) to the prescribed precision. No denominator prime of \(X\) belongs to this odd-depth list. At each formal prime of even depth, \(v_p(L)=-3a\) is even, so any negative valuation of \(b\) is automatically even, regardless of the error. At the fixed preparation primes, \(X\) is integral and the imposed congruences give the required unit/real preparation as in Section 4. At every nonformal prime, \(L\) is integral because the support of \(u\) was included in the initial formal places; the same parity argument applies without any approximation requirement. The real inequalities again make \(0<e<1\), independently of \(m\). Thus \(e\) is prepared and the BB theorem completes a rational solution.

For a nonintegral \(X\), these quotients are not equal to \(X\); they must satisfy the exponential lower bound. The construction makes them large by CRT and does not contradict that bound. This proves an actual false-positive theorem for the six-coordinate source, not merely a numerical compatibility of inequalities.

Consequently any attempt to complete this approach must supply an additional relation **excluding exponentially large quotients while still admitting \(U=[m]H\) for arbitrarily large references at every fixed integer \(m\)**. In particular, if such a relation with no more than three additional ordinary rational coordinates and one shared finite encoder is proved, and if it guarantees \(\log(1+|j/h|)\le C qh^2+O(1)\) for a fixed \(C\), choose \(N\) large enough that \((N+2)/7-1/1196>C\); then increase the fixed reference cutoff. The resulting relation would define all nonzero integers, with zero added by a polynomial factor. The hypothetical count would be at most nine. The required growth relation is not established here; it cannot be replaced by local congruences at finitely many actual reference primes.

## Scope and attribution

The primitive denominator input and rank-one rational chart are from the project's v82 EDS construction; the local logarithm truncation and fixed contact-height inputs are the v111/v63 arguments. The terminal pole uses Bhargava--Burungale, arXiv:2611.16130v2. The merged scalar \(L=y(H)+u^{-401}\), height forcing by depth 100, removal of the foreign input-contact primes, precise quotient comparison, and false-positive proof are new. The fixed constants are selected here for convenient strict margins, not claimed optimal. The proof uses ordinary rational abc and not a weaker modular height substitute: the logarithmic primitive-prime mass and input-contact estimate are indispensable in the stated quantitative conclusion. No new defining-polynomial record or quartic count follows.
