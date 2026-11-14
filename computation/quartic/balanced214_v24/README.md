# Smaller coefficients for the pinned 214-variable quartic

The [paper](../../../papers/quartic/coefficient_balancing_20261113_v24.pdf) proves an exact rational coordinate equivalence. Set C=149^N and A=149 C^2. Multiply source coordinates 90, 91, 93, 117, 118 and 120 by C, and remove the common powers of C from the seven indicated quadratic rows. The input coordinate is unchanged.

The result has **214 variables, 188 quadratic rows, exact degree four, integer content one and 2919 coordinate monomials**. There are 2924 symbolic terms before powers of C at the same coordinate monomial are collected. It has the same rational input projection as the pinned source for every N>=1.

With K=31581660^28 and J=5898050446009651968, the exact coefficient height is

    max((J*K)^2, K*149^(2*N)).

It is K*149^(2*N) for every N>=57, and is strictly smaller than the source height 149^(4*N+2)+1 for every N>=53. These are coefficient thresholds, not effective defining thresholds. No improvement in the variable count is claimed.

The arithmetic claim is inherited only to the extent established for the exact source. This directory does not certify the upstream prime-pattern, pole-realization, elliptic-rank or modular-height foundations, or independent acceptance of their complete assembly.

## Reproduction

```sh
python computation/quartic/balanced214_v24/build.py
python computation/quartic/balanced214_v24/check.py
```

Both programs use only the standard library. The checker imports no producer. It authenticates the reconstructed original coefficient file against its published Git blob, expands all 188 original quadratic squares, verifies all 188 rescaling identities, expands all new squares, and checks every one of the 2919 height-envelope inequalities. A deliberately corrupted coefficient is rejected.

`source/` retains the exact numerical source polynomial, reconstructed quadratic equations and coordinate names. `PROVENANCE.json` identifies the original repository, commit and published artifact. The source 214-variable construction and its arithmetic proofs are credited to the upstream contributors; the contribution here is the coefficient rescaling and its exact proof and verification. No upstream repository was changed.
