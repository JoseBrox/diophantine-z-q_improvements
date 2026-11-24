# Polynomially bounded true references for the height-anchored quotient

## Statement

In the [six-coordinate quotient construction](../height_anchored_quotient_20261124/README.md), retain the rational cyclic chart and the prepared BB pole theorem. Fix its precision \(N\ge1\) and any required fixed lower cutoff on the absolute reference index. For **every** nonzero integer input \(m\), there are true witnesses \(H=[h]P,\ U=[mh]P\), with
\[
 0<|h|\le C_N(1+|m|)^{8100}.
\]
The constant may depend on the fixed cutoff and precision but not on \(m\). The statement permits signed reference indices; the original source has no positivity guard on \(h\). It improves the original qualitative completeness construction for the purpose of choosing a bounded reference. It does not restrict the false witnesses of that construction.

Put \(q=\widehat h(P)>0\), and use \(h_{\rm W}\) for logarithmic height. On these true witnesses one may moreover choose the rational conic charge of the [one-conic construction](../one_conic_foreign_charge_20261124/README.md) so that
\[
 \log(1+h_{\rm W}(g_U)),\quad \log(1+h_{\rm W}(s))
 \ \le\ 16202\,h_{\rm W}(m)+O_N(1).
\]
Here the charge is the new conic coordinate, not the second parameter of the BB pole. Thus even an exponential cap in the **input height alone** has a sufficient numerical budget for some true witnesses. No Diophantine constraint realizing that budget on all solutions is asserted.

## 1. A polynomially bounded finite-place progression

Use the parent notation
\[
 u=\prod_{\ell=1}^{10}(m^2+100-\ell),\quad M_0=401,\quad
 L=y(H)+u^{-M_0}.
\]
For integral \(m\), \(u\) is a positive integer of degree twenty in \(m\).
Let \(S\) be a fixed finite set including the bad primes, \(2,7,29\), and the fixed exceptions and coefficient denominators required by the parent at precision \(N\). Choose a fixed integer \(D_*\) such that every nonzero multiple of \(D_*\) gives a point in a sufficiently deep formal subgroup at every prime of \(S\). This is possible by the finite-index formal subgroups of the local elliptic groups; on a sufficiently deep disk the logarithm is an isometry. Include depth at least three at two, and take \(D_*\) larger than the fixed absolute-index cutoff. No uniform effective bound on this last cutoff is claimed.

For each \(p\mid u\) outside \(S\), let \(r_p\) be the order of the reduction of \(P\). Put
\[
 D=D_*\,u^{401}\prod_{\substack{p\mid u\\p\notin S}}r_p .
\]
For a nonzero index divisible by \(D\), \(H\) is formal at each such \(p\), of depth at least \(1+401v_p(u)\). Indeed \([r_p]P\) is formal at the good odd prime \(p\), and multiplying a formal point adds the valuation of the integer multiplier to its depth. At a prime in \(S\) dividing \(u\), the same conclusion with the fixed initial deep depth follows by first entering the deep subgroup using \(D_*\). Therefore \(y(H)\) strictly dominates \(u^{-401}\) in valuation at all these primes. At any other formal prime the domination follows from \(u\) being a unit.

By Hasse, \(r_p\le p+1+2\sqrt p\le p^3\) for every \(p\ge2\); the elementary last inequality follows from \(2\sqrt p\le p+1\). Consequently
\[
 D\le D_*u^{404}\ll_N(1+|m|)^{8080}.
\]
This construction of the progression depends on the integer input, and no simultaneous tailored-prime supplier is needed.

## 2. Real preparation near the identity instead of a fixed arc

We keep every rational function of the original source. In particular, with \(z=-x/y\), \(R=N+4\), and the polynomial \(\ell_R\) of the parent,
\[
 Z_V=L^2/x(V)^4,\quad \chi_V=(1+Z_V)^{-1},\quad
 F=\frac{\ell_R(z(U))/\ell_R(z(H))-m}{z(H)^N},\quad
 T=\frac{LF^2}{1+LF^2},
\]
\[
 C=1-\chi_H\chi_U(1-T),\qquad b=1+LC^2,\qquad e=112b/841 .
\]
Instead of choosing the real reference in an arc where \(y(H)\) is bounded, choose \(H\) on the \(y>0\) side of a sufficiently small real neighborhood of the identity. Write \(z_0=z(H)\) and \(M=1+|m|\). We prove that the requirement
\[
 0<|z_0|\le c_N M^{-20},\qquad z_0<0
 \tag{1}
\]
suffices, with a fixed sufficiently small positive constant \(c_N\).

In the real local parameter at the identity the analytic elliptic logarithm \(\ell\) has derivative one, \(\ell(z)=z+O(z^5)\), and
\[
 \ell_R(z)/\ell(z)=1+O_N(|z|^e),\qquad e=4(R+1)=4N+20.
\]
This is the ordinary convergent real Taylor series at the identity; it follows from the same invariant differential as the parent's formal logarithm. The letter \(e\) in this local Taylor estimate denotes an exponent, not the pole scalar. Denote this exponent instead by \(d=4N+20\) in the remaining estimates.

Take \(c_N\) small enough that the local real logarithm and its inverse exist on fixed neighborhoods and that the entire multiplication by \(m\) is inside the logarithm neighborhood: the product \(|m\,\ell(z_0)|\) is small by (1). In particular \(U=[m]H\) satisfies
\[
 \ell(z(U))=m\ell(z_0),\qquad |z(U)|\ll M|z_0|.
\]
The constants are independent of \(m,z_0\) in this range. Since \(x(z)\sim z^{-2},y(z)\sim-z^{-3}\),
\[
 0<L\ll |z_0|^{-3},\quad Z_H\ll |z_0|^2,\quad
 Z_U\ll M^8 |z_0|^2 .
\]
Also \(\ell_R(z_0)\ne0\). By the relative Taylor estimates and the exact logarithm ratio,
\[
 |F|\ll_N M^{d+1}|z_0|^{d-N},\qquad
 0\le T\le LF^2\ll_N M^{2d+2}|z_0|^{2(d-N)-3}.
\]
For every \(N\ge1\), \(20(2(d-N)-5)\ge2d+2\). Hence (1) implies \(T\ll_N |z_0|^2\). For positive \(L\) the quantities \(Z_V,T\) are nonnegative, \(\chi_V\) lies in \((0,1]\), and
\[
 0\le C\le Z_H+Z_U+T\ll_N M^8|z_0|^2.
\]
Therefore
\[
 0\le b-1\ll_N M^{16}|z_0|\ll_N c_N M^{-4}.
\]
Shrinking \(c_N\) gives \(1\le b\le2\), which is more than sufficient for \(0<112b/841<1\). Every real denominator of the source is now nonzero. The square-abscissa chart and the nontorsion group ensure that both \(H\) and \(U\) are nonidentity points of nonzero abscissa and ordinate.

## 3. Dirichlet approximation in the progression

The identity component of the real elliptic group is a circle, with angle normalized modulo one. The point \(P\) is in this component because it is doubled. Its angle is irrational since \(P\) is nontorsion. For the angle of \([D]P\), Dirichlet approximation, or the pigeonhole proof of that theorem, gives an integer \(1\le k\le Q\) with distance of \(k\) times that angle from an integer at most \(1/Q\).

Choose \(Q=\lceil A_N M^{20}\rceil\) with a sufficiently large fixed \(A_N\); the local parameter \(z\) is Lipschitz in the real angle near the identity. The approximation is not the identity, and replacing \(kD\) by its negative if necessary gives the side with \(z_0<0\). Thus \(h=\pm kD\) satisfies (1) and
\[
 0<|h|\ll_N M^{8080+20}=M^{8100}.
\]
The choice still lies in the exact finite-place progression and meets the fixed absolute-index cutoff. This argument does not require a quantitative inhomogeneous rotation estimate for an arc far from the identity.

## 4. Completion of all finite places and the pole

On this actual true pair \(H,U\), the finite-place completeness proof in Section 4 of the parent applies verbatim. For clarity, at every formal prime of \(H\), of depth \(a\), the ordinate dominates the scalar term by Section 1. The true multiple \(U=[m]H\) has depth at least \(a\). The parent's logarithm truncation estimates give \(v_p(F)\ge4a\), \(v_p(T)\ge5a\), \(v_p(C)\ge2a\), and hence \(v_p(b-1)\ge a\). This includes the sufficiently deep fixed bad places. All primes dividing \(u\) are already among those formal places. At a nonformal prime of \(H\), \(L\) is integral; if its valuation is even, any pole of \(b=1+LC^2\) has even valuation, and if its valuation is odd the parent parity calculation makes \(C\) integral. Therefore \(b\) has square reduced denominator, is a unit at seven, and is \(1\bmod 8\) at two. The fixed scaling gives a square reduced denominator for \(e=112b/841\), \(v_2(e)=4\), and two-adic squareclass seven. Section 2 gave \(0<e<1\).

Apply the same BB prepared-pole theorem to this actual input. No change of \(H,U\) or additional local approximation of the BB witnesses is required. This proves the stated true-reference theorem with the original coordinate count.

Finally the canonical height comparison gives
\[
 h_{\rm W}(g_U)=q m^2h^2+O(1),\qquad
 h_{\rm W}(g_H)=q h^2+O(1).
\]
For the charge conic \(r^2=1+(g_U/g_H^2)s^2\), set \(L_c=g_U/g_H^2\). Taking conic parameter \(t=1\) if \(L_c\ne1\) and \(t=2\) otherwise, the explicit parametrization \(s=2t/(1-L_ct^2)\) gives \(s\ne0\), and \(h_{\rm W}(s)\le h_{\rm W}(L_c)+O(1)\). Both heights are \(O_N(M^{16202})\). Taking logarithms gives the stated budget, because \(\log M\le h_{\rm W}(m)+\log2\).

## Scope and relevance to the new cap

The numerical exponents are conservative, not optimal. The argument uses ordinary real Dirichlet approximation, the explicit finite-place progression, and the same prepared-pole and chart assumptions as the old construction. It is a completeness-side upper bound on **chosen** witnesses, not a bound on all solutions. In particular it neither supplies rational points on the additional [ico cap](../ico_exponential_cap_20261125/README.md) nor contradicts its finiteness of true references for large fixed multipliers. It shows why abandoning arbitrarily-large-reference completeness in favor of at least one suitably bounded reference per integer is a viable change of strategy for the old source, provided an additional cap can be realized at such a reference.