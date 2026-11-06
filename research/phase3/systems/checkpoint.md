# Phase-three systems checkpoint

All statements in `low_degree_systems.tex` are independent of the proposed
arithmetic definition. The main agent independently read the complete proof
and found no gap in its projection induction, cubic-cone descent, curve
argument, or four-coordinate consequences. The source references have been
checked and documented in `source_notes.md`.

1. A system of at most two quadratic equations in ANY number of coordinates
   has finite rational input image whenever that image lies in the ring of
   integers of a number field. Nonzero guards and finite unions are allowed.
   The proof uses projection from a rational point, the cubic unirationality
   theorem, Siegel's theorem for curves, and induction on the ambient space.
   Singular, reducible, and common-factor cases are included.
2. Therefore a quadratic system defining the ring of integers needs at least
   three independent quadratic residuals after its linear equations are
   removed. This is an equation-count restriction, not a variable count.
3. Arbitrary systems in two total coordinates are impossible. In three
   total coordinates every nonzero residual must have degree at least four,
   and all residuals share a horizontal irreducible factor of degree at
   least four. In four coordinates two coprime quadratic residuals already
   prevent such a definition, even if further residuals have higher degree.
   Consequently all-quadratic systems require at least five total coordinates.

4. `systems_combination.tex` proves that finite systems and single equations
   have the same unrestricted minimum total coordinate count over every
   number field. Over a field with a real embedding, sum of squares doubles
   the degree with no new coordinate. Finite alternatives use a product,
   again without selectors. A generic nonzero guard costs one new inverse
   witness; removing that cost requires an independently proved absorption.
5. The same file proves an exact universal-combiner degree bound: degree two
   is optimal for every number of inputs over a number field with a real
   embedding; for a totally imaginary field it is optimal for 2–4 inputs,
   while degree three is optimal for 5–9. This concerns a combiner valid for
   all residual-value tuples, not necessarily a specific dependent system.
   The degree-three upper bound invokes the separate division-norm theorem.
6. `projection_limits.tex` proves the obstruction to finite-fiber compression
   below the dimension of a preserved source component, and explains why it
   is not an absolute lower bound on an equivalent rational presentation.
   It also proves that the rational-point closure in every definition has
   a horizontal component of dimension at least two.

The main number-fields agent owns the central-division-algebra construction.
The systems section invokes its theorem for degree ceil(sqrt(s)) times the
system degree, and explicitly distinguishes conjunction preservation from
an arithmetic definition after changing fields. No construction with two
to ten total coordinates is claimed here. No phase-two file or git commit
has been changed by this work.
