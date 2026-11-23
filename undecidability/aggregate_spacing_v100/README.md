# A retained aggregate supplies the contact spacing

This proved continuation removes the free spacing coordinate from the general and specified affine-contact systems. The complete v99-based tables have **971 variables / 826 quadratic rows** and **1145 variables / 996 rows**, respectively. The ordinary-`abc` system is unchanged.

The key choice is `D=T_b/16`, where `T_b` is the first aggregate shift of the retained root block. This shift depends only on the fixed difference points and stays fixed when the later comparison-prime construction retunes the reference index. Its two-adic depth is exactly the common lower bound for all contact positions: the shared Lucas point `Q3` strictly dominates every other aggregate contribution. Multiplication by any nonzero difference of indices in `{0,...,15}` cannot erase the four additional powers of two in the denominator of `D`. Thus every translated contact list remains disjoint.

In both charts the stored spacing is the affine expression

```text
contact_common_spacing = (int_b_68 - int_b_2) / 16.
```

Substituting it everywhere and removing its coordinate preserves every old row after reconstruction. It introduces no new row or guard and preserves quadratic degree. Completeness follows from the original ordered finite-family supplier with the now fixed shifts. The earlier candidate using a scalar secant coordinate remains blocked by reference dependence; this construction uses a different invariant and does not validate that candidate.

## Deliverables and reproduction

- `aggregate_spacing.tex` / `.pdf`: complete valuation, supplier-order, chart and census proof.
- `aggregate_spacing_general_quadrics.json` / `_certificate.json`: complete 971/826 system.
- `aggregate_spacing_specified_quadrics.json` / `_certificate.json`: complete 1145/996 system.
- `build_aggregate_spacing.py`: deterministic compiler from the frozen v99 tables.
- `verify_aggregate_spacing.py`: independent exact audit, importing no compiler.

From the repository root:

```sh
python undecidability/aggregate_spacing_v100/build_aggregate_spacing.py
python undecidability/aggregate_spacing_v100/verify_aggregate_spacing.py
```

The audit checks all fourteen or twenty-two changed rows, 812 or 974 unchanged rows, primitive constant multipliers, complete support, degree, coefficient rings, retained aggregate/gauge equations, metadata and hashes. Seventy-five modular Lucas fixtures and all 120 index differences provide additional exact checks; the proof supplies the quantified arithmetic argument. The arithmetic interfaces, general-parameter scope and cited Jones coding theorem are unchanged.
