# Common-twist applications

The exact checker verifies witness substitutions, two pairs of prepared inputs,
all required square classes and quadratic residue symbols, and the curve
isomorphism for a change of base square class. The second pair has overlapping
complements with common prime 89. The existing finite-family theorem is retained
as an explicit input, not proved by these finite checks.

```sh
python -B computation/pole_parameters/common_twists_v30/check.py
```

The mathematical proof is in `papers/pole_parameters/common_twists_20261114_v30.tex`.
The supplied row-5a audit is preserved unchanged in `sources/hexagon` and bound
by its SHA-256 digest. The published two-twist theorem of Jaswal and the supplied
finite-family strengthening are attributed separately.

The count is three retained pole parameters instead of four for two inputs on
the stated compatibility locus. It is **not** a new twelve-variable definition
of the integers. No explicit numerical common twist or full pole witness for
the displayed pairs is claimed to have been computed.
