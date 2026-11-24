# Common physical point chart: a 656-variable presentation

The explicit ordinary-abc transfer in this directory has **656 rational
unknowns and 575 quadratic residuals**, reduced from its 674/593 odd-Pell
predecessor. All thirteen integer predicates remain. Its sum of squared
residuals has degree exactly four. The ordinary rational abc assumption,
retained arithmetic source premises, ineffective sufficient parameter,
and externally cited Jones coding theorem are unchanged.

The earlier common-numerator theorem permits one physical point `U` for
all input blocks. Its whole point chart can now be shared. With
`S=y(U)/x(U)`, `F=1/x(U)`, and private fields `t,G,h`, only two private
field quadrics are needed:

```math
A=(h+S+t)F-Gh=0,\qquad
B=\Delta(F+G)-(S-t)h+t^2=0.
```

The shared curve equation is `C=F*S^2+Delta*F^2-1=0`. The old scale row
is redundant by the exact polynomial identity

```math
Gh(S-t)-\Delta FG-1=C-FB-(S-t)A.
```

Another identity recovers the private curve equation. Both reciprocal
abscissas are nonzero, and tangent fibers and zero ordinates are covered.
A common reference quotient `sigma=v_H/w_H` changes the second reciprocal
relation to `sigma*conjugate(L_i)=weight_i*G_i`, where the scalar
`weight_i=c_i*X_i^2` costs only one rational coordinate. This avoids a
private scaled reciprocal field.

Every new rational zero has a polynomial lift to the complete predecessor:

```math
s_i^{\rm old}=X_iS,\quad F_i^{\rm old}=X_i^2F,\quad
G_i^{\rm old}=c_iX_i^2G_i,\quad
h_i^{\rm old}=X_ih_i,\quad d_i^{\rm old}=c_iX_i^3G_ih_i.
```

The retained scaled `t` and half-trace have explicit quadratic equations.
No division by `X_i` occurs, so soundness includes zero input fibers.
Completeness reselects the simultaneous physical points using the previous
common-numerator theorem; it preserves the source instance rather than
every arbitrary predecessor auxiliary witness.

For `k` inputs, the tuple construction has **44k+22 coordinates and
39k+17 rows**, saving `2k-8` coordinates and rows from the preceding
common-reciprocal presentation. For `k=13`, the eighteen-coordinate and
eighteen-row saving gives **656/575** after the odd-Pell refinement.

## Files and reproduction

- `common_point_rechart.tex` and its PDF: complete algebraic proof, source
  projection, edge cases, counts, and retained-hypothesis scope.
- `point_rechart_abc_quadrics.json`: every coordinate and quadratic row.
- `point_rechart_abc_certificate.json`: deterministic metadata and hashes.
- `build_point_rechart.py`: deterministic compiler from the frozen v104 table.
- `verify_point_rechart.py`: independent check, without importing the compiler.
- `independent_verification.json`: exact audit receipt.

Run from the repository root:

```sh
python -B undecidability/abc_point_rechart_v105/build_point_rechart.py
python -B undecidability/abc_point_rechart_v105/verify_point_rechart.py
```

The independent verifier checks 197 old row interpretations, 179 new or
changed rows, all 396 unchanged rows, every occurrence of all 132 removed
coordinates, eight universal field identities, coefficient ring, support,
degree, counts, and hashes. It does not certify the retained arithmetic
premises or a sufficient numerical defining parameter.
