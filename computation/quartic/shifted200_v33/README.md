# Corrected 200-variable quartic

All counts include the input. `build.py` reconstructs the unbalanced family
from the immutable 204-variable source. `check.py` reconstructs every changed
and retained equation independently and expands every quartic coefficient.
`check_normalization.py` separately checks the physical scalar ratios.
`balance.py` applies the invertible diagonal coordinate map; `check_balance.py`
independently reconstructs that map and certifies exact height and support for
all positive parameters, without sampling.

The previous unpublished v32 formula subtracted 2 from a stored ratio that
is R times the physical ratio. The correct shift subtracts 2R. The older
checker repeated the same error. Its tables are superseded, not certified by
this release. The new scalar-normalization check deliberately rejects it.

The family has 200 variables, 186 quadratic rows, exact degree four, content
one and exactly 3221 monomials. The sufficient defining exponent remains
ineffective. The coefficient condition N>=57 does not certify a defining
member. Arithmetic implications retain the source premises; finite checks
are not an independent audit of them.

Run `python -B scripts/verify_v33.py` from the repository root. It regenerates
all new data in a temporary directory and compares deterministic bytes.
