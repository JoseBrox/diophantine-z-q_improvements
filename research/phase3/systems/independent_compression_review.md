# Independent review of the geometric and denominator obstructions

Reviewed files:

- `../compression/geometric_compression.tex`
- `../compression/denominator_obstructions.tex`

## Geometric density: confirmed

The isomorphism between the two conjugate elliptic curves uses
`u=d/sqrt(N)`, so `u^4 sigma(d)^2=d^2`. An automorphism fixing
`K(i)` and reversing `sqrt(N)` fixes the first point and negates the
second. All geometric endomorphisms are defined over `K(i)`: the
order-four automorphism and complex uniformization identify their ring
with `Z[i]`. Applying this automorphism to a proposed endomorphism
relation makes both terms torsion, which is impossible for a nonzero
endomorphism of a nontorsion point.

The subgroup-closure step is also correct. A proper positive-dimensional
connected subgroup of the product has elliptic-curve projections;
neither can be zero because both coordinates are nontorsion. A dual
isogeny then gives a nontrivial endomorphism relation after multiplying
by the finite component-group order. This contradicts the preceding
argument and establishes geometric density in the surface.

For the concrete point, the depth-one calculation at three was checked
independently through the closed identity

`z(2P) = -2*y*(x^2+D)/(x^4-6*D*x^2+D^2)`.

The reproducible independent implementation is
`check_point_depth_independent.py`. Both rational coefficients of the
displayed formal parameter have valuation one, and `T^2-2` is irreducible
modulo three, so the parameter itself has depth one. The formal-group
argument is valid at this minimal depth: in the short Weierstrass
coordinate `z=-x/y`, inversion is exactly `z -> -z`; multiplication
series are odd. The nonlinear terms of `[3](z)` have valuation at least
three, exceeding the valuation two of the leading term. Repeated
multiplication by three raises the depth by one; multiplication by
integers prime to three preserves it. Thus the point is nontorsion.

The implication for nine independent modules is restricted correctly:
it excludes finite-algebra decoding of their full product from fewer
than eighteen retained parameters. It is not a lower bound of eighteen
variables for a new definition of the integers.

## Denominator tests: confirmed after one finite-exception clarification

The monomial obstruction correctly uses a nonzero vector in the kernel
of the parity matrix and a fresh prime. Negative monomial exponents do
not cause a problem: every output valuation at that prime is even,
whether positive or negative.

The positive-Boolean theorem handles finite exceptional equality
branches, identically false predicates, constant rational functions,
and the case of no denominator predicates. The prime-value lemma is a
valid elementary proof of the needed special case of Schur's theorem.
A simple root modulo a new prime has exactly one lift to a root modulo
its square, leaving a residue class of exact valuation one.

I requested that the bad-branch argument explicitly exclude the prime
supports of rational scalar factors in the denominator factorization
and all coefficient denominators. The author incorporated this change.
The residue classes then give exactly the asserted valuation `-e`, and
CRT simultaneously eliminates every bad branch on an infinite
progression.

For a surviving branch the proposed perturbations `n+M/p^L` are
nonintegers. At the new denominator prime, unit leading coefficients
force the degree valuation formula; divisibility of `L` by every
required exponent makes it admissible. At other new primes the unit
resultants prevent simultaneous numerator and denominator vanishing.
At the finitely many old primes, local constancy preserves the original
valuations. Real continuity preserves positivity and the polynomial
nonzero conditions. The proof establishes infinitely many accepted
nonintegers converging to an accepted integer.

The subsequent strengthening to arbitrary finite Boolean combinations
was also checked. Choose the accepted integer away from the finitely
many zeros and poles of every nonzero rational function in the formula.
A negative denominator literal is then witnessed either by a negative
real value, or by one forbidden negative valuation. Each witness persists
in a neighborhood; adjoining the finitely many relevant primes to the
approximation conditions preserves all negative literals. Identically
zero negative literals are automatically true. The positive-literal
argument and its choice of denominator exponent are unchanged.

## Primary references checked

- H. Pasten, *Bivariate polynomial injections and elliptic curves*,
  Corollary 1.2, arXiv:1811.02416v2:
  <https://arxiv.org/pdf/1811.02416>.
  The stated injection on rational points of an open elliptic square is
  exactly the conclusion in the primary paper. Its geometric generic
  fibers are one-dimensional, so it does not supply the finite-algebra
  decoder prohibited here.
- J. S. Milne, *Abelian Varieties*, corrected author version,
  2 January 2022:
  <https://www.jmilne.org/math/xnotes/AVs.pdf>.
  This is the cited author version of the 1986 chapter, with Sections
  8 and 12 covering the isogeny and endomorphism background.

No original arithmetic input, exact image of a pole system, or absolute
eighteen-variable lower bound is certified by this review.
