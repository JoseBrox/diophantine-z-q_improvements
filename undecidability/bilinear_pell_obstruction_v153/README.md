# v153: global obstruction to fixed bilinear Pell certificates

The affine obstruction of [v151](../shared_pell_global_obstruction_v151/README.md) extends to every bare fixed integer bilinear certificate
\[
 L=\lambda hj+\mu h+\nu j+\xi\in\mathbb Z,\qquad
 \lambda,\mu,\nu,\xi\in\mathbb Z,\quad\lambda\ne0.
\]
In particular it applies to the product \(hj\), products of shifted quotients and sum-plus-product certificates. **The two Pell ordinates may both be nonintegral on every false packed instance**, even with this single certified integer, every retained norm and the actual triangular margin witnesses. No new arithmetic assumption is used. This is not a no-go theorem for higher-degree nonlinear certificates or for additional genuine arithmetic constraints.

## 1. Ensure distinct squareclasses

Use the notation and the modified congruences of v148/v150. Fix a false packed prefix with \(b\) a power of two, \(r\ge3\), and the other hypotheses of v151. (The actual cofinite packed prefixes have \(r\gg3\).) Put \(B=2r+1\), \(w=2^B/b\), \(U=wM\), and now allow the positive integer \(s\) to vary. Then
\[
 a=A_0s,\quad A_0=(U+1)rM,\qquad
 P=1+P_0s^2,\quad P_0=2Ur^2M^2,\qquad
 A=P^2-1 .
\]
Here \(P_0\) is a positive scalar constant, not the project's elliptic reference point. Write \(c(s)=Y_B(A_0s)\), with \(Y_n\) the integer Pell polynomial (\(Y_1=1,\ Y_2=2X,\ Y_{n+1}=2X Y_n-Y_{n-1}\)). Its \(2r\) roots are distinct: they are the scaled roots \(\cos(k\pi/B)/A_0\) of the Chebyshev polynomial of the second kind, \(1\le k<B\). Since \(2r>4\) and \(A(s)\) has degree four, some irreducible factor \(f\) of \(c(s)\) over \(\mathbb Q\) does not divide \(A(s)\).

Choose an odd prime \(\ell\) outside the fixed prime supports of coefficients needed for the factorization, discriminants and resultants (including the resultant of \(f\) with \(A\)) and dividing a nonzero value of a primitive integral representative of \(f\). Such a prime exists by Schur's elementary argument: if all nonzero values of a nonconstant integer polynomial have prime support in a finite set \(S\), choose \(f(u)\ne0\) and \(C=f(u)\prod_{p\in S}p\); then the integer \(f(u+Ct)/f(u)\) is congruent to 1 modulo every \(p\in S\) for integer \(t\), yet is unbounded, a contradiction. Enlarging the finite excluded set does not affect the argument.

The chosen root modulo \(\ell\) is simple and no other factor of \(c\), or \(A\), vanishes there. Choose a lift \(s\) modulo \(\ell^2\) not giving the lifted zero of \(f\); then \(v_\ell(c)=1,\ v_\ell(A)=0\). Choose \(s>0\) arbitrarily large in this progression. Set \(c=Y_B(a),\ d=X_B(a)\), and choose the integer \(\gamma\) and the halftrace square as in v151. Take the second Pell exponent \(q\) a positive multiple of \(c\) and of the matrix order modulo \(Mc^2\), so \(F=X_q(a)\) and \(i'=Y_q(a)/(Mc^2)\) are integers. Put
\[
 G=a+F^2(c+1-a),\qquad D=G^2-1 .
\]
The second norm gives \(v_\ell(F^2-1)\ge4\) and \(F\) a unit. The identity
\[
 G-1=cF^2-(a-1)(F^2-1)
\]
implies \(v_\ell(G-1)=1\), and \(G+1\equiv2\bmod\ell\) is a unit. Thus \(v_\ell(D)=1\ne v_\ell(A)\bmod2\). In particular the imaginary quadratic fields \(\mathbb Q(\sqrt{-1/A})\) and \(\mathbb Q(\sqrt{-1/D})\) differ. All of these choices work on a false prefix and are made before the small and third Pell ordinates are varied.

## 2. Fixed bilinear certificate gives a smooth genus-one curve

Use the usual integral small starting witness
\[
 k_0=Y_{r+1}(P),\quad \tau_0=X_{r+1}(P),\quad
 h_0=(k_0-r-1)/M^2 .
\]
As in v151, for the third exponent \(v=B+4q n\) put
\[
 H_v=Y_v(G),\quad I_v=X_v(G),\qquad
 H_b=c+F^2(B-c),\quad j_v=(H_v-H_b)/(cF)\in\mathbb Z.
\]
Both \(h_0,j_v\) are positive for sufficiently large choices. Complete the product in the proposed certificate:
\[
 (\lambda h+\nu)(\lambda j+\mu)=\lambda L-\lambda\xi+\mu\nu .
\]
Set
\[
 \alpha_0=r+1-M^2\nu/\lambda,\qquad
 \delta_0=H_b-cF\mu/\lambda .
\]
The first is fixed before \(s\) varies; the second is fixed after \(F\) is chosen. We can and do choose \(s\) large enough that \(k_0\ne\alpha_0\) (the small Pell starting ordinate tends to infinity). Choose \(v\) large enough that \(H_v\ne\delta_0\). Define the nonzero rational \(R_v=(k_0-\alpha_0)(H_v-\delta_0)\) and the certified integer
\(L_v=\lambda h_0j_v+\mu h_0+\nu j_v+\xi\).
The coefficient of \(j_v\) is nonzero; increasing \(v\) also avoids \(L_v=0\).

For arbitrary rational \(k,H\) with \(k\ne\alpha_0\), the equation that fixes the certificate to \(L_v\) is exactly
\[
 (k-\alpha_0)(H-\delta_0)=R_v,\qquad
 H(k)=\delta_0+R_v/(k-\alpha_0).
\]
Thus the two rational Pell conditions are represented by the projective intersection of quadrics
\[
\begin{split}
 T^2&=W^2+A K^2,\\
 J^2&=(K-\alpha_0W)^2+D(\delta_0(K-\alpha_0W)+R_vW)^2 .
\end{split}                                                    \tag{1}
\]
On \(W=1\), \(k=K,\ \tau=T,\ I=J/(k-\alpha_0)\), and the nonzero-denominator restriction recovers exactly the original two norms and bilinear linkage. The distinguished rational point is \(O_v=(k_0,\tau_0,(k_0-\alpha_0)I_v)\).

To see smoothness, the first branch polynomial \(1+Ak^2\) has two distinct roots, and the second branch polynomial is the pullback of \(1+D H^2\) by the nonconstant Möbius transformation \(H(k)\), after multiplying by \((k-\alpha_0)^2\). It has two distinct finite roots, since \(1+D\delta_0^2>0\), and neither root equals \(\alpha_0\). If there were a common root, then \(H(k)\) would give a square root of \(-1/D\) in \(\mathbb Q(\sqrt{-1/A})\), impossible by section 1. The two square classes in \(\overline{\mathbb Q}(k)^\times/(\overline{\mathbb Q}(k)^\times)^2\) are independent because the branch sets are disjoint. The resulting degree-four cover of the line is geometrically connected, simply branched in the two independent quadratic factors at four points, and unramified at infinity. Riemann–Hurwitz gives genus one, and the affine Jacobian check and nonzero leading coefficients give smoothness at the points of the displayed projective model, including infinity. Equivalently use adjunction for the smooth complete intersection. With origin \(O_v\), this is an elliptic curve over \(\mathbb Q\).

## 3. A non-torsion point via a new good prime of the third trace

As in v151 we will use the distinct point \(Q_v=(k_0,\tau_0,-(k_0-\alpha_0)I_v)\), with sign reversed only in the second square root. We require a prime \(p\mid I_v\) at which (1) has good reduction, with the finite exceptional set independent of \(v\).

Exclude 2, numerator/denominator primes of the nonzero constants \(A,D,\tau_0,k_0-\alpha_0,1+D\delta_0^2\), and denominators of \(\alpha_0,\delta_0,k_0\). At a remaining prime dividing \(I_v\), put \(t=H_v\bmod p\). Then \(Dt^2=-1\bmod p\) and \(t\pm\delta_0\ne0\), since otherwise \(1+D\delta_0^2=0\). In particular \(R_v\) is a unit. The two second-branch values of \(k\) are \(k_0\) and
\[
 k_1=\frac{k_0\delta_0+(2\alpha_0-k_0)t}{t+\delta_0}.
\]
Indeed \(H(k_0)=t\), and substituting \(H=-t\) into the fixed-product equation gives the second expression. At the first branch point \(1+A k_0^2=\tau_0^2\) is a unit. For the second consider the fixed polynomial
\[
 N(T)=(T+\delta_0)^2+
       A(k_0\delta_0+(2\alpha_0-k_0)T)^2.
\]
In \(\mathbb Q[T]/(DT^2+1)\) this value is nonzero: otherwise the quotient expression \(k_1\) would be a root of \(1+Ak^2\) inside \(\mathbb Q(\sqrt{-1/D})\), contradicting the distinct-squareclass construction. Its field norm is a fixed nonzero rational. Exclude the numerator and denominator primes of that norm, and any remaining fixed coefficient denominators of \(N\). Then \(N(t)\ne0\bmod p\), so the first and second branch sets are disjoint modulo \(p\), with each set consisting of two distinct geometric roots. Both leading coefficients are units; there is no extra branch at infinity.

These checks establish good reduction of the displayed pointed genus-one model at \(p\): it is the finite locally free degree-four cover of \(\mathbb P^1\) obtained by adjoining the two square roots in the degree-one line bundle, and both the generic and geometric special fibers are smooth by the disjoint-branch calculation. The two rational points \(Q_v,O_v\) reduce to the same point there, yet are distinct over \(\mathbb Q\). The kernel of reduction is torsion-free for odd \(p\) by the formal logarithm, so \(Q_v\) has infinite order in the group with identity \(O_v\).

To obtain such \(p\), freeze the valuations of \(I_v\) at the entire fixed exceptional set by restricting the arithmetic progression for \(v\) to a further progression using the orders of the integral Pell matrix modulo one power higher than each of the fixed valuations, exactly as in v151. The traces \(I_v\) tend to infinity while their part supported on the fixed exceptional set is constant. Hence every sufficiently large trace in that progression has a prime divisor outside the set. No prime density or primitive-divisor conjecture is needed.

## 4. Real and dyadic approximation supplies the false witnesses

On \(W=1\), the second radicand of (1) is strictly positive at every real \(k\) because \(R_v\ne0\). The branch with \(T=+\sqrt{1+Ak^2}\) and the sign of \(J\) at \(O_v\) therefore gives a continuous real path through the origin to every finite real \(k\), including the point \(k=\alpha_0\) where the original coordinate \(H(k)\) has a pole. We use only an interval disjoint from that pole. This resolves the possible component/sign problem caused by replacing an affine link by a Möbius link.

The strict margin holds in an interval near \(k=c/Y\), since there it is \((c/Y)^2>1\). Choose a nonempty bounded open subinterval avoiding \(\alpha_0\). At the origin \(k_0,H_v\) are integers and the Möbius denominator is nonzero, so choose a small enough dyadic neighborhood of \(O_v\) on which \(k,H(k)\in\mathbb Z_2\). A suitable multiple of the non-torsion point \(Q_v\) belongs to an open subgroup inside that neighborhood and to the real identity component. Its multiples are dense in that real component and stay in the dyadic subgroup. This is the compact-group argument of v151, not an assertion of weak approximation on arbitrary genus-one curves.

On the chosen bounded subinterval both \(k\) and \(H(k)\) are bounded. The points with either coordinate an integer form a finite set (the Möbius map is one-to-one on the interval and the square roots have at most four sign choices). Hence there is a rational point of (1) in the interval, with both ordinates nonintegral, in the prescribed dyadic neighborhood. The same calculation as v151 gives rational triangular witnesses because \(\eta=k^2-4(c-kY)^2>1\) and \(8\eta-5\in3+8\mathbb Z_2\). Legendre's theorem after clearing the odd denominator proves the actual equations, not merely the real margin inequality.

Recover \(h=(k-r-1)/M^2\), \(j=(H-H_b)/(cF)\), and \(I\) from \(J\) by division by \(k-\alpha_0\). The proposed certificate is the nonzero integer \(L_v\) by construction. Both quotients are nonintegral. The other certified values, first and second Pell norms, shifted trace, halftrace square, all packed-prefix rows and all source guards are satisfied exactly. For a false source instance choose the false packed digit tuple \(f=1,b=4,g=0\) as in v151. Thus a hypothetical transfer using only this bare bilinear certificate would give false positives under its usual simultaneous integer-tuple realization premises.

## 5. Limits and the exact repair by a second symmetric moment

The theorem rules out fixed integer bilinear combinations. It does not rule out a nonlinear certificate of higher bidegree, a different Pell system, or an extra equation not implied by the proposed linkage.

A sufficient genuinely restrictive extra condition is the second symmetric integer moment: certify \(L=h+j\) and \(K=hj\). Then \(h,j\) are roots of the monic polynomial \(X^2-LX+K\) over \(\mathbb Z\), hence rational-root integrality gives \(h,j\in\mathbb Z\). Conversely every canonical integer witness has both moments integral. With the usual nonzero shifted targets if necessary, this gives a complete nonlinear shared *two-moment* certificate and eliminates the genus-one deformation: at fixed \(L,K\) the two ordinates have at most two ordered possibilities. The product moment is not known to be integral from the first alone; v151 shows why it cannot simply be assumed. This repair uses two independent integer predicates, just as the original separate certificates did, and adds quadratic source rows rather than saving them. It is therefore **not** a seven-certificate compiler improvement. A replacement for the second moment by arithmetic already enforced on the retained witnesses remains open.

The proof of the bilinear obstruction is unconditional, apart from invoking the prior exact Pell congruence identities and standard elliptic group facts. The exact checker verifies algebraic and finite residue identities only; no computational rank assertion or uncomputed universal bound is being inferred from those checks.
