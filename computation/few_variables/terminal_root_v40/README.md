# A possibly singular final quadratic extension

The four finite specifications in `specifications/` retain the v30 integral
algebra, root envelopes, separator and variable counts. They remove the
nonzero condition on the final pole ordinate and exactly two large norm
factors from each scalar guard. Every source denominator and every preceding
quadratic radicand remains guarded. Original sources are unchanged.

The complete proof is
`papers/finite_algebra/terminal_quadratic_root_20261115_v40.tex`.
Its geometric-character descent permits nilpotents in the final quadratic
extension. The elementary pole obstruction permits a zero ordinate, so
soundness and the old sufficient coefficient parameters are retained.
The permitted retained-coordinate tuples need not equal the former ones.

| Source | Total variables | Total degree at most | Strict degree bound |
|:--|--:|--:|:--|
| Inherited-premise family | 25 | 5,059,009,872,658,432 | 2^53 |
| Specified inherited-premise member, L=20483 | 27 | 99,279,020,543,180,800 | 2^57 |
| Weak abc at 121/100 | 13 | 43,211,777 | 2^26 |
| Weak abc at 16/15 | 13 | 39,858,177 | 2^26 |

All counts include the input. These are bounds for unexpanded polynomials.
The explicit 27-variable member has coefficient height below `2^(2^70)`.
The other sufficient defining parameters remain ineffective; their small
stored parameters are reconstruction fixtures only. Support upper bounds are
respectively below `2^1193`, `2^1401`, `2^284`, and `2^283`.

Rebuild and check from the repository root:

```sh
python -B computation/few_variables/terminal_root_v40/build.py
python -B computation/few_variables/terminal_root_v40/check.py
```

The separate checker does not import the new producer. It checks the parent
specifications using their existing independent checker, then independently
derives the smaller support from the native circuits and checks every
denominator and numerical bound. Twenty corruption controls and eight exact
small finite-algebra examples include repeated eigenvalues from terminal
dual-number factors and the failure when a nonterminal radicand is zero.
The parent check requires SymPy 1.14.0; the producer uses the standard library.
These computations do not independently certify the inherited arithmetic
premises or establish smaller variable counts.
