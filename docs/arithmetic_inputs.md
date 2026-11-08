# Arithmetic inputs and theorem scope

The construction theorems identify the rational input projections of two explicit integer polynomials with $\mathbb Z$, under precisely stated arithmetic inputs. The [29-variable paper](../papers/few_variables/few_variables_20261108_v8.pdf) and the [392-variable quartic paper](../papers/quartic/quartic392_20261108_v8.pdf) give the full statements and proofs of these implications.

The [arithmetic-dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) proves that the four inputs used by the 29-variable construction follow from the pinned source statements and Sun's Theorem 4.1. It checks the required simultaneous congruences, avoidance at every prescribed fixed odd prime, the special case of seven, preservation of the real approximation conditions, and realization with zero preparation parameters.

## The four common inputs

| Input | Mathematical content used | Scope of the finite checks |
|:--|:--|:--|
| Elliptic group and index height | For the specified curve over $K=\mathbb Q(\sqrt2)$ and point $P$, the equality $2E(K)=\mathbb ZP$ and the lower bound $h(x([n]P))\ge n^2-6$ for $n\ne0$. | Exact point identities, finite-field counts and local constants are checked. The complete group assertion and the global lower bound are cited arithmetic results. |
| Contact height | The five-contact radical $M_5(t)$ satisfies $h(t)\le H_{19}M_5(t)^{19}$, with the specified explicit constant $H_{19}$. | Independent prime enumerations and integer computations give $H_{19}<2^{2093448}$. These computations evaluate the constant appearing in the cited inequality. |
| Pole obstruction and realization | The specified pole equations exclude negative odd valuations outside the exceptional primes and admit rational solutions under the stated positivity, squareclass and local-depth conditions. | Coordinate identities and their domains are checked. The obstruction and realization theorems are stated separately; the dependency paper verifies the exact zero-preparation statement being used. |
| Simultaneous prime patterns | Prescribed prime values, Gaussian congruences, fixed avoidance, conjugate reduction orders and compatible real approximation can be achieved together. | The dependency paper derives the required quantified form from Sun's Theorem 4.1 and the source reduction-order lemma. Finite checks verify the congruence and order calculations. |

Here

$$
H_{19}=2^{110}210^{1800}\left(\prod_{p\le76176}p\right)^{19}+128.
$$

The extra fixed prime used in each scalar normalization belongs to a finite set chosen before the prime-pattern theorem is applied. Its inclusion is covered by the stated fixed-avoidance condition.

## Quantitative input for the quartic

The 392-variable quartic also uses the quantitative form of the prime-pattern input retained by its comparison construction. For fixed distinct coefficients $c_j$, the admissible patterns $p_j=u+c_jw^2$ in

$$
N/2\le u\le N,\qquad 1\le w\le\tau(N)\sqrt N
$$

have total weight at least $c_0N^{3/2}\tau(N)$, with individual weights $O((\log N)^k)$. The function $\tau(N)$ may decrease arbitrarily slowly after the fixed congruences and avoidance conditions have been imposed. The quartic paper states this premise and explains the separation step that uses it. The 29-variable theorem does not require this quantitative strengthening.

## Results proved within this project

The papers prove the odd-product height identity, the rational point charts, the input normalizations, the elementary Lucas growth estimate, the forced-prime index bounds and their simultaneous realization, and the guarded finite-algebra elimination theorem. The weighted companion-norm argument proves the coefficient bound for the same 29-variable polynomial without altering its expression. Every use of a cited arithmetic input is identified in the construction proofs.

The degree and coordinate lower bounds, equation-combination theorem, number-field transfer statements, elliptic-chart obstruction, quadratic upper height estimate and uniform logarithm truncation estimates have the hypotheses stated in their own papers. They do not depend on the four global construction inputs above.

## Exact sources

The 29-variable coefficient construction uses the Version 9 source at commit `14e8f601fe0d9173d4a5f084aedc3e07066a7688`. Its arithmetic interpretation incorporates the Version 11 Kato index-set and retained-class correction at commit `650b298a2a18fa956f8859f3ca80e9d7c8cedd82`. The prime-pattern reference is Sun, arXiv:2610.20691v2, Theorem 4.1. The [dependency paper](../papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.pdf) provides the exact statement identifiers and bibliographic references.

The quartic source is Version 13 at commit `5bbd74f6a479776a332cbe036809d5dddae63720`. Its source paths, normalization conventions and hashes are recorded in [the quartic provenance file](../computation/quartic/PROVENANCE.json).

The coefficient data, degree counts, algebraic identities and finite numerical certificates are unconditional assertions about the supplied expressions. The conclusion that their rational projections equal $\mathbb Z$ has the arithmetic hypotheses stated above. A passing computational receipt certifies its listed finite assertions; it does not independently prove those global hypotheses.
