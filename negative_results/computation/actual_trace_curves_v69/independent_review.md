# Independent review of the v69 actual-trace curve and family theorem

Date: 17 November 2026. Reviewer: `height_and_fields`, independently of the author.

**Status: PASS.** The reviewed manuscript is
`curves_and_abelian_families_20261117_v69.tex`, SHA256
`9cae2d87fb33bee15951cd82c718887f8818e77f0870fdae85e4eaf56cffd9cd`.
This review concerns the stated fixed-input geometric obstructions. It does not prove global rational realization, exclude all rational witnesses, or change a defining-polynomial coordinate bound.

The final typography change replaces five occurrences of `mathscr X` by `mathcal X`; reversing precisely those substitutions reproduces the previously reviewed source hash `6c48f3dddce551d25fec7947bf7d2be7a74469177d22d374767d7f28e30774e7`. No mathematical change is included in that repinning.

## Arithmetic surface and low-genus curves

The conjugate-twist argument proves nonisogeny over `K(i)`, not over an algebraic closure. Negating `sqrt(7)` fixes every geometric endomorphism of the j=1728 curve and negates the displayed isomorphism to its conjugate. Thus it negates every homomorphism between the two curves, giving a zero fixed subgroup. An elliptic subvariety of the rational Weil restriction cannot project nontrivially to both conjugate factors, and neither single factor descends. Hence the rational surface is simple; its powers have no rational elliptic abelian subvariety. Independent elementary point counts give 20 and 16 points at the specified good prime 17.

A genus-one curve need not have a rational point for the Jacobian argument: its difference map induces a rational homomorphism from its Jacobian. This is precisely the scope of Milne, Chapter III, Proposition 6.4 and the preceding paragraph, which I checked in the author PDF. A geometrically integral rational curve with constant projection has a rational constant point. Consequently its remaining map is into a fixed double-cover fiber. Riemann–Hurwitz then excludes normalization genus zero or one; Faltings applies to every remaining fixed curve. The finite singular locus and intersections of conjugate components account for nonnormal and non-geometrically-integral curves. Finite chart covers have finite fibers and do not create a contracted curve.

## Derivative detector and its guards

The eighteen contacts are distinct for `a>10`. At each, `u'=±18`; the reciprocal product has positive order in each slot, and the radicand has first term `2u`. This yields eighteen simple branch points and genus at least eight, regardless of cancellation between the trace slots. The claimed four nonzero reciprocal tests are consistent with the actual retained derivative circuit: `unit_norm_v28/build_sources.py` inverts both point coordinates, and its `difference()` explicitly guards the norm of the abscissa difference. The last two comparisons may vanish.

The infinity expansions give `u~z^2/a`, reciprocal products tending to one, and radicand tending to four. The two rational infinity points and the local-square argument, including the `1+8Z_2` condition at two, are valid. These points and the eighteen branch points do not meet the guarded affine source. Local solubility here does not impose the source's selected-prime preparation or imply a global rational witness.

## Abelian families

A rational reference map from an abelian variety over `Q` extends and is a homomorphism followed by translation; rational simplicity makes it constant or surjective. In the surjective case, simultaneous zeros of the two reference tests are the inverse image of a point in the two-dimensional surface. The fiber has codimension two, so no prime divisor is contained in that common zero set. In each geometric slot, at least one reference test therefore has valuation at most zero at every prime divisor.

At a positive odd order `nu` of the derivative weight argument, parity gives
`v(D_i)=max(2v(C_i),−nu)` and
`v(1+D_i^2/u)=min(0,2v(D_i)−nu)`.
Every factor has nonpositive order, and one reference factor in each slot has order at most `−nu`. Thus `v(V)≥nu`, while the radicand has exact order `nu`, contradicting a square. Cancellation in the trace strengthens this conclusion.

Every contact fiber consequently has even multiplicity. Since there are eighteen contacts, their product has an even divisor, including its poles. The resulting quadratic cover is finite étale (or trivial). After passage to a connected component over `C`, it is an abelian variety. The direct complex-torus argument in the manuscript is valid and avoids reliance on a problematic arrow in the cited lecture notes. Its nonconstant map to the fixed genus-eight hyperelliptic curve is impossible by the Jacobian embedding and the translation-homomorphism theorem. This argument fixes the root point as well as the input; it leaves constant slopes unexcluded in the derivative source.

## The two-trace general source

I matched the displayed first detector to `reweighted_elliptic_detectors_20261116_v53.tex` and the square radicand to `trace_conic_criterion_20261117_v57.tex`. Its first scale is exactly one, so fixing the input fixes the scalar and all ten contact values even while all nine point roles vary.

The ten values in `(2+Theta) union (4+Theta)` are distinct and avoid `−1`. Their contact function has simple zeros. For a fixed point tuple,
`G_k=R^(kappa+2) S_k/(1+R S_k)` and therefore
`G_k^2/w^(2kappa−1)` has order at least five. Only the two nonzero reference reciprocals are needed for the field factors. Thus `V0=O(w0)` and `C0=2w0+O(w0^2)` give ten simple branch points and genus at least four. Zero numerator tests do not invalidate the argument.

For a varying abelian family, at an odd contact divisor every field or scalar factor has nonpositive order because its second summand has odd order. The reference-pair codimension argument supplies one factor of order at most `−nu` per slot. Hence the radicand has exact odd order. The product of ten contact functions has even divisor; the resulting étale abelian cover would map to a genus-four curve. This proves that the common slope is constant without fixing any root point. The second square equation can only restrict the locus; every component of a fixed two-square fiber maps finitely to the first cover.

The three small-class multipliers are units at the contact valuations. They therefore preserve both arguments, including finite menus.

## Primary references checked

- Milne, *Abelian Varieties*, v2.0 (2008), Chapter I, Theorem 3.2 and Corollary 3.7; Chapter III, Proposition 6.4 and preceding paragraph. https://www.jmilne.org/math/CourseNotes/AV.pdf
- Faltings, *Endlichkeitssätze für abelsche Varietäten über Zahlkörpern*, Invent. Math. 73 (1983), 349–366. Original paper opened; the Mordell implication is recorded in its introduction. The precise smooth-projective curve statement and normalization qualification were also checked in Milne, Chapter IV, introduction. https://doi.org/10.1007/BF01388432

The review establishes the written implications using these standard theorems. The finite arithmetic checks are supporting calculations, not substitutes for the general parity, Jacobian or étale-cover arguments.
