# Bounded native complement levels

The associated theorem replaces constant complement levels by fixed rational
functions of the actual detector norm. The canonical multiplier is
`m = Norm(W) / (1 + Norm(W))`, with level `17*m^2`.

At every odd valuation of the physical weight, this multiplier is a local unit.
The proof includes both signs of that valuation and the general and conditional
sources. The additional denominator and complement are units at all characters
of a prepared actual point algebra. A simultaneous rational realization theorem
would give 21/9 variables without adding a retained parameter; it remains unproved.

Run from the repository root with Python 3.12 and SymPy 1.14.0:

```sh
python -B computation/pole_parameters/bounded_norm_levels_v48/check.py
```

Use `--output PATH` to reconstruct the deterministic `certificate.json` in a
chosen temporary file. The symbolic checks verify the native factor presentation,
complement/norm witness substitutions, Cayley quadric and real-bound identities.
The residue enumeration and valuation screens supplement the universal proofs.
The small rational identity fixtures are explicitly not asserted to be native
elliptic realizations. No established variable count changes.

Paper:
[Bounded complement levels from native detector norms](../../../papers/pole_parameters/bounded_norm_levels_20261116_v48.tex).
