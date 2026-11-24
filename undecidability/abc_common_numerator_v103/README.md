# Common numerator: 675-variable ordinary-abc quartic

The complete ordinary-abc undecidability transfer drops from **695 to 675
rational variables**, retaining all thirteen integer predicates. There are
**594 quadratic residuals**, whose sum of squares has degree exactly four.
All arithmetic premises of the previous 56-coordinate integer interface,
ordinary rational abc, its ineffective sufficient coefficient, and the
externally cited Jones coding theorem remain required.

The simultaneous construction shares one physical numerator point `U`
and keeps private `V_i=U-[n_i]R0`. The all-sign prime-order CRT, including
arbitrary prime-power accuracy and the inherited half-generator halving
lemma, makes this compatible with every input's comparison primes. The
fixed differences and dyadic contact offsets are preserved.

The existing chart's input-scaled point coordinates remain private.
The saving instead comes from the reciprocal-product fields. Their common
part is `X_i^2*J`, where `J=f(H)f(U)`. Replace the two old fields by

    old_U_i = X_i^2*J + L_i
    old_V_i = X_i^2*J - L_i.

One private field `L_i` replaces two. The three common fields
`J`, `E=v_H*J`, and `K=J^2` cost six rational coordinates. The old product
is `X_i^4*K-L_i^2`, which is quadratic using the retained fourth-power
register. The first product uses `X_i^2*E`; the second uses `L_i`.
Thus the net saving is `2k-6`, or twenty coordinates for `k=13`.

For any `k`, this proves a tuple construction with **46k+14 coordinates
and 41k+9 rows**, improving the preceding 48k+8 count when `k>3`.
Soundness covers every rational zero, including zero input values.
Simultaneous completeness is proved for nonzero integer tuples, which
suffices because the corrected source reselects positive witnesses.
There is no claim of a bijection with arbitrary predecessor witnesses.

The algebraic compression works over any fixed finite-dimensional
commutative rational algebra with its multiplication table: if its dimension
is `d`, replacing each such pair of fields by one private element and three
common elements saves `d*(k-3)` rational coordinates and adds `2d` quadratic
component equations. The same difference-of-squares and reconstruction
identities prove it. This statement is only about polynomial presentations;
it supplies no new arithmetic completeness theorem over other fields.

## Files and reproduction

- `common_numerator.tex`: full arithmetic preparation, quadratic rechart,
  exact reconstruction identities, counts, and retained-hypothesis scope.
- `common_numerator_abc_quadrics.json`: every coordinate and quadratic row.
- `common_numerator_abc_certificate.json`: deterministic metadata and hashes.
- `build_common_numerator.py`: deterministic compiler from the frozen v101 table.
- `verify_common_numerator.py`: independent audit, with no compiler import.
- `independent_verification.json`: receipt for the exact audit.

Run from the repository root:

```sh
python -B undecidability/abc_common_numerator_v103/build_common_numerator.py
python -B undecidability/abc_common_numerator_v103/verify_common_numerator.py
```

The independent checker verifies all 78 changed rows by explicit polynomial
identities, all 512 unchanged rows, four common definitions, complete
coordinate occurrences, inherited square/fourth-power equations, coefficient
ring, degree, support, counts, and hashes. It does not certify the retained
arithmetic premises or an effective defining parameter.
