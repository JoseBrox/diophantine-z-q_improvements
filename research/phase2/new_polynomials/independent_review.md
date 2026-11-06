# Independent mathematical review of the shared-point source

This review concerns the rational system in `shared_source.tex`, including
its fixed-17, preparation-zero pole refinement and its single ordinate
chart. It is a mathematical review, not a verification of an emitted
polynomial or a new verification of the underlying arithmetic theorems.
The construction remains conditional on the source manuscript's arithmetic
inputs and on Sun's additional simultaneous prime-pattern theorem.

## Variable accounting

The retained coordinates are the input, twenty abscissa components of ten
halfpoints, two Lucas proxies, one common slope, eighteen structural
coordinates for nine poles, and three scalar-pole structural coordinates.
Their sum is 45. The finite coordinates are ten quartic roots and 21
quadratic roots (18 coordinate-pole roots, two scalar-pole roots, one Lucas
root), giving degree product at most `4^10 * 2^21 = 2^41`. Constants,
fixed finite branch choices, integer labels of points, and the temporary
prime-pattern parameters in the completeness proof are not quantified
coordinates. A valid application of the one-extra-coordinate finite-algebra
theorem therefore gives 46 total coordinates.

The finite exclusion product has an astronomically large fixed number of
factors. This does not add coordinates. It must remain described as an
indexed formula, rather than a computed expanded table. Replacing it by
the three-witness semilocal anchor adds two retained coordinates and one
finite quadratic generator, as stated.

## Point chart

For `a^3-Da=A+B sqrt(2)` and `C!=0`, the relation
`C^4-A C^2+B^2/2=0` is exactly equivalent to
`(C+(B/(2C))sqrt(2))^2=A+B sqrt(2)`. At a permitted rational
point, `A^2-2B^2` is the nonzero norm of the radicand, so the extra
guard loses no nonzero ordinate. It also proves separability at `C`.

The two-torsion translation in the source is correct:
`(a,b)+(0,0)=(-D/a,D b/a^2)`. If both rational ordinate components
vanished, then `D/a^2` would be rational. Writing `a=d w` forces
`w` to be rational or a rational multiple of `sqrt(2)`. The displayed
values `d^3=45-29 sqrt(2)` and `d^3 sqrt(2)=-58+45 sqrt(2)` then
contradict the rationality and nonvanishing of `b^2`. The single chart
therefore covers every required doubled point without a hidden selector.

## Height and size constants

The projective transformation `phi(t)=2+1/t` has coefficient matrix
`[[2,1],[1,0]]`, determinant -1, and the maximum absolute row sum of
its inverse is 3. Thus `h(t)<=h(phi(t))+log(3)`. Its inverse images
of the five original contacts are exactly the five displayed contacts.
Their fixed denominators, pairwise differences and differences from the
normalizing point 1 introduce only primes below 76176.

If both radicals of the base slope and its square rescaling have their
K-th powers dividing N, then
`2 h(x_r)=h(A_r)<=h(lambda)+h(A_r lambda)` gives
`h(x_r)<=(H+log(3)) |N|^(24/K)`. For a point abscissa
`x+y sqrt(2)`, the usual sum and product height inequalities give
`h(x+y sqrt(2))<=h(x)+h(y)+(3/2)log(2)`. Since H>=1, the resulting
constant is strictly smaller than 7H. Thus the original Lucas and scalar
contradictions genuinely keep their original height constant.

The finite guard excludes exactly all nonzero cyclic labels with
absolute value at most M: on a Weierstrass curve equal abscissas mean
opposite points, and the cyclic group has no torsion. The chosen
`M=2^9566463` exceeds `(20H)^2`, because
`2(log2(20)+4783227)<9566463`.

## Compatibility of the common elliptic index

At each fixed small prime, continuity at the nonzero points with indices
64 and 60 gives one progression `h=64 mod L`, with `64|L`, on which
all eighteen comparison expressions have uniform lower valuation bounds.
One can enlarge L to include any further fixed factors. The avoidance
modulus in the prime theorem must contain all its odd prime factors
other than 7 and also 3 and 17.

Let U be the lcm of the selected `d_minus` orders and V the lcm of
the selected `d_plus` orders. Sun's stated theorem gives
`gcd(U,V)=4`, `v2(U)=6`, `v2(V)=2`. All odd factors of L are avoided:
those other than 7 by the avoidance modulus, and 7 because
`pi=1+3i mod 7` makes the two orders 2 and 6 modulo 7.
Consequently `gcd(U,L)=64` and `gcd(V,L)=4`. The three congruences
`h=0 mod U`, `h=4 mod V`, `h=64 mod L` are pairwise compatible.
This checks the need for the reversed orientation; the orientation is
not optional when preserving this small-prime progression.

The compact real-group argument applies unchanged to the reciprocal
logarithm functions: each basic expression is a rational function of
one real elliptic coordinate, with finitely many poles. Every connected
component of the closure of the cyclic orbit projects onto both real
identity circles. A bounded neighborhood can be chosen on every component
before the progression modulus is chosen. Every arithmetic progression
has a closure containing a full component, so these bounds are uniform
in the later modulus. No additional real variable is needed.

## Pole completeness with preparation fixed to zero

For a positive b in the square-denominator set which is locally square
at 2, 3 and 17, the original completeness proof only needs
`U^2<17b`, `v2(U^2/(17b))>=3`, and
`v3(U^2/(17b)),v17(U^2/(17b))>=1` for its preparation step.
Putting U=b reduces these exactly to
`b<17`, `v2(b)>=3`, `v3(b)>=1`, `v17(b)>=2`.
The rest of the original support and simultaneous-realization argument
then applies without alteration. The new preparation-zero equations are
literally the old equations with its preparation parameter zero.

The Gaussian congruences in the stated prime theorem give selected primes
square at 2, 3 and 17: `pi=9 mod 16` gives a norm congruent to 1
modulo 8, and `pi=i mod 3*17` gives a norm congruent to 1 at both
odd primes. Each detector is a product of five such primes divided by
a rational square; dividing further by the trace square preserves its
three local square classes. The real and local estimates in the source
allow all four smallness requirements above to be imposed simultaneously.

## The scalar block and remaining implementation requirements

The extra scalar guard `b_*!=0` is safe for completeness. For integral
input `|r_beta|>1`, and the old construction makes the scalar norm root
a unit at every prime dividing this integer. For an exact compiler,
the fixed binary tree must retain constant leaf 1 on its all-left path,
and its six tests must be normalized by `r_beta` to their assigned powers.

The Lucas quadratic can have a repeated rational root at arbitrary
rational base values: `xi=0,zeta=1/2,tau=0` is an example. A finite-algebra
compiler using derivative guards must include its zero-discriminant
stratum, or explicitly impose a nonzero discriminant and justify that
restriction by completeness. The intended integral values with
`|xi|>M` have positive discriminant, so the latter choice also preserves
the required input projection. Pole square roots likewise require their
zero-radicand strata if arbitrary old witnesses are to be preserved.

No hidden retained coordinate, failure of the displayed 7H bound, or
failure of the three-congruence compatibility was found. At the time of
this initial review, the proposed 44-coordinate refinement still required
a complete argument preserving its scalar local conditions. That argument
has subsequently been completed, as recorded in the addendum below.

## Primary arithmetic text inspected

Sun, *86 unknowns for Hilbert's tenth problem over the rationals*,
arXiv:2610.20691v2, Theorem 4.1 and the compact-group proof of Lemma 8.1:
<https://arxiv.org/html/2610.20691v2>.
The original repository's `quartic_12504.tex`, especially its exact pole
completeness and scalar correction paragraphs and its reciprocal logarithm
and final arithmetic interpretation. Reading these applications is not a
verification of the new analytic prime-pattern theorem itself.

## Completed sharing argument and precision refinements

The full independent proof of identifying the scalar-height point with
the common comparison point is in `sharing_review.tex`. Its decisive
step is to choose the scalar pole witnesses after the final comparison
index. The old scalar local conditions persist on a fixed progression;
the reversed reduction-order orientation makes that progression compatible
with the prime-pattern congruences. The resulting scalar norm root is a
unit at every prime supporting the corrected scalar contact, so its final
pole input has square denominator and the required local square classes.
No real bound on that norm root is needed in this version.

This proves the 44-total-coordinate construction using the indexed finite
exclusion, and the 46-total-coordinate version using the semilocal anchor,
under the stated arithmetic and finite-algebra inputs. The proof has also
been incorporated into `shared_source.tex`; its reviewed SHA-256 is
`d7e8d1322ac326474f1b2621c10c8587d56e6e7c0dc7874f30c422bf457d0e71`.

The precision-52 supplement was independently checked, including the
logarithm tail, the strict constant inequality, and the enlarged anchor.
For `precision52.tex` SHA-256
`a13fd44060ea10dc73ed97a6821466aea922019cb9666fc2b9b557b6ccdc7bac`,
the required label size is `|a|>(21H)^(13/2)`. It follows from the
semilocal anchor `C=3^(2^26)`, whose quartic coefficient is
`2C^4=2*3^(2^28)`. The alternative indexed cutoff
`M_52=2^31091008` is also sufficient. This change shortens logarithms
without changing the retained-coordinate count.

The further scalar-order-32 corollary in `../quartic/scalar32.tex` is
valid under that enlarged size condition: it implies `|a|>(20H)^4`,
so `H|a|^(3/4)<|a|/20`, exactly the estimate needed in the scalar
contradiction. The smaller scalar order weakens the required divisibilities
at the supporting primes, and the constant-left norm-tree unit argument
is unchanged. These reviews concern the source mathematics; numerical
quartic gate counts and emitted polynomial coefficients have separate
independent certificates.
