# A computable family in 27 variables

This module specifies integer polynomials `F_L` in **27 total variables**, including the input, with **degree less than `2^154`**. The fixed odd integer `L >= 3` is a coefficient parameter.

Under the four arithmetic inputs stated in the accompanying paper, every sufficiently large odd `L` defines the integers over the rationals. The proof uses an ineffective additive height constant. **No numerical sufficient threshold is known.** Reconstructing a numerical member does not certify that it defines the integers.

## Construction

The source retains the input, 18 rational components of nine elliptic points, one comparison slope, and two parameters for each of three poles: 26 rational coordinates in total. Nine monic quartic point roots and three monic quadratic pole roots are replaced by one rational coordinate using the guarded finite-algebra theorem. The finite algebra has rank `2^21`.

The inherited simultaneous-realization proof constructs elliptic points outside the two-torsion subgroup. Their ordinates are nonzero, so all pole certificates can be chosen with `p != 0` and `q != 0`. The first conic therefore needs only

```text
e = (tau^2 - B)/(tau^2 + 3*B)
p = -4*B*tau/(tau^2 + 3*B).
```

Every pole quadratic generator is guarded nonzero. There is one conic-chart choice and one quadratic-stratum choice. The strengthened predicate retains both properties used by the arithmetic proof: its denominator obstruction and completeness for every admissible pole input. The construction does not assert equivalence of the strengthened and original pole predicates for all rational inputs.

Four factors for each point chart are automatically nonzero at every rational retained base and are omitted from the materialized guard. All other denominators remain guarded.

The exact uniform degree majorant is

```text
20373348814943897785292785017798269643599642624 < 2^154.
```

The polynomial is specified completely by integer coefficient graphs, finite algebras, determinants, resultants, traces, and finite products. Their formal generators and finite selectors are not quantified variables.

## Reproduction

Only Python's standard library is required. Run

```sh
python3 reproduce.py --anchor-exponent 137731
```

This reconstructs the packaged numerical member, checks the source and polynomial specification independently, and proves the degree bound uniformly by treating the two fixed prime powers as independent coefficient symbols of degree zero. An optional `--output DIRECTORY` retains a reconstruction.

The numerical example at `L=137731` has 7,369 source coefficient nodes and 3,032 compiled coefficient nodes. The independent checks cover nine point quartics, three rational-square clearings, 104 atomic source guards, the 36 automatic point factors, the single quadratic stratum, and every finite-product and coefficient-bound operation. The scalar normalizer is checked at all 76,249 residue classes.

For this numerical example the coefficient height is at most `2^(2^165)`. This is **not** a coefficient-height bound for a member certified to define the integers. The proved defining-polynomial result is the eventual-existence theorem with a uniform degree bound.

## Files

| File | Role |
|---|---|
| `build_forced_prime_source.py` | Exact source builder |
| `check_forced_prime_source.py` | Independent source identities, inventory, arithmetic profile, and inherited-code audit |
| `check_direct_points.py` | Independent polynomial verification of the nine point charts |
| `compile_source.py` | Complete finite-algebra polynomial specification |
| `verify_specification.py` | Independent coefficient conversion, guard, case, and bound checks |
| `verify_family_degree.py` | Uniform degree audit with formal coefficient symbols |
| `reproduce.py` | End-to-end reconstruction and byte comparison |
| `example_L137731/` | Numerical example with explicit theorem-status metadata |

The scripts verify the algebraic specification and its bounds. The arithmetic inputs and the nonzero-witness argument are stated and proved, with their precise dependencies, in the accompanying papers.
