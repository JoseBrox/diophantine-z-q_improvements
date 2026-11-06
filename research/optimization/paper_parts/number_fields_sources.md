# Number-field research: sources and scope

## Exact current mathematical sources inspected

1. Peter Koymans and Carlo Pagano, *Hilbert's tenth problem via additive combinatorics*, arXiv:2412.01768, v3; Theorem 1.2 states that Z is Diophantine over O_K for every number field K. The full introduction and theorem statement were inspected at https://arxiv.org/html/2412.01768v3 . Published online August 10, 2026, J. Amer. Math. Soc., DOI https://doi.org/10.1090/jams/1081 . Primary source refs: `turn10view1`, `turn6search1`. This is not O_K Diophantine in K.

2. Levent Alpöge, Manjul Bhargava, Wei Ho, Ari Shnidman, *Rank stability in quadratic extensions and Hilbert's tenth problem for the ring of integers of a number field*, Invent. Math. **243** (2026), 1129–1139, published online December 1, 2025, DOI https://doi.org/10.1007/s00222-025-01392-3 . Full introduction, Theorem 1.1 and Corollary 1.2 were inspected at https://link.springer.com/article/10.1007/s00222-025-01392-3 . Corollary 1.2 explicitly states Z Diophantine in O_K for all number fields. Primary source ref: `turn10view0`. arXiv:2501.18774.

3. Barry Mazur, Karl Rubin, Alexandra Shlapentokh, *Existential definability and diophantine stability*, J. Number Theory (2023), https://www.sciencedirect.com/science/article/abs/pii/S0022314X23001324 . Theorems 3.1 and 4.8 give the ring-of-integers transfer from rank stability. The source discusses defining a number-field subfield with one universal quantifier, not an unrestricted existential definition. Primary refs `turn16search14`, `turn6search7`. Needed only for context, not the original proofs in our fragment.

4. Alexandra Shlapentokh, *Defining the integers in large subrings of number fields using one universal quantifier* (2007/2008). Search-extracted Proposition 6.2 and Remark 6.3 distinguish the one-universal-quantifier definition of O_{M,W}∩K from the unavailable existential proof for W equal to all primes. Do not cite this as a current nonexistence theorem; it is historical context only. Full primary publication not yet retrieved, so not used as a mathematical premise.

## Exact repository evidence

Pinned repository revision: `28e87b1b62af0effd954605af7f70b2699dd5672`.

Expanded table: `quartics/quartic-12504/polynomial.expanded.txt`.
SHA-256: `7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca`.

Independent residual representation: `quartics/quartic-12504/residuals.json.gz`.

The specialization to indices 0,2242,2243 is exactly
`5937913971887799417367 + 4*t^2 + t^4 + u^2 + v^2`.
This proves that the released polynomial accepts every element of Q(i).

`check_base_change.py` uses exact fractions and Gaussian rational pairs, checks the specialized polynomial from the table and residuals independently, and then performs the generic substitution in Q(i)[t] independently on both representations.

The earlier exploratory Cornacchia search found an optional exact identity
`95006623550204790677889 = 136^2 + 303178899968^2 + 55580375713^2`.
No primality claim from that search is needed or used. The stronger two-square identity over Q(i) supersedes this numerical route.

## Interpretation

The explicit Q(i) example disproves direct scalar extension of this particular polynomial. It does not disprove Z[i] Diophantine in Q(i), and we have found no number field for which a field-dependent definition of its ring of integers can be ruled out.

The formal equivalence (under Z Diophantine Q)
O_K Diophantine K <=> Z Diophantine K <=> Q Diophantine K
has complete proofs in `number_fields.tex`. Its only non-elementary premise is the already published theorem Z Diophantine O_K.

## BibTeX entries

```bibtex
@article{KoymansPagano2026,
  author = {Koymans, Peter and Pagano, Carlo},
  title = {Hilbert's tenth problem via additive combinatorics},
  journal = {Journal of the American Mathematical Society},
  note = {Published electronically August 10, 2026; arXiv:2412.01768},
  year = {2026},
  doi = {10.1090/jams/1081},
  url = {https://arxiv.org/html/2412.01768v3}
}
@article{AlpogeBhargavaHoShnidman2026,
  author = {Alp{\"o}ge, Levent and Bhargava, Manjul and Ho, Wei and Shnidman, Ari},
  title = {Rank stability in quadratic extensions and {Hilbert}'s tenth problem
           for the ring of integers of a number field},
  journal = {Inventiones Mathematicae},
  volume = {243},
  pages = {1129--1139},
  year = {2026},
  doi = {10.1007/s00222-025-01392-3},
  url = {https://link.springer.com/article/10.1007/s00222-025-01392-3}
}
```
