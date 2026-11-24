# Both first-Pell signs have the same coding projection

This complete reduction deletes the first-Pell half-trace square and its one
private coordinate from the short-power sources. The resulting conditional
quartics have **970 variables / 825 quadratic residuals** for the general
interface and **695 variables / 590 residuals** for ordinary rational `abc`.
The specified route is unchanged by this result.

## Mathematical content

The proof is `signed_branch_projection.tex`, with a rendered companion PDF.
It closes four points that prevent simply dropping the old sign square:

1. The strengthened margin, together with the specially chosen auxiliary
   parameter, excludes `s=0`. Its necessary divisibility `A0-1 | 5^60`
   contradicts the factorization `(b-1)H0(b)` and the exact valuation
   `v5(H0(b))=2` when `b-1=5^a`, `a>=3`.
2. Both first-Pell signs give `bw=sign(w)*2^(2r+1)`. The four possible signs
   of the first trace and second coordinate are treated explicitly.
3. A signed binomial truncation, with both error terms below `1/4`, recovers
   `M | binom(2r,r)` for negative as well as positive `w`.
4. The auxiliary power proof works with negative `A`, using absolute moduli,
   and still forces `q=b^(5^60)`.

The result preserves the **coding-prefix and instance projection**. A new
solution can have negative binomial witnesses; positive binomial, CRT, power,
and integer-interface witnesses are reconstructed for the same coding prefix.
The result does not assert that all the original signed auxiliary coordinates
extend to the predecessor sign-selected system.

Every arithmetic-interface premise, the thirteen integer inputs, the cofinite
tail `x>32*z`, and the cited Jones coding theorem are retained. This is not an
unconditional undecidability claim.

## Exact artifacts

| Interface | Predecessor | New table | Variables | Rows |
|---|---|---|---:|---:|
| General | `aggregate_spacing_v100/aggregate_spacing_general_quadrics.json` | `signed_branch_general_quadrics.json` | 970 | 825 |
| Ordinary `abc` | `pell_product_v99/product_abc_quadrics.json` | `signed_branch_abc_quadrics.json` | 695 | 590 |

Each table has a same-prefix certificate. Its only deleted coordinate is
`pell_d_positive_square`; its only deleted row is
`jones1980.pell_positive_root`. All retained residuals are copied exactly
after renumbering. Obsolete positivity and half-trace metadata are preserved
under `pell_signed_branch_predecessor_guard_metadata`; active metadata records
the signed conclusions and the projection-only scope.

From the repository root, run:

```sh
python undecidability/pell_signed_branch_v101/build_signed_branch.py
python undecidability/pell_signed_branch_v101/verify_signed_branch.py
python undecidability/pell_signed_branch_v101/verify_signed_branch_lemmas.py
```

The full-table checker imports no builder and verifies exact deletion,
unchanged rows, complete support, coefficient integrality, degree, metadata,
and hashes. The independent lemma checker imports no table builder and
verifies:

- All 58 possible zero-branch divisors `b-1=5^a`, `3<=a<=60`, after the
  manuscript's proved reduction.
- The parameter factorization and 30 symbolic Pell identities.
- 2,640 four-sign power fixtures including index zero, with 33 negative
  auxiliary-parameter fixtures.
- 352 four-sign first-Pell congruences, 192 normalized ratios, 64 alternating
  tails, and 35 elementary growth checks.
- Ten large exact local signed-binomial cores, covering both signs of `w`
  and both parities of `r`.

These local fixtures check the first and small Pell norms, integer congruence
quotients, the old strict margin, and rounding estimates. They do not claim to
instantiate the full coding prefix or the third Pell completion. The negative
`w` fixtures have negative half-trace right side, which checks the reason that
the theorem is formulated as projection equivalence. The quantified proof is
the manuscript, independently reviewed by the root and contact agents.
