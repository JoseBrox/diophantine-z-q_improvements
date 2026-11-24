# Bhargava–Burungale replaces the native pole in the general quartics

**24 November 2026 — preferred current result.** This is an independent continuation of the [v88 source audit](results_20261123_v88.md) and the [v82 163/179-variable constructions](results_20261120_v82.md). All current few-variable constructions already use the Bhargava–Burungale product-pole argument. The general quartics previously retained a different non-CM pole.

The [complete new manuscript](../papers/quartic/bb_native_quartics_20261124.tex) proves that, after one extra fixed local preparation at 7 and tightening the real pole inputs to `0<b<1`, each original pole block may be replaced by the three congruent-number equations

```math
9e^2-9+7bp^2=0,\qquad 9uv-9e+7eb=0,\qquad 9u^2-9v^2-7bq^2=0.
```

Their arithmetic content is Bhargava–Burungale, arXiv:2611.16130v2, Theorem 2.3 and Lemma 2.2, applied at `d=7b/9`. The proof does not import Elliot's Theorem 5.3, Route K, CR₃, or Proposition N. Every other geometric, elliptic, trace-height, comparison, recurrence and prime-pattern input remains exactly as in the historical source.

## Complete new systems

| | General quartic family | Fully specified quartic |
|---|---:|---:|
| Variables including rational input | **163** | **179** |
| Quadratic residuals | 137 | 151 |
| Old non-CM pole residuals replaced | 9 | 12 |
| Other residuals unchanged | 128 | 139 |
| Nonzero expanded monomials | **2,771** | **3,012** |
| Historical v82 monomials | 2,789 | 3,036 |
| Improvement | 18 fewer | 24 fewer |
| Total degree | 4 | 4 |
| Integer content | 1 | 1 |
| Exact decimal TXT bytes | **60,638** (N=1 fixture) | **66,484** |
| Previous TXT bytes | 60,907 (N=1 fixture) | 66,905 |

The 163-variable coefficient height remains `max(126616122944180358034867798936, 149^(4*N+2))` for `N>=1`; the sufficient defining parameter is still ineffective. The fixed 179-variable member retains the exact 748-bit height `(A0 * Ba^4)^2`, with the constants and arithmetic hypotheses pinned in the [new package](../computation/bb_native_quartic_20261124/README.md). The Busy Beaver fixed-member estimate of the original v82 table is historical, not automatically transferred to the changed source.

## Why the modified arithmetic is correct

For arbitrary rational zeros, the new three-equation pole test forces `d=7b/9` to have square denominator: if `v_p(d)<0` is odd, the first equation makes `e` a unit, the second requires `v_p(uv)` odd, while the third makes `v_p(u)=v_p(v)`, a contradiction. Therefore every prime except 7 has the same sound denominator obstruction for `b` (at 3 the valuation changes by minus two, preserving parity). Prime 7 was already excluded by the source's fixed height theorem.

For integer completeness, the v82 scalar real bound already implies `b_s<1`; the comparison inputs tend to `(204/409)^2<1` at real places. Their 7-adic limiting value is a unit, so finite approximation can ensure the comparison inputs are 7-adic units. The scalar input can be made 7-adically integral by preparing one more fixed formal depth, using the same arbitrary-finite-set recurrence. The old 3-adic depth `>=2` remains. Thus `d=7b/9` is positive below one, square-denominator, in the squareclass `7 Q_2^{*2}` with 2-adic depth `>=4`, so BB supplies its rational witnesses. Their rational family also provides the nondegenerate witness choices needed for finite-algebra guards.

The prior proposal `d=3b/5` fails for a comparison input that is a 5-adic unit; this was detected and excluded before release. The earlier valid but less efficient `d=7b/17^2` is preserved as [a checkpoint](bb_quartic_native_migration_20261124.md). The final choice is **`d=7b/9`**.

## Verification and provenance

The [primary new package](../computation/bb_native_quartic_20261124/README.md) includes full ordinary quadratic residuals, complete coefficient expansions, a producer and a separate independent checker. The independent reconstruction from original Laurent source rows checked all 9/12 replaced rows, and an ordered complete re-expansion checked all 2,771/3,012 monomials, content and degree. The source algebra and coefficient heights passed. Numerical checks are not proofs of the cited external analytic input or other inherited foundations.

The [fully expanded 163-variable N=1 fixture](../computation/bb_native_quartic_20261124/expanded/quartic163-N1.txt) is **not certified to define the integers**; it is an exact algebraic fixture. The [179-variable decimal polynomial](../computation/bb_native_quartic_20261124/expanded/quartic179.txt) is the fixed specified member under the source arithmetic premises.

No historical v82 source file or coefficient table was overwritten. No changes are required in Elliot Glazer's repository. The previously opened Elliot-side draft PR #172 was closed unmerged.

**Next research direction:** pursue smaller quartic variable counts by reusing the native pole coordinates or dropping the now redundant non-CM argument from higher-level source documents, only after producing an exact quadratic inverse map. All old source artifacts remain attributable historical records.
