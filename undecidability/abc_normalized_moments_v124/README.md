# Exact normalized moments (v124)

**309 rational variables, 257 quadratic residuals**. This is a bijective rational-zero-set projection of v123, not a change of its arithmetic assumptions or completeness argument. In particular ordinary rational abc, the retained elliptic/prime-pattern inputs and the Jones coding source are unchanged.

Write (a) for the positive contact center, (u c=1), (r_i) for the twelve derivative coefficients, (S=\sum_i r_i), (L=\sum_i r_i X_i), (D_i) for the scalar failures, and μ for the exact mean. The old equations are
```
au=a*u, au*S=12,
L=sum r_i*X_i, M2=sum r_i*X_i^2,
12*mu=au*L, var=au*M2-12*mu^2,
F=sum r_i*D_i, J=au*F.
```
Keep L and replace the other equations by
```
a*S=12*c,
mu*S=L,
var*S=12*(sum r_i*X_i^2-mu*L),
J*S=12*sum r_i*D_i.
```
All four are quadratic since the X_i^2 registers already exist. The first equation, together with u*c=1, implies a,S nonzero and recovers au=a*u=12/S. The second and third give the original mean and variance since L=mu*S; the fourth gives the original J. Conversely all new rows follow from the old rows by multiplication and substitution. Restore the three deleted coordinates uniquely by their defining expressions. This establishes projection equivalence even at zero values of individual derivative coefficients or source integers.

The table removes n_au, n_mX2 and n_failSum_0 and replaces seven equations by four; all other 253 equations are preserved by renumbering. The sum of squares has exact degree four. The sufficient shift remains ineffective, and the twelve certified inputs and the single BB-native pole are unchanged.

Run `node undecidability/abc_normalized_moments_v124/build.mjs` to compare the complete generated table against its pinned v123 predecessor (`--write` regenerates it). The generator checks full variable support, degrees and exact counts. It was executed against the predecessor in this continuation; no full repository CI run is claimed.
