# Mixed torsion signs for doubled reference points

The exact certificate gives a prime above the current local cutoff and an infinite progression of global doubled reference points whose two relevant reductions are `O` and `T0`. This disproves automatic agreement of the two torsion-translation signs. It does not assert that any such point completes the full detector system.

The proof is in [the manuscript](../../papers/elliptic_charts/mixed_reference_signs_20261116_v42.tex).

Run from the repository root:

```sh
python -B negative_results/computation/mixed_sign_v42/build.py
python -B negative_results/computation/mixed_sign_v42/check.py
```

`build.py --output PATH` reconstructs `certificate.json` in another directory. `check.py --certificate PATH` verifies that file independently. Only the Python standard library is used. The producer uses affine arithmetic; the checker uses Jacobian arithmetic and reconstructs the constants rather than importing the producer.

The checker certifies exact point orders by one annihilating multiple and nonzero multiples for every prime divisor of the claimed order. It also checks trial-division primality, the progression congruences, a second good reduction proving that the fixed point is non-torsion, exact doubling over `Q(sqrt(2))`, and the translation identities as Laurent polynomials.
