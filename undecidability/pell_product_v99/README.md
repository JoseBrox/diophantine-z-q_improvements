# One product identity removes one coordinate

The retained identity a=(U+1)*sr replaces p=2*U*sr2 by
p=2*a*sr-2*sr^2. Delete sr2 and its square definition.
This is an exact polynomial equivalence, including every zero branch,
with the unique inverse lift sr2=sr^2.

| Interface | Variables | Quadratic residuals |
|---|---:|---:|
| General | 972 | 826 |
| Specified | 1146 | 996 |
| Ordinary abc | 696 | 591 |

The predecessor arithmetic premises, instance ranges and Jones coding
theorem remain unchanged. No new integrality or nonzero assumption is
introduced. The complete proof is pell_product_elimination.tex.

Rebuild and check:

    python undecidability/pell_product_v99/build_product.py
    python undecidability/pell_product_v99/verify_product.py

The checker imports no builder and checks the polynomial identities,
every changed and unchanged coefficient row, support, degree, metadata
and hashes. Each interface has its complete coefficient table and
certificate in this directory.
