# Exact monomial coordinate eliminations

`build.py` constructs family196 from the uploaded 198-variable source.
`build_explicit.py` constructs the successive 259- and 258-variable tables
from the retained explicit260 source. Neither production script uses an
optimization solver. All exponent vectors are frozen in the JSON inputs.

`check.py` and `check_explicit.py` do not import the producer. They verify
literal unit guards, every Laurent polynomial identity, exact inverse-map
accounting, every coefficient, all-parameter heights, and corrupted controls.
They regenerate all output files in temporary directories byte for byte.

The full mathematical proof is
`papers/quartic/laurent_elimination_20261115_v38.tex`, with its explicit
exponent appendix. All parent arithmetic premises and sufficient defining
parameters are preserved. The original source proofs are retained separately.
