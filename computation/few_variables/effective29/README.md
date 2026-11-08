# An explicit polynomial in 29 variables

This directory specifies an integer polynomial whose rational input projection is the integers, conditional on the four arithmetic inputs stated in the companion paper, [explicit29_effective_20261108_v10.tex](../../../papers/few_variables/explicit29_effective_20261108_v10.tex).

The polynomial has **29 total variables**, including its input. Its degree is less than **2^166**, and its coefficient height is at most **2^(2^175)**. The fixed coefficient exponent is **L = 137731**, which meets the proved effective cutoff. No ineffective constant enters this specification.

The construction uses nine direct elliptic point charts, three comparison scales `1`, `S0^2`, and `(S0+S1)^2`, and one scalar pole. Here `S0 + S1*sqrt(2)` is the sum of the four root-point abscissas. The effective elliptic sum-height theorem proves the necessary height estimate. The source retains 28 rational coordinates; the finite-algebra construction replaces its thirteen finite roots by one further rational coordinate.

## Reproduce

Only the Python standard library is needed. Run:

```sh
python3 reproduce.py
```

This rebuilds the source and polynomial specification, runs both independent verifiers, and compares the two generated specifications byte for byte with the packaged certificate. To retain a new reconstruction, use:

```sh
python3 reproduce.py --output /absolute/path/to/new-directory
```

The default exponent is the certified value `137731`. A larger fixed odd exponent can be supplied with `--anchor-exponent`; it remains a coefficient choice and adds no variable. The displayed coefficient-height bound and packaged certificate concern the default exponent.

## Exact specification

The `certificate` directory contains:

| File | Contents |
| --- | --- |
| `source.json.gz` | The guarded rational source, all coefficient nodes, finite roots, pole charts, and scalar normalization. |
| `polynomial-specification.json` | The integer coefficient graph and exact finite determinant, trace, resultant, and product formula. |
| `source-verification.json` | Independent source identities, finite-field avoidance, and fixed-exponent cutoff checks. |
| `verification.json` | Independent finite-algebra conversion, guard coverage, finite cases, and degree/coefficient bounds. |
| `construction-report.json` | Size data and specification hashes. |
| `reproduction.json` | Results of the complete reconstruction. |
| `reproduction-transcript.txt` | The commands and their verification output. |

The representation is exact. It does not expand the enormous final polynomial into a monomial list. Its formal matrix entries and finite-algebra generators are bound by the specification, not additional quantified variables.

## Arithmetic assumptions and verification scope

The defining-set assertion uses precisely the stated elliptic group and index-height input, the exponent-nineteen contact-height input, preparation-zero pole completeness, and the simultaneous prime-pattern input. Their exact scope is recorded in the accompanying arithmetic dependency paper. The effective sum-height argument and the direct square-root chart introduce no additional arithmetic assumption.

`check_forced_prime_source.py` imports no source producer. It verifies the changed expressions by independent polynomial expansion and binds unchanged arithmetic methods to recorded canonical syntax hashes. `verify_specification.py` imports no polynomial producer. It reconstructs each coefficient substitution and recomputes the complete degree and coefficient majorants independently.

The checks include nine point quartics, four rational-square clearings, all sixteen quadratic-support cases, all sixteen conic-chart cases, and 110 atomic source guards. Exactly 36 point-chart factors are omitted from the localization product after independent identity checks and the proved nonvanishing theorem. Other denominator guards remain in place. The normalizer is checked at all 76,249 residue classes; the cutoff is checked with exact integer arithmetic.

The programs verify the algebra and numerical certificates. The mathematical proofs establish the nonvanishing, height estimates, and the implication from the four arithmetic inputs to the defining-set assertion.
