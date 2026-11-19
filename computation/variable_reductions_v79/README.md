# Variable reductions and exact audits, v79

The ordinary-abc quartic is reduced from 62 to 59 total variables, including the input. Its source chart and Laurent packing derive from **notes of Gabe Conant with Astra 6.2**, audited in v78. The derivative contact and uniform normalizer are subsequent project work. All defining statements retain the arithmetic premises explicitly listed in the proof.

- `abc/`: builder, independent checker and complete expanded coefficient tables for the 59-variable quartic; 51 quadratic rows and 873 monomials.
- `pole_normalization/`: independent verification of the physical maps for all ten native pole blocks in the original and enhanced 165/180 tables.
- `quartics/`: an exact parity certificate excluding one full hyperbolic pair in the specified integral Laurent compilation; no global lower bound is asserted.

The complete proof is `papers/quartic_existence/single_derivative59_20261119_v79.tex`. The continuation guide is `docs/results_20261119_v79.md`. The 25-, 165-, 180- and unrestricted-degree 11-variable counts have not been reduced in this continuation.

Run `python -B scripts/verify_v79.py` from the repository root. This reconstructs the builder output in a temporary tree, compares every published coefficient, checks the independent physical-map audits and verifies source and review hashes. It does not establish the retained arithmetic premises.
