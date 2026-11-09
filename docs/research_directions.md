# Research priorities and proved constraints

The targets are **fewer than ten total coordinates**, and **fewer than one hundred for a quartic**. Every count includes the input. Neither target has been achieved. The leading conditional constructions have 27 coordinates, or 279 at degree four; the fully specified alternatives have 29 and 322. The priority remains coordinates, degree, and then coefficient height. The [main table](../README.md#main-results) records their arithmetic scope.

## Fewer than ten coordinates

The finite-algebra theorem already replaces all finite algebraic choices by one rational coordinate. Improving its degree estimates does not remove a retained parameter. The [structural paper](../papers/elliptic_charts/structural_constraints_20261109_v13.pdf) proves that a finite algebraic presentation recovering arbitrary tuples of $r$ independent points on the specified Weil restriction needs at least $2r$ retained rational coordinates. This applies to that presentation problem; it is not a lower bound for all integer-defining polynomials.

### 1. A complete pole certificate with one retained parameter

For a prepared pole input $b$, put $B=17b$ and $V=B(B-b^2)$. The specialization $e=-1/3$ leaves

$$
Bq^2=(s^2+V/3)(s^2-V).
$$

Here only $s$ would remain a free rational parameter; $q$ would be a finite algebraic choice. This could reduce each comparison or scalar pole presentation.

The next required lemma is affine rational solubility with $q\ne0$ for every $b$ satisfying exactly the existing preparation conditions. The inherited simultaneous-realization theorem chooses a fresh twist and does not establish this fixed specialization. Exact local tests and descent in explicit prepared families can either reject it or identify an appropriate rational-point theorem. The preparation hypotheses must be verified before using such a family.

Sharing a nondegenerate pole parameter instead forces equal squareclasses of the inputs. Sharing the conic-chart parameter avoids that particular restriction but creates a different simultaneous rational-point problem. Neither has a completeness proof. Pole savings alone cannot attain the target while all nine elliptic point roles remain.

### 2. Replace the separate input point by a scalar certificate

Identifying the input label with the scalar label could remove two point roles. The [uniform scalar normalization](../papers/scalar_normalization/uniform_scalar_normalization_20261109_v13.pdf) supplies the needed real boundedness: the point carrying the large index need not approach a prescribed real neighborhood.

The next required lemma is local completeness for a prescribed index. Divisibility of $a-1$ by powers of a contact prime does not make $[a-1]P$ formal there; the elliptic reduction order must also divide $a-1$. Enlarging the power of the contact product does not supply those additional factors. A replacement certificate must enforce the required arithmetic implication without restoring as many free parameters as it removes. The integer index cannot simply be recovered by a finite algebraic extension of point coordinates: the graph $(n,[n]P)$ is Zariski dense in the product of the affine line with the abelian variety.

### 3. A different integer-label construction

A rank-one curve over $\mathbb Q$ would cost fewer rational coordinates per point, but the present paired-place argument does not transfer. Requiring $H$ and $H-P$ to be formal at the same good prime forces the fixed $P$ to reduce to the identity. Using two rational curves with an algebraic curve of common-index pairs forces an isogeny relation and prevents arbitrarily large coprime reduction orders.

A concrete alternative is a Diophantine divisibility relation on indices of a fixed rank-one curve, with few unrestricted rational parameters. The next lemma would characterize $n\mid m$ through a small field-witness system for $[n]P$ and $[m]P$. It must prove the equivalence between denominator conditions and index divisibility, including small indices, torsion, and bad primes. An integer-label definition based on this relation would still need a proved connection to the ordinary rational input.

There is a further restriction on that connection. Corvaja–Zannier, [Theorem 1.1](https://arxiv.org/html/2608.28255v1), implies that finite unions of fixed rational-function images of finitely generated subgroups of semiabelian varieties miss infinitely many rational integers. By Mordell–Weil this applies to all rational points on fixed abelian varieties and their finite products. Consequently a fixed collection of sums, products, or ratios of elliptic coordinates cannot cover every integer. General algebraic correspondences and unrestricted affine parameters are outside this assertion.

## Fewer than one hundred coordinates at degree four

The current 279-coordinate system has the following disjoint budget. The [exact certificate](../computation/quartic/coordinate-budget279.json) lists every coordinate, and its [checker](../computation/quartic/check_coordinate_budget.py) reconstructs the partition from the quadratic table.

| Block | Coordinates |
|:--|--:|
| Input, input square, common slope | 3 |
| Four root point charts | 24 |
| Auxiliary and difference point charts, including eight alternate parameters | 58 |
| Formal logarithm data | 20 |
| Comparison ratios and Lucas residual | 22 |
| Squared tests and shared higher powers | 30 |
| Aggregate trace square | 1 |
| Comparison contacts, scales, numerators, and denominator clearing | 26 |
| Comparison weight powers | 14 |
| Comparison trace values and pole inputs | 8 |
| Comparison pole witnesses | 14 |
| Local factor values and intermediate products | 32 |
| Scalar height and fixed-prime block | 27 |
| **Total** | **279** |

The elliptic charts use 82 coordinates and the two comparison detectors use 94. Even discarding the complete detector block leaves 185. More narrowly, the four root charts, auxiliary charts after deleting all eight alternate parameters, scalar block, and input already use $24+50+27+1=102$. Thus retaining those literal blocks prevents the target. This is an accounting statement about the present circuit, not a universal lower bound.

The [contact-height theorem](../papers/contact_heights/contact_height_amplification_20261109_v13.pdf) provides exponent $19/r$ from $5r$ disjoint contacts. Ordinary comparison order $k$ suffices when $rk>38$, and input order $\mu$ when $2r\mu>19$. The 279-variable polynomial implements $r=4$. Increasing $r$ permits shorter logarithms, but the degree-$5r$ contact product costs more operations. In the present circuit, ten of the twenty logarithm coordinates are still reciprocal-abscissa squares used in local factors; two describe the shared denominator logarithm. Constant approximants alone therefore remove at most eight, before replacement powers are counted.

The highest priorities are:

1. **Reduce the repeated point charts.** A smaller quadratic presentation of paired points $U,V$ with $U-V=Q$ must preserve their index domains and required formal parameters, including $U=O$, $V=O$, torsion, and all denominator-zero branches.
2. **Replace the growth relation together with its points.** The Lucas mechanism uses two root charts and two auxiliary pairs. A cheaper relation must still supply exponential growth of the relevant integer labels and complete realization. A single fixed plane polynomial relation cannot do so for unbounded input: the ordinary root bound limits the other coordinate to polynomial growth outside finitely many input values.
3. **Compress the pole and scalar systems.** A quadratic pole predicate with fewer than seven rational coordinates would save witnesses in three places. The scalar replacement must preserve both the sublinear input-height bound and the forced lower bound for the large index.
4. **Optimize local factors jointly with their power circuits.** Even valuations allow additional combinations beyond the current four or five factors. These can yield incremental improvements, but the retained 102-coordinate block shows why factor optimization alone cannot meet the target.

The coefficient height is controlled exactly by $A_N^2+1$. Reducing the effective exponent or changing the fixed prime remains a secondary task and requires repeating the global height and local squareclass arguments. An effective one-scalar height estimate could make a smaller existing construction explicit; it does not by itself reduce the coordinate count.

## Rings of integers in their fraction fields

No number-field counterexample and no general positive fraction-field theorem is established. Failure of one formula, or even of a fixed finite list, does not exclude a formula chosen separately for each field. A genuine counterexample would persist under finite extension and yield a totally imaginary Galois counterexample, by the descent theorem in the [number-field paper](../papers/number_fields/number_field_definability_20261109_v12.pdf).

The most direct sufficient target is a Diophantine set $S\subset K$ such that

$$
\mathbb Z\subseteq S,\qquad MS\subseteq\mathcal O_K
$$

for a fixed positive integer $M$. Then $T=\bigcup_{j=0}^{M-1}(j+MS)$ satisfies $\mathbb Z\subseteq T\subseteq\mathcal O_K$, and an integral basis gives $\mathcal O_K=\sum_i\omega_iT$. The [elliptic-ratio paper](../papers/number_fields/elliptic_ratios_and_integrality_20261109_v13.pdf) proves the statement with coordinate and degree bounds.

Rank-stable elliptic curves yield Diophantine subsets of the rational subfield, but their fixed rational images cannot supply this $S$, by Corvaja–Zannier. The four-coordinate example in the same paper is simultaneously dense in every finite product of completions and locally soluble for every input, while excluding $-1$ globally. Thus neither infinitude nor complete local evidence establishes integer containment.

The next tasks are to construct an input-dependent algebraic correspondence with proved integer coverage and a uniform denominator bound; to investigate rational-subfield, trace-graph, or relative norm-image definitions with genuine base-field restrictions; and to seek a formula-independent obstruction in a specific number field. The established definability of $\mathbb Z$ in $\mathcal O_K$ uses integral witnesses. It does not supply unrestricted field witnesses for any of these tasks.
