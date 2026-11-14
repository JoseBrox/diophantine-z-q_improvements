# Complete reference-chart replacements

`build.py` replaces the six common-point equations and two reciprocal-square definitions in the retained 226- and 262-variable sources. The results have 224 and 260 variables, respectively. The latter is fully specified at the original certified N=9682; the row replacement is projection-equivalent for every fixed N and introduces no new arithmetic premise.

`check.py` independently reconstructs every changed and retained row, expands all quartic coefficients, checks the exact height envelopes, and rejects corruptions. It also checks the new `pole81_v27` alternative. The complete chart proof and exceptional-case certificate are in `papers/elliptic_charts/compressed_reference_20261114_v27.tex` and `../abc79_v27`.
