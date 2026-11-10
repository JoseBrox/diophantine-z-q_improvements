# An inverse-weight contact circuit

## Exact algebraic statement

Let

\[
P(r)=r^5-e_1r^4+e_2r^3-e_3r^2+e_4r-e_5,
\qquad N(r)=r^5-P(r),
\]

with fixed rational coefficients and \(e_5\ne0\). Suppose the surrounding system already has rational coordinates \(q,s\) and the equation \(qs=1\). The current contact construction stores four outputs

\[
r=\delta^2,\quad u=r^2,\quad w=ru,\quad F=P(r),
\qquad (1+q)F=uw.
\]

The occurrence of \(F\) is only in this contact circuit. The monomial \(P(r)\) is expressed quadratically in \(r,u,w\).

Replace these four outputs by three outputs \(r,u,v\) satisfying

\[
r=\delta^2,\quad u=r^2,
\]
\[
v=ru-e_1(1+s)u+e_2(1+s)r,
\]
\[
uv-(1+s)(e_3u-e_4r+e_5)=0.
\]

All four equations are quadratic. Substituting the first three into the fourth gives

\[
r^5-(1+s)N(r)=0.
\]

Since \(qs=1\), multiplication by \(q\) yields
\[
qr^5-(q+1)N(r)=qP(r)-N(r)=0.
\]

This is exactly \((1+q)P(r)=r^5\), the original contact normalization. Conversely, the original normalization and \(qs=1\) give the last new equation, with \(v\) uniquely determined by its displayed formula. The old coordinates recover uniquely as \(w=ru\), \(F=P(r)\). Thus the two systems have exactly the same rational projection onto every retained coordinate.

## Boundary cases

If \(P(r)=0\), the common normalization forces \(r=0\), contradicting \(P(0)=-e_5\ne0\). Hence \(P(r)\) never vanishes.

If \(r=0\), the new last equation gives \(1+s=0\). Consequently \(s=q=-1\), which is precisely the old allowed \(\delta=0\) boundary. No interpretation of the rational function \(P(r)/r^5\) is used on this boundary.

There is no additional zero-weight branch: \(qs=1\) is retained literally.

## Application and count

For the current quartics,

\[
P(r)=\prod_{\theta\in\Theta}\bigl(r-(1-\theta)^2\bigr),
\quad
\Theta=\{0,-1/2,-1,1/2399,-32/407\}.
\]

Every \((1-\theta)^2\) is nonzero, so \(e_5\ne0\). The existing inverse weight \(s_1\) satisfies \(qs_1=1\). Replacing the four contact outputs by three saves one rational coordinate and one quadratic row for each detector, with no change to the local factors, pole inputs, completeness witnesses, or height arguments.

- Two detectors: 228 to **226** variables; 202 to **200** rows.
- Three detectors: 265 to **262** variables; 237 to **234** rows.

These are algebraic counts pending full literal-source reconstruction and independent coefficient verification. The mathematical projection equivalence above does not add an arithmetic premise. The effective threshold improvement being audited by the parent can be inherited without changing this circuit.
