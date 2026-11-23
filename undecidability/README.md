# Variable bounds for undecidability over the rationals

This subject is separate from defining the integers with one polynomial. Here
`N` counts **existential rational unknowns in a decision problem**. The integer
input specifying an instance is part of its coefficients and is not counted.
The defining-polynomial tables elsewhere in the repository include their input.
All numbers below are upper bounds; no global least value is claimed.

## Initial registration, 23 November 2026

The previous research session obtained the transfer formula

```math
N=15m+94,
```

where the integer predicate has `m` total coordinates and is a sum of squares
of quadratic polynomials. The source is a universal positive-integer quadratic
system. Its source audit and a new independent reconstruction are in progress.
The [baseline checkpoint](checkpoints/baseline_20261123.md) records exactly
which claims are inherited and the earlier transcription correction.

| Source integer predicate | Additional height hypothesis | Reported quartic transfer | Status |
|:--|:--|--:|:--|
| General quartic, 163 total coordinates | No additional abc hypothesis | 2,539 | Previous transfer checkpoint; source audit being reconstructed |
| Fully specified quartic, 179 total coordinates | No additional abc hypothesis | 2,779 | Same transfer instantiated at the fully specified source |
| Ordinary-abc quartic, 56 total coordinates | Ordinary rational abc | 934 | Same transfer; sufficient fixed source shift is ineffective |

These are not claims of unconditional rational undecidability. They retain
the defining theorems' explicit arithmetic interfaces, as well as the
universal integer system used in the transfer. An algebraic count does not
establish those arithmetic interfaces. In particular a small stored fixture
must not be substituted for a defining parameter.

The machine-readable [registry](results.json) separates imported checkpoints
from subsequently proved transfer theorems. New systems, proofs, certificates,
and research checkpoints concerning undecidability belong in this directory.

## Sources and conventions

- A. Mishchenko and A. Treier, *Universal input of knapsack problem for groups*,
  Journal of Physics: Conference Series **1050** (2018), 012054,
  [doi:10.1088/1742-6596/1050/1/012054](https://doi.org/10.1088/1742-6596/1050/1/012054).
- J. P. Jones, *Universal Diophantine equation*, Journal of Symbolic Logic
  **47** (1982), 549--571,
  [doi:10.2307/2273588](https://doi.org/10.2307/2273588).
- [General 163/179-coordinate predicates](../papers/quartic/scalar_point163_179_20261120_v82.tex).
- [Ordinary-abc 56-coordinate predicate](../papers/quartic_existence/paired_contact56_20261119_v81.tex).

The 57-positive-integer-variable / 47-equation claim is being checked against
the complete source equations. Universality, positivity, integrality,
coefficient effectiveness, and total degree are separate proof obligations.
