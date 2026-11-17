# Cofinite coupling obstruction — independent review points

The polished proof is `cofinite_mobius_coupling_obstruction_20261117_v64.tex`. No repository edits were made.

## New statement

For each fixed coefficient B in the v63 obstructed progression, a positive integer input progression n=1 mod L_B has no guarded prescribed-root witness A=[n]P, simultaneously for every fixed finite exponent and multiplier menu and all twelve Möbius branches. This excludes finite exceptional-input repairs of any coupled polynomial source whose other equations force this exact root. An optional corollary thins the B progression to obtain one input modulus uniformly for all remaining B.

## Decisive checks

- The v63 square gaps make all ten nontrivial quadratic discriminants nonzero rational nonsquares at n=1. Each rational nonsquare has a finite-place obstruction, and every nonzero local square class is open. At 2, use 1+8 Z_2, not 1+2 Z_2.
- For trace continuity, prescribe every place of K over each relevant rational prime, including both split places. Affine coordinates and every relevant nonzero denominator remain defined after shrinking neighborhoods. Initial denominators need not be units; primes of bad reduction are allowed for these continuity arguments.
- Compactness alone gives a close multiple but does not by itself control all subsequent multiples. The proof first chooses small open formal subgroups, then uses their finite index to force every multiple of [L]P into those subgroups. This is valid at bad primes and at 2.
- At each selected good inert contact prime p_e, preserve a_e(n) modulo p_e^2. The initial exact valuation v(a_e(1)-4)=1 then persists, as do the units a_e(n), t_j-1 and the Möbius denominator. The prime lies outside all numerator and denominator supports of the finite multiplier menu.
- The inert-prime contradiction remains uniform in H,U and every other auxiliary coordinate; it uses the unchanged reference translator P, not the varying root A.
- Identity exclusion holds for every positive input and for odd exponents too: [n]P=2[n]R0 is non-torsion, both real abscissas are positive, T_n>6, and a_e(n)>4.
- The root hypothesis is exact A=[n]P. Equality of an index only modulo an unspecified torsion translate is not silently substituted. The paper explicitly limits the consequence for an actual polynomial presentation accordingly.
- Fixed B gives a possibly B-dependent input modulus. Uniformity in B is proved only after further restricting the B progression.

No numerical experiment or computational certificate is needed: the result follows from the v63 finite menu and exact contacts, local continuity, formal subgroups, and finite index in compact local elliptic groups. The paper has not been compiled in this directory; use the root build pipeline for visual checks.
