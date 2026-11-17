# Independent audit of the order-two scalar / eighth-order comparison transfer

Audited file: `checkpoints/general_scalar_v56/precision_transfer_20261117_v56.tex`.
Audit date: 17 November 2026. The retained external arithmetic inputs are
not independently reproved here.

## Formal logarithm

With `f=1/x`, `q=D f^2`, and `z=-x/y`, the curve equation gives
`z^2=f/(1-q)`. Write the logarithm as `z A(q)`. Comparing its
derivative with `dx/(2y)=z df/(2f)` gives

`(1+q) A(q)+4q(1-q) A'(q)=1-q`.

Thus `a_0=1`, `a_1=-2/5`, and
`a_j=a_(j-1)(4j-5)/(4j+1)` for `j>=2`, as stated.
For `r=v(z)>=1`, one has `v(q)=4r`. Omitted terms start at `j=2`.
Below `4j+1<p` their coefficients are integral. Above this threshold,
`v_p(a_j)>=-j` suffices: the denominator divides a product of the
integers at most `4j+1`, whose p-adic valuation is at most
`(4j+1)/(p-1)<=j` for the relevant primes. Since `p>76176`, the
tail starts at `j>=19044`, and `4jr-j>=3jr>=8r`. The coefficient
series converges and the logarithm divided by `z` is a unit.
The claimed relative precision eight follows.

## Every character and every denominator

At a prepared point-chart specialization, each real slot of a geometric
character is a signed original multiple. Every guarded difference is
again a signed nonzero multiple, with indices of the forms
`±h±1` and `±hn_i±n_i`. They cannot vanish for `h>2` and nonzero
root labels. The square-abscissa source gives `x^2>D` in each real
embedding, hence the new factor `1-2D/(5x^2)>3/5`.

All new denominators are consequently nonzero simultaneously at every
prepared character. At fixed finite places they are nonzero and locally
bounded, so the existing compact/local neighborhood and large-slope
argument still applies. The source's fixed avoidance set must continue
to include the prime support of `1+rho`, as required in Reweighted.

## Local index extraction

At least one of `h,h-1` is a p-adic unit. That ratio of integer indices
is integral, so its logarithmic approximation is integral. The paired
comparison, of order at least one, forces the other approximation and
then its exact ratio to be integral. This is the required step before
turning relative precision eight into absolute precision eight.

For the order-six comparisons, the identity

`j/h - n = -(h-1) [j/h-(j-n)/(h-1)]`

then gives congruence of the ratio with the root label modulo `p^6`.
The input comparison needs only modulus `p`.

Scalar order two yields `v_p(c)>(5/4)|v_p(rho)|`, so every scalar
alternative contributes `p^2|c`. Thus the stated divisibilities
`M_j^6 | Delta c^3` and `M_j | (u-nv)c` are correct.

## Heights, Lucas growth, and uniformity

The scalar contact radical has square dividing `c`, giving the exponent
`(7/3)/2=7/6` in the scalar height bound. The consumed prime gives
`log c>(5L/4) log ell`, enough to absorb `2L log ell` with factor `8/5`.

The residual `Delta=F(s^2,t,b)` has degree six. Its comparison-height
exponent is `(6+3)*7/36=7/4<2`; the remaining scalar exponent is
`7/6<2`. Therefore its vanishing follows uniformly for sufficiently
large fixed `L`.

After vanishing, the retained elementary Lucas lemma applies with
`a=s^2`. Since `b!=0` and forced `c=|s-1|` is large,

`log B_0 >= log|t| > s^2-3 >= c(c-2)-2`.

This quadratic growth contradicts the upper bound of order `c^(7/6)`
from a nonzero input residual. All new exponents and rational functions
are fixed; the source's constants remain independent of `L`.

## Ordered completeness

Choosing the scalar root label `s=c+1`, with `c` a sufficiently divisible
positive multiple of six, preserves scalar preparation and gives
`s` odd and `s=1 mod 3`. Then `a=s^2` is odd and `a=1 mod 3`.
For `k=2(a-2)`, the recurrence has `U_k=0 mod (a-2)`, and
`k=1 mod 3`. The mod-two recurrence has period `0,1,1`, so both
`b=U_k/(a-2)` and `t=U_(k+1)` are positive odd integers. All roots
and scales are fixed before prime selection, as required.

At fresh contacts the actual ratios have integral exact targets, hence
the new field errors have valuation at least eight. Order-six field
summands have valuation at least `16-11=5`; reciprocal-abscissa field
summands have valuation at least three. The unchanged extra divisibility
at selected primes keeps scalar component valuations nonnegative or at
most minus two, so the same normalizers remain integral. With the
reweighted extra factor of `R_j`, all scalar summands have valuation at
least three. No deeper opposite-place congruence is needed.

Conclusion: the transfer's proof is valid under its retained premises.
It preserves the existing twenty-five-coordinate census and gives no
twenty-one-variable realization by itself.
