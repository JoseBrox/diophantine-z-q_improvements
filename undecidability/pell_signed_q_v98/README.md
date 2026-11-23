# Signed power recovery and an absorbed Pell bound

This proved continuation removes both separate positivity wrappers introduced by the short Pell-power replacement. The complete general table has **973 variables and 827 quadratic residuals**; the ordinary-`abc` table has **697 variables and 592 residuals**. The general system saves six variables and two rows from v97. The ordinary-`abc` system also reuses an existing fourth power, saving seven variables and three rows in total. The thirteen integer inputs and all arithmetic-interface hypotheses remain unchanged.

## Why the two wrappers can be removed

The retained coding slack and the already proved congruence `q = +/-1 mod(b^5-1)` force `Q=abs(q) >= b^5-2`, without assuming that `q` is positive. On the retained cofinite instance range `x>32z`, exact estimates give `S>14Q^7` and `abs(T)<2Q^7`. Thus the prefix still gives `r>=M>L`, even for a temporarily negative `q`. The original Pell index argument applies with `Q`; its final signed congruences force `q=b^(5^60)>0`.

The auxiliary bound `power_C^2<c^2` is absorbed into the existing integer margin `eta=k^2-4(c-kY)^2`: strengthen it to `eta-power_C^2>0`. This implies the old margin and `abs(power_C)<abs(k)<abs(c)`. For canonical witnesses, integrality gives `eta>=k`, while `p>4A^2` and `r>L` give `power_C^2<p^(L-1)<k`. Therefore completeness is preserved.

The new tables delete the six `power_positive_q_*` / `power_positive_bound_*` coordinates and their two rows, and add the monomial `-2*power_C^2` to the retained `jones1980.positive.eta` residual. In the ordinary-`abc` table, `int_b_30` already equals `b^4`; substitute it for `power_b4` in the `B5` and `A` definitions and delete the duplicate coordinate and row. The general table does not have this same unscaled fourth-power register. Every other coefficient remains the same.

## Files and reproduction

- `signed_q_and_absorbed_bound.tex` / `.pdf`: complete proof, including the independent bound-absorption section `bound_absorption.tex`.
- `signed_q_general_quadrics.json` / `_certificate.json`: complete general system, 973/827.
- `signed_q_abc_quadrics.json` / `_certificate.json`: complete ordinary-`abc` system, 697/592.
- `build_signed_q.py`: deterministic transformation of the frozen v97 tables.
- `verify_signed_q.py`: independent exact audit; imports no builder.

From the repository root:

```sh
python undecidability/pell_signed_q_v98/build_signed_q.py
python undecidability/pell_signed_q_v98/verify_signed_q.py
```

The checker audits all removed occurrences, both removed wrapper polynomials, the strengthened margin, both ordinary-`abc` fourth-power substitutions, all 826 or 589 unchanged rows, full support, degree, interface metadata, and hashes. The proof establishes the quantified arithmetic statements; the coefficient audit does not replace them.

The general sufficiently large fixed parameter may be chosen as in v97, and the ordinary-`abc` result retains its stated premise. The same cited Jones coding theorem is used; its universality has not been independently reproved here. No new universality hypothesis is introduced.
