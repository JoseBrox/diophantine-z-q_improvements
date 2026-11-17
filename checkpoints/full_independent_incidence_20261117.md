# Fixed-slope finiteness for fully independent source points

## Proved extension, independently audited

Let A=Res_{Q(sqrt2)/Q} E, E:y^2=x^3-(3-sqrt2)^2*x.
Then End_Q(A)=Z and A is Q-simple. This does not require the retained
rank-one assertion about E(K).

Proof: over K, A=E×E^sigma. Set d=3-sqrt2, d'=3+sqrt2, dd'=7.
The isomorphism over K(sqrt7) is

    (x,y) -> (7*x/d^2, 7*sqrt7*y/d^3).

Seven is not a square in K(i). An automorphism fixing K(i) and negating
sqrt7 negates this isomorphism and fixes every CM endomorphism in Z[i].
Every geometric homomorphism E -> E^sigma is its composition with a CM
endomorphism, so Hom_K(E,E^sigma)=0. Since K is real, End_K(E)=Z.
Galois swaps the two diagonal endomorphism rings; End_Q(A)=Z. Poincare
complete reducibility implies Q-simplicity.

Fix the rational input, the slope, and all defining constants. In block0
the contact value/physical weight and comparison scale are then fixed.
On its prepared positive domain, all detector factors are at least one.
For any positive-dimensional Q-abelian translate in A^p meeting the guard
domain, choose a simple A-direction. Its coordinates are multiplication
by integers forming a primitive vector. At least one coordinate is odd.

The conditional tested point roles are H,U,H-P,U-A0; the general roles
include every U_i and U_i-Q_i. Their coefficient forms span all point
coordinates modulo two. Consequently at least one tested point is an
odd multiple of the A-direction plus a fixed real point. Odd multiplication
is onto A(R). Make both real slots of that tested point approach (0,0),
avoiding the proper restricted guard divisors. Its reciprocal abscissa
diverges in both slots. Positivity forces both reciprocal detector slots
to zero, hence their trace tends to zero. At a guarded real point it is
strictly positive. The actual trace is therefore nonconstant on every
positive-dimensional Q-abelian translate meeting its domain.

For any fixed smooth genus-one trace curve B, apply Mordell-Lang to the
incidence V_actual(H)=g(Q) inside A^p×B. Hom_Q(A,B)=0. Any positive
Q-abelian subgroup either contains a B-direction, contradicting
nonconstancy of g, or a nonzero A-direction, contradicting the preceding
trace theorem. Rational subgroup closures descend to Q, so geometric
cosets do not evade this argument. Thus there are only finitely many
guarded rational source tuples at fixed input and slope, allowing every
point index to vary independently and all rational points of B.

This includes the three small elliptic trace tests and fixed finite
elliptic menus. It does not assert emptiness. The untwisted conic,
point-dependent curve coefficients, and jointly varying slope/point
tuples remain outside the theorem. Established counts remain25/13/71;
21/9 are not proved.

The polished manuscript and independent audit are being completed in
independent_route_v56/negative_results and general_scalar_v56. Primary
sources verified: Milne, Abelian varieties, Proposition12.1; Gao–Ge–Kühne,
The uniform Mordell–Lang conjecture, Theorem1.1 and equation(1.1),
Publications Mathématiques de l'IHÉS143(2026),189–235.
