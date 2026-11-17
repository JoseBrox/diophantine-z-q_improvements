# Elliptic index poles and amplified congruences

The [manuscript](../../../papers/elliptic_divisibility/elliptic_index_poles_20261117_v60.tex) gives a balanced intrinsic-pole source that forces divisibility of elliptic indices. It proves complete preparation for every nonzero integer quotient, implements the fixed subgroup cosets by monic finite algebras, and amplifies the comparison with an external rational input to any fixed order without a new free coordinate.

Run from the repository root:

```sh
python -B computation/elliptic_divisibility/index_poles_v60/check.py --output /tmp/index-poles-v60.json
```

The certificate verifies 13 symbolic formal-logarithm terms, the multiplication-by-two and multiplication-by-three monic isogeny identities, 19,744 valuation cases, and exact coprime-index constants. Preparation at two uses a uniform initial formal depth of four.

The mathematical theorem assumes weak rational abc at one fixed exponent strictly between one and two, together with the stated intrinsic-pole realization input. The checker does not prove those external inputs. Equality between the external input and the integer quotient still requires a separate argument; no smaller defining-variable bound is asserted.
