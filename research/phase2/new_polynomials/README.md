# Shared-point source constructions

The preferred sources lead to conditional definitions of the integers with
**43 total rational coordinates**, or **45** with the semilocal size anchor.
The totals include the input coordinate, so the witness counts are 42 and 44.
Their arithmetic hypotheses are the stated results of the pinned original
manuscript and Sun's simultaneous prime-pattern theorem, arXiv:2610.20691v2,
Theorem 4.1. The arithmetic inputs are not independently certified by the source
or compiler checks in this directory. Sun's undecidability theorem is not used
as a definition of the integers.

## Preferred exact sources

| File | Retained coordinates | Finite generators | Intermediate algebra rank | Final total |
|---|---:|---:|---:|---:|
| `source-43-conic.json.gz` |42|20|2^29|43|
| `source-45-conic-semilocal.json.gz` |44|21|2^30|45|

These are complete coefficient DAGs and finite branch specifications for the
rational source system. The finite-anchor source additionally uses an indexed
product over 1≤n≤2^9566463, with explicitly computable fixed elliptic multiples.
That product has not been expanded. The semilocal source has a fully materialized
coefficient DAG, whose large fixed constant is encoded by an integer power node.
Final polynomial specifications, degree bounds, coefficient-height bounds, and
independent compiler checks belong to the separate finite-algebra packages.

Both preferred sources use comparison order 64, beta order 16 and scalar
order 48. They share the scalar-height point with the common comparison point,
normalize the scalar contact to remove its preparation coordinate, use fixed
nonzero coordinate scales, and parametrize all ten first pole conics. The only
fixed finite choices are 16384 scalar corrections and ten binary conic charts.
Repeated roots are subsequently handled by the finite-algebra compiler.

## Mathematical proof order

1. `shared_source.tex`: the complete shared construction, including the
   two-anchor comparison, reciprocal trace, five-contact height transfer,
   prime-pattern completeness, single ordinate chart, and sharing proof.
2. `scalar_preparation_zero.tex`: the scalar normalization, local squareclass
   basis, real neighborhood argument, and 43/45 coordinate counts.
3. `degree_refinements.tex`: fixed coordinate scales and exact parametrization
   of the pole conics, giving the intermediate ranks in the table.
4. `precision52.tex`: a separate refinement for the quartic circuit. It permits
   comparison order 52 with C=3^(2^26), or finite cutoff 2^31091008. The preferred
   finite-algebra sources above retain order 64.

`sharing_review.tex`, `scalar_preparation_zero_review.md`, and
`independent_review.md` record independent mathematical reviews. The sharing
proof is already included in `shared_source.tex` and should not be included
twice when assembling the paper.

## Reproduction

Run from the repository root:

```sh
python research/phase2/new_polynomials/build_shared_source.py --anchor finite --share-height --normalize-scalar --parametrize-poles --fixed-scales --output research/phase2/new_polynomials/source-43-conic.json.gz
python research/phase2/new_polynomials/build_shared_source.py --anchor semilocal --share-height --normalize-scalar --parametrize-poles --fixed-scales --output research/phase2/new_polynomials/source-45-conic-semilocal.json.gz
python research/phase2/new_polynomials/check_source_structure.py
python research/phase2/new_polynomials/check_scalar_preparation_zero.py
python research/phase2/new_polynomials/check_degree_refinements.py
python research/phase2/new_polynomials/check_precision52.py
```

The checks distinguish their scope explicitly: frozen-byte reproducibility and
triangular monicity; exact finite arithmetic for the scalar normalization;
small polynomial identities; and numerical precision inequalities. Their
success does not replace the mathematical proof or certify its external
arithmetic hypotheses. Previous source variants remain available and reproduce
byte for byte when the corresponding options are omitted.

## Primary inputs

- Original source, commit 28e87b1b62af0effd954605af7f70b2699dd5672:
  <https://github.com/elliotglazer/diophantine-z-q/blob/28e87b1b62af0effd954605af7f70b2699dd5672/quartic_12504.tex>.
  Relevant statements include the cyclic elliptic-group computation,
  five-contact height estimate and explicit H bound, pole completeness,
  reciprocal logarithm estimates, and original scalar norm argument.
- Zhi-Wei Sun, *86 unknowns for Hilbert's tenth problem over the rationals*,
  arXiv:2610.20691v2, Theorem 4.1:
  <https://arxiv.org/pdf/2610.20691v2>.
  The construction uses its simultaneous prime patterns, Gaussian residue
  classes, and cross-prime reduction-order coprimality. The curve change is
  supplied explicitly in `shared_source.tex`.
- Daans, Dittmann and Fehm, arXiv:2102.06941v5:
  <https://arxiv.org/pdf/2102.06941v5>.
  This supplies the broader literature context for variable compression and
  essential fibre dimension; the repository paper gives the specific finite
  algebra construction used to produce the final indexed polynomials.
