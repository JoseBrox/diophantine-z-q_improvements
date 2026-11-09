# Number fields: finite correspondences and exceptional fibers

Date: 9 November 2026. The finiteness theorem follows unconditionally
from semiabelian Mordell--Lang; the genus-one extension also uses
Siegel and Merel. No point-stability hypothesis,
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

## Bounded outputs from unirational fibers

A nonconstant rational function f∈k(T) has values with arbitrarily
negative valuation at infinitely many finite places. For a polynomial,
use arguments of very negative valuation outside the coefficient
exceptions. Otherwise choose an irreducible denominator factor H.
Schur's elementary prime-divisor argument applied to a cleared norm
polynomial N_{k/Q}(H(T)) supplies infinitely many primes having a simple
local root of H, after excluding discriminant/resultant primes. Hensel
lifts that root, the coprime numerator is nonzero there, and weak
approximation gives k-arguments arbitrarily close to the pole. Removing
finitely many arguments changes nothing.

Consequently a nonconstant rational function on a k-unirational variety
cannot have uniformly bounded denominators on all its rational points
in the domain: compose a dominant rational parametrization with a
suitable k-line and use the preceding lemma.

Suppose pi:V→A has geometrically integral fibers, and each fiber with
a k-point in the domain of h is k-unirational. If h(V(k)) has bounded
denominators, h must be constant on every such soluble fiber. Let W
be its constructible graph image in A×A1. The locus of a for which
W_a is finite is constructible, by constructibility of fiber dimensions
(Stacks, tag05F9, applied to a finite locally closed decomposition of W).
All actual output points lie over this locus. Its graph image has finite
geometric fibers, so the main theorem applies. Such a bounded-output
construction still misses almost every power of2 and cannot contain Z.

This applies in particular to smooth conic or positive-dimensional
quadric families over an abelian base: a soluble fiber is k-rational.
Additional equations must be included in V before assessing this
hypothesis; the statement does not silently replace their existential
projection by all points of a parametrizing ambient space.

## Genus-one families, without a section

Let B be a finite-type locally closed subvariety of an abelian variety
A/k. Let C→B be a smooth proper family of geometrically connected
genus-one curves equipped with a relatively ample line bundle L.
Let h be a rational output on an open domain U. If every value in
h(U(k)) has uniformly bounded denominators, then the output set meets
every a+bΛ (b≠0, Λ⊂k* finitely generated) in finitely many values.
It therefore cannot contain all integers. A zero section is NOT required.

Complete proof: the constructible image W⊂A×A1 has a constructible
finite-image fiber locus B0, by fiber-dimension constructibility
(Stacks tag05F9 on a finite locally closed decomposition). Actual
outputs above B0 are handled by the main theorem. On every other
fiber contributing a rational witness, the output is nonconstant on
a nonempty open subset of a projective genus-one curve. Siegel gives
only finitely many rational points with the required denominator
bound. Since the fiber is soluble, its rational points are a torsor
under its Jacobian's k-points, so that Jacobian must have rank zero.
Merel gives one integer N=N(k) annihilating all its rational points.

The positive degree d=deg(L_b) is locally constant; split finitely
many connected components so it is constant. The relative Jacobian
J=Pic^0(C/B) is an elliptic scheme. The intrinsic divisor-class map

    α_L: C → J,  P ↦ [O(dP)⊗L_b^(-1)]

is induced by O(dΔ)⊗pr2*L^(-1) on C×_B C. Over a geometric fiber,
choosing any origin identifies it with a translate of [d], so its
degree is d². It is proper and quasi-finite, hence finite. For every
rational witness on a nonconstant contributing fiber, α_L(P) lies in
J_b(k), which is torsion annihilated by N. Therefore all those witnesses
lie in the fixed finite cover F=α_L^(-1)(J[N])→B. Its composite to A
is quasi-finite, so the main theorem handles their outputs as well.
Affine transforms of h preserve the bounded-denominator hypothesis.

The chosen rational origin in a soluble fiber is used ONLY to infer
rank zero. It is not used to construct F. The intrinsic degree-d
map is why genus-one torsors are covered too. Taking L=O(O), d=1,
recovers the simpler elliptic-scheme proof. Finite stratifications
of the base preserve the result. Higher-genus curves remain outside
this argument because finite rational point sets do not force their
Jacobians to have rank zero.

Primary sources:
- L. Merel, *Bornes pour la torsion des courbes elliptiques sur les
  corps de nombres*, Invent. Math.124 (1996),437--449, introductory
  Corollary; author PDF:
  https://perso.imj-prg.fr/wp-content/uploads/merel-pub/torsion.pdf.
- S. Bosch, W. Lütkebohmert, M. Raynaud, *Néron Models*, Springer1990,
  Chapter9 (relative Jacobians), especially §9.4 Theorem1 for the
  smooth separated Picard identity component in the semistable case;
  smooth connected fibers make this an abelian scheme.
  https://doi.org/10.1007/978-3-642-51438-8_10.
  Primary chapter text indexed at
  https://math.arizona.edu/~cais/scans/BLR-Neron_Models/neron4.pdf
  (full web fetch exceeded size limit; indexed theorem text checked).
- S. Y. An et al., *Jacobians of genus one curves*, J. Number Theory90
  (2001),304--315, §1 explicitly gives Q↦[dQ−D] of degree d²:
  https://archive.math.arizona.edu/wmc/Research/JacobianFinal.pdf.
  Author's corrigendum permits any positive degree, not just minimal:
  https://www.math.lsu.edu/~aperlis/publications/jacobians/.

## Stable deliverables and exact verification

- finite_correspondences_and_denominators_20261109_v14.tex:
  polished complete paper; source statements and all new consequences
  have full proofs. PDF is compiled from this source.
- check_exceptional_correspondence.py: standard-library exact sparse
  Laurent-polynomial checker of the sharp exceptional surface.
- exceptional-correspondence-certificate.json: PASS, including both
  inverse identities, all four complete exceptional lines, and boundary
  Jacobian minors ±36.

No general counterexample to Diophantine definability of O_k in k is
claimed. The obstruction now covers finite correspondences, soluble
unirational fibers with bounded outputs, and smooth projective genus-one
families with bounded outputs. Positive-dimensional higher-genus or other
non-unirational fibers remain genuine possibilities.
