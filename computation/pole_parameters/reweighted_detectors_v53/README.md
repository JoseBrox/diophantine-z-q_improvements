# Quadratic reweightings of native elliptic detectors

The [source theorem](../../../papers/pole_parameters/reweighted_elliptic_detectors_20261116_v53.tex) proves the full soundness, ordered completeness and guard transfer under the retained arithmetic premises. The source counts remain **25 and 13**, including the input. No defining-polynomial degree bound from a different source is transferred to these families.

The general source uses the physical weight $w=u/(1+u)^2$ throughout the detector and one extra contact factor in each scalar numerator. The conditional source retains its physical weight and uses the quadratic product

```math
W(t)=\prod_{i=1}^6\left(1+\frac{C_i^2}{F(t)}\right).
```

Its last comparison is $C_6=r+\bar s-2X$. The two comparison tests are an invertible rational change of the original tests. The new product satisfies $W-1=O(w^3)$ at the fixed preparation places as the slope tends to infinity.

From the repository root:

```bash
python -B computation/pole_parameters/reweighted_detectors_v53/check.py
```

The default command reconstructs the certificate in memory and compares it with the distributed bytes. `--output PATH` writes a newly reconstructed certificate. The checks include exact symbolic identities, weight and scalar valuation examples, 648 generic native-product cases and 432 negative odd pole cases. They supplement the universal manuscript proofs; they neither prove the external arithmetic premises nor establish simultaneous rational square values on actual detector tuples.
