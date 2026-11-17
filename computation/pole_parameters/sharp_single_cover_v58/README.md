# Signed mixed-power heights and single-cover criteria

The [manuscript](../../../papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex) proves the universal height theorem under its stated weak rational abc inequality. The computations verify its exact denominator identities and the parameter optimization; they do not prove abc or actual rational realization.

- `check.py` checks 3,133 exact rational fixtures, both signs, zero terms, unrelated denominators, nontrivial square gcds and denominator cancellation.
- `check_criteria.py` reconstructs every contraction, the exact scalar-argument degrees, and the complete smaller-degree exclusions with exact rational arithmetic.
- `independent_criteria.py` checks the optimization through separate integer inequalities, allowing every integer inner exponent and every even outer exponent in the admissible range.

Each checker accepts `--output PATH`; the repository verifier writes temporary certificates and compares them byte-for-byte with the distributed files.

The ordinary-abc scalar-argument degrees are **48** for fixed classes and **60** for the class menu with support budget two. They are not degrees of a complete defining polynomial. Actual source realization remains unproved; the established defining counts remain **25 and 13**.
