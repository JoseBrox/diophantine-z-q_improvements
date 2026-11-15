# A 196-variable quartic with 176 quadratic squares

The complete rational zero set is unchanged from the pinned 196-variable parent. The complete paired formal-parameter ratios imply three stored reciprocal curve equations, so their six rational components are deleted. There remain 196 total coordinates, 176 primitive integral quadratic rows and 2853 coordinate monomials in the quartic.

`quadratic.json` and `polynomial.json` use the unbalanced coefficient A=149^(2N+1). The `balanced-` tables use C=149^N and have the unchanged exact height

    11903780636513165769654680680436132271178681610029854792 * C^2

for every N>=1. The source arithmetic premises and its ineffective sufficient defining threshold are unchanged. Counts include the input; N is fixed.

From the repository root:

```sh
python -B computation/quartic/paired_redundancy196_v40/build.py
python -B computation/quartic/paired_redundancy196_v40/check.py
```

The independent checker authenticates the parent tables, verifies all 176 remaining rows, reconstructs the six removed curve components, checks the two universal defect identities, and independently expands all quadratic squares. It verifies that each coefficient profile stays nonzero for every C>=149, the uniform height majorant and its attainment. The full proof is `papers/quartic/quartic196_redundancy_20261115_v40.tex`; the paired-ratio theorem is in the companion elliptic-chart paper.

No decrease in variable count, numerical defining threshold, or independent audit of the external arithmetic premises is claimed.
