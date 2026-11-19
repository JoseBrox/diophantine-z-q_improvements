# One derivative contact: 59-variable ordinary-abc quartic

This package reduces the audited ordinary-abc quartic from 62 to **59 total
variables**, including the input. It retains the translated-secant chart and
shared detector originating in notes of **Gabe Conant with Astra 6.2** and audited
in v78. The single derivative contact, uniform rational normalizer and derivative
register elimination are subsequent project work.

The complete proof is
[single_derivative59_20261119_v79.tex](../../../papers/quartic_existence/single_derivative59_20261119_v79.tex).
All defining claims retain its explicitly listed elliptic, formal comparison,
trace-index, simultaneous prime-pattern and simultaneous-twist premises, in
addition to ordinary rational abc. The finite check does not establish those
premises or an effective sufficient shift.

## Complete specification

The polynomial is the sum of the **51 quadratic residual squares** in
`quartic59/quadrics.json`. Its full expanded coefficient list is
`quartic59/polynomial.json`. The two contact slots use an extra derivative
identity on their zero fibers; their additional rows are not claimed to be
algebraically independent.

For every positive integer parameter `B`, the polynomial has degree 4, content
one, 873 coordinate monomials, and exact coefficient height

```math
H(F_B)=\max\{22838305425411,B^2+4092\}.
```

Every sufficiently large odd `B` gives integer input projection under the stated
premises. This sufficient threshold is ineffective. The coefficient formula is
separate from that threshold.

The three key changes are:

1. A single derivative quotient at the midpoint
   `a=(B+X^8+T_sc^2)^4` combines input and trace heights. It requires one native
   pole block, instead of two.
2. The normalizer `g=(1+uD^2)/(1+u^3D^2)` preserves extraction at positive odd
   valuations of `u` and makes negative odd valuations harmless for **arbitrary**
   actual auxiliary-point denominators. A denominator argument valid only for
   previously fixed points would not suffice.
3. The two identities `tG'-8G=P_6(t)` and
   `(4t^2+a_6)G'-32tG=Q_6(t)` eliminate the separate cubic-power registers.
   Here `a_6=-102`; the identities have no common exceptional fiber, including
   `t=0`.

## Reproduction

From the repository root, with Python 3.12 and SymPy 1.14.0:

```sh
python -B computation/variable_reductions_v79/abc/build59.py
python -B computation/variable_reductions_v79/abc/check59.py
```

The builder uses exact integer sparse arithmetic. The independent checker does
not import the builder: it reconstructs the retained physical chart from the
pinned parent, derives the new equations, and expands the polynomial separately
with SymPy. `quartic59/maps.json` records the precise retained-coordinate map,
the new coordinates, the contact shifts, and the parent file hash.

The polynomial accepts all source zero, tangent and finite torsion fibers
covered in the proof. No rational one-parameter specialization of the intrinsic
pole surface is asserted. This package does not lower the separate
eleven-variable unbounded-degree count or establish the proposed nine-variable
actual-realization theorem.
