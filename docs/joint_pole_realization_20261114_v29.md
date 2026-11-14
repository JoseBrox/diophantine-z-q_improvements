# Joint pole realization and reference-point restrictions

The general records remain **25 and 13 total variables**, with their v28 degree
bounds and stated arithmetic premises. No smaller defining polynomial is
claimed in this update; no result-table entry is changed.

## A proved reduction for compatible pole inputs

The [joint-realization manuscript](../papers/pole_parameters/joint_pole_realization_20261114_v29.tex)
proves that any number of older pole inputs can share one pair of retained
parameters when their square classes `[b]` and `[17-b]` agree. Its witness
transformations are explicit, invertible on the specified locus, and preserve
nonzero auxiliaries. With `r` pole conditions, the retained parameter count
is **2 instead of 2r**. The required additional square roots remain finite
algebraic choices, checked by a single common separating coordinate, not
unquantified assumptions.

The analogous result for the congruent-number equations uses matching classes
`[b]` and `[1-b]`. It retains the exact use of Jaswal's Hexagon Theorem 1.2;
a distinct common-first-parameter theorem states its multi-twist hypothesis
explicitly. Separate applications of a two-twist theorem do not establish
that stronger hypothesis. An exact prepared example and rational transfer
formulas accompany the proofs.

These are reductions of compatible pole subsystems, **not a new completeness
theorem for the current integer definitions**. In the existing 13-variable
prime construction, a prime belonging only to one nonzero contact makes the
two pole input classes different. The proposed sharing therefore cannot be
obtained by renaming the present witnesses.

## The geometry of a replacement family

At fixed comparison scale `a>4`, matching the first pole classes in the
six-contact route is equivalent to a rational-point condition on a
**genus-four curve**. In the ten-contact route the analogous genus is
**9** for two disjoint contact blocks; for three disjoint blocks it is **27**.
For each such fixed set of scales these curves have only finitely many rational
points by Faltings' theorem. This is not a uniform bound as the scales vary.
A replacement completeness proof must supply suitable finite slope choices,
rather than reuse the existing arbitrarily-large-slope assertion.

The separate [reference-point manuscript](../papers/elliptic_charts/progression_density_20261114_v29.tex)
proves that the family `(hP, hnP, (h-1)nP)` remains Zariski dense even when,
for each label `n`, the reference indices are restricted to an arbitrary
label-dependent infinite subset. It includes an explicit divisor-intersection
bound. Thus congruence restrictions leaving infinitely many choices per label
cannot by themselves make a reference point algebraically recoverable.
A new family with finitely many reference choices per label is not ruled out.
Neither result is an absolute lower bound on variable counts.

## Exact checks and limitations

Run from the repository root:

```sh
python -B computation/pole_parameters/joint_realization_v29/check.py
python -B scripts/verify_v28.py
python -B scripts/verify_release_v27.py
python -B scripts/verify.py --full
```

The new deterministic certificate records 14 symbolic identities, 9 prepared
witness transfers, 13 finite-algebra examples, 81 exact elliptic group examples,
contact branch counts, and deliberate corruption controls. It authenticates
its source files and checks the published certificate byte for byte. The
universal density, realization and genus arguments are mathematical proofs;
finite examples do not replace them. Inherited arithmetic inputs and
independent non-author mathematical review remain separate dependencies.
Only TeX sources, code and certificates are published in this update.
