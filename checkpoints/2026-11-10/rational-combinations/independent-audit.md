# Independent audit: one rational function cannot detect both contact parities

## Status and scope

The theorem below is proved by formal power series, elementary prime-divisor arguments, and finite congruences. It applies to arbitrary direct rational dependence on the input and pole parameter, not only to a rational function of the two contact values.

It is an obstruction to uniform detection of the union of two odd contact valuations by the parity of one rational function. It is not a counterexample to the complete defining source, a variable lower bound, or a proof that every possible one-pole construction fails.

## Exact data

Put
\[
 R(t)=\frac{t(t+1)(2t+1)(3t+1)(4t+1)(5t+2)}
 {120(t-1)^8}.
\]
The contact at \(-1\) is simple and
\[
 R'(-1)=-\frac{3}{5120}.
\]
Indeed the product of the five nonvanishing numerator factors at \(-1\) is \(-18\), and the denominator is \(120\cdot 2^8=30720\).

Fix an odd integer \(B\ge3\), a nonzero integer \(n\), and the rational number
\[
 T=T(n)=\operatorname{Tr}_{\mathbb Q(\sqrt2)/\mathbb Q}
                 x([n]P)>6
\]
from the source. Define
\[
 \beta(X)=2X^2+B,\qquad a(X)=\beta(X)^8+T^8.
\]

The inequality \(T(n)>6\) has a direct verification. On
\(E:y^2=x^3-(11-6\sqrt2)x\), the point \(P\) is a non-torsion double.
Every nonzero multiple \([n]P\) is a non-torsion double. The doubling formula makes its abscissa positive at both real embeddings. The equation
\(y^2=x(x^2-D)>0\), with \(x>0\), then gives \(x>\sqrt D\).
Here \(\sqrt{11-6\sqrt2}=3-\sqrt2\) and the conjugate square root is
\(3+\sqrt2\). Their sum is six.

## The stronger theorem

Let \(\Psi(X,L)\) be any nonzero element of \(\mathbb Q(X,L)\), and let \(S_0\) be any finite set of rational primes. There are an integer \(C\ge1\), a nonzero vector
\(\epsilon=(\epsilon_1,\epsilon_2)\in(\mathbb Z/2\mathbb Z)^2\), and infinitely many primes \(p\notin S_0\) with the following property.

For every pair of positive integers \(r,s\) satisfying
\[
 s>Cr,\qquad (r,s)\equiv\epsilon\pmod2,
\]
there exist
\[
 X\in \tfrac12\mathbb Z\setminus\mathbb Z,\qquad
 \lambda=z^2+w^2>1\quad(z,w\in\mathbb Z)
\]
such that
\[
 v_pR(\lambda)=r,\qquad v_pR(a(X)\lambda)=s,
\]
\[
 v_p(\beta(X)-n)=0,\qquad
 v_p\Psi(X,\lambda)\equiv0\pmod2.
\]
The value \(\Psi(X,\lambda)\) is defined and nonzero. The chosen \(X\) and \(\lambda\) can each exceed any prescribed real bound.

In particular, at least one contact value has positive odd valuation while the proposed rational parity detector has even valuation. Both contact depths can be arbitrarily large. The theorem also holds after requiring all primes to avoid any prescribed finite set of source exceptions.

## 1. A simple algebraic contact point

Let
\[
 F(X)=a(X)-1=(2X^2+B)^8+T^8-1.
\]
It has degree sixteen and derivative
\[
 F'(X)=32X(2X^2+B)^7.
\]
It is separable. A common zero of \(F\) and \(F'\) would have either \(X=0\), giving
\(B^8+T^8-1=0\), or \(2X^2+B=0\), giving \(T^8-1=0\).
Both equalities are impossible because \(B\ge3\) and \(T>6\).

Fix one root \(\alpha\) of \(F\), and put \(K=\mathbb Q(\alpha)\).
Then
\[
 a(\alpha)=1,\qquad a'(\alpha)\ne0.
\]
The point \((X,L)=(\alpha,-1)\) is a simultaneous simple contact point.
Introduce local coordinates
\[
 u=L+1,\qquad v=a(X)L+1.
\]
Their inverse relation is
\[
 L=u-1,\qquad
 a(X)-1=\frac{u-v}{1-u}.
\]
The Jacobian determinant of \((X,L)\mapsto(u,v)\) at
\((\alpha,-1)\) is \(a'(\alpha)\), up to the order chosen for the coordinates, and is nonzero.

## 2. The integral formal inverse

There is a localization
\[
 A=\mathcal O_K[S^{-1}]
\]
at finitely many finite primes such that \(A\) contains \(\alpha\), the coefficients of \(a\), the coefficients of polynomial representatives for the numerator and denominator of \(\Psi\), and \(a'(\alpha)^{-1}\).
The rational primes below the inverted primes will later be excluded.

Write
\[
 a(\alpha+h)-1=c_1h+c_2h^2+\cdots+c_dh^d,
 \qquad c_j\in A,\quad c_1\in A^\times.
\]
There is a unique formal inverse
\[
 h=\mathcal H(z)\in zA[[z]]
\]
satisfying \(a(\alpha+\mathcal H(z))-1=z\).
This assertion introduces no unbounded set of denominator primes:
the coefficient of \(z^k\) in the inverse equation is \(c_1\) times
the new coefficient of \(\mathcal H\), plus a polynomial with integer coefficients in the previously determined coefficients and the \(c_j\).
Thus every inverse coefficient is obtained by ring operations and division only by the fixed unit \(c_1\).

Substitution gives
\[
 X=\alpha+
 \mathcal H\!\left(\frac{u-v}{1-u}\right),\qquad L=u-1,
\]
with all coefficients in \(A[[u,v]]\).
The substitution is injective on \(K[X,L]\). More precisely it is the isomorphism of completed local rings induced by the inverse formal coordinate maps
\[
 h\longmapsto
 \mathcal H\!\left(\frac{u-v}{1-u}\right),\quad L+1\longmapsto u
\]
and
\[
 u\longmapsto L+1,\quad
 v\longmapsto 1+a(\alpha+h)L.
\]
Their compositions are the identities by the defining inverse equation.

Write \(\Psi=P/Q\), with \(P,Q\in\mathbb Q[X,L]\) nonzero. Their substituted formal series
\[
 \widetilde P(u,v),\quad \widetilde Q(u,v)
\]
are nonzero elements of \(A[[u,v]]\).

## 3. A single cone with monomial leading terms

For a nonzero formal series
\[
 S(u,v)=\sum_{i,j\ge0}c_{ij}u^iv^j,
\]
let \(j_0\) be the least \(v\)-exponent occurring, and let \(i_0\)
be the least \(u\)-exponent occurring among the terms with \(v\)-exponent \(j_0\).
If \(r,s>0\) and \(s>i_0r\), the term
\(c_{i_0j_0}u^{i_0}v^{j_0}\) has strictly smaller weighted degree
\(ir+js\) than every other term:

- for \(j=j_0\), every other nonzero term has \(i>i_0\);
- for \(j>j_0\), its excess weighted degree is at least
  \(s-i_0r>0\).

Apply this to \(\widetilde P\) and \(\widetilde Q\). Denote their selected exponent pairs by
\((i_P,j_P)\) and \((i_Q,j_Q)\), and take
\[
 C=\max(i_P,i_Q)+1.
\]
Exclude the finitely many rational primes at which either selected
nonzero algebraic coefficient is not a unit. This can be done by excluding the numerator and denominator primes of their field norms, together with the already inverted primes.

At every remaining embedding \(K\hookrightarrow\mathbb Q_p\), all formal coefficients are \(p\)-integral and the two selected coefficients are units. Consequently, for all \(p\)-adic \(u,v\) with
\[
 v_p(u)=r>0,\quad v_p(v)=s>Cr,
\]
the series converge, their selected terms are uniquely minimal, and
\[
 v_p\widetilde P=i_Pr+j_Ps,\qquad
 v_p\widetilde Q=i_Qr+j_Qs.
\]
The valuation of their quotient is therefore
\[
 Ar+Bs,\qquad
 A=i_P-i_Q,\quad B=j_P-j_Q.
\]
Here the letters \(A,B\) in this displayed linear form are integer
coefficients only; they are unrelated to the localization and the
fixed input constant. Equivalently one may denote these coefficients
by \(d_1,d_2\).

A linear map from \(\mathbb F_2^2\) to \(\mathbb F_2\) has a nonzero
kernel vector. Choose such a vector \(\epsilon\) for the row
\((d_1,d_2)\). All depth pairs in its parity class make the quotient
valuation even. This parity class meets the cone \(s>Cr\) with both coordinates arbitrarily large. For example, choose
\[
 r=2k+\epsilon_1,\qquad
 s=2(C+1)r+\epsilon_2,\qquad k\ge1.
\]

## 4. Infinitely many admissible rational primes

Let \(g\in\mathbb Z[X]\) be a primitive integer multiple of the minimal polynomial of \(\alpha\). Exclude the primes dividing its leading coefficient or discriminant, all primes already excluded above, and the primes \(2,3,5\).

There are infinitely many remaining primes for which \(g\) has a root modulo \(p\). The elementary prime-divisor argument suffices. For completeness, if a nonconstant integer polynomial \(g\) had all prime divisors of its nonzero values in a fixed finite set, choose an integer \(b\) with \(A_0=g(b)\ne0\), and let \(M\) be divisible by those primes. The polynomial
\[
 \frac{g(b+A_0Mt)}{A_0}\in\mathbb Z[t]
\]
is nonconstant, has constant term one, and is congruent to one modulo
\(M\). For some integer \(t\) its absolute value is greater than one.
Any prime divisor of that value lies outside the proposed finite set,
a contradiction. The same argument remains valid after excluding any
further finite set of primes.

At a chosen prime, a root of \(g\) is simple, so successive linear
lifting gives a root \(\alpha_p\in\mathbb Z_p\) and an embedding
\(K\hookrightarrow\mathbb Q_p\). All localization and unit conditions
above hold for this embedding.

Also exclude the numerator primes of the nonzero rational number
\[
 D_n=n^8+T^8-1.
\]
If \(X\equiv\alpha_p\pmod p\) and
\(\beta(X)\equiv n\pmod p\), reducing \(a(X)-1\) modulo \(p\) would give
\(D_n\equiv0\pmod p\), which is excluded. Hence every such \(X\) has
\[
 v_p(\beta(X)-n)=0.
\]

This argument requires only degree-one primes and ordinary Hensel
lifting. No prime-pattern theorem, unproved density assertion, or
Chebotarev input is being assumed.

## 5. Exact local depth choices

Fix a chosen prime and a permissible depth pair \(r,s\). Take
\[
 u_p=p^r,\quad v_p^{\mathrm{coord}}=p^s,\quad
 L_p=u_p-1,\quad
 z_p=\frac{u_p-v_p^{\mathrm{coord}}}{1-u_p}.
\]
The notation \(v_p^{\mathrm{coord}}\) here denotes a coordinate, not
the valuation. Define
\[
 X_p=\alpha_p+\mathcal H(z_p).
\]
All inverse series converge because \(z_p\in p\mathbb Z_p\). These
values satisfy
\[
 L_p+1=u_p,\qquad a(X_p)L_p+1=v_p^{\mathrm{coord}}.
\]
The leading-term computation proves that \(\Psi(X_p,L_p)\) is
defined and nonzero and has even valuation.

Because the zero of \(R\) at \(-1\) is simple, for \(p\ne2,3,5\),
\[
 R(-1+z)=z\,U(z),\qquad U(z)\in\mathbb Z_p[[z]],
 \quad U(0)=-3/5120\in\mathbb Z_p^\times.
\]
Thus these coordinate depths are precisely the two contact depths.

## 6. Half-integral input and a positive integer norm

Choose \(N>\max(r,s)\). A rational \(X\) in
\(\tfrac12\mathbb Z\setminus\mathbb Z\) can realize any prescribed
jet in \(\mathbb Z_p/p^N\mathbb Z_p\) because \(p\) is odd.
Explicitly, choose an odd integer \(k\) with
\(k\equiv2X_p\pmod{p^N}\), and set \(X=k/2\).
The two congruences on \(k\), modulo \(p^N\) and modulo two, are
compatible. Adding multiples of \(2p^N\) makes \(X\) arbitrarily large.

Every residue \(-1\) modulo an odd prime is a sum of two squares.
Indeed the sets of squares and minus one minus a square each have
\((p+1)/2\) elements, so they intersect. At such a representation
\(z_0^2+w_0^2=-1\), at least one coordinate is nonzero.
Consequently one partial derivative of \(z^2+w^2\) is a unit.
Successive one-variable linear lifting therefore produces, for
any prescribed residue \(\ell\equiv-1\pmod p\), integer residues
\(z,w\) satisfying
\[
 z^2+w^2\equiv\ell\pmod{p^N}.
\]
Apply this with \(\ell=L_p\bmod p^N\). Choose integer lifts and put
\(\lambda=z^2+w^2\). Adding arbitrary multiples of \(p^N\) to one
lift makes \(\lambda>1\), or larger than any prescribed real bound.

The rational functions defining \(u=L+1\) and \(v=a(X)L+1\) have
integral coefficients at the chosen prime. Thus the resulting
rational pair satisfies
\[
 v_p(\lambda+1)=r,\qquad v_p(a(X)\lambda+1)=s.
\]
It remains on the same inverse branch: \(X\equiv\alpha_p\pmod p\),
and the solution near \(\alpha_p\) of
\(a(X)-1=(u-v)/(1-u)\) is unique by its unit derivative.
Therefore its numerator and denominator are precisely the evaluations
of \(\widetilde P,\widetilde Q\), and the same unique-leading-term
valuation formula applies. No extra approximation precision depending
on the size of \(P,Q\) is needed.

Finally \(B\ge3\), \(T>6\), and \(\lambda>1\) ensure \(a(X)>1\).
Both arguments \(\lambda\) and \(a(X)\lambda\) exceed one, so they
avoid every contact and pole over the real numbers. Their \(R\)-values
are defined, nonzero, and positive. The already established local
condition gives \(v_p(\beta(X)-n)=0\). This completes the theorem.

## Rational combinations of the two contacts

For a nonzero \(\Phi(U,V)\in\mathbb Q(U,V)\), the rational function
\[
 \Psi(X,L)=\Phi(R(L),R(a(X)L))
\]
is nonzero: the map \((X,L)\mapsto(R(L),R(a(X)L))\) has nonzero
Jacobian at \((\alpha,-1)\), with determinant
\(a'(\alpha)R'(-1)^2\), and is therefore dominant.
The stronger theorem applies.

Allowing \(a(X)\), \(\beta(X)\), or other rational functions of the
input and pole parameter as coefficients does not evade this
obstruction, since they are already covered by arbitrary \(\Psi(X,L)\).

## Optional higher-dimensional lemma

For \(m<d\) nonzero rational functions in \(d\) independent contact
coordinates, choose a common positive cone where each numerator and
denominator has a unique least monomial. Outside finitely many
coefficient primes, the \(m\) valuations are integer-linear forms in
the \(d\) contact depths. Their matrix over \(\mathbb F_2\) has a
nonzero kernel vector. The corresponding parity class meets the
positive cone with arbitrarily large coordinates. Thus all \(m\)
combined valuations can be even while at least one original contact
depth is odd.

For the actual source theorem only \(d=2,m=1\) is needed, and the
elementary single-cone argument above avoids any finite-support or
Newton-polyhedron machinery.

## Audit qualifications

1. The finite exceptional set depends on the fixed rational function,
   the source constants, and the fixed label \(n\). The theorem makes
   no uniform quantitative prime bound.
2. The conclusion concerns freely chosen allowed source parameters
   \(X,\lambda\) and the fixed genuine point \([n]P\). It does not solve
   the other elliptic comparison equations or exhibit all pole
   witnesses of a false source solution.
3. The theorem therefore rules out a specific uniform parity-covering
   requirement. It does not prove a lower bound on the number of
   variables in an arbitrary Diophantine definition.
4. No floating-point computation or finite sample is used for the
   general assertion. The derivative, separability, formal inverse,
   parity kernel, prime existence, and global realization are each
   proved above.
