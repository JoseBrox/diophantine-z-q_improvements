# Nested parity selector (v122)

**319 rational unknowns, 268 quadratic residuals; one native pole; twelve certified integers.** This is a projection-equivalent replacement in the v121 ordinary-rational-abc system, under exactly its retained arithmetic premises and sufficient fixed shift. It does not claim a bijection of all auxiliary zeros.

## Proof

Use the notation and retained-prime lemma of [v120](../abc_mean_shifted_curve_v120/README.md) and the exact [v121 table](../exact_multiroute_elimination_v121/abc_quadrics.json). At each retained good prime p and in each local slot, v(u)=1, v(c)=-1. Put R=slotR, t=conj(h_U+h_U^{-1}), e=C0-mu, so the unchanged registers unitT2 and primaryE2 store t^2 and e^2. The inverse of h_U is still enforced. If h_U is a unit in the conjugate slot then v(t)>=0 (including t=0); otherwise v(t)=-|v(h_U)|<0. The three terms of R have distinct classes modulo four, as proved in v120, so v(R)>0 exactly when the three original formal-group tests pass; otherwise v(R)<0. Zero has valuation +infinity.

Instead of multiplying the three separately computed Boolean selectors, define

    A = R^2 + u*t^2,
    V = A^2 + c*e^2,
    chi*(1+V) = 1.

At a retained slot the two summands of A, if nonzero, have even and odd valuations. Their valuations cannot coincide. Both are strictly positive precisely when R passes and t is integral. Otherwise the minimum is strictly negative. Thus v(A)>0 in the first case and v(A)<0 otherwise. The same argument for V yields v(V)>0 precisely when those two tests and v(e)>0 pass. Otherwise v(V)<0. In particular the residue of chi is exactly 1 when all three old tests pass and 0 otherwise; chi is integral and its denominator cannot vanish at a retained slot. Every downstream Boolean, weight, variance, signed-abscissa, radical and height argument is unchanged. For nonretained primes, the pole denominator soundness does not require integrality of chi.

For completeness use the very same choices of integer labels, common points and contact slope in v120. At each chosen prime the same successful slot and failed slots give the required residues, with 1+V nonzero. At prepared places and over the reals, as the slope tends to infinity, u tends to infinity in absolute value, c tends to zero, R tends to zero, and t stays bounded and nonzero (the same finite exceptional point loci as for the old unit selector are avoided). The bounded C0 and mean give bounded e. Thus A grows as u*t^2, V grows as A^2, and chi tends to zero. This is the only limiting property of the former selector used in the downstream Z0 and BB-pole preparation. Away from the selected and prepared primes, square-denominator parity of the physical pole input follows from its square factor as before. The same BB point theorem finishes the witnesses. There is no new condition on contact primes or the source.

## Exact table

Delete the eight coordinates chi0, chiU, chiE, chiP over Q (four K-fields) and their defining rows. Keep chi, replace its two rows, and add the four rational coordinates of A,V and their four rows. All equations displayed above are quadratic when unitT2 and primaryE2 are kept. The table preserves the other 262 residuals by literal monomial renaming. Thus 323-8+4=319 and 272-10+6=268. The sum of squares has exact degree four, since unchanged quadratic terms remain. The source table is pinned by its Git blob hash.

Run `node undecidability/abc_nested_selector_v122/build.mjs` to verify exact regeneration (or add `--write` to regenerate). The coefficient generator was executed in the connector's JavaScript environment; the independent finite valuation grid is a sanity check, not a substitute for the parity proof. No full repository CI run is claimed.
