# Current dependence on congruent-number pole theorems

Updated 24 November 2026. This map concerns **current preferred defining-polynomial specifications**, not the unchanged historical source manuscripts or unfinished research checkpoints. It is not a claim that all the non-pole arithmetic foundations have been independently established.

| Current construction | Pole arithmetic supplier | Need for Elliot's Theorem 5.3 or Route K? | Exact artifact |
|---|---|---|---|
| General 25-variable family | Bhargava–Burungale v2, Lemma 2.2, with the normalized product pole | **No** | [v88 theorem](../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) |
| Fully specified 27-variable polynomial | Same | **No** | [v88 theorem](../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) |
| Ordinary-abc 11-variable construction | Same, with twelve-contact preparation | **No** | [v88 theorem](../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) |
| Weak-abc 11-variable families (both stated exponents) | Same, with the project's verified extra preparation | **No** | [v88 theorem](../papers/few_variables25/bb_product_degree_transfer_20261123_v88.tex) |
| General 163-variable quartic | Bhargava–Burungale v2, Theorem 2.3/Lemma 2.2, through the native three-conic interface (d=7b/9) | **No** | [new complete quartic](../papers/quartic/bb_native_quartics_20261124.tex) and [tables](../computation/bb_native_quartic_20261124/README.md) |
| Fixed 179-variable quartic | Same | **No** | [new complete quartic](../papers/quartic/bb_native_quartics_20261124.tex) and [tables](../computation/bb_native_quartic_20261124/README.md) |
| Ordinary-abc 56-variable quartic | Burungale/Bhargava–Burungale Theorem B on the class-seven prepared locus | **No** | [v81 theorem](../papers/quartic_existence/paired_contact56_20261119_v81.tex) |
| Current undecidability transfers | The chosen underlying project source, generally BB-native/product-pole; compare their **specific** inherited assumptions | No new Route K hypothesis introduced here | [undecidability index](../undecidability/README.md) |

These are two **different** polynomial presentations using the same general congruent-number arithmetic, not one common literal pole template:

* The **product pole** uses a short polynomial equation whose rational zero set enforces the required one-sided denominator obstruction.
* The **native conic pole** preserves the 163/179 quartic's existing five auxiliary physical slots and two square registers. The three replaced equations are
  [
  9e^2-9+7bp^2=0,qquad 9uv-9e+7eb=0,qquad
  9u^2-9v^2-7bq^2=0.
  ]
  This preserves the quartic degree and variable counts, while reducing monomials.

**What is removed.** Current source premises no longer require a non-CM restricted 2-converse for (E_ell:y^2=x(x-ell)(x+3ell)), nor Route K's 2-Selmer slots, CR₃ or project Proposition N to obtain the relevant rational pole witnesses. BB's theorem proves the required existence of those witnesses itself, by congruent-number arithmetic.

**What remains.** The inherited elliptic carrier group, formal logarithm, contact-height estimates, prime-pattern and recurrence hypotheses are **not** eliminated by replacing the pole. The 179 fixed-coefficient effectiveness and the 163 qualitative existence retain their prior scopes. Historical v82 polynomial tables and v86/v87 Busy Beaver coefficient records are preserved; the latter have not automatically been transferred to the changed BB-native polynomial.

**Verification.** The new [proof](../papers/quartic/bb_native_quartics_20261124.tex) checks the extra 7-adic condition and the smaller real interval. Every replacement row was independently reconstructed from the original weighted source, and both complete quartic expansions independently checked. The finite certificates do not replace the cited deep results of Bhargava–Burungale/Tian–Yuan–Zhang and the retained source literature.

**Repository boundary.** All new commits for this replacement are in **JoseBrox/diophantine-z-q_improvements**. No changes were applied to Elliot Glazer's main repository; his draft PR #172 was closed without merging.
