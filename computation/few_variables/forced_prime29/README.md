# A polynomial in 29 variables

This directory gives a complete finite expression for an integer polynomial
\(F(X,Y_1,\ldots,Y_{28})\) whose rational zero set projects to the integers,
under the four arithmetic inputs identified in the accompanying paper.
The variable count is **29 in total, including the distinguished input**.
The proved bounds are

\[
\deg F\le 2^{174},\qquad
\max|\operatorname{coeff}(F)|\le 2^{2^{177}}.
\]

The scalar contact uses the fixed prime 76249 and forces the necessary
elliptic-index size. There is no finite exclusion over elliptic multiples.
The expression is specified by an integer coefficient graph, finite
algebra relations, and bounded determinant, trace, resultant and product
operations. These operations define one polynomial exactly; its monomial
expansion is not stored.

## Reproduction

Run from any working directory with Python 3.10 or newer:

```sh
python path/to/this/directory/reproduce.py
```

Only the Python standard library is used. No network, computer-algebra
system, earlier release or external source directory is required.

The command regenerates the rational source and final polynomial
specification. It then checks the source identities and finite arithmetic,
recomputes the explicit contact-height constant, and independently checks
the complete source-to-polynomial conversion and coefficient bounds.

## Files

| File | Purpose |
|---|---|
| `source.json.gz` | Complete guarded rational source, coefficient graph and finite choices. |
| `polynomial-specification.json` | Exact one-polynomial expression, finite-algebra recipe and integer majorants. |
| `build_forced_prime_source.py` | Deterministic source producer. |
| `compile_source.py` | Exact finite-algebra compiler. |
| `check_forced_prime_source.py` | Independent contact-identity, inventory, semantic-preservation and integer checker. |
| `verify_specification.py` | Independent affine-substitution, guard, finite-case and bound checker. |
| `verify_explicit_height_constant.py` | Independent trial-division evaluation of the stated height constant. |
| `source-verification.json`, `verification.json`, `explicit-height-constant-verification.json` | Machine-readable results of the three checkers. |
| `construction-report.json` | Variable count, degree and coefficient bounds, and specification hashes. |
| `source-semantic-reference.json`, `provenance.json` | Bindings to the reviewed arithmetic routines and the exact changed formula. |
| `field_circuit.py`, `finite_algebra_core.py`, `finite_algebra_check_core.py` | Exact arithmetic and independent checking utilities. |
| `coefficient-bound-equality.json`, `verify_bound_equality.py` | Certificate and independent check that the improved coefficient bound describes the same polynomial. |
| `manifest.json` | Complete portable file inventory and checksums. |

## Mathematical scope

The source proof uses four identified inputs: the normalized elliptic
group and index-height result, the contact-height theorem, the pole theorem,
and Sun's simultaneous prime-pattern theorem. The dependency argument
checks the precise quantified statements required, including arbitrary
fixed avoidance and zero preparation. The proof incorporates the corrected
Kato index-set and retained-class identification in the cited source.

The source normalization, the forced-prime bound, the Lucas estimate,
the simultaneous reduction, and the finite-algebra elimination are proved
in the paper. The computational checks verify exact identities and the
specified finite expression. They do not claim to verify the deep source
theorems by finite testing.
