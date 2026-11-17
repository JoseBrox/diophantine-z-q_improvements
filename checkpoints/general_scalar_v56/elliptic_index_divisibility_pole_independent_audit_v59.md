# Independent audit: the two-point elliptic index pole test

Reviewed source:
`../independent_route_v56/elliptic_index_divisibility_pole_v59.tex`.

The arithmetic soundness and completeness arguments pass. The source
must use the fixed cyclic subgroup stated in its hypotheses. Its newer
weak4/3 formulation should take the fixed generator in4E(Q), as required
by the strengthened primitive denominator theorem.

## Soundness

At a simple primitive denominator prime p of H=[h]P, outside the fixed
exceptional set, q_H has valuation−1 and u=c/q_H has valuation1. For
D=C²/(1+u C²), valuation(D)=max(2 valuation(C),−valuation(u)) whenever
valuation(u) is odd. Every factor1+D²/u has nonpositive valuation.
If U is not formal at p then C=1/x(U) has nonpositive valuation,
so W has valuation at most−1 and b=4uW²/(1+u)² has negative odd
valuation. The intrinsic pole equation excludes this. Thus U is
formal and the reduction order of P, exactly|h|, divides j.

Adding other detector factors cannot undo this negative valuation.
The finite exceptional-index restriction is a fixed nonzero product
guard. No extra free coordinate is required for that restriction.

## Completeness for a prescribed integer quotient

For U=[m]H and integer m≠0, positive odd valuations of u occur at
formal primes of H. Integral formal multiplication gives
valuation(1/x(U))≥2 valuation(u) and
valuation(ζ(U)/ζ(H)−m)≥valuation(u). Thus all detector factors
are units at these primes. At negative odd u-valuations the balanced
transform makes every factor a unit without any point condition.
At even u-valuations the valuation of b is even regardless of
cancellation. These facts prove a square reduced denominator.

The fixed choice c=q_0 L² with valuation2(L)=2 and
valuation7(L)=−1 prepares the remaining hypotheses. In a sufficiently
small finite-place neighborhood of the fixed P, u is a local square,
valuation2(u)=4, and valuation7(u)=−2. At2 the tests have sufficient
formal depth. At7,−1 is not a square, which prevents the otherwise
possible equal-valuation cancellation in1+u C². Therefore
valuation2(b)=6 and valuation7(b)=2. The scalar L can be chosen
large in the real embedding, while keeping its two prescribed local
valuations. Real u>50 implies0<b<1/7 uniformly for both listed tests.

A rational square root q_H is selected coherently by the duplication
formula on a fixed rational half-point. Arithmetic progressions of
multiples return arbitrarily close to that half-point in its real
component, while retaining the finite-place congruences. This gives
infinitely many admissible h for each fixed m. The intrinsic density
theorem then avoids the finitely many additional radicand guards.

## Encoding and scope

The square-abscissa image characters are real at the prepared values,
and u is positive and independent of the ordinate signs. This gives
the asserted detector guard avoidance on every image character.
An eventual compiled source should audit a chosen finite-isogeny
cover explicitly: some preimage characters can be nonreal, even
though their image-point detector values are real. The present
arithmetic statement does not claim a completed compiler census.

The optional comparison only imposes local congruences with j/h.
The weight class is independent of the external X at fixed H,U,
so small rational perturbations of X persist. Accordingly this
source alone does not define the integers and gives no new complete
variable bound. This limitation is correctly stated in the draft.
