# Direct-index transfer with a computed height anchor and linear shifts (v129)

This strengthens the unrestricted-degree direct-index transfer of [v111](../direct_index_transfer_v111/README.md) and [v127](../direct_index_transfer_v127/README.md), with the same variable counts and retained arithmetic premises. It removes the large fixed powers of the aggregate abscissas from the contact translations. This is a degree/circuit simplification, not a new numerical quartic bound.

## 1. The coefficient anchor

Let \(Q(a,Z_1,\ldots,Z_k)\) be the accepted fixed integer source, with nonnegative instance \(a\). As before use the finitely many branches \(Q(a,m_1-s,\ldots,m_k-s)\), \(0\le s\le k\), with all labels \(m_i\ne0\). Let \(D\ge1\) and \(C\ge1\) be the maximum total degree and coefficient one-norm of these branch polynomials, **including \(a\)**. They are independent of the anchor chosen below.

Choose a fixed positive integer \(K\), and include the *computed coefficient point* \(A_0=[a+K]P\) in the abscissa sum \(Z=U+\sqrt2 V=\sum_{i=0}^{k}x(A_i)\), with \(T=2U\), \(B=\max_i |m_i|\), \(m_0=a+K\). There is no new unknown. In particular \(B\ge K\), \(a\le B\), and every nonzero residual \(N=Q(a,m_1-s,\ldots,m_k-s)\) satisfies \(1\le |N|\le C B^D\). Unlike substitution \(a=m_0-K\) followed by a coefficient-norm estimate, this estimate has no dependence of \(C\) on \(K\).

Replace \(T^J,U^J,V^J\) by \(T,U,V\), respectively, in the v111/v127 two- and three-contact lists. Keep the point tests, finite-logarithm precision, pole equations, and character extraction. There is no new arithmetic inference from the coefficient point: it is only used in the height sum.

## 2. Subquadratic growth with a fixed exponent

Let \(L=\lfloor D/2\rfloor+1\), \(C'=\lceil C^{1/L}\rceil\), \(R_S\) an integer upper bound on the product of all fixed excluded primes as in v127, and \(b(n)\) the positive integer bit length. The local test of v127 gives \(M_S(t)^L\mid N\). Set
\[
 H_0=2^{551} R_S C',\quad A=199+b(R_S)+b(C'),\quad
 H_1=H_0(A+4L)^2.
\]
The retained modular height bound then yields
\[
 h(t)\le H_0 B^{D/L}(A+\log B)^2
 \le H_1 B^{2-1/(2L)} .
\]
Indeed \(2-D/L\ge1/L\); for \(x\ge0\), \(e^{-x/(4L)}(A+x)\le A+4L\) (use \(y e^{-y}\le1\)). These constants are independent of \(a,K\), and \(B\). This explicitly retains the strict subquadratic exponent that was discarded in the fixed-power construction.

In the two-contact route the old trace theorem bounds \(B^2\le A_* h(T)\) for a fixed, possibly ineffective \(A_*>0\); the sum of square abscissas gives \(h(T)\ge1\). Subtracting the two arguments bounds \(h(T)\le 2H_1 B^{2-1/(2L)}+\log2\). Therefore the nonzero residual is impossible if \(K>(A_*(2H_1+1))^{2L}\). Take any sufficiently large fixed integer \(K\); there is no assertion of a numerical value for the ineffective constant.

In the specified three-contact route retain v111's explicit \(K_r=18+((r-1)2^{r-1})^2+2r\,2^{r-1}\), \(r=k+1\), with \(B^2\le K_r(h(U)+h(V))\). Subtracting the three arguments gives \(h(U)+h(V)\le(4H_1+2)B^{2-1/(2L)}\), including \(V=0\). The explicit sufficient choice
\[
 K=1+\bigl[K_r(4H_1+2)\bigr]^{2L}
\]
is computable from the fixed source and excluded primes. Thus \(N=0\) in either route.

## 3. Completeness and the finite recipe

For an integral source solution, first fix the nonzero shifted labels and the coefficient point, then the abscissa translations. The translated contact positions may coincide between contact lists; merge repeated positions as in v111. Every occurrence imposes exactly the same tests on exactly the same tuple. The supplier and simultaneous congruence and recurrence assumptions therefore remain applicable. All local congruences, the behavior at real and prepared finite infinity (the translations are fixed), and the class-seven BB pole preparation are unchanged. The whole-guard tagged encoder in v127 also applies verbatim, since the change concerns only the contact translations and the fixed coefficient point. This works on all the original finite-algebra characters; no new division has been introduced.

For the specified route the procedure to compute the coefficient point for instance \(a\) is finite elliptic scalar multiplication of the fixed rational point over \(\mathbf Q(\sqrt2)\). Its complexity and coefficient size can be very large; effectiveness here is not a complexity assertion. The degrees in the *existential unknowns* of the contact shifts are those of the unpowered abscissa sums. The v127 determinant recipe and degree-majorant expressions apply with its \(\delta\) recomputed for the linear shifts, not with an asserted numerical improvement for an unevaluated full Sun source. The counts remain \(4k+8,4k+10\), in particular 48 and 50 for Sun's accepted ten-integer source.

This modification suggests using a low-degree system on the elliptic indices for quartic compilation: large powers \(J\) are no longer necessary. It does **not** assert a low-cost quadratic compilation of the full ten-variable source or of the finite determinant.
