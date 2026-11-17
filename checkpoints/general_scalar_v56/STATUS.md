# Scalar precision transfer checkpoint

## Latest complete intrinsic-pole transfer

The preferred same-count transfer is
`burungale_scalar_transfer_20261117_v56.tex`:

\[
\rho_L=A_Lr/(1+C_Lr)^2
\quad\longmapsto\quad
\rho_L^*=7A_Lr/(1+7C_Lr)^2.
\]

It keeps the original normalized physical weights and uses the
intrinsic degree-nine pole equation directly at `d=b`. It covers
both retained general scalars and either v53 or corrected order-two
scalar tests. It is a complete 25-coordinate transfer under the
remaining source premises and Burungale Theorem B, with no new
small-variable theorem or numerical determinant-degree bound.

`check_scalar_seven_transfer.py` and
`scalar_seven_transfer_certificate.json` pass. The consumed-prime
certificate enumerates every one of 76249 residues for each scalar.
The independent auditor uses polynomial gcds instead of enumeration;
its receipt and certificate are in
`../single_cover_realization_v56/general_source_transfer_independent_audit.md`
and `../single_cover_realization_v56/scalar_transfer_independent_certificate.json`.
The manuscript compiles cleanly in three passes.

The earlier coherent physical-weight transfer
`burungale_general_transfer_20261117_v56.tex` is also proved, but
is an alternative to the simpler scalar-only transfer. The larger
constant tuning in `scalar_constant_seven_transfer.md` is unnecessary.
Only the scalar-only version is proposed as the current polished result.

`conditional_burungale_independent_audit.md` records a passing audit
of the other agent's simplified 13-coordinate intrinsic-pole transfer.

## Fixed finite squareclass menus

`finite_squareclass_menu_audit.md` proves the native local obstruction
and finite one-encoder disjunction for any fixed finite positive
S-unit squareclass menu. Its exact discriminant checker passes.
The formal 21/9 censuses are preserved, but the required actual
rational realization remains unproved.

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
