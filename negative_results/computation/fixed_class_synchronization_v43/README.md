# Fixed-class synchronization: exact verification

Run from the repository root with Python and SymPy:

```sh
python negative_results/computation/fixed_class_synchronization_v43/verify.py
```

To regenerate the saved certificate:

```sh
python negative_results/computation/fixed_class_synchronization_v43/verify.py --output negative_results/computation/fixed_class_synchronization_v43/certificate.json
```

The checker verifies the branch discriminant and pairwise resultant,
the pole-scaling identity, the two explicit genus-five quotient equations,
the dimensions of the displayed differential spaces, and the local
ordinary-double-point quotient and resolution forms. It also checks the
arithmetic of the genus formula for one through eight factors and the
fixed-fiber Jacobian invariants used in the literature note.

The general genus, isogeny decomposition, canonical-bundle formula, and
finite-fixed-class conclusion are proved in the accompanying paper.
The checker does not certify rational-point existence or nonexistence for
actual detector tuples, and does not assert a defining-variable reduction.
