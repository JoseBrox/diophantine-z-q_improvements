# Degree-eight input polynomial and norm-compatible scalar

The [manuscript](../../../papers/pole_parameters/norm_compatible_scalar_20261116_v47.tex)
proves the source transfer and both bare norm-conic assertions under the
retained arithmetic premises. The input polynomial reflects integrality;
the scalar is an explicit norm from `Q(sqrt(10657))` and retains the required
odd valuation at 76249 and the local preparation at 2, 3 and 17.

`check.py` uses standard-library exact arithmetic for the constants,
polynomial identities, denominator cases, source hashes and congruences.
`independent-check.py` reconstructs the constants and valuation checks using
SymPy without importing the first checker. Both accept `--output`.

The source keeps 25 total coordinates. Matching the actual prescribed
detector traces is unproved; no smaller defining count or new degree bound
for the resulting defining polynomial is assigned.

```sh
python -B scripts/verify_v47.py
```
