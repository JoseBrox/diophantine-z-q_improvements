# Two precise transfer lemmas — 17 November 2026

Files:

- `rank_stable_adjacent_contacts_20261117_v63.tex`: proved obstruction to directly substituting a base-field rank-stable elliptic curve into the conjugate adjacent-index detector.
- `finite_exceptions_and_integrality_20261117_v63.tex`: proved finite-correction and bounded-height criterion, with explicit coordinate and degree counts.

## Reduction obstruction

The proof works for arbitrary finite L/K, any E/K, and any non-torsion P in E(L) having a fixed positive multiple in E(K). Rank stability supplies this hypothesis through finite index of Mordell–Weil groups. A further fixed multiplication annihilates rational torsion.

At a prime where E has good reduction, two identity reductions of [h]P+T1 and [h-c]P+T2 at any two places over that base prime force [c][t]P to reduce to O over the base residue field. No splitting or unramified hypothesis is needed; the places may coincide. The proof never divides by t, so it explicitly includes residue characteristics dividing t. Finiteness of possible primes follows from a fixed integral global model after adding its finite discriminant support, thereby covering globally nonminimal equations at intrinsically good primes as well.

For c=1 this excludes the simultaneous reciprocal-abscissa contacts of H and the conjugate of H-P at all sufficiently large primes. A fixed finite menu of nonzero c also fails outside a fixed finite set. This does not exclude curves genuinely defined over the larger field, other local comparison architectures, or O_K definability.

No numerical experiment materially strengthens this elementary group-reduction proof. No computational certificate is claimed or needed.

## Finite exceptions

The strongest stated criterion needs S to contain all but finitely many rational integers and only requires a height bound on S minus O_K. Northcott makes the nonintegral exception set finite. Correcting S with one new inverse variable and finite-union factor produces a Diophantine sandwich Z subset S0 subset O_K, after which an integral basis defines O_K. S0 may contain nonrational algebraic integers; a rationality definition is not required.

For original total count N and degree D, finite deletion A and insertion B produce a single polynomial with N+1 coordinates and degree at most |B|+2 max(D,|A|+1), using a fixed nonsquare coefficient in K. For d=[K:Q], the integral-basis construction uses d(N+1) coordinates and d equations of that degree. A degree-d field norm combines them without extra variables.

Under the stronger height bound on S minus Z, the correction defines Z directly. The finite sets may be ineffective; no claim of a computable identification or an actual complete detector S is made.

The cited Northcott theorem number was checked: Hindry–Silverman, Diophantine Geometry, Theorem B.2.3. Zywina's rank-stability statement was checked in the author-hosted manuscript and is cited as arXiv:2505.16960v1, a preprint.

These statements are elementary reductions and should not be described as a proof that every ring of integers is Diophantine in its field of fractions. The unresolved global witness and local detector construction remains essential.

No build was attempted here after the earlier pdflatex format failure. Root's build pipeline should compile and inspect the files before publication.
