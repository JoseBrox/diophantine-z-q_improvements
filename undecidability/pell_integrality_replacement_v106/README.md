# A half-trace square replaces the c-integrality predicate

**Proved arithmetic replacement; complete-table counts are to be supplied
by the separate compilers.** This checkpoint removes an arithmetic need
for a c-integrality predicate, with one restored rational half-trace
square. It makes no numerical claim by itself.

The key lemma is unconditional:

> If `a` is an integer divisible by three and rational `c,d,zeta` satisfy
> `d^2-(a^2-1)c^2=1`, `T=d-(a-2)c` is an integer, and
> `zeta^2=2(ad+(a^2-1)c+1)`, then `c,d` are integers.

The first norm and integral shifted trace make `den(c)` divide `4a-5`.
The half-trace square has the same reduced denominator as `c`, because

```math
8(2a^2-2a-1)+3=(4a-5)(4a+1),\qquad 3\mid a.
```

Thus `den(c)` is a square. The rational Pell classification rules out
every nonintegral square denominator for both signs of `a`. The zero
case is also covered. The complete proof is in
[pell_integrality_replacement.pdf](pell_integrality_replacement.pdf)
and its [TeX source](pell_integrality_replacement.tex).

## The source already supplies the needed multiple of three

Write the integral prefix in its current form

```math
n=q^{16},\quad M=q^{32},\quad
r=S(M-n)+T_0(M-1),\quad a=(wM+1)rsM.
```

If `3|q`, then `3|M`. Otherwise `n=M=1 mod3`, so `3|r`.
In both cases `3|a`. This uses the preliminary integrality of `q,S,T_0`
and the retained integer inputs `w,s`; it does not require recovery of
the exponent of `q`, or integrality of `c`.

The current first linear row gives
`d-(a-2)c=bw+(4a-5)gamma`, an integer. Therefore restoring the single
quadratic row

```math
\zeta^2-2ad-2aA_c+2c-2=0,\qquad A_c=ac,
```

allows soundness to infer `c` integrality directly. The register `A_c`
already exists in the relevant tables. A compiler deleting the c chart
must separately retain its borrowed `c^2` register and any other live
dependencies.

For completeness, the canonical positive witnesses have
`c=Y_(2r+1)(a)`, `d=X_(2r+1)(a)` and permit
`zeta=2X_(r+1)(a)`. This is the same half-trace row deleted in v101.
All remaining arithmetic-interface and source-coding premises stay in
force. Completeness must rebuild elliptic witnesses for the reduced
integer-input tuple.

## The sharper signed classification

For `a=-A<=-2`, the preceding finite seed classification simplifies to
the two seeds

```math
(c,d)=(0,1),\qquad
\left(\frac3{4A+5},\frac{5A+4}{4A+5}\right),
```

and one extra seed

```math
\left(\frac2h,\frac{2A+1}{h}\right)
\quad\text{only if }4A+5=h^2.
```

Every rational solution with integral shifted trace is a signed Pell-unit
translate of one of these seeds, with its c denominator unchanged.
When `3|A`, `4A+5=2 mod3` is nonsquare, so the third seed cannot occur;
the second seed's denominator is exactly `4A+5`, also nonsquare.

## Verification and scope

```sh
python -B undecidability/pell_integrality_replacement_v106/verify_replacement.py
```

The checker compares the simplified negative seed formula against the
independent square test in the preceding classifier, verifies exact
denominator and coefficient identities, checks the prefix congruence,
and validates half-trace completions on exact Pell fixtures. Its
certificate distinguishes this quantified arithmetic theorem from any
separate full-table variable-count claim.
