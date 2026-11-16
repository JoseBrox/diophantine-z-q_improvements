# Adaptive native complement levels

The companion manuscript is [Adaptive levels and varying norm classes for native elliptic detectors](../../../papers/pole_parameters/adaptive_native_complements_20261116_v50.tex).

The exact normalization replaces the weight by `w/(1+w)^2` and the detector product by `(1+w)W`. It leaves the physical output `b` unchanged. At a negative odd pole, the normalized weight, reciprocal trace and reciprocal norm all reduce to zero. This permits level denominators that need only be units at that residue configuration, provided their prepared whole-character guards are proved separately.

The concrete denominator `1-Vstar+Jstar` is positive at every prepared character. The normalized class `1-4*wstar/17` is at least `16/17` and has the fixed bare norm point `(1,1)`. The manuscript also proves the larger varying-class and coefficient families, the exact finite-algebra census, and a sufficient scaled norm-one incidence on the actual detector products.

## Reproduction

```bash
python -B computation/pole_parameters/adaptive_levels_v50/check.py --output /tmp/adaptive-levels.json
```

Compare the output byte for byte with `certificate.json`. The checker uses Python 3.12, SymPy 1.14.0 and exact rational arithmetic. It verifies:

- 12 universal symbolic identities, including the unchanged detector output and the scaled norm-one/trace identity;
- 1,296 native-product specializations at 12 primes, including all three residue configurations and 792 negative odd poles;
- 23,328 varying-class valuation evaluations, using both signs of odd original weight valuations;
- 36 weight-unit cases in which the normalization introduces an even negative valuation;
- an exact positive-contact example where the new level multiplier has valuation minus one.

The native-product examples are not asserted to be elliptic detector tuples. The finite computations do not prove a global rational point on an actual prescribed-trace incidence. The manuscript supplies the universal valuation and whole-character arguments.

**No new defining-variable bound is certified.** The established general counts remain 25 and 13. The counts 21 and 9 are proved consequences of the explicitly unproved simultaneous actual-realization premise.
