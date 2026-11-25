# v154: higher-genus nonlinear shared Pell candidates

**Proved canonical completeness and elimination of the fixed-fiber elliptic deformation; integrality soundness remains open.** These candidates are not installed in a preferred quartic compiler and give no new bound on the number of independently certified source integers.

Let the fixed source data be as in the redesigned v148/v150 binomial block, keeping the other certified integer inputs and their exact guards. Abstractly, write the two affine congruence rows and norms as
\[
 k=b_1+n_1h,\quad H=b_2+n_2j,\qquad
 \tau^2=1+A k^2,\quad I^2=1+D H^2 ,
\]
where \(A,D\) are positive integers, \(b_1,b_2\) are integers, and \(n_1,n_2\) are nonzero integers. In the source \(b_1=r+1,\ n_1=M^2,\ b_2=c+F^2(B-c),\ n_2=cF,\ A=P^2-1,\ D=G^2-1\). Retain the separate first/second-norm and shifted-trace arguments establishing integrality of the fixed data; \(c\ne0\) follows already from the strict margin and \(|Y|\ge16\). Require \(A,D\ge1\), adding a real nonnegative square-sum guard if necessary. All these guards hold on positive canonical completions.

## 1. One nonlinear certified integer

Fix an even integer \(d=2m\ge2\). Replace the two individual integer predicates on \(h,j\) by the single nonlinear target
\[
 \Lambda=h^d+j^d\in\mathbb Z,\qquad
 \Lambda>(b_1^2+b_2^2+2)^m.                              \tag{1}
\]
Retain the norms, affine congruence rows, margin equations and all other source conditions.

Canonical completeness holds: for each yes-instance use the canonical small Pell value and the integer \(h_0\) from v150. Choose the integral third-Pell quotient in the progression of v151 arbitrarily large positive, leaving the small witness and its margin unchanged. The sum \(h_0^d+j_v^d\) is then an integer satisfying (1) for sufficiently large \(v\). No new residue-class assertion or conjecture about a varying curve is used for completeness. Since all coefficients in the bound are integral, the strict inequality can be imposed by four rational squares representing \(\Lambda-(b_1^2+b_2^2+2)^m-1\); every canonical nonnegative integer difference has such a representation. The same applies to integer nonnegative guards on \(A-1,D-1\). This makes the new restriction polynomial, though no cost saving is claimed.

If the two ordinates are integral, the redesigned coprime moduli of v148 imply \(h,j\in\mathbb Z\) also with this power-sum target in place of the sum. In fact their reduced denominators divide the respective coprime moduli, so at a denominator prime of one quotient the other is integral and its power cannot cancel the negative valuation. Thus the conditional signed binomial soundness result of v150 still applies in that case.

## 2. Every guarded fixed-parameter fiber has high genus

Fix the integer parameters and a value of \(\Lambda\) satisfying (1). The base curve
\[
 C_0:\ h^d+j^d=\Lambda W^d\subset\mathbb P^2
\]
is smooth and geometrically connected, since \(d\ne0\) in characteristic zero and \(\Lambda\ne0\). Its genus is \(g_0=(d-1)(d-2)/2\). On its affine chart \(W=1\) adjoin the square roots of
\[
 f=1+A(b_1+n_1h)^2,\qquad g=1+D(b_2+n_2j)^2.
\]
The two zeros of the first quadratic in \(h\) are \(h_\pm=(-b_1\pm i/\sqrt A)/n_1\), and similarly the two zeros of the second quadratic in \(j\) are \(j_\pm=(-b_2\pm i/\sqrt D)/n_2\). They are distinct, and
\[
 |h_\pm|^2\le b_1^2+1,\qquad |j_\pm|^2\le b_2^2+1.
\]
Thus
\[
 |h_\pm^d+j_\pm^d|
 \le (b_1^2+1)^m+(b_2^2+1)^m
 \le(b_1^2+b_2^2+2)^m<\Lambda .
\]
There is no common zero of \(f,g\) on \(C_0\). Also \(\Lambda\) is greater than the modulus of each individual power, so over each \(h_\pm\) there are \(d\) distinct nonzero values of \(j\); at these points \(h-h_\pm\) is a uniformizer by the implicit derivative in \(j\). Thus \(f\) has exactly \(2d\) simple zeros. The same holds for \(g\), on a disjoint set. At infinity all \(d\) base points have both homogeneous coordinates \(h,j\ne0\), and \(W\) has a simple zero there (transversality follows by differentiating \(h^d+j^d\)). Both functions have poles of order two, giving no geometric ramification there.

The two square classes are independent in the geometric function field, by their distinct simple-zero supports. The smooth projective normalization of the biquadratic extension is therefore geometrically connected, of degree four over \(C_0\). Each of the \(4d\) simple branch points has two points above it of ramification index two, and there is no other ramification. Riemann–Hurwitz gives
\[
 2g_{\rm total}-2=4(2g_0-2)+8d,\qquad
 \boxed{g_{\rm total}=2d^2-2d+1}.
\]
In particular the quadratic nonlinear target (\(d=2\)) gives a genus-five curve, and the fourth-power target gives genus 25. The affine curve of the two norm equations and power-sum relation is already smooth by the same simple/disjoint branch checks. For \(d=2\) its standard complete intersection in \(\mathbb P^4\) is smooth also at infinity (all of \(h,j,\tau,I\) are nonzero there, and the three Jacobian rows are independent).

Faltings' theorem now shows that each guarded fixed-parameter fiber has only finitely many rational points. This rules out the v151/v153 construction of infinitely many rational points by a dense orbit on a fixed elliptic curve, for **every** such fiber, not just generically. The genus computation and completeness are unconditional. See Faltings, *Endlichkeitssätze für abelsche Varietäten über Zahlkörpern*, Invent. Math. 73 (1983), 349–366; the precise smooth-geometrically-connected-projective genus-at-least-two formulation is also recalled in Theorem 1.1 of [Quantitativity in the Mordell Conjecture](https://epubs.siam.org/doi/full/10.1137/25M1804091).

## 3. Why the new restriction is not yet sound

Finiteness is much weaker than integrality. In particular it provides neither a uniform list of all rational points on these varying fibers nor a proof that the points in the source margin are integral. It also does not exclude isolated false rational witnesses, including on false packed instances. The fixed finite fiber result is not a proof of effective computation of rational points.

There is a direct local obstruction for every power \(d\). Fix any nondegenerate integral data and integer \(\Lambda\). Choose a prime \(p\) splitting both \(A,D\) as square units, with \(p\nmid n_1n_2\), \(p\equiv1\bmod 2d\) and outside the fixed exceptional set. Such primes exist by taking a suitable common congruence modulus, quadratic reciprocity and Dirichlet's theorem. For arbitrary \(e\ge1\), put \(h=p^{-e}\). The equation
\[
 t^d=\Lambda p^{de}-1
\]
has a unit solution \(t\in\mathbb Z_p^\times\): its reduction has a nonzero simple root because \(-1\) is a \(d\)-th power modulo \(p\) and \(p\nmid d\). Set \(j=p^{-e}t\). Both affine ordinates have negative valuation \(-e\). Since \(A,D\) are square units, their norm equations have roots in \(\mathbb Q_p\) by Hensel applied after dividing by the square leading terms. Both quotients are nonintegral and \(\Lambda=h^d+j^d\) is exactly the prescribed integer. This is only a local example; it does not contradict the global finiteness theorem.

The two-moment repair in v153 is sound but retains two certified integers. The candidate (1) really uses one certified integer and prevents the previous infinite deformation while preserving canonical completeness; it is **not a sound transfer until the remaining global rational-point problem is solved**. No quartic count is assigned to it. The next concrete task is to exploit the special Pell coefficients and the ample freedom of the third exponent to impose further equations or a uniform rational-point exclusion, not to infer integrality from genus alone.
