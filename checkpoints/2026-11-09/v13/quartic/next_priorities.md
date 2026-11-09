# Toward a quartic with fewer than100 total variables

## Exact present budget

The current existence construction has279 total variables, including its input. The disjoint count below is reproduced directly from `family279/quadratic-family279.json` by `check_coordinate_budget.py`; `coordinate-budget279.json` lists every coordinate in its category. The explicit construction remains322 variables.

| Block | Variables |
|---|---:|
| Input X, input square, common slope λ |3|
| Four integer-label root point charts |24|
| Auxiliary and difference point charts, including eight z-values |58|
| Formal logarithm data |20|
| Eight field comparison ratios and Lucas residual |22|
| Squared tests and shared higher powers |30|
| Aggregate trace square scale |1|
| Comparison contact polynomials, scales, numerator and δ clearing |26|
| Comparison weight power gates |14|
| Comparison trace values and pole inputs |8|
| Comparison pole witnesses |14|
| Local factor values and intermediate products |32|
| Scalar height and fixed-prime block |27|
| **Total** |**279**|

Thus the elliptic charts consume82 variables and the two comparison detectors consume94. Reaching99 requires removing180 variables. Deleting the entire94-variable detector block would still leave185.

There is a precise accounting obstruction to relying only on contact amplification: the four root charts(24), auxiliary charts after even discarding all eight alternate z-values(50), unchanged scalar block(27), and input(1) already total102. This is a statement about retaining these literal disjoint blocks, **not** a lower bound for arbitrary quartics or alternative encodings. At least one of these blocks must change, and substantially more must change if any current comparison machinery remains.

## What arbitrarily many contact blocks can do

The proved amplification gives exponent19/r; ordinary comparison order k is sufficient when rk>38, and input order μ when2rμ>19. With enough blocks, constant logarithm approximations suffice. But in the present circuit10 of the20 logarithm coordinates are reciprocal-abscissa squares needed by local factors, and two are the shared denominator logarithm. Merely setting the approximants to1 therefore removes at most the remaining eight coordinates, before any replacement powers are counted. Collapsing all orders to1 can remove at most eight of the current14 weight gates while retaining q²,q⁴,q⁸ for both detectors. These are literal-circuit counts, not universal optimality claims.

Meanwhile the contact polynomial has degree5r. Any triangular polynomial circuit with quadratic assignment rows, starting from the single parameter t and constants, needs at least ceil(log₂(5r)) computed coordinates to reach that degree: every assignment can at most double the largest preceding degree. This bound applies to that evaluation architecture, not to arbitrary implicit systems. Thus increasing r cannot keep shrinking these circuits indefinitely. The checked r4 construction gives279; the optional MILP screens are restricted cost searches, not global lower bounds.

## Next priorities

1. **Replace the repeated elliptic point representation.** Four root charts and four auxiliary difference charts are the largest structural target. A useful next lemma would give a quadratic presentation of the paired points U,V with U−V=Q, their required formal parameters, and their index domains using fewer than the present ten rational chart coordinates per pair, without adding inverse guards or losing the identity branches. Every proposed rescaling must be checked on U=O, V=O, torsion, and all cleared-denominator strata. More ambitious rational-field constructions need a replacement for the two conjugate local places; simply making H and H−P formal at the same prime forces the fixed P formal there and cannot work at arbitrary contact primes.

2. **Replace the Lucas growth mechanism together with its comparison points.** The two growth labels t,b generate two root charts and two auxiliary pairs, besides logarithms and tests. Seek a cheaper relation that supplies log B≥c|a| with completeness for unbounded a and is expressible with fewer rational quadratic witnesses. Directly eliminating all witnesses to one fixed polynomial relation P(a,t)=0 cannot supply this growth for unbounded a: the ordinary polynomial root bound gives |t|≤C|a|^M outside finitely many a. A successful replacement must retain some additional witness mechanism; it cannot just be a lower-degree plane curve.

3. **Compress the pole and scalar presentations.** A quadratic presentation of the inherited pole predicate using fewer than seven rational coordinates, with exactly the same obstruction and realization domains, would save variables simultaneously in three blocks. For the scalar circuit, preserve both the sublinear input-height bound and the forced lower bound for |a−1|. Improving only the size of a fixed constant does not supply either projection implication.

4. **Broaden local factor allocation as an incremental project.** A new proved elementary option is
   T=1+qA²+q²B²+q³C²
   when v(A),v(B),v(C) are even and v(q) is odd. Its four term valuations are distinct modulo4, so the minimum is unique and the same trace argument applies. At selected contacts with v(q)=−1 and all three test valuations≥2, T≡1. The H test can also occupy the middle class with weight q³⁸ in the order20 construction, or q¹⁰ in the order6 construction. Optimize these allocations jointly with weight gates before claiming another polynomial count. This may improve279/322 but cannot overcome the102-coordinate retained-block obstruction by itself.

No sub100 construction or impossibility theorem has been proved. The next decisive advance must change the elliptic or growth/scalar architecture, while the present algebraic improvements provide smaller verified starting points.
