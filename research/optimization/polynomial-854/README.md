# Explicit polynomial in 854 variables

This package specifies an integer polynomial in **854 total variables**, of
which **853 are existential witnesses**. It is obtained from the separate
855-variable circuit by absorbing its global denominator guard into the
private quadratic witness of the semilocal anchor. The integer arithmetic
circuit and finite products are an exact polynomial specification; circuit
gates do not introduce quantified variables. An expanded monomial list is
not provided.

## Exact transformation

The three private anchor witnesses satisfy
`u² + 6v² - 2w² - 3r² + 2C⁴ = 0`, with a fixed nonzero rational `C`.
They cannot all vanish. If `u = 0`, replace `(u,w) = (0,w)` by `(4w,3w)`
when `w != 0`; otherwise replace `(u,v) = (0,v)` by `(-12v/7,-5v/7)`.
These rational transformations preserve the anchor and make `u != 0`.

The cleared anchor is `B u² + N = 0`, where `B = S²` is a polynomial
square. Let `G` be the product of all branch denominator factors, including
those of `B`, and let `F_i` be the other cleared residuals. Rescaling
`t = S u` gives `t² + N = 0` with `t != 0`. Replace the anchor and the
independent inverse witness with

```text
Psi = 1 + N G² U²
Q   = sum_i F_i² + Psi².
```

At `GU = 0`, `Psi = 1`. Otherwise
`Psi = (GU)² [(1/(GU))² + N]`, so a zero recovers `t = 1/(GU)` and
`u = 1/(GSU)`. The input projection is unchanged. The forward construction
may change all three private anchor witnesses; it does not claim to
preserve every fiber with both `v` and `w` fixed. See
`anchor-guard-proof.tex` for the full proof.

The two finite parameter lists contain 212 choices of the common point
chart and 256 height squareclasses. The specified polynomial is the product
of the 54,272 branch polynomials. Each branch enforces its own guards.

## Files and reproduction

- `polynomial-circuit.json`: exact integer DAG and finite-product specification.
- `construction-report.json`: variable inventory, hashes, and rigorous bounds.
- `verification.json`: receipt from the independent exact verifier.
- `anchor-guard-proof.tex`: mathematical proof and scope of the certificate.
- `../build_compact_854.py`: producer, which imports the separate 855 producer.
- `../verify_compact_854.py`: independent verifier; imports neither producer.

From the repository root:

```sh
python3 research/optimization/build_compact_854.py --output research/optimization/polynomial-854
python3 research/optimization/verify_compact_854.py
```

The verifier reads the pinned parent circuit in `polynomial-855/`. It checks
the unchanged 296 rational residuals and 1,681 guards by collision-free
structural interning, checks the complete ternary-anchor and reciprocal identities
by exact sparse polynomial arithmetic, and verifies all denominator guards,
the sum of 297 squares, the finite parameter sets, DAG topology, coordinate
inventory, and degree/coefficient-norm bounds. The 855 parent has its own
audit in `../compact-audit-855.md` and `../verification-855.json`.

## Certified inventory and bounds

| Quantity | Value |
| --- | ---: |
| Total declared variables | 854 |
| Existential witnesses | 853 |
| Point coordinates | 633 |
| Pole-block coordinates | 210 |
| Anchor coordinates | 3 |
| Proxy coordinates | 3 |
| Other coordinates, including input | 5 |
| Stored DAG nodes | 95,538 |
| Nodes reached from branch output | 94,393 |
| Finite branches | 54,272 |
| Degree upper bound | 63,570,781,474,816 |
| Base-2 logarithm of coefficient-height upper bound | 757,866,260,454,400 |

All 854 declared variables are reached from the output DAG. The degree and
coefficient values are rigorous upper bounds, not exact expansion statistics.

Circuit SHA-256:
`aef6888809817e37e372471fd780f83d0241e58f04ddeafd03fd6b46cfa39d62`.

The original arithmetic characterization is inherited from source commit
`28e87b1b62af0effd954605af7f70b2699dd5672`. This package proves and certifies
the stated transformation of the rational system; it does not independently
settle every arithmetic claim in the source manuscript. No global minimality
is claimed, and no commits are made by these scripts.
