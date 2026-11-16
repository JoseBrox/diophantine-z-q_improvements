# Actual prepared neighborhoods without square complements

The companion proof is
[`actual_square_complement_neighborhoods_20261116_v43.tex`](../../papers/pole_parameters/actual_square_complement_neighborhoods_20261116_v43.tex).
For every odd exponent of the native general source, one input in
`{3,6,7}` admits complete guarded prepared actual return families whose
detector complements are all nonsquares in `Q_23`. Thus shrinking an
arbitrary prepared return neighborhood cannot force rational square
complements. Other actual tuples and common rational pole fibers remain
outside this obstruction's scope.

Run from the repository root:

```sh
python negative_results/computation/actual_square_complement_v43/check.py
```

The checker requires only Python and writes `verification.json`.
Use `--output PATH` for an independent reconstruction. It checks all
eleven exponent residue classes using exact rational arithmetic and a
separate modular computation, evaluates eleven native general-source
scalar circuits, and verifies the explicit27 member at `L=20483`, `X=6`.
There the scalar is 22 modulo 23 and all three complements are 7 modulo 23.

The certificate binds the native coefficient builder and supporting
source papers by SHA-256. The finite computations certify the residue
identities and source bindings. Actual source completeness and independent
index returns use the retained arithmetic premises and the proofs stated
in the manuscript.
