# Research directions

The current bounds are **25 total variables**, or **238 for a quartic**, under the stated inherited arithmetic premises. The fully specified alternatives have **29 variables** and **318 for a quartic**. A weak abc inequality gives **13 variables**; ordinary rational abc gives **93 for a quartic**. Every count includes the input. The priorities are the number of variables, degree, then coefficient height. The [main table](../README.md#main-results-and-arithmetic-assumptions) records precise hypotheses and effectiveness.

## Where the variables occur

The [25-variable source](../papers/few_variables25/few_variables25_merged_20261110_v18.pdf) retains the input, eighteen rational coordinates for nine elliptic points over a quadratic field, one slope, and four coordinates for two pole predicates. One separating coordinate eliminates all finite algebraic choices. The scalar conditions already share the two comparison pole predicates.

Thus another substantial reduction requires a new arithmetic argument that removes a point role, removes a pole parameter pair, or replaces the nine-point source. Reducing circuit nodes or simplifying a finite algebra does not by itself remove a retained rational parameter. The existing elimination theorem already uses only one additional rational coordinate.

The degree bound for the 25-variable family is 104263275909198787271196672, below $2^{87}$. The exact polynomial is specified by finite operations and determinants but has not been expanded. Its certified support bound is below $2^{2035}$. These are upper bounds, not exact degree and support counts.

## Combining local conditions

The useful arithmetic change is the rational normalization

$$\Psi_z(D)=\frac{zD^2}{1+zD^2}.$$

It makes inactive tests integral at odd valuations of the coefficient even if the original test has an arbitrarily deep pole. Two balanced contact functions with disjoint contact and pole sets ensure that at least one is a unit at every scalar odd prime. Integer rounding permits normalization and denominator exponents both seven, while plain elliptic parameters give the required fourth-order accuracy.

The key global divisibility is $M_j^4\mid Nc$: a comparison prime may divide the desired residual or the separately controlled scalar index. This is stronger than deleting all primes shared by the scalar and comparison supports. The latter deletion need not preserve the height estimate. A further combination must retain an equally complete treatment of shared primes and prove simultaneous realization.

A potentially shorter normalization, such as $zD/(1+zD)$, needs a new audit of the case $v(z)+v(D)=0$. Odd coefficient valuation no longer excludes cancellation. Local pole orders of elliptic points are not uniformly bounded, so a finite-depth assertion cannot be assumed. Until the cancellation and rational-witness arguments are proved, this is a research direction rather than a defining-polynomial construction.

## Reducing the thirteen-variable construction under abc

The [conditional source](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) has three elliptic point roles and two pole predicates. Its height comparison already removes the Lucas and separate scalar-growth mechanisms. The normalization used in the 25-variable construction therefore does not automatically remove another pair of coordinates here.

The most direct targets are a single complete pole predicate for the two comparison scales, or an arithmetic family needing only two elliptic point roles. Both require a new global argument. A product of contact functions can lose every odd valuation when the two contact configurations are related by a rational symmetry. Choosing scales that depend on the slope can also make the prime-selection argument circular: its coefficients must be fixed before the primes and the final common index are chosen.

The [six-contact product theorem](../papers/pole_parameters/six_contact_product_obstruction_20261110.pdf) proves this cancellation for the exact conditional contact set. Its involution $\phi(t)=-(2t+1)/(3t+2)$ gives a negative-square product. For $\lambda_m=-1/m$ and $a_m=m(m-2)/(2m-3)$, with $m\ge5$, the odd radical of $R(\lambda_m)R(a_m\lambda_m)$ is one while $h(a_m)$ is unbounded. Thus the product alone cannot yield an unrestricted height bound. Whether the source restriction $a=\beta^8+T(n)^8$ and its other equations prevent this cancellation remains open.

The present six-contact and projective-height inequalities have strict absorption coefficient $14641/16169<1$. Ordinary Szpiro supplies the needed weak abc exponent. Removing the extra height hypothesis requires an estimate on every rational solution of the proposed source, not merely on the specially chosen integer witnesses. The [restricted-abc analysis](../papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) records why the available small-denominator and asymmetric-size theorems do not apply to the current families.

No construction below thirteen total variables under abc is established.

## Quartics and coefficient size

The [common-point chart](../papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) describes $H,H-P$ by three quadrics in four field coordinates. It retains both reciprocal abscissas and both $y/x$ values. Direct ratio equations avoid a separate numerator parameter. The current 238- and 93-variable quartics use this chart, with complete treatment of every leading-coefficient exception.

For a further variable reduction, inspect intermediate values that occur in only one equation, repeated denominator normalization, and fixed-difference point pairs. A proposed quadratic substitution must be reversible on every required rational branch or have a separate proof that its additional branches are impossible. Counting fewer generic coordinates while overlooking an exceptional component does not give a new polynomial.

For fixed coordinates, rational changes of the equation basis can reduce coefficient height without changing the rational zero set. The current six-row change has exact determinant $-1/362963666515968$. The abc quartic has coefficient height $\max(4153456,B^2+797687)$; the inherited-premise family has height $149^{4N+2}+1$ for $N\ge53$. An algebraic coefficient threshold is distinct from the ineffective defining threshold.

Degree four is already minimal for a single equation with the stated integer projection. Globally nonnegative quartics and quadratic systems require at least five total coordinates by the [lower-bound theorem](../papers/lower_bounds/lower_bounds_20261109_v15.pdf). These lower bounds do not show that five coordinates suffice.

## Contact-height improvements

The [scalar-character theorem](../papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf) gives

$$h(a)<2^{330670}M_5(a)^3(1+\log M_5(a)).$$

It also proves a bound with exponent $2+\eta$ on sets where the powers of two dividing the contact primes minus one are uniformly bounded. That restriction fails uniformly even for the integral scalar family $51X^2+2504$. It cannot be imposed on all rational solutions merely because the primes selected for completeness lie in favorable congruence classes.

A useful improvement would either control the relevant modular character orders on the full source family, or replace the scalar/contact family by one where that control follows from its equations. The explicit counterfamily in the same paper should be checked against either proposal.

## Number fields: counterexamples and positive constructions

No counterexample to $\mathcal O_K$ being Diophantine in $K$ is known from this project. The [number-field reductions](../papers/number_fields/number_field_definability_20261109_v12.pdf) show that a counterexample would persist in every finite extension, so it would produce a totally imaginary Galois counterexample. Failure of one unchanged formula after extension does not answer this question.

For positive constructions, a Diophantine subset containing all rational integers and having uniformly bounded integral denominators would suffice. Rank stability alone gives only a potentially much smaller subset of the rational subfield. Norms and traces written with base-field coordinates do not automatically restrict an unrestricted extension-field witness to that base field.

The [finite-correspondence results](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) rule out several proposals based on finitely many rational functions of abelian point coordinates, quasi-finite covers, and the stated families of low-genus fibers. Exceptional positive-dimensional fibers must be checked explicitly. A promising new family must go beyond those hypotheses and provide a uniform denominator theorem, not just local density.

## Established limits on shortcuts

The [fixed-pole](../papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf), [combined-pole](../papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf), and [quartic-pole](../papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) papers give exact counterexamples to specified simplifications. Fixed actual pole parameters fail on prepared inputs; some fixed conic parameters fail on real-dense sets of such inputs; simple products can cancel the odd radical; and the proposed one-parameter quartic pole predicate has prepared local obstructions.

These theorems have explicit scopes. They do not rule out a new predicate on a narrower family of generated inputs, a different contact configuration, or a different arithmetic construction. A new proposal should state precisely which previous obstruction it avoids and prove both soundness and rational completeness.
