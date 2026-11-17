# A height obstruction for labels on the growing Pell conics

**Status:** proved checkpoint statement, with the stated scope; not a new defining-variable bound. The originating exact checker passed before the execution outage. Publication to main awaits the normal independent-review and integration workflow.

For an integer s with |s|>=3, set a=s^2, A=a(a-2), B=(a-2)^2 and
F_s(t,b)=t^2-A bt+B b^2-1.
This is a smooth geometrically integral conic.

## Algebraic label bound

Let fixed G in Q[s,t,b,Y]. Divide by the monic F_s in t:
G = F_s H + G_0(s,b,Y)+tG_1(s,b,Y).
Let d be the maximum Y-degree of the remainder. For y=u/v in lowest terms, v>0, multiply by a fixed common coefficient denominator and by v^d, obtaining p(b),q(b) in Z[b].

For every integral pair (t,b) satisfying F_s=G(s,t,b,y)=0, b is a root of
N(b)=p(b)^2+A b p(b)q(b)+(B b^2-1)q(b)^2.
Indeed N is the quadratic norm of p+tq, since the two roots of F_s have sum A b and product B b^2-1.

If G(s,t,b,y) does not vanish identically on the specialized conic, N is nonzero. The algebra Q(b)[t]/F_s is a field, so a zero norm would force p=q=0. Its coefficient height is at most
C_0(1+|s|)^D max(|u|,v)^(2d),
for constants depending only on G. Its nonzero integer leading coefficient has absolute value at least one. The integer-root bound therefore gives
log|b| <= 2d h(y)+D log(1+|s|)+C
whenever b is nonzero. This includes degree drops and y=0.

## Growth of the integral Pell solutions

Put z=(a-2)b. The equation is t^2-a t z+z^2=1.
The elementary Lucas descent gives, for b nonzero,
|z|=U_j(a)
for some positive integer j, where U_0=0, U_1=1 and U_(j+1)=a U_j-U_(j-1).
The same classification and descent are proved in the retained few-variable manuscript.

Modulo a-2 the recurrence has parameter two, so U_j(a) is congruent to j. Since a-2 divides z, j is a positive multiple of a-2. The recurrence gives U_j(a)>=(a-1)^(j-1). Consequently
log|b| >= (s^2-3)log(s^2-1)-log(s^2-2).

If h(y)<=C_1|s-1|^theta+C_2 with fixed theta<2, this contradicts the preceding upper bound for sufficiently large |s| unless the specialized G is identically zero on its conic.

## Rational labels

Let y=R(s,t,b) be a fixed rational function, with its denominator retained nonzero. Clearing that denominator gives G=N_R-YD_R, so d<=1. If R is nonconstant on the generic conic over Q(s), a nonzero two-by-two minor of the reduced coefficient vectors of N_R and D_R excludes constant specialization outside finitely many s. Thus this rational label cannot meet the stated subquadratic height bound on unbounded scalar indices.

If R is constant on the generic conic, R lies in Q(s). The conic has the rational point (1,0), so its function field over Q(s) is a purely transcendental field in one variable.

## Fixed fibers of algebraic labels

If G is not divisible by F_s, only finitely many rational y can have integral solutions with b nonzero and unbounded |s|.

For a fixed y, a nonzero reduced coefficient polynomial in s remains nonzero outside finitely many s. The integer-root upper bound is then O_y(log|s|), contrary to the Lucas lower bound. Therefore an unbounded fiber requires G_0(s,b,y)=G_1(s,b,y)=0 identically in s and b. A nonzero coefficient polynomial in Y of the generic remainder has only finitely many such rational roots y.

## Application and limits

The retained scalar source uses theta=7/6. Hence a fixed nonconstant rational invariant of its existing Lucas coordinates cannot replace the independent input label while retaining unbounded scalar preparation. Nor can a fixed nontrivial algebraic label relation retain such unbounded fibers for every rational or integer input.

This statement does not exclude a redesigned norm equation, including norm=beta(X)^2; an additional free arithmetic parameter; or a scalar-only label with a different reduction-order preparation. It supplies no 21- or 9-variable definition.

## Reproduction record

Before the outage the checker verified 9 resultant identities, 24 Lucas-growth fixtures, 756 coefficient/integer-root checks and 108 constant specializations. Canonical TeX SHA256:
9f79d9ef50c1699aeb68a757dc2f97c2028721c90727df63796fb0fdd09001a2.

Local source paths, if recovered:
checkpoints/general_scalar_v56/negative_results/low_height_pell_labels_v61.tex
checkpoints/general_scalar_v56/negative_results/check_low_height_pell_labels_v61.py
checkpoints/general_scalar_v56/negative_results/low_height_pell_labels_v61_certificate.json

Mathematical dependencies: the elementary Lucas descent in papers/few_variables/few_variables_20261108_v8.tex and the scalar height bound in papers/pole_parameters/precision_transfer_20261117_v56.tex. The finite fixtures supplement the proof above.
