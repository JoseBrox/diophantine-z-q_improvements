# False witnesses for an input-only height helper

The [proof](../../papers/pole_parameters/input_only_weight_false_witnesses_20261117_v61.tex)
constructs noninteger rational inputs for the stated two-block source.
The extra degree-eight input weight supplies a genuine input-height bound,
but the integer quotient can grow through the local congruences.

```sh
python -B negative_results/computation/input_only_weight_v61/check.py
```

The exact checker covers the input polynomial, fixed local square classes,
compatible reference-index progressions, valuation inequalities and finite
formal-logarithm interpolation maps. It does not numerically construct the
global witnesses. Their existence uses the manuscript proof and the retained
intrinsic-pole realization theorem. No assertion concerns all two-point
sources or all nine-variable definitions.
