# Polynomial presentations of the integers over the rationals

Defining-polynomial constructions under stated arithmetic hypotheses, unconditional structural theorems, and reproducible exact computations.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, its rational input projection is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height is the largest absolute integer coefficient after fixed constants are substituted.

## Main results and arithmetic assumptions

Every row retains the source arithmetic premises specified in its paper. **“None” means no additional conjecture beyond those premises**, including the stated application of Sun's prime-pattern theorem. The rows with abc or Szpiro have an additional conjectural hypothesis.

| Construction | Additional hypothesis | Total variables | Degree | Nonzero monomials | Coefficient information |
|:--|:--|--:|:--|:--|:--|
| [Fewest variables under inherited premises](papers/few_variables27/few_variables27_nontorsion_20261109_v15.pdf) | None | **27** | $<2^{87}$ | Exact count undetermined; **$<2^{2202}$** | Every sufficiently large fixed odd exponent works; sufficient threshold ineffective. |
| [Best quartic under inherited premises](papers/quartic_existence/quartic248_20261109_v17.pdf) | None | **248** | **4, exact** | **3,189, exact** | $H(P_N)=149^{4N+2}+1$ for $N\ge53$; sufficient defining threshold ineffective. |
| [Explicit construction with few variables](papers/few_variables/explicit29_nontorsion_20261109_v15.pdf) | None | **29** | $<2^{89}$ | Exact count undetermined; **$<2^{2417}$** | $H(F)\le2^{\,2^{99}}$; fixed exponent $137731$ is certified under the premises. |
| [Explicit quartic](papers/quartic/quartic322_20261109_v13.pdf) | None | **322** | **4, exact** | **4,992, exact** | $H(P)=80989^{109858}+1<2^{1791283}$; every coefficient is specified. |
| [Few variables with an additional height conjecture](papers/conditional_few_variables/conditional13_20261109_v16.pdf) | **Weak abc with exponent $121/100$; ordinary abc or ordinary Szpiro suffices** | **13** | $<2^{44}$ | Exact count undetermined; **$<2^{509}$** | Every sufficiently large fixed odd shift $B$ works; sufficient threshold ineffective. |
| [Quartic under additional abc](papers/quartic_existence/quartic_abc97_20261109_v17.pdf) | **Ordinary rational abc** | **97** | **4, exact** | **879, exact** | $H(P_B)=\max(11600064,B^2+169997)$ for integer $B\ge3$; sufficient odd defining shift ineffective. |

The **97-variable quartic meets the target below one hundred under additional abc**. A count below 27 under the inherited premises, a count below ten under abc, and an inherited-premise quartic below one hundred remain open.

Monomials are counted in the polynomial coordinates, including the input, **after the fixed coefficient parameter is substituted and like terms are collected**. The three few-variable determinant polynomials have not been expanded. Their entries are certified support upper bounds, not exact monomial counts; the [support certificate](computation/few_variables/monomial-bound-certificate.json) gives the exact integer bounds and their derivation.

These are **conditional projection theorems**: under the arithmetic premises stated in their papers, the polynomials have rational input projection exactly $\mathbb Z$. The quantitative prime selection used by the quartics is derived from the cited prime-pattern estimates in the [prime-selection paper](papers/prime_selection/prime_selection_20261109_v12.pdf); it is not an additional independent conjecture. The collection makes no claim of a global minimum in the number of variables.

The 27-, 248-, 13-, and 97-variable results prove that all sufficiently large members of computable coefficient families work, with ineffective sufficient thresholds. The 29- and 322-variable constructions instead have certified fixed parameters and fully specified integer coefficients. Fixed parameters are coefficients, not extra variables. The numerical 27-variable example at exponent $137731$, and the conditional examples at shift $B=3$, are algebraic reproduction fixtures and are **not certified to define $\mathbb Z$**.

The 322-variable polynomial is the sum of squares of **294 quadratic equations**, and its largest coefficient has exactly **1,791,283 binary digits**. The 248-variable family uses **222 quadratic equations**; the additional-abc quartic uses **85**. All three quartics have integer content one. The first two support counts hold for every positive value of their fixed coefficient parameter, respectively $A_N=149^{2N+1}$ and $A_N=80989^{2N+1}$; the 879-monomial count holds for every positive integer shift $B$. These algebraic statements do not determine the ineffective defining thresholds.

### Additional height conjectures

The [thirteen-variable theorem](papers/conditional_few_variables/conditional13_20261109_v16.pdf) needs only the weak abc inequality with exponent $121/100$. A degree-four rational map supplies six rational contact values and the bound $h(t)\le\frac{121}{74}\log M(t)+C$. The projective height estimate
$h(1:u:v)\le\frac{121}{437}h(u^8+v^8)+C$ gives the strict absorption coefficient $14641/16169<1$. This replaces the Lucas and scalar-growth mechanisms. Three elliptic point roles and two pole certificates remain, with six local tests of order one. The exact degree majorant is **12,339,485,119,488**. More generally, any one weak abc exponent below $4/3$ suffices for thirteen coordinates with a suitable fixed even power.

The [97-variable abc quartic](papers/quartic_existence/quartic_abc97_20261109_v17.pdf) uses eight contacts symmetric about one, the scale $\beta^4+T^4$, and two factors at each detector. The two height estimates give the strict absorption coefficient $8/9$. With $r=(t-1)^2$, the relations $c=qr$, $k=cr$, and $k^2-30kc+273c^2-820cq+576q^2=kr$ compute the contact normalization using four coordinates. Three quadratic outputs compute the fourth-power scale. An affine change makes the input-comparison value a coordinate, so the fixed shift occurs only in the row $I_0-L_0+2X^2+B=0$. This gives 879 monomials and the quadratic coefficient-height formula in the table.

The [arithmetic-hypotheses paper](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) explains the other conjectures. **Ordinary Szpiro suffices for the thirteen-variable construction**, using its implication of weak abc with every exponent $6/5+\epsilon$. Modified Szpiro and the stated truncated Vojta conjecture supply ordinary abc. No variable reduction from RH, GRH, or Grimm is established. A Pell family shows why distinct prime assignments alone do not control odd valuations. Bombieri–Lang supplies polynomial injections by Poonen's theorem, but an injection does not eliminate its inverse's rational witnesses. Mazur's connected-component conjecture would forbid an existential definition of $\mathbb Z$ and is incompatible with premises that imply one.

The [restricted-abc paper](papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) proves why two available unconditional theorems do not yet remove the extra hypothesis. In the natural Frey family for a sum of even powers, the reduced denominator of $j$ grows exponentially in its logarithmic height, outside the small-denominator hypothesis. Along the integer witnesses required by the one-point construction, fixed asymmetric-size hypotheses also fail infinitely often. These are exact applicability obstructions, not evidence against abc; a different arithmetic family could still use those theorems.

### How the constructions attain these bounds

At every good unramified place of the elliptic curve, a nonzero reciprocal abscissa has even valuation. The [explicit quartic proof](papers/quartic/quartic322_20261109_v13.pdf) uses this parity to place sixteen local tests in four factors with distinct valuation classes. Smaller powers suffice, and the shared reference point needs formal depth ten. The proof establishes integrality of the comparison ratios before obtaining precision forty; it covers identity numerators and the enlarged reference-point chart.

The [248-variable construction](papers/quartic_existence/quartic248_20261109_v17.pdf) uses the source's underlying modular realization and the proved stronger contact-height theorem below. Two reflected five-contact blocks give a height exponent $7/4$. Their product is degree five in $r=(t-1)^2$ and takes four quadratic outputs to evaluate. The balanced normalization $R=F_{10}/(t-1)^{10}$ gives $F_{10}(1+q)=r^2r^3$; its reciprocal is affine in $q$. Three weight outputs $q^2,q^4,q^7$ suffice, using $q q^7=(q^4)^2$. Plain formal parameters give comparison orders four and one. The scalar denominator uses $R_s^4$. The sharper cubic logarithmic height bound, together with $149^{L_N}M_5(\beta)^3\mid c=|a-1|$, gives $h(\beta)\le2^{330770}149^{-L_N}c(1+\log c/3)$. The integral Lucas estimate $\log B\ge(c-5)\log(c-2)$ supplies strict absorption for sufficiently large fixed $N$. Every degenerate stratum is treated in the proof. No additional abc or Szpiro hypothesis is used.

The 248- and 322-variable systems use an invertible affine scalar change that makes the contact product itself a coordinate. Their normalizers are $R+\ell^2rR-A_Nr$, with $\ell=149$ and $\ell=80989$ respectively. Five exact nonsquare tests and the local preparation at $2,3,17$ justify the smaller prime in the 248-variable family.

The few-variable constructions use a guarded finite algebra and one additional rational coordinate. The [finite-algebra theorem](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) first isolates the algebraic branches on which the source guard is nonzero. The product of their guard values gives a quantitative separation bound, from which one polynomial element distinguishes all those branches. A rational reciprocal eigenvalue then recovers a rational source witness. The construction handles disappearing branches and inactive nilpotents. Its final product has 262,144 factors for the 27- and 29-variable constructions and 64 factors for the thirteen-variable construction. These products give the degree and coefficient bounds in the table. The source's nonzero-ordinate realization supplies a single conic chart and nonzero quadratic generators. All inherited restricted-converse and descent hypotheses remain explicit.

The [uniform scalar normalization](papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.pdf) supplies a positive rational function bounded above and below at the real places, with the required square denominator and fixed exceptional primes. Replacing the unbounded elliptic parameter by $y/(x^2+D)$ removes a real-approximation condition on the point carrying the large index. Its exact coefficient multiplier is controlled by a resultant in $X^2$. This is a proved preparation lemma; the published 27- and 29-variable specifications are unchanged. Their variable counts cannot be lowered simply by prescribing an index divisible by powers of the contact primes, because the elliptic reduction orders impose additional divisibility conditions.

## Read the papers

Each paper contains definitions, proofs, precise dependencies, and a ready-to-read PDF.

| Result | PDF | LaTeX |
|:--|:--|:--|
| Thirteen variables from weak abc; ordinary Szpiro suffices | [Read](papers/conditional_few_variables/conditional13_20261109_v16.pdf) | [Source](papers/conditional_few_variables/conditional13_20261109_v16.tex) |
| The 97-variable quartic under additional rational abc | [Read](papers/quartic_existence/quartic_abc97_20261109_v17.pdf) | [Source](papers/quartic_existence/quartic_abc97_20261109_v17.tex) |
| Applicability of restricted unconditional abc estimates | [Read](papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) | [Source](papers/restricted_abc/restricted_abc_inputs_20261109_v17.tex) |
| Additional arithmetic hypotheses and their implications | [Read](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) | [Source](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.tex) |
| Degree and coordinate lower bounds | [Read](papers/lower_bounds/lower_bounds_20261109_v15.pdf) | [Source](papers/lower_bounds/lower_bounds_20261109_v15.tex) |
| Finite-algebra separation on the nonzero guard locus | [Read](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) | [Source](papers/finite_algebra/active_finite_algebra_20261109_v15.tex) |
| Finite correspondences over abelian varieties and denominator obstructions | [Read](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) | [Source](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.tex) |
| Obstructions to fixed parameters in pole certificates | [Read](papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf) | [Source](papers/pole_parameters/fixed_pole_parameters_20261109_v17.tex) |
| A local obstruction to a quartic pole equation | [Read](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) | [Source](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.tex) |
| Obstructions to sharing and multiplying pole certificates | [Read](papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf) | [Source](papers/pole_parameters/combining_pole_certificates_20261109_v16.tex) |
| Density and algebraic avoidance for pole witnesses | [Read](papers/pole_parameters/pole_witness_density_20261109_v14.pdf) | [Source](papers/pole_parameters/pole_witness_density_20261109_v14.tex) |
| The 27-variable family, degree less than $2^{87}$ | [Read](papers/few_variables27/few_variables27_nontorsion_20261109_v15.pdf) | [Source](papers/few_variables27/few_variables27_nontorsion_20261109_v15.tex) |
| The explicit 29-variable polynomial, degree less than $2^{89}$ | [Read](papers/few_variables/explicit29_nontorsion_20261109_v15.pdf) | [Source](papers/few_variables/explicit29_nontorsion_20261109_v15.tex) |
| The 248-variable quartic from ten symmetric contacts | [Read](papers/quartic_existence/quartic248_20261109_v17.pdf) | [Source](papers/quartic_existence/quartic248_20261109_v17.tex) |
| The explicit 322-variable quartic from even valuations | [Read](papers/quartic/quartic322_20261109_v13.pdf) | [Source](papers/quartic/quartic322_20261109_v13.tex) |
| Differential evaluation, modular Jacobian heights, and the cubic logarithmic contact bound | [Read](papers/contact_heights/evaluation_of_differentials_20261109_v17.pdf) | [Source](papers/contact_heights/evaluation_of_differentials_20261109_v17.tex) |
| Disjoint contact sets and height amplification | [Read](papers/contact_heights/contact_height_amplification_20261109_v13.pdf) | [Source](papers/contact_heights/contact_height_amplification_20261109_v13.tex) |
| A four-coordinate locally dense proper subset of the rational subfield | [Read](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf) | [Source](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.tex) |
| Uniform real preparation of the scalar elliptic certificate | [Read](papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.pdf) | [Source](papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.tex) |
| Structural constraints on reducing elliptic witnesses | [Read](papers/elliptic_charts/structural_constraints_20261109_v13.pdf) | [Source](papers/elliptic_charts/structural_constraints_20261109_v13.tex) |
| Shared local weights and exact quartic coefficient height | [Read](papers/local_tests/shared_local_weights_20261109_v12.pdf) | [Source](papers/local_tests/shared_local_weights_20261109_v12.tex) |
| Weighted finite-algebra elimination with one extra coordinate | [Read](papers/finite_algebra/weighted_finite_algebra_20261109_v12.pdf) | [Source](papers/finite_algebra/weighted_finite_algebra_20261109_v12.tex) |
| Quantitative prime selection and completeness of local weights | [Read](papers/prime_selection/prime_selection_20261109_v12.pdf) | [Source](papers/prime_selection/prime_selection_20261109_v12.tex) |
| Rings of integers, subfields, norm images, and transfer obstructions | [Read](papers/number_fields/number_field_definability_20261109_v12.pdf) | [Source](papers/number_fields/number_field_definability_20261109_v12.tex) |
| A local obstruction to correction-free quadratic input maps | [Read](papers/input_normalization/quadratic_input_obstruction_20261109_v12.pdf) | [Source](papers/input_normalization/quadratic_input_obstruction_20261109_v12.tex) |
| Local tests with different required orders: valuation proof and exact circuits | [Read](papers/local_tests/mixed_valuation_tests_20261109_v11.pdf) | [Source](papers/local_tests/mixed_valuation_tests_20261109_v11.tex) |
| A sharp degree-four threshold for finite scalar fibers over every number field | [Read](papers/scalar_heights/cubic_scalar_height_obstruction_20261109_v11.pdf) | [Source](papers/scalar_heights/cubic_scalar_height_obstruction_20261109_v11.tex) |
| Effective heights of elliptic sums with coprime indices | [Read](papers/coprime_sums/coprime_elliptic_sums_20261109_v11.pdf) | [Source](papers/coprime_sums/coprime_elliptic_sums_20261109_v11.tex) |
| Optimal degree-six square predicates over quadratic extensions | [Read](papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) | [Source](papers/square_predicates/quadratic_square_predicates_20261108_v10.tex) |
| Effective heights of arbitrary elliptic abscissa sums | [Read](papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) | [Source](papers/effective_sums/effective_elliptic_sums_20261108_v10.tex) |
| Aggregate elliptic trace heights | [Read](papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) | [Source](papers/trace_heights/aggregate_trace_height_20261108_v9.tex) |
| Square-root charts over quadratic extensions | [Read](papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) | [Source](papers/quadratic_squares/quadratic_square_chart_20261108_v9.tex) |
| Square-abscissa charts for the elliptic subgroup | [Read](papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) | [Source](papers/square_abscissa/square_abscissa_charts_20261108_v9.tex) |
| Scalar contact normalization | [Read](papers/scalar_normalization/scalar_normalization_20261108_v9.pdf) | [Source](papers/scalar_normalization/scalar_normalization_20261108_v9.tex) |
| Arithmetic dependencies and the corrected source argument | [Read](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) | [Source](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex) |
| Eliminating finite algebraic choices with one extra coordinate | [Read](papers/finite_algebra/finite_algebra_20261107_v7.pdf) | [Source](papers/finite_algebra/finite_algebra_20261107_v7.tex) |
| Combining equations and extending number fields | [Read](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.pdf) | [Source](papers/systems_and_fields/systems_and_field_extensions_20261108_v8.tex) |
| An obstruction to one-parameter elliptic point presentations | [Read](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.pdf) | [Source](papers/elliptic_charts/elliptic_chart_obstruction_20261107_v7.tex) |
| Explicit elliptic height estimates | [Read](papers/elliptic_heights/elliptic_heights_20261108_v8.pdf) | [Source](papers/elliptic_heights/elliptic_heights_20261108_v8.tex) |
| Uniform formal-logarithm estimates | [Read](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.pdf) | [Source](papers/elliptic_logarithms/elliptic_logarithms_20261108_v8.tex) |

### Proof and replication dependencies

The following complete results supply the arithmetic arguments and exact source circuits used by the leading constructions.

| Result | PDF | LaTeX |
|:--|:--|:--|
| Shared-weight source with two scales | [Read](papers/quartic_existence/quartic297_20261109_v12.pdf) | [Source](papers/quartic_existence/quartic297_20261109_v12.tex) |
| Shared-weight source with three scales | [Read](papers/quartic/quartic342_20261109_v12.pdf) | [Source](papers/quartic/quartic342_20261109_v12.tex) |
| Mixed local-test source with two scales | [Read](papers/quartic_existence/quartic301_20261109_v11.pdf) | [Source](papers/quartic_existence/quartic301_20261109_v11.tex) |
| Mixed local-test source with three scales | [Read](papers/quartic/quartic351_20261109_v11.pdf) | [Source](papers/quartic/quartic351_20261109_v11.tex) |
| Two-scale quartic source and trace-height argument | [Read](papers/quartic_existence/quartic317_family_20261108_v9.pdf) | [Source](papers/quartic_existence/quartic317_family_20261108_v9.tex) |
| Three-scale quartic source and effective parameter | [Read](papers/quartic/quartic370_20261108_v10.pdf) | [Source](papers/quartic/quartic370_20261108_v10.tex) |
| Exact arithmetic source for the quartic families | [Read](papers/quartic/quartic389_20261108_v9.pdf) | [Source](papers/quartic/quartic389_20261108_v9.tex) |
| Baseline quartic arithmetic contract | [Read](papers/quartic/quartic392_20261108_v8.pdf) | [Source](papers/quartic/quartic392_20261108_v8.tex) |
| Few-variable arithmetic source and finite-algebra proof | [Read](papers/few_variables/few_variables_20261108_v8.pdf) | [Source](papers/few_variables/few_variables_20261108_v8.tex) |

## Arithmetic scope

The inherited arithmetic inputs are the specified elliptic group and index-height assertions, the contact-height theorem, pole obstruction and realization, and simultaneous prime patterns. The additional-conjecture constructions replace the exponent-nineteen contact-height input by their proved consequences of weak abc or ordinary abc. They retain the specified elliptic, pole, and prime-pattern premises. The few-variable constructions retain the restricted-converse and descent hypotheses used in the source realization proof. The quartics additionally use the quantitative consequence of the cited prime-pattern estimates proved in the prime-selection paper. The [arithmetic input guide](docs/arithmetic_inputs.md) separates these inputs from finite coefficient verification.

The aggregate trace-height argument applies [Von Buhren's Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf) after verifying its geometric hypotheses. Its additive constant is ineffective. Enlarging a fixed coefficient absorbs that constant in the 27- and 248-variable existence theorems and, through its one-point case, in the 13- and 97-variable additional-conjecture theorems. The explicit 29-variable and 322-variable constructions instead use the proved effective height estimate for the two components of an elliptic sum.

## Structural results and number fields

The [lower-bound paper](papers/lower_bounds/lower_bounds_20261109_v15.pdf) proves that a single equation with infinite input projection contained in a ring of $S$-integers over a number field has **degree at least four**. Any finite system needs at least **three total coordinates**. Systems of equations of degree at most three need at least four; quadratic systems need at least **five**. Over $\mathbb Q$, every globally nonnegative quartic also needs at least **five total coordinates**, whether or not it is a sum of squares. A nonnegative polynomial in three coordinates would need degree at least eight. These are lower bounds, not assertions that the bounds are attained. The sharp unrestricted minimum remains unknown.

A hypothetical three-coordinate quartic defining $\mathbb Z$ must be absolutely irreducible, have Zariski-dense smooth rational points, and change sign. The nonnegative-quartic obstruction uses its singular locus and the geometry of surfaces of degree at most three. The proofs allow the stated open conditions and finite alternatives.

Over $\mathbb Q$, any finite quadratic system becomes one quartic by summing its squares, without adding coordinates. Over a fixed number field, $s$ equations of degree at most $d$ can be combined, without extra coordinates, into one equation of degree at most $\lceil\sqrt{s}\rceil d$.

For every quadratic extension $K/F$ of number fields, square membership has a complete **degree-six polynomial test using two input components and one auxiliary coordinate over $F$**. Degree six, and degree four in that auxiliary coordinate, are optimal in the stated class of equality-based definitions. Over $\mathbb Q(\sqrt2)$ the displayed polynomial has ten monomials and coefficient height seven. These are square predicates, not definitions of rings of integers.

The scalar-height paper proves a separate sharp degree threshold over **every number field**: no rational function of two variables with numerator and denominator of degree at most three is finite-to-one on any nonempty archimedean open set. A suitable quartic has finite fibers. This concerns arbitrary pairs; it does not rule out height comparisons on a restricted set of elliptic multiples.

For pairwise coprime elliptic indices and positive abscissas over a totally real field, the sum-height paper gives an effective bound with loss at most the finite-place height of the fixed base point. On the specified curve, adding a fixed abscissa when the number of summands is even removes the loss entirely. Coprimality is an additional hypothesis and is not assumed before it is established by the arithmetic construction.

No one unchanged existential formula can define rings of integers in every finite extension. The field paper proves this obstruction and gives an exact quadratic-field counterexample for the baseline quartic. It does not exclude a different defining polynomial for each number field.

The [number-field paper](papers/number_fields/number_field_definability_20261109_v12.pdf) proves the following equivalences for a number field $K$:

$$
\mathcal O_K\text{ Diophantine in }K
\quad\Longleftrightarrow\quad
\mathbb Z\text{ Diophantine in }K.
$$

This uses the established theorem that $\mathbb Z$ is Diophantine in $\mathcal O_K$. Assuming separately that $\mathbb Z$ is Diophantine in $\mathbb Q$, these properties are also equivalent to $\mathbb Q$ being Diophantine in $K$. For every finite characteristic-zero extension $L/K$, defining $K$ in $L$ is equivalent to defining the relative norm image in $L$, or the norm graph, or the trace graph. A finite-difference identity gives the norm-image reduction with explicit coordinate bounds.

A genuine counterexample to the ring-of-integers question would remain a counterexample in every finite extension; it would yield a totally imaginary Galois counterexample. A fixed finite collection of unchanged formulas fails simultaneously in a suitable extension, but this does not exclude formulas chosen separately for each field. **No actual counterexample and no general positive theorem for fraction fields is established here.**

Rank stability supplies infinite Diophantine subsets of the rational subfield, rather than a definition of that subfield by itself. On $y^2=x^3-2$, all rational abscissas have even $5$-adic valuation, although $(3,5)$ has infinite order. Therefore ratios and finite products of these abscissas cannot represent $5$. This obstructs that multiplicative strategy; it does not obstruct sums or more elaborate definitions.

The [elliptic-ratio paper](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf) gives an explicit polynomial with **four total coordinates, degree 13, and height 162**. In eight specified real or imaginary quadratic fields, it defines the same proper subset $D\subset\mathbb Q$: it contains $0,1$ and excludes $-1$. Nevertheless, $D$ is simultaneously dense in every finite product of rational completions, and every local input has witnesses over every completion of each field. Unconditional elliptic rank calculations certify the global exclusion. This is an obstruction to a proposed rational-subfield construction, not a counterexample to defining a ring of integers. The same paper proves that a Diophantine set containing $\mathbb Z$ with uniformly bounded integral denominators would suffice to define the full ring of integers.

The same paper applies [Corvaja–Zannier, Theorem 1.1](https://arxiv.org/html/2608.28255v1) to show that **every fixed finite collection of rational combinations of abelian point coordinates misses infinitely many integers**. This includes finite sums, products, and ratios of the stable-elliptic sets, and a separate four-coordinate slope polynomial of degree 11 and height 162. Consequently these operations cannot by themselves produce the bounded-denominator set containing all integers required by the integral-basis criterion. The [finite-correspondence paper](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) extends this obstruction: if each geometric fiber over an abelian variety has only finitely many output values, the rational outputs meet every finitely generated multiplicative subgroup in a finite set. Quasi-finite covers are included. Bounded-denominator constructions with soluble unirational fibers, or with smooth proper genus-one fibers equipped with an ample line bundle, are also excluded. The genus-one argument uses Siegel, uniform torsion, and a finite cover of the relative Jacobian. Exceptional positive-dimensional fibers require explicit treatment; a smooth example birational to a product of elliptic curves nevertheless represents every field element along four exceptional affine lines. Higher-genus fibers are not excluded by these results.

The [differential-evaluation theorem](papers/contact_heights/evaluation_of_differentials_20261109_v17.pdf) bounds a Jacobian's stable Faltings height by the discriminant of one unramified fibre. Integral differentials map into the trace-dual order of that fibre; the complex mean-value inequality bounds the determinant of evaluation. For the inherited modular realization, this gives $h(a)<2^{330770}M_5(a)^3(1+\log M_5(a))<2^{330789}M_5(a)^{7/2}$, without an additional abc or Szpiro assumption. Disjoint contact blocks give exponent $7/(2r)$ for $r$ blocks. The constant and modular-curve identities have exact certificates.

The [input-map paper](papers/input_normalization/quadratic_input_obstruction_20261109_v12.pdf) proves that no integer quadratic can simultaneously reflect rational integrality, take odd values at every integer, and make the specified uncorrected five-contact product a square in $\mathbb Q_2$ at every integer. If positivity at all integers is also required, degree four is optimal in that restricted class, attained by $8X^4+3$. This is a restriction of that normalization, not a lower bound for all defining polynomials. Current research priorities and their proved constraints appear in the [research guide](docs/research_directions.md).

The [fixed-parameter pole obstruction](papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf) rules out every constant rational choice of the actual pole parameter in the stated certificate. The fixed conic-chart values $\tau=\pm1,\pm17$ also fail on prepared inputs, with unconditional rank and descent certificates. For $\tau=\pm17$, failing prepared inputs are dense in every real subinterval of $(0,17)$, so shrinking the allowed real interval cannot repair universal completeness. These statements concern all prepared inputs and leave the narrower prime-pattern-generated families open.

The [quartic pole equation](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) gives the required odd-valuation implication with one rational parameter, but fails completeness on prepared inputs. For every $m\ge1$, the prepared number $b_m=409(204/1013^m)^2$ makes $Y^2=1+b_m(1+b_mv^2)^2$ insoluble over $\mathbb Q_{1013}$, including at infinity. These inputs tend to zero. More generally, no finite fixed set of nonzero rational coefficients $\kappa$ makes $Y^2=1+\kappa b(1+bv^2)^2$ complete on all prepared inputs. The proof leaves completeness on the restricted comparison-prime family unresolved.

The [paper on combining pole certificates](papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf) gives two further exact obstructions. One prepared pair admits no common actual pole parameter, including its degenerate values. For the eight symmetric contacts, the reflection identity $R(2-t)=R(t)$ makes $R(\lambda)R(a\lambda)$ a square at $\lambda=2/(a+1)$ for arbitrarily large scale height, so simply multiplying these detectors loses the needed odd radical. Neither result excludes every possible replacement. The [density theorem](papers/pole_parameters/pole_witness_density_20261109_v14.pdf) permits avoiding finitely many polynomial zero sets for independent witnesses; it does not imply a common conic-chart parameter exists.

## Reproduce the results

The polynomial constructions and structural algebraic certificates require Python 3.10 or newer and its standard library:

~~~sh
python3 scripts/verify.py --full
~~~

The current leading quartic theorems use 248 and 322 variables under the inherited premises, and 97 variables under additional ordinary abc. Intermediate coefficient tables are retained for exact reconstruction; their coefficient checks alone do not assert an integer projection.

The standard-library verifier reconstructs the pinned source circuits, independently checks every quartic coefficient and the affine normalizations, rebuilds the 27-, 29-, and weak-abc 13-variable specifications using separation on the nonzero guard locus, and checks their degree, coefficient, and support bounds. It reconstructs the parity-based quartics and the disjoint-contact certificates, and checks the finite identities and residue certificates supporting the number-field, pole-merger, and input-map results. It works in a temporary copy and leaves published inputs unchanged. The numerical 27-variable example and the conditional shift-three examples are algebraic reproducibility fixtures and are **not** certified to exceed their ineffective defining thresholds.

The [verification receipt](data/verification-v17.json) records **82 passing stages**, including the unconditional PARI rank and fixed-pole descent calculations and the exact subtraction identity. The standard-library route runs 77 stages.

To additionally rerun the unconditional elliptic rank calculations and the exact function-field subtraction check, install `cypari2` and use `python3 scripts/verify.py --full --with-pari`. The supplied rank certificates record exact bounds and torsion computations; analytic rank and BSD are not used.

The [reproducibility guide](docs/reproducibility.md) gives individual commands and verification boundaries. The [data-format guide](docs/data_format.md) explains the complete coefficient tables and finite-algebra specifications. [MANIFEST.json](MANIFEST.json) records file sizes and SHA-256 hashes; [data/results.json](data/results.json) records exact bounds, effectiveness, and theorem scope.

To rebuild the PDFs with a standard TeX installation:

~~~sh
python3 scripts/build_papers.py
~~~

## Sources and license

The papers identify the underlying sources, including [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the cited OpenAI preprint, Sun's theorem, Von Buhren's height theorem, and primary references for the structural results. Computational provenance pins source commits and exact input bytes.

Original project contributions are licensed under **Creative Commons Attribution 4.0 International**: [license](LICENSE). Third-party material retains its existing notices and rights; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) provides citation metadata. The repository includes computer-assisted mathematical writing and verification; the hypotheses and proof of each theorem are stated in its paper.
