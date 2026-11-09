# Arithmetic inputs, theorem scope, and effectiveness

The construction papers prove that the indicated rational input projections equal $\mathbb Z$ under their stated arithmetic inputs. Two constructions specify all coefficients: the [29-variable polynomial](../papers/few_variables/explicit29_nontorsion_20261109_v11.pdf) and the [351-variable quartic](../papers/quartic/quartic351_20261109_v11.pdf). Two further results prove the existence of sufficiently large members of computable coefficient families: the [27-variable family](../papers/few_variables27/few_variables27_nontorsion_20261109_v11.pdf) and the [301-variable quartic family](../papers/quartic_existence/quartic301_20261109_v11.pdf).

The [arithmetic-dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) derives the precise inputs used by the few-variable construction from the pinned source statements and Sun's Theorem 4.1. It checks simultaneous congruences, avoidance at every prescribed fixed odd prime, the special case of seven, preservation of real approximation conditions, and realization with zero preparation parameters. The [baseline quartic paper](../papers/quartic/quartic392_20261108_v8.pdf) supplies the full comparison and realization argument used by the quartic constructions.

## The four common arithmetic inputs

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

## Additional quantitative input for the quartics

Both the explicit 351-variable quartic and the 301-variable quartic family retain the quantitative prime-pattern premise of the baseline comparison construction. For fixed distinct coefficients $c_j$, the admissible patterns $p_j=u+c_jw^2$ in

$$
N/2\le u\le N,\qquad 1\le w\le\tau(N)\sqrt N
$$

have total weight at least $c_0N^{3/2}\tau(N)$, with individual weights $O((\log N)^k)$. The function $\tau(N)$ may decrease arbitrarily slowly after the fixed congruences and avoidance conditions have been imposed. The quartic papers state this premise and the separation step that uses it. The 29-variable and 27-variable theorems do not require this quantitative strengthening.

## The aggregate height theorem and its ineffective constant

The [aggregate trace-height paper](../papers/trace_heights/aggregate_trace_height_20261108_v9.pdf) proves, for the specified point $P$ and any fixed number of nonzero integer labels, a comparison of the form

$$
\sum_i\widehat h_E([n_i]P)
 \le M\,h\!\left(\operatorname{Tr}_{K/\mathbb Q}
                         \sum_i x([n_i]P)\right)+M_0.
$$

Its geometric argument excludes every positive-dimensional abelian translate through a source tuple from a constant trace fiber. The proof includes translates defined over the algebraic closure, establishes the required endomorphism independence of the conjugate points, and applies [Von Buhren, Theorem 1.1](https://www.numdam.org/item/10.5802/jtnb.981.pdf) to a fixed graph and finite-rank subgroup. This comparison is unconditional for the displayed points; it does not assume their full Mordell–Weil group has been computed.

The slope $M$ can be chosen effectively from the fixed geometry. The additive constant $M_0$ exists by the published theorem but is not determined effectively here. Consequently:

- In the 27-variable family $F_L$, every sufficiently large fixed odd $L$ defines $\mathbb Z$, under the four common arithmetic inputs. The uniform degree bound is $2^{154}$.
- In the quartic family $P_N$, every sufficiently large fixed $N$ gives the required projection, under the same inputs and the weighted prime-pattern premise. Every member has 301 total variables and exact degree four.
- No certified numerical sufficient parameter is supplied for either family. In particular, the packaged 27-variable example at $L=137731$ certifies algebraic specifications and bounds, not the assertion that this specific member defines $\mathbb Z$.
- The parameters are fixed coefficients. The ineffectivity adds no quantified coordinate and does not change the degree bounds.

This is a proved existence statement with an ineffective coefficient threshold, rather than a new unproved height hypothesis. The explicit 29-variable and 351-variable theorems retain their fully specified coefficients independently of these two families.

## Direct point charts and the input map

The [square-abscissa paper](../papers/square_abscissa/square_abscissa_charts_20261108_v9.pdf) gives a complete elementary descent proof that

$$
x=h^2,\qquad j^2=h^4-(3-\sqrt2)^2,\qquad y=hj
$$

describes exactly the nonzero integer multiples of $P$, assuming $2E(K)=\mathbb ZP$. This removes parity requirements from the point coordinates. The sum-trace height theorem works for arbitrary nonzero integer labels.

The [quadratic square-root paper](../papers/quadratic_squares/quadratic_square_chart_20261108_v9.pdf) then supplies a single finite quartic chart for $j$. Its completeness follows from an elementary noncube argument and holds, with suitable fixed coefficients, over every quadratic extension of every number field. It has no dependence on an auxiliary elliptic rank calculation or on the four arithmetic inputs.

The quartic family's input map is $\beta=51X^2+2504$. If $X=u/v$ in lowest terms and $\beta$ is integral, then $v^2\mid51$; squarefreeness of 51 forces $v=1$. The changed scalar correction $9792=2^6\cdot3^2\cdot17$ has its required local squareclasses checked in the quartic proof and exact certificate.

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

The three scales $1,S_0^2,(S_0+S_1)^2$ therefore suffice for the explicit 29-variable and 351-variable constructions. Their thresholds are numerical: $L=137731$ and $N=27464$, respectively. No new arithmetic premise is introduced. This effective estimate controls two rational linear forms; it does not make the sufficient thresholds of the separate 27-variable and 301-variable trace families effective.

The [square-predicate paper](../papers/square_predicates/quadratic_square_predicates_20261108_v10.pdf) proves its construction and lower bounds unconditionally for every quadratic extension of number fields. Its one auxiliary variable ranges over the base field, and its predicate concerns squares rather than algebraic integers.

## Scope of the nonzero pole-witness consequence

The leading 27- and 29-variable constructions use the restricted-converse and descent hypotheses underlying the retained simultaneous-realization argument. That construction supplies points outside two-torsion, hence nonzero ordinates. The resulting nonzero pole witnesses permit the single conic chart and removal of zero quadratic strata. Bare pole solvability alone would not imply this strengthening; the full argument and exact inherited scope are given in both replacement papers.

The 301- and 351-variable quartics retain the local orders and arithmetic hypotheses of their 317- and 370-coordinate source systems. Their new factor grouping is justified by the uniform valuation proof and simultaneous-completeness argument; it introduces no stronger prime-pattern hypothesis. The weighted quantitative selection premise remains explicit.
