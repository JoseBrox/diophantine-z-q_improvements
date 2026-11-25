# 25 November continuation: 162/177 quartics and remaining routes

## Established transfers

The [harmonic-scalar reduction](../computation/harmonic_scalar_20261125/README.md)
and [uniform-anchor rechart](../computation/depressed_scalar_20261125/README.md)
reduce the two non-abc quartic records from 163/178 to 162/177, under
the same retained arithmetic premises. The latter gives the specified
177-variable polynomial at C=331^26, with 149 quadratic residuals,
3,008 expanded monomials, 1,923-bit coefficient height and 72,580 bytes.
An exact independent BigInt replay of both pinned harmonic tables and
their two replacements verified 2,782 and 3,025 parameter-separated
terms, respectively. The specialized expanded 177-variable TXT was
parsed and checked coefficient by coefficient. All 331 residue
classes of the anchor prime passed. A reproducible standard-library
Python verifier is supplied; the executed replay used independent
JavaScript BigInt arithmetic. Neither is a new audit of all inherited
arithmetic premises.

## A 52-coordinate candidate: complete contact preparation, insufficient height margin

This is **not** a new defining polynomial. Keep all 45 pre-contact
coordinates and the gate/pole of the
[53-variable theorem](../computation/reciprocal_gate53_20261124/README.md).
Use the same midpoint a=M+16, x=a-z, y=a+z, and G(t)=P(t^2)
from the [asymmetric contact proof](../computation/asymmetric_contact54_20261124/README.md).
Try instead

    A=G(x), H=G(y)/y^4, c=H/A+3/H, u=1/c.

There is a seven-coordinate contact circuit (z,r_x,r_y,s_x,s_y,F,H):

    r_x=x^2, r_y=y^2, s_x=r_x^2, s_y=r_y^2,
    u F=P(r_x), H s_y=P(r_y),
    F H=H^2+3uF.

As in the parent P is evaluated quadratically using r and s.
The nonzero P(0) excludes y=0. If either F or H vanishes, the
last row and u != 0 force both to vanish, hence G(x)=G(y)=0.
That contradicts x+y=2a>32 and the old roots in [-8,8].
Thus F=cA, and division recovers the stated contact weight.
The parent unit row already guards c. This circuit uses one
fewer contact register and no new guard coordinate.

For the ordered integer witnesses, retain the same sixteen-prime
supplier, finite avoidance, and successful-slot depths. At selected
x-primes the two summands have valuations -1 and 0; at selected
y-primes they have valuations 1 and -1 (exclude 3). At nonselected
integral slope primes outside the enlarged fixed set, A and G(y)
are units. If y is a unit both summands are integral; if v(y)>0
the first summand has negative even valuation, the second positive
even valuation. At slope infinity c ~ 4/z^4, with integral
relative expansion coefficients outside the fixed exceptional
primes. Thus at nonintegral slope primes outside that set c has
positive even valuation. At the fixed finite places the supplier
allows sufficiently large local slope, and c tends to zero;
at two it lies in the squareclass of 4/z^4. At positive real
infinity c tends to zero through positive values. The preceding
reciprocal gate preparation applies verbatim to these cases,
including foreign negative odd valuations of u via its true
multiplication identity. This gives integer completeness under
the parent's premises.

Soundness is not proved. At a simple x-contact, writing k=v(H),
the competing depths are k-1 and -k. Failure can only occur for
positive even k. At a simple y-contact, writing l=v(A), depths
are 1-l and -1; discard l>=2 (at l=2 cancellation is possible).
The parent's ordinary-abc simple and multiple support estimates
therefore give only

    log r^+_odd,S(u) >= max((4-2eps)h(x)-(2+eps)h(y),
                             (4-2eps)h(y)-(2+eps)h(x))-O(1)
                       >= (1-3eps/2)h(M)-O(1).

Here h(x+y) <= h(x)+h(y)+log 2. The old comparison upper bound
uses 2h(X) <= (1002/997)h(M)+O(1), so the strict margin is lost
even in the limit eps->0. A sharper joint collision estimate
or a stronger input-height estimate is needed. This is a
limitation of the proved estimates, not a counterexample to
integrality of the 52-coordinate candidate.

## Frontier and scope

* General unrestricted and specified unrestricted remain 25 and 27.
* Ordinary-abc and both weak-abc unrestricted routes remain 11.
* Ordinary-abc quartic remains 53.
* The new quartic records are 162 and 177, not unconditional claims
  independent of the project's retained arithmetic premises.

The affine elimination method from the undecidability branch does
not immediately yield eliminations in the old 163/178/53 tables:
the quadratic parts have full row rank modulo a tested prime at
the tested parameter specialization. This only rules out constant
linear combinations cancelling the quadratic parts at that
specialization, not general nonlinear chart changes.

The ico cap still lacks completeness for all integers. Independent
BB pole coordinates cannot be identified on the basis of the
separate pole existence theorems; an actual joint realization
argument is required. No count has been lowered merely by
assuming those missing assertions. Further investigation should
focus on a strict height margin in the 52-coordinate contact
chart, shared pole realization with the required squareclasses,
and a different route to an all-integer quotient cap.
