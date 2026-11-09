# Arithmetic inputs, theorem scope, and effectiveness

The construction papers prove that the indicated rational input projections equal $\mathbb Z$ under their stated arithmetic inputs. The [29-variable polynomial](../papers/few_variables/explicit29_nontorsion_20261109_v15.pdf) and the [322-variable quartic](../papers/quartic/quartic322_20261109_v13.pdf) have certified fixed coefficient parameters under the inherited premises. The [27-variable family](../papers/few_variables27/few_variables27_nontorsion_20261109_v15.pdf) and the [263-variable quartic family](../papers/quartic_existence/quartic263_20261109_v16.pdf) prove the existence of sufficiently large members of computable coefficient families. With additional height hypotheses, the [13-variable family](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) needs only weak abc with exponent $121/100$, and the [98-variable quartic](../papers/quartic_existence/quartic_abc98_20261109_v16.pdf) uses ordinary rational abc. Ordinary Szpiro suffices for the thirteen-variable theorem. All four existence families have ineffective sufficient thresholds.

The [arithmetic-dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) derives the precise inputs used by the few-variable construction from the pinned source statements and Sun's Theorem 4.1. It checks simultaneous congruences, avoidance at every prescribed fixed odd prime, the special case of seven, preservation of real approximation conditions, and realization with zero preparation parameters. The [baseline quartic paper](../papers/quartic/quartic392_20261108_v8.pdf) supplies the full comparison and realization argument used by the quartic constructions.

## The four inherited arithmetic inputs

| Input | Mathematical content used | Scope of the finite checks |
|:--|:--|:--|
| Elliptic group and index height | For the specified curve over $K=\mathbb Q(\sqrt2)$ and point $P$, the equality $2E(K)=\mathbb ZP$ and the lower bound $h(x([n]P))\ge n^2-6$ for $n\ne0$. | Exact point identities, finite-field counts, and local constants are checked. The full group statement and the stated global lower bound are inherited arithmetic inputs. |
| Contact height | The five-contact radical $M_5(t)$ satisfies $h(t)\le H_{19}M_5(t)^{19}$, with the specified constant $H_{19}$. | Independent prime enumeration and integer computations give $H_{19}<2^{2093448}$. They evaluate the constant in the cited inequality. |
| Pole obstruction and realization | The specified pole equations exclude negative odd valuations outside the exceptional primes and admit rational solutions under the stated positivity, squareclass, and local-depth conditions. | Coordinate identities and their domains are checked. The dependency paper establishes the exact zero-preparation implication from the source realization theorem. |
| Simultaneous prime patterns | Prescribed prime values, Gaussian congruences, fixed avoidance, conjugate reduction orders, and compatible real approximation can be achieved together. | The dependency paper derives the required quantified form from Sun's Theorem 4.1 and the source reduction-order lemma. Finite checks verify congruence and order calculations. |

Here

$$
H_{19}=2^{110}210^{1800}\left(\prod_{p\le76176}p\right)^{19}+128.
$$

The fixed prime in each scalar normalization belongs to a finite set chosen before the prime-pattern theorem is applied. It is therefore covered by the established fixed-avoidance condition. Increasing a fixed coefficient changes finite divisibility requirements, which are likewise set before the later prime choices.

The 13- and 98-variable additional-conjecture constructions retain the specified elliptic group, pole obstruction and nonzero realization, and simultaneous prime-pattern inputs. They replace the exponent-nineteen contact-height premise by the logarithmic bounds proved from their additional weak-abc or ordinary-abc assumptions. The one-point trace-height theorem used with those bounds is proved, not an additional conjecture.

## Quantitative prime selection for the quartics

The [prime-selection paper](../papers/prime_selection/prime_selection_20261109_v12.pdf) derives the quantitative separation needed by the quartics from [Sun, arXiv:2610.20691v2](https://arxiv.org/abs/2610.20691v2), Propositions 5.1 and 6.2 and Section 6.1. It records the order of choices and the separation argument already used in the upstream construction. This is a consequence of those cited estimates, not an additional independent conjecture.

For fixed distinct coefficients $c_j$, the admissible patterns $p_j=u+c_jw^2$ lie in

$$
X/2\le u\le X,\qquad 1\le w\le\tau(X)\sqrt X.
$$

First fix the prime cutoff and the finite congruence and avoidance conditions. The cited estimates leave a positive proportion of total weight of size $X^{3/2}\tau(X)$ after the reduction-order obstructions are removed. Each individual weight is $O((\log X)^k)$. For any fixed $1/4<\alpha<1/2$, the strip $w<X^\alpha$ has weight $O(X^{1+\alpha}(\log X)^k)$, which is negligible after the permitted slow diagonal choice of $\tau$. The surviving patterns have pairwise gaps much larger than $\sqrt X$, which separates their prime values from the Hasse-sized reduction-order errors. The paper also proves the square-denominator preparation used in simultaneous completeness.

The projection theorems still depend on the cited prime-pattern and arithmetic results. Finite coefficient checks do not independently prove them. The few-variable theorems do not need the quantitative separation step.

## The aggregate height theorem and its ineffective constant

The [aggregate trace-height paper](../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) proves, for the specified point $P$ and any fixed number of nonzero integer labels, a comparison of the form

$$
\sum_i\widehat h_E([n_i]P)
 \le M\,h\!\left(\operatorname{Tr}_{K/\mathbb Q}
                         \sum_i x([n_i]P)\right)+M_0.
$$

Its geometric argument excludes every positive-dimensional abelian translate through a source tuple from a constant trace fiber. The proof includes translates defined over the algebraic closure, establishes the required endomorphism independence of the conjugate points, and applies [Von Buhren, Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf) to a fixed graph and finite-rank subgroup. This comparison is unconditional for the displayed points; it does not assume their full Mordell–Weil group has been computed.

The slope $M$ can be chosen effectively from the fixed geometry. The additive constant $M_0$ exists by the published theorem but is not determined effectively here. Consequently:

- In the 27-variable family $F_L$, every sufficiently large fixed odd $L$ defines $\mathbb Z$, under the four common arithmetic inputs. The uniform degree bound is $2^{87}$.
- In the quartic family $P_N$, every sufficiently large fixed $N$ gives the required projection, under the same inputs and the stated consequence of the prime-pattern estimates. Every member has 263 total variables and exact degree four.
- In the separate 13- and 98-variable families, the one-point trace theorem bounds the elliptic index after their additional height hypotheses bound the input and trace together. Every sufficiently large fixed odd shift $B$ then gives the required projection.
- No certified numerical sufficient parameter is supplied for these families. In particular, the packaged 27-variable example at $L=137731$ and the additional-conjecture examples at $B=3$ certify algebraic specifications and bounds, not the assertion that those specific members define $\mathbb Z$.
- The parameters are fixed coefficients. The ineffectivity adds no quantified coordinate and does not change the degree bounds.

The aggregate trace comparison is a proved existence statement with an ineffective additive constant. The additional-conjecture constructions separately state their weak-abc or ordinary-abc hypotheses. The explicit 29-variable and 322-variable theorems retain their fully specified defining coefficients independently of the ineffective families.

## Direct point charts and the input map

The [square-abscissa paper](../papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) gives a complete elementary descent proof that

$$
x=h^2,\qquad j^2=h^4-(3-\sqrt2)^2,\qquad y=hj
$$

describes exactly the nonzero integer multiples of $P$, assuming $2E(K)=\mathbb ZP$. This removes parity requirements from the point coordinates. The sum-trace height theorem works for arbitrary nonzero integer labels.

The [quadratic square-root paper](../papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) then supplies a single finite quartic chart for $j$. Its completeness follows from an elementary noncube argument and holds, with suitable fixed coefficients, over every quadratic extension of every number field. It has no dependence on an auxiliary elliptic rank calculation or on the four arithmetic inputs.

The 263- and 322-variable quartics use the input map $\beta=51X^2+2504$. If $X=u/v$ in lowest terms and $\beta$ is integral, then $v^2\mid51$; squarefreeness of 51 forces $v=1$. The scalar correction $9792=2^6\cdot3^2\cdot17$ has its required local squareclasses checked in the quartic proof and exact certificate. The 13- and 98-variable constructions use $\beta=2X^2+B$ for a fixed odd $B\ge3$. The same denominator argument gives $v^2\mid2$, again forcing $v=1$; the lower real bound $\beta\ge B$ supplies the final uniform-shift contradiction.

## Other results proved within this project

The papers prove the odd-product height identity, rational point-chart identities, input normalizations, elementary Lucas growth estimate, forced-prime index bounds, their simultaneous realization under the stated prime-pattern input, and guarded finite-algebra elimination. Weighted companion norms prove the coefficient bound for the specified 29-variable polynomial. Every use of an inherited arithmetic input is identified in the construction proofs.

The degree and coordinate lower bounds, equation-combination theorem, finite-algebra theorem, field-extension obstruction, elliptic presentation obstruction, quadratic upper-height estimate, uniform logarithm truncation estimates, and quadratic square-root chart do not depend on the four global construction inputs. Each has the scope stated in its own paper. The number-field trace-height corollary requires the explicit independence hypotheses given there and does not itself define any ring of integers.

## Exact source provenance

The explicit 29-variable coefficient construction uses the Version 9 source at commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`. Its arithmetic interpretation incorporates the Version 11 Kato index-set and retained-class correction at commit `650b298a2a18fa956f8859f3ca80e9d7c8cedd82`. The prime-pattern reference is Sun, arXiv:2610.20691v2, Theorem 4.1. The dependency paper provides exact statement identifiers and bibliography.

The baseline quartic source is Version 13 at commit `5bbd74f6a479776a332cbe036809d5dddae63720`. Source paths, normalization conventions, and hashes appear in [the quartic provenance file](../computation/quartic/PROVENANCE.json). Each additional construction records its own exact source, specification, and verification hashes.

The coefficient data, degree counts, algebraic identities, and finite numerical certificates are unconditional assertions about the supplied expressions. Their rational projections equal $\mathbb Z$ under the construction theorems' explicit arithmetic hypotheses. A passing computational receipt certifies its listed finite assertions; it does not replace those hypotheses or determine an ineffective threshold.

## Effective heights in the specified constructions

The [effective sum-height paper](../papers/effective_sums/effective_elliptic_sums_20261108_v10.pdf) proves, for the four positive abscissas,

$$
h(S)\ge\max_i h(x([n_i]P))-24\log B-\log864,
\qquad B=\max_i|n_i|.
$$

This theorem is unconditional and has explicit constants. Applying the retained index-height input and writing $S=S_0+S_1\sqrt2$ gives

$$
B^2\le2h(S_0)+2h(S_0+S_1)+82.
$$

The three scales $1,S_0^2,(S_0+S_1)^2$ therefore suffice for the explicit 29-variable and 322-variable constructions. Their thresholds are numerical: $L=137731$ and $N=27464$, respectively. No new arithmetic premise is introduced. This effective estimate controls two rational linear forms; it does not make the sufficient thresholds of the separate 27- and 263-variable trace families, or the 13- and 98-variable additional-conjecture families, effective.

The [square-predicate paper](../papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) proves its construction and lower bounds unconditionally for every quadratic extension of number fields. Its one auxiliary variable ranges over the base field, and its predicate concerns squares rather than algebraic integers.

## Scope of the nonzero pole-witness consequence

The leading few-variable constructions use the restricted-converse and descent hypotheses underlying the retained simultaneous-realization argument. That construction supplies points outside two-torsion, hence nonzero ordinates. The resulting nonzero pole witnesses permit the single conic chart and removal of zero quadratic strata. The additional-abc quartic uses the same nonzero realization to recover its normalized pole coordinates. Bare pole solvability alone would not imply this strengthening; the full argument and exact inherited scope are given in the construction papers and the [nonzero-witness paper](../papers/pole_parameters/pole_witness_density_20261109_v14.pdf).

The 322-variable quartic retains the comparison orders and effective global threshold of its source. Even reciprocal-abscissa valuations permit lower powers in its local factors and reference depth ten. The proof obtains integrality before improving formal depth.

The 263-variable quartic uses four disjoint affine copies of the five-contact set, arranged symmetrically about one. The [contact-height theorem](../papers/contact_heights/contact_height_amplification_20261109_v13.pdf) derives exponent $19/4$ from the stated exponent-19 input. The symmetric configuration adds the exceptional primes $247957$, $368323$ and $2029147$, fixed before prime selection. Comparison orders twelve and three and reference depth three suffice. A degree-ten polynomial in $(a\lambda-1)^2$ and the equations $Fq=r^9$, $k=qr^2$, $kb=\tau^2$ give the complete normalization. The system has 237 quadratic equations and its quartic has exactly 3,312 monomials. This construction has a new ineffective threshold; the numerical threshold for the 322-variable family does not transfer to it. No stronger prime-pattern hypothesis is introduced.

The [fixed-parameter paper](../papers/pole_parameters/fixed_pole_parameters_20261109_v16.pdf) proves that no constant actual pole parameter works for every prepared input. It also gives exact rank and descent counterexamples for the conic-chart values $\tau=\pm1,\pm17$. The [paper on combining pole certificates](../papers/pole_parameters/combining_pole_certificates_20261109_v16.pdf) excludes a common actual pole parameter for one prepared pair and proves a reflection obstruction to a simple product of symmetric detectors. These statements concern the specified proposed simplifications. They neither lower-bound the size of every possible pole certificate nor exclude a different argument on a narrower family of generated inputs.


## Number-field reductions

The number-field paper uses the published result of Alpöge–Bhargava–Ho–Shnidman, Corollary 1.2: $\mathbb Z$ is Diophantine in the ring of integers of every number field. It does not replace integral witnesses in that theorem by unrestricted field witnesses. Equivalence with defining the rational subfield additionally assumes a definition of $\mathbb Z$ in $\mathbb Q$; the other elementary reduction and descent statements do not require that assumption. Norms and traces with base-field coordinates are distinguished from their graphs on one unrestricted extension-field input.

The abscissa-valuation example and the restricted quadratic-input obstruction are unconditional elementary theorems. They rule out the explicitly stated constructions only and do not supply a counterexample to existential definability of an entire ring of integers in its field of fractions.


## New preparation and number-field certificates

The uniform scalar-normalization theorem has fixed exceptional primes independent of its large odd parameter. It uses the smaller resultant in $X^2$ and the multiplier $102^6J^2$. Its bounded elliptic parameter removes a real-approximation requirement. It does not replace the divisibility of indices by elliptic reduction orders, and it does not change the current few-variable counts.

The elliptic-ratio paper proves its four-coordinate proper-subset theorem over eight quadratic fields using unconditional upper and lower Mordell--Weil rank bounds and exact torsion calculations. The optional PARI verification repeats those computations; it invokes neither analytic rank nor BSD. The polynomial has witnesses for every local input while excluding $-1$ globally. These statements concern this specific subset, not the existence of other definitions of the rational subfield or the full ring of integers.


## The thirteen-variable theorem from weak abc

The [thirteen-variable family](../papers/conditional_few_variables/conditional13_20261109_v16.pdf) assumes only one weak rational abc inequality with exponent $\kappa=121/100$, together with the specified elliptic group, pole obstruction and nonzero realization, and simultaneous prime patterns. Applying this inequality to

$$
\varphi(z)=\frac{z(z+2)^3}{(2z+1)^3},\qquad
\varphi(z)-1=\frac{(z-1)^3(z+1)}{(2z+1)^3}
$$

and changing coordinates by $z=2+1/t$ gives six finite rational contacts and

$$
h(t)\le\frac{121}{74}\log M(t)+C_0.
$$

The primitive common-denominator calculation gives the projective estimate

$$
h(1:u:v)\le\frac{121}{437}h(u^8+v^8)+C_1.
$$

The scales are $1$ and $\beta^8+T^8$, where $T$ is the trace of the abscissa of one elliptic multiple. No square condition on the latter scale is needed: its sixth-power prefactor in the contact product is a square. All six local tests have order one. If $\beta\ne n$, their odd contact radicals divide the positive numerator $N$ of $\beta-n$, and

$$
h(1:\beta:T)\le\frac{14641}{16169}\log N+C.
$$

This coefficient is less than one. Since $\log N\le h(\beta)+\log(1+|n|)$, the inequality and the one-point trace-height theorem bound $n$ and the input height independently of $B$. Every sufficiently large fixed odd shift excludes this case. There are three point pairs, two independent pole pairs, one slope and the input; finite-root elimination adds one coordinate, giving thirteen in total.

The exact source and bound certificates in [the weak-abc module](../computation/few_variables/weak_abc13/README.md) give uniform degree at most 12,339,485,119,488, strictly below $2^{44}$. Its 64-factor polynomial specification has not been expanded. The shift-three coefficient-height check does not determine a sufficient defining shift.

More generally, every one weak exponent $1<\kappa<4/3$ suffices after choosing an even $d$ with $(8/\kappa-6)(d/\kappa-3)>2$ and using $\beta^d+T^d$. The same thirteen-coordinate count holds. The supplied numerical degree certificate concerns only $\kappa=121/100,d=8$.

## The additional-abc quartic

The [98-variable family](../papers/quartic_existence/quartic_abc98_20261109_v16.pdf) uses the six integer contacts $\{-2,-1,0,2,3,4\}$. Ordinary abc, through Granville's squarefree binary-form bound, gives $h(t)\le(2/3)\log M(t)+C_0$. A separate consequence gives $h(1:u:v)\le(2/5)h(u^6+v^6)+C_1$. The two scales $1$ and $\beta^6+T^6$ therefore yield strict absorption coefficient $8/15$.

Its complete quadratic point chart includes identity numerator points. The shortened subtraction formula is interpreted only after a height argument excludes $E[2]$, $P+E[2]$ and $-P+E[2]$ for the shared point. This makes all removed denominators legitimate. The packed local tests bootstrap integrality before using formal-logarithm errors as congruences. The prime-pattern preparation allows arbitrary positive rational scales because the sixth-power scale prefactor is a square.

The source has 98 total coordinates and 86 primitive quadratic equations. Their sum of squares has exact degree four, content one, and 882 monomials for every positive integer shift. For integer $B\ge3$, its height is exactly $\max(11600064,2B^4+169997)$. No numerical sufficient odd shift is certified. The full coefficient tables and independent reconstruction checks are in [the exact source directory](../computation/quartic/family_abc98).

## Other conjectures and finite verification

The [arithmetic-hypotheses paper](../papers/arithmetic_hypotheses/arithmetic_hypotheses_20261109_v16.pdf) verifies that the ordinary discriminant--conductor form of Szpiro implies weak abc with every exponent $6/5+\epsilon$; choosing $\epsilon=1/100$ gives the thirteen-variable theorem. The modified Szpiro statement and the stated truncated Vojta conjecture supply ordinary abc. None of these implications removes the inherited elliptic or pole-realization premises.

No coordinate reduction is derived from RH, GRH or Grimm's conjecture. The paper gives a Pell family with distinct prime assignments and constant odd squarefree part, and explains why a polynomial injection supplied by Bombieri–Lang does not itself remove inverse witnesses. Mazur's connected-component conjecture would forbid an existential integer projection, so it cannot consistently be added to premises already yielding one.

The 27-, 29- and 13-variable determinant specifications have certified monomial upper bounds $<2^{2202}$, $<2^{2417}$ and $<2^{509}$ respectively. These are support bounds in all polynomial coordinates, including the input, after fixed coefficients are substituted; their exact monomial counts are undetermined. In contrast, the 263-, 322- and 98-variable quartics are fully expanded, with exact counts 3,312, 4,992 and 882. The [support certificate](../computation/few_variables/monomial-bound-certificate.json) and the quartic tables establish finite algebraic assertions. They do not prove an arithmetic conjecture or determine an ineffective defining threshold.
