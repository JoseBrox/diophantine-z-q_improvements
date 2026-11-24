# An odd second-Pell quotient removes one inverse

The complete ordinary-abc quartic transfer decreases from **675 to 674
rational unknowns**, with **593 quadratic residuals**. All thirteen integer
predicates remain. The construction retains ordinary rational abc and
every arithmetic premise and ineffective sufficient parameter of the
preceding interface, together with the external Jones coding theorem.

The second Pell quotient can always be chosen odd. In the positive
completion, `B=2r+1` is odd and `c=Y_B(a)` is odd. Taking the second Pell
index `q=Bc` gives

```math
i=Y_q(a)/c^2\in 2\mathbb Z+1,\qquad i>1.
```

Replace the formerly certified input `i` by the certified positive integer
`i_half=(i-1)/2`. The actual source value is now `2*i_half+1`, so its
nonvanishing is automatic. The two old rows

```math
i\,i_{\rm inverse}=1,\qquad i_{\rm inverse}E=c^2
```

are replaced by the single quadratic row

```math
E=(2i_{\rm half}+1)C_2,\qquad C_2=c^2.
```

The coordinate `C_2` is the already retained `int_c_29`. Thus the inverse
coordinate and one residual disappear without adding any coordinate.
The old `integer.i.*` row labels and `int_i_reciprocal_*` private names
remain historical role names; those rows now certify `i_half`.

Soundness reconstructs the integer source quotient from `i_half`.
Completeness chooses the odd positive Pell quotient and then rebuilds the
simultaneous elliptic witnesses for the new integer tuple. This is
equivalence on the **instance projection**, not a same-coordinate lift
preserving the old `i`-certificate witnesses.

The full proof is [odd_pell_quotient.pdf](odd_pell_quotient.pdf), with
[TeX source](odd_pell_quotient.tex).
The complete sparse table, its deterministic builder and its independent
verifier are included. Run from the repository root:

```sh
python -B undecidability/odd_pell_quotient_v104/build_odd_quotient.py
python -B undecidability/odd_pell_quotient_v104/verify_odd_quotient.py
```

The independent audit checks all 592 unaffected rows under the explicit
coordinate renaming, the one changed and one deleted row, every occurrence
of the old quotient and inverse, all coordinates and coefficient domains,
and exact finite Pell fixtures. The quantified theorem is proved in the
manuscript. There is no unconditional rational undecidability assertion.
