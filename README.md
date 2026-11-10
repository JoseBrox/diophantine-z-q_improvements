# Polynomial presentations of the integers over the rationals

Mathematical proofs and exact computational specifications for defining the integers by one polynomial equation over the rationals.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, the required equality is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}=\mathbb Z.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height is the largest absolute integer coefficient after fixed coefficient parameters have been substituted. The optimization priorities are the number of variables, degree, and coefficient height, in that order.

## Main results and arithmetic assumptions

The projection theorems retain the arithmetic premises stated in their papers: the specified elliptic group and index-height statements, contact heights or the underlying modular realization where used, the pole obstruction and nonzero realization, and simultaneous prime patterns. **“None” below means no additional conjecture beyond those premises.** The abc and Szpiro hypotheses are additional. Finite coefficient calculations do not prove these arithmetic inputs.

| Construction | Additional hypothesis | Total variables | Degree | Nonzero monomials | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|:--|
| [Fewest variables under inherited premises](papers/few_variables25/few_variables25_merged_20261110_v18.pdf) | None | **25** | $<2^{87}$ | Exact count unknown; $<2^{2035}$ | Every sufficiently large fixed odd exponent works; sufficient threshold ineffective. |
| [Quartic under inherited premises](papers/quartic_existence/quartic238_20261110_v18.pdf) | None | **238** | **4, exact** | **2,924, exact** | $H(P_N)=149^{4N+2}+1$ for $N\ge53$; sufficient defining threshold ineffective. |
| [Fully specified construction](papers/few_variables/explicit29_nontorsion_20261109_v15.pdf) | None | **29** | $<2^{89}$ | Exact count unknown; $<2^{2417}$ | $H(F)\le2^{2^{99}}$; exponent $137731$ is certified under the premises. |
| [Fully specified quartic](papers/quartic/quartic318_20261110_v18.pdf) | None | **318** | **4, exact** | **5,060, exact** | $H(P)=80989^{109858}+1$; all coefficients specified. |
| [Few variables under a height conjecture](papers/conditional_few_variables/conditional13_20261109_v16.pdf) | **Weak abc with exponent $121/100$; ordinary abc or ordinary Szpiro suffices** | **13** | $<2^{44}$ | Exact count unknown; $<2^{509}$ | Every sufficiently large fixed odd shift works; sufficient threshold ineffective. |
| [Quartic under abc](papers/quartic_existence/quartic_abc93_20261110_v18.pdf) | **Ordinary rational abc** | **93** | **4, exact** | **920, exact** | $H(P_B)=\max(4153456,B^2+797687)$ for $B\ge3$; sufficient odd defining shift ineffective. |

The quartics are sums of **212**, **290**, and **81** primitive quadratic squares, respectively, and have integer content one. Their monomial counts are exact after collecting all terms with the same coordinate monomial. The determinant polynomials with few variables have not been expanded; their support entries are certified upper bounds.

Fixed parameters are coefficients, not quantified variables. An algebraic coefficient-height threshold such as $N\ge53$ does not certify the threshold for defining $\mathbb Z$. The supplied $L=3$ fixture for the 25-variable existence family and the conditional $B=3$ fixtures are **not certified defining members**. The explicit 29- and 318-variable constructions have separately proved numerical sufficient parameters. No global minimum in the number of variables is claimed. See [arithmetic inputs](docs/arithmetic_inputs.md) and [machine-readable results](data/results.json).

## Arithmetic and algebraic methods

### A common elliptic point in four field coordinates

For $E:y^2=x^3-Dx$ and a suitable fixed point $P$, three quadratic equations retain the four values

$$
\frac{y(H)}{x(H)},\quad\frac{y(H-P)}{x(H-P)},\quad\frac1{x(H)},\quad\frac1{x(H-P)}.
$$

The [fixed-difference theorem](papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) identifies every solution, including the cases where a leading coefficient vanishes. Its equations and direct formal-parameter ratios give the current 238- and 93-variable quartics. An explicitly invertible rational change of the six component equations controls coefficient size; its determinant is $-1/362963666515968$. The expanded quartics and every changed equation have independent exact reconstructions.

The 238-variable construction uses ten reflected contacts, a balanced contact product, and five factors for its sixteen local tests. Its scalar certificate and a Lucas estimate give the global contradiction. The abc quartic uses eight symmetric contacts and the scale $\beta^4+T^4$; the contact and projective-height estimates give the strict absorption coefficient $8/9$.

### Rational normalization of local conditions

The **25-variable family** combines the scalar divisibility conditions with the comparison conditions in two pole predicates. Nine elliptic point-coordinate pairs, the input, a slope, and two pole-parameter pairs give 24 rational coordinates; one separating coordinate eliminates the remaining finite algebraic choices. Its exact degree majorant is **104,263,275,909,198,787,271,196,672**, uniformly in the fixed odd coefficient exponent.

The function

$$\Psi_z(D)=\frac{zD^2}{1+zD^2}$$

has valuation $\max(0,v(z)+2v(D))$ whenever $v(z)$ is odd. Thus a factor $z^K\Psi_z(D)$ remains sufficiently divisible even when $D$ has an arbitrarily deep pole. At a unit coefficient, positive valuation of $\Psi_z(D)$ is equivalent to positive valuation of $D$. The [local-normalization paper](papers/local_tests/rationally_normalized_local_tests_20261110.pdf) proves the corresponding extraction results for two collections of tests, treats nonzero even valuations of the other coefficient, and constructs two balanced contact functions with the required unit alternative.

At every comparison prime, the local conditions force divisibility of either the integer residual $N$ or the scalar index $c$. Thus $M_j^4\mid Nc$; primes shared by the two arithmetic coefficients are retained. Two disjoint contact groups and the refined modular height estimate close the global argument with exponents $19/24<1$ and $95/48<2$. The sufficient fixed coefficient is ineffective.

### Contact heights and finite algebraic choices

The [scalar-character refinement](papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf), using the source's normalized modular realization, proves

$$
h(a)<2^{330670}M_5(a)^3(1+\log M_5(a))<2^{330671}M_5(a)^{7/2}.
$$

It determines the relevant character order from $(\varepsilon\chi)^2=1$ and also evaluates differentials on a unit fibre. A stronger restricted exponent is proved when the powers of two dividing the contact primes minus one are bounded. The paper gives an obstruction to imposing that restriction throughout the scalar family, so it is not used as an unrestricted height theorem.

The constructions with few variables eliminate finite algebraic choices using [separation on the nonzero guard locus](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf). One additional rational coordinate recovers a rational character of the finite source algebra. The argument includes disappearing branches and inactive nilpotents. Under weak abc, three elliptic point roles and two pole certificates suffice; the thirteen-variable degree majorant is **12,339,485,119,488**. The [arithmetic-hypotheses paper](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) establishes the stated implication from ordinary Szpiro. No reduction below thirteen under abc is established here.

For the six contacts used in that construction, a [rational involution](papers/pole_parameters/six_contact_product_obstruction_20261110.pdf) makes a product of two contact functions a negative square while the scale height tends to infinity. Consequently an unrestricted height estimate based only on that product's odd radical cannot justify merging the two pole predicates, even under abc. This obstruction does not cover the more restricted scales imposed by the defining source.

## Current papers

Every listed paper has a complete LaTeX source beside its PDF. The supporting papers are organized by mathematical subject.

| Subject | Main paper |
|:--|:--|
| Few variables under inherited premises | [Defining family](papers/few_variables25/few_variables25_merged_20261110_v18.pdf) |
| Quartics under inherited premises | [238-variable family](papers/quartic_existence/quartic238_20261110_v18.pdf) |
| Fully specified coefficients | [29-variable polynomial](papers/few_variables/explicit29_nontorsion_20261109_v15.pdf), [318-variable quartic](papers/quartic/quartic318_20261110_v18.pdf) |
| Additional height conjectures | [13-variable family](papers/conditional_few_variables/conditional13_20261109_v16.pdf), [93-variable quartic](papers/quartic_existence/quartic_abc93_20261110_v18.pdf) |
| Elliptic equations | [Three quadrics for two translated parameters](papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) |
| Local conditions | [Rational normalization of valuation tests](papers/local_tests/rationally_normalized_local_tests_20261110.pdf) |
| Contact heights | [Scalar characters and contact heights](papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf), [differential evaluation](papers/contact_heights/evaluation_of_differentials_20261109_v17.pdf) |
| Elimination | [Separation in finite algebras](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) |
| Arithmetic dependencies | [Inherited inputs](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf), [prime selection](papers/prime_selection/prime_selection_20261109_v12.pdf), [additional conjectures](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) |
| Lower bounds | [Degree and coordinate obstructions](papers/lower_bounds/lower_bounds_20261109_v15.pdf) |
| Number fields | [Definability reductions](papers/number_fields/number_field_definability_20261109_v12.pdf), [elliptic ratios](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf), [finite correspondences](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf) |
| Limits of pole simplifications | [Fixed parameters](papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf), [combined certificates](papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf), [six-contact products](papers/pole_parameters/six_contact_product_obstruction_20261110.pdf), [quartic pole equation](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) |
| Restricted unconditional abc estimates | [Applicability and obstructions](papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) |

## Rings of integers in number fields

No counterexample and no general positive theorem for $\mathcal O_K$ in its fraction field $K$ is established here. The [number-field reductions](papers/number_fields/number_field_definability_20261109_v12.pdf) prove

$$
\mathcal O_K\text{ Diophantine in }K
\quad\Longleftrightarrow\quad
\mathbb Z\text{ Diophantine in }K.
$$

This uses the established definability of $\mathbb Z$ in $\mathcal O_K$. Assuming separately a definition of $\mathbb Z$ in $\mathbb Q$, the conditions are also equivalent to the rational subfield being Diophantine in $K$. A genuine counterexample would remain a counterexample in every finite extension and would therefore yield a totally imaginary Galois example.

The papers distinguish these general questions from failures of particular constructions. One unchanged formula cannot work in every finite extension. Rank stability alone gives infinite Diophantine subsets of the rational subfield, but not necessarily the whole subfield. Exact examples are locally dense while omitting a rational integer globally. The finite-correspondence results obstruct several methods based on bounded denominators and rational functions of abelian point coordinates; they do not exclude all Diophantine definitions.

The [lower-bound paper](papers/lower_bounds/lower_bounds_20261109_v15.pdf) proves degree at least four for a single defining equation, at least three total coordinates for any finite system, and at least five for a quadratic system or a globally nonnegative quartic over $\mathbb Q$. These bounds leave a large gap. [Research directions](docs/research_directions.md) identifies the arithmetic changes needed to close it.

## Reproduce the results

Python 3.10 or newer and its standard library suffice for the polynomial reconstructions and finite algebraic certificates:

~~~sh
python3 scripts/verify.py --full
~~~

The verifier works in a temporary copy. It checks source hashes, reconstructs every required dependency, independently expands the quartics, and checks the finite-algebra specifications, degree and support bounds, local identities, and exceptional cases. Intermediate coefficient families are retained as exact reconstruction dependencies, not as current numerical records.

Optional exact elliptic ranks, descents, and function-field calculations use `cypari2`:

~~~sh
python3 scripts/verify.py --full --with-pari
~~~

The [standard-library verification](data/verification-standard-v18.json) passed all **89 stages**. The [verification including PARI](data/verification-v18.json) passed all **95 stages**. These calculations use exact rank bounds and torsion computations, not analytic rank or BSD. The [reproducibility guide](docs/reproducibility.md) gives individual commands and their scope. [Data formats](docs/data_format.md), [quartic provenance](computation/quartic/PROVENANCE.json), [results](data/results.json), and [MANIFEST.json](MANIFEST.json) identify the complete specifications and their hashes.

To rebuild the papers with a standard TeX installation:

~~~sh
python3 scripts/build_papers.py
~~~

## Sources and license

Primary references appear in the papers. They include [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the pinned source manuscript, Sun's prime-pattern theorem, von Buhren's height theorem, and the cited structural results. Computational provenance fixes source commits and exact input bytes.

Original contributions are licensed under [CC BY 4.0](LICENSE). Third-party material retains its existing notices; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) supplies citation metadata. The collection includes computer-assisted mathematical writing and verification; each theorem states its assumptions and proof.
