# Automatic first conics: exact obstructions

Companion paper: [Obstructions to automatic first conics in pole certificates](../../../negative_results/papers/pole_parameters/automatic_conic_obstruction_20261115_v41.tex).

Run from the repository root:

```bash
python computation/pole_parameters/automatic_conic_v41/check.py
```

Use `--output /absolute/path/report.json` to write a temporary verification report. The default output is `verification.json` beside the checker. The report is deterministic and uses only exact rational and integer arithmetic and SymPy polynomial identities.

The checker verifies two dense families of prepared inputs whose first congruent-number conic is automatic but whose second pole equations have no rational solution, including solutions with zero second ordinate.

The smaller example has `e=9/41`, `b=(348/349)^2`, and noncongruent area square class `17`. The second lies on the fully split contact map

```text
e(delta) = (49 delta^2 - 1)/(120 delta^3)
1-e(delta)^2 = product_(a=3,5,8)(delta^2-1/a^2)/delta^6
```

at `delta=7`. It has `b=969(38864/1235629)^2` and noncongruent area square class `15499155`.

Noncongruence follows from the unconditional necessary direction of Tunnell's original theorem. Exact coefficients of its formal power series are `a(17)=-4` and `a(15499155)=-256`. The larger computation enumerates the finite Euler pentagonal expansion; independent ternary counts and a direct low-degree product computation check the arithmetic. The coefficient is not inferred from a numerical rank or an unproved converse to Tunnell's theorem.

The certificate also checks both conic parametrizations, their preparation conditions, the exact square factors, zero-ordinate exclusion, and a positive-control full pole witness. The density statements are proved in the paper. These obstructions concern prepared multipliers; they do not assert that the exhibited multipliers occur in the full integer-defining detector construction, and they prove no global variable lower bound.
