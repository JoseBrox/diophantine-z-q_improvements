# Polynomial presentations of the integers over the rationals

Mathematical proofs and exact computational specifications for defining the integers by one polynomial equation over the rationals.

For an integer polynomial $F(X,Y_1,\ldots,Y_m)$, the required equality is

$$
\{x\in\mathbb Q:\exists\boldsymbol y\in\mathbb Q^m,\ F(x,\boldsymbol y)=0\}=\mathbb Z.
$$

**Every variable count includes the input.** Degree means total degree. Coefficient height is the largest absolute integer coefficient after fixed coefficient parameters have been substituted. The optimization priorities are the number of variables, degree, and coefficient height, in that order.

## Main results and arithmetic assumptions

The projection theorems retain the arithmetic premises stated in their papers: the specified elliptic group and index-height statements, the full normalized modular realization where used, the pole obstruction and nonzero realization, and simultaneous prime patterns. **“None” below means no additional conjecture beyond those premises.** The abc and Szpiro hypotheses are additional. Finite coefficient calculations do not prove these arithmetic inputs.

| Construction | Additional hypothesis | Total variables | Degree | Nonzero monomials | Coefficients and effectiveness |
|:--|:--|--:|:--|:--|:--|
| [Fewest variables under inherited premises](papers/few_variables25/few_variables25_merged_20261110_v19.pdf) | None | **25** | $<2^{85}$ | Exact count unknown; $<2^{1979}$ | Every sufficiently large fixed odd exponent works; sufficient threshold ineffective. |
| [Quartic under inherited premises](papers/quartic_existence/quartic226_20261110_v21.pdf) | None | **226** | **4, exact** | **2,835, exact** | $H(P_N)=149^{4N+2}+1$ for $N\ge53$; sufficient defining threshold ineffective. |
| [Fully specified construction](papers/few_variables27/explicit27_20261110_v19.pdf) | None | **27** | $<2^{87}$ | Exact count unknown; $<2^{2192}$ | $H(F)<2^{2^{99}}$; fixed exponent $20483$ is certified under the premises. |
| [Fully specified quartic](papers/quartic/quartic262_20261110_v21.pdf) | None | **262** | **4, exact** | **3,494, exact** | $H(P)=149^{38730}+1$; all coefficients specified, with $N=9682$. |
| [Few variables under weak abc](papers/conditional_few_variables/direct_input13_20261110_v22.pdf) | **Weak abc with exponent $121/100$; ordinary abc or ordinary Szpiro suffices** | **13** | $\le11774654098433<2^{44}$ | Exact count unknown; $<2^{508}$ | Sixth-power scale; every sufficiently large fixed odd shift works, with an ineffective threshold. |
| [Lower degree under stronger weak abc](papers/conditional_few_variables/direct_input13_20261110_v22.pdf) | **Weak abc with exponent $16/15$; ordinary abc suffices** | **13** | $\le11212784195585<2^{44}$ | Exact count unknown; $<2^{507}$ | Fourth-power scale; every sufficiently large fixed odd shift works, with an ineffective threshold. |
| [Quartic under abc](papers/quartic_existence/quartic_abc87_20261110_v21.pdf) | **Ordinary rational abc** | **87** | **4, exact** | **918, exact** | $H(P_B)=\max(4153456,B^2+797681)$ for $B\ge3$; sufficient odd defining shift ineffective. |

The three quartics are sums of **200**, **234**, and **75** primitive quadratic squares, respectively, and have integer content one. Their monomial counts are exact after collecting all terms with the same coordinate monomial. The determinant polynomials with few variables have not been expanded; their support entries are certified upper bounds.

Fixed parameters are coefficients, not quantified variables. An algebraic coefficient-height threshold such as $N\ge53$ does not certify the threshold for defining $\mathbb Z$. The supplied $L=3$ fixture for the 25-variable existence family and the conditional $B=3$ fixtures are **not certified defining members**. The explicit 27- and 262-variable constructions have separately proved numerical sufficient parameters. No global minimum in the number of variables is claimed. See [arithmetic inputs](docs/arithmetic_inputs.md) and [machine-readable results](data/results.json).

## Arithmetic and algebraic methods

### Quadratic contact-height bounds from modular multiplicity

The [multiplicity theorem](papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf), under the source's full normalized modular realization, proves

$$
h(a)\le C_2M_5(a)^2(1+\log M_5(a))^2,
\qquad C_2<2^{221231}.
$$

In particular,

$$h(a)<2^{221234}M_5(a)^{7/3}.$$

These bounds hold for every rational argument outside the contacts. They impose no congruence restriction on the contact primes and add no abc or Szpiro conjecture.

The key fact is that, over the field realizing the quaternionic surface, every coefficient conjugate of its modular form has the same rational Frobenius traces. The corresponding modular abelian variety is therefore isogenous to a power $A^r$ of the surface. Its coefficient field contains the nebentypus values, giving $r\ge\varphi(s)/2$ when the character has order $s$. Rémond's height inequality selects a surface subquotient whose height is bounded by the ambient height divided by $r$; a dimension-two isogeny theorem then transfers that bound to $A$. The [scalar-character result](papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf) supplies the power-of-two character bound used for the explicit constant. The finite numerical certificate is separate from these representation and height arguments.

### Raw comparison tests and linear scalar normalization

The **25-variable family** combines scalar divisibility and elliptic comparison conditions in two pole predicates. Nine elliptic point-coordinate pairs, the input, a slope, and two pole-parameter pairs give 24 rational coordinates; one separating coordinate eliminates the remaining finite algebraic choices. Its exact degree majorant is **20,747,108,969,426,225,455,955,968**, uniformly in the fixed odd coefficient exponent.

The comparison functions enter the local factors directly. Reciprocal-abscissa tests and the input comparisons need order one; the three Lucas-label comparisons and the Lucas residual need order three. The first four scalar tests need only positive valuation, while the two logarithm-ratio components retain order three. These scalar tests use

$$\Phi_z(D)=\frac{zD}{1+zD}.$$

This function can have a pole when $v(zD)=0$; the proof does not assume otherwise. For completeness, an additional congruence makes the common elliptic index divisible by every selected prime. The clustered-prime and reduction-order estimates make those congruences compatible. The resulting formal depth excludes the valuation-zero case in every scalar normalization at a selected comparison prime. Fixed-place preparation treats the remaining denominators.

At every comparison prime the conditions force divisibility of either the desired integer residual $N$ or the separately controlled scalar index $c$. Thus $M_j^3\mid\Delta c$ for the Lucas residual, and $M_j\mid(u-nv)c$ for the input residual, including primes shared by the scalar and comparison supports. Two disjoint contact blocks and the multiplicity height theorem give the strict exponents

$$\frac79<1,\qquad \frac{35}{18}<2.$$

These inequalities control the scalar and Lucas residual. For the input residual, keeping $c$ separate in $|(u-nv)c|\le2e^{h(\beta)}Bc$ uses the additional strict exponent $7/6<2$ and gives a logarithmic bound contradicted by Lucas growth. The full extraction and simultaneous realization proofs are in the [25-variable paper](papers/few_variables25/few_variables25_merged_20261110_v19.pdf).

### Quartics with reciprocal local weights

The [fixed-difference chart](papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf) uses three quadratic equations for the four field values

$$
\frac{y(H)}{x(H)},\quad\frac{y(H-P)}{x(H-P)},\quad
\frac1{x(H)},\quad\frac1{x(H-P)}.
$$

Every exceptional leading-coefficient case is included in its proof. Direct formal-parameter ratios then avoid separate numerator parameters.

A further saving comes from clearing each local factor by a reciprocal fourth power. For example,

$$
T=1+q^5C^2+q^2D^2+q^4B^4
$$

is imposed by

$$
s_4T=s_4+qC^2+s_2D^2+(B^2)^2,
\qquad qs_1=1,\quad s_2=s_1^2,\quad s_4=s_2^2.
$$

The squares are already stored, so the right side is quadratic in the retained coordinates. Five field fourth powers disappear from the inherited-premise quartics. The new contact-height bound permits comparison order three. The abc construction uses a related reciprocal system; its possible zero component is excluded algebraically by the fixed-difference point equations before any division is made.

The [226-variable family](papers/quartic_existence/quartic226_20261110_v21.pdf) uses ten reflected contacts and five factors for sixteen local tests. The fully specified 262-variable construction instead uses four factors, sharing four deep-comparison fourth powers across its three comparison scales. Their distinct valuation classes give the same local precision, and the net saving is one rational coordinate. The [87-variable abc family](papers/quartic_existence/quartic_abc87_20261110_v21.pdf) uses eight symmetric contacts and the scale $\beta^4+T^4$; its two abc height estimates give the strict absorption coefficient $8/9$.

The contact equations use the inverse weight already present in each detector. Write

$$P_5(r)=r^5-e_1r^4+e_2r^3-e_3r^2+e_4r-e_5.$$

With $qs_1=1$, the three outputs $r,u,v$ satisfy

$$u=r^2,\qquad v=ru-e_1(1+s_1)u+e_2(1+s_1)r,$$
$$uv=(1+s_1)(e_3u-e_4r+e_5).$$

These quadratic equations are equivalent to $(1+q)P_5(r)=r^5$ on the entire rational zero set, including $r=0$. No coordinate storing $P_5(r)$ is needed. The full independent reconstruction checks all changed rows, every retained row, and all quartic coefficients.

For the abc quartic, the squared contact distances are $1,4,9,36$. Pairing their products at $36$ gives

$$\frac{(r-1)(r-4)(r-9)(r-36)}{r^2}
 =\left(r+\frac{36}{r}\right)^2-50\left(r+\frac{36}{r}\right)+481.$$

This identity reduces each contact calculation to two quadratic outputs. The new contact set has its own complete arithmetic proof. Every zero-weight and zero-contact case is excluded algebraically before the inverse coordinates are interpreted.

### Fully specified parameters

Write the sum of four root abscissas as $S_0+\sqrt2S_1$, and let $B$ be the largest absolute elliptic index. The [effective abscissa-sum theorem](papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) gives

$$B^2\le2h(S_0)+2h(S_0+S_1)+82.$$

The explicit quartic uses the three scales $1,S_0^2,(S_0+S_1)^2$. The explicit 27-variable construction uses the scalar coefficient $\rho$ to form the scales

$$1,\qquad(1+\rho S_0^2)^2,\qquad(1+\rho(S_0+S_1)^2)^2.$$

The latter preserve the unit alternative needed by the combined scalar and comparison predicates. All constants in the resulting soundness arguments are effective. Retaining the quadratic logarithmic factor in the contact-height theorem gives linear radical bounds on each pair of contact blocks. This sharper estimate supplies the explicit coefficient thresholds. Exact integer inequalities certify **$L=20483$** for the [27-variable polynomial](papers/few_variables27/explicit27_20261110_v19.pdf), and **$N=9682$** for the [262-variable quartic](papers/quartic/quartic262_20261110_v21.pdf). The latter's largest coefficient has **279,599 binary digits**.

The 27-variable degree majorant is **85,829,362,869,408,651,982,929,920**. The finite-algebra constructions use [separation on the nonzero guard locus](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf), including disappearing branches and inactive nilpotents.

### Conditional constructions and product obstructions

The [13-variable families](papers/conditional_few_variables/direct_input13_20261110_v22.pdf) compare the elliptic index directly with the input $X$. A separate positive height scale satisfies

$$\beta=X^2+B\ge B,\qquad 2h(X)\le h(\beta).$$

With the second comparison scale $\beta^d+T(n)^d$, the sixth-power construction under weak abc with exponent $121/100$ has absorption coefficient $14641/17538<1$ and degree at most **11,774,654,098,433**. The fourth-power construction under exponent $16/15$ has coefficient $8/9<1$ and degree at most **11,212,784,195,585**. Ordinary rational abc supplies both hypotheses; ordinary Szpiro supplies the first, as established in the [arithmetic-hypotheses paper](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf).

Three elliptic point roles, two pole predicates, and finite-root elimination give thirteen total variables. Completeness permits every nonzero integer index, including negative and even indices. The final polynomial $F_B=XQ_B$ includes zero without another variable. Its sufficient shift remains ineffective. The [input-height paper](papers/contact_heights/input_height_amplification_20261110_v22.pdf) proves the general height argument and related five- and six-contact criteria. It also gives an unconditional four-contact example with odd radical one and unbounded argument height; those contacts cannot satisfy the proposed logarithmic estimate. No construction below thirteen total variables under abc is established here.

The [product-height obstruction paper](papers/pole_parameters/product_height_obstructions_20261110_v19.pdf) proves that, for these six contacts, **every prescribed rational scale $a>4$** admits a negative-slope cancellation with product odd radical one. This includes both current scales $\beta^6+T(n)^6$ and $\beta^4+T(n)^4$. Separate families give positive slopes that are sums of two rational squares, and slopes greater than one with product in $7\mathbb Q^{\times2}$. The paper determines all twelve rational contact automorphisms and proves the elliptic family's infinitude. These are counterexamples to specified product-height bounds; they do not assert solutions of the full defining source or failure of every combined pole predicate.

The [rational contact-parity theorem](papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.pdf) rules out a broader local simplification. For every fixed nonzero rational function $\Psi(X,\lambda)$, infinitely many good primes admit the exact scale $a=(2X^2+B)^8+T(n)^8$, a half-integral input, and a positive slope that is a sum of two integer squares, for which at least one contact has positive odd valuation but $\Psi$ has even valuation. The input residual is a unit at that prime. One may additionally require $\lambda=1+s^2$ with integer $s$, so $\lambda-1$ is an integer square. Explicit dependence on the input or scale does not avoid this obstruction. The theorem is unconditional for the stated rational parameters; it does not construct a false solution of the full source or give an absolute variable lower bound.

The [quadratic-cover theorem](papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf) treats algebraic parity conditions. For every rational $a>4$, the curve $z^2=dR(\lambda)R(a\lambda)$ has genus four. Hence only finitely many rational slopes at a fixed scale have equal odd contact sets outside a fixed finite set of primes. The negative-square condition gives the soundness implication needed by a proposed one-pole construction, but completeness remains unproved. The explicit negative-square section fails the elliptic comparison conditions for infinitely many odd input shifts; an exact inert-prime certificate proves that assertion. These are obstructions to specified simplifications, with no new defining variable count.

The [index-product theorem](papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.pdf) proves that, for a non-torsion point $P$, the set of triples $([n]P,[h]P,[nh]P)$ is Zariski dense in the cube of its elliptic curve whenever $n$ ranges through an infinite set and each $n$ has infinitely many allowed auxiliary indices $h$. Thus a fixed correspondence with finite geometric fibers cannot reconstruct the product point from the two retained points uniformly on these sets. The elliptic proof is elementary; a Mordell–Lang argument gives the corresponding theorem for a Zariski-dense cyclic subgroup of an abelian variety. This excludes one elimination strategy, without giving an absolute variable lower bound.

## Current papers

Every PDF has its complete LaTeX source beside it. The supporting papers are organized by mathematical subject.

| Subject | Main paper |
|:--|:--|
| Few variables under inherited premises | [25-variable family](papers/few_variables25/few_variables25_merged_20261110_v19.pdf) |
| Quartics under inherited premises | [226-variable family](papers/quartic_existence/quartic226_20261110_v21.pdf) |
| Fully specified coefficients | [27-variable polynomial](papers/few_variables27/explicit27_20261110_v19.pdf), [262-variable quartic](papers/quartic/quartic262_20261110_v21.pdf) |
| Additional height conjectures | [Two 13-variable families](papers/conditional_few_variables/direct_input13_20261110_v22.pdf), [87-variable quartic](papers/quartic_existence/quartic_abc87_20261110_v21.pdf) |
| Elliptic equations | [Three quadrics for two translated parameters](papers/elliptic_charts/fixed_difference_charts_20261110_v18.pdf), [index products and finite correspondences](papers/elliptic_charts/index_products_and_finite_correspondences_20261110_v21.pdf) |
| Contact heights | [Input heights and odd contact radicals](papers/contact_heights/input_height_amplification_20261110_v22.pdf), [modular multiplicity and quadratic bounds](papers/contact_heights/multiplicity_and_contact_heights_20261110_v19.pdf), [scalar characters](papers/contact_heights/nebentypus_and_contact_heights_20261110_v18.pdf), [differential evaluation](papers/contact_heights/evaluation_of_differentials_20261109_v17.pdf) |
| Effective heights | [Elliptic abscissa sums](papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) |
| Elimination | [Separation in finite algebras](papers/finite_algebra/active_finite_algebra_20261109_v15.pdf) |
| Arithmetic dependencies | [Inherited inputs](papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf), [prime selection](papers/prime_selection/prime_selection_20261109_v12.pdf), [additional conjectures](papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) |
| Lower bounds | [Degree and coordinate obstructions](papers/lower_bounds/lower_bounds_20261109_v15.pdf) |
| Number fields | [Definability reductions](papers/number_fields/number_field_definability_20261109_v12.pdf), [elliptic ratios](papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf), [finite correspondences](papers/number_fields/finite_correspondences_and_denominators_20261109_v14.pdf), [complex multiplication and trace cancellation](papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.pdf) |
| Limits of pole simplifications | [Fixed parameters](papers/pole_parameters/fixed_pole_parameters_20261109_v17.pdf), [combined certificates](papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf), [product-height obstructions](papers/pole_parameters/product_height_obstructions_20261110_v19.pdf), [rational contact parity](papers/pole_parameters/rational_combinations_of_contacts_20261110_v20.pdf), [quadratic contact covers](papers/pole_parameters/quadratic_contact_covers_20261110_v21.pdf), [quartic pole equation](papers/pole_parameters/quartic_pole_obstruction_20261109_v17.pdf) |
| Restricted abc estimates | [Applicability and obstructions](papers/restricted_abc/restricted_abc_inputs_20261109_v17.pdf) |

## Rings of integers in number fields

No counterexample and no general positive theorem for $\mathcal O_K$ in its fraction field $K$ is established here. The [number-field reductions](papers/number_fields/number_field_definability_20261109_v12.pdf) prove

$$
\mathcal O_K\text{ Diophantine in }K
\quad\Longleftrightarrow\quad
\mathbb Z\text{ Diophantine in }K.
$$

This uses the established definability of $\mathbb Z$ in $\mathcal O_K$. Assuming separately a definition of $\mathbb Z$ in $\mathbb Q$, these conditions are also equivalent to the rational subfield being Diophantine in $K$. A counterexample would persist in every finite extension and would therefore yield a totally imaginary Galois example.

The papers distinguish these general questions from failures of particular constructions. One unchanged formula cannot work in every finite extension. Rank stability alone gives infinite Diophantine subsets of the rational subfield, but not necessarily the whole subfield. Exact examples are locally dense while omitting a rational integer globally. The finite-correspondence results obstruct several methods based on bounded denominators and rational functions of abelian point coordinates; they do not exclude all Diophantine definitions.

The [complex multiplication and trace cancellation](papers/number_fields/complex_multiplication_and_trace_cancellation_20261110_v19.pdf) theorem gives an explicit obstruction over $L=\mathbb Q(\sqrt2,i)$. For the curve $E_D:y^2=x^3-Dx$, adjoining $i$ doubles its rank. If $C=(1+i)P$ for the displayed non-torsion point, then $\operatorname{Tr}_{L/\mathbb Q}x([n]C)=0$ for every nonzero $n$, while its height grows quadratically. Four distinct doubled points also have zero abscissa sum and unbounded heights. These statements are unconditional, with an exact non-torsion certificate; they obstruct this rank and height encoding over complex fields, not Diophantine definability of their rings of integers.

The [lower-bound paper](papers/lower_bounds/lower_bounds_20261109_v15.pdf) proves degree at least four for a single defining equation, at least three total coordinates for any finite system, and at least five for a quadratic system or a globally nonnegative quartic over $\mathbb Q$. [Research directions](docs/research_directions.md) describes the arithmetic changes still needed for substantially fewer variables.

## Reproduce the results

Python 3.10 or newer and its standard library suffice for the polynomial reconstructions and finite algebraic certificates:

~~~sh
python3 scripts/verify.py --full
~~~

The verifier works in a temporary copy. It checks source hashes, reconstructs required dependencies, independently expands the quartics, and checks finite-algebra specifications, degree and support bounds, local identities, and exceptional cases. Intermediate coefficient families are exact reconstruction dependencies. The source auditors explicitly distinguish exact symbolic checks from finite-field formula evaluations.

Optional exact elliptic ranks, descents, and function-field calculations use `cypari2`:

~~~sh
python3 scripts/verify.py --full --with-pari
~~~

The current release receipt is [standard-library verification](data/verification-standard-v22.json). The unchanged elliptic rank, descent, and function-field dependencies also have a [verification receipt including PARI](data/verification-v19.json). These computations use exact rank bounds and torsion calculations, not analytic rank or BSD. The exact contact-parity examples and the input-height and four-contact identities are checked by the full verifier. The [reproducibility guide](docs/reproducibility.md) gives individual commands and their scope. [Data formats](docs/data_format.md), [quartic provenance](computation/quartic/PROVENANCE.json), [results](data/results.json), and [MANIFEST.json](MANIFEST.json) identify the complete specifications and their hashes.

To rebuild the papers with a standard TeX installation:

~~~sh
python3 scripts/build_papers.py
~~~

## Sources and license

Primary references appear in the papers. They include [elliotglazer/diophantine-z-q](https://github.com/elliotglazer/diophantine-z-q), the pinned source manuscript, Sun's prime-pattern theorem, von Buhren's height theorem, Faltings' isogeny theorem, Rémond's height inequality, and the Gaudron–Rémond isogeny estimates. Computational provenance fixes source commits and exact input bytes.

Original contributions are licensed under [CC BY 4.0](LICENSE). Third-party material retains its existing notices; see [attribution](THIRD_PARTY.md). [CITATION.cff](CITATION.cff) supplies citation metadata. The collection includes computer-assisted mathematical writing and verification; each theorem states its assumptions and proof.
