# Linear rational normalization: local theorem and remaining completeness audit

This is a research checkpoint, not an asserted improvement of the defining polynomial. The completed publication uses Psi_z(D)=z D^2/(1+z D^2), K=A=7, and 25 variables with degree below 2^87.

## Local consequence

Define Phi_z(D)=zD/(1+zD), with every denominator guarded. For arbitrary integral normalized valuations,

v(Phi_z(D)) <= max(0,v(z)+v(D));

if v(z)=0, positive valuation is equivalent to v(D)>0 and then equals v(D). The equal-valuation cancellation case only lowers the valuation.

Use E=z^4 Phi_z(C), G=w^4 Phi_w(S), R=zw, denominator exponent4, and a product of factors1+R(E/R^4)^2 and1+R(G/R^4)^2. The same trace pole exclusion gives vE,vG >13(vz+vw)/4 when vz+vw is odd. At comparison valuation nu=vw>0 odd and mu=vz even:

- If 0<=mu<=nu, vC>(13nu-7mu)/4. For nu1, mu0, integer rounding gives vC>=4; for nu>=3 the bound is larger.
- If mu>nu, vS>(13mu-7nu)/4>=19/4, giving vS>=5.
- If mu<0, negative mu+nu is impossible and positive mu+nu gives stronger comparison extraction.

At an odd scalar valuation mu>0, the other balanced contact function is a unit, and vS>13mu/4>=4. The forced index bound c>=ell^(3L+1) survives. These inequalities would retain the existing global fourth-power radical proof.

## Remaining completeness requirements

At a selected comparison prime, linear normalization of inactive scalar tests fails to be automatically integral only when v(R)+v(S)=0. Since v(R)=1, it suffices to exclude v(S)=-1 for all six rational scalar components.

A plausible preparation imposes primary formal depth v(z(H))>=2, with only first formal depth for H-P at the conjugate place. The rational components of f(H) are then integral. Exclude the fixed denominators of f(S-P) and z(S-P). The two rational components of z(S-P)/z(H) have valuations at most-2: the primary term has that negative valuation, while the conjugate term is a unit. Thus none of the six values has valuation-1.

The additional congruences h=0 modulo the selected rational primes must be compatible with every opposite reduction order. This needs a precise application of the proved quantitative separation of prime values beyond the Hasse errors, not merely the earlier odd coprimality of elliptic reduction orders. The resulting real and finite-place simultaneous realization must also be checked.

Unlike the quadratic normalization, 1+rho C need not be positive at a real embedding. One must prove that all new denominator zero sets can be avoided in the required compact cyclic neighborhoods. Positivity of each final product factor still follows once its denominators are nonzero and rho R>0. A complete avoidance proof, source reconstruction, independent certificate, and degree calculation are not yet supplied.

No new variable count or degree bound follows from this checkpoint alone. The anticipated gain is in the degree of the existing25-variable family, not its variable count.
