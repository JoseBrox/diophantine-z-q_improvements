# Rings of integers and existentially defined subfields

The paper `number_field_definability_20261109_v12.tex` gives complete proofs of the following statements. Counts include distinguished inputs.

- For every number field K, its ring of integers is Diophantine in K if and only if Z is Diophantine in K. The implication from the ring of integers uses the established Denef–Lipshitz theorem, cited to Alpöge–Bhargava–Ho–Shnidman, Corollary 1.2.
- Assuming Z is Diophantine in Q, these statements are equivalent to Q being Diophantine as a subfield of K.
- For every finite characteristic-zero extension L/K, defining K in L is equivalent to defining the relative norm image, norm graph, or trace graph as subsets of powers of L. The norm-image implication uses a finite-difference identity. For quadratic extensions, defining the conjugation graph is equivalent as well.
- A definition of Z inside a degree-n number field with N total coordinates gives a definition of its ring of integers with nN total coordinates.
- An N-coordinate definition of O_L in L descends along a degree-d extension L/K to a definition of O_K in K with 1+d(N−1) total coordinates. A genuine counterexample therefore remains a counterexample in every finite extension.
- Rank stability gives an infinite Diophantine subset of the rational subfield, while the cited ring-transfer theorem quantifies over rings of integers and the field-transfer theorem retains one universal quantifier. The positive-rank curve y²=x³−2 gives a concrete obstruction to the simple multiplicative approach: every rational abscissa has even 5-adic valuation, so no multiplicative combination can equal 5.
- A fixed finite family of existential formulas cannot define the rings of integers across all finite extensions. This concerns reuse of formulas, not separately chosen formulas for individual fields.

The paper does not claim that every number field has a Diophantine ring of integers in its field of fractions, and it does not supply a counterexample.

## Exact verification

Run:

```sh
python check_norm_image_reduction.py
```

The script uses only Python's standard library. It independently checks every coefficient of

```text
sum_{j=0}^{n-1} (-1)^(n-1-j) binom(n-1,j) (T+j)^n
    = n! T + n!(n-1)/2
```

for n=1,...,64, plus exact rational and quadratic examples. It also enumerates the reductions of y²=x³−2 at 5 and 7 in two independent ways, confirming group orders 6 and 7, and checks the exact double of (3,5). It writes `norm-image-reduction-verification.json`. The proof for every n is in the paper; the finite checks are supplementary and do not establish any new defining polynomial for a ring of integers.

## Primary bibliography

- L. Alpöge, M. Bhargava, W. Ho, A. Shnidman, *Rank stability in quadratic extensions and Hilbert's tenth problem for the ring of integers of a number field*, Inventiones Mathematicae 243 (2026), 1129–1139, Corollary 1.2. <https://doi.org/10.1007/s00222-025-01392-3>
- B. Poonen, *Rank stability makes rings of integers diophantine*, 3 July 2026, sections 1.2, 4, 5. <https://math.mit.edu/~poonen/papers/h10_over_OK.pdf>
- Stacks Project, Chevalley's theorem, Tag 00FE. <https://stacks.math.columbia.edu/tag/00FE>

- G. Cornelissen, A. Shlapentokh, *Defining the integers in large rings of a number field using one universal quantifier*, J. Math. Sci. 158 (2009), 713–726, Theorem 4 and Remark 6.3. <https://arxiv.org/abs/0708.3075v2>
