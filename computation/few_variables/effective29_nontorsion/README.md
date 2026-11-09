# An explicit polynomial in 29 variables

This module specifies an integer polynomial in **29 total variables**, including the input, with **degree less than `2^161`** and **coefficient height at most `2^(2^171)`**. Under exactly the four arithmetic inputs identified in the accompanying paper, its rational input projection is the set of integers.

The coefficient exponent is the fixed explicit value `L=137731`. The effective height comparison proves that this exponent is sufficient. The polynomial is specified by exact integer coefficient graphs, finite algebras, determinants, resultants, traces, and finite products. Matrix coordinates, algebra generators, and finite selectors in those operations are bound formal quantities, not additional quantified variables.

## Construction

The source retains the input, 18 components of nine elliptic points, one comparison slope, and two parameters for each of four poles: 28 rational coordinates. Nine monic quartic point roots and four monic quadratic pole roots are replaced by one rational coordinate. The finite-algebra rank is `2^22`.

The inherited pole realization constructs elliptic points outside the two-torsion subgroup. It therefore supplies nonzero `p` and `q`. Every first pole conic is represented by the single chart

```text
e = (tau^2 - B)/(tau^2 + 3*B)
p = -4*B*tau/(tau^2 + 3*B).
```

Every quadratic pole root is guarded nonzero, and no quadratic zero stratum is required. This strengthened source preserves the denominator obstruction and completeness for all admissible pole inputs. Its nonzero-witness proof uses the same inherited arithmetic hypotheses.

Four factors per point chart are automatically nonzero and are omitted from the materialized guard. All remaining denominators stay guarded. The comparison scales are `1`, `S0^2`, and `(S0+S1)^2`, where `S0+S1*sqrt(2)` is the sum of the four root-point abscissas. The effective height theorem and fixed scalar exponent are unchanged.

The exact degree and logarithmic coefficient-height majorants are

```text
degree <= 2021432499262561030580590567538985948904131919872 < 2^161
log2(height) <= 1824327990117465218468581252398965551307997696753664 < 2^171.
```

These are upper bounds; the expanded polynomial is not asserted to attain them.

## Reproduction

Only Python's standard library is required:

```sh
python3 reproduce.py
```

The command rebuilds the source, independently checks its identities and arithmetic profile, compiles the polynomial, independently checks all coefficient conversions and bounds, and compares the two specifications byte for byte with `certificate/`. Add `--output DIRECTORY` to retain a new reconstruction.

The source contains 7,944 coefficient nodes; the compiled graph contains 3,243. Checks cover nine quartic charts, four rational-square clearings, the single quadratic stratum and conic-chart choice, 114 atomic source guards, 36 automatic point factors, and all 76,249 residue classes for the scalar normalizer. The sufficient cutoff inequalities are checked by exact integer arithmetic.

## Files

| File | Role |
|---|---|
| `build_forced_prime_source.py` | Exact source construction |
| `check_forced_prime_source.py` | Independent source and cutoff checks |
| `check_direct_points.py` | Independent chart identities and automatic guard checks |
| `compile_source.py` | Complete integer polynomial specification |
| `verify_specification.py` | Independent conversion, finite-case, guard, and bound audit |
| `reproduce.py` | Full reconstruction and byte comparison |
| `certificate/` | Exact source, polynomial specification, reports, and reproduction transcript |

The scripts verify the algebraic specification and exact numerical bounds. Identification of its rational projection with the integers additionally uses the four stated arithmetic inputs; no computation is presented as a proof of those deep inputs.
