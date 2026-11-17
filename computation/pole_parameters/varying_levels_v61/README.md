# Rationally soluble varying pole levels

The [manuscript](../../../papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex)
proves local solubility at every rational level, and infinitely many rationally
soluble levels for each prepared input under the stated simultaneous-twist
theorem. Each selected level has infinitely many rational points. The
two-parameter witness set is dense and avoids every retained character guard.

```sh
python -B computation/pole_parameters/varying_levels_v61/check.py
python -B computation/pole_parameters/varying_levels_v61/check_independent.py
```

The symbolic checker proves the transformations, the degree-nine radicand's
exact support and height, and the explicit nonsquare-complement example.
The independent standard-library checker verifies the local valuation cases,
2,048 finite-field fibers, and 16 rational witness pairs on four levels.
These finite checks supplement the manuscript's proofs of the infinite
statements. Neither a prescribed detector level nor simultaneous realization
for two actual detector inputs is established. Both free pole coordinates
remain in the count.
