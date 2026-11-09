# Few-variable research checkpoint — 2026-11-09

## Verified scope

The attached v11 papers count the distinguished input. Their results are 27 total variables with degree below 2^154 and an ineffective sufficient odd coefficient exponent, and 29 total variables with degree below 2^161 and a specified exponent 137731. The input-projection statements retain the explicitly listed elliptic group/height, contact-height, pole obstruction/realization (including restricted-converse/descent), and prime-pattern hypotheses. The finite algebra compression itself is unconditional.

The 27-variable source retains 26 rational coordinates: input; nine pairs of square-root abscissa components; one comparison slope; two pairs for comparison poles; one pair for the scalar pole. There are nine independent quartic point roots and three quadratic pole roots, hence finite algebra rank n=2^21. The explicit 29-variable source has one additional comparison-pole pair and one additional quadratic root, hence n=2^22. A final one-coordinate finite algebra theorem adds the 27th/29th coordinate.

## Audited compression and bottleneck

The finite algebra theorem uses a separating element G(1+sum ell^i z_i), with 0<=ell<=m*n*(n+1)/2, and n degree cases for det(I-V M). Its factor count is n*(1+m*n*(n+1)/2), before any source branching. The global derivative resultant makes the selected nonzero spectrum simple, which is essential to recover a rational character from a rational eigenvalue. The elementary eigenline, adjugate trace, reciprocal, and degree-drop arguments appear internally sound. No new variable reduction is proved at this checkpoint.

For point charts alone, all quartic discriminants and nonzero roots are automatic at every rational retained base point. The pole quadratics can be nonreduced on some other geometric branches; the source guard contains their roots, and the theorem correctly discards those inactive branches. A deterministic primitive element would substantially lower degree if all relevant discriminants and guard norms could be made globally invertible. That stronger condition is NOT established, and requiring a norm of a guard to be nonzero can exclude a valid rational branch when another branch is singular or inadmissible.

## Promising approaches under investigation

1. Improve the finite algebra elimination degree at unchanged variable count, especially avoid all-spectrum separation and/or the n degree cases.
2. For a totally real tower, an explicitly dominating linear form can separate sign choices, but this must handle complex residue factors at invalid base points and guards vanishing on unrelated branches. Assuming all factors are real merely because one rational point exists is invalid for these quartics.
3. A simultaneous-square polynomial can combine independent nonzero rational square roots using coefficients dominating all ratios of their absolute values. This offers a specialized route, but the pole radicands depend on the earlier point roots, so the independent-radicand argument is not yet a valid replacement for the full compiler.
4. Reducing retained pole parameters by fixing one parameter would require a new uniform arithmetic realization theorem for a lower-dimensional subfamily. It cannot be inferred from current pole solvability.

## Small exact simplification (not yet a claimed new bound)

For one degree case H_d(V) with constant term 1 and g=a_d Res(H_d,H'_d), the polynomial H_d(gU) automatically excludes g=0 and U=0. Thus reciprocal reversal is not logically necessary: combine H_d(gU), coefficients a_k for k>d, and the adjugate traces R_i(gU) by a sum of squares. This gives the same rational projection with the same one coordinate. Its quantitative advantage has not yet been computed; it does not remove the dominant selector/degree branching.
