# Fixed-slope trace incidence

The [manuscript](../../papers/rational_fibers/fixed_slope_trace_finiteness_20261117_v59.tex) proves finiteness for the actual first trace in the stated reweighted sources, at a fixed input and prepared slope, on a fixed smooth genus-one trace curve. All point roles may vary independently.

`check.py` verifies the explicit CM isomorphism over the quadratic extension and all **518 nonzero direction-parity vectors** for the conditional and general tested-point lists. Run it with `--output PATH` to reproduce [certificate.json](certificate.json).

The endomorphism descent, real nonconstancy and Mordell–Lang argument are mathematical proofs, not finite computational conclusions. Individual witnesses, varying slopes, point-dependent auxiliary curves and the untwisted conic remain outside the finiteness conclusion. No transfer to the derivative detector is asserted.
