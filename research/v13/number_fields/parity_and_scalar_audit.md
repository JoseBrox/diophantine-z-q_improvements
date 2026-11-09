# Independent local audits

Date: 9 November 2026.

## Quartic parity reduction

Audited `work/v13/quartic/even_local_tests_20261109_v13.tex`.

The new local implications are sound. At an unramified good odd place of
`y^2=x^3-Dx`, a nonunit abscissa has even valuation: the dominating term
is x cubed when v(x)<0 and -Dx when v(x)>0. Thus finite valuations of
the reciprocal abscissa are even, also after conjugation.

For each proposed factor, the finite nonconstant term valuations have
exact powers of two divisors 1,2,4,8. The minimum, including the constant
term of valuation zero, is unique. Each factor is nonzero, has
nonpositive valuation, and reduces to 1 whenever that valuation is zero.
Zero test values simply remove the corresponding terms.

The cleared trace equations give a nonzero trace reciprocal. If ell is
the maximum valuation of W above the contact prime, then
`v_p(b) <= nu+2*ell`, and this valuation is odd. The retained pole
obstruction therefore forces nu>0 and ell>-nu/2. At a place attaining
ell, the nonpositive factor valuations imply that every factor has
valuation at least ell. All terms at that same place have valuation
greater than -nu/2. The respective exponents force comparison orders
40 and 10, reciprocal-abscissa order 20 for H by evenness, and positive
even valuations for all the order-one branch tests. This is a common
place for all sixteen tests, rather than separately chosen places.

For the depth improvement, put h=m/2 when H=mR0+T with T two-torsion.
At an odd prime, h and h-1 are both integral and one is a unit.
The exact logarithm relations show that the corresponding full index
ratio is integral, and the analytic correction factors are units.
Positive cross precision transfers integrality to the other ratio.
Only then does the primary approximant z(U_i)/z(H) show depth at least
10 for every nonzero U_i. Its logarithm error has precision at least
40; zero numerator points have exact zero error. This avoids circular
use of the improved depth. The same reasoning handles half-integral
h and inert places. Formal denominator logarithms are nonzero by the
formal-logarithm isometry and the prior nontorsion exclusions.

The original completeness depths make every new term positive at the
selected primary place. At the opposite place each factor is either
of negative valuation or is 1 in the residue field, giving trace
reduction 1 or 2. Every new weight is a positive power of q, so the
existing finite-denominator preparation and real limit remain valid.

One editorial issue was communicated to the author: nonvanishing of a
rational approximant does not by itself imply nonvanishing of the
analytic formal logarithm. The paper should explicitly distinguish
the two justifications; the later formal-logarithm isometry provides
the correct analytic justification. This does not affect the circuit.

This audit verifies the changed local mathematics. The source arithmetic
premises remain conditional, and complete row/support verification is
provided separately by the quartic producer and its independent checker.

## Amplified 279-coordinate variant

The additional changes described in `build_quartic279.py` and
`check_quartic279.py` also pass the local mathematical audit.
For r=4 the contact polynomial has degree 20, and the normalization is

`R=F20/(a^20*delta^22)`,
`e=(a*delta)^20/F20`, `q*delta^2=e`.

Consequently `e*delta^2=1/R`, so the modified cleared trace row is
correct. Fixed-prime preparation gives
`v(q)=18v(a)-2v(lambda)`, tending to positive infinity as the fixed
square denominator is enlarged; at the real embeddings,
`q ~ a^18 lambda^-2`, tending to zero through positive values.
The same zero-stratum argument applies because 1 is not a contact and
the radical at 1 equals 1.

The new H term `q^10*f(H)^2` forces v(f(H))>4.75*nu; evenness gives
v(f(H)) at least 6 and formal depth at least 3. The integrality-first
argument above therefore gives primary relative precision at least 12.
The quadratic Taylor polynomial

`G2(w)=1-(2/5)w-(2/15)w^2`

has relative precision at least 12 at every nonidentity formal point.
The constant approximant G0=1 has relative precision at least 4,
sufficient for the order-three input comparison. Its numerator
`15-6w-2w^2` has roots `(-3±sqrt(39))/2`, neither in Q(sqrt(2)).
Thus the new global approximant denominator is nonzero. The independent
split-prime 17 certificate is valid as well: any local root would be
integral because the leading coefficient is a unit, whereas the
residue polynomial has no root.

The proposed five factors retain distinct term valuation classes and
the same common-place trace argument. Their extraction orders are 12
for the high comparisons, 3 for the input comparisons, 6 for f(H),
and positive for the other formal-branch tests. Multiplying five
nonpositive factor valuations rather than four changes no step.

The amplified height exponent is alpha=19/4. With residual order 12,
`4*alpha/12=19/12<2`; with input order 3, `2*3>alpha`. The coefficient
of h(beta) in the logarithmic index bound is
`alpha/(2*3-alpha)=19/5`. Hence the same sublinear scalar-height
estimate gives eventual soundness. The new sufficient coefficient
threshold remains ineffective: 27464 cannot be asserted to suffice
for this amplified variant without a new effective global estimate.

No hidden global nonvanishing issue was found. This is a mathematical
audit of the changed implications, not a replacement for the supplied
complete row and coefficient reconstruction.

## Scalar resultant normalization

Audited the odd-valuation lemma and surrounding normalization in
`work/v13/few_variables/uniform_scalar_normalization_20261109_v13.tex`.
The displayed J^4 argument is valid but can be sharpened substantially.

For p not 2 or 3, put u=v_p(rho(X)), v=v_p(h(X)), and suppose u is odd.
Then `v_p(rho-6h^2)=min(u,2v)`. If a resultant Bezout identity supplies
`min(u,v)<=j`, then

`2j+u-2min(u,2v)>0`.

Indeed, for u<=j this is at least 2j-u>0. Otherwise v<=j. If u<2v,
oddness gives u<=2v-1, and the expression is at least 1. If u>2v,
oddness gives u>=2v+1, and the expression is at least
`2(j-v)+1`. Equality u=2v is impossible. Thus the square of a
resultant already removes every negative odd valuation.

In this application all exponents of X in both rho and H=512h are
even. Write rho(X)=rho_tilde(X^2), H(X)=H_tilde(X^2), and put

`J0=Res_Y(rho_tilde,H_tilde)`.

The standard substitution identity gives the original
`J=Res_X(rho,H)=J0^2`, while Bezout for the smaller polynomials,
evaluated at Y=X^2, gives `min(u,v)<=v_p(J0)`. It follows that the
original J, rather than J^4, suffices in the fixed scalar multiplier:

`c_*=102^6*J`.

It is positive and a rational square. The fixed-prime depth is then
`L+v_ell(J)` and remains a positive odd integer because J is a square.
The real normalization bounds, local squareclasses, and index bound
`v_ell(c)>=19L+1` are unchanged. The reduction affects coefficient
size only; it is not a variable reduction. This improvement was sent
to the scalar-paper author before changing the deliverable.

The other key scalar checks pass: the real denominator is strictly
negative by its positive shift; its resultant is nonzero; the small
prime bounds follow from parity at 2,3 and the nonsquare unit 6 at 17;
and all finite-path norm-tree inequalities place each normalized leaf
above valuation -nu. The real boundedness argument does not resolve
the separately stated divisibility by variable elliptic reduction
orders, so the paper's remaining finite-place condition is essential.

The author has incorporated this improvement with cleaner notation:
the final paper calls the smaller Y-resultant J and uses `102^6*J^2`.
Its checker independently verifies the 15 by 15 resultant, the product
of five quadratic-factor formulas, and equality of its square with the
original 30 by 30 resultant. Thus the final notation is equivalent to
the reduction proved above.
