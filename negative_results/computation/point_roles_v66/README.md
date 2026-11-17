# Restrictions on elliptic point-role couplings

The [paper](../../papers/integer_labels/point_role_restrictions_20261117_v66.tex) proves a finite-menu quadratic obstruction for the full general source, a scalar-reference obstruction, three individual obstructions for exact multiplication witnesses, and a finite-menu obstruction for pairs of independent fixed group words. It also proves the shifted Lucas congruence and states the additional joint-realization problem precisely. No reduced defining-polynomial count is asserted.

## Reproduce the algebra checks

Python 3 with SymPy is required. Run from this directory:

```sh
python check.py --output certificate.json
```

The checker verifies the conic determinant; a universal resultant identity, including degree-drop strata; the coefficient degrees for a fully generic quadratic relation; squarefreeness of the scalar-contact product; the fixed prime's good split reductions; the universal Lucas matrix identity; and exact integral specializations checked independently by matrix powering and recurrence.

The certificate concerns those algebraic identities and finite specializations. The external arithmetic premises, the infinite-input obstruction proofs, and the unresolved joint prime and real realization are not certified by these computations.
