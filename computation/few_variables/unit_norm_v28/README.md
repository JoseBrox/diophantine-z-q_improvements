# General constructions by a single norm determinant

The complete proof is `papers/finite_algebra/unit_norm_20261114_v28.tex`.
Every variable count includes the input. No smaller variable count is asserted.

| Source | Variables | Degree upper bound | Parameter status |
|:--|--:|--:|:--|
| General inherited-premise family | 25 | 64674204453175296 < 2^56 | Sufficient odd L ineffective |
| Fully specified inherited-premise family | 27 | 442502070853959680 < 2^59 | L=20483 remains certified |
| Weak abc at 121/100 | 13 | 155568385 < 2^28 | Sufficient odd B ineffective |
| Weak abc at 16/15 | 13 | 126445825 < 2^27 | Sufficient odd B ineffective |

At L=20483 the 27-variable coefficient height is below 2^(2^72).
The other stored coefficient bounds apply only to L=3 or B=3 fixtures, not
certified defining polynomials. The general degree bounds are uniform in the
permitted fixed parameters. The arithmetic premises are inherited and their
complete independent audit is not claimed.

`build_sources.py` gives the complete guarded rational sources using the
four-dimensional point basis 1,U,V,W. These are four basis elements, not three
independent quadratic generators. `build.py` produces the finite integer
polynomial specifications: all guards and square extractions, the scalar norm
that excludes vanishing conjugate denominators, the separating element, and
the determinant. Production matrices of rank up to 2097152 are specified but
not materialized or expanded.

The additional completeness argument is essential: a base tuple with any
vanishing conjugate guard is excluded, even if another character is valid.
The proof establishes an admissible tuple for every required integer input;
it does not assert equivalence on all old retained base tuples.

From the repository root:

```sh
python -B scripts/verify_v28.py
python -B computation/few_variables/unit_norm_v28/build.py --output /tmp/v28 --native-sources
```

The separate checker proves the point multiplication, primitive polynomial and
discriminant, homogeneous difference and pole-rescaling identities exactly.
It independently checks every factor certificate and bound. Three complete
rank-eight separator examples, partially vanishing and nilpotent guard cases,
fourteen parameter fixtures and 180 finite-field reconstructions test the
implementation. These finite examples do not establish the arithmetic inputs.
Altered degree bounds and radicand signs, a corrupted point table, an incorrect
pole rescaling, a nonseparating element and omission of the norm guard are
separately tested. `inputs.json` authenticates the source dependencies.
