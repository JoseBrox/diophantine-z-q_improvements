# A 212-variable quartic with additive comparisons

The full transformation and arithmetic proof are in
`papers/quartic_existence/quartic212_20261113_v25.tex` and its matching PDF.
The pinned predecessor has 214 coordinates and 188 equations. Its complete
numeric source is retained in `../balanced214_v24/source`, with upstream
commit and byte identities in that directory's provenance records.

Both new presentations have **212 coordinates, 186 primitive quadratic
equations, exact degree four, content one, and 2908 nonzero monomials**.
Their rational input projections agree at each fixed parameter. Under the
same stated arithmetic premises, every sufficiently large fixed N defines Z.
The sufficient threshold remains ineffective and is not identified with the
predecessor's threshold. No additional abc assumption is introduced.

## Exact coefficient heights

The unbalanced table uses `A=149^(2*N+1)` and has height `max(C0,A^2+1)`;
the full integer C0 is specified in `construction-report.json`. This is
`149^(4*N+2)+1` for N>=53.

The balanced table uses `C=149^N` and has height

```
max((5898050446009651968*31581660^28)^2,31581660^28*C^2).
```

This is `31581660^28*149^(2*N)` for N>=57. These are coefficient thresholds,
not sufficient defining thresholds. The rescaling fixes the input and is
invertible over Q for every nonzero C.

## Changes to the source

The arguments are `lambda` and `lambda+T`, where T is the same positive
quarter-trace of four root abscissas used in the source. The aggregate row is
quadratic after keeping its existing positive scalar weight. Each contact
block can now use three unscaled outputs and the existing inverse weight.
The contact identity is `(1+q)*P5(r)=r^5`, including the boundary r=0.

In the pinned 214 indexing, rows 22--25,35--38,182 change; rows 64,65 and
coordinates 119,120 disappear. The remaining **177 rows are unchanged**.
The two-coordinate coefficient rescaling uses parent coordinates 117,118.
Neither local-factor exponents nor scalar or pole equations are removed.

The additive arguments change the arithmetic source: this is **not** a
bijection with the old 214 witness tuples. The new completeness proof uses
twenty distinct fixed contact coefficients, and the height proof uses
`h(T)<=h(t0)+h(t1)+log(2)`. All inherited arithmetic suppliers remain explicit.

## Reproduction

```sh
python3 computation/quartic/additive212_v25/build.py
python3 computation/quartic/additive212_v25/check.py
```

The checker imports no producer. It first reproduces the predecessor's
complete published quartic from all 188 source rows. It reconstructs all
changed rows and verifies every retained row, the old and new physical contact
identities, every balanced scaling identity, and both complete quartics. It
checks height for all positive parameters, not a finite parameter sample.
Deliberately corrupted coefficients and missing rows are rejected.
This finite verification is separate from the written arithmetic proof,
independent non-author review and the incomplete foundational audit.
