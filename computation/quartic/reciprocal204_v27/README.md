# 204-variable quartic

The full arithmetic proof is `papers/quartic_existence/quartic204_20261114_v27.tex`; the positive weighted trace supplier is `papers/trace_heights/weighted_trace_20261114_v27.tex`. All counts include the input. The sufficiently large defining parameter is ineffective; N=57 concerns coefficient height only.

Run `build.py`, then `check.py` and `check_arithmetic.py` from this directory, or use `python -B scripts/verify_v27.py --authenticate-sources` from the repository root. The independent checker reconstructs all 186 quadratic rows and all 3046 coefficient profiles in each presentation, including the 22 rescaling rows, and rejects deliberately corrupted data. The arithmetic checker verifies identities and bounded prime/preparation examples, not the infinite arithmetic hypotheses.

The balanced and unbalanced presentations have the same rational input projection for every fixed N. The new point domain includes half-integral indices and finite torsion differences; the complete height and completeness arguments are supplied in the papers, not inferred from row counts.
