# Scoped follow-up on the new 68-coordinate quartic table

Source inspected: `computation/quartic/abc68_v65/build.py` and its generated quadratic table. No construction below 68 coordinates was found in this review.

## New chart, with notation separated from the reference block

Write `p=h+s+t`, `delta=betaFourth`, and `a0=Re(hp)`. The new six-field block is

```math
d=pF,\qquad d=hG,\qquad
D(F+G)-(s-t)h+t^2=0,\qquad
\delta-d(s-t)+DFG=0.
```

Its rational height output is `a0=Re(hp)`. Only that component is used. The deletion of the imaginary output in the current table is exact and exhausts the unused-output opportunity.

## Direct deletion of the product field d

Substituting `d=hG` and using the secant row gives the exact identity

```math
\delta=G(t^2+DG).
```

Similarly substituting `d=pF` gives `delta=F(s^2+DF)`. Both leave a cubic curve row. The existing comparison-square helpers do not immediately fix it: for example

```math
t^2=I_2+2T_Ht-T_H^2,
```

where `T_H` is affine in the reference coordinates. The resulting products `G*T_H*t` and `G*T_H^2` remain cubic. No bilinear identity removing these products is supplied by the new table.

## Direct deletion of the rational height output

The sole defining row is `a0=Re(h(h+s+t))`. Its remaining consumer is the term `4*a0^2` in the detector argument. Direct substitution produces a quartic residual.

There is a simple exact obstruction to representing this square by a quadratic polynomial in the remaining **chart** coordinates modulo its displayed equations. Set

```text
s=t=F=G=d=delta=0,
h=r (r rational).
```

All four field equations hold, while `a0=r^2` and `a0^2=r^4`. A quadratic polynomial in the remaining chart coordinates specializes to a polynomial of degree at most two in `r`, and cannot equal `r^4`. This remains an obstruction after allowing the existing comparison-square outputs: on this specialization those outputs are the fixed reference squares, independent of `r`. Products J,K vanish. Reference variables may be fixed at any valid reference point.

This argument concerns polynomial output identities for direct elimination. It is **not** a lower bound for all alternative quadratic presentations, nor an obstruction after localization at the input `X`, since the displayed specialization has `delta=X=0`.

## Immediate Laurent substitutions

The existing scalar units are the detector inverse weights. Multiplying coordinates and rows by their Laurent monomials does not change the number of factors from nonunit chart coordinates in a monomial. In particular it cannot lower `G*t^2` below cubic degree or the pure `h.0^4` term below quartic degree. Holding those units fixed also preserves the preceding one-parameter obstruction.

The reference quantities `u_H,w_H,v_H` are units in the quadratic field, but their individual rational components are not certified units. A field-valued substitution would require a new simultaneous rewrite of the reference, product and comparison rows; it is not an immediate use of the current scalar-unit rescaling. The substitutions `F=(v_H/u_H)J` and `G=(v_H/w_H)K` transfer the difficulty into higher products, without a verified coordinate saving.

## Conclusion and scope

The new table is concretely blocked for the immediate deletions inspected: the unused imaginary output has already been removed; deleting d leaves cubic curve terms; deleting the real output leaves a genuine quartic output square; existing scalar-unit Laurent rescaling does not change those degrees. A further saving would need a new quadratic chart identity, a nontrivial field-unit rewrite, or a different height expression with its own arithmetic proof. No broader optimality or impossibility claim is made.
