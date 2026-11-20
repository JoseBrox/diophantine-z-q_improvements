# Fully expanded ASCII polynomials and Busy Beaver coefficient family

This new package does not change the published v81/v82 source
polynomials, manuscripts, hypotheses, or their verification receipts.
All expansions use one line without whitespace or trailing newline,
`x1` as the rational input, and `x2` through `xm` as auxiliaries.
A kilobyte is exactly 1,000 ASCII bytes.

| Artifact | What it represents | Bytes |
|---|---|---:|
| [quartic163-N1.txt](quartic163-N1.txt) | Complete 163-variable \(N=1\) decimal fixture; **not certified defining** | 60,907 |
| [quartic179.txt](quartic179.txt) | Complete 179-variable decimal polynomial with certified defining coefficients | 66,905 |
| [quartic56-B3.txt](quartic56-B3.txt) | Complete 56-variable \(B=3\) decimal fixture; **not certified defining** | 11,564 |
| [quartic163-BB_t-symbolic.txt](quartic163-BB_t-symbolic.txt) | Complete monomial expansion with three symbolic \(149^{2BB(t)}\), \(149^{4BB(t)}\) coefficients, **not decimal** | 60,931 |

The defining 163-variable statement is valid for **all sufficiently
large Busy Beaver indices**, with an **unknown threshold**. A
particular fixed index (including \(2^{1000}\)) has not been certified.
See [the proof and exact size formula](../../docs/busy_beaver_and_expanded_sizes_20261120_v84.md)
and [structured size report](size_report.json).

The [producer](build.py) is read-only by default. To regenerate
all four TXT files into an independent directory:

```sh
python -B computation/expanded_text_v84/build.py --output /tmp/expanded-v84
python -B scripts/verify_v84.py
```

The verifier has a separate decimal-polynomial parser and
cross-checks every monomial and integer coefficient against the
immutable published coefficient tables. The unrestricted-degree
file-size bounds in the main README are very loose, fixture-only
bounds; those large determinant polynomials have not been expanded.
