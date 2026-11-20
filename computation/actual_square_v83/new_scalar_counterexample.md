# A prepared obstruction on the proposed raw-square scalar locus

This is an obstruction for prepared scalar data on the **exact proposed scalar locus**. It is not an actual contact-and-elliptic-detector tuple and does not disprove the required actual-input realization.

Put
\[
L(t)=t^2-14t+77,\qquad
 d(t)=\frac{28t(t-7)(t-11)}{L(t)^2}.
\]
The two identities
\[
1+d(t)=\left(\frac{t^2-77}{L(t)}\right)^2,
\qquad
49-28d(t)=\left(\frac{7(t^2-22t+77)}{L(t)}\right)^2
\]
hold identically. Neither suffices for the one-parameter genus-one realization.

Take
\[
t=\frac{49}{4},\quad r=\frac{196}{889},\quad
 d=15r^2=\frac{576240}{790321},\quad
 V=\frac{17r}{2}=\frac{1666}{889}.
\]
Then
\[
L(t)=\frac{889}{16},\qquad
1+d=\left(\frac{1169}{889}\right)^2,\qquad
49-28d=\left(\frac{4753}{889}\right)^2,
\]
\[
e=\frac{4d}{V^2}=\frac{240}{289},\qquad
H=V^2+d=\frac{349r^2}{4}.
\]
These data have \(t>11\), \(0<V<2\), \(0<d,e<1\), and square reduced denominators for both \(d\) and \(e\). Moreover
\[
v_2(t)=-2,\qquad v_2(d)=v_2(e)=4,\qquad v_2(V)=1,
\]
and \(d,e\in7\mathbb Q_2^{\times2}\).

Nevertheless
\[
Y^2=d(s^4-H^2)
\]
has no rational solution. Indeed a solution would map to
\[
E_{5235}: y^2=x^3-5235^2x,
\qquad
x=60(s/r)^2,\qquad y=120sY/r^4.
\]
The case \(s=0\) is impossible because \(d,H>0\). Thus \(x\) would be nonzero in the class \(15\mathbb Q^{\times2}\).

PARI algebraic descent gives `ellrank(E_5235) = [0,0,2,[]]`. The rational torsion group has order four, so its finite abscissas are \(0,5235,-5235\). The negative abscissa is outside the positive class; the positive one has quotient
\[
5235/15=349,
\]
which is not a rational square. This excludes the asserted solution.

As a consistency check, PARI also gives rank interval \([0,0]\) for the two-isogenous curve \(y^2=x^3+4\cdot5235^2x\). Both computations use the same PARI implementation; they are not independent algorithms.

The adjacent checker verifies the exact input identities, the valuations and square classes, the curve-map identity, the rank intervals, and the torsion group. It does **not** verify that \(V\) is attained by the actual elliptic trace, and no such assertion is made.
