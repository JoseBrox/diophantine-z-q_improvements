# Rationality of the varying-input pole surface

This package verifies the exact algebraic formulas in
[`varying_input_quadric_20261116_v44.tex`](../../../papers/pole_parameters/varying_input_quadric_20261116_v44.tex).

For fixed `D>0` and rational `tau != 0` with `tau^2 != D`, set

```text
e = (tau^2-D)/(tau^2+3D),
p = -4D*tau/(tau^2+3D).
```

The surface

```text
Q^2 = D*(u^2-e*(289*V^2-D))*(u^2+3e*(289*V^2-D))
```

is birational over the rationals to the smooth quadric

```text
x^2-D*y^2 = e*(sigma^2+3D),
```

which has the rational point `(x,y,sigma)=(tau,1,tau)`. The paper gives full
inverse maps, their exact open loci, projection from this point, and a
rational curve with finite nonzero pole ordinates and input tending to zero
through positive rational values. Products for fixed positive weights and a
common first-conic parameter are rational.

## Verification

Python 3 and SymPy are required. From the repository root, run:

```bash
python computation/pole_parameters/varying_input_quadric_v44/check.py
```

This reproduces the complete report and compares it byte for byte with
`certificate.json`. To write a regenerated report to another **file**, use:

```bash
python computation/pole_parameters/varying_input_quadric_v44/check.py --output /tmp/varying-input-quadric.json
```

All birational and open-locus identities are checked by exact polynomial
remainders modulo the appropriate defining equation. The checker also tests
the projection parametrization, native positive-input curve, an exact
rational example, and incorrect-sign controls.

## Scope

The scale `V` is freely variable here. The native pole input is
`b = D/(17*V^2) = 4w/V^2`, where `w = D/68`. Prescribing `V` by an existing
elliptic detector adds equations that this rationality result does not solve.
The package asserts no lift to that prescribed detector, no solution for an
arbitrarily fixed `V`, and no smaller complete defining polynomial. The
explicit curve verifies real smallness and the rational square class; other
finite-prime preparation conditions remain separate.
