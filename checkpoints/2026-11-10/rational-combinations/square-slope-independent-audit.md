# Independent audit of the square-norm corollary

The corollary in paper blob 53b30f034445daace36bf9deb7e7ec0a8430f081 is valid.

Let alpha be the chosen simple root of a(X)-1 and let
L=Q(alpha,sqrt(-2)). Choose a nonzero primitive algebraic integer eta
for L/Q. Such a generator exists: multiply a primitive element by a
suitable nonzero integer, and translate first if necessary to avoid
zero in degree one. Its minimal polynomial g is monic, nonconstant,
separable, and has nonzero constant term.

Schur's elementary prime-divisor argument gives infinitely many
primes p where g has a root modulo p, even after excluding any
specified finite set. Exclude p=2, the discriminant of g, all earlier
bad primes, and all fixed coefficient and denominator exceptions.
Every remaining root is simple. Hensel lifting yields a Q-algebra
embedding L -> Q_p. This one embedding simultaneously supplies the
images of alpha and sqrt(-2); separate unrelated choices of roots are
not being assumed.

All original formal inverse coefficients belong to a fixed
localization of O_{Q(alpha)} and remain integral at the selected
embedding. The two selected leading coefficients remain units because
their norm primes were excluded. No infinite new set of exceptional
primes appears on passing to L.

Write zeta for the image of sqrt(-2). Since zeta^2=-2 and p is odd,
zeta and 2*zeta are p-adic units. For the desired local parameter
lambda_*=-1+p^mu, the polynomial
S^2-(lambda_*-1) has the simple residue root zeta modulo p.
Hensel's lemma gives s_* in Z_p with
s_*^2=lambda_*-1.

For M>max(mu,nu), choose an integer s congruent to s_* modulo p^M.
Then lambda=1+s^2 is congruent to lambda_* modulo p^M. Arbitrarily
large lifts of s give lambda>1 and s!=0. This parameter is a sum of
two integer squares, namely 1^2+s^2, and lambda-1 is an integer
square. The separately chosen half-integral X jet is unaffected.
The unit denominators and integral coefficients preserve both exact
contact depths; the unique formal inverse branch preserves the
integer-linear valuation formula for the arbitrary rational function
Psi(X,lambda).

Thus all the main theorem's conclusions, including the p-unit input
residual and arbitrarily large depths, remain valid under this stronger
restriction. The prime set may be replaced by the infinite set selected
through L.

No use of Chebotarev is required. No square root of -2 over Q is
asserted or needed: the square root is used only in Q_p, and the
eventual integer s need only realize a finite congruence.

This remains an obstruction to a uniform local parity implication.
It does not exhibit a false solution of the full Diophantine source
or prove an absolute variable-count lower bound.
