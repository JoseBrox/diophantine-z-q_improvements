# One rational harmonic selector (v130)

**292 variables, 241 quadratic residuals**, with ordinary rational abc and the same remaining arithmetic and coding inputs as v128. All twelve certified source integers remain. This is an equivalence of the source-instance projections, not of all auxiliary zeros.

Let \(u,c=1/u,R,A,V,t_2,C_0,\mu,J,\mathrm{var}\) denote exactly the common quantities in v125/v128. Retain
\[
 R=c f_U+c^2 f_H^2+\bar f_{H-R_0}^2,\quad
 A=R^2+ut_2,\quad V=A^2+c(C_0-\mu)^2.
\]
Delete the two components of \(V^2\) and the two components of \(\chi=u/(u+V^2)\). Introduce one rational \(D\) and the quadratic equation
\[
 D\,\operatorname{Tr}V=\operatorname{Nm}V.
\]
Replace \(Z_0=(1-\operatorname{Tr}\chi)^2+cJ^2\) by
\[
 Z_0=D^2+cJ^2.
\]
Keep \(Z=Z_0^2+c\,\mathrm{var}^2,\ \alpha=u+Z^2,\ \tau(1+\alpha)=\alpha,\ b=7c\tau^2\), and the native pole.

## Local soundness (including zero and inert slots)

At every retained prime of the v126 radical bound, \(v(u)=1\). The exact parity calculations in v125 show that \(v(V)>0\) in a slot if and only if that slot satisfies the three formal conditions, the opposite-unit test, and the primary ratio congruence. In particular at most one slot can pass: simultaneous primary and opposite formal membership of both \(H\) and \(H-R_0\) in the same reduction kernel would make \(R_0\) reduce to the identity, a fixed excluded condition. At an inert prime there is no passing slot. Therefore \(V=0\) is impossible at any retained prime; the two slot values are finite nonzero field values there (inert slots are counted twice).

If \(\operatorname{Tr}V=0\), the new equation implies \(\operatorname{Nm}V=0\), hence \(V=0\) in the field. Thus the quotient is well defined at the retained primes without an extra guard. If one slot passes, with valuations \(v_1>0\ge v_2\), the trace has valuation \(v_2\) and the norm has valuation \(v_1+v_2\). Hence \(v(D)=v_1>0\). If neither passes, both valuations are nonpositive and
\[
 v(D)=v_1+v_2-v_p(\operatorname{Tr}V)\le\max(v_1,v_2)\le0 .
\]
The same inequality applies at inert primes. Consequently the scalar test \(v(D)>0\) is exactly equivalent to the existence of the unique passing slot.

The unchanged native-pole obstruction gives \(v(\alpha)>0\), then \(v(Z)>0\), and by the distinct parity of the two summands in \(Z\) and \(Z_0\) it gives \(v(D)>0,v(J)>0,v(\mathrm{var})>0\). This does not presuppose that any private failure value is integral. After the common success is proved, the v123 primary depth estimate and Boolean failure proof apply to every private point, and the v119 signed-index argument applies to every active contact group. The denominator-height and strict absorption estimate of v126 are unchanged. In particular no new exceptional primes or arithmetic hypothesis are needed, and the sufficiently large fixed shift remains ineffective.

## Ordered completeness and preparations

Use the same canonical integer inputs and interpolated points as v125/v126. Each selected contact has its unique passing slot, so the new harmonic quotient has positive valuation there; \(J\) and the variance also have positive valuation. Thus \(\alpha\) and the actual pole input have valuation one. At every fixed prepared place and really, keep the earlier bounded point neighborhoods, with \(t_2=(s+s^{-1})^2\ne0\) bounded away from zero, and use the same slope preparation \(c\to0,\ u\to\infty\). The v125 asymptotic now gives
\[
 V\sim u^2t_2^2,\qquad \operatorname{Tr}V\sim2u^2t_2^2,\qquad D\sim u^2t_2^2/2 .
\]
These are uniform asymptotics in the chosen sufficiently small neighborhoods at each fixed place; the leading term is rational and nonzero, including at two. The private errors and variance remain bounded, \(J\to0\), so \(Z_0\sim D^2,\ Z\sim D^4,\ \alpha\sim D^8\) at the prepared infinities. In particular \(\tau\to1\) and \(b\sim7c\), just as required for the real and fixed-place BB preparation. At nonselected primes the unchanged expression \(\alpha=u+Z^2\) gives the previous negative-odd-\(v(u)\) normalizer argument; at all even valuations the square factor preserves parity outside seven. The physical pole has the same square-denominator, real and dyadic preparation. All new quotients have nonzero denominators at these prepared witnesses. Invoke the same native BB realization theorem. This supplies every required source-instance witness.

## Compiler

In the pinned v128 table delete four coordinates and the five rows defining \(V^2,\chi,Z_0\). Add one coordinate and two quadratic rows, giving \(295-4+1=292\) and \(244-5+2=241\). Every other row is unchanged by named monomial reindexing. The deterministic builder verifies full support and degree at most two; the nonzero quadratic rows make the sum-of-squares degree exactly four. This reduction does not rely on numerical checking of p-adic cases. It is not a removal of an integer predicate.
