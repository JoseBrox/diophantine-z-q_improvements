# Research priorities and proved constraints

The targets are **fewer than ten total coordinates** and **fewer than one hundred for a quartic**. Every count includes the input. Neither target is attained by the constructions under the inherited arithmetic premises. Their leading bounds are 27 coordinates, or 267 at degree four; fully specified alternatives have 29 and 322. Under the additional rational abc conjecture, a separate family reaches **13 coordinates** and degree below 2^44, with an ineffective sufficient shift. The priority is coordinates, degree, then coefficient height. The [main table](../README.md#main-results-under-the-inherited-arithmetic-premises) records the arithmetic scope.

## What the lower bounds establish

The [lower-bound theorem](../papers/lower_bounds/lower_bounds_20261109_v15.pdf) gives the following necessary counts for an infinite projection contained in a fixed ring of S-integers.

| Class of presentations | Necessary total coordinates |
|:--|--:|
| Arbitrary finite polynomial systems | 3 |
| Systems of equations of degree at most three | 4 |
| Quadratic systems | 5 |
| Globally nonnegative quartics over the rationals | 5 |

A single defining equation has degree at least four. A nonnegative equation in three coordinates has degree at least eight. None of these coordinate bounds is claimed to be attained by a definition of the integers. The sharp general minimum is unresolved.

Any three-coordinate quartic candidate must change sign and have an absolutely irreducible surface with dense smooth rational points. Searching only sums of squares would miss this entire possibility.

## Reducing the retained arithmetic witnesses

The [finite-algebra theorem](../papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) already compresses all finite choices into one additional rational coordinate. Its current degree bounds are below 2^87 and 2^89 for the 27- and 29-variable constructions. Further elimination improvements cannot remove a retained free parameter.

The [point-presentation theorem](../papers/elliptic_charts/structural_constraints_20261109_v13.pdf) shows that a finite algebraic presentation recovering arbitrary tuples of r independent points on the specified Weil restriction requires at least 2r retained rational coordinates. This concerns that presentation problem, not all definitions of the integers.

### Stronger contact-height control

The present arithmetic construction uses a power bound on logarithmic height, of the form h(t) <= C M(t)^19. A logarithmic bound h(t) <= C log M(t) + C0 changes the growth comparison and eliminates the Lucas mechanism and its separate scalar-growth certificate together with their point witnesses.

The abc conjecture supplies such logarithmic control for the fixed squarefree five-contact binary form. It also supplies a linear height bound for positive scalar combinations u^6+v^6. These are additional arithmetic consequences of abc, not consequences of the published exponent-19 estimate. The [thirteen-variable theorem](../papers/conditional_few_variables/conditional13_20261109_v15.pdf) implements this route with sixth powers: three point pairs, two pole pairs, one slope, the input, and one finite-algebra coordinate. The exact degree is bounded by 13155996618240. Its six local tests all have order one. The priorities are to prove the needed logarithmic bounds on the specific inputs without abc, reduce the remaining point or pole roles with a complete arithmetic argument, and compile this smaller arithmetic source into an independently verified quartic system.

### Pole certificates

The [fixed-parameter theorem](../papers/pole_parameters/fixed_pole_parameters_20261109_v14.pdf) excludes every constant rational choice of the retained pole parameter in the stated certificate. In particular, the specializations e=-1/3 and e=1 fail on explicit prepared inputs; unconditional rank and descent computations prove this even though the corresponding curves are locally soluble. Repeating local tests cannot repair these specializations.

Sharing a nondegenerate pole parameter across inputs forces equal squareclasses. Sharing the conic parameter avoids that specific restriction but leaves a simultaneous rational-point problem. The [density theorem](../papers/pole_parameters/pole_witness_density_20261109_v14.pdf) proves avoidance of finitely many algebraic conditions for independent witnesses; it does not prove such intersections nonempty. A useful replacement must have a complete rational-point theorem for every prepared input.

### A different connection between rational inputs and elliptic indices

A rank-one curve over the rationals costs fewer rational coordinates per point, but the paired-place argument does not transfer directly. Requiring H and H-P to be formal at the same good prime forces the fixed P to reduce to the identity. Two rational curves with an algebraic curve of common-index pairs must have an isogeny relation, which obstructs the required independent reduction orders.

A promising alternative would be a small Diophantine certificate for index divisibility on a rank-one elliptic curve, together with a proved connection to the ordinary rational input. Every denominator condition must be justified in both directions, including torsion, small indices, and bad primes. The graph (n,[n]P) is Zariski dense in the product with the affine line, so the index cannot be recovered by simply adding a finite algebraic choice to point coordinates.

Prescribing high divisibility of a-1 by contact primes does not prescribe divisibility by the corresponding elliptic reduction orders. The [uniform scalar normalization](../papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.pdf) resolves the real boundedness condition, but not this independent local completeness requirement.

## Reducing the quartic

The current 267-coordinate system has the exact disjoint count below. Its [full table](../computation/quartic/family267/quadratic-family267.json) and independent checker specify every coordinate.

| Block | Coordinates |
|:--|--:|
| Point charts, scalar certificate, contacts, logarithms, and weights | 229 |
| Three shared fourth powers over the quadratic field | 6 |
| Five local factors and private products for two detectors | 32 |
| **Total** | **267** |

The quartic has 241 quadratic equations and 3422 monomials. Its degree-twenty contact evaluation computes both required values with six coordinates at each scale. A scale-independent normalization allows the positive trace itself to be used as the second scale, removing its square and the scaled numerator powers.

The main structural savings require removing arithmetic roles. The four root charts, the auxiliary charts even after deleting their eight alternate parameters, the scalar block, and the input already account for 102 coordinates. Retaining those literal blocks prevents the target below one hundred.

The priorities are:

1. Replace the Lucas relation and scalar-growth certificate together with their elliptic witnesses. A stronger logarithmic contact-height inequality gives a concrete route.
2. Find a smaller complete quadratic presentation of U,V with U-V=Q, including identity, torsion, and denominator-zero branches.
3. Replace the pole certificate with a smaller quadratic system having a full completeness proof.
4. Optimize the remaining local factors jointly with their power circuits. Further contact translates reduce congruence precision but also increase the contact polynomial's evaluation cost.

The coefficient height remains exactly 80989^(4N+2)+1 for N>=23. Reducing the defining exponent or changing the fixed prime is secondary and requires a new global height and local squareclass argument. The sufficient defining N for this family remains ineffective.

## Rings of integers in their fraction fields

No counterexample and no general positive theorem is established. Failure of one formula, or even a fixed finite list, does not exclude different formulas for individual fields. A genuine counterexample persists under every finite extension, so one may seek a totally imaginary Galois counterexample using the [descent theorem](../papers/number_fields/number_field_definability_20261109_v12.pdf).

A useful sufficient target remains a Diophantine set S in K with Z contained in S and MS contained in the ring of integers for a fixed positive integer M. Translating MS by 0,...,M-1 then using an integral basis gives the whole ring of integers.

The [finite-correspondence theorem](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) excludes several broad approaches over an abelian base:

- Finitely many geometric output values on each fiber, including quasi-finite covers.
- Soluble unirational fibers with a uniform denominator bound.
- Smooth proper genus-one fibers equipped with an ample line bundle, again with a uniform denominator bound.

The first obstruction is semiabelian Mordell–Lang. The genus-one case combines Siegel with uniform torsion and a finite map to the relative Jacobian; it does not assume a section. A smooth surface birational to a product of elliptic curves nevertheless has exceptional affine lines representing every input, so a statement restricted to a generic fiber cannot justify the conclusion.

Further work must address genuinely input-dependent positive-dimensional fibers outside these classes, or a direct rational-subfield, trace-graph, or norm-image definition with actual base-field restrictions. Higher-genus families remain outside the genus-one obstruction. Complete local solubility, density in completions, and rank stability by themselves do not prove integer coverage or a uniform denominator bound.
