# Approximation by rationally soluble pole levels

**Status:** proved research checkpoint, with an independent root review of the argument. No defining-variable reduction or prescribed-detector incidence is asserted.

Fix a prepared d, put eta=1-d, and choose the fixed n supplied by the retained simultaneous-twist theorem. On the smooth projective genus-one model of
C': V^2=d^3 b^4-d n^2 eta^2,
choose a rational point Q_0=(b_0,V_0) with b_0,V_0>0. Its image (d b_0^2,b_0 V_0) lies on E_(n eta). Take Q_0 as origin and let J be the Jacobian.

The degree-two morphism C'->E_(n eta), translated to send the origin to the origin, is an isogeny. Hence J has rank one. Define
rho(b,V)=V/(d b^2+n eta).
At the chosen positive point rho=r_0 lies in (0,sqrt(d)), and every point of this cover produces one of the rationally soluble levels of the published theorem.

## Finite-prime and real approximation

Let S be a finite set of primes and T a nontorsion rational point of J. Choose an even positive integer L so that [L]T lies in a sufficiently deep torsion-free formal-logarithm neighborhood at each p in S. Put e_p=v_p(log_p([L]T)). Its logarithm is nonzero: otherwise a nonzero multiple of a rational nontorsion point would be zero over Q_p, and thus also over Q.

The closure of
{Q_0+[Lm]T : m in Z}
inside the product of the local cover groups over p in S is exactly
product_p (Q_0+J_(e_p)(Q_p)),
where the indicated formal subgroup is identified by log_p with p^(e_p) Z_p. Indeed the logarithm of [Lm]T is m log_p([L]T), and the same integers are dense in the product of the finitely many Z_p by the Chinese remainder theorem.

After any finite collection of p-adic approximation conditions is fixed, the admissible m contain an arithmetic progression. Its real orbit is still dense in Q_0+J(R)^0: the step is a nonzero multiple of T in the connected circle group, hence an irrational rotation. The even factor L places the step in the identity component. Therefore finite-prime and real approximation hold simultaneously, with infinitely many rational points and avoidance of any finite set of points.

## Neighborhoods in the level coordinate

Write k=d b^2/n. The exact identity
rho^2=d(k-eta)/(k+eta)
gives on the positive arc
d rho/db = 2d^2 eta b/[n rho(k+eta)^2],
which is nonzero. Hence rho is etale at Q_0. By taking L sufficiently divisible, the analytic inverse function theorem makes each local formal neighborhood map onto a ball
r_0+p^(N_p) Z_p,
with N_p=e_p+v_p(d rho/d z_J at Q_0), in the chosen formal parameter.

The connected real arc b>sqrt(n eta/d), V>0 contains Q_0, and rho increases from 0 to sqrt(d) along that arc. Consequently the rationally soluble levels are simultaneously dense in these finite-prime balls and in every real interval contained in (0,sqrt(d)). Every selected level retains infinitely many rational s from the independent first elliptic curve. The combined choices allow finite guard avoidance.

## Exact scope

The prime-adic balls are neighborhoods of one fixed rational lift on the same genus-one cover. The assertion does not cover arbitrary local points on arbitrary fixed twists. It does not make rho equal to an existing detector coordinate, and it does not synchronize levels for two different actual detector inputs.

Density in open neighborhoods does not imply intersection with the required exact algebraic incidence. In particular this refinement does not prove 21 or 9 variables.

Dependencies: the fixed-twist construction in papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex; the elementary local formal logarithm and real group structure of elliptic curves (Silverman, The Arithmetic of Elliptic Curves, Chapters IV and VII). The proof uses the covering curve's Jacobian, not an unjustified lift of all rational points from E_(n eta).
