# Exact checks for fixed trace obstructions

The [manuscript](../../papers/pole_parameters/fixed_trace_obstructions_20261116_v51.tex) proves three separate restrictions: the original general source cannot use a finite fixed set of normalized trace targets uniformly; the conditional six-contact unit-trace equations satisfy an all-slope scale bound excluding prepared source witnesses for shift `B>=19`; and the specified normalization orbit preserves a quadratic norm restriction.

Run from the repository root:

```bash
python -B negative_results/computation/fixed_traces_v51/check.py
python -B negative_results/computation/fixed_traces_v51/check_chamber.py
python -B negative_results/computation/fixed_traces_v51/check_positive_scale.py
python -B negative_results/computation/fixed_traces_v51/check_negative_scale.py
```

The first script uses rational arithmetic and deterministic trial division. It verifies the prime `252877`, the input `X=4`, scalar-contact valuations, both disjoint contact residue sets, native normalization identities, valuation cases, and scalar-prepared norm-orbit examples. Its certificate is `certificate.json`.

The second script uses SymPy 1.14.0 to check the exact derivative identities, the polynomial with positive coefficients after translation by `19/5`, and the rational weight bound used in the real-interval proof. Its certificate is `chamber_certificate.json`.

The two additional scale scripts check the exact reference-point inequalities and rational product bounds on the remaining real intervals.

All four scripts accept `--output PATH`. The integration verifier reconstructs the certificates in temporary directories and compares their complete bytes. The universal statements follow from the manuscript proofs; finite checks do not establish rational realization. The norm-orbit examples are native products, not asserted elliptic detector tuples. No obstruction to the full varying-coordinate norm equations, no new defining-variable count, and no global minimum is claimed.
