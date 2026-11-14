# Exact checks for joint pole realization

From the repository root, run:

```sh
python -B computation/pole_parameters/joint_realization_v29/check.py
```

Python and SymPy 1.14.0 are required. The default mode does not modify the
checkout: it authenticates `inputs.json`, reconstructs every listed exact
check, and compares the resulting deterministic JSON bytes with
`data/audits/joint_pole_realization_20261114_v29.json`.

To produce a separate certificate, use `--output /path/to/certificate.json`.
The checker has explicit failure tests; optimized Python cannot remove the
checks, which use explicit exceptions rather than `assert` statements.

The two manuscripts are
`papers/pole_parameters/joint_pole_realization_20261114_v29.tex` and
`papers/elliptic_charts/progression_density_20261114_v29.tex`.
The checks certify polynomial identities, explicit rational examples, finite
algebraic examples, and branch-count calculations. They do not prove the
external arithmetic inputs, rational-point finiteness, or a smaller global
Diophantine construction. **The current counts remain 25 and 13.**
