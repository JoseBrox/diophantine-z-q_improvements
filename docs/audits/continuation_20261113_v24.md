# Audit continuation and algebraic improvements — 13 November 2026

## Conclusions

Two algebraic improvements are proved. Neither changes the number of variables or the arithmetic assumptions. The finite-algebra construction lowers the degree bounds for all four current few-variable routes, and the 214-variable quartic admits a much smaller coefficient-height formula after an invertible rational coordinate rescaling. No construction with fewer than 25 total variables under the inherited premises, fewer than 13 in the current additional-height routes, or fewer quartic variables than the pinned source was established in this continuation.

The source arithmetic foundations are **not** independently accepted as a complete proof by this report. The earlier review limitations for Sun's paper and the upstream manuscript remain open. The work below supplies exact new algebra and scoped source checks, not an audit-completion declaration.

## Finite-algebra argument

The existing construction uses a lower bound on all nonzero guard values and a common bound for point and pole roots. A triangular combination of the pole roots instead has distinct values without any lower bound on a nonzero radicand. Bounding the point roots separately prevents the large pole weights from entering their separation factor. The correct nonzero component has dimension 2^s r, allowing its determinant to be truncated to that size.

The proof checks every degree-drop case. If r exceeds the true degree, the projector is zero and the determinant is one. If r is smaller, a nonzero squared tail coefficient prevents a rational root. At the correct r, excluded nilpotents are killed and all remaining geometric character values are distinct and nonzero. This includes nonreal roots. These are the specific arguments needed to preserve all rational solutions rather than only a generic open subset.

All four source algebras have the required scalar separable point quartics, quadratic pole roots over the point algebra, a nonzero condition G=g times the product of the pole roots, and no further residual equations. The point-quartic discriminant hypotheses are checked in the paper. The exact old certificate and specification identities are retained in `inputs.json`. Complete-checkout byte authentication is a remaining execution step; the new standalone calculations do not pretend it was run.

The resulting degree bounds are 185517288563368898320200 (25 variables), 679086760181946108087584 (explicit27), 207969001841 (weak13), and 199368913265 (abc13). The explicit 27-variable member retains L=20483, and its coefficient-height bound is less than 2^(2^92). Other coefficient bounds remain fixture-only. Source soundness and completeness are transferred only under their unchanged premises.

## The actual upstream quartic coefficients

The pinned source is commit `1f7e1f1fb0438feda3c9f3da9cc16982126aeeed`. All 188 printed quadratic equations were reconstructed from its current manuscript without OCR. Their sum of squares reproduces the published 246349-byte polynomial exactly, including Git blob `f6a32cc2f7ebcc37a952c5ce737169608cfe27c2`. This is stronger than merely reproducing the announced counts. It does not authenticate a separate quadratic-table serialization or verify the arithmetic proof.

The new coordinate change is invertible for each positive fixed parameter and fixes the input. Every changed and unchanged row is checked. The exact coefficient-height calculation covers all 2919 profiles, not a sample. The improved height is 31581660^28 *149^(2N) for N>=57, and is smaller than the source height for every N>=53. Neither bound establishes a numerical defining parameter.

## Variable-removal attempts

The direct transfer of the earlier inverse-contact elimination to the 214-variable equations did not yield a proved quadratic system with two fewer coordinates. The actual source uses reciprocal and rescaled contact coordinates, whose other consumers prevent the naive substitution from remaining quadratic. A restricted search for diagonal rescalings did not resolve that obstacle. This is not an impossibility theorem for a 212-variable construction.

Combining the two conditional pole conditions, eliminating an elliptic point role, and replacing the pole surface by a lower-dimensional complete family remain unresolved. Local extraction or a generic parameter count is insufficient: any proposal must retain rational witnesses for every integer input and must control all exceptional components. No failed restricted search is used as a global lower bound.

## Review and execution boundaries

The bound calculations have two separately written implementations; the finite-algebra examples use exact multiplication matrices and include 13 cases. The quartic checker imports no producer and verifies all source and transformed coefficients. Both checks have deliberate rejection controls. These programs were written in one authoring session and are not represented as non-author review.

Both new papers were compiled twice and their rendered pages inspected. The source constructions' previous full verification suite was not rerun locally, because a complete authenticated checkout was unavailable. The supplied application script performs source authentication and requires the existing full verifier before preparing its final integration records.

The GitHub tools available for this continuation expose read actions only. No commit or push was made to the user's main branch, and no change was made to the upstream repository. The package is a prepared update with exact source pins and reproducible checks; it is not a claimed published release.

## Next mathematical priorities

The principal target remains a reduction in retained elliptic or pole coordinates. For quartics, the next useful step is a complete treatment of the rescaled contact equations and their consumers, rather than counting a deletion before checking quadratic degree. The recursive prime-pattern and pole-realization audits also remain necessary before any complete arithmetic-acceptance claim.
