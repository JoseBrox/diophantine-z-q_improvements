# A guarded square criterion on actual detector traces

The [manuscript](../../../papers/pole_parameters/native_square_criterion_20261116_v53.tex) proves negative odd pole exclusion, whole-character positivity and guards, admissible source-dependent coefficients, the exact prescribed-coordinate elliptic identity, and the finite-algebra implication giving 21/9 variables **conditional on uniform actual rational realization**. That realization is not proved; the established source counts remain 25 and 13.

From the repository root:

```bash
python -B computation/pole_parameters/native_squares_v53/check.py
```

The checker reconstructs the certificate in memory and compares it with the distributed bytes. `--output PATH` writes the reconstruction. It verifies the rational-function identities, conditional decay, symmetry, 784 safe-parameter integer-order cases, the displayed local limits, and three exact actual multiplication examples using the retained source fixture.

These computations neither assert that the example radicands are rational squares nor establish local square values at every prime. The point examples certify the actual test permutations, detector conjugation and radicand invariance. The manuscript states the precise additional global realization needed for the smaller counts.
