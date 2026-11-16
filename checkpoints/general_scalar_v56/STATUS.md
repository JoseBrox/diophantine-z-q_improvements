# Scalar precision transfer checkpoint

## Proved revision

`precision_transfer_20261117_v56.tex` gives the full source transfer with
scalar orders `(1,1,1,1,2,2)`, unchanged reciprocal orders one, paired
comparison orders `(1,6,6,6,1,6)`, the truncated logarithm

\[
\ell_8=z(1-2Df^2/5),
\]

and the exact Lucas equation `F(s^2,t,b)=0`. Its relative formal error has
valuation at least eight at first formal depth. The unchanged CRT thus
suffices. The scalar height exponent is `7/6`; the nonzero Lucas-residual
exponent is `7/4`. Both are less than two. Completeness retains the order
of choices, all scalar normalizers, both pole blocks, and every point,
difference, trace, and whole-character guard.

This is a **25-variable source**, under exactly the retained arithmetic
premises. It does **not** prove 21 variables, and no numerical sufficient
exponent or degree bound has been calculated.

## Correction to the earlier depth proposal

The proposed increase of both primary and opposite reciprocal test
orders to three cannot be supplied by unrestricted deeper CRT
preparation. At the explicit split good prime `76289`, both conjugate
minimal formal returns have depth exactly one. Raising both depths to
two forces `76289 | h` and `76289 | h-1`. The exact finite-field and
modulo-square certificate is separate in `depth_obstruction_certificate.json`.
The new logarithmic truncation fixes this problem without altering those
reciprocal orders.

## Reproduction

Run from the workspace root:

```sh
python checkpoints/general_scalar_v56/check_precision_transfer.py
```

The standard-library checker returns `PASS` and writes
`precision_transfer_certificate.json`. It verifies the exact exponents,
formal coefficients, explicit Lucas integer witnesses, prime and point
orders, projective multiplication modulo the prime square, and the two
nonzero first formal returns. These checks support the stated algebra
and counterexample; they do not replace the arithmetic hypotheses of
the source or prove a smaller variable bound.

## Remaining target

To save the scalar point and its paired auxiliary, a new coupling must
both bound the input height and accommodate arbitrary elliptic reduction
orders at scalar contact primes. Merely replacing `S` by the input point
is incomplete. An alternative source or a new arithmetic construction is
still required.
