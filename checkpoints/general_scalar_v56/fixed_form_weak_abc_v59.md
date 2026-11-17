# A fixed weak-abc exponent for the derivative source

## Quantified Belyi transfer

Let H(A,B) be a fixed squarefree homogeneous integer form of degree h.
Let phi=P/Q be a rational Belyi map of degree N, defined over Q,
which sends every projective zero of H into {0,1,infinity}. Under
weak rational abc with exponent kappa>1,

`log rad(H(A,B)) >= (h-2-N(1-1/kappa)) log max(|A|,|B|)-O(1)`

for primitive integer pairs with H(A,B) nonzero.

Proof: choose integral homogeneous representatives P,Q of degree N,
with no common projective zero. Their evaluation gcd is bounded by a
fixed resultant. Rational-map height comparison gives
`h(phi(A:B))=N h(A:B)+O(1)`. Riemann–Hurwitz says that the reduced
preimage of {0,1,infinity} has exactly N+2 points. Thus the squarefree
product of P,Q,P-Q is a constant times H times a fixed squarefree form
J of degree N+2-h. The abc radical is at most a fixed constant times
`rad(H(A,B))*|J(A,B)|`, and `log|J(A,B)| <= (N+2-h)h(A:B)+O(1)`.
Applying weak abc and rearranging proves the formula. The finitely many
rational pairs on a zero of P,Q,P-Q but not H are absorbed into the
additive constant. No number-field version of abc is used.

## The two forms actually used

For the sixteen-shift, M³ derivative source, only the following two
fixed homogeneous forms need the ordinary-abc squarefree-form estimate:

`H1(A,B) = product_{c=-8,...,-1,1,...,8}(A+cB)` (degree 16),

`H2(A,B) = AB product_{s=-16,...,-1,1,...,16}(2A³+sB³)` (degree 98).

Both are squarefree over Qbar. H1 has 16 Galois-stable roots of
exponential height at most 8. H2 has 98 Galois-stable roots, and a
nonzero finite root satisfies alpha³=-s/2, so its height is at most
16^(1/3)<3. Including zero and infinity does not increase this bound.

Let N be the maximum of the degrees of two rational Belyi maps for
these forms. Then weak abc at the single exponent

`kappa_star = 1+1/(100N)`

gives losses `N_i(1-1/kappa_star)<1/100`. Since N>=96, this exponent
is below 1001/1000, and its weak abc inequality implies the latter
weaker one. All radical, signed-height and binary-power inequalities
in the eleven-coordinate proof therefore follow with the published
constants. The existence of a suitable rational Belyi map is a theorem,
not an extra arithmetic realization premise; rational maps can be
enumerated and the finite branch/root conditions checked exactly.

## An explicit, very conservative exponent

Khadjavi's effective Belyi theorem bounds the degree for a Galois-stable
set of N0 algebraic points of exponential height at most H0 by

`(4 N0 H0)^(9 N0³ 2^(N0-2) N0!)`.

This exact statement appears in Javanpeykar–Voight, Proposition2.10,
with citation to Khadjavi, Theorem1.1(c). Their introduction explicitly
records that the constructed map on P1 is defined over Q.
Using N0<=100 and H0<=8 for both forms, set

`E = 9*100³*2^98*100!`, `U = 3200^E`.

Then both map degrees are at most U. Consequently the completely
specified rational exponent

`kappa_explicit = 1+1/(100U)`

suffices for the eleven-coordinate source with every other premise
unchanged. This bound is not an optimized weak-abc exponent and does
not establish the result at 16/15 or 121/100. The maps need not be
inserted into the defining polynomial: they are used only in its
height proof, so this change does not change the native circuit,
variable count, degree or coefficient specification.

## Verified sources

- Z. Rudnick, P. Sarnak, A. Zaharescu, *The distribution of spacings
  between the fractional parts of n²alpha*, Inventiones145(2001),
  37–57, Appendix A.2, equation(A.2):
  https://www.math.tau.ac.il/~rudnick/papers/rsz.pdf.
  The primary statement and its explicit attribution to Belyi,
  Elkies and Langevin were reopened.
- N. D. Elkies, *ABC implies Mordell*, IMRN1991, no.7, 99–109:
  https://pazuki.perso.math.cnrs.fr/index_fichiers/Elkies91.pdf.
- L. S. Khadjavi, *An Effective Version of Belyi's Theorem*,
  J. Number Theory96(2002),22–47, Theorem1.1(c),
  DOI10.1006/jnth.2001.2748. Author's institutional abstract explicitly
  states rational coefficients and prescribed algebraic input points:
  https://digitalcommons.lmu.edu/math_fac/141/.
- A. Javanpeykar and J. Voight, *The Belyi degree of a curve is
  computable*, Proposition2.10 and introduction:
  https://jvoight.github.io/articles/belyidegree-14102018.pdf.
  The exact effective degree bound was reopened in this research paper.

This checkpoint does not claim numerical optimization or new rational
witness realization. The primitive-denominator route is being pursued
separately for a genuine further coordinate reduction.
