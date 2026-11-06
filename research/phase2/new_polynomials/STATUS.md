# Frozen source status

The preferred sources are **source-43-conic.json.gz** and
**source-45-conic-semilocal.json.gz**. They retain respectively 42 and 44
coordinates and have maximum finite-algebra ranks 2^29 and 2^30. Their final
indexed polynomials, degree/height bounds and passing independent checks are
in the corresponding **../finite_fibre/** packages.

The complete arithmetic proof is assembled from **shared_source.tex**,
**scalar_preparation_zero.tex** and **degree_refinements.tex**. The preferred
sources use comparison order 64, beta order 16 and scalar order 48.
They share the scalar-height point, fix the scalar preparation at zero,
use nonzero square scales and parametrize all ten first pole conics.

The separate quartic construction uses comparison order 52 and scalar order
32, with a stronger size anchor. Its final tables use 1367 and 1391 total
variables. The source's earlier scalar preparation coordinate is retained
there because its quadratic evaluation is cheaper.

All these arithmetic interpretations assume the explicit source lemmas and
Sun's simultaneous prime-pattern theorem, arXiv:2610.20691v2, Theorem 4.1.
The exact source and compiler checks do not certify those arithmetic inputs.
The supplied proof establishes the new conclusions from the stated inputs.

The README files, final-source-manifest.json, individual verification receipts
and the aggregate phase2 receipt identify the final artifacts. Earlier source
variants are retained only as comparison constructions. No commit has been made.
