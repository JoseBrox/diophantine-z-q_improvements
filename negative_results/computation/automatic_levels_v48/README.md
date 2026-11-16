# Automatic norm levels: exact certificates

The accompanying paper proves a local norm-valuation bound for every guarded
tuple of the original conditional detector. Admissible automatic levels then
give only finitely many contact arguments, by Faltings' theorem. The two coupled
arguments cannot support infinitely many integer inputs. This concerns the
specific level `w * Norm(W)`, not independently prescribed norm incidences.

Run from the repository root with Python 3.12 and SymPy 1.14.0:

```sh
python -B negative_results/computation/automatic_levels_v48/check.py
```

To reconstruct a certificate in a chosen temporary path, add `--output PATH`.
The output is deterministic and reproduces `certificate.json` byte for byte.

The self-contained implementation uses exact arithmetic in `Q(sqrt(2))` and
does not import an earlier detector producer. It verifies the exceptional
prime support, contact squarefreeness, actual split/inert examples, complement
identities, and consistency with the published finite benchmark. The finite
valuation screen supplements the all-valuation proof. The script does not
enumerate the genus-two rational points or verify an effective finiteness bound.

Paper:
[Finiteness of automatic norm levels for conditional elliptic detectors](../../papers/pole_parameters/automatic_level_finiteness_20261116_v48.tex).
