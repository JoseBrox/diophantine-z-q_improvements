# The 456-variable quartic

The [quartic paper](../../papers/quartic/quartic_20261107_v7.pdf) gives the mathematical construction, its domain conditions, the local proofs, and the conditional integer-projection theorem.

The exact quartic has 456 total variables, 426 quadratic residuals, 27,784 coordinate monomials, degree four, content one, and coefficient height $64\cdot3^{105665812}$. The fixed integer $S=3^{52832906}$ is represented symbolically as a coefficient.

From the repository root:

```bash
python3 scripts/restore_data.py
python3 computation/quartic/verify_quartic456.py
```

The checker imports no producer code. It verifies the complete coordinate substitution from the 474-coordinate baseline, each of the four pole rescalings, the reciprocal-power chain, the quadratic residuals, and every coefficient of their expanded sum of squares.

To rebuild the final tables in a separate directory:

```bash
python3 computation/quartic/build_quartic456.py --output /tmp/reconstructed-quartic456
```

The complete [baseline source verification](baseline/) identifies that baseline with the explicit arithmetic source. It requires Node.js 18 or newer as well as Python. The root command `python3 scripts/verify.py --full` restores all compressed source data in an isolated temporary tree, runs the baseline verification, compares the final baseline bytes with the final producer's input, rebuilds the 456-variable polynomial, and performs the independent checks.

The exact algebra and coefficient checks do not certify the global arithmetic premises listed in the paper. In particular, the single equation is equivalent to its quadratic system over $\mathbb Q$; the field-extension paper explains why that equivalence cannot be assumed over every extension field.
