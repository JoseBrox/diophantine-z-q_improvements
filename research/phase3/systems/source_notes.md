# Sources and scope for the phase-three systems results

## Sources used in the proofs

1. János Kollár, *Unirationality of cubic hypersurfaces*, J. Inst. Math.
   Jussieu 1 (2002), no. 3, 467–476, Theorem 2.
   <https://arxiv.org/pdf/math/0005146>
   <https://doi.org/10.1017/S1474748002000117>
   The actual theorem was reread: over a perfect field, an irreducible
   cubic hypersurface of dimension at least two which is not a cone is
   unirational iff it has a rational point, equivalently a smooth rational
   point. The proof here first handles geometrically nonintegral factors,
   then handles all cones separately. It never silently applies the
   theorem to a cone. The master bibliography key `lbKollar2002` is reused.

2. Serge Lang, *Fundamentals of Diophantine Geometry*, Springer 1983,
   Chapter 8; DOI <https://doi.org/10.1007/978-1-4757-1810-2>.
   The needed input is Siegel's theorem for integral values of a fixed
   nonconstant rational function on a positive-genus curve. Its reduction
   to the S-integral-point theorem is included in the proof. The master
   key `lbLang1983` is reused.

3. John Voight, *Quaternion Algebras*, Graduate Texts in Mathematics 288,
   Springer 2021, Theorems 14.6.1 and 14.6.9.
   <https://doi.org/10.1007/978-3-030-56694-4_14>
   The first theorem supplies a quaternion algebra ramified at any two
   specified finite places; the second is Hasse–Minkowski over global
   fields. The chapter was read directly, and the master key `Voight2021`
   is reused.

4. Alexander Merkurjev and Raman Parimala, *Quadratic Forms Beyond
   Arithmetic*, Notices AMS 72 (2025), no. 7, 711–718,
   DOI <https://doi.org/10.1090/noti3192>.
   Author manuscript:
   <https://www.math.ucla.edu/~merkurev/papers/quadratic8.pdf>.
   Section 5.1 explicitly states that the u-invariant of a nonarchimedean
   local field and of a totally imaginary number field is four. It is
   used only for the exact quadratic universal-combiner obstruction.
   The official August 2025 AMS issue independently identifies the title,
   authors, volume and opening page:
   <https://www.ams.org/journals/notices/202507/202507FullIssue-optimized.pdf>.
   The new bibliography entry is in `references.bib`.

## What is proved independently here

The two-quadratic obstruction in arbitrary ambient dimension is proved
directly by a rank-zero/rank-one/rank-two projection induction. No general
classification theorem about singular intersections of quadrics is
assumed. The low-degree hypersurface lemma proves the needed statement
for arbitrary regular input functions on open subsets, not merely for
linear coordinate projections. This distinction is necessary after
projecting from a rational point.

The main agent has independently read the complete proof and found no
gap in the projection induction, cubic-cone case, curve argument, or
four-coordinate consequences. This review is recorded in `checkpoint.md`.

The division-algebra construction for general numbers of residuals is
owned by the separate number-field supplement:
`../number_fields/division_norm_compiler_20261106_v1.tex`, theorem
`thm:division-norm-conjunction-phase3`. The systems supplement invokes
that theorem and proves only the substitution, degree, and minimal-variable
consequences. The 72-degree example is an exact conjunction-preservation
claim, not a definition of a new number field's ring of integers.

## Restrictions and nonclaims

There is no construction in two to ten total coordinates in this lane.
Multiple equations have exactly the same unrestricted minimum coordinate
count as one equation; over Q their degree can be doubled with no new
coordinate. Inequations are not free: the generic inverse construction
adds one coordinate unless a separate absorption lemma is supplied.

The geometric dimension barrier concerns finite-fiber projection of a
specified component. It is not a proof that the current 43- or 41-variable
construction has minimal variable count. Rational-point loci may be
smaller than the geometric hypersurface, and positive-dimensional fibers
can sometimes be deleted if rational lifting is independently proved.
