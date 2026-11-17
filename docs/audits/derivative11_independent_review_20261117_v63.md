# Independent audit: removing the scale from the derivative quotient

## Verdict

The normalization

\[
u_0=-2k\frac{F}{F_a},\qquad
F=G(a-z)G(a+z),\quad a=M^4,
\]

recovers every simple contact prime dividing the denominator of `M`.
If the shifts have no zero pair sum, it also recovers every such prime
dividing the numerator of `M`, outside a fixed set of coefficient primes.
Thus no numerator or denominator support of `M` must be discarded.
The derivative-height loss is `(2+epsilon) h(M)`, and nine contacts suffice.
This audit concerns the new normalization, radical accounting and local
preparation. The retained external arithmetic premises and source encoder
are unchanged and are not recertified by the finite calculations below.

## Denominator primes of M

Let `p` lie outside the fixed coefficient set, including primes dividing
`2k` and differences of distinct shifts. Start with a simple contact
`v_p(G(x))=1`, where `x=a-z`, `y=a+z=2a-x`.
Then `x` is integral, exactly one `x+c_i` has valuation one, and
`G'(x)` is a unit.

If `v_p(M)<0`, put `r=v_p(a)=4v_p(M)<0`. Since `p` is odd,
`v_p(y)=r`, hence

\[
v_p(G(y))=kr,\qquad v_p(G'(y))\ge(k-1)r.
\]

In

\[
F_a=G'(x)G(y)+G(x)G'(y),
\]

the first term has valuation `kr`; the second has valuation at least
`1+(k-1)r>kr`. Consequently `v_p(F_a)=kr`, `v_p(F)=1+kr`, and
`v_p(u_0)=1`. No denominator prime of `M` is lost.
This does not assume that the full derivative of `G` has unit leading
coefficient; the lower bound displayed above suffices.

## Numerator primes of M

Also exclude the fixed prime divisors of all nonzero sums `c_i+c_j`.
Suppose no such pair sum is zero, including repeated indices.
If `v_p(M)>0`, then `a=0` modulo `p`. At the unique simple contact,
`x=-c_i` modulo `p`, and thus `y=c_i` modulo `p`. Every factor
`y+c_j` is a unit. Therefore `G(y)` is a unit and `G'(y)` is integral.
The first summand of `F_a` is a unit, and the second is divisible by
`p`. Hence `F_a` is a unit and `v_p(u_0)=1` again.

The enlarged exceptional set is fixed before `M,z,B` vary. For the
specific shifts below, its new primes are already below the source's
retained cutoff `76176`.

At `v_p(M)=0` the collision argument in the derivative manuscript is
unchanged: discard `J(y)` and the multiple-prime support of the product
of the distinct nonzero `2M^4+c_i+c_j`. Their respective height costs
are `(2+epsilon)h(y)` and `(2+epsilon)h(M)`. There is no additional
cost from the support of `M`.

Thus, under the same ordinary rational abc input,

\[
\log r^+_{\mathrm{odd},S}(u_0)
\ge \frac{k-6-3\epsilon}{2}h(M^8-z^2)
     -(2+\epsilon)h(M)-O(1).
\]

## Nine contacts and strict absorption

The set

\[
\{-10,-8,-5,1,2,3,4,6,7\}
\]

has nine distinct nonzero shifts, sum zero, and no pair with sum zero.
For `epsilon=1/100`, the height constants are

\[
\gamma=\frac{297}{200},\qquad C=\frac{201}{100}.
\]

With the retained
`alpha=997/1001` and `Q=501/997`, exact arithmetic gives

\[
Q\left(C+\frac1{2\alpha}\right)
=\frac{125473947}{99400900},\qquad
\gamma-Q\left(C+\frac1{2\alpha}\right)
=\frac{44272779}{198801800}>0.
\]

The sum of the shifts, rather than symmetry under sign, is what is
needed for the leading local square. The loss of evenness in `a`
does not affect the following arguments.

## Completeness preparation

Because the shifts sum to zero,

\[
F\sim-z^{18},\qquad F_a\sim18az^{16},\qquad
u_0\sim z^2/a,\qquad w=\frac{u_0}{(1+u_0)^2}\sim a/z^2.
\]

The scale `a=M^4` is a nonzero rational square. Therefore the leading
expressions for both `u_0` and `w` are squares at every finite place.
For each already fixed `a` and each fixed preparation place, sufficiently
large `z` makes the quotient by the leading square sufficiently close to
one to be a square. At `2` this means closeness in `1+8 Z_2`; it can
be obtained by increasing the prescribed denominator valuation of `z`.

The original source has `a>10`. Requiring `z>a+10` at the real place
gives `F<0`, `F_a>0`, and `u_0>0`. Consequently the balanced test
denominators and product/trace guards retain their real positivity.

All fixed numerator and denominator primes of `a` are in the temporary
preparation set. At these places dominance yields

\[
v_p(u_0)=2v_p(z)-v_p(a),
\]

which is even, since `v_p(a)=4v_p(M)`. The same local approximation
allows the two-adic square and arbitrarily high even valuation conditions
for `w`, then `b`, exactly as before. Since `V` tends to `2`,
`v_2(V)=1`, and the required `v_2(b)>=4` is available. The preparation
at `7` likewise retains the required nonnegative valuation.

Away from this temporary finite set, `a` is a unit. At selected prime
contacts, all scale constants are units and the simple quadratic factor
has nonzero derivative `2(a+c_i)`, so `v_p(u_0)=1` as before.
At an unselected prime with integral `z`, `F` is a unit and `F_a` is
integral, so `v_p(u_0)<=0`. At an unprepared prime with `v_p(z)<0`,
the leading terms dominate, and `v_p(u_0)=2v_p(z)` is even.
The derivative's leading coefficient `18a` is a unit here because the
fixed prime set contains primes dividing `2k`.

New negative odd valuations arising from `F_a` remain harmless by the
balanced transformation: both slots of `W` are congruent to one, `V`
is a unit at the odd prime, and `v_p(b)=-v_p(u_0)>0`. Even valuations
remain even after division by the square factors. No additional prime
support appears in completeness or in soundness.

The prime pattern now has eighteen positions. Their coefficients are
distinct because the shifts are distinct and `a>10` makes every
`a+c_i` positive. Every nonzero-pair-sum guard `2a+c_i+c_j` is positive
in the prescribed completeness data.

## Exact polynomial checks

An exact SymPy expansion of the displayed nine-factor polynomial gives:

- `F_a` has integer content exactly `2`.
- The coefficients of `z^18` in `F` and `z^16` in `F_a` are `-1`
  and `18a`, respectively.
- Assigning degree `32` to `a` and degree `1` to `z`, the exact weighted
  degrees of `F,F_a` are `576,544`.

Writing `H=F_a/2` primitive, the new quotient is `u_0=-9F/H`.
The already retained guard on `F_a` is the guard on `H` up to a
nonzero integer. No new free coordinate, inverse, or guard is needed.

For comparison, the earlier symmetric ten-shift intermediate proposal
also passes, with `C=301/100`, `gamma=397/200` and strict margin
`43774279/198801800`; it is subsumed by the nine-contact argument above.
