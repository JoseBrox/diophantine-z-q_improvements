# Exact anchor replacement: verified packages

Both packages preserve the rational projection of their respective parents. The semantic replacement is the proved semilocal quaternion lemma; the computer checks its exact placement, all incidence conditions, and the complete resulting coefficient table. The source arithmetic characterization of the integers retains the upstream manuscript's proof status.

| Package | Total variables | Witnesses | Degree | Residuals | Monomials | Coefficient bound |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [quartic-anchor-packed](quartic-anchor-packed/README.md) | 12,493 | 12,492 | 4 | 11,936 | 135,667 | < 2^80 |
| [quartic-anchor-packed-large](quartic-anchor-packed-large/README.md) | 12,465 | 12,464 | 4 | 11,908 | 130,427 | < 2^3247 |

The first package saves eleven variables at the released coefficient bound. The second includes the independently checked 28 eliminations and 13 invertible row operations of the large-coefficient variant and then saves eleven more variables.

## Verified scope

The checker replays the released baseline certificate, matches all six anchor equations exactly, checks that the sixteen deleted variables occur nowhere else, establishes that the retained constant C is nonzero from its actual defining chain, checks the three replacement quadratics and their five fresh variables, and expands all ordered products independently. Every displayed variable occurs in the resulting polynomial. No source file in the released quartic was modified.

The full table SHA-256 values are:

- `quartic-anchor-packed`: `06c2eeb37871341588f232d72eee72a49b8a76a2c904dc8465518d280f3378a9`.
- `quartic-anchor-packed-large`: `de8e8080587ef83e19653e3545a1c15805526ac847547c66dc6cc21dd1bc466c`.

## Reproduce

From the repository root:

```sh
python3 -E -B research/optimization/quartic-anchor-packed/verify_anchor.py research/optimization/quartic-anchor-packed --baseline quartics/quartic-12504
python3 -E -B research/optimization/quartic-anchor-packed-large/verify_anchor.py research/optimization/quartic-anchor-packed-large --baseline quartics/quartic-12504
```

`pack_anchor.py` is the producer; `verify_anchor.py` imports no producer code. The copied parent certificates allow the large-coefficient suffix to be replayed even after its temporary build directory is removed. The baseline package remains a required pinned input for the earlier certificate replay.

No commits or pull requests have been made.
