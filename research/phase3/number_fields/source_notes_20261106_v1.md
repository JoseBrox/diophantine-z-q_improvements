# Primary sources used in the number-field supplement

All entries were opened and inspected on 6 November 2026. The new
explicit counterexamples, elementary local valuation arguments, and
polynomial computations are proved in the companion TeX files; the
references below support the external structural theorems used.

## J. S. Milne, Class Field Theory, version 4.03 (2020)

URL: https://www.jmilne.org/math/CourseNotes/CFT.pdf

Chapter IV develops simple algebras, modules over division rings,
Brauer groups, and cyclic algebras. The norm construction uses those
standard algebraic facts, while giving its own matrix formula,
integrality proof, local division proof, and coprime-extension proof.
The explicit degree-36 proof over `Q(i)` is elementary and does not
need a hidden appeal to period-index equality.

## Kiran S. Kedlaya, Notes on Class Field Theory

URL: https://kskedlaya.org/cft/

Section 2.4 treats Chebotarev's density theorem, used to choose a prime
that is inert in a cyclic field and split completely in a given normal
closure. Section 7.6, especially Theorem 7.6.12, gives the global Brauer
exact sequence and its local invariants:
https://kskedlaya.org/cft/sec_brauer.html

The supplement uses explicit cyclic primes and a local valuation proof
instead of merely asserting existence from that exact sequence.

## The Stacks Project, Tag 00FE

URL: https://stacks.math.columbia.edu/tag/00FE

Theorem 10.29.10 is Chevalley's theorem: the image of a constructible
set under a morphism of affine schemes of finite presentation is
constructible. Applied over an algebraic closure, this gives the
uniformity obstruction for finite existential formulas. The one-line
input image is finite or cofinite. This argument concerns points over
the algebraic closure, followed by descent of a finite witness tuple
to a finite extension; it does not assert constructibility of the
rational-point projection over a number field.

## Saugata Basu, Algorithms in Real Algebraic Geometry: A Survey

URL: https://arxiv.org/pdf/1409.1534

Section 1.1 discusses real closed fields, including real algebraic
numbers; Theorem 2.1 states quantifier elimination. Used for the
semialgebraic real input projection and its finite interval structure.

## Daniel Plaumann, Real Algebraic Geometry, IHP lectures (2023)

URL: https://wwwold.mathematik.tu-dortmund.de/~dplauman/notes/rag-ihp.pdf

Corollary 4.5 states transfer between real closed fields; Example 4.6
explicitly applies it to solvability of rational polynomial systems
over the reals versus the real algebraic numbers. This supplies a
finite witness field with a real embedding. It does not supply a
totally real field. The separate quartic anchor counterexample is
proved totally real by its explicit polynomial.
