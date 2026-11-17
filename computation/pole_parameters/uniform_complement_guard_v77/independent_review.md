# Independent mathematical review

Status: PASS for the stated guard theorem, source transfer, and conditional
finite-root replacement. No global nine-variable realization is proved.

## Real point characters and uniform bounds

The actual rank-four point charts have four geometric characters, obtained
from the two ordinate signs in each real embedding. At a rational tuple
representing actual points, all these characters are real. The original
point and difference guards are retained at every character; this review
does not infer them from a numerical test of one selected point.

In either real embedding the curve is `y^2=x(x^2-delta^2)`, with
`0<delta<=3+sqrt(2)<5`. A real point therefore has `x>=-delta>-5`.
For each of the four reciprocal abscissae and `u>=10`,
`D=1/(x+u)` is strictly between zero and `2/u`. This is valid for
negative abscissae as well. The literal denominator `1+u/x` need not
be positive, but is nonzero; the cleared denominator `x+u` is positive.
For the two comparison tests, `0<=C^2/(1+u*C^2)<1/u`, including `C=0`.

Thus every real detector slot lies strictly between one and
`(1+4/u^3)^6`. Taking the two reciprocal slots proves the stated strict
trace bounds. Both positive factors in
`7*u/(1+u)^2*(1+4/u^3)^12` decrease on `u>=10`.
The exact endpoint inequality gives `0<eta<147/242<1` at every
point character. Hence the complement is a unit in the finite point
algebra, not merely nonzero at the selected rational character.

For either actual contact set, all `a+c` are positive and below `z`
on `a>max(abs(c))`, `z>a+10`. Logarithmic differentiation gives
`u=2k/sum(2(a+c)/(z^2-(a+c)^2))`. Each summand is strictly below
`1/(10-c)`. The independent checker reconstructs the two exact harmonic
sums, both strict lower bounds greater than ten, and the integer margin.
No sampling is used to justify the inequalities for arbitrary real points.

## Native identity and sound nine-coordinate criterion

Independent integer polynomial convolution verifies the factorization

`P_d(1,c)-[2d(1-d)]^2 = d(d+1)^2*(c^2-(1-d))*(c^2+(1-d))`.

Consequently `c^2=1-d` supplies the stated native witness, whose ordinate
is nonzero on the proved completeness real domain. For an arbitrary
rational soundness tuple, a negative odd valuation of `d` is also the
valuation of `1-d`; hence that complement cannot be square. This direct
parity argument includes zero candidate square roots and the prime two.
Outside the source's exceptional set, multiplication of the pole input
by seven does not alter the consumed valuations.

The unchanged extraction and height proof requires ordinary rational
abc and the explicitly retained arithmetic inputs. The point algebra
has rank 64 and one finite quadratic step gives rank 128. Removing the
two free pole parameters leaves input, six point coordinates, physical
slope and encoder, for nine total coordinates. This is a sound source
and a conditional completeness criterion. No coefficient specification
for a new nine-variable definition has been certified.

## Reference-aligned constant normalizer

The replacement `w*=16u/(4+7u)^2` keeps all old guards and adds
`4+7u!=0`. Outside two and seven, the cases `v(u)>0`, `v(u)<0`,
and `v(u)=0` give precisely the valuations stated in the manuscript.
Thus positive odd contact extraction is unchanged. At negative odd
valuations the original balanced detector still gives `W=1 mod p` in
both slots and `V=2 mod p`, so the new pole input has positive odd
valuation. If `v(u)` is even, its parity remains even after division
by either squared denominator. In particular fresh primes of `4+7u`
cannot create a negative odd pole.

The fixed-place preparation uses the unchanged limit `u~z^2/a`, with
`a` a rational square. The new leading weight `16/(49u)` is square.
At two, `v(b*)=4-v(u)` is even and can be made at least four, with
the required square class. At seven, choose even `v(u)<=-4`; then
`v(b*)=-v(u)-2>=2`. All stronger finite depths and real lower bounds
can be fixed before the original prime-pattern call, because no new
constant depends on subsequently chosen auxiliary indices.

On the full auxiliary real domain, `u>=10` gives
`w*<=40/1369` and `0<eta*<294/1369<1`, using the same four-abscissa
bound as above. The added normalizer is positive and independent of
ordinate signs. The original intrinsic-pole existence and guard
avoidance therefore give a complete eleven-variable source variant
under the same premises. No smaller complete variable bound or new
polynomial degree bound follows.

The checker separately verifies `(4+7u)^2-112u=(4-7u)^2`.
This aligns the complement at `V=2`. On the chosen real completeness
domain `u>=10`, every finite guarded actual tuple has `V<2`, since the four nonzero reciprocal-abscissa
factors strictly exceed one. Therefore the reference identity is not
a rational witness on the actual source. Its proposed nine-coordinate
replacement still requires the actual equation
`S^2=V^2-448u/(4+7u)^2` to have a rational solution.

## Independent computation and scope

`check_independent.py` imports neither the producer nor a computer
algebra system. It recomputes the polynomial identities, harmonic
sums, exact rational bounds and integer comparison from its own data.
The producer separately binds the two previously audited source
specifications and checks their metadata and guard labels. Those
metadata checks do not constitute a fresh reconstruction of the full
source circuits or a reproof of the imported arithmetic foundations.

The associated JSON review binds the final manuscript, producer,
certificates, this review and independent checker by SHA256.
