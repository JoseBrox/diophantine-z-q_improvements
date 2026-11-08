# Polynomial data formats

## Complete quartic tables

The quartic package distributes complete quadratic systems and the full coefficient tables of their sums of squares. Every variable count includes coordinate 1, the distinguished input.

| Final construction | Quadratic residuals | Total variables | Terms with parameter powers separate | Ordinary coordinate monomials |
|:--|--:|--:|--:|--:|
| Specified quartic `final389/` | 361 | 389 | 6,219 | 6,198 |
| Quartic family `family317/` | 291 | 317 | 5,047 | 5,032 for $N\ge27464$ |

Both have degree exactly four and integer content one. For the family, those two assertions hold for every integer $N\ge1$. Its defining-polynomial theorem applies to every $N\ge N_0$ for an ineffective threshold $N_0$. The support bound $N\ge27464$ does not determine that threshold.

The defining expressions are

$$
P_{389}=\sum_{j=1}^{361}q_j^2,
\qquad
P_N=\sum_{j=1}^{291}q_{N,j}^2,
$$

with the primitive integer quadratic residuals listed in the corresponding system files.

### Files and format identifiers

Paths in this table are relative to `computation/quartic/`.

| File | `format` value |
|:--|:--|
| `final389/quadratic-system389.json` | `integer-quadratic-system-v1` |
| `final389/polynomial389.json` | `integer-quartic-consecutive-coordinates-v3` |
| `family317/quadratic-family317.json` | `integer-quadratic-family-v2` |
| `family317/polynomial-family317.json` | `integer-quartic-family-v2` |

A quadratic-system object has `coordinates` and `residuals` arrays. Each residual has a `sourceId`, a `name`, and a `terms` array. A quartic object instead gives one complete `terms` array for the sum of squares. Both identify `variables`, `inputCoordinate`, and `fixedParameter`.

### Coordinates and terms

A coordinate record gives its consecutive `id`, stored `name`, upstream `sourceId`, and `kind`. Source IDs need not be consecutive; they bind retained coordinates to the arithmetic circuit. Stored names are provenance annotations. Some coordinates have affine normalizations, which are verified by `verify_detector_normalizations.py` and explained in the [389-variable paper](../papers/quartic/quartic389_20261108_v9.pdf).

Every term has three fields:

- `coefficient`: a signed decimal integer string, preserving arbitrary precision across JSON readers;
- `monomial`: a sorted list of coordinate IDs, with repetition denoting powers and the empty list denoting the constant monomial;
- `parameterPower`: a nonnegative integer exponent of the fixed coefficient parameter.

For example,

```json
{"coefficient":"-5","monomial":[1,3,3],"parameterPower":1}
```

represents $-5A X_1X_3^2$. Terms with the same coordinate monomial but different parameter powers must be collected after substituting the fixed parameter. This explains the distinction between the two term counts in the table above.

### Fixed parameter and family parameter

For `final389`, the parameter record specifies

$$
A=80989^{54929}.
$$

The exponent is a JSON integer and `coordinate` is `false`. All coefficients are therefore completely determined. The exact largest coefficient is recorded as a polynomial in $A$ in [the construction report](../computation/quartic/final389/construction-report389.json). It has 1,791,357 binary digits, so the height is less than $2^{1791357}$.

For `family317`, the exponent field is the expression string `2*N+1`, specifying

$$
A_N=80989^{2N+1},\qquad N\ge1.
$$

To specialize a member, choose an integer $N$ and replace each term's parameter factor by $A_N^{\texttt{parameterPower}}$. The string denotes this displayed arithmetic formula. Neither $N$ nor $A_N$ is a quantified coordinate. The exact family exists for every such $N$; the proof identifies no numerical sufficient value for the integer-projection theorem.

Every coefficient in the family is an integer polynomial of degree at most two in $A_N$. The independent certificate proves

$$
H(P_N)<2^{1520}A_N^2=2^{1520}80989^{4N+2}.
$$

It also proves that no listed coefficient vanishes for $N\ge27464$, yielding the stated count of 5,032 ordinary monomials.

### Exact object hashes

| Object | SHA-256 |
|:--|:--|
| 389-variable quadratic system | `f7fb5bdf6a3d47275f1d78ed5e275954e2cc1f21fec8204d6a395bfc2f8b5394` |
| 389-variable quartic | `debd9c8c9cba39e5a845ff63920b3c91dcee2b45be00905ecb0c00b6b0c73205` |
| 317-variable quadratic family | `21ba60789e880826dff7298301ffcda1f33e465ed09a45ecf93170069deb9157` |
| 317-variable quartic family | `15027a2510f03944e008938508c8bd9b552e940063eb8005baaf7710ea0702b2` |

The [quartic provenance file](../computation/quartic/PROVENANCE.json) records all source, script, table and proof hashes. The independent checkers compare complete tables; they do not rely on numerical sampling.

### Replication dependencies

The `family329/` objects use `integer-quadratic-family-v1` and `integer-quartic-family-v1`. They are an internal algebraic stage: the 317-variable producer removes the private odd-index charts, applies the invertible affine input substitution, and changes the scalar shift. Their parameter convention is the same $A_N=80989^{2N+1}$.

The direct 392-variable baseline is distributed in `baseline392/` as two gzip files. The new builders decompress these archives internally and check the original uncompressed hashes before use:

| Baseline object | Uncompressed SHA-256 |
|:--|:--|
| `baseline392/quadratic-system392.json.gz` | `b66609c16f649481ea8edb14785af2fb6f9da151f76d75dfa203f9db189e93a0` |
| `baseline392/polynomial392.json.gz` | `65f978c8b6418395535816a485093213631623766024555c69ef5db6c185450d` |

The `upstream/` and `final392/` files additionally reproduce that baseline from the pinned 394-variable source. Their four gzip objects are listed in [the compressed-data inventory](../data/compressed_sources.json). `python3 scripts/restore_data.py` restores those files and verifies their uncompressed lengths and hashes. The separate 392-variable field-specialization certificate refers specifically to this baseline.

From the repository root, `python3 scripts/verify.py` verifies the manifest, restores the compressed dependencies, and reconstructs all stages in a temporary copy. The [quartic README](../computation/quartic/README.md) gives the individual reproduction commands and their required order.

## The fully specified polynomial in 29 variables

[The finite-algebra package](../computation/few_variables/forced_prime29/README.md) specifies one polynomial in 29 total variables, including the input, with bounds

$$
\deg F\le2^{174},\qquad
\max|\operatorname{coeff}(F)|\le2^{2^{177}}.
$$

Its `source.json.gz` records the guarded rational source. Its `polynomial-specification.json` records the integer coefficient graph, triangular monic relations, denominator guards, finite conic choices, quadratic zero/nonzero cases, separating forms, degree cases, and determinant, trace, resultant and finite-product formulas. The final rational coordinate supplied by the finite-algebra theorem is included in the total count.

All products and matrix operations have explicit finite ranges. They define an ordinary integer polynomial exactly; the full monomial expansion is not stored. The scalar index bound is forced by the fixed prime 76249. The specification contains no finite exclusion over elliptic multiples.

A coefficient-graph node count describes the representation, not the number of monomials in the expanded polynomial. The `bounds` field contains certified integer majorants. The independent checker verifies these majorants using weighted companion-matrix norms and includes every zero-root case and degree drop required by the finite-algebra theorem.

| Object | SHA-256 |
|:--|:--|
| Complete polynomial specification | `05930eebc0834299ec043cef63bd94f7c99e7e012c8015cef60f4bf6480b6a9b` |
| Mathematical specification with only `bounds` omitted | `b90086cb00b5206c6dbb54a839ca7f3b06d09336630cfe09d90928192734d77d` |

An independently checked equality certificate proves that the weighted-norm refinement changes only the bound annotations. It preserves the polynomial expression and its exact degree majorant.

## The computable family in 27 variables

[The 27-variable family package](../computation/few_variables/trace27_cubic_family/README.md) uses the same finite-algebra specification conventions and has a uniform degree bound $2^{158}$. Its fixed odd integer exponent $L\ge3$ changes coefficient constants and contributes no quantified coordinate. Under the stated arithmetic premises, every sufficiently large odd $L$ defines the integers; its sufficient threshold is ineffective.

The source retains 26 rational coordinates. Nine monic quartic point roots and three quadratic pole roots are eliminated with one further rational coordinate. Formal algebra generators, matrix coordinates, and coefficient-graph nodes are not additional existential variables.

The directory `example_L137731/` contains a fully specified numerical algebraic example, including its source, complete polynomial specification, and independent certificates. Its verified coefficient bound $2^{2^{168}}$ applies to that example. The example is not certified to define the integers, since the sufficient exponent threshold is unknown.

The separate `degree-family-verification.json` treats both powers of the fixed prime as independent integer coefficient symbols of degree zero and verifies the degree recurrence uniformly. It makes no numerical coefficient-height claim for an unknown sufficiently large exponent. The [family paper](../papers/few_variables27/few_variables27_cubic_20261108_v9.pdf) states the precise existence theorem.

## Exact constants and proof references

The height-constant data give the complete prime list through 76,176 and the unsigned big-endian binary encoding of $H_{19}$. Independent enumeration and exact integer arithmetic verify these objects. The decisive prime, valuation and coefficient comparisons use exact arithmetic.

Source-graph proof identifiers refer to statements in the accompanying papers. They are provenance annotations; running a checker does not require opening a TeX file. The [arithmetic-input page](arithmetic_inputs.md) distinguishes finite algebraic certificates from global arithmetic premises, and the individual family papers identify the ineffective constants separately.
