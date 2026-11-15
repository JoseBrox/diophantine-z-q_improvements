# Local solubility of every shared pole parameter

Companion paper: [Local solubility at every shared pole parameter](../../../papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex).

Run from the repository root:

```bash
python computation/pole_parameters/shared_parameter_local_v41/check.py
```

Use `--output /absolute/path/report.json` for a temporary report. The default is `verification.json` beside the checker.

For every prepared original pole input `b=d t^2` and every rational `tau`, the quartic

```text
D = 17 d
C = 17(17-b)
e = (tau^2-D)/(tau^2+3D)
q^2 = D(s^2-eC)(s^2+3eC)
```

has points at every completion of the rationals. The proof treats every prime, including the bad primes and conic-denominator primes. Smooth local points yield infinitely many affine witnesses avoiding zero ordinates and finite polynomial guards. Thus any finite prepared family can use any one rational `tau` locally.

The exact verifier checks the symbolic identities and discriminant, all 7704 unit quartics over its twelve specified prime fields, and 19008 local valuation branches. It gives complete bad-prime local certificates for four concrete prepared examples, including the published old fixed-parameter global counterexamples. An input with a negative odd valuation at 409 verifies that dropping the square-denominator hypothesis can destroy local solubility.

The verifier reconstructs all four current arithmetic circuits and audits their v40 norm specifications. The sole pole-stage guard factor depending on `tau` but not `s` is the conic denominator, which is nonzero at `tau=0`; the reconstructed first ordinate is not stored or guarded. Earlier point-algebra guards are assumed. The saved report binds the specification files by SHA-256.

The universal local result is proved in the paper, not inferred from the finite grid. It does not prove simultaneous rational realization and does not lower a polynomial's variable count. Its exact global reformulation asks for prescribed abscissa square classes on correlated quartic-twist elliptic families.
