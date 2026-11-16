# Current quartic coefficient families

All counts include the input. The rational input projection is the integers under the arithmetic premises stated in each paper. The [main results table](../../README.md) distinguishes every additional hypothesis and parameter threshold.

| Coefficient package | Additional hypothesis | Variables | Quadratic rows | Ordinary monomials | Defining parameter |
|:--|:--|--:|--:|--:|:--|
| [primitive_basis196_v40](primitive_basis196_v40) | None beyond the inherited premises | 196 | 176 | 2,994 | Every sufficiently large fixed N; threshold ineffective |
| [laurent_recovery_v38/family258](laurent_recovery_v38/family258) | None beyond the inherited premises | 258 | 230 | 3,705 | N=9682 |
| [abc76_v44](abc76_v44) | Ordinary rational abc | 76 | 66 | 1,250 | Every sufficiently large fixed odd B≥81; threshold ineffective |

Each family has exact total degree four and integer content one. The full coefficient specifications, arithmetic proofs and source attributions are linked from the main table. No global minimum is claimed, and the full independent audit of the inherited arithmetic premises is not declared complete.

## Exact coefficient heights

For the 196-variable family, for every N≥1,

$$H(P_N)=\max\{126616122944180358034867798936,\ 32561227748626372080\cdot149^{2N}\}.$$

For the explicit 258-variable member at N=9682,

$$H(P)=9792^2\cdot149^{19364}.$$

For the 76-variable ordinary-abc family, for every fixed odd B≥81,

$$H(Q_B)=\max\{20828275368498373068800,\ B^2+275933278576697172\}.$$

These coefficient formulas do not provide sufficient numerical defining thresholds for the ineffective families. In particular B=81 is only an algebraic fixture.

## The 76-variable equations

The [complete theorem](../../papers/quartic_existence/quartic_abc76_20261116_v44.tex) retains the full reference and paired-point domains. Fourth powers of comparison errors and second powers of point reciprocals occupy distinct contact valuation classes modulo four. A square rescaling of each pole input gives quadratic equations without a cube-weight coordinate. Zero contacts form a finite bounded-height set and are included in soundness without an additional nonzero constraint.

The package contains every primitive quadratic row and the complete expanded polynomial. Its independent checker derives the twelve changed rows, authenticates the 54 retained rows, expands all coefficients, and checks the pole map, degree, content, support and uniform height formula. The paper proves the infinite soundness and completeness statements.

## Reproduction and dependencies

Use Python 3.12 and SymPy 1.14.0. From the repository root:

```sh
python -B scripts/verify_v44.py
python -B scripts/verify_v40.py
python -B scripts/verify_v38.py
```

The [full reproduction instructions](../../README.md#reproduction) include the retained suites and the 126-stage legacy verifier. Exact predecessor tables remain as reconstruction dependencies, with their corresponding papers and checkers. The [source provenance](PROVENANCE.json) authenticates the legacy source chain; it does not replace the current construction table. The current [results JSON](../../data/results_20261116_v44.json) identifies the coefficient package used for each record.
