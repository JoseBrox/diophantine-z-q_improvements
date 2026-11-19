# Amplified rationality descent and ten-coordinate encoding

This package audits and extends **Hector Pasten and Xavier Vidaux,
arXiv:2611.24748v1**. The new constructions define **Q inside a fixed
number field K**. They assume positive elliptic rank stable from Q to
K, the stated six-point truncated-height inequality (supplied by abc
over K), and the published class-seven prepared pole theorem.

The amplified descent has a transparent sixteen-coordinate realization.
The finite-algebra compression reduces it to **ten total K-coordinates**:
one input, four elliptic abscissas, four pole parameters and one encoder.
The full polynomial is a finite determinant specification; it is not
fully expanded. Its exceptional correction is ineffective.

## Files and read-only checks

- `independent_check.py` and `independent_certificate.json`: exact
  multiplier menus, cubic divisor, pole clearing, valuation identities,
  height margins and the sixteen-coordinate census.
- `compression_check.py` and `compression_certificate.json`: scalar
  source clearing, monic rank-64 algebra, primitive separator bound,
  guarded shifted encoder, zero-eigenvalue case and nonsplit triangular
  root reconstruction.
- `proof_review.md` and `manual_review.json`: the separately reviewed
  amplified descent and source dependencies.
- `compression_proof_review.md` and `compression_manual_review.json`:
  the universal ten-coordinate equivalence, class-seven density and
  source pins.
- `tex_review.json` and `tex_review10.json`: final manuscript layout
  receipts; these are separate from mathematical verification.

From the repository root:

```sh
python -B computation/number_fields/pasten_vidaux_v81/independent_check.py
python -B computation/number_fields/pasten_vidaux_v81/compression_check.py
python -B scripts/verify_v81.py
```

The fixed field selector gives counts 10N for Z inside K and
10N[K:Q] for the ring of integers when an N-coordinate definition
of Z over Q is supplied. Its arithmetic assumptions remain in the
composition. For the project's eleven-coordinate source these are
110 and 110[K:Q]. That source originates in **notes of Gabe Conant
with Astra 6.2**, with the subsequent audits and extensions identified
in its own paper.

No result here lowers the 25/11 counts over Q or the 165/180 general
quartics. No finite certificate proves the external arithmetic inputs
or a uniform numerical effective bound.
