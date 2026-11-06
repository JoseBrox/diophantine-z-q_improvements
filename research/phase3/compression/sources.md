# Primary sources checked for phase 3 compression

## Daans–Dittmann–Fehm

Nicolas Daans, Philip Dittmann, Arno Fehm, *Existential rank and essential dimension of diophantine sets*, arXiv:2102.06941v5.

- https://arxiv.org/abs/2102.06941v5
- https://arxiv.org/html/2102.06941v5
- https://arxiv.org/pdf/2102.06941
- Checked Corollary4.21 (essential fibre dimension plus one in characteristic zero), Remark8.8 (no one-witness definition of rings of integers), Remark8.23 (MRDP transfer is relative to the existing integrality rank), and Corollary8.24 (polynomial injection plus infinite existential rank would obstruct integrality).
- The HTML identifies arXiv version5 with submission date19 November2025; its typeset date currently reads24 August2026. We cite the version identifier rather than infer a publication date.

## Poonen

Bjorn Poonen, *Multivariable polynomial injections on rational numbers*, Acta Arithmetica145(2) (2010),123–127, DOI10.4064/aa145-2-2.

- https://math.mit.edu/~poonen/papers/QQ.pdf
- Checked Theorem1.1, Remarks1.2–1.5. The number-field polynomial injection is conditional on a non-density hypothesis implied by Bombieri–Lang. It does not give a geometric finite-fibre decoder.

## Pasten

Hector Pasten, *Bivariate polynomial injections and elliptic curves*, Selecta Mathematica(New Series)26 (2020),article22, DOI10.1007/s00029-020-0548-x.

- https://arxiv.org/pdf/1811.02416
- https://link.springer.com/article/10.1007/s00029-020-0548-x
- Checked Theorem1.1 and Corollaries1.2–1.3. Corollary1.2 provides the exact example needed: a surface with dense rational points and a morphism to the line injective on rational points. Its generic geometric fibres have dimension one.

## Hirvensalo

Mika Hirvensalo, *On injective multivariate polynomials over rational numbers*, Theoretical Computer Science1082 (2 September2026),116158, DOI10.1016/j.tcs.2026.116158.

- https://doi.org/10.1016/j.tcs.2026.116158
- https://www.sciencedirect.com/science/article/pii/S0304397526003877
- https://research.utu.fi/converis/portal/detail/Publication/526990307?lang=en_GB
- Checked Definition1 and Theorem2 in the primary publisher text. The actual domain is the bounded set Z[1/p:p in Pi] intersect[0,1]. The abstract's use of “subring” for that set is not used in our statement. The degree is MN; degree12 forPi={5},M=4,N=3.

## Milne

James S. Milne, *Abelian Varieties*, in Arithmetic Geometry(Springer,1986),103–150; corrected author version2 January2022.

- https://www.jmilne.org/math/xnotes/AVs.pdf
- Sections8 and12 supply standard isogeny and endomorphism facts used in the conjugate-twist density argument.

## New self-contained arguments

- `direct_polynomial.tex`: substitution of the Lucas polynomial directly in the approximate logarithmic ratios; retains the same arithmetic hypotheses as the earlier construction.
- `geometric_compression.tex`: dimension obstruction for finite algebra decoding, plus density of the specific cyclic group in its two-dimensional Weil restriction. Exact fixed-curve calculations are reproduced by `check_elliptic_density_data.py`.
- `denominator_obstructions.tex`: full mod2 rank is necessary for monomial aggregation of square-denominator predicates; arbitrary finite Boolean combinations of fixed rational pullbacks of perfect-denominator predicates cannot define Z. The proof first treats positive combinations and then preserves negative literals by finitely many local neighborhoods. Proofs are self-contained and independently reviewed; no novelty or literature-exhaustiveness claim is made.

These references do not resolve the arithmetic assumptions underlying the original claimed integrality definition, and do not prove a two-to-ten-coordinate definition.
