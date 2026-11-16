# Norm preparation in the detector field

The [manuscript](../../../papers/pole_parameters/detector_field_norm_scalar_20261116_v52.tex) gives a degree-four integrality-reflecting label and a scalar norm from `Q(sqrt(2))`. Its full transfer through the retained general source keeps 25 total variables. The prepared physical weights, including those of the unchanged conditional sources, are norms from the same field. The prescribed-trace realization needed for 21/9 remains unproved.

Run:

```bash
python -B computation/pole_parameters/detector_field_norm_v52/check.py
```

The standard-library checker compares the complete certificate by default. Use `--output PATH` to reconstruct it elsewhere and `--repo PATH` to specify the source checkout. It expands the universal norm identity, reconstructs every coefficient of the input and contact polynomials, verifies the uniform denominator-dominance inequalities and fixed local divisibilities, and checks explicit rational specializations. Six retained source files are pinned by SHA-256.

The certificate does not replace the source-transfer proof, the conic Hasse principle, or the retained external arithmetic premises. No numerical sufficient exponent or defining-polynomial degree is inferred from it.
