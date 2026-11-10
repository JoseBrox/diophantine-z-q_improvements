# Six contacts with a separately amplified input

## Arithmetic statement

Let the input be \(X\in\mathbb Q\), and put
\[
\gamma=2X^2+1,\qquad \beta=2\gamma^2+B,
\qquad B\ge3\text{ an odd fixed integer}.
\]
Compare the elliptic index \(n\) to \(\gamma\), and use \(\beta\) only in the height scale
\[
a_1=\beta^4+T^4.
\]
For integer input, \(\gamma\) is a positive odd integer, so the nonidentity root-point and completeness requirements remain available. Conversely, \(\gamma\in\mathbb Z\) implies \(X\in\mathbb Z\).

For a reduced fraction \(\gamma=a/b\), \(a\ge b>0\), the reduced numerator of \(\beta\) is
\[
\frac{2a^2+Bb^2}{\gcd(2,b^2)}\ge a^2.
\]
Hence
\[
h(\gamma)\le\tfrac12h(\beta)
\]
exactly and uniformly in \(B\). The original unsuccessful proposal of using this estimate directly for \(\operatorname{num}(\beta-n)\) is invalid: that numerator can have logarithm comparable to \(h(\beta)\), rather than half its height. The comparison must actually be changed to \(\gamma-n\).

Use the six contacts
\[
\{-2,-1,0,2,3,4\}=\{1\pm1,1\pm2,1\pm3\}.
\]
Granville's degree-six consequence of ordinary rational abc, with \(\epsilon=1/4\), gives
\[
h(t)\le\tfrac23\log M(t)+C.
\]
If both detector radicals divide the nonzero reduced numerator \(N_\gamma\) of \(\gamma-n\), the unchanged fourth-power projective-height lemma yields
\[
H:=h(1:\beta:T)\le\tfrac{16}{9}\log N_\gamma+C',
\]
while
\[
\log N_\gamma\le h(\gamma)+\log(1+|n|)
\le\tfrac12H+\log(1+|n|).
\]
Therefore \(H\le16\log(1+|n|)+9C'\). The index-height estimate bounds \(n\), then \(H\), independently of \(B\), contradicting \(\beta\ge B\) for all sufficiently large fixed \(B\). The arithmetic approach is valid under the same retained premises and ordinary rational abc.

## Exact contact circuit and actual cost

Put \(\delta=t-1\), \(r=\delta^2\), and
\[
P_3(r)=(r-1)(r-4)(r-9)=r^3-14r^2+49r-36.
\]
Choose
\[
q=r^2/P_3(r),\qquad s=q^{-1},\qquad R_{\rm contact}=P_3(r)/r^4.
\]
Two contact outputs suffice. In unshifted form they are \(r,h\), with
\[
r=\delta^2,\qquad h=r^2-(14+s)r,
\qquad rh+49r-36=0.
\]
Equivalently, use \(R=r-1\), \(H=h+13\):
\[
R=t^2-2t,\qquad H=R^2-12R-(R+1)s,
\qquad (R+1)H+36R=0.
\]
All three equations are quadratic, with zero absolute constant coefficients. The equation \(rh+49r-36=0\) excludes \(r=0\). The unchanged numerator-pair argument excludes \(s=0\).

The same three weights \(s,s_2=s^2,s_3=ss_2\) and the same factor/product scaling as in abc87 give
\[
b=\frac{s}{r^2}\tau_0^2=\frac{P_3(r)}{r^4}\tau_0^2.
\]
Thus the local and completeness interfaces retain their required form.

However, this uses the same **two contact outputs per detector** as the certified87-variable construction. The separate coordinate \(\beta=2\gamma^2+B\) costs one additional rational coordinate and one quadratic row. A direct implementation therefore has **88 variables**, not fewer than87. No leading polynomial was changed or new coefficient family implemented for this route.

## A restricted geometric obstruction to one contact output

The following statement concerns exact algebraic graph encodings over an algebraic closure. It is not a lower bound for arbitrary rational Diophantine encodings.

With the fixed functions
\[
s=\frac{P_3(\delta^2)}{\delta^4},\qquad s^2,\qquad s^3,
\]
consider the parametrized graph whose homogeneous coordinates include
\(1,\delta,s,s^2,s^3\), together with at most one further rational function of \(\delta\). The function \(s^3\) has a pole of order12 at \(\delta=0\) and order6 at infinity. The five displayed functions already have a base-point-free pole divisor of degree18; adding a further coordinate cannot lower its degree. The map is birational onto its image because it retains \(\delta\). Consequently the projective image in \(\mathbb P^5\) has degree at least18.

If that image were an isolated one-dimensional component cut out by quadrics, four generic quadratic combinations would isolate it at its generic point. Bézout's degree bound would give degree at most \(2^4=16\), a contradiction. Thus an exact geometric graph model with these fixed weight functions cannot use just one contact output and only quadratic defining equations.

This does **not** rule out different weight functions, a different pole normalization, extra rational branches, a construction whose rational zero set is smaller than its algebraic closure, or a scheme using additional arithmetic relations. In particular it is not a proof that87 is globally optimal.

## Four contacts

The four-contact variant does not supply a valid logarithmic odd-contact height estimate. For a binary form of degree \(d\), the cited argument gives squarefree exponent \(d-4-2\epsilon\). It is nonpositive at \(d=4\); the bound with coefficient greater than one belongs to five contacts. The height auditor has an explicit positive-rank elliptic twist for the proposed four-contact set, showing unbounded heights with bounded odd contact radical. This route is stopped unless an additional arithmetic restriction changes that obstruction.
