# Explicit polynomial in 853 variables

This package specifies an integer polynomial in **853 total variables**,
including the input and **852 existential witnesses**. It combines the
private semilocal anchor and the middle proxy's Pell equation into one
coordinate. The arithmetic DAG and finite products are an exact polynomial
specification; gates are expressions and add no quantified variables.

The transformation is independently verified. Its identification of the
input projection with the integers inherits the arithmetic theorem used by
the original repository, pinned at commit
`28e87b1b62af0effd954605af7f70b2699dd5672`.

## Mathematical construction

The two cleared conics in each pole block force its denominator
`delta = 1 + b t²` to be nonzero over the rationals. If `delta = 0`, the
second conic forces `e = 0` and the first forces `(p t)² = -17`.
Thus 42 guards may be removed. The remaining guard product `G` is independent
of every proxy and anchor coordinate.

The cleared anchor is `B u² + N = 0`, with `B = S²`. Its three private
witnesses can be adjusted rationally so that `u != 0`, so `T = S u != 0`.
The proxy equation is `tau² - a tau + b0 = 0`, where

```text
a     = s(s-2)z
b0    = (s-2)² z² - 1
Delta = a² - 4b0
V     = 2 tau - a.
```

Now `T² = -N` and `V² = Delta`. Choose the free sign of `T` so that
`W = T + V != 0`. This needs no new finite branch. The two equations are
equivalent, on `W != 0`, to

```text
h(W) = W⁴ + 2(N-Delta)W² + (N+Delta)² = 0.
```

Set `W = 1/(G U)`. The replacement residual and reconstructed proxy are

```text
Psi  = 1 + 2(N-Delta)G²U² + (N+Delta)²G⁴U⁴
tau  = P_tau / Q_tau
P_tau = 1 + 2aGU + (N+Delta)G²U²
Q_tau = 4GU.
```

`Psi` is 1 when `G U = 0`, so every zero enforces the retained guards.
Each of the other 295 residual numerators `F_i` is replaced by the exact
polynomial `Q_tau^d_i F_i(P_tau/Q_tau)`. The branch polynomial is the sum
of their squares and `Psi²`. The specified polynomial is the product over
the unchanged 54,272 chart and height choices. The input projection is
preserved; the argument may change the private anchor witnesses.

Full definitions, proofs, reverse reconstruction, and scope appear in
`quadratic-combination-proof.tex`.

## Files and reproduction

- `polynomial-circuit.json`: complete integer DAG and finite-product specification.
- `construction-report.json`: inventory, hashes, and rigorous bounds.
- `verification.json`: independent emitted-DAG audit receipt.
- `producer-review.json`: separate review and exact inventory checks.
- `quadratic-combination-proof.tex`: full mathematical proof.
- `../build_compact_853.py`: producer; uses the separate 855/854 producer utilities.
- `../verify_compact_853.py`: exact verifier, which imports no producer.
- `../verify_pole_guard_removal.py`: independent guard-removal checker, rerun by the verifier.

From the repository root:

```sh
python3 research/optimization/build_compact_853.py --output research/optimization/polynomial-853
python3 research/optimization/verify_compact_853.py
```

The verifier requires the unchanged parent circuit in `polynomial-855/`
and the exact-polynomial helpers in `verify_compact_854.py`. It checks every
transformed residual by the invariant `new_H = Q_tau^d old_H(P_tau/Q_tau)`,
checks both reconstruction identities formally, and checks the final sum
of squares, guard list, variable map, finite branches, and bounds. The
transformation identities use no sampled or probabilistic tests.

## Inventory and bounds

| Quantity | Value |
| --- | ---: |
| Total declared variables | 853 |
| Existential witnesses | 852 |
| Point coordinates | 633 |
| Pole-block coordinates | 210 |
| Anchor coordinates | 3 |
| Proxy coordinates | 2 |
| Other coordinates, including input | 5 |
| Stored DAG nodes | 95,084 |
| Nodes reached from output | 94,946 |
| Finite branches | 54,272 |
| Squares per branch | 296 |
| Maximum proxy homogenizing exponent | 1,280 |
| Degree upper bound | 894,090,701,148,160 |
| Base-2 logarithm of coefficient-height upper bound | 29,154,205,340,326,912 |

All 853 declared coordinates are reached from the output DAG. The degree
and coefficient values are rigorous upper bounds, not exact statistics of
an expanded monomial list. Compared with the 854-variable package, this
construction reduces variables while increasing the degree bound.

Circuit SHA-256:
`67992338a1d904d623d9b1b076f28b9da6b84e44736d34e90784f75f305e5d63`.

No global minimality is claimed. Guard removal is proved over the rationals;
it must not be used without justification in an argument about fibers over
an algebraic closure. No commits are made by these scripts.
