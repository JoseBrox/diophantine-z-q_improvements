# An arbitrarily deeply prepared obstruction on the new scalar locus

## Scope and statement

Consider the proposed rational scalar
\[
 L(t)=t^2-14t+77,\qquad d(t)=\frac{28t(t-7)(t-11)}{L(t)^2}.
\]
Its exact identities are
\[
1+d(t)=\left(\frac{t^2-77}{L(t)}\right)^2,
\qquad
49-28d(t)=\left(\frac{7(t^2-22t+77)}{L(t)}\right)^2.
\]
For every integer \(k\ge2\), every real \(T_0>0\), and every \(0<\epsilon<1\), there exist rational \(t,V\) such that
\[
t>\max(11,T_0),\qquad 2-\epsilon<V<2,
\]
\[
0<d=d(t)<\epsilon,\qquad 0<e=4d/V^2<\epsilon,
\]
with square reduced denominators for both \(d\) and \(e\), and
\[
d,e\in7\mathbb Q_2^{\times2},\qquad
v_2(t)=-2k,\quad v_2(d)=v_2(e)=2k+2,\quad v_2(V)=1.
\]
Nevertheless the genus-one curve
\[
 C_{d,V}:\quad Y^2=d\bigl(s^4-(V^2+d)^2\bigr)
\]
has **no rational point**. These are prepared scalar data on the exact proposed scalar locus. No assertion is made that \(t\) and \(V\) are attained together by the actual contact-and-elliptic detector.

## 1. A complete Kummer obstruction

Set \(N=3615=15\cdot241\) and
\[
 E_N:\quad y^2=x^3-N^2x.
\]
PARI algebraic descent gives rank interval \([1,1]\) for both this curve and its two-isogenous curve \(y^2=x^3+4N^2x\). The rational torsion of \(E_N\) has order four. Both rank computations use the same implementation; no independent rank algorithm is claimed.

The point
\[
 R=(-441,75348)
\]
lies on \(E_N\). Consider the full two-descent map
\[
 \delta(P)=([x(P)],[x(P)-N])\in(\mathbb Q^\times/\mathbb Q^{\times2})^2,
\]
with its usual limiting definitions at the two-torsion. The points consisting of the four two-torsion points and their translates by \(R\) have the following distinct pairs of signed squarefree representatives:

| Point | Kummer pair |
|---|---|
| \(O\) | \((1,1)\) |
| \((0,0)\) | \((-1,-3615)\) |
| \((N,0)\) | \((3615,2)\) |
| \((-N,0)\) | \((-3615,-7230)\) |
| \(R\) | \((-1,-6)\) |
| \(R+(0,0)\) | \((1,2410)\) |
| \(R+(N,0)\) | \((-3615,-3)\) |
| \(R+(-N,0)\) | \((3615,1205)\) |

The checker obtains the four translated points by independent rational chord-and-tangent addition. Since the rank is one and the torsion is \((\mathbb Z/2\mathbb Z)^2\), the group \(E_N(\mathbb Q)/2E_N(\mathbb Q)\) has order eight. These eight distinct pairs therefore give its entire image. This argument does not assume that \(R\) generates the free part of the Mordell-Weil group.

In particular every nonzero rational abscissa lies in one of the four classes
\[
 1,\quad -1,\quad N,\quad -N.
\]
The class \(15\) is absent.

## 2. The scalar curve and its local depths

Use the elliptic curve
\[
 \mathcal E:\quad y^2=x(x-735)(x-1155)
\]
and the rational point
\[
 P=(5145/4,77175/8).
\]
It is non-torsion: its reduction has order six at the good prime 13, whereas \(\#\mathcal E(\mathbb F_{17})=16\). A torsion point of order divisible by three would give nontrivial rational three-primary torsion, which injects at 17, a contradiction. The finite checker verifies these assertions by direct enumeration and group addition, independently of PARI.

For a rational point \((x,y)\) on the positive real branch, put
\[
 t=x/105,\qquad z=y/11025,\qquad r=14z/L(t)=\frac{2y}{1575L(t)}.
\]
The curve equation gives
\[
 t(t-7)(t-11)=105z^2,\qquad d(t)=15r^2.
\]
At \(P\), \(v_2(t)=-2\). On the integral model \(y^2=x^3+Ax^2+Bx\), where \(A=-1890\) and \(B=848925\), duplication gives
\[
 x(2Q)=\frac{(x(Q)^2-B)^2}{4x(Q)(x(Q)^2+Ax(Q)+B)}.
\]
If \(v_2(x(Q))<0\), the leading terms have uniquely least valuation, and therefore
\[
 v_2(x(2Q))=v_2(x(Q))-2.
\]
Consequently \([2^{k-1}]P\) has \(v_2(t)=-2k\). Odd multiplication preserves the valuation of the formal parameter, and hence preserves this abscissa valuation. Thus every positive odd multiple of \([2^{k-1}]P\) has
\[
 v_2(t)=-2k,\quad v_2(y)=-3k,\quad v_2(L(t))=-4k,
 \quad v_2(r)=k+1.
\]
Here the formal parameter is \(-x/y\); its leading term under multiplication by an odd integer has unit coefficient and all remaining terms have strictly higher valuation.

The point \(P\) lies on the real identity component, since \(x(P)>1155\). Odd multiples of any non-torsion point on this component are dense in it. We may therefore choose the preceding odd multiples approaching the real identity from the positive-ordinate side. They give
\[
 t\longrightarrow+\infty,\qquad r\longrightarrow0^+,
\]
while keeping all the specified 2-adic valuations. The scalar identity \(1+d(t)\in\mathbb Q^2\) implies globally that every negative valuation of \(d\) is even: if \(d=a^2-1\) has negative valuation, it equals \(2v_p(a)\). Hence its reduced denominator is a square.

## 3. A conic preserving the obstructed level

Choose rational \((q,c)\) on
\[
 q^2+15=241c^2.
\]
This conic has the point \((1/4,1/4)\). A rational parametrization is
\[
 q=\frac{-1-241m^2+482m}{4(1-241m^2)},\qquad
 c=\frac{1+241m^2-2m}{4(1-241m^2)}.
\]
At the prime two, for every \(k\ge2\), there is a local point with \(q=2^{-k}\): indeed
\[
 \frac{1+15\cdot2^{2k}}{241}\in1+8\mathbb Z_2
\]
is a square, giving \(v_2(c)=-k\). The restriction \(k\ge2\) matters; \(v_2(q)=-1\) is impossible on this particular conic.

After choosing the scalar point and hence \(r\), rational approximation on the conic allows us simultaneously to retain \(v_2(q)=-k\) and to impose
\[
 (2-\epsilon)/r<q<2/r.
\]
The assertion follows from the displayed rational parametrization and ordinary weak approximation on \(\mathbb P^1\). The real condition describes a nonempty open interval on the positive branch; the 2-adic condition describes a nonempty open neighborhood of the local point just constructed.

Set
\[
 V=qr,\qquad e=\frac{4d}{V^2}=\frac{60}{q^2},
 \qquad H=V^2+d.
\]
Then \(2-\epsilon<V<2\). By choosing \(r\) sufficiently small before selecting \(q\), we obtain \(d<\epsilon\) and \(e<\epsilon\). Moreover
\[
 v_2(V)=1,\qquad v_2(d)=v_2(e)=2k+2.
\]
Both \(d\) and \(e\) have square class \(15\), which is \(7\) in \(\mathbb Q_2^\times/\mathbb Q_2^{\times2}\).

The reduced denominator of \(e\) is a square. Outside \(\{3,5\}\), its valuation is even by \(e=60/q^2\). At either 3 or 5, a positive valuation of \(q\) would give \(v_p(q^2+15)=1\), contradicting \(q^2+15=241c^2\). Thus \(v_p(q)\le0\) there, and \(v_p(e)=1-2v_p(q)>0\).

Finally
\[
 H=241r^2c^2,\qquad dH=3615(r^2c)^2.
\]
A rational point on \(C_{d,V}\) would map to \(E_{3615}\) by
\[
 x=15\left(\frac{s}{rc}\right)^2,
 \qquad y=\frac{15sY}{r^4c^3}.
\]
The case \(s=0\) is impossible because its right-hand side in the original quartic is negative. Thus the abscissa is nonzero in the excluded class \(15\). This proves the asserted obstruction.

## 4. An exact prepared fixture and verification scope

For a finite example with \(k=2\), take the scalar point \([18]P\) and the conic parameter \(m=-2/51\). Then
\[
 q=-52729/6548,\qquad c=3769/6548.
\]
The scalar value has approximately \(t=12.2331\); its chosen ordinate gives \(r<0\), so \(V=qr>0\). The checker verifies exactly that \(0<d,e<1\), \(0<V<2\), both reduced denominators are squares, and
\[
 v_2(t)=-4,\quad v_2(r)=3,\quad v_2(d)=v_2(e)=6,\quad v_2(V)=1.
\]
It constructs all large rational coordinates exactly by repeated rational group addition and records a hash of their complete canonical JSON representation rather than printing the large fractions.

The checker also verifies the scalar, conic, duplication, and curve-map identities; the finite non-torsion certificate; both rank intervals; all eight Kummer classes; and several finite depth fixtures. These finite checks accompany the universal approximation proof above. They do not prove that \(V\) is an actual detector trace and do not establish a smaller Diophantine definition.


## 5. A further limitation of the fixed square class

The class \(d\in15\mathbb Q^{\times2}\) also limits the contact radical of this family. If \(p\notin\{2,3,5,7,11\}\) and \(v_p(t)>0\), the displayed scalar formula gives \(v_p(d)=v_p(t)\): both \((t-7)(t-11)\) and \(L(t)\) are units. Hence \(v_p(t)\) cannot be odd. The positive odd radical of \(t\), outside a fixed exceptional set containing these primes, is therefore one. In particular these fixed-class tuples cannot themselves be the derivative-contact inputs in a sufficiently large defining source whose retained height inequality forces that radical to grow. The counterfamily rejects a universal theorem based on the scalar and preparation conditions alone; it does not decide the actual-input realization problem.
