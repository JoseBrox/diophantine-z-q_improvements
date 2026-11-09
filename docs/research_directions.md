# Research priorities and proved constraints

The targets are **fewer than ten total coordinates** and **fewer than one hundred for a quartic**. Every count includes the input. Under the inherited arithmetic premises, the leading bounds are 27 coordinates, or 263 at degree four; fully specified alternatives have 29 and 322. An additional weak abc inequality gives **13 coordinates** and degree below $2^{44}$; ordinary Szpiro already supplies that inequality. Under additional ordinary rational abc, the **98-variable quartic meets the target below one hundred**. The sufficient coefficient thresholds for these existence families remain ineffective. The priority is coordinates, degree, then coefficient height. The [main table](../README.md#main-results-and-arithmetic-assumptions) records their different arithmetic scopes.

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

The [finite-algebra theorem](../papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) already compresses all finite choices into one additional rational coordinate. Its current degree bounds are below $2^{87}$ and $2^{89}$ for the 27- and 29-variable constructions, and below $2^{44}$ for the weak-abc thirteen-variable construction. Their final polynomials have not been expanded. Certified support bounds are respectively $2^{2202}$, $2^{2417}$ and $2^{509}$, all strict upper bounds rather than exact monomial counts. Further elimination improvements cannot remove a retained free parameter.

The [point-presentation theorem](../papers/elliptic_charts/structural_constraints_20261109_v13.pdf) shows that a finite algebraic presentation recovering arbitrary tuples of r independent points on the specified Weil restriction requires at least 2r retained rational coordinates. This concerns that presentation problem, not all definitions of the integers.

### Stronger contact-height control

The present arithmetic construction uses a power bound on logarithmic height, of the form h(t) <= C M(t)^19. A logarithmic bound h(t) <= C log M(t) + C0 changes the growth comparison and eliminates the Lucas mechanism and its separate scalar-growth certificate together with their point witnesses.

The [thirteen-variable theorem](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) needs only weak abc with exponent $\kappa=121/100$. The degree-four map $z(z+2)^3/(2z+1)^3$ gives six rational contacts and

$$
h(t)\le\frac{121}{74}\log M(t)+C,
\qquad
h(1:u:v)\le\frac{121}{437}h(u^8+v^8)+C'.
$$

Using the two arguments $\lambda$ and $(\beta^8+T^8)\lambda$ gives a strict absorption coefficient $14641/16169<1$. The source contains three point pairs, two pole pairs, one slope, the input, and one finite-algebra coordinate. Its degree is bounded by 12,339,485,119,488, and all six local tests have order one. More generally, any one weak abc exponent $1<\kappa<4/3$ works after choosing an even $d$ with $(8/\kappa-6)(d/\kappa-3)>2$; only the displayed specialization has the supplied numerical degree certificate.

Ordinary Szpiro implies the required weak inequality. Ordinary abc also gives the shorter contact and scalar circuits used by the [98-variable quartic](../papers/quartic_existence/quartic_abc98_20261109_v16.pdf). The next arithmetic task is to prove the needed logarithmic bounds on the restricted inputs without an extra conjecture, or to remove another retained point or pole role with a complete rational-witness argument. No construction below thirteen total coordinates has been established under abc.

The [arithmetic-hypotheses paper](../papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) records the scope of other conjectures. Truncated Vojta supplies ordinary abc. RH, GRH and Grimm do not currently give a proved reduction. Distinct prime assignments do not control odd valuations, as an explicit Pell family shows. Polynomial injections supplied by Bombieri–Lang do not alone eliminate the witnesses needed to invert them. Mazur's connected-component conjecture would exclude the desired existential definition itself.

### Pole certificates

The [fixed-parameter theorem](../papers/pole_parameters/fixed_pole_parameters_20261109_v16.pdf) excludes every constant rational choice of the actual pole parameter in the stated certificate. In particular, the specializations $e=-1/3$ and $e=1$ fail on explicit prepared inputs; unconditional rank and descent computations prove this even though the corresponding curves are locally soluble. The fixed conic-chart choices $\tau=\pm1,\pm17$ fail on explicit prepared inputs too. These results rule out universal completeness over all prepared inputs; they leave the narrower inputs produced by a chosen prime-pattern construction open.

The [paper on combining pole certificates](../papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf) proves that sharing a nondegenerate actual parameter forces equal squareclasses. An explicit prepared pair excludes the two degenerate choices as well, so it has no shared actual parameter. Sharing the conic-chart parameter avoids this squareclass argument but leaves a simultaneous rational-point problem. The [density theorem](../papers/pole_parameters/pole_witness_density_20261109_v14.pdf) proves avoidance of finitely many algebraic conditions for independent witnesses; it does not prove these intersections nonempty.

Simply multiplying the two eight-contact detectors also fails: the reflection identity $R(2-t)=R(t)$ makes $R(\lambda)R(a\lambda)$ a square when $\lambda=2/(a+1)$, while $h(a)$ is unbounded. Collisions of distinct nonzero contacts are supported on the finitely many equations $a\theta-\eta=0$ modulo primes; controlling their total contribution incurs a height-dependent term. A useful merger must address those collisions and prove simultaneous completeness. These obstructions do not establish a global minimum for the number of pole coordinates.

### A different connection between rational inputs and elliptic indices

A rank-one curve over the rationals costs fewer rational coordinates per point, but the paired-place argument does not transfer directly. Requiring H and H-P to be formal at the same good prime forces the fixed P to reduce to the identity. Two rational curves with an algebraic curve of common-index pairs must have an isogeny relation, which obstructs the required independent reduction orders.

A promising alternative would be a small Diophantine certificate for index divisibility on a rank-one elliptic curve, together with a proved connection to the ordinary rational input. Every denominator condition must be justified in both directions, including torsion, small indices, and bad primes. The graph (n,[n]P) is Zariski dense in the product with the affine line, so the index cannot be recovered by simply adding a finite algebraic choice to point coordinates.

Prescribing high divisibility of a-1 by contact primes does not prescribe divisibility by the corresponding elliptic reduction orders. The [uniform scalar normalization](../papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.pdf) resolves the real boundedness condition, but not this independent local completeness requirement.

## Reducing the quartic

The current [263-coordinate system](../papers/quartic_existence/quartic263_20261109_v16.pdf) has **237 quadratic equations and 3,312 monomials**. Its [complete table](../computation/quartic/family263/quadratic-family263.json) and independent checker specify every coordinate. Twenty contacts symmetric about one make the contact polynomial degree ten in $r=(a\lambda-1)^2$, allowing five quadratic outputs at each scale. The equations $Fq=r^9$ and $k=qr^2$ supply $1/R=k$, where $R=F/(a\lambda-1)^{22}$. The positive trace itself serves as the second scale. This keeps comparison orders twelve and three and reference depth three under the inherited premises.

The [98-coordinate abc system](../papers/quartic_existence/quartic_abc98_20261109_v16.pdf) has **86 quadratic equations and 882 monomials**. It removes the Lucas and scalar-growth roles using logarithmic height control. Six symmetric contacts, the scale $\beta^6+T^6$, and two factors per detector give a height absorption coefficient $8/15$. The contact product and its inverse normalization are evaluated jointly, without storing the contact product as another coordinate. Its compressed subtraction formula is used only after the proof excludes all three exceptional cosets $E[2]$, $P+E[2]$, and $-P+E[2]$. This excludes unintended solutions while preserving the complete quadratic point chart, including identity numerator points.

Further large savings under the inherited premises require removing arithmetic roles. The unchanged four root charts, auxiliary charts even after deleting their eight alternate parameters, scalar block, and input already account for 102 coordinates. This obstruction concerns those literal blocks; the additional-abc construction passes below one hundred by removing several of them.

The priorities are:

1. Obtain the logarithmic contact-height control on the restricted arithmetic inputs under the inherited premises, or replace the Lucas and scalar-growth roles by a different complete arithmetic certificate.
2. Find a smaller complete quadratic presentation of U,V with U-V=Q, including identity, torsion, and denominator-zero branches.
3. Replace the pole certificate with a smaller quadratic system having a full completeness proof.
4. Optimize the remaining local factors jointly with their power circuits. Further contact translates reduce congruence precision but also increase the contact polynomial's evaluation cost.

For the 263-variable family, coefficient height is exactly $80989^{4N+2}+1$ for $N\ge23$. For the additional-abc quartic it is $\max(11600064,2B^4+169997)$ for integer $B\ge3$. Reducing the defining exponent or shift is secondary to the coordinate count and requires a global height argument. Neither sufficient defining threshold is determined effectively.

## Rings of integers in their fraction fields

No counterexample and no general positive theorem is established. Failure of one formula, or even a fixed finite list, does not exclude different formulas for individual fields. A genuine counterexample persists under every finite extension, so one may seek a totally imaginary Galois counterexample using the [descent theorem](../papers/number_fields/number_field_definability_20261109_v12.pdf).

A useful sufficient target remains a Diophantine set S in K with Z contained in S and MS contained in the ring of integers for a fixed positive integer M. Translating MS by 0,...,M-1 then using an integral basis gives the whole ring of integers.

The [finite-correspondence theorem](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) excludes several broad approaches over an abelian base:

- Finitely many geometric output values on each fiber, including quasi-finite covers.
- Soluble unirational fibers with a uniform denominator bound.
- Smooth proper genus-one fibers equipped with an ample line bundle, again with a uniform denominator bound.

The first obstruction is semiabelian Mordell–Lang. The genus-one case combines Siegel with uniform torsion and a finite map to the relative Jacobian; it does not assume a section. A smooth surface birational to a product of elliptic curves nevertheless has exceptional affine lines representing every input, so a statement restricted to a generic fiber cannot justify the conclusion.

Further work must address genuinely input-dependent positive-dimensional fibers outside these classes, or a direct rational-subfield, trace-graph, or norm-image definition with actual base-field restrictions. Higher-genus families remain outside the genus-one obstruction. Complete local solubility, density in completions, and rank stability by themselves do not prove integer coverage or a uniform denominator bound.
