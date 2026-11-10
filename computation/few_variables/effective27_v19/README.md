# An explicit polynomial in twenty-seven variables

This directory specifies the polynomial proved in
[`explicit27_20261110_v19.tex`](../../../papers/few_variables27/explicit27_20261110_v19.tex).
Under the paper's stated modular-realization, elliptic-group, pole-realization, and simultaneous prime-pattern inputs, the fixed odd coefficient exponent **L=125001** gives a Diophantine definition of the integers over the rationals. No additional abc hypothesis is used. The effective sum-height estimate provides the numerical threshold; no ineffective aggregate trace constant is used for this branch.

The source has 26 retained rational coordinates: the input, 18 coordinates for nine elliptic points, one nonzero slope, and six pole parameters. Nine quartic point generators and three nonzero quadratic pole generators belong to a finite coefficient algebra of rank 2^21. One additional separating coordinate eliminates these finite generators. The final polynomial has **27 total variables**, including the input.

Write the sum of the four root abscissas as `S0+S1*sqrt(2)` and let `rho` be the scalar contact coefficient. The three scales are

```text
1, (1+rho*S0^2)^2, (1+rho*(S0+S1)^2)^2.
```

Each detector has two disjoint translated five-contact blocks. The ten raw reciprocal-abscissa tests and two input comparisons use denominator order one. The three Lucas-label comparisons and the Lucas residual use order three. The scalar components use linear normalization `Phi_R(D)=R*D/(1+R*D)`, with numerator factor and denominator order one for the first four components and three for the last two. The same additional common-index divisibility used in the 25-variable source gives completeness.

## Certified bounds

| Quantity | Certified value |
|---|---:|
| Total polynomial variables | 27 |
| Fixed coefficient exponent | 125001 |
| Total degree upper bound | 85829362869408651982929920, less than 2^87 |
| Support upper bound | less than 2^2192 |
| Coefficient height upper bound | less than 2^(2^102) |
| Binary logarithmic coefficient-norm bound | 3593722961921650418383728672749 |
| Rational source coefficient nodes | 6898 |
| Integer source coefficient nodes | 2588 |
| Atomic guard factors | 164 |
| Finite product factors | 262144 |

These are upper bounds for the unexpanded determinant polynomial. The exact monomial count and exact degree are not asserted. The complete polynomial is specified by finite integer coefficient operations, determinants, and products with explicit ranges.

## Reproduction

From the repository root, using the Python standard library:

```sh
python computation/few_variables/effective27_v19/build_effective_source.py --anchor-exponent 125001 --output computation/few_variables/effective27_v19/certificate
python computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/effective27_v19/certificate/source-polynomial-specification.json computation/few_variables/effective27_v19/active27
python computation/few_variables/effective27_v19/check_effective_source.py computation/few_variables/effective27_v19/certificate --output computation/few_variables/effective27_v19/independent-source-verification.json
python computation/few_variables/effective27_v19/check_effective_bounds.py --output computation/few_variables/effective27_v19/independent-bound-verification.json
python computation/few_variables/effective27_v19/check_effective27_constants.py
```

`check_effective_source.py` proves the source-to-integer conversion, point quartics, square clearings, and guard coverage exactly. Its 15 independent finite-field formula reconstructions are bounded supplementary evidence; the arithmetic projection theorem is proved in the paper. `check_effective_bounds.py` independently verifies the matrix bounds and literally sums all 262144 finite-product cases. It additionally certifies degree uniformity in the fixed exponent by treating the powers of 76249 as independent coefficient symbols of degree zero. `check_effective27_constants.py` separately certifies the numerical constants and inequalities in the effective soundness proof.

The valuation-profile and complete exceptional-prime checks shared with the 25-variable source are in `../merged25_v19/check_local_profile.py`. They verify the five extra exceptional primes, their product below 2^100, and exclusion of the forced prime 76249.
