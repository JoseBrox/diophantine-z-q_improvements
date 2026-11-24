# Adaptive joint quotient and polynomial-residual transfer

This note transfers two tools from the undecidability part of the project to
the ordinary-rational-abc quotient source:

* the adaptive odd-support union of [v136](../../../undecidability/recursive_scalar_v136/README.md);
* the truncated logarithm and direct polynomial-residual comparison of
  [v111](../../../undecidability/direct_index_transfer_v111/README.md) and
  [v127](../../../undecidability/direct_index_transfer_v127/README.md).

The new relation shares one height anchor, one reference, one pole and
one finite-character encoder among arbitrarily many external rational inputs
and integer quotient labels. The transfer is rigorous but **does not give a
quotient-size cap**. A simultaneous CRT theorem below explains why adding
arbitrarily many fixed polynomial residual tests of this type cannot by
itself give such a cap.

## 1. Statement and assumptions

Use the rational curve and generator of the
[six-coordinate source](../height_anchored_quotient_20261124/README.md),
\[
 E:y^2=x^3-2x,\qquad P=(9/4,-21/8),\qquad q=\widehat h(P)>0.
\]
Retain its cyclic square-abscissa point chart, ordinary rational abc, and
the prepared class-seven pole theorem of
[v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex).
In particular use the full simple denominator mass of the doubled-point
sequence, proved in the
[duplication-mass continuation](../duplication_mass_and_bounded_quotients_20261124/README.md).
No new prime-pattern supplier or primitive-divisor hypothesis is imposed.

Fix integers \(1\le k\le r\), a precision \(N\ge1\), and a finite list
of polynomials \(\Psi_\nu(X_1,\ldots,X_k,M_1,\ldots,M_r)\) over
\(\mathbb Z\). The list may be empty. There is an integer polynomial
relation in **\(k+r+4\) total ordinary rational coordinates** with
distinguished inputs \(X_1,\ldots,X_k\), representing nonidentity
points \(H=[h]P,U_i=[j_i]P\) with nonzero integer indices, and having
the following properties. Here \(H_*=qh^2\) and \(h_{\rm W}\) is
the logarithmic rational height, to distinguish it from the index \(h\).

1. Every zero has \(h\mid j_i\) for every \(i\), after a fixed
   finite reference-index exclusion. Put \(m_i=j_i/h\in\mathbb Z
   \setminus\{0\}\) and \(B=\max(1,|m_1|,\ldots,|m_r|)\).
2. On every zero,
   \[
       \sum_{i=1}^k h_{\rm W}(X_i)\le H_*/100+O(1).
   \]
   There is a squarefree integer \(R_H\) (not a coordinate) with
   \(\log R_H\ge(9/10)H_*\), such that for every prime \(p\mid R_H\)
   \[
   v_p(m_i-X_i)\ge N+2\quad(1\le i\le k),\qquad
   v_p(\Psi_\nu(X,m))\ge N+2
   \]
   for every \(\nu\).
3. If some \(X_i\ne m_i\), then
   \[
   \log(1+B)\ge
      \left(\frac9{10}(N+2)-\frac1{100}\right)H_*-O(1).
   \]
   For a nonzero residual \(D_\nu=\Psi_\nu(X,m)\) of positive degree
   \(d_\nu\) in the \(M\)-variables and total degree at most \(D\),
   \[
   d_\nu\log(1+B)\ge
       \left(\frac9{10}(N+2)-\frac D{100}\right)H_*-O(1).
   \]
   A residual of degree zero in \(M\) must vanish after increasing
   the fixed reference cutoff if \(9(N+2)/10>D/100\).
4. For every tuple \(x_i\in\mathbb Z\setminus\{0\}\), and every
   \(m\in(\mathbb Z\setminus\{0\})^r\) with \(m_i=x_i\) for \(i\le k\)
   and \(\Psi_\nu(x,m)=0\) for all \(\nu\), the relation admits
   witnesses with these exact labels and arbitrarily large positive
   reference index \(h\).

All constants are independent of the varying rational witnesses.
They may depend on the fixed number of inputs, the precision and
the fixed list of polynomials. The reference cutoff is ineffective,
as in the parent theorem. No explicit degree optimization is claimed.

## 2. Adaptive normalization, fixed before the reference is chosen

Set
\[
 f(t)=\prod_{\ell=1}^{10}(t-\ell),\quad
 \phi(w)=\frac{w}{(1+w)^2},\quad
 S_0=1,
\]
\[
 W_i=S_{i-1}X_i^2,\qquad t_i=100+\phi(W_i),\qquad
 S_i=S_{i-1}\frac{f(t_i)}{f(100)}\quad(1\le i\le k),
 \qquad u=\phi(S_k).
\]
The quantities \(S_i,W_i,t_i,u\) are rational functions of the inputs,
not additional coordinates. At real rational inputs \(W_i\ge0\),
\(100\le t_i\le100+1/4\), and \(1\le f(t_i)/f(100)<2\).
For the last strict inequality, each of the ten factors in that ratio
is at most \(1+1/360\), and
\((1+1/360)^{10}<2\), an integer inequality. Thus \(1\le S_k\le2^k\),
\(u>0\), and
\[
                  4\le u^{-1}=S_k+2+S_k^{-1}\le2^k+3.
\]
In particular all normalization denominators are nonzero on real rational
inputs, including zeros of individual \(X_i\).

Let \(\mathcal S\) be a fixed exceptional set containing the bad and
preparation primes, primes of \(f(100)\), differences of contacts and
the fixed logarithm denominators. For a rational \(t\) let \(M(t)\)
denote the product of primes outside \(\mathcal S\) at which \(f(t)\)
has positive odd valuation. The adaptive property is
\[
       p\mid M(t_i)\quad\Longrightarrow\quad v_p(u)>0\text{ odd}.
       \tag{1}
\]
Indeed, if \(v_p(S_{i-1})\) is odd, then for \(X_i\ne0\),
\(v_p(W_i)\) is odd and nonzero. For any rational \(w\) of nonzero
valuation, \(v_p(\phi(w))=|v_p(w)|\). Hence \(t_i\equiv100\pmod p\)
and \(f(t_i)/f(100)\) is a unit. This also holds for \(X_i=0\).
An old odd valuation of \(S_{i-1}\), of either sign, is therefore
preserved exactly. At a new positive odd contact of \(t_i\), the
old valuation must have been even, so the update makes it odd.
All later stages preserve it, and the final \(\phi\) makes it
positive odd. This is the v136 persistence argument with a different
fixed seed and contact polynomial.

Use the standard fixed split-polynomial abc bound in the parent
source, with \(\epsilon=1/100\):
\[
             \log M(t_i)\ge \gamma h_{\rm W}(t_i)-O(1),
             \qquad \gamma=10-4-2\epsilon=299/50 .
             \tag{2}
\]
The denominator of each \(t_i\) is a square, because for reduced
\(w=a/b\ge0\), \(\phi(w)=ab/(a+b)^2\) is reduced, and integral
translation preserves the reduced denominator. The bound (2) is
also the finite-contact simple/odd estimate of the parent; fixed
excluded primes affect only its additive constant. The recursive
support mechanism does not require the individual prime supports
to be disjoint.

## 3. One pole and all local tests

Fix \(K=1000(k+1)^2\) and put
\[
 L=y(H)+u^{-(4K+1)},\qquad
 Z_V=L^2/x(V)^4,\quad \chi_V=(1+Z_V)^{-1}
 \quad(V=H,U_1,\ldots,U_r).
\]
Let \(z=-x/y\). The finite logarithm truncation of the original
six-coordinate source is
\[
 \ell(z)=\sum_{b=0}^{N+4}
        \frac{(-1)^b\binom{2b}{b}2^b}{4b+1}z^{4b+1},
 \qquad
 \lambda_i=\frac{\ell(z(U_i))}{\ell(z(H))}.
\]
Its relative error at a formal point of depth \(a\ge1\), at a good
odd prime, has valuation at least \((N+4)a\).
Indeed the invariant differential is
\(dz/\sqrt{1+8z^4}\); each omitted relative term has valuation
at least \(4ba-v_p(4b+1)\ge 2ba\) for \(b\ge1\), since
\(3^{2b}>4b+1\). At 2 the coefficient denominators are odd, and
we use the logarithm only on sufficiently deep disks.
Guard all indicated divisions, \(L\ne0\), and \(\ell(z(H))\ne0\).

Make a finite test list
\[
 F_i=\frac{\lambda_i-X_i}{z(H)^N}\ (1\le i\le k),\qquad
 F_\nu'=\frac{\Psi_\nu(X,\lambda)}{z(H)^N}.
\]
For each test \(F\) define \(T_F=F^2/(L^{-1}+F^2)\). Impose the
single BB pole
\[
 C=1-\chi_H\prod_{i=1}^r\chi_{U_i}\prod_F(1-T_F),\qquad
 b=1+LC^2,\quad e=112b/29^{2d},
\]
\[
                     Y^2=(1-e)(v^4-e^2)(w^4-e^2),\qquad e\ne0.
                     \tag{3}
\]
Choose once and for all a positive integer \(d\) so large that
\[
        112(4+(2^k+3)^{4K+1})<29^{2d}.
\]
This is a computable fixed coefficient choice, not a variable.
The use of \(d\) here is unrelated to polynomial degrees.

At an odd valuation \(\nu=v_p(L)\), the valuation of \(Z_V\)
is \(2\nu-4v_p(x(V))\), which cannot be zero. Hence each \(\chi_V\)
is integral with residue 0 or 1. Similarly the terms of
\(L^{-1}+F^2\) have different valuation parity, and \(T_F\)
and \(1-T_F\) are integral with residues 0 or 1.
If \(\nu<0\) is odd and \(p\notin\{2,7,29\}\),
the square-denominator obstruction of (3) forces
\[
                        v_p(C)>-\nu/2.
                        \tag{4}
\]
Otherwise \(LC^2\) has negative odd valuation, as do \(b\) and
\(e\), contradicting the pole theorem. Infinite valuations of zero
tests or of \(C=0\) are included. Thus each factor of \(1-C\)
has residue 1. Unlike a sum of failures, the product of these
Boolean residues requires no exclusion of small primes depending
on the number of tests.

At a positive odd valuation \(\mu=v_p(u)\) outside the fixed
exceptional set, if \(H\) has formal depth \(a<K\), then
\(v_p(y(H))\ge-3a>-(4K+1)\mu\), and
\[
 v_p(L)=-(4K+1)\mu,\qquad
 v_p(Z_H)\le-2(4K+1)\mu+8a<0.
\]
This would give \(\chi_H\equiv0\) and \(C\equiv1\), contrary to
(4). Therefore every such prime forces formal depth at least \(K\).
Using (1), for each input
\[
 K\log M(t_i)\le\log B_h\le H_*+O(1),
 \qquad h_{\rm W}(t_i)\le H_*/(\gamma K)+O(1),
 \tag{5}
\]
where \(B_h\) is the denominator of a reduced square root of
\(x(H)\).

## 4. Uniform height budget and exact divisibility

The elementary rational-map height estimates give
\[
 h_{\rm W}(S_i)\le 10\sum_{l\le i}h_{\rm W}(t_l)+O(1),\qquad
 h_{\rm W}(u)\le2h_{\rm W}(S_k)+O(1).
\]
Also \(2h_{\rm W}(X_i)\le h_{\rm W}(W_i)+h_{\rm W}(S_{i-1})\).
For nonnegative rational \(W_i=a/b\) in lowest terms,
\(h_{\rm W}(\phi(W_i))=2\log(a+b)\ge2h_{\rm W}(W_i)\);
the zero case is immediate. Thus, using (5),
\[
 2h_{\rm W}(u)+\sum_{i=1}^k h_{\rm W}(X_i)
 \le
 \frac{40k+k/4+5k(k-1)/2}{\gamma K}\,H_*+O(1)
 \le H_*/100+O(1).
 \tag{6}
\]
For the last inequality it suffices to note that the numerator is
\((5/2)k^2+(151/4)k\) and
\(\gamma K/100=(299/5)(k+1)^2\). All constants are uniform in the
indices and inputs. There is no assumption of their integrality
in this calculation.

Let \(R_H\) be the product of all exponent-one denominator primes
of \(H\) outside \(\mathcal S\) and the support of \(u\).
The full simple-denominator mass from the duplication theorem is
\((1-o(1))H_*\), and the support of a nonzero rational number \(u\)
has logarithmic prime weight at most \(2h_{\rm W}(u)\).
Equation (6) gives \(\log R_H\ge 9H_*/10\) for all sufficiently
large \(|h|\). Exclude the finitely many smaller nonzero indices
by the usual nonzero guard on the square-abscissa coordinate.
The error \(o(1)\) comes from the fixed elliptic sequence, hence
is uniform in every other witness.

At every \(p\mid R_H\), \(v_p(L)=-3\), \(\chi_H\equiv1\), and
(4) gives \(v_p(C)\ge2\). Every \(U_i\) is formal, since otherwise
\(v_p(Z_{U_i})\le-6\). Consequently the reduction order of \(P\)
divides both \(h\) and \(j_i\) at all such primes, so \(R_H\)
divides the denominator of the square abscissa at index
\(g_i=\gcd(h,j_i)\). If \(g_i<|h|\), then
\[
  (9/10)qh^2\le\log R_H\le qg_i^2+O(1)\le qh^2/4+O(1),
\]
a contradiction after increasing the same fixed cutoff. This gives
\(h\mid j_i\) simultaneously without using a primitive prime theorem.

Now the actual formal logarithm ratios are \(m_i=j_i/h\in\mathbb Z\),
and \(\lambda_i\equiv m_i\pmod {p^{N+4}}\).
For every test, \(T_F\equiv0\) implies \(2v_p(F)>3\);
hence \(v_p(F)\ge2\). The input comparisons first give
\(X_i\equiv m_i\pmod{p^{N+2}}\), in particular \(p\)-integrality
of all \(X_i\). Only after that conclusion evaluate the fixed
integer-coefficient polynomial residuals; replacing the integral
\(\lambda_i\) by the integral \(m_i\) changes their values by a
multiple of \(p^{N+4}\). This proves all asserted congruences.
It is important not to use the absolute polynomial evaluation
estimate before recovering local integrality.

For any nonzero comparison residual the numerator is divisible
by \(R_H^{N+2}\). The height upper bounds for the differences and
polynomials are, respectively,
\[
 \log|\operatorname{num}(m_i-X_i)|
      \le h_{\rm W}(X_i)+\log(1+B)+O(1),
\]
\[
 \log|\operatorname{num}(\Psi_\nu(X,m))|
      \le D\sum_i h_{\rm W}(X_i)+d_\nu\log(1+B)+O_\nu(1).
\]
The latter follows by clearing the individual input denominators to
their maximum degrees and bounding each monomial using the
coefficient one-norm. Substitution of (6) gives the discrepancy
bounds in the statement. The argument handles polynomial residuals
which are zero, constants, or have no dependence on \(M\).

## 5. Integer completeness on every actual prepared prime

Fix a tuple of integer inputs and integer labels as in the theorem.
The entire adaptive scalar \(u\) is fixed **before** selecting \(H\).
This ordering is essential. At the finite support of \(u\), and at
the fixed exceptional primes, choose \(H\) sufficiently deep in
the formal group. In particular choose enough depth at 2, 7, 29.
Choose \(H\) at the same time in the real arc near \(-P\) with
\(0<y(H)<3\), avoiding the finitely many zeros of the nonconstant
rational function \(\ell(z(H))\). The cyclic formal-group
recurrence and real density give arbitrarily large positive
\(h\) with these properties. Set \(U_i=[m_i]H\).
They have nonzero abscissas and ordinates in the retained chart.

At every formal prime of \(H\), of depth \(a>0\), \(y(H)\)
dominates \(u^{-(4K+1)}\), by the finite initial preparation
on the support of \(u\) and automatically off that support.
Every \(U_i\) has formal depth at least \(a\).
Thus \(v_p(L)=-3a\), \(\chi_V\equiv1\pmod {p^{2a}}\),
and the truncated logarithms differ from their integral ratios
by at least \((N+4)a\). The polynomial equalities assumed for
the labels give the same error estimate for all polynomial tests.
Every \(F\) has depth at least \(4a\), \(T_F\) at least \(5a\),
and hence \(C\) at least \(2a\). In particular
\(v_p(b-1)\ge a\).

At every other prime \(L\) is integral. If its valuation is even,
negative valuations of \(b=1+LC^2\) are even. If its valuation
is odd, all fractions are integral by parity, hence \(b\) is integral.
The proof is unchanged at the fixed good and bad primes because
they were included in the initial deep preparation. This handles
foreign denominator primes of all the numerator points, rather
than assuming that the point choices introduce no new primes.

In the real arc \(0<L<3+(2^k+3)^{4K+1}\). All factors
\(\chi_V\) lie in \((0,1)\), all \(T_F\) in \([0,1)\),
and \(0<C<1\). Consequently \(0<e<1\) by the choice of
\(d\). The finite preparation gives \(b\equiv1\bmod8\) at 2,
and unit values at 7 and 29. Therefore \(e\) has the required
dyadic class and valuation four, is positive and less than one,
and has square reduced denominator. The BB theorem supplies
the terminal witnesses for this actual scalar after the points
have been chosen. No simultaneous supplier is used.

## 6. Exact coordinate accounting

For each point \(V\) use its square-abscissa chart
\(V=(g_V^2,g_V\eta_V)\), \(\eta_V^2=g_V^4-2\), with the retained
cyclic-group and nonidentity guards. The ordinary base consists
of the \(k\) inputs, \(r+1\) square-abscissa coordinates,
and the two pole parameters \(v,w\).
All recursive normalizations, ratios and tests are rational
functions of these coordinates and the finite square-root
characters. Clear a terminal rational radicand \(A/B\) by
adjoining the monic equation \(Y_*^2=AB\), with \(B\ne0\).
Use the existing
[selected-character encoder](../../../undecidability/papers/joint_finite_algebra_encoder.tex)
for the point and terminal finite roots and all guards, requiring
one ordinary coordinate. This is a finite coefficient prescription
of rank at most \(2^{r+2}\) in the square-abscissa version.
The total is \(k+(r+1)+2+1=k+r+4\).

If the first foreign-charge conic of
[the seven-coordinate continuation](../one_conic_foreign_charge_20261124/README.md)
is appended for each numerator point, its charge adds just one
ordinary coordinate per point; its other coordinate is another
finite root. It can be realized independently after the point and
pole choices. A common independent exponential cap on those charges
would bound every \(m_i\) by \(\exp(AH_*/2+O(1))\);
the discrepancy bounds above would then force all the input
equalities and all polynomial residuals for sufficiently high
fixed precision and reference cutoff. This is an implication of
a cap, **not a construction of one**.

## 7. Simultaneous CRT obstruction, including Pell residual tests

The polynomial tests of Section 3 cannot supply the missing cap
on their own. In fact fix **any rational** inputs \(x\) and a tuple
\(\xi\in\mathbb Q^r\) with
\[
 \xi_i=x_i\ (i\le k),\qquad
 \Psi_\nu(x,\xi)=0\text{ for every }\nu.
\]
Assume all these fixed rationals are integral at 2, 7 and 29.
Then the relation has witnesses with arbitrarily large positive
\(h\), and, **at each one of these fixed reference points**, each
integer multiplier \(m_i\) ranges through a whole arithmetic
progression with the zero value omitted.

Indeed, fix the actual adaptive scalar \(u(x)\) and choose \(H\)
deep at its finite support and at all fixed exceptional primes
and denominator primes of the \(x_i,\xi_i\). At the latter prescribe
even formal depth. This is possible by the formal-group isometry
and CRT on the index: after entry into each sufficiently deep
subgroup, multiplication by an integer adds its \(p\)-adic
valuation to the depth. The finite congruences and real arc
requirements are compatible just as in the six-coordinate
false-positive theorem.

Now fix \(H\). At every odd-depth formal prime of \(H\), the
tuple \((x,\xi)\) is locally integral. Require
\[
                     v_p(m_i-\xi_i)\ge(N+4)a_p(H)
\]
at these finitely many primes, and at 2, 7 and 29 even if the
depths there are even. Choose each nonzero \(m_i\in\mathbb Z\)
in its nonempty CRT progression and put \(U_i=[m_i]H\).
For every tested prime, the truncation and polynomial evaluation
give the same depth estimates as in integer completeness.
At every even-depth formal prime \(L\) has even valuation,
so the negative denominator valuations of \(b\) are even
without any test approximation. At nonformal primes \(L\)
is integral and the old parity argument applies.
The real upper bound on \(e\) is independent of all \(m_i\).
Thus every choice in the progressions gives a fully prepared
BB input, and the theorem supplies actual pole witnesses.
The optional conics also have their unconditional rational
parametrizations for each such choice.

In particular fix a single integer input and integer tuple
satisfying the prescribed polynomials. The unbounded progressions
at its fixed reference point exclude a finite bound on any
of the quotients in terms of that point and that input.
With a numerator-charge conic appended, the charge heights
are also unbounded, by the foreign simple-prime lower bound.
When the displayed rational system has a noninteger input
solution integral at the three preparation primes, the same
argument supplies actual noninteger input zeros. There is no
claim that every integer polynomial system has such a rational
solution.

This is the precise limitation of transplanting the Pell,
Lucas, or other polynomial index residuals of the undecidability
compiler to the rational quotient source. Their successful use in
v111/v127 depends on an independently height-controlled collection
of **integer** root labels and contact arguments selected before
the auxiliary multiplication witnesses. Here the quotient labels
are allowed to grow without bound, and the finite congruences
do not turn their polynomial residuals into equalities.
A genuinely new arithmetic restriction is required.

## Scope

This is a new joint subrelation, not a defining-polynomial record.
It integrates adaptive odd support and direct index tests without
a cyclic prime selection or any assumption that external inputs
are integral. Its proofs establish completeness and the stated
quantitative alternative; they do not establish the requested
nine-coordinate height cap. The ordinary-abc assumption and all
inherited point and pole assumptions remain explicit.
