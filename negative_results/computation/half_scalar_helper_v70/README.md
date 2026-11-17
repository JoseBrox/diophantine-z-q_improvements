# Half of the scalar helper

The [complete proof](../../papers/elliptic_charts/half_scalar_helper_20261117_v70.tex) excludes one proposed deletion in a specified translated-secant chart. Its 21-coordinate interface has exactly seventeen quadratic identities. They all admit an explicit incorrect nonzero scalar quotient at a nontorsion point pair.

The finite-field minor is an exact certificate for the characteristic-zero identity dimension: the paper proves the necessary torsion-free specialization and saturated-lattice statements. It is not a statistical inference from samples.

From the repository root:

```sh
python -B negative_results/computation/half_scalar_helper_v70/check.py --manuscript negative_results/papers/elliptic_charts/half_scalar_helper_20261117_v70.tex --output /tmp/half-helper-v70.json
python -B negative_results/computation/half_scalar_helper_v70/check_independent.py --certificate negative_results/computation/half_scalar_helper_v70/certificate.json --output /tmp/half-helper-independent-v70.json
```

The producer uses only the standard library; the independent checker uses SymPy to expand the seventeen coefficient identities independently. It reads the retained graph points, checks both split elliptic slots and all guards, and directly reconstructs the nonzero minor. The paper and independent review supply the characteristic-zero and density arguments.

Additional global coordinates, other helpers, higher-degree equations and different charts are outside this result. The construction count remains 195.
