# Five local detector factors

The [paper](../../../papers/quartic/revised_detector_factors_20261117_v66.tex) proves valuation separation at every positive odd contact depth, extraction from the inherited trace and pole equations, selected-contact residues, and finite and real preparation limits. Zero tests are included. No smaller complete quadratic table or defining-polynomial count is asserted.

Run from the repository root:

```sh
python -B computation/quartic/local_detector_factors_v66/check.py
```

The standard-library checker verifies the complete residue period modulo eight, seven exact extraction coefficients, all sixteen selected-contact bounds, and the fixed-place limit depths. The infinite valuation and preparation statements follow from the paper's proofs, rather than from sampled valuations.
