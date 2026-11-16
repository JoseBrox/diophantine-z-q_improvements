# Quadratic reference and height rescaling

The [manuscript](../../../papers/elliptic_charts/scaled_reference_height_20261116_v43.tex) proves the chart isomorphism, exact rescaling on the nonzero locus, recovery of the original rational trace, and the counted nonzero guard.

Run from the repository root:

    python -B computation/elliptic_charts/scaled_reference_v43/check.py --output /tmp/scaled-reference.json

Use SymPy 1.14.0. The checker verifies 36 exact identities, the reference boundary values, the degenerate zero-scale family, and the rational-coordinate accounting. The block count is **33 originally**, **32 on the open rescaled locus**, and **33 after the explicit nonzero guard**. Detector conversion is outside this block comparison. No complete defining-variable reduction is claimed.

The stored `verification.json` is reconstructed byte for byte by `scripts/verify_v43.py`. The algebraic checks do not replace the manuscript's isomorphism and domain arguments.
