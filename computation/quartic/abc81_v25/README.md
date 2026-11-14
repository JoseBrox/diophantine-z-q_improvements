# An 81-variable quartic under rational abc

All counts include the input. The complete proof is in
`papers/quartic_existence/quartic_abc81_20261113_v25.tex` and its matching PDF.
The algebraic trace-height and reciprocal-point arguments are proved separately in
`papers/trace_heights/trace_on_all_points_20261113_v25.tex`.

The family has **81 rational coordinates, 73 primitive quadratic equations,
exact degree four, content one, and 941 nonzero monomials** for every positive
coefficient parameter B. Its exact coefficient height is
`max(4153456, B^2+797551)`. The defining theorem uses sufficiently large fixed
odd B, with an ineffective threshold. **B=3 is not a certified defining member.**

The additional hypothesis is ordinary rational abc. The elliptic group,
prepared pole realization, pole obstruction, and fixed-data simultaneous-prime
inputs are retained exactly as stated in the paper. No modular contact-height
premise is used. Passing computations do not establish those inputs.

## Mathematics

Two reciprocal points `(f,h)` and `(g,k)` on `h^2=f-D*f^3` determine their
difference through a secant or tangent parameter s. Storing its trace rather
than a separate square-abscissa root chart reduces the elliptic coordinates.
The new source includes half-integral indices and torsion translates. The
proved all-point trace theorem supplies the required uniform height bound.
The input map is `beta=X^2+B`; using the predecessor's `2*X^2+B` would not give
the needed denominator conclusion for half-integral indices.

The two comparison arguments are `lambda` and `lambda+beta^4+T^4`.
Two quadratic height outputs compute this difference without retaining a
separate comparison-scale coordinate. The proof checks the new sixteen-contact
prime pattern, identity and tangent cases, torsion components, zero weights,
and the order of all existence choices. Completeness deliberately uses integer
indices `n=beta`, not arbitrary half-integral indices.

## Exact specification and reproduction

Run from the repository root:

```sh
python3 computation/quartic/abc81_v25/build.py
python3 computation/quartic/abc81_v25/check.py
python3 computation/quartic/abc81_v25/check_examples.py
```

The builder emits the complete coordinate list, all quadratic equations,
expanded quartic, and exact counts and height. The parameter is represented by
`parameterPower` and is never a quantified coordinate. The first six common
reference equations use the fixed invertible matrix in
`common-row-reduction.json`. Every other normalization is a primitive integer
row normalization, with a specified sign.

The checker imports no producer. It reconstructs every field equation with
SymPy, checks the row change, expands all 73 squares independently, and checks
all 941 coefficient profiles and deliberate rejection controls. The exact
example checker uses rational arithmetic in Q(sqrt(2)) and checks 702 ordered
point pairs, including 24 tangent pairs, 52 identity pairs, 78 torsion
differences and 352 half-integral differences. These examples are finite
supplementary evidence, not a proof of all rational cases or complete defining
witness tuples. The universal proofs are in the papers. Separately written
implementations in this session are not independent non-author review.
