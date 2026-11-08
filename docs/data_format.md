# Polynomial data formats

## The quartic in 392 variables

The quartic data specify

$$
Q=\sum_{j=1}^{364}q_j^2\in\mathbb Z[X_1,\ldots,X_{392}],
$$

where the $q_j$ are the supplied primitive integer quadratic polynomials. Coordinate 1 is the distinguished input. The polynomial has degree 4, content 1, exactly 6,204 nonzero coordinate monomials, and coefficient height less than $2^{1791357}$.

Four large JSON objects are distributed as lossless gzip files:

| Distributed file, under `computation/quartic/` | Content |
|:--|:--|
| `upstream/candidate394-ir.json.gz` | Pinned upstream 394-variable quadratic system. |
| `upstream/polynomial394.json.gz` | Pinned upstream quartic coefficient table. |
| `final392/quadratic-system392.json.gz` | All 392 coordinates and 364 quadratic equations of the stated construction. |
| `final392/polynomial392.json.gz` | Complete coefficient table of their sum of squares. |

Run `python3 scripts/restore_data.py` from the repository root to restore the JSON files. Their uncompressed byte lengths and SHA-256 hashes are checked against [the compressed-data inventory](../data/compressed_sources.json). The top-level verifier performs this restoration automatically in its temporary working copy.

### Coordinates and coefficients

A coordinate record gives its consecutive `id`, mathematical `name`, and upstream `sourceId`. A term consists of an integer `coefficient`, a sorted list `monomial` of coordinate indices with repetitions, and a nonnegative integer `parameterPower`. An empty monomial denotes the constant term. Coefficients are stored as decimal strings to preserve arbitrary-precision integers across JSON readers.

The fixed parameter is

$$
A=80989^{54929}.
$$

A term with `coefficient: c` and `parameterPower: e` represents $cA^e$ times its coordinate monomial. This parameter is a specified integer coefficient. Equal coordinate monomials must be combined after its substitution. The table contains 6,225 terms over $\mathbb Z[A]$ and 6,204 ordinary coordinate monomials after specialization; the independent checker verifies that the stated coefficients are nonzero.

The exact maximum coefficient is recorded as a polynomial in $A$ in [the construction report](../computation/quartic/final392/construction-report392.json). Its binary length is 1,791,357. The main uncompressed hashes are:

| Object | SHA-256 |
|:--|:--|
| Final quadratic system | `b66609c16f649481ea8edb14785af2fb6f9da151f76d75dfa203f9db189e93a0` |
| Final quartic | `65f978c8b6418395535816a485093213631623766024555c69ef5db6c185450d` |

The independent quartic checker reconstructs the pinned source sum of squares, verifies the changed equations and all retained equations, and expands the complete final sum of squares. It compares every coefficient with the distributed table.

## The polynomial in 29 variables

[The finite-algebra package](../computation/few_variables/forced_prime29/README.md) specifies one polynomial in 29 total variables, including the input, with bounds

$$
\deg F\le2^{174},\qquad
\max|\operatorname{coeff}(F)|\le2^{2^{177}}.
$$

Its `source.json.gz` records the guarded rational source. Its `polynomial-specification.json` records the integer coefficient graph, triangular monic relations, denominator guards, finite conic choices, quadratic zero/nonzero cases, separating forms, degree cases, and determinant, trace, resultant and finite-product formulas. The final rational coordinate supplied by the finite-algebra theorem is included in the total count.

All products and matrix operations have explicit finite ranges. They define an ordinary integer polynomial exactly. The full monomial expansion is not stored. The scalar index bound is forced by the fixed prime 76249; the specification contains no finite exclusion over elliptic multiples.

A coefficient-graph node count measures the representation, rather than the number of monomials in the expanded polynomial. The `bounds` field contains certified integer majorants. The independent checker verifies those majorants using weighted companion-matrix norms, and includes every zero-root case and degree drop required by the finite-algebra theorem.

| Object | SHA-256 |
|:--|:--|
| Complete polynomial specification | `05930eebc0834299ec043cef63bd94f7c99e7e012c8015cef60f4bf6480b6a9b` |
| Mathematical specification with only `bounds` omitted | `b90086cb00b5206c6dbb54a839ca7f3b06d09336630cfe09d90928192734d77d` |

The package includes an independently checked equality certificate showing that the weighted-norm refinement changes only the bound annotations. It preserves the polynomial expression and the exact degree majorant.

## Exact constants and proof references

The height-constant data give the complete prime list through 76,176 and the unsigned big-endian binary encoding of $H_{19}$. Independent enumeration and exact integer arithmetic verify these objects. The decisive prime, valuation and coefficient comparisons use exact arithmetic.

Source-graph proof identifiers refer to statements in the accompanying [29-variable paper](../papers/few_variables/few_variables_20261108_v8.pdf) and [quartic paper](../papers/quartic/quartic392_20261108_v8.pdf). They are provenance annotations; running a checker does not require opening a TeX file. The [arithmetic-input page](arithmetic_inputs.md) distinguishes the finite algebraic certificates from the global arithmetic hypotheses.
