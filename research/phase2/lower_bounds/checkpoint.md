# Phase-two lower-bound checkpoint

Proved in `results.tex`; a second mathematical review by the main agent
confirmed the dense-component, surface-projection, ruled-variety, and
nonnegative-polynomial arguments. The bibliography and primary-source
notes are in `references.bib` and `source_notes.md`; `paper.tex` is a
standalone wrapper including the earlier unrestricted lower bounds.

1. A system of quadratic equations in at most four total variables over a
   number field has finite projection whenever that projection lies in the
   ring of integers. The proof includes reducible/nonreduced intersections:
   a relevant surface component of two quadrics in P4 is either a quadric,
   birational to a cubic surface, or birational to a curve times P1.
2. Consequently any sum-of-squares quartic defining Z over Q requires at
   least **five total variables / four existential witnesses**.
3. A nonnegative polynomial in three total variables with infinite rational
   projection contained in Z requires a repeated irreducible factor of degree
   at least four, hence degree at least eight. Squarefree nonnegative
   polynomials in three variables cannot have such a projection at any degree.
4. Every occurring coordinate, including the input, must have individual
   degree at least two in a defining polynomial.
5. A hypothetical unrestricted quartic with two witnesses must be geometrically
   integral, sign-changing, have Zariski-dense rational points, and have no
   nonvertical rational curve or positive-rank genus-one curve over Q.
6. Weak Bombieri–Lang excludes two-witness presentations with general-type
   projective surface; smooth degree >=5 surfaces are an example. This is
   conditional and does not settle quartic K3 surfaces.
7. A finite family of equations in two witnesses, each of joint witness
   degree at most two but arbitrary input degree, has one of two behaviors:
   a generic rational section makes the union of projections cofinite in
   the field, or its complement contains infinitely many elements of every
   integral arithmetic progression. Consequently it cannot define the
   ring of integers, or any superset of that ring with infinite complement.
   This also excludes such a compression of the semilocal ring
   Z_(2) intersect Z_(3). The full argument is in `conic_obstruction.tex`.

The unrestricted lower bound remains three total variables / two witnesses.
There is no claimed construction at the lower bounds.

The conic specialization proof has received a second mathematical review
by the main agent, including finite Faddeev residues, the degree-one
Chebotarev specialization, bad classes modulo the square of a prime,
degenerate rank-two conics with their only rational point at infinity,
and simultaneous integral Hilbert irreducibility. Its three additional
primary references have been checked in full text; their exact roles and
URLs are recorded in `source_notes.md`. This result is unconditional and
does not depend on the proposed arithmetic definition in the repository.
