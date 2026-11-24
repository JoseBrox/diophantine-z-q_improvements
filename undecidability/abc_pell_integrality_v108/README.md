# One half-trace square replaces the c integer predicate

The complete ordinary-abc quartic transfer now has **605 rational unknowns
and 528 quadratic residuals**, with **twelve integer predicates**. This
saves forty coordinates and thirty-six residuals from the checked 645/564
predecessor. Its sum of squared residuals has degree exactly four.

The improvement uses a proved arithmetic theorem: if `a` is an integer
divisible by three, then

```math
d^2-(a^2-1)c^2=1,\qquad d-(a-2)c\in\mathbb Z,\qquad
\zeta^2=2\bigl(ad+(a^2-1)c+1\bigr)
```

forces both `c` and `d` to be integers. It covers positive, negative,
and zero `a`. The theorem is proved in
`../pell_integrality_replacement_v106/pell_integrality_replacement.tex`.

The source already forces `3 | a` before assuming `c` integral. Its
remaining integer inputs recover the integral prefix
`n=q^16`, `M=q^32`, `r=S*(M-n)+T*(M-1)`, and
`a=(w*M+1)*r*s*M`. Modulo three, either `M=0` or `n=M=1` and `r=0`.
This avoids using the source's later power-of-two reconstruction.

The compiler deletes the whole `c` elliptic integer block except its
still-used square register. That register is renamed `source_c_square`
and retained as the ordinary source equation `source_c_square=c^2`.
Using the existing `ac=a*c` coordinate, the only new row is the quadric

```math
\zeta^2-2ad-2a(ac)+2c-2=0.
```

All twelve remaining integer blocks, shared point fields, shared reference
equations, and surviving contact offsets remain unchanged. The exact
occurrence audit removes 41 private coordinates and 37 residuals, then
adds one coordinate and one residual: **605/528**.

Soundness first recovers the twelve remaining integer inputs, then uses
the new Pell theorem to recover `c,d`, and finally applies the existing
source soundness proof. Completeness uses the canonical positive Pell
witnesses and `zeta=2*X_(r+1)(a)`, then chooses simultaneous elliptic
witnesses. The equivalence concerns the source instance; it does not
assert a same-auxiliary-witness lift to the removed `c` block.

Ordinary rational abc, all retained arithmetic-interface premises, the
ineffective sufficient coefficient, and the externally cited Jones coding
theorem remain required. The new c-integrality theorem is proved, rather
than introduced as another assumption. No unconditional rational
undecidability claim is made.

## Files and reproduction

- `abc_c_integrality.tex` and its PDF: complete application proof and counts.
- `c_integrality_abc_quadrics.json`: every variable and quadratic residual.
- `c_integrality_abc_certificate.json`: metadata, hashes, and occurrence audit.
- `build_abc_integrality.py`: deterministic compiler from frozen 645/564.
- `verify_abc_integrality.py`: independent verifier, without compiler import.
- `independent_verification.json`: exact audit receipt.

Run from the repository root:

```sh
python -B undecidability/abc_pell_integrality_v108/build_abc_integrality.py
python -B undecidability/abc_pell_integrality_v108/verify_abc_integrality.py
```

The checker compares all 526 unchanged rows, the retained square row,
and the new half-trace; audits every occurrence of all 41 removed
coordinates; checks shared point and contact interfaces; independently
interprets ten prefix rows; checks all 27 residue cases modulo three,
three symbolic denominator identities, and 32 exact half-trace fixtures;
and verifies coefficient ring, support, degree, counts, and hashes.
