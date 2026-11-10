# Twenty-five variables with raw comparison functions

This directory specifies the family proved in
[`few_variables25_merged_20261110_v19.tex`](../../../papers/few_variables25/few_variables25_merged_20261110_v19.tex).
Every sufficiently large fixed odd coefficient parameter `L` defines the integers over the rationals under the paper's stated inherited arithmetic inputs. The sufficient threshold is ineffective because of the aggregate trace-height theorem. **The supplied `L=3` fixture is not certified to define the integers.** No additional abc hypothesis is used.

The source retains 24 rational coordinates: the input, 18 coordinates for nine elliptic points, one nonzero slope, and four pole parameters. Nine quartic point generators and two nonzero quadratic pole generators belong to a finite coefficient algebra. The separating-element construction removes them with one additional rational coordinate. The final polynomial therefore has **25 total variables**, including the input.

The two comparison products use the ten raw reciprocal abscissas at denominator order one and six raw ratio/residual functions at denominator order three. The six rational scalar components use `Phi_R(D)=R*D/(1+R*D)`, with numerator factor `R^3` and denominator order three. Formal-logarithm precision four means the plain local parameter `z=-x/y`. Completeness additionally chooses the common elliptic index divisible by each selected comparison prime. The clustered-prime and Hasse arguments prove that these extra congruences are compatible with all prescribed reduction orders.

## Certified bounds

| Quantity | Certified value |
|---|---:|
| Total polynomial variables | 25 |
| Uniform total degree upper bound | 24072202920766797054476288, less than 2^85 |
| Uniform support upper bound | less than 2^1984 |
| Rational source coefficient nodes | 5860 |
| Integer source coefficient nodes | 2239 |
| Atomic guard factors | 136 |
| Finite-algebra rank | 2^20 |
| Finite product factors | 262144 |

The degree and support bounds hold uniformly for every fixed odd `L`. The support bound is not an expanded monomial count. Coefficient estimates for the numerical fixture apply only to that fixture and do not certify the ineffective defining member.

## Files and verification

`certificate/source.json.gz` is the guarded rational source. `certificate/source-polynomial-specification.json` is its exact integer finite-algebra specification. `active25/polynomial-specification.json` specifies the final polynomial by finite integer operations and determinants, without materializing the rank-sized matrices or expanded polynomial.

`check_merged_source.py` independently checks the exact affine source-to-integer conversion, point quartics, square clearings, automatic guards, and variable census. It also reconstructs every new rational expression over 15 finite-field samples without importing the producer's arithmetic. Those samples are finite evidence for the formula translation; the universal arithmetic theorem is proved in the paper.

`check_merged_bounds.py` verifies the weighted-degree and operator-norm recurrences and literally sums every active-algebra factor. It additionally treats the two powers of the fixed prime as independent coefficient symbols of degree zero to certify uniformity in `L`.

`check_local_profile.py` checks rational normalization examples, exact integer-rounding inequalities, the Hasse clustering polynomial identity, and the complete exceptional-prime sets for both the two-detector and three-detector constructions. These exact finite checks supplement the local proofs and do not replace them.

From the repository root, using only the Python standard library:

```sh
python computation/few_variables/merged25_v19/build_merged_source.py --anchor-exponent 3 --output computation/few_variables/merged25_v19/certificate
python computation/few_variables/active_elimination/build_active_specification.py computation/few_variables/merged25_v19/certificate/source-polynomial-specification.json computation/few_variables/merged25_v19/active25
python computation/few_variables/merged25_v19/check_merged_source.py computation/few_variables/merged25_v19/certificate --output computation/few_variables/merged25_v19/independent-source-verification.json
python computation/few_variables/merged25_v19/check_merged_bounds.py --output computation/few_variables/merged25_v19/independent-bound-verification.json
python computation/few_variables/merged25_v19/check_local_profile.py --output computation/few_variables/merged25_v19/local-profile-verification.json
```
