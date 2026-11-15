# Rational sections of fixed-input pole fibrations

The companion [manuscript](../../papers/pole_parameters/rational_sections_20261116_v42.tex) classifies the existence of rational-function sections in the conic parameter. For prepared fixed inputs, a section exists exactly when `C=17(17-b)` is a rational square. This does not assert nonexistence of rational points at any rational parameter or of one parameter shared by several inputs.

Run from the repository root:

```sh
python -B negative_results/computation/rational_sections_v42/check.py
```

The checker requires SymPy and reconstructs `verification.json`. Its optional `--output PATH` writes the same certificate to another file. It checks the quotient substitution, the Weierstrass maps and invariants, the isomorphism over `Q(sqrt(C))` and its inverse, the Galois involution, the Jacobian twist equation, the two fixed-point charts, and the explicit sections. All calculations are exact polynomial or rational-function identities.

The geometric non-CM, morphism and Galois-descent arguments are proved in the manuscript, with primary references for CM integrality and the morphism theorem. Those arguments are not inferred from finite computational examples.
