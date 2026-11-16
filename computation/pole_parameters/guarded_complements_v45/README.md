# Guarded native square complements

The [proof](../../../papers/pole_parameters/guarded_complement_reduction_20261116_v45.tex) shows that prepared actual detector tuples have nonzero complements at every point-algebra character. It gives a conditional finite-algebra reduction to 21/9 variables, assuming the explicitly stated native rational-complement realization theorem. That realization theorem is unproved; 25/13 remain the general records.

The exact checker verifies 24 point-block character identities, 5 free-input section identities, and two prepared free inputs at a common rational pole parameter. It does not test native realization or establish a new variable record.

Run from the repository root:

```sh
python -B computation/pole_parameters/guarded_complements_v45/check.py --output /tmp/complement-certificate.json
```
