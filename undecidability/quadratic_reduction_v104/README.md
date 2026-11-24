# BB-native poles in the complete combined quartics

The complete general **963-variable / 818-row** system and specified **1140-variable / 991-row** system now use Bhargava–Burungale's congruent-number point theorem for all their private pole witnesses. This changes 117 rows in 39 general poles and 132 rows in 44 specified poles, with no change of variables or rows. The old non-CM pole realization, Route K, original Theorem 5.3, certified-rank hypothesis, and project Proposition N are no longer needed for these systems. All non-pole arithmetic interfaces and the external integer-coding theorem remain premises.

This is an improvement in assumptions, not a claim of a further variable saving or a bijection between the old and new complete rational zero sets. The arithmetic conclusion is preservation of the intended integer-input projection under the stated premises.

## What is proved

For the actual pole input `b`, put `d = 7*b/9`. The physical equations become

```text
9*e^2 - 9 + 7*b*p^2 = 0
9*e - 7*e*b - 9*u*v = 0
9*u^2 - 9*v^2 - 7*b*q^2 = 0
```

Their elementary valuation argument excludes every negative odd valuation of `b` outside the already excepted prime 7. For integer completeness, the actual shared construction simultaneously makes every pole input lie in `(0,1)`, have square reduced denominator, satisfy the old 2- and 3-adic preparations, and be integral at 7. Then the cited BB theorem supplies each private pole witness. The proof includes the direct two-point construction and allows zero pole auxiliaries; it does not need a density theorem.

The new 7-adic preparation uses one common reference point and one common scalar point for all inputs. If `r_i=v_7(R_i)` and `k_i=v_7(R_i*(R_i+9792))`, one common scalar index depth `t >= max_i ceil((10*r_i-k_i)/4)` gives `v_7(b_scalar_i)=k_i+4*t-10*r_i >= 0` after increasing the common reference depth. The formal expansion permits a fixed denominator loss; no good-reduction-at-7 claim is made. Every comparison input tends to `(204/409)^2`, a 7-adic unit, using the **actual sum of all contact weights**. The existing finite-family supplier preserves these finite open conditions along with the common-index CRT.

## Complete artifacts and reproduction

- `bb_native_combined.tex` / `.pdf`: simultaneous preparation, physical chart dictionary, reconstruction, scope, and references.
- `bb_native_general_quadrics.json` / `_certificate.json`: complete 963/818 system.
- `bb_native_specified_quadrics.json` / `_certificate.json`: complete 1140/991 system.
- `build_bb_native.py`: deterministic coefficient replacement from the frozen v103 tables.
- `verify_bb_native.py`: independent checker; imports no builder code.

From the repository root:

```sh
python undecidability/quadratic_reduction_v104/build_bb_native.py
python undecidability/quadratic_reduction_v104/verify_bb_native.py
```

The checker reconstructs all 249 changed rows from six physical scale maps, pins all 166 square-register rows, verifies 1560 unchanged rows literally, and checks existing nonzero gauge and scalar inverse rows, every variable occurrence, coefficient rings, source metadata, hashes, and degrees. It independently derives the two-BB-point substitution and verifies one exact prepared local pole witness. These finite checks do not prove the external BB theorem or the retained non-pole arithmetic interfaces.

Historical predecessor hashes and papers retain their historical meanings in the metadata. The current pole interpretation and its arithmetic scope are recorded explicitly in the `bb_native_*` fields.
