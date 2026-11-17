# Arithmetic of an actual derivative trace

The [complete proof](../../../papers/pole_parameters/actual_trace_arithmetic_20261117_v70.tex) factors each fixed-tuple actual-trace square equation through a weight curve of genus at most 36. It states the exact degree-nine equation, rational-square test and original guards required to lift a rational point back to the derivative source.

The explicit fixture `X=1`, `B=3`, `A=P`, `H=U=5P` has weight-curve genus 24, squared-slope-quotient genus 224, companion-quotient genus 225 and slope-curve genus 449. The certificate lists the exact integer numerator and denominator of the actual trace and the physical weight map. The degree-450 composition polynomial is specified by homogeneous composition; modulo-101 Bezout identities certify squarefreeness without a huge printed expansion.

The fixture uses the actual six test values, not a free trace parameter. The independent checker reconstructs every coefficient using only exact standard-library arithmetic and validates both Bezout identities and all genus counts. It also checks an actual slope which is a square at 17 and a nonsquare at 31. Those primes lie in the retained exceptional set. This is a local illustration, not full preparation or a completeness counterexample.

`B=3` is an algebraic fixture, not a sufficient defining shift. No rational point surviving all lift and preparation conditions has been obtained, and no defining-variable count changes.

From the repository root:

```sh
python -B computation/pole_parameters/actual_trace_arithmetic_v70/check.py --manuscript papers/pole_parameters/actual_trace_arithmetic_20261117_v70.tex --output /tmp/actual-trace-arithmetic-v70.json
python -B scripts/verify_v70.py
```

The integration gate replays the independent checker in a temporary source directory containing exact copies of the author checker, certificate and manuscript, so the publication contains only one manuscript copy. The retained independent review covers square-denominator changes, zero terminal roots, singular affine points, the two quotient maps and every rational lift exclusion.
