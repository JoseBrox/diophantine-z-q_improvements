# Joint rationality and source-positivity continuation, 24 November 2026

The exact source-positivity reduction replaces positivity of t,m by positivity of ell-u,e-y; the retained positive slack forces b>xy, hence b^5-2z>0 and t,m>0. It removes three ordinary variables and one residual in each of the v108 quartics. See [proof, coefficient tables, certificate and verifier](../undecidability/positivity_theta_reduction_20261124/README.md). The general and specified results are 884/1049 variables with 749/912 residuals. The 602-variable abc result is superseded by [v113](results_20261124_v113.md), which uses the theta reduction, aggregate contacts, and a shared pole to reach 519.

For the number-field constructions:

* [Joint rationality](../papers/number_fields/joint_rationality_20261124/README.md): Q^k in K^k, 7k+3 total coordinates instead of 10k; the two approximation stages use separate common denominator points. Composition gives 80 and 157 for the old single-input integer definition.
* [Monic absorption](../papers/number_fields/absorbed_joint_rationality_20261124/README.md): 7N+2 total K coordinates for transferring any N-coordinate Z^d definition with at least one existential coordinate. A finite degree stratification absorbs an existential root; selected-character Hankel ranks and an anisotropic norm replace the previous etale-only encoder. This handles degree drops, repeated roots, and invalid guards at unselected characters.
* For N=11, Z inside K uses 79 coordinates. The [v110](../undecidability/abc_selective_pole_v110/README.md) joint integer predicate gives O_K in 21[K:Q]+58 coordinates, hence 100 over quadratic K, instead of 220. Integral-basis substitution leaves the count unchanged and gives coefficients in O_K. The stable-rank, v81 height, pole completeness, and original integer-definition hypotheses are all retained. The finite correction remains ineffective.

See [the current undecidability frontier](../undecidability/frontier_20261124_v113.json) for the separate direct-index and selective-pole results. The 25/27/11 and 163/179/56 single-input bounds over Q are unchanged, as is the ten-coordinate Q-in-K single-input bound. The 21/9 targets remain open; no global minimum or proof of all inherited hypotheses is asserted.

Checkpoints: c6d16223d3ce345e02b12a19dcac777b4915b239 (theta), c093271fd45abcb79438f2bf1c13d011054c5386 (joint rationality), 9e28ce29a59e1fa7a99b803c7904de01ef80773d (monic absorption). Verification is separate from a proof of arithmetic premises.
