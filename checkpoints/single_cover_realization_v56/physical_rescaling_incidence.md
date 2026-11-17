# Physical rescaling and the actual single-cover incidence

This checkpoint records exact algebra and local valuation lemmas, not an
arithmetic realization theorem.

## Fixed-W square-class incidence

Write `W=A+B sqrt(2)`, `N=A^2-2B^2`, `H=N-A`, `J=N-2A+1`.
The reciprocal-trace representative of the native square test is

`S=w(Nw+H)/(Nw^2+2Hw+J)`.

The equation `S=k^2` is quadratic in `w`:

`N(1-k^2)w^2+H(1-2k^2)w-Jk^2=0`.

Its discriminant is

`H^2+8B^2 k^2(k^2-1)`.

The rational points `k=0,±1` on this quartic do not automatically have
the required physical square class. If `w=d_0 r^2`, clearing the square
denominator and dividing out the forced `r^2` gives

`Y^2=d_0(N d_0 r^2+H)(N d_0^2 r^4+2H d_0 r^2+J)`.

When `B N H J d_0 !=0`, the right side has six distinct roots: the
quartic's discriminant in `r^2` is `8 B^2 d_0^2`, and its value at
`r^2=-H/(N d_0)` is `-2B^2/N`. The smooth curve therefore has genus
two. It always has two rational points at infinity, since the leading
coefficient is `N^2 d_0^4`; finite rational witnesses are not supplied
by those points.

After dividing `Y` by `N d_0^2`, the equation is the particularly useful
form

`y^2=(r^2+alpha)((r^2+alpha)^2-2 q^2)`,

where `alpha=H/(N d_0)` and `q=B/(N d_0)`. It is the pullback of the
elliptic curve `y^2=x^3-2q^2 x` under `x=r^2+alpha`. The missing
condition is an actual elliptic point whose abscissa minus the prescribed
`alpha` is a rational square.

## A rescaling that preserves every odd contact valuation

Let `w_0,c` be nonzero rational numbers and define, for a free rational
parameter `tau`,

`r=(1+w_0 tau^2)/(1+c w_0 tau^2)`.

Retain the nonzero numerator and denominator guards. At a prime outside
the support of `c`, if `v_p(w_0)` is odd then `v_p(w_0 tau^2)` is odd
and nonzero (or `tau=0`, in which case `r=1`). If it is positive,
both numerator and denominator are units. If negative, both have that
same negative valuation. Hence `v_p(r)=0` in either case.

It follows that `w=w_0 r^2` has exactly the same valuations as `w_0`
at all odd-weight primes outside the fixed support of `c`. The detector
product may remain unchanged in a local trace-extraction argument
depending only on those valuations. This avoids the unrestricted
rescaling problem, where large `v_p(r)` would weaken the extraction
threshold.

However, substitution of this restricted `r` into the genus-two
incidence imposes an additional cover. No uniform rational witness has
been constructed. The one-parameter family is a legitimate arithmetic
target, not a one-parameter completeness theorem.

## A fixed coefficient-seven normalizer

For a revised general source one may test the coherent weight change
`w=u/(1+7u)^2` in place of `u/(1+u)^2`. At primes other than seven,
every odd valuation of `u` becomes its positive absolute value, as
before. For positive real `u`, one has `0<w<=1/28`.

If `v_7(u)>=0`, then `v_7(w)=v_7(u)>=0`. If `v_7(u)` is negative
and even, then `v_7(w)=-v_7(u)-2>=0`. Thus the limiting physical
weight of a prepared scalar with square denominator is 7-integral.
When the reciprocal trace is sufficiently close to two, the detector
input `b=4w/V^2` is also 7-integral. The bound `1<=W<2` in both real
slots gives `V>1` and consequently `b<1/7`.

These facts suggest the scale `d=7b` for the intrinsic height-four pole
test. Full ordered preparation and whole-character guards still require
an independent whole-source audit before a replacement is claimed.
