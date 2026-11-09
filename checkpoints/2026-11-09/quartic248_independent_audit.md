# Independent mathematical audit of the 248-variable quartic

Status: PASS, 9 November 2026. This audit concerns
`papers/quartic_existence/quartic248_20261109_v17.tex`. It supplements
the full249 audit and the separately saved forced-prime149 audit.
The inherited modular-realization, elliptic, pole, and prime-pattern
premises remain exactly as stated in the paper.

## Fourth-power scalar tree

For A=(Z0^2+R Z1^2)/R^4 and W=(A^2+R F^2)/R^4, the positive
odd valuation nu of R gives, without cancellation,
v(A)>7nu/4, v(F)>5nu/4, v(Z0)>23nu/8 and v(Z1)>19nu/8.
All exceptional H classes are still excluded by v149(F)>0 before
ratios are interpreted. The same formal-group identity therefore gives
M5(beta)^3 | c and149^L_N | c,
L_N=floor(19(2N-1)/8)+1.
Since149 is outside the radical by definition, the product divides c.

The now independently proved torsion-different refinement is
h(beta)<=C3 M5(beta)^3(1+log M5(beta)), C3=2^330770.
Consequently
h(beta)<=C3*149^(-L_N)*c*(1+(log c)/3).
All constants are fixed independently of N and of the input.

## Strong Lucas growth

When the residual vanishes, write A0=|a|>=7 and
w=sgn(a)(a-2)b. Then t^2-A0*t*w+w^2=1. In the quadratic order
Z[eta], eta=(A0+sqrt(A0^2-4))/2, every positive norm-one unit
is a power of eta: reducing into[1,eta) makes its eta coefficient
an integer in[0,1), hence zero, and leaves the unit1.

Thus |w|=U_j and |t| is U_(j-1) or U_(j+1), j>=1, for
U_(j+1)=A0*U_j-U_(j-1). The congruences
U_j=j mod(A0-2) and U_j=(-1)^(j-1)j mod(A0+2)
show j>=A0-2 if a>0 and j>=A0+2 if a<0. The induction
U_j>=(A0-1)^(j-1) proves
log B>=(A0-4)log(A0-1)>=(c-5)log(c-2), c>=8.
This checks the negative-a signs as well as the smaller root branch.

The comparison detectors still give
log B<=C'+7h(beta) if the input residual is nonzero. Choose N large
enough that7*C3*149^(-L_N)<=1. Its right side is then at most
C'+c+(c log c)/3, strictly smaller than the Lucas bound for all
sufficiently large c. The forced c>=149^L_N makes the contradiction
uniform for every larger N. The earlier Lucas-residual contradiction
is unchanged and remains strict because its exponent is7/4<2.

## Completeness and algebraic scope

At finite places, lowering the fixed normalization power from8 to4
does not obstruct arbitrary depth preparation: both pairs of scalar
test coefficients can still be made arbitrarily small. At fixed real
neighborhoods, W=O(R^-3) and the positive pole input is O(R^-4),
uniformly in the integral input and N. The verified149 preparation
preserves all local squareclasses and square-denominator properties.

The deletion of R^8 changes no point chart or comparison denominator.
The two contact detectors, degenerate strata, residue-class packing,
integrality transfer and order-four formal comparisons are unchanged
from the already audited249 proof. Their simultaneous completeness
continues to hold.

No unresolved mathematical gap was found in these modifications.
The separate independent coefficient reconstruction is being performed
by the few_variables agent; this note does not substitute for that
finite check.
