# Independent audit of the small trace cubic

**Verdict: PASS.** For every rational `0 < w <= 1/4`, the point
`P=(4,4)` has infinite order on

\[
E_w:\quad y^2=x^3-(w+4)x^2+4(w+1)x.
\]

The audited manuscript is
`../independent_route_v56/small_cubic_rank_section_v58.tex`.
The independent implementation is
`check_small_cubic_rank_independent_v58.py`, and its exact output is
`small_cubic_rank_independent_v58_certificate.json`.

## Independent calculation

The calculation uses tangent and chord addition in the exact rational
function field `Q(w)`. It does not use a division-polynomial recurrence.
Curve membership is checked after every addition. The reduced
abscissas have the following degrees:

| Multiple | Numerator degree | Denominator degree | Degree of primitive denominator square root | Leading coefficient of that root |
|---|---:|---:|---:|---:|
| 8 | 32 | 30 | 15 | 1 |
| 10 | 50 | 48 | 24 | 5 |
| 12 | 72 | 70 | 35 | 3 |

Each reduced denominator is a nonzero rational constant times the
square of a primitive integer polynomial. The square root is recovered
directly from the denominator by triangular coefficient comparison,
and its full square is checked. These three independently recovered
polynomials agree coefficient by coefficient with the primitive
division-polynomial arrays produced by the other implementation.

The rational-root theorem excludes a root in `(0,1/4]` for the first
and third polynomials: their reduced root denominators must divide
`1` and `3`, respectively. The second has leading coefficient `5`, so
its only possible rational root in the interval is `1/5`. The
independent direct-denominator polynomial has value

\[
-\frac{55421818556438910529961984}{11920928955078125}
\]

there; its residue modulo three is `2`. This checks possible rational
denominators explicitly, rather than merely testing integer weights.

## Geometric and torsion deductions

The discriminant is

\[
256w(w-8)(w+1)^2,
\]

which never vanishes on the asserted interval. The nontrivial
quadratic factor of the cubic has discriminant `w(w-8)<0`, so `(0,0)`
is the unique nonidentity rational two-torsion point. Mazur's
classification therefore leaves cyclic torsion of order
`2,4,6,8,10,12`. Any rational torsion point consequently has order
dividing at least one of `8,10,12`.

At a smooth specialization, multiplication of the section `P` commutes
with specialization. If `[n]P` specialized to the identity, its
abscissa would have a pole. The independent denominator calculation
shows that this cannot occur for `n=8,10,12` anywhere in the specified
rational interval. This proves the infinite-order assertion directly,
as well as independently validating the manuscript's
division-polynomial proof.

The underlying torsion theorem was reopened in the primary source:
B. Mazur, *Modular curves and the Eisenstein ideal*, Publications
mathématiques de l'IHÉS **47** (1977), 33–186, Introduction,
Theorem (8), p. 35; see also III, (5.1).
[Numdam primary text](https://www.numdam.org/item/PMIHES_1977__47__33_0.pdf).

The checker also verifies the source change of variables

\[
(V+2)\bigl(V^2+w(2-V)\bigr)
=x^3-(w+4)x^2+4(w+1)x,\qquad x=V+2,
\]

and the exact duplication formulas

\[
x(2P)=\frac{(w-3)^2}{4},\qquad
y(2P)=\frac{(w-3)(w^2-8w-1)}8.
\]

## Scope

The proof supplies positive rank for every rational normalized weight
in the interval. It does not prescribe the abscissa of a rational
point. In particular, it does not prove that a rational point has
abscissa equal to `V+2` for the actual detector trace. No new defining
variable bound follows from this rank statement alone.

The independent computation confirms the primitive coefficient
arrays; the separate recurrence implementation additionally certifies
their division-polynomial contents. Both proofs were checked with
their stated scope. No mathematical correction is required.
