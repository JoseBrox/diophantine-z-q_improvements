# Quartics from simultaneous valuation conditions

The complete coefficient tables specify two quartic families. Every variable count includes the input coordinate.

| Construction | Total variables | Degree | Quadratic rows | Nonzero monomials | Defining parameter |
|---|---:|---:|---:|---:|---|
| Aggregate trace | 301 | 4 | 275 | 4305 | Every sufficiently large integer `N`; the sufficient threshold is ineffective |
| Effective abscissa sum | 351 | 4 | 323 | 4990 | Every integer `N >= 27464`; the explicit member uses `A = 80989^54929` |

The projection assertions retain the arithmetic premises of the elliptic source construction, including its quantitative weighted prime-selection premise. Finite coefficient verification does not establish those arithmetic premises. The 301-variable theorem specifies a family and proves that sufficiently large members define the integers; it does not select a particular defining member.

## Mathematical construction

For weights `q_m = R^(1-2*m) * delta^(-2*m-2)`, the local factors are

`1 + sum_j q_(m_j)^(2^j) * D_j^(2^(j+1))`.

At a consumed prime, `v(R)` is odd and `delta` is a unit. A nonzero summand in position `j` has valuation exactly `2^j` times an odd integer. The summand valuations are therefore distinct and nonzero. The trace and pole argument forces each `D_j` to have its assigned order `m_j` at one common place. Different required orders can occur in the same factor.

The sixteen tests retain their orders `1, 10, 40`. Five or six factors use powers already present in the logarithm circuit, together with five or nine additional field squares. Placing all order-forty tests in position zero removes the stored square and cube of `q_40`. The scalar normalizer, rational logarithm approximants, point exclusions, and height inequalities are unchanged.

The results are documented separately:

- [Simultaneous valuation conditions and explicit quartics](../../papers/local_tests/mixed_valuation_tests_20261109_v11.pdf): the general local theorem, simultaneous completeness, exact normalizations, and quadratic implementation.
- [A family of quartics in 301 variables](../../papers/quartic_existence/quartic301_20261109_v11.pdf): the aggregate-trace family and its ineffective sufficient threshold.
- [An explicit quartic in 351 variables](../../papers/quartic/quartic351_20261109_v11.pdf): the fully specified quartic and its effective parameter.

## Reproduction

From `computation/quartic`, run:

```bash
python build_quartic_mixed.py
python check_quartic_mixed.py
```

The producer consumes the existing pinned systems `family317/quadratic-family317.json` and `family370/quadratic-family370.json` directly. Their mathematical proofs remain explicit dependencies. No intermediate construction is required.

The outputs are:

- `family301/quadratic-family301.json` and `family301/polynomial-family301.json`.
- `family351/quadratic-family351.json` and `family351/polynomial-family351.json`.
- Construction reports and independent verification receipts in those folders.
- `mixed-identities.json`, recording the exact toric exponents and supplementary finite valuation checks.

The independent checker imports no producer. It reconstructs every changed row from `D = 11 - 6*sqrt(2)`, checks every retained row, and independently expands the sum of squares using unordered pairs of terms. It also derives the input-square and Lucas-square affine corrections directly from their four source rows and compares them with the semantic field squares. This checks the literal normalizations rather than relying on coordinate names.

Each table records powers of the fixed coefficient `A = 80989^(2*N+1)` separately. The uncollected tables have 4320 and 5005 terms. The ordinary monomial counts are 4305 and 4990 for every `N >= 27464`; the checker proves that no coefficient can cancel in this range. Both families have degree four, content one, and

`H(P_N) < 2^1520 * 80989^(4*N+2)`.

At `N = 27464`, the 351-variable polynomial has a largest coefficient with 1,791,357 binary digits. It is the constant coefficient.

## Source checksums

| Source system | SHA-256 |
|---|---|
| `quadratic-family317.json` | `21ba60789e880826dff7298301ffcda1f33e465ed09a45ecf93170069deb9157` |
| `quadratic-family370.json` | `d4b9505504345de00c5b4493f32fa1a725405fa631e1226e178280831c078624` |

