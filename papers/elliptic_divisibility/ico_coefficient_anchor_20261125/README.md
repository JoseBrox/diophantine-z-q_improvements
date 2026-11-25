# One-coordinate interpolation and a fully rational eight-coordinate cap

## Result and scope

This continues the [optimal ico interpolation](../ico_boundary_interpolation_20261125/README.md) and the [adaptive shared height anchor](../adaptive_joint_quotient_20261124/README.md).

There are three new deductions.

1. One of the two mixed coefficients of the degree-fifteen form is a rational function of the other coefficient and the plane chart. Thus the mixed-domain construction needs only eight ordinary coordinates, not nine. This eliminates a variable, not the two localized-integer requirements.
2. The adaptive height anchor can be applied to the input and both mixed coefficients while comparing just the input to the hidden integer quotient. This gives a fully rational eight-coordinate polynomial relation, with a **proved uniform numerical denominator budget** and soundness for the rational input under the retained ordinary rational abc and other arithmetic hypotheses. It requires no integrality predicate on either coefficient.
3. At a fixed numerator coordinate and a fixed allowed prime set, all guarded boundary-controlled lifts lie in an explicit two-term S-unit equation. This reduces fixed-reference existence to a finite decision problem.

The second result is a sufficient alternative to the desired coefficient-support condition, not an exact definition of membership in a prescribed localized integer ring. It is **not** a complete definition of the integers. In particular we do not assert that the new adaptive coefficient-height constraints admit even all old true witnesses. The remaining ordered completeness issue is stated precisely below. The companion [Szpiro obstruction](../../../negative_results/papers/elliptic_divisibility/ico_szpiro_obstruction_20261125.md) gives a fundamental reason for caution about general completeness of the boundary-controlled ico approach.

## 1. Eliminate the second mixed coefficient

Use the guarded chart \(Z=Z(w,t)\) of the ico surface \(\sigma_2=\sigma_4=0\) from the [exponential cap](../ico_exponential_cap_20261125/README.md). All its projective coordinates are nonzero. Write
\[
 D=\sigma_1(Z)^{15},\qquad A=\sigma_3(Z)^5,\qquad C=\sigma_5(Z)^3.
\]
In particular \(C\ne0\). For the interpolation
\[
 D+aA+bC=0
\]
one may use the single free coefficient \(a\) and the computed rational function
\[
                         b=-\frac{D+aA}{C}.                 \tag{1}
\]
This identity holds on the full guarded chart, including \(A=0\) or \(D=0\); there is no new genericity condition. For any finite rational-prime set \(S\), the previous Bezout proof gives
\[
 \operatorname{supp} B(Z)\subseteq S
 \quad\Longleftrightarrow\quad
 \exists a\in\mathbb Z[S^{-1}]\ \text{with }b\in\mathbb Z[S^{-1}].
\]
Here \(B(Z)\) is the intrinsic coordinate-point reduction radical, and the right-hand \(b\) is the function (1). We still need two ring-membership conditions on rational functions; we have eliminated only the free coordinate for \(b\).

More generally, let \(d_0\) be the positive least common denominator of \(a,b\) (used only in the proof). Then the integral homogeneous form
\[
 d_0\sigma_1^{15}+(d_0a)\sigma_3^5+(d_0b)\sigma_5^3
\]
has all five diagonal coefficients \(d_0\ne0\). The minimal-radical theorem gives
\[
 \log B(Z)\le \log\operatorname{rad}(d_0)
       \le \log d_0\le h_{\rm W}(a)+h_{\rm W}(b).             \tag{2}
\]
Here and throughout \(h_{\rm W}\) is logarithmic Weil height, with \(h_{\rm W}(0)=0\). The variables \(b,d_0,A,C,D\) need not be retained as ordinary coordinates in an unrestricted-degree construction.

## 2. An actual rational denominator-budget certificate

Use the same cyclic square-abscissa chart on
\[
 E:y^2=x^3-2x,\qquad P=(9/4,-21/8),\quad q=\widehat h(P)>0.
\]
The ordinary variables are
\[
        X,\ g_H,\ g_U,\ t,\ a,\ v_1,\ v_2,\ \text{encoder}.
\]
Here \(H=[h]P,U=[j]P\) are nonidentity points, \(g_H^2=x(H),g_U^2=x(U)\); the finite roots encode the ordinates as in the six-coordinate source. Take \(w=g_U\) in \(Z(w,t)\), guard the plane chart, and compute \(b\) by (1).

In the recursive scalar anchor take the list of **three** rational arguments
\[
       x_1=X,\quad x_2=a,\quad x_3=b .
\]
These arguments are not assumed integral. Use
\[
 f(T)=\prod_{i=1}^{10}(T-i),\quad \phi(W)=W/(1+W)^2,\quad S_0=1,
\]
\[
 W_i=S_{i-1}x_i^2,\quad T_i=100+\phi(W_i),\quad
 S_i=S_{i-1}f(T_i)/f(100),\quad u=\phi(S_3).
\]
Fix \(K=16000\), put \(L=y(H)+u^{-(4K+1)}\), and use \(Z_V=L^2/x(V)^4,\ \chi_V=(1+Z_V)^{-1}\) for \(V=H,U\).
Write \(z=-x/y\). For fixed precision \(N=1\), or any larger fixed precision, use the original polynomial logarithm truncation of order \(N+4\) in its series index, denoted by \(\ell\), and put
\[
 F=\frac{\ell(z(U))/\ell(z(H))-X}{z(H)^N},\quad
 T_F=\frac{F^2}{L^{-1}+F^2},\quad
 C_{\rm pole}=1-\chi_H\chi_U(1-T_F).
\]
Guard all denominators. The comparison tests involve **only \(X\)**, not the two coefficients. Impose the old BB equation
\[
 e=\frac{112}{29^{2d}}(1+LC_{\rm pole}^2),\quad e\ne0,\qquad
 Y^2=(1-e)(v_1^4-e^2)(v_2^4-e^2),
\]
where \(d\) is any fixed positive integer with
\[
                    29^{2d}>112(4+11^{4K+1}).
\]
The variables here have the same meanings as in the prepared class-seven pole theorem used in the parent construction. All its arithmetic hypotheses are retained, as are ordinary rational abc, the doubled-point simple-denominator mass theorem, and Fan--von Kanel's ico height theorem.

### Soundness of the coefficient budget

For real rational arguments, \(1\le S_3\le8\) and \(4\le u^{-1}\le11\). At every positive odd contact prime of \(f(T_i)\) outside a fixed finite exceptional set, the recursive persistence calculation of the adaptive anchor forces \(v_p(u)>0\) odd. Indeed a previous odd valuation of \(S_{i-1}\) makes \(v_p(W_i)\) odd (when \(x_i\ne0\)); hence \(\phi(W_i)\) is small at that prime and \(f(T_i)/f(100)\) is a unit. If \(x_i=0\) the same update is one. At a new odd contact, the previous valuation had to be even. This proves persistence through the three updates and the final application of \(\phi\).

For a prime with \(v_p(L)\) odd, all \(\chi_V,T_F\) and \(1-T_F\) are integral with Boolean residues. If \(v_p(L)<0\) odd outside the scaling primes, the pole obstruction implies
\[
 v_p(C_{\rm pole})>-v_p(L)/2.
\]
This proof uses only the single comparison test present here. At an odd positive contact of \(u\), if the formal depth of \(H\) were below \(K\), the scalar term in \(L\) would dominate with negative odd valuation and \(\chi_H\) would have zero residue. Then \(C_{\rm pole}\equiv1\), impossible. Thus each odd contact prime has reference depth at least \(K\), regardless of the values of the coefficient arguments.

Let \(H_*=qh^2\). With \(\gamma=299/50\) the ordinary-abc contact height inequality used in the adaptive anchor gives
\[
 h_{\rm W}(T_i)\le H_*/(\gamma K)+O(1).
\]
The rational-map height inequalities of that construction give
\[
\begin{split}
 2h_{\rm W}(u)+\sum_{i=1}^3 h_{\rm W}(x_i)
 &\le \frac{40\cdot3+3/4+5\cdot3\cdot2/2}{\gamma K} H_*+O(1)\\
 &=\frac{543}{382720}H_*+O(1)
 \le \frac{1}{100}H_*+O(1).                                 \tag{3}
\end{split}
\]
For clarity, this uses \(h_{\rm W}(S_i)\le 10\sum_{l\le i}h_{\rm W}(T_l)+O(1)\), \(h_{\rm W}(u)\le2h_{\rm W}(S_3)+O(1)\), and
\(2h_{\rm W}(x_i)\le h_{\rm W}(W_i)+h_{\rm W}(S_{i-1})\le h_{\rm W}(T_i)/2+h_{\rm W}(S_{i-1})+O(1)\). The latter follows from the reduced fraction identity for nonnegative \(W_i\): \(h_{\rm W}(\phi(W_i))=2\log(\operatorname{num}(W_i)+\operatorname{den}(W_i))\ge2h_{\rm W}(W_i)\). The case \(W_i=0\) also holds. All constants are independent of the arguments and the point indices. In particular the reasoning applies to the rational function \(b\) without using integrality of either coefficient.

Combining (2) and (3) gives the actual support budget
\[
                     \log B(Z)\le H_*/100+O(1).              \tag{4}
\]
It is not just a bound on an auxiliary scalar defined by unrelated coefficients. We have used precisely the integral form obtained from the computed coefficient \(b\) and the free coefficient \(a\).

### Soundness of the input

The intrinsic ico bound from the previous interpolation proof and the inverse chart height inequality imply
\[
  \log(1+h_{\rm W}(g_U))\le24\log B(Z)+O(1)
                       \le(6/25)H_*+O(1).
\]
Since \(h_{\rm W}(g_U)=qj^2+O(1)\) and \(|h|\ge1\), it follows that
\[
                  \log(1+|j/h|)\le(3/25)H_*+O(1).          \tag{5}
\]

For the simultaneous divisibility argument remove the fixed bad primes and support of \(u\) from the simple denominator primes of \(H\). By (3), the remaining squarefree product \(R_H\) has \(\log R_H\ge(9/10)H_*\) beyond a fixed absolute reference-index cutoff. At each such prime \(v_p(L)=-3\), the pole forces the numerator point \(U\) to be formal, and the sole test gives \(X\equiv j/h\bmod p^{N+2}\) once the divisibility is proved. For completeness of this deduction, formality of \(H,U\) implies \(R_H\) divides the square-root denominator at the index \(\gcd(h,j)\). If this gcd were smaller than \(|h|\), its denominator height would be at most \(qh^2/4+O(1)\), a contradiction. Thus \(m=j/h\in\mathbb Z\). The formal logarithm ratio is exactly \(m\), and its polynomial truncation differs by an element of \(p^{N+4}\mathbb Z_p\) at a simple denominator prime. Boolean success implies \(v_p(F)\ge2\), giving the stated comparison.

If \(X\ne m\), the numerator of \(m-X\) is divisible by \(R_H^{N+2}\). Using (3) gives
\[
       \log(1+|m|)\ge
           ((9/10)(N+2)-1/100)H_*-O(1).
\]
Already \(N=1\) gives \(269/100>3/25\). Beyond a single fixed reference-index cutoff this contradicts (5). Every actual solution therefore has \(X=m\in\mathbb Z\). The cutoff may be ineffective, just as in the parent. The positive margin and the height estimate hold for arbitrary signs of the retained rational square roots.

### Coordinate and completeness accounting

All new plane and coefficient expressions and the scalar anchor are rational functions in the six original ordinary variables and \(t,a\). The finite point and pole characters, zero residuals and nonzero guards are handled by the same rank-eight selected-character determinant as the parent. Thus clearing denominators gives an eight-coordinate integer polynomial relation with input projection contained in \(\mathbb Z\). Zero may be added by multiplying by \(X\) if desired. No explicit degree bound or nonzero witness for each integer follows from this argument.

An actual sufficient completeness condition is the following: for each nonzero integer \(m\), find one \(H=[h]P\) beyond the fixed cutoff, set \(U=[m]H\), and find \(t,a\) in the guarded chart such that the reference is sufficiently deep at 2, 7, 29 and at **every prime of the support of the computed \(u(X,a,b)\)**. More precisely, at every support prime require formality and \(3v_p(z(H))>(4K+1)v_p(u)\), with the usual fixed-place deep logarithm conditions; require also \(0<y(H)<3\) and the real guards of the parent. These conditions suffice: at every formal prime \(y(H)\) dominates the scalar term, both points are formal, and the original logarithm estimate gives \(v_p(C_{\rm pole})\ge2v_p(z(H))\). At other primes \(L\) is integral, and the parity proof applies. The fixed scaling and real inequality then prepare the actual BB scalar.

The order of choices matters. One cannot take an arbitrary parent witness, compute coefficients \(a,b\) afterwards, and then choose the same reference deeper at the new support primes without changing \(U,Z,a,b\). Nor does the Bezout interpolation control coefficient heights sufficiently to imply (3) for a preselected reference. We have not found the simultaneous lifts meeting the above condition. Even an unrestricted off-diagonal choice with genuinely S-integral coefficients does not automatically give this stronger adaptive preparation. The new relation thus resolves the **soundness budget** part with eight variables, not all-integer completeness and not literal exact \(S\)-integrality.

## 3. Finite fixed-reference reduction to an S-unit equation

Fix \(w\in\mathbb Q\setminus\{0,1\}\) and a finite allowed prime set \(S\). Write
\[
 R(w)=\prod_{p:\ v_p(w)\ne0\ {\rm or}\ v_p(1-w)\ne0}p,
 \qquad S'=S\cup\{p:p\mid R(w)\}.
\]
Suppose \(t\) is a guarded lift of \(w\) with boundary radical supported in \(S\). Then
\[
                  t,\ 1-t\in\mathbb Z[S'^{-1}]^\times.     \tag{6}
\]

Indeed outside \(S'\), both \(w\) and \(w-1\) are units. Use the factored chart polynomials from the interpolation theorem,
\[
 a_0=(t-1)(wt+w-1),\quad a_1=-(w-1)((w+1)t-1),\quad
 a_2=-w(t^2+w-1),\quad a_3=-(t-w)(t+w-1),\quad
 A=-t(t+w^2-1).
\]
The normalized point is \((-A/a_0:-A/a_1:-A/a_2:-A/a_3:1)\).

* If \(v_p(t)<0\), the four values \(a_0,a_2,a_3,A\) have valuation \(2v_p(t)\); \(v_p(a_1)\ge v_p(t)>2v_p(t)\). The second normalized coordinate is the unique pole, so reduction is a coordinate point.
* If \(v_p(t)>0\), all \(a_i\) are units and \(v_p(A)>0\), making the fifth coordinate the unique unit.
* If \(v_p(1-t)>0\), only \(a_0\) among \(A,a_0,\ldots,a_3\) has positive valuation, again giving a coordinate-point reduction.

All three cases contradict the support assumption. This proves (6) including the case \(w+1\equiv0\bmod p\). The guards already exclude \(t=0,1\).

Swapping \(w,t\) preserves \(B(Z)\) and the guarded chart: the ordered tuple \((a_0,a_1,a_2,a_3,-A)\) becomes \((-a_1,-a_0,A,-a_3,-a_2)\), the negative of a permutation. Its reciprocal projective vector is exactly \(Z\) up to projective scaling. The inverse guard in the swapped chart follows from \(A'=t'(a_0'+a_2')\ne0\). Consequently
\[
 \operatorname{supp} R(t)\setminus\operatorname{supp} B(Z)
   =\operatorname{supp} R(w)\setminus\operatorname{supp} B(Z).
\]
Thus (6) gives a necessary, symmetric constraint, independent of the choice of off-diagonal coefficients.

For a **fixed** reference and multiplier and any fixed allowed set \(S\), the existence of a lift with support in \(S\) can be decided by solving the two-term S-unit equation \(x+y=1\) over \(S'\) and filtering its solutions \(x=t,y=1-t\) by the guards and the exact boundary gcd test. The S-unit requirement is not sufficient by itself. Alternatively the effective ico height bound gives a completely explicit finite enumeration without an S-unit solver: set \(B_S=\prod_{p\in S}p\); the inverse height inequality gives \(h_{\rm W}(t)\le8\cdot 10^{10^{12}}B_S^{24}+\log6\). Enumerate coprime numerator-denominator pairs up to the exponential of this bound and test the same guards and gcd. The search is finite but generally infeasible. Neither procedure supplies a uniform existence theorem as the integer multiplier varies. The polynomial bound on references from the earlier bounded-reference paper concerns the parent and is not an upper bound on the first reference admitting this new lift.

Under ordinary rational abc, the S-unit implication also yields the necessary inequalities
\[
 h_{\rm W}(t)\le\kappa(\log B(Z)+\log R(w))+O_\kappa(1),
 \qquad
 h_{\rm W}(w)\le\kappa(\log B(Z)+\log R(t))+O_\kappa(1)
\]
for each fixed \(\kappa>1\). For example \(\log R(w)\le3h_{\rm W}(w)+\log2\), by using a reduced pair \(w=A_w/B_w\) and bounding the prime support of \(A_w B_w(A_w-B_w)\). These inequalities do not imply a uniform bound of \(h_{\rm W}(w)\) in terms of \(\log B(Z)\) alone.

## Conclusion

The old two-coefficient support gap has a new eight-coordinate **sound rational replacement**, as well as an exact fixed-fiber arithmetic characterization. General completeness of that replacement or of the earlier mixed-domain system remains unproved. No current defining-polynomial bound changes. The [companion obstruction](../../../negative_results/papers/elliptic_divisibility/ico_szpiro_obstruction_20261125.md) shows that a complete uniform boundary budget would even contradict a standard higher-dimensional height conjecture. The exact checks concern the finite algebra, valuations and height-budget constants, not the conjectural arithmetic inputs or general witness existence.
