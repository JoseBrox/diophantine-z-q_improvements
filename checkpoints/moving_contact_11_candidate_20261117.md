# Moving-contact eleven-coordinate candidate — audit in progress

This is a research checkpoint, not an established defining theorem.
Current published general counts remain25/13; ordinary-abc quartic71.
The original21/9 actual rational-square realization is still unproved.

## Candidate source

For conditional input X, root point A, beta=X^2+B and T=Tr x(A), set

    M=beta^e+T^e, a=M^8, t=a^2-z^2,
    c in {-4,-3,-2,-1,1,2,3,4},
    F=product_c((a+c)^2-z^2), D=-partial_a F (holding z fixed),
    u=F/D, w=u/(1+u)^2,
    D_i=C_i^2/(1+u*C_i^2),
    W=product_i(1+D_i^2/u), V=Tr(W^-1), b=4w/V^2.

The C_i are the six actual conditional detector tests, including the
symmetric final comparison. Retain one full intrinsic pole block for7b.
All displayed nonzero denominators and existing point guards are retained.

Formal coordinate census: input1, three K-point pairs6, z1, two intrinsic
pole parameters2, finite-algebra encoder1: total11. This census alone is
not a defining theorem.

## New normalization identity — exact local proof

If nu=v_p(u) is odd and c=v(C_i), parity prevents cancellation in
1+u*C_i^2. Therefore

    v(D_i)=max(2*c,-nu).

For nu>0, v(D_i)>0 is equivalent to v(C_i)>0; the pole trace argument
therefore recovers every original test at a consumed positive odd prime.
For nu<0, v(D_i)>=-nu>0, so v(D_i^2/u)>=-3*nu>0. Every detector slot
is1modp and V=2modp. Odd denominator primes of u are automatically safe,
even if some original C_i has a pole.

For u>0 in every real character, 1+u*C_i^2>0 and
0<=D_i<=1/u. Hence W>=1 and W-1=O(u^-3) uniformly on real tuples.
No new rational coordinate is used for these normalizations.

## Proposed height argument

Write x=a-z,y=a+z, G(X)=product_c(X+c), soF=G(x)G(y), xy=t.
Under ordinary abc, for fixed eight shifts, the product of primes having
valuation exactly1 in the reduced numerator of G(x) has log at least
(8-4-2epsilon)h(x)-O(1). The squareful prime support of G(y) costs at most
(2+epsilon)h(y)+O(1). Choose the branch of larger rational height.

Simple primes are recovered byu except mixed-order collisions (charged
to the squareful support of the other branch), or equal-order derivative
cancellation (charged to the squareful support of the fixed resultant
product(2M^8+c_i+c_j)). The latter support is bounded by
(2+epsilon)h(M)+O(1), independent of8 in its coefficient, by applying
polynomial abc to AB*product(2A^8+s_i B^8). A zero shift needs separate
numerator/denominator support bookkeeping.

The claimed candidate bound is

    log r_odd^+(u) >= (8-6-3epsilon)/2*h(t)
                         -(4+epsilon)*h(M)-O(1).

Every coefficient and omitted-prime charge is under independent audit.
With d=16, e=4 and kappa near1, the sharp signed-height coefficient
Q=(2kappa-1)/(16-kappa*10) tends1/6. The expected contraction is
Q*(C+1+1/(2alpha))<gamma, alpha=e/kappa-3, approximately11/12<1.
Do not claim this parameter row until the complete radical proof is checked.

## Ordered completeness to audit

For integer input fix A=[X]P and M before all prime choices. Choose z>a+4
using the16 Sun positions z±(a+c), with all position numerators prime.
Avoid fixed primes dividing coefficient differences and resultants.
Each selected contact then has v(F)=1 and D a unit. Deep source-index
preparation gives the actual C_i positive at the chosen place.

At infinity, D~16*a*z^14 and u~z^2/(16a), so
w~16a/z^2=(4M^4/z)^2. Symmetry makes D=a times a polynomial in a^2,z^2.
At every fixed denominator place of a, choose z p-adically dominant.
At other denominator primes of z, its leading monomial is unique and
has even valuation. This should make the reduced denominator ofD square
in the prepared family. Odd positive valuations ofu then occur only at
selected contacts; odd negative valuations are safe by the normalization.
The square leading term supplies the original fixed-place pole preparation.

Agents general_scalar_v56 and independent_route_v56 are independently
auditing height and completeness respectively. single_cover_realization_v56
is writing the proposed full theorem. No completed11-variable result yet.
