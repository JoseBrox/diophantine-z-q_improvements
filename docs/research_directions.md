# Research directions

The current bounds are **25 total variables**, or **226 for a quartic**, under the stated inherited arithmetic premises. Fully specified constructions use **27 variables**, or **262 for a quartic**. A weak abc inequality gives **13 variables**; ordinary rational abc gives **87 for a quartic**. Every count includes the input. The priorities remain the number of variables, degree, then coefficient height. The [main table](../README.md#main-results-and-arithmetic-assumptions) states the hypotheses and effectiveness.

## Removing retained variables

The [25-variable source](../papers/few_variables25/few_variables25_merged_20261110_v19.pdf) retains the input, eighteen rational coordinates for nine elliptic points over a quadratic field, one slope, and four coordinates for two pole predicates. One further coordinate eliminates all finite algebraic choices. The scalar conditions already share the two comparison pole predicates.

A substantial reduction therefore requires a new arithmetic construction: fewer point roles, a complete pole predicate with fewer retained parameters, or a different representation of the integer labels. Simplifying arithmetic expressions improves the degree but does not remove retained variables. The elimination theorem already uses only one additional coordinate.

The nine points arise from four numerator roles and a common reference, together with translated points needed to compare the same integer labels at complementary denominator indices. The useful targets are an alternative integer-growth relation requiring fewer independent labels, or a local argument recovering a label from fewer point comparisons. Any replacement must work on every rational solution and must still supply witnesses for every integer input. The [elliptic witness constraints](../papers/elliptic_charts/structural_constraints_20261109_v13.pdf) identify limitations of several direct parameterizations; they are not lower bounds for arbitrary Diophantine constructions.

Rational substitution of elliptic points has a precise restriction. Every rational map $E^r\dashrightarrow E$ is a translated homomorphism ([Milne, Chapter I, Corollary 3.7](https://www.jmilne.org/math/CourseNotes/AV.pdf)). Under $2E(K)=\mathbb ZP$, every $K$-endomorphism is multiplication by an integer: subtract the multiplication agreeing with its value on $P$, and the difference kills a nontorsion point, so it is zero. Thus a rational point formula sending integer multiples back to that subgroup has label $m_0+\sum m_i n_i$. It cannot produce multiplication or squaring of the integer labels. This excludes nonlinear rational substitutions as a way to remove a point role; its scope does not include arbitrary additional input equations or constructions on other varieties.

Finite algebraic choices have a stronger restriction. The [index-product density theorem](../papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.pdf) proves that, for a non-torsion point $P$, the triples $([n]P,[h]P,[nh]P)$ are Zariski dense in $E^3$ for every infinite set of labels $n$ with infinitely many permitted $h$ for each label. A fixed algebraic correspondence with finite geometric fibers over the two input points therefore cannot supply the product point on all these pairs, even after restricting to a nonempty open domain. The same obstruction applies to $([n]P,[n^2]P)$ on any infinite set of indices. For elliptic curves, the proof compares the increasing degrees of the graphs of multiplication with the bounded degree of fibers of a fixed divisor.

This statement concerns finite geometric fibers, not positive-dimensional fibers with finitely many rational points. It also allows no additional free rational parameter. A smaller arithmetic source could therefore still use specially selected auxiliary indices, a positive-dimensional correspondence with a proved rational-point restriction, or a different growth relation. For the rational-root Pell proposal, the missing requirement remains a global rational root on every integer input together with a sound denominator argument; local quadratic-residue conditions alone do not provide it.

The degree bound of the current 25-variable family is

$$20747108969426225455955968<2^{85}.$$

The support bound is below $2^{1979}$. The finite-operation specification is exact, but the determinant polynomial has not been expanded, so neither upper bound is asserted to be an exact count.

## The height estimate and local conditions

The [modular multiplicity theorem](../papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf) proves

$$h(a)\le C_2M_5(a)^2(1+\log M_5(a))^2,
\qquad C_2<2^{221231}.$$

It gives an effective exponent $2+\eta$ for every $\eta>0$, on the full rational contact family. The coefficient-field multiplicity absorbs the modular character order: if the character order is $s$ and the associated modular abelian variety is geometrically isogenous to $A^r$, then $s/r\le4$. Height superadditivity supplies one surface factor of height at most $h(J_H)/r$, and an explicit dimension-two isogeny estimate transfers that bound to the required surface. The full normalized source modular realization is essential; a conductor bound alone does not imply this theorem.

Taking exponent $7/3$ and combining two disjoint five-contact sets gives exponent $7/6$. This supports order-three comparisons. The current few-variable source uses the raw comparison functions and the scalar normalization

$$\Phi_R(S)=\frac{RS}{1+RS}.$$

The potentially troublesome case $v(RS)=0$ is excluded in the completeness construction by clustered prime selection together with the extra congruence $h\equiv0\pmod p$. This works without a bound on the depth of elliptic reduction. At shared scalar and comparison primes, the proof retains $M_j^3\mid\Delta c$ for the Lucas residual and $M_j\mid(u-nv)c$ for the input residual; it does not discard shared prime support.

Further useful work should optimize the whole arithmetic relation and its local precision together. A lower required valuation can save polynomial operations or quadratic coordinates, but replacing a growth equation can also increase its degree. Both costs must be measured in the actual source. Merely improving a real constant while leaving the same integer rounding thresholds may not change the polynomial.

## Effective coefficients

The [explicit 27-variable construction](../papers/few_variables27/explicit27_20261110_v19.pdf) uses three scales

$$1,\qquad(1+\rho S_0^2)^2,\qquad(1+\rho(S_0+S_1)^2)^2.$$

The two rational components of the elliptic abscissa sum give a fully effective height bound. Retaining the coprime factor

$$76249^{2L+1}(M_\beta^\circ)^3\mid c$$

yields the certified odd parameter $L=20483$, degree below $2^{87}$, support below $2^{2192}$, and coefficient height below $2^{2^{99}}$.

An effective trace-height bound of suitable strength could remove the third pole predicate and make the 25-variable family fully specified. The existing aggregate trace theorem has an ineffective additive constant. A proof must control cancellation on all relevant integer-index tuples; positivity of a selected real witness is not enough to supply that uniform arithmetic estimate.

## Reducing the abc constructions

The [13-variable construction](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) has three elliptic point roles and two pole predicates. Its height comparison removes the Lucas and separate scalar-growth mechanisms. The most direct targets are a single complete pole predicate for the two scales, or an arithmetic family requiring only two point roles.

Simple multiplication of the contact functions does not supply the needed height estimate, even at the actual source scales. For

$$F(t)=\frac{t(t+1)(2t+1)(3t+1)(4t+1)(5t+2)}{120},
\qquad R(t)=\frac{F(t)}{(t-1)^8},$$

the [product-height obstruction theorem](../papers/pole_parameters/product_height_obstructions_20261110_v19.pdf) proves that every rational $a>4$ admits

$$\lambda=-\frac{a+1}{5a},\qquad
R(\lambda)R(a\lambda)\in-\mathbb Q^{\times2}.$$

The odd radical is therefore one, including for scales $a=\beta^8+T(n)^8$. Additional elliptic and pole equations could exclude these particular slopes, but a proposed combined predicate must prove that exclusion and a sufficient height estimate on its entire rational solution set. Restricting the sign of the slope does not settle the problem: the same paper gives positive unbounded-scale counterfamilies, with their precise scope stated separately.

A stronger [local obstruction](../papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.tex) applies to every fixed nonzero rational function of the input and slope, including expressions that depend on the scale. Near a common simple contact, two independent contact depths give an integer-linear valuation formula in a suitable cone; its reduction modulo two has a nonzero kernel. Infinitely many primes realize the resulting failure with the exact scale, half-integral input, and a positive integer sum of two squares for the slope. The obstruction also persists with $\lambda=1+s^2$ for an integer $s$, so requiring $\lambda-1$ to be a square does not remove it. Thus a single rational parity test cannot uniformly retain both sets of odd contact primes. A successful single-pole construction would need a different arithmetic implication or additional conditions proved on every full source solution. The theorem does not exclude such constructions or prove a variable lower bound.

The weak abc/Szpiro construction has strict absorption coefficient $14641/16169<1$. The quartic with 87 variables uses ordinary rational abc and an eight-contact estimate, with absorption coefficient $8/9$. These hypotheses should not be conflated. The [restricted-abc analysis](../papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) explains why available small-denominator and asymmetric-size estimates do not replace the required uniform inequalities.

The [quadratic-cover theorem](../papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf) makes the distinction precise. Adding $z^2=-R(\lambda)R(a\lambda)$ does force equality of the odd contact radicals and proves soundness with one pole under the same weak abc premise. For each fixed $a>4$, however, its curve has genus four; equality of odd contact sets outside any fixed finite prime set permits only finitely many rational slopes. The usual prime-selection argument therefore cannot supply an unbounded slope family on this cover. Its explicit rational section also fails the comparison tests for infinitely many odd shifts, by an inert-prime obstruction. A successful route must prove an arithmetic existence statement for other cover points, change the contact geometry, or avoid requiring equality of the two entire parity sets.

No construction below thirteen total variables under abc is established.

## Quartic coordinates and coefficient height

The [current quartics](../computation/quartic/README.md) clear each local factor by the inverse fourth power of its weight. Fourth powers of five existing field values become quadratic expressions in their stored squares. The inherited-premise factors use inverse weights $q^{-1},q^{-2},q^{-4}$; the abc construction uses three weights $s,s^2,s^3$ with $s=1/q$, without retaining $q$ itself. The zero-weight components are excluded in the full proofs. The unconditional contact equations use three outputs and the existing inverse weight; the reciprocal-symmetric abc contacts use two outputs. For the abc quartic, rescaling the factor product and trace preserves the original pole input exactly; affine contact shifts reduce the coefficient height.

The next useful targets are the remaining powered comparison values, the number of separately stored local factors, and quadratic representations of the point-pair relations. Distinct valuation classes prevent cancellation within a factor. Any attempt to pack more tests into fewer factors must check every odd valuation and arbitrary witness pole orders, and must preserve the rational completeness argument. A coordinate count on a generic open subset is insufficient without a proof for the excluded strata.

The fully specified quartic uses $N=9682$ and has coefficient height $149^{38730}+1$, with 279599 binary digits. The 226-variable family has height $149^{4N+2}+1$ for $N\ge53$, while its sufficient defining threshold remains ineffective. The abc quartic has height $\max(4153456,B^2+797681)$ and an ineffective sufficient odd shift. Replacing a row by a rational multiple or an invertible rational row combination can reduce height without changing the zero set; primitive integer normalization and the resulting expanded coefficients must then be recomputed exactly.

Degree four is minimal for a single defining equation under the [lower-bound theorem](../papers/lower_bounds/lower_bounds_20261109_v15.pdf). Globally nonnegative quartics and quadratic systems require at least five total coordinates. These results do not prove that five coordinates suffice or exclude different quartics with far fewer variables than the current constructions.

## Rings of integers of number fields

No counterexample to $\mathcal O_K$ being Diophantine in $K$ has been established here. The [number-field reductions](../papers/number_fields/number_field_definability_20261109_v12.pdf) show that a counterexample would persist in every finite extension, and therefore would give a totally imaginary Galois counterexample. Failure of a particular rational defining polynomial after scalar extension does not answer the general question.

The [complex multiplication obstruction](../papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.pdf) shows that this particular $j=1728$ curve doubles its rank after adjoining $i$. An infinite cyclic subgroup then has identically zero abscissa trace and unbounded heights, and four distinct doubled points can have zero abscissa sum. Thus neither the original cyclic-group assertion nor an unrestricted trace or sum-height bound survives this extension. Zywina's rank-stability theorem allows a different curve for a prescribed quadratic extension, but the remaining denominator and local comparison arguments still need a proof.

A Diophantine subset containing all rational integers and having uniformly bounded integral denominators would suffice for a positive construction. Rank stability alone can produce a much smaller rational subset. Norms or traces expressed in base-field coordinates do not automatically restrict unrestricted extension-field witnesses to that base field.

The [finite-correspondence results](../papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) exclude several proposals based on finitely many rational functions on abelian varieties, quasi-finite covers, and specified low-genus fibers. A promising replacement should supply a uniform denominator theorem outside those hypotheses and analyze exceptional positive-dimensional fibers explicitly. Local density and bounded searches are useful diagnostics, but neither proves that all integers occur.

## Scope of the obstructions

The [fixed-pole](../papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf), [combined-pole](../papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf), and [quartic-pole](../papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) papers prove exact counterexamples to specified simplifications. They leave open different contact configurations, different predicates on restricted generated inputs, and different arithmetic constructions. New proposals should identify the obstruction they avoid and prove both soundness and rational completeness.
