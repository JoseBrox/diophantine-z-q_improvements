# A 78-variable quartic under ordinary rational abc

The source retains the group, fixed-data prime-pattern, and prepared pole
realization premises of the corrected 79-variable construction. It removes
`inputComparison.real`, reuses the two height coordinates for X^2 and X^4,
compares the elliptic index with X^2+3, and uses the additive scale
B+X^8+T^2. Every sufficiently large fixed odd B defines the integers under
those premises. B=81 is not a certified defining member.

Run from the repository root:

```sh
python -B computation/quartic/abc78_v34/build.py
python -B computation/quartic/abc78_v34/check.py
```

The checker does not import the producer. It authenticates the parent files,
reconstructs every unchanged and changed row, expands every quartic
coefficient, checks parameter profiles and deliberate corruptions, and
repeats the build in an isolated directory. SymPy is used only for exact
factorization in the height examples. The construction itself uses the
Python standard library.

The full proof is `papers/quartic_existence/quartic_abc78_20261115_v34.tex`.
No independent audit of the inherited arithmetic inputs is asserted.
