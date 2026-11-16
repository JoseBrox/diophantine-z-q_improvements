# Local cancellation in shared reference tests

The [manuscript](../../papers/elliptic_charts/shared_reference_test_obstructions_20261116_v43.tex) proves the local cancellation of the stated squared reference factor and the Hensel-lifting obstructions for both whole-factor odd-cube repairs.

Run from the repository root:

    python -B negative_results/computation/shared_reference_tests_v43/check.py --output /tmp/shared-reference-tests.json

Use SymPy 1.14.0. The checker verifies the exact factor identities, the selected split-prime data, the normalized Hensel equations, modular lifts, and the contact-polynomial inverse used to realize the local parameter. These computations support the manuscript's local existence proof.

The scope is an obstruction to the specified **local factor implications**. The examples are not asserted to be simultaneous global, cyclic, doubled, or two-detector solutions, and no false solution of a complete defining source is claimed. The stored `verification.json` is reconstructed byte for byte by `scripts/verify_v43.py`.
