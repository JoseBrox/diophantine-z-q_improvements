# No rational rescaling identity for free trace data

Let `A,B,w_0` be independent variables over Q, put `N=A^2-2B^2`, and
define

`alpha=(N-A)/(N w_0)`, `q=B/(N w_0)`.

These parameters are birational to `(A,B,w_0)`: with
`D=(1-w_0 alpha)^2-2w_0^2 q^2`,

`A=(1-w_0 alpha)/D`, `B=w_0 q/D`, `N=1/D`.

There do not exist rational functions `r,y` in Q(A,B,w_0) satisfying

`y^2=(r^2+alpha)((r^2+alpha)^2-2q^2)`.

Indeed, regard `k=Q(q)` as the constant field. A solution would give
a `k(alpha,w_0)`-point on the constant nonsingular elliptic curve

`E_q: y^2=x^3-2q^2 x`, with `x=r^2+alpha`.

A rational map from a rational surface to an elliptic curve is
constant: restricting to a general projective line yields a rational
map from P1, which extends by properness and is constant by
Riemann–Hurwitz. Thus both elliptic coordinates are in `k`.
The equality `r^2=x(q)-alpha` is impossible because the divisor
`alpha=x(q)` has odd valuation on its right side.

Consequently no rational choice of physical square rescaling
`w=w_0 r^2` makes the native single-cover radical a square identically
for completely free trace data. This does not rule out rational
witnesses for individual actual detector tuples, or rational sections
after a proper arithmetic coupling of the trace data.
