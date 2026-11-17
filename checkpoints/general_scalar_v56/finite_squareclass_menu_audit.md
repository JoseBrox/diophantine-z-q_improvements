# Independent audit: a fixed finite menu of native square classes

## Statement and local proof

Let `S` be the fixed exceptional set of the native detector theorem.
Choose, once and for all, a finite nonempty set `D` of distinct positive
squarefree integers whose prime divisors lie in `S`. The same statement
holds for positive rational `S`-unit representatives after replacing
them by these equivalent squarefree integer representatives.

Replace the native requirement `R in Q^{*2}` by

\[
[R]\in\{[d]:d\in D\}
\quad\Longleftrightarrow\quad
\exists d\in D:\ dR\in\mathbb Q^{\times2}.
\]

At a hypothetical negative odd valuation of the physical pole input
`b=4w/V^2` at `p` outside `S`, the native proof gives
`v_p(R)` negative and odd. Each `d` is a unit at `p`, so `dR` has the
same odd valuation and cannot be a rational square. Therefore the
entire finite menu retains native pole soundness and all subsequent
source soundness arguments. The set `S` and the menu must be fixed
before the input and witnesses are chosen.

## Finite algebra and all characters

Write `R=N/D0` on the retained guarded point algebra and put `M=N D0`.
The guard already makes `M` a unit. The menu is encoded by

\[
P(Y)=\prod_{d\in D}(Y^2-dM).
\]

This is monic of degree `2m`, where `m=|D|`. A rational character of
this extension is exactly a rational character of the point algebra
with one allowed square class. At every prepared real character,
`M=R D0^2>0`; hence all `2m` roots are real and nonzero.

Its discriminant is

\[
\operatorname{Disc}_Y P
=4^m\Bigl(\prod_i d_i\Bigr)
 \Bigl(\prod_{i<j}(d_i-d_j)^4\Bigr)
 M^{m(2m-1)}.
\]

Thus the extension is etale on the existing guard locus. No additional
nonzero source condition is required: the `d_i` and all nonzero
differences are fixed rational constants. The direct finite-algebra
rank is multiplied by `2m` for one block and by
`(2m_0)(2m_1)` for two independently chosen blocks.

### A fully specified encoder without a new separation argument

The separator printed in the existing v28 unit-norm paper is written
for quadratic generators. It cannot simply be quoted verbatim for
the new degree-`2m` generator. One may either extend that separator
using the displayed discriminant or use the following simpler finite
disjunction, which already proves the coordinate count.

For each menu choice, apply the existing quadratic encoder with
radicand `dM`. Let its polynomial be `F_d(x,U)` and use the same
encoder variable `U` for all branches. Then

\[
F(x,U)=\prod_{d\in D} F_d(x,U)
\]

has a rational zero exactly when some allowed branch has one. For two
blocks take the product over `D_0 x D_1`. Every branch has the same
retained source coordinates and one encoder coordinate; the finite
product introduces none. All branch polynomials still have value one
at `U=0` on the norm-guard failure locus and before the optional
conditional input factor. Their degrees and coefficient bounds grow,
but the coordinate census does not.

This proves the same formal censuses: **21** for the two-block general
source and **9** for either two-block conditional source or the
one-block mixed-height conditional candidate. It proves no realization
for any of these sources. A defining bound still requires an actual
rational tuple in at least one menu class at every required integer
input, with all other source conditions retained.

## Avoid an unnecessary restriction in the realization statement

The new realization property should retain the actual detector
equations and the whole-character real and guard locus. It need not
retain optional old neighborhoods forcing the radicand to be locally
square at every exceptional prime. If `R` is square in every `Q_p`
for `p in S`, and its positive rational square class is supported on
`S`, its valuations at all primes are even, so its class is already
one. In particular the added class `2` gives no new witness on a
locus that still requires `R in Q_2^{*2}`. Allowing the menu can be a
strict relaxation only when the corresponding optional preparation
restriction is also relaxed. Soundness outside `S` is unaffected.

## Exact check

`check_finite_squareclass_menu.py` checks the discriminant formula for
menus of sizes one through four by direct symbolic discriminants.
The logical pole argument and finite-disjunction equivalence above
are proofs, not conclusions inferred from those examples.

## Repository sources audited

* `papers/pole_parameters/native_square_criterion_20261116_v53.tex`,
  native valuation obstruction, positivity, and finite-algebra section.
* `papers/finite_algebra/unit_norm_20261114_v28.tex`, single determinant,
  separator, and rational-character theorem.
* Recovery `single_cover_criterion_20261116_v55.tex`, its rank-128
  quadratic extension and unresolved realization property.
