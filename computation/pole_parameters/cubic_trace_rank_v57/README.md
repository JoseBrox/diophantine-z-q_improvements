# Cubic trace rank certificate

The exact data certify the torsion specializations of the section
`P=(49,336)` on `y²=x³−(2+24w)x²+(1+1176w)x`.

Run `python -B check.py` to reconstruct the division recurrences and verify
all quotient, factor, projective residue and surviving torsion-order checks
using only standard-library rational arithmetic. `division_data.json` is
immutable input to this verifier. `generate_data.py` reproduces it using
SymPy 1.14.0.

Run `python -B independent_check.py` for a separate tangent-and-chord
calculation of the abscissa denominators of the multiples 8, 10 and 12.
Both checkers accept `--output PATH` for their deterministic receipts.

The universal deduction uses Mazur's torsion classification and the stated
division-polynomial vanishing theorem. The manuscript supplies the real
and finite-place approximation argument. No actual detector trace matching
or new defining-polynomial variable count is claimed.
