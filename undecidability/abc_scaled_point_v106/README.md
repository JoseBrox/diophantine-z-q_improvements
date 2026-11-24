# Directly scaled private points: 645 variables

This complete ordinary-abc transfer has **645 rational unknowns and 564
quadratic residuals**, with all thirteen integer predicates retained. Its
sum of squared residuals has degree exactly four. The ordinary rational
abc assumption, retained arithmetic premises, ineffective sufficient
parameter, and externally cited Jones coding theorem are unchanged.

This is a fresh, reproducible construction from the frozen 674/593
odd-Pell table. It surpasses the earlier quoted 649-variable count; it
does **not** claim to recover that unavailable artifact or establish
which transformations the earlier artifact used.

The new step keeps the private ordinate ratio and chord input-scaled:
`T=X*t` and `H=X*h`. A shared field `SF=S*F` and private field `Z=X*H`
make the pair equations quadratic:

```math
(H+T)F+X(SF)-GH=0,\qquad
\Delta X_2(F+G)-SZ+TH+T^2=0.
```

The retained half-trace is directly
`Re(H^2+S*Z+H*T)`. Thus the unscaled ordinate field, its two scaling rows,
the unscaled half-trace, and its scaling row are unnecessary. Relative
to the preceding 656/575 presentation, the net saving is one coordinate
and row per input, at a global cost of two: **eleven coordinates and rows
for thirteen inputs**.

For unrestricted symbolic field variables, write
`A=(H+X*S+T)*F-G*H`,
`B=Delta*X^2*(F+G)-(X*S-T)*H+T^2`, and
`C=F*S^2+Delta*F^2-1`. The exact identity

```math
GH(XS-T)-\Delta X^2FG-X^2=X^2C-FB-(XS-T)A
```

recovers the old scale equation. All removed old coordinates have a
polynomial reconstruction, without dividing by `X`. Therefore every new
rational zero lifts **directly to the complete 674/593 predecessor**, even
at zero inputs. The map is not asserted to pass through every auxiliary
fiber of the intermediate 656-coordinate system.

Completeness uses the same simultaneous physical numerator theorem and
the source's positive integer completion. No new prime, approximation,
contact or pole condition is imposed. The tuple interface has **43k+24
coordinates and 38k+19 rows**.

## Files and reproduction

- `scaled_private_points.tex` and its PDF: complete proof, zero-input
  lift, arithmetic scope, and exact counts.
- `scaled_point_abc_quadrics.json`: every coordinate and quadratic row.
- `scaled_point_abc_certificate.json`: metadata, occurrence audit, and hashes.
- `build_scaled_point.py`: deterministic compiler from the frozen v104 table.
- `verify_scaled_point.py`: independent verifier, without compiler import.
- `independent_verification.json`: exact audit receipt.

Run from the repository root:

```sh
python -B undecidability/abc_scaled_point_v106/build_scaled_point.py
python -B undecidability/abc_scaled_point_v106/verify_scaled_point.py
```

The checker verifies 197 old row interpretations, all 168 new or changed
rows, all 396 unchanged rows, every occurrence of all 106 removed
coordinates, nine universal field identities, coefficient ring, support,
degree, counts, and hashes. Its scope is algebraic verification; it does
not certify the retained arithmetic premises or a numerical defining
coefficient.
