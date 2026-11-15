# Primitive quadratic basis for the 78-variable quartic

An explicit invertible rational 8-by-8 matrix replaces the reference equations
of `abc78_reduced_v40`. All other equations and all coordinates are unchanged.
The rational zero set is identical for every fixed parameter. The retained
count is 78 variables and 68 primitive quadratic equations, of total squared
degree four and integer content one.

The fixed transformation, its inverse and exact determinant are stored in
`basis-certificate.json`. The producer applies that certificate directly; no
lattice search is required for reproduction. The independent checker imports
no producer code, verifies the transformation in both directions and uses
SymPy for a separate expansion and all-parameter coefficient checks.

```sh
python -B computation/quartic/abc78_balanced_v40/build.py
python -B computation/quartic/abc78_balanced_v40/check.py
```

The exact coefficient height and support are in `construction-report.json`.
The proof of invariance and the coefficient statements are in
`papers/quartic/primitive_quadratic_bases_20261115_v40.tex`.
The defining threshold is unchanged and remains ineffective; the underlying
ordinary-abc, group, prime-pattern and prepared pole-realization inputs retain
their original status.
