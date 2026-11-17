# Independent audit: the prepared E_791 covering obstruction

**Result: PASS.** The manuscript
`../independent_route_v56/negative_results/prepared_q0_sha_counterexample.tex`
proves that the prepared input `d=112/225` has an everywhere locally
soluble, but rationally empty, one-coordinate specialization. This audit
does not assert that this value is realized by an actual detector tuple.

## Literature conventions independently checked

I reopened the primary sources:

- Zhangjie Wang, *Congruent Elliptic Curves with Non-trivial
  Shafarevich-Tate Groups*, arXiv:1511.03810v2, Sections 2.1–2.2,
  equations (2.1)–(2.3) and the radical statement following (2.3):
  https://arxiv.org/pdf/1511.03810.
- Shenxing Zhang, *On non-congruent numbers as multiples of
  non-congruent numbers*, 28 August 2025 manuscript, Sections 2.1–2.2:
  https://zhangshenxing.github.io/publications/Zhang2025.pdf.

Both use the Kummer triple `(x−n,x+n,x)` and the three conics printed in
the audited manuscript. Wang orders the Monsky vector by `(d1,d2)`;
Zhang orders it by `(d2,d1)`. The independent checker deliberately uses
Zhang's block order. Its matrix is `diag(0,0,1,0)`, the block swap of
the manuscript's `diag(1,0,0,0)`. Both give pure 2-Selmer dimension three.
The tangent-plane Hilbert-symbol convention and Mordell–Weil inclusion
in the pairing radical are exactly the stated source results.

## Exact local pairing audit

For `Λ=(1,7,7)` and `Λ'=(113,1,113)`, the three tangent forms are exactly
the gradients at the listed rational conic points divided by 14. In
particular no sign or coordinate-order correction is needed.

The partner identities are polynomial consequences of the first and
third conics:

\[
(u_2-u_3)(u_2+u_3)=113t^2,
\]
\[
(226t+3u_1-17u_2)(226t-3u_1+17u_2)
=-(17u_1-21u_2)^2/7.
\]

At a prime outside `{2,7,113}`, primitive integral projective
coordinates prevent both members of either partner pair from
vanishing modulo the prime. In the second case the relevant determinant
is `−226`. Each tangent valuation is therefore even. This proves the
local Hilbert factor is one at **every** such prime, including 3 and 17;
it is not a finite-prime search or an implicit good-reduction assumption.

At two and seven, 113 is a local square; at infinity it is positive.
At 113 the exact point `(0,−sqrt(7),−1,1)`, with `sqrt(7)≡32`, gives
tangent product `45 mod113`. Its Legendre symbol is minus one.
Thus the global Cassels pairing is minus one.

## Rank and class exclusion

A nonzero alternating form on the three-dimensional pure Selmer space
has one-dimensional radical. Its Mordell–Weil image gives rank at most
one. The exact point `P=(−784,−2940)` has pure Kummer class
`(113,113,1)`, which is nonzero. The manuscript's torsion argument is
valid: none of the nonzero 2-torsion classes is trivial in full descent,
so there is no rational 4-torsion; odd torsion is divisible by two.
As a separate cross-check, the good reduction orders are
`#E(F3)=4`, `#E(F5)=8`, confirming that rational torsion has order four.
Hence the rank is one and P generates the free part modulo two.

The abscissa square-class image is exactly `{1,−1,791,−791}`. The class
`−7` is absent. The exact map

\[
z^2=7(113^2-t^4)\longrightarrow E_{791},\qquad
(t,z)\longmapsto(-7t^2,7tz)
\]

therefore proves rational emptiness, including the separately excluded
zero-coordinate and infinity cases.

The checker also verifies the prepared normalization, quartic
discriminant support `{2,7,113}`, all tangent gradients, both partner
identities, the 113-adic residue, the full and pure Kummer classes, and
the complete three-dimensional Monsky kernel. It does not implement or
replace the cited general Selmer and Cassels-pairing theorems.

## Files and reproduction

Run `python checkpoints/general_scalar_v56/check_prepared_q0_independent.py`.
It writes `prepared_q0_independent_certificate.json`, which returns
`PASS`.

The obstruction is specific to the uniform `q0=0` prepared-input route.
It neither excludes a suitably restricted actual-detector family nor
rules out another one-coordinate pole equation or the 21/9 objectives.
