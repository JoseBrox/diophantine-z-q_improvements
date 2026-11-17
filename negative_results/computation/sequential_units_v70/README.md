# Sequential six-unit detector obstruction

**Proved result.** The specified two-detector factor design cannot be made
quadratic by integer diagonal Laurent changes and monomial row division on
any of the **2834 distinct six-unit bases** defined below. A standard-library
checker reconstructs the complete finite enumeration and the exact
two-detector contradiction. The proof is independent of the supplementary
SMT runs.

This is an obstruction for a particular factor design and unit family. It
does not give a lower bound for arbitrary quartics, arbitrary geometric
charts, or general Diophantine definitions. No new quartic with fewer than
195 variables is produced by this package.

## Unit family and guards

The physical contact weights are `q0=u` and **`q1=u*v`**. Start with four
unit coordinates

```math
u,\quad u^{-1},\quad v,\quad z=u^s/v,\qquad -2\le s\le2.
```

Their guards are `u*u_inverse=1` and `v*z=u^s`. The latter uses a square of
`u` or `u_inverse` when `s=2` or `s=-2`, so it remains quadratic. Include
the zero exponent for the constant 1. Add two new, distinct unit exponents
sequentially: each belongs to `P+P-P` for the exponent set then available.
An exponent `e=a+b-c` has quadratic definition `U_e*U_c=U_a*U_b`.
The guards make the denominator coordinate nonzero, so each extension is
unique and invertible on the original unit domain.

| Initial `s` | Ordered extension choices | Distinct bases at that `s` | Single-comparison survivors |
|---:|---:|---:|---:|
| -2 | 1140 | 762 | 0 |
| -1 | 868 | 592 | 0 |
| 0 | 648 | 458 | 2 |
| 1 | 868 | 592 | 0 |
| 2 | 1140 | 762 | 0 |
| Total | 4664 | 3166 | 2 |

There are **2834 globally distinct final bases**, after duplicates between
different initial `s` are removed. The subfamily `s=-1,0,1` has 2384 ordered
choices, 1642 distinct `(s,basis)` pairs and 1557 globally distinct bases.

The two surviving exponent sets have `s=0`, first new coordinate `v^-3`
and second new coordinate `u^-1*v^-6` or `u*v^-6`. Their defining equations
are, respectively,

```math
vY=(v^{-1})^2,\qquad uZ=Y^2,
```

and

```math
vY=(v^{-1})^2,\qquad u^{-1}Z=Y^2.
```

## Factor design and exact contradiction

Each detector has four regular factors with constant term 1, two quadratic
test slots, and additional separate linear terms. Four comparison fourth
powers and four raw reciprocal squares are assigned bijectively to the
eight quadratic slots, independently in each detector. The stored comparison
fourth powers have profile `u^-6*J_i^2`; the raw squares have profile `R_i^2`.

| Test type | First slot | Second slot |
|---|---|---|
| Comparison | `q_j^9*u^-6*J_i^2` | `q_j^11*u^-6*J_i^2` |
| Raw reciprocal | `q_j*R_i^2` | `q_j^3*R_i^2` |

All square blocks are separate field coordinates over `Q(sqrt(2))`, with
nonzero component coefficients. No displayed constant or square monomial
is cancelled. A full square forces its two component weights to agree,
and forces the real and imaginary factor-row multipliers to agree, even
if independent multipliers were initially allowed.

For one comparison with common coordinate weight `w`, the factor exponents
must be

```math
r_0=2w+(-6+p_0,0),\qquad r_1=2w+(-6+p_1,p_1),
\qquad p_0,p_1\in\{9,11\}.
```

The constant terms require `-r_j` to lie in `P+P`. Exact enumeration of
these necessary conditions leaves the two bases above. On either basis,
all four comparisons have a single common weight and use power 9 in
detector 1. Therefore all four raw tests use power 3 there, forcing every
raw test's `v` weight to be 3.

Two comparisons cannot share a factor in detector 0: their first-slot and
second-slot exponents would differ by `(2,0)`. Each factor consequently
pairs one comparison with one raw test. The comparison forces the factor's
`v` exponent to be 0, whereas the raw square forces it to be 6. This
contradiction excludes every quadratic-test assignment on both surviving
bases. It uses no chart or reference equations, special factors, product
chains, or linear-test assignments.

## Exact verification

```sh
python -B check.py --output certificate.json
```

`check.py` uses only the Python standard library. It reconstructs the
enumeration, all surviving comparison states, admissible unit definitions,
and both vector contradictions. It records hashes of the sorted finite
sets. The proof does not rely on an SMT `unsat` result or on floating-point
optimization. The polished statement and proof are in
[the manuscript](../../papers/quartic/sequential_unit_detector_obstruction_20261117_v70.tex).

## Supplementary 30-model search ledger

The two surviving bases were also tested against a complete retained support
model for each of the 15 choices of two square helpers among
`A1,B1,A3,B3,A4,B4`. All **30** runs returned `unsat`, with unbounded integer
weights. The total reported solver time is approximately 74.64 seconds;
timings are descriptive and machine-dependent. `runs.json` records every
model hash, helper choice, solver version, timeout, status and elapsed time.

The nominal storage accounting is

```math
195-42+36+4+1=194.
```

Three seven-field-coordinate point blocks are replaced by three six-field
blocks, two field square helpers add four rational coordinates, and the
five original rational unit coordinates are replaced by six. This is a
proposed storage count only; there is no completed 194-coordinate table.

For the optional full support search, the pinned prototypes are in
`computation/quartic/search194_v69/models`. They use the invertible
eight-dimensional reference row change and the corrected real-only
aggregate certified by that package. The present generator modifies only
the unit basis/guards and the two square-helper selections. No prototype
or full generated model is duplicated here. The physical factor output
unit exponents remain `(1,0)` and `(1,2)`.

The full models allow independent quadratic and linear test allocations
between detectors, with `C2` in the first regular factor in either slot.
They retain common row multipliers for new field equations and independent
multipliers for the retained literal rational rows. All model weights are
unbounded integers. The exact factor theorem above does not need the `C2`
position normalization or the other retained rows.

From the repository root, recreate and authenticate all 30 models with:

```sh
python -B negative_results/computation/sequential_units_v70/generate_models.py \
  --source-package computation/quartic/search194_v69 \
  --output /tmp/sequential-unit-models
```

Omitting `--output` verifies all 30 byte-exact model hashes without writing
the generated models. To repeat the optional SMT runs:

```sh
python -m pip install -r negative_results/computation/sequential_units_v70/requirements.txt
python -B negative_results/computation/sequential_units_v70/solve.py \
  --models-dir /tmp/sequential-unit-models --output /tmp/sequential-unit-rerun.json
```

The solver dependency is pinned to `z3-solver==5.4.1.0`. These runs concern
only their named support models. The standard-library factor certificate
is the mathematical result retained here.
