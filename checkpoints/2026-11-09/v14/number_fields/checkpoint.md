# Number fields: finite correspondences and exceptional fibers

Date: 9 November 2026. All statements below are unconditional consequences
of the semiabelian Mordell--Lang theorem. No point-stability hypothesis,
Diophantine definition of Z in Q, or Vojta conjecture is used.

## Main theorem: finite values on geometric fibers

Let k be a number field, A/k an abelian variety, V/k a variety, and
pi:V→A a morphism. Let h:V⇢P1 be a rational map, evaluated on its
domain. Suppose that for each a∈A(kbar), the set of finite values of h
on the geometric fiber over a is finite. Then for every finitely
generated multiplicative subgroup U⊂k*,

    h(V(k)) ∩ U is finite.

In particular this applies whenever pi is quasi-finite, including
finite covers and all their open subsets. The finiteness assumption is
geometric; merely having finite rational fibers is insufficient for
the proof.

### Complete proof mechanism

Restrict to the locus on which h is defined, finite, and nonzero.
Its image W under (pi,h) is a constructible subset of A×Gm by
Chevalley's theorem. Every geometric fiber of W→A is finite by
hypothesis. Let Sigma consist of the actual image points with
h-value in U; it lies in the finitely generated group A(k)×U.
Let Z be the Zariski closure of Sigma, not the closure of all of W.

Semiabelian Mordell--Lang says that Z is a finite union of translates
of connected algebraic subgroups. This follows also by applying the
integral-point statement to Z and a fixed model containing the given
finitely generated group. Disconnected subgroups may be split into
their finitely many connected translates. All arguments can be made
after base change to kbar; torsion translates cause no exception.

Every connected subgroup of A×Gm is B×{1} or B×Gm. Indeed its
projection to A has kernel either Gm or finite. In the first case it
is the full product with its image B. In the second case it is finite
over B and hence proper, so its morphism to Gm is constant; the
identity forces that constant to be 1.

If an irreducible component of Z were a translate of B×Gm, then
Sigma would be dense in that component after removing the other
components. The constructible intersection W with that component
would therefore contain a nonempty open subset. Such an open subset
has an infinite geometric fiber over some point of B, contradicting
the finite-fiber hypothesis. Thus each component has constant Gm
coordinate. There are finitely many components, so Sigma has only
finitely many distinct second coordinates, as required.

## Consequences stronger than omission of integers

For any a,b∈k with b≠0 and any finitely generated U⊂k*, the image
also meets a+bU in a finite set, by applying the theorem to (h-a)/b.
Finite unions of such constructions and added finite sets preserve
this property. In particular all but finitely many a+b·2^n are
omitted. No such construction contains an integer arithmetic
progression, so it cannot supply Z⊂S⊂M^(-1)O_k for any fixed M.

The complement satisfies weak approximation over k. Given target
neighborhoods at finitely many places, choose a∈k approximating
their centers, choose nonzero b sufficiently divisible at the given
finite places, and choose a rational prime q below none of those
places. Then a+bq^(-n) stays in the prescribed finite-place
neighborhoods, and tends to a at every archimedean place. Only
finitely many terms belong to the image, so arbitrarily large n
give the desired complementary values.

## Generically finite maps and the exceptional locus

For a generically finite morphism pi:V→A, the quasi-finite locus
V_qf is dense open. The theorem applies to V_qf. Consequently all
but finitely many values in any fixed affine multiplicative sequence
that are represented at all must be represented by witnesses in
V\V_qf. This locates the necessary escape in positive-dimensional
geometric fibers; it does not exclude such fibers.

A useful stronger specialization: if an output t satisfies
F(a,t)=sum_i c_i(a)t^i=0 with regular coefficient functions on an
open part of A, then away from the common-zero locus of all c_i
there are only finitely many output values over each a. Therefore
all sufficiently large represented powers must lie above that
common-zero locus. A monic output relation has no such locus, so
no additional existential witnesses can make it represent all Z.

## Sharp counterexample for merely generically finite maps

Let E:y²=x³+9 and consider the affine surface

    V: y²=t³s³+9,   z²=s³+9.

The morphism pi:V→E_aff×E_aff sends
(t,s,y,z) to ((ts,y),(s,z)). Over s≠0 it is an isomorphism onto
the open subset x2≠0, with inverse t=x1/x2. Thus it is birational
and generically finite. At s=0, y,z may independently be ±3;
each of the four resulting affine lines permits every t∈k.
Therefore the regular output t maps V(k) onto k.

The surface is smooth: on s≠0 this follows from the isomorphism;
on s=0 the y,z Jacobian columns have nonzero diagonal entries
2y,2z. It is irreducible: every irreducible component of the
two-equation locus in A4 has dimension at least two, whereas its
s=0 part has dimension one, and the s≠0 open is irreducible.
Its non-quasi-finite locus is exactly s=0. This is a chart of
the blow-up resolving the abscissa ratio at the four base points.
Even when E(k)=E(Q), the exceptional fibers introduce arbitrary
k-valued outputs; they do not give a bounded-denominator set.

## Verified primary sources

- P. Vojta, *Integral points on subvarieties of semiabelian varieties,
  I*, Invent. Math.126 (1996),133--181, DOI10.1007/s002220050092.
  Author bibliography confirms publication details:
  https://math.berkeley.edu/~vojta/bib.html.
- P. Vojta, *Nevanlinna theory and Diophantine approximation*, MSRI
  Publications37 (1999),535--564, Theorem2.2, especially the
  closure formulation on p.542. Primary author exposition retrieved:
  https://library.slmath.org/books/Book37/files/vojta.pdf.
- P. Corvaja and U. Zannier, appendix by D. Masser,
  *Rational and integral values of rational functions at rational
  points*, arXiv:2608.28255v1, Theorems1.1,1.10 and §4.
  https://arxiv.org/html/2608.28255v1.

The present conclusions extend the rational-map obstruction to
geometrically finite correspondences by adding the constructible
image argument. They are applications of established arithmetic
theorems, not claims of a new proof of Mordell--Lang or of a
counterexample to general Diophantine definability of O_k in k.
