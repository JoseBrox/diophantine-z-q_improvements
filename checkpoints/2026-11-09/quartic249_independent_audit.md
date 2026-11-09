# Independent mathematical audit of the 249-variable quartic

Status: PASS, 9 November 2026. This audit concerns
`papers/quartic_existence/quartic249_20261109_v17.tex`, the literal
`family249_v17` tables, and the independent checker. The stated inherited
arithmetic premises remain premises; this audit does not reprove them.

## Exact algebra

`python computation/quartic/check_quartic249_v17.py` passes with 249 total
coordinates, 223 quadratic equations, and 3192 coordinate monomials.
The quadratic-table hash is
`5bf51acf7575c5ed41d364c8716fd3db7644f2ed8711657a5f28d00ac49302c0`;
the quartic-table hash is
`54f3269832ca3dcf509d1e88d24ff9db7c5eeec49b5278e0f59449bb286115e1`.

The three local-weight equations force q2=q^2, q4=q^4 and q7=q^7
whenever q is nonzero. At q=0 the contact radical is one, so the free
q7 coordinate has no role in soundness; completeness lifts with q7=0.
The independent strata delta=0 and q=0 are correctly separated.

## Scalar guards and local extraction

The inverse of the rational component of g_S excludes S=P. As an
additional exact check, at the chart
h_S=-1+(7/4)sqrt(2), j_S=39/8-(9/2)sqrt(2), the two literal scalar
subtraction rows have zero constant part and coefficient matrix
[[7089/8,-1293],[1293/2,-7089/8]] on (g0,g1). Its determinant is
3245247/64, so both components must vanish. The simultaneous sign
change of h_S,j_S gives the same conclusion.

The eighth-power norm tree has A=(Z0^2+R Z1^2)/R^8 and
W=(A^2+R F^2)/R^8. The pole input is exactly R(R+9792)W^2.
Since R>0 and F=Norm(f(H)) is nonzero, W and the pole input are
strictly positive before any ratio interpretation.

At positive odd nu=v_p(R), distinct valuation parity gives
v(A)>15nu/4, v(F)>13nu/4, v(Z0)>47nu/8,
and v(Z1)>43nu/8. The forced prime first excludes the exceptional
torsion translates of H, without using any stored logarithm ratio.
At a place where H is formal, a point with positive z-valuation is
formal or reduces to (0,0); translation by that torsion point preserves
the z-valuation. The integral group identity then gives the claimed
index valuation. Hence M5(beta)^6 divides c=|a-1| and
h(beta)<=2^330789 c^(7/12). The forced index grows uniformly with N.

## Comparisons and global argument

The valuation classes in all five factors are distinct. The new
weight q^7 has the same necessary residue class modulo four as the
old high weight. Extraction gives the exact required orders
(4,4,4,4) for C2,C3,C4,G; two for I and f(H); one for C1.
All finite reciprocal-abscissa valuations are even.

At least one of h,h-1 is a p-adic unit. Positivity of the cross test
transfers integrality from that full logarithm ratio to the other
ratio before relative formal errors are used as absolute errors.
Plain z has relative error of order four at every nonidentity formal
point. This gives the claimed high comparisons modulo p^4 and input
comparison modulo p, including identity numerator points and inert
primes.

The two-block contact exponent is 7/4. If the Lucas residual is
nonzero its size is at most 14B^4, yielding B^2<=C14^(7/16)B^(7/4)+M2.
The scalar lower bound contradicts this for large N. If the input
residual is nonzero, the exact logarithmic rearrangement is
log B<=4log(2C)+7log 2+7h(beta), contradicted by Lucas growth because
7/12<1.

## Completeness

The fixed compact real neighborhood keeps z(H) bounded away from
zero; choosing the scalar point near O bounds both ratio components.
The source's paired real orbit and finite progression conditions
give these neighborhoods simultaneously. The eighth-power tree then
has W=O(R^-7) and pole input O(R^-12), uniformly for the chosen
neighborhoods and all integral inputs. The finite preparation and
local squareclasses persist, since all new finite depth requirements
are fixed before contact prime selection.

At comparison primes, natural formal depth one gives all parameter
ratio errors order four. Together with the exact Lucas relation this
also gives v(G)>=4. All packed terms have positive valuation on the
selected branch. The opposite branch gives the required trace unit.
The contact degree ten is even, so the nonsquare positive trace scale
introduces no odd denominator valuation. The real comparison input
tends to (408/409)^2/4 in (0,17). All remaining rational charts lift.

No unresolved mathematical gap was found in the new modifications.
