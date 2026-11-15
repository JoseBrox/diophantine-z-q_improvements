# Joint realization of compatible pole conditions

The [current construction table](../README.md) states the variable and degree bounds. The transfer results below apply to specified compatible pole inputs and do not provide a new completeness theorem for the full definitions.

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

The compatibility conditions are hypotheses of these transfer theorems. The [fresh-prime and fixed-scale obstructions](../negative_results/papers/pole_parameters/fresh_prime_squareclass_obstruction_20261116_v42.tex) are presented separately. The [negative-results index](../negative_results/README.md) also records the limits of algebraic reference-point elimination.

## Exact checks and limitations

Run from the repository root:

```sh
python -B computation/pole_parameters/joint_realization_v29/check.py
python -B scripts/verify_v28.py
python -B scripts/verify_release_v27.py
python -B scripts/verify.py --full
```

The deterministic certificate records 14 symbolic identities, 9 prepared
witness transfers, 13 finite-algebra examples, 81 exact elliptic group examples,
contact branch counts, and deliberate corruption controls. It authenticates
its source files and checks the published certificate byte for byte. The
universal density, realization and genus arguments are mathematical proofs;
finite examples do not replace them. Inherited arithmetic inputs and
independent non-author mathematical review remain separate dependencies.
Only TeX sources, code and certificates are published in this update.
