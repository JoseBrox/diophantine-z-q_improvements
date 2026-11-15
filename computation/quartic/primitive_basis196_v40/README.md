# A primitive quadratic basis for the 196-variable quartic

The fixed invertible rational matrix in `transform.json` replaces eight reference rows of the 176-row source. Two contactCombination coordinates are then rescaled by the nonzero constant 1/3813373161796. Every row is normalized to primitive integers. The input is fixed, and the entire rational solution set is preserved by this coordinate bijection.

The resulting polynomial has 196 total variables, 176 primitive quadratic summands, exact degree four, integer content one and 2994 monomials. With C=149^N, N>=1, its exact height is

    max(126616122944180358034867798936, 32561227748626372080 * C^2).

The constant term in this maximum dominates for N=1,2; the C² term dominates for N>=3. This is a coefficient crossover, not a numerical defining threshold. The original arithmetic hypotheses and ineffective sufficient threshold remain unchanged.

```sh
python -B computation/quartic/primitive_basis196_v40/build.py
python -B computation/quartic/primitive_basis196_v40/check.py
```

`quadratic.json` and `polynomial.json` are the complete coefficient specifications. `normalizations.json` records every primitive-row factor. `certificate.json` includes the inverse rational row transformation and all count/height conclusions. The checker imports no producer or lattice-reduction code; it uses only exact standard-library arithmetic to verify the fixed matrix, complete row identities, expanded quartic, support for every C>=149 and coefficient height for all N>=1.

The proof, including the analogous 78-variable construction, is `papers/quartic/primitive_quadratic_bases_20261115_v40.tex`. The sparser 2853-monomial 176-row specification remains available in the sibling `paired_redundancy196_v40` directory.
