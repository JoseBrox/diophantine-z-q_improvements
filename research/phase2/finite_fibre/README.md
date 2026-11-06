# Explicit polynomials from guarded finite algebras

This directory implements the one-additional-variable finite-algebra
construction as exact indexed determinant/coefficient/product polynomials.
The general theorem and all exceptional cases are explicit. No generic
primitive-element stratification is left for a future computation.

## Implemented specifications

All counts include the input coordinate. Coefficient height means the maximum
absolute value of an integer coefficient. The displayed numerical bounds are
upper bounds; none claims an exact expanded degree or height.

| Package | Total variables | Existential witnesses | Degree bound | Coefficient-height bound | Maximum algebra rank |
|---|---:|---:|---:|---:|---:|
| **`polynomial-43-conic`** | **43** | **42** | **`2^9566680`** | **`2^(2^86098389)`** | **`2^29`** |
| **`polynomial-45-conic-semilocal`** | **45** | **44** | **`2^243`** | **`2^(2^246)`** | **`2^30`** |
| `polynomial-43` | 43 | 42 | `2^9566740` | `2^(2^86098449)` | `2^39` |
| `polynomial-44` | 44 | 43 | `2^9566734` | `2^(2^86098443)` | `2^39` |
| `polynomial-45-semilocal` | 45 | 44 | `2^302` | `2^(2^306)` | `2^40` |
| `polynomial-46-semilocal` | 46 | 45 | `2^296` | `2^(2^300)` | `2^40` |
| `polynomial-558` | 558 | 557 | `2^3122` | `2^(2^3127)` | `2^508` |

Every package contains the exact specification, producer receipt, passing
independent audit receipt, and reproduction instructions. The two bold rows
are preferred: fixed square height scales remove eight finite branches, and
rational parametrizations eliminate ten finite first-conic roots without
increasing the variable count. Their exceptional conic points are included.
The other variants are preserved to allow the source changes to be reviewed
independently. The 43/44-variable
variants include a canonically specified indexed finite elliptic exclusion
product. The semilocal 45/46-variable variants have completely materialized
coefficient DAGs before the outer determinant construction. The 558-variable
specification implements the original larger finite-fiber source directly.

The matrices, finite products, and expanded monomial tables are too large to
materialize. Their dimensions, index bounds, entries, and polynomial recipes
are completely specified. Formal algebra generators and the determinant's
coefficient variable are eliminated by these finite operations; they are not
additional quantified variables. The representation is explicitly more
succinct than a circuit listing every arithmetic gate.

## Proof and audit structure

`finite_algebra_polynomial.tex` proves the general construction. A reciprocal
norm polynomial sees guarded points, a finite separating-parameter range and
explicit degree/resultant cases isolate simple eigenlines, and trace-adjugate
polynomials impose the closed conditions. A reciprocal transformation imposes
all final base guards using only one additional rational witness.

`source_558.tex` and `source_shared.tex` prove the source conversions, including
all zero-radical cases. `coefficient_bounds.tex` proves the recursive weighted
degree and operator-norm estimates. `fixed_anchor_height.tex` proves the
coefficient bounds for the fixed elliptic exclusion product without expanding
that product.

`verify_558_specification.py` and `verify_shared_specification.py` are separate
from the producers. They verify source identities, denominator coverage,
monicity, triangularity, simplicity guards, variable inventories, finite
ranges, and the recorded degree and coefficient bounds. The shared-source
checker also independently verifies every rational-square clearing
`Z=D*q`, `Z^2=N*D` and its denominator guard before the subsequent affine
coordinate conversions.

`small_algebra_interpreter.py` materializes the complete construction on eight
small algebras designed to exercise nilpotents, excluded components, collisions,
degree drops, irrational roots, and zero quadratic cases. It checks 177 full
selector/degree factors and emits a fully expanded degree-16 example.
`check_fixed_anchor_height.py` verifies exact group arithmetic and the stated
finite height inequalities for the first 24 fixed multiples; the companion
proof establishes the uniform bound for every multiple.

These implementation results preserve the input projections of the supplied
sources. The claim that those projections equal the integers additionally
depends on the source arithmetic proofs and their cited inputs. Neither the
audits nor the small computations are presented as independent proofs of all
that arithmetic. No script commits changes.
