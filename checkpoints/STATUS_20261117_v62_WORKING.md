# Recovery checkpoint: upstream audit and effective quartics

Date: 17 November 2026. This is a working checkpoint, not a publication of new defining-variable records.

## Authoritative branches

- Main: `9aa0e31ede062c6bfee592e72468444611642ce5`, all 35 CI steps passed.
- Recovery branch: `checkpoints/v57-recovery-20261117`.
- Current clean worktree: `research-v62`, local branch `research/v62-audit`.
- Preserve the older `research-repo` worktree and its staged changes.

## Source identification

The requested Version 59 has not been located. The exposed upstream main, tags, release files, and manuscript identify Version 19. The exact audited release is `elliotglazer/diophantine-z-q@498efba6fe75e9d28d6804f1391d7f70e4150afa`, tag `quartic-195-version-19`. PR 59 is a different, closed/unmerged Lean contribution. Do not relabel Version 19 as Version 59.

## Completed finite algebra

The upstream explicit 250-coordinate quartic consists of a 244-coordinate, 216-row family and six coordinates used only for a constant ladder. Keeping the integer parameter as a coefficient removes those six coordinates. The source 244 table is Carbon's and must be attributed accordingly.

An invertible rescaling of its two scalar power coordinates gives a primitive quartic with 244 total coordinates, 216 quadratic rows, 3344 monomials, and exact height `149^(2N+2)+1` at every sufficiently large permitted N. At the upstream sufficient N=10220 this is `149^20442+1`. The full tables, independent checker, pinned source, certificate, and draft are at `checkpoints/quartic250_v62/literal244/`. Its finite checker passed. The arithmetic audit of a stronger threshold is in progress.

## New effective height extension

For finite points `Qi=mi R0+Ti`, with `Ti` two-torsion on `y^2=x^3-(11-6sqrt(2))x`, put `d=3-sqrt(2)`, `M=max(1,|mi|)`, and `Z=sum x(Qi)+4d+1`. The formal-logarithm argument extends to torsion translates, since a finite two-torsion point has integral abscissa and multiplication by two kills torsion. The same positive subset numerators give

`h(Z) >= max h(x(Qi)) -24 log M -log864 -(log7)/2`.

The source duplication bound gives `h(x(Qi)) >= mi^2/4-3`; the weaker `-6` suffices for `M^2 < 8h(Z)+456`. For labels `n=m1/2, a=m2, t=m3, b=2m4+1` and `B=max(1,|n|,|a|,|t|,|b|)`, this gives `B^2 < 40h(Z)+2285`.

Proposed three-detector shifts are `U1=t1-t0=13+S0/2` and `V2=t2-t1=17+(S0-S1)/2`, where `sum x(Qi)=S0+S1 sqrt(2)`. Since `x(Qi)>=-d` at each real embedding, `U1>=7,V2>=9`; the thirty contact coefficients are distinct. The exact identity

`Z=-(2+2sqrt(2))t0+(2+4sqrt(2))t1-2sqrt(2)t2-13+4sqrt(2)`

has integral coefficients with sums of absolute values less than 32 at each real embedding. Thus `h(Z)<=sum h(tj)+log32`, giving `B^2<40 sum h(tj)+2425`. This extends the effective three-detector strategy to the full half-index and torsion domain of the 195-coordinate source.

The anticipated complete table has 229 coordinates: 195 plus a 34-coordinate third detector after its already-used fourth-power elimination. The two fourth-power savings from 198 to 196 cannot be counted again. The actual 229 table, all Laurent compatibilities, effective soundness threshold, and complete witnesses are still being checked. Do not publish 229 as proved before these are finished.

## Threshold refinement in progress

An independent audit has reduced the sufficient N for the 244 table to 10118 using direct height-constant accounting. A stronger joint accounting of the two reflected contact radicals may almost halve the exponent: outside their finite collision set even the small-prime supports are disjoint. This needs its denominator, collision-prime, and product-bound proof before publication. The original safe N=10220 remains available.

## General 21/9 target

No complete improvement to the established 25/13/11 general counts is proved. A contact-alignment specialization `lambda=4/(rho T^2)` aligns the two ten-contact numerators of the general source, and their normalized weights have square ratio. However, prescribing the slope removes the existing free simultaneous-prime argument. Global rational realization and every source guard remain to be proved. The conditional source has a different contact set; no conditional saving follows automatically.

## Publication constraints

Write only to JoseBrox/diophantine-z-q_improvements. Preserve the README Contributors and citation section, SHA-256 `bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285`. Proved polished results belong on main; experiments remain on this checkpoint branch; proved negative results stay under negative_results. Mathematical source premises must stay explicit. Build, inspect, and verify all final papers and complete coefficient tables before publishing the new record.
