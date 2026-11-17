# The actual trace for the inputs one and minus one

This is an exact reduction of the revised conditional detector on its
actual point tuple. It does not establish simultaneous rational
realization.

For `epsilon=1` or `-1`, set

\[
X=\varepsilon,\qquad A=[\varepsilon]P,\qquad
U=[\varepsilon]H.
\]

The functions `f=1/x` and `z=-x/y` are even and odd, respectively,
under elliptic negation. Therefore both ratio functions in the
revised source are identically `epsilon`, and its last two tests
vanish. The first four tests occur in equal pairs. Write

\[
a=f(H)^2,\qquad b=\overline{f(H-P)}^2,\qquad \eta=F(t).
\]

Then the actual detector is

\[
W=Z^2,\qquad
Z=\left(1+\frac a\eta\right)
  \left(1+\frac b\eta\right).
\]

Writing `Z=c+d*sqrt(2)` gives the exact actual trace

\[
V=\frac{2(c^2+2d^2)}{(c^2-2d^2)^2}.
\]

On the real preparation domain `eta>0`, both real values of `Z`
are strictly greater than one, since the guarded reciprocal
abscissas are nonzero. Consequently `0<V<2`; the rational reference
section with `V=2` is never an actual tuple of this family.

## An explicit target for the weight-dependent section

The safe weight-dependent cubic has the rational section `V=1`.
For the displayed actual square detector, this target is equivalent
to the conic

\[
2u^2+4v^2=1,\qquad Z^{-1}=u+v\sqrt2.
\]

A rational parametrization is

\[
u=\frac{2k}{1+2k^2},\qquad
v=\frac{1-2k^2}{2(1+2k^2)}.
\]

For example, `k=1` gives the totally positive value
`Z=(12+3*sqrt(2))/7`, whose two real values are greater than one
and whose reciprocal-square trace equals one. This is a target
value for the detector product, not an actual elliptic witness.

The actual realization problem is the field equation

\[
(\eta+a)(\eta+b)
=\eta^2\frac{u-v\sqrt2}{u^2-2v^2},\qquad \eta=F(t),
\]

with `a,b` derived from the same elliptic point `H`. For simultaneous
realization, both prescribed slope arguments and the same actual
point must satisfy their equations. No free value may be substituted
for `eta`, `a`, or `b`.

For completeness, write `a+b=s0+s1*sqrt(2)`,
`ab=t0+t1*sqrt(2)`, and let the target `Z=z0+z1*sqrt(2)`.
The two rational equations are

\[
(1-z_0)\eta^2+s_0\eta+t_0=0,\qquad
-z_1\eta^2+s_1\eta+t_1=0.
\]

On the chart `L=z1*s0+(1-z0)*s1 != 0`, they force

\[
\eta=-\frac{z_1t_0+(1-z_0)t_1}{L}.
\]

Substitution into either quadratic and the condition `eta=F(t)`
remain necessary. No rational solution of these coupled equations
has been constructed here. The square identity `W=Z^2` alone does
not imply squareness of any trace-test radicand.
