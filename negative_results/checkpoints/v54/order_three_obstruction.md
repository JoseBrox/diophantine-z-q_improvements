# Inert obstruction to a deterministic order-three contact coupling

## Statement

Let \(K=\mathbb Q(\sqrt2)\), \(D=11-6\sqrt2\), and
\[
 E:y^2=x^3-Dx,\qquad
 P=2(1+\sqrt2,2\sqrt2)
   =\left(\frac{57-28\sqrt2}{8},\frac{-660+417\sqrt2}{32}\right).
\]
For a positive odd integer \(B\) and a positive integer \(X\), prescribe
\[
 A=[X]P,\quad T_X=\operatorname{Tr}_{K/\mathbb Q}x(A),\quad
 u=(X^2+B)^4+T_X^4,
\]
and put
\[
 t_0=\frac{1-3u}{7u},\qquad
 t_1=-\frac{u+2}{7},\qquad
 a=\frac{u(u+2)}{3u-1}.
\]
Define
\[
 F(t)=\frac{t(t+1)(2t+1)(3t+1)(4t+1)(5t+2)}{120},
 \qquad q(t)=7t^2+5t+1,\qquad \eta(t)=\frac{F(t)}{q(t)^3}.
\]

**Theorem.** For every positive odd \(B\), infinitely many positive integers
\(X\) satisfy
\[
 v_{81421}(F(t_0))=v_{81421}(F(t_1))=1.
\]
Every displayed denominator and scale guard is a unit at this prime.
For either of the detector pairs
\[
 (d_0,w)=\left(F(t_0),\frac{F(t_0)}{4(t_0-1)^8}\right)
 \quad\text{or}\quad
 (d_0,w)=\left(\eta(t_0),\frac{\eta(t_0)}{(1+\eta(t_0))^2}\right),
\]
every defined auxiliary tuple whose tests include \(f(H)\) and
\(\overline{f(H-P)}\), where \(f=1/x\), gives a negative odd valuation
of \(b=4w/\operatorname{Tr}(W^{-1})^2\) whenever the trace is nonzero.
Here \(W=\prod_i(1+C_i^2/d_0)\). A zero trace already violates its guard.

The theorem concerns the prescribed root \(A=[X]P\) and this height
substitution. It does not exclude a different height function, an independently
varying root label, a different specialization, or a construction retaining a
free slope. Those alternatives require separate soundness and completeness
arguments.

## Algebraic identities

The map \(\gamma(t)=-(2t+1)/(7t+3)\) has order three, and
\[
 F(\gamma(t))=\frac{F(t)}{(7t+3)^6},\qquad
 q(\gamma(t))=\frac{q(t)}{(7t+3)^2}.
\]
Thus \(\eta\circ\gamma=\eta\), and \(t_1=\gamma(t_0)=at_0\). Direct substitution gives
\[
 F(t_0)=
 \frac{(u-5)(u+2)(2u-3)(3u-1)(4u+1)(5u-4)}
 {14117880u^6},\qquad F(t_1)=u^6F(t_0),
\]
\[
 q(t_0)=\frac{u^2-u+1}{7u^2},\qquad q(t_1)=\frac{u^2-u+1}{7}.
\]
For \(u>5\), both contact values are positive and all real domain guards are nonzero.

## Inert-place lemma

Let \(p\ne2,7\) be inert in \(K\), with \(v_p(d_0)=v_p(w)=1\).
The curve has good reduction at \(p\), since its discriminant is \(64D^3\)
and \(N_{K/\mathbb Q}(D)=49\). The displayed point \(P\) has affine integral
coordinates and does not reduce to the identity.

If both \(f(H)\) and \(\overline{f(H-P)}\) had positive valuation, both
\(H\) and \(H-P\) would reduce to the identity. Conjugation preserves the
valuation because \(p\) is inert. Their difference \(P\) would then reduce
to the identity, a contradiction. Hence one of these tests has valuation
at most zero.

Every nonzero factor satisfies
\[
 v(1+C_i^2/d_0)=\min(0,2v(C_i)-1)\le0;
\]
the two summands have different valuation parity. Zero tests give factor one.
At least one factor has valuation at most \(-1\), all factors are nonzero,
and \(W^{-1}\) has valuation at least one. Its trace is consequently in
\(p\mathbb Z_p\). If this trace \(V\) is nonzero, then
\[
 v_p(b)=1-2v_p(V)<0
\]
is odd. This proves the lemma for all auxiliary tuples, not only multiplication
families or tuples in a finite search.

## Finite certificate

Put
\[
 p=81421,\qquad N=6629217184.
\]
The exact certificate proves that \(p\) is prime, \(p\equiv5\pmod8\),
\(p\nmid N\), and \([N]\widetilde P=O\) over \(\mathbb F_{p^2}\).
It does not assert that \(N\) is the exact order.

The following rows satisfy
\(T_n=\operatorname{Tr}x([n]\widetilde P)\) and
\(y^4+T_n^4=u_0\) in \(\mathbb F_p\).

| \(n\) | \(T_n\) | \(u_0\) | \(y\) |
|---:|---:|---:|---:|
| 1 | 61080 | \(4/5\) | 8576 |
| 1 | 61080 | \(4/5\) | 35004 |
| 6 | 17254 | \(4/5\) | 73321 |
| 1 | 61080 | \(4/5\) | 46417 |
| 10 | 74125 | \(3/2\) | 3133 |
| 9 | 45107 | \(4/5\) | 80711 |
| 20 | 31595 | \(5\) | 57446 |
| 19 | 25083 | \(5\) | 42108 |
| 23 | 78190 | \(3/2\) | 73 |
| 18 | 57250 | \(3/2\) | 1060 |
| 29 | 41438 | \(3/2\) | 77025 |
| 24 | 26788 | \(3/2\) | 23167 |
| 2 | 21974 | \(5\) | 29234 |

Writing \(Y\) for the last column, exact enumeration verifies
\[
 \bigcup_{y\in Y}\bigl(y-(\mathbb F_p^\times)^2\bigr)=\mathbb F_p.
\]
All listed point coordinates and \(y\) are units. The three \(u_0\) values
are simple roots of \(F((1-3u)/(7u))\); all slope, scale and denominator
guards are units there. The recovery checker independently recomputes the
curve arithmetic, the full coverage, simple contacts, and the fixture below.

## Proof for every shift

Fix \(B\). Coverage supplies a row and \(x\ne0\) with \(x^2+B=y\pmod p\).
Choose \(X_0>0\) by
\[
 X_0\equiv n\pmod N,\qquad X_0\equiv x\pmod p.
\]
These congruences are compatible because \(p\nmid N\). The annihilator
identity gives \([X_0]\widetilde P=[n]\widetilde P\), whence \(u\equiv u_0\pmod p\).

By good reduction, \([N]P\) lies in the first formal-group filtration.
The integral series \([p](z)=pz+O(z^2)\) implies that \([pN]P\) lies in the
second filtration. Adding \(pN\) to the integer index therefore preserves
the affine coordinates and \(T_X\) modulo \(p^2\). It changes the other term by
\[
 ( (X+pN)^2+B)^4-(X^2+B)^4
 \equiv8X(X^2+B)^3pN\pmod{p^2}.
\]
Its coefficient after division by \(p\) is nonzero modulo \(p\), since
\(x,y,N\) are units. The contact is simple, so at least one of the two lifts
\(X_0,X_0+pN\) gives valuation exactly one for \(F(t_0)\).
The relation \(F(t_1)=u^6F(t_0)\), with \(u\) a unit, gives the other valuation.

Adding positive multiples of \(p^2N\) preserves all these congruences.
It gives infinitely many positive integers \(X\), eventually with \(u>5\).
The same denominator-unit statements give
\(v_p(d_0)=v_p(w)=1\) for both detector pairs. Apply the inert-place lemma.

## Explicit fixture

For \(X=98,B=81\), computation modulo \(p^2=6629379241\) gives
\[
 x(A)=(1181463837,1902694508),\qquad
 y(A)=(3842721784,4607123365)
\]
in the basis \(1,\sqrt2\), and
\[
 T_X=2362927674,\quad u=4429750217,\quad
 t_0=4664473388,\quad t_1=2208341072,\quad a=4421038170.
\]
In particular,
\[
 F(t_0)\equiv44771p,\qquad F(t_1)\equiv73604p\pmod{p^2}.
\]
The same fixed input works for every odd \(B=81+13258758482k\), \(k\ge0\).
The full coverage argument above is stronger and covers every positive odd \(B\).

## Sources and verification scope

The source curve, point chart, and tests are from
[papers/conditional_few_variables/direct_input13_20261110_v22.tex](../../../papers/conditional_few_variables/direct_input13_20261110_v22.tex)
and the revised detector from
[papers/pole_parameters/reweighted_elliptic_detectors_20261116_v53.tex](../../../papers/pole_parameters/reweighted_elliptic_detectors_20261116_v53.tex).

The corresponding complete TeX manuscript was compiled in two passes,
five pages, with no warnings before the workspace outage. Its scoped SHA-256
was 6f66969212d0be78a6b70a6364560f06d4bf3603903958e5725617b2b534d73a.
This recovery text records the proof and all finite data; it is not a claim
that the original local source bytes have been recovered.
The standard-library Python checker and an independent exact BigInt checker
both passed. Finite computation verifies the displayed certificate; the
infinitely-many-input conclusion uses the proof above.

The established defining-variable counts remain 25 and 13, with 71 for
the ordinary-abc quartic under the repository's stated arithmetic premises.
No 21-variable or 9-variable defining polynomial is claimed here.
