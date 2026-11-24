# The twelve abc poles already have the BB-native CM form

**No polynomial row or variable changes.** This audit applies to the
frozen **605-variable, 528-row** table in
`../abc_pell_integrality_v108/c_integrality_abc_quadrics.json`, SHA-256
`4cacba002f7537c2c3732fadb00f7961dffc9bfc7fc91ef42740a903bc9b1eb7`.
Its twelve remaining pole blocks are already the native CM equations

```math
e^2+b p^2=1,\qquad e(1-b)=uv,\qquad u^2-v^2=bq^2.
```

The prepared completeness construction satisfies the hypotheses of the
Bhargava–Burungale rational-point theorem, so the former non-CM
pole-realization assumption is unnecessary for these blocks. No `7/9`
change is needed in the abc table: its physical input is already
`b=7*c*tau^2`.

This removes the old non-CM pole-realization premise, including the
Route K / original Theorem 5.3 / Proposition N support for that
realization. It does not prove or remove any other arithmetic interface.
Ordinary rational abc, the retained elliptic-group, comparison,
trace-index, finite-prime-pattern, local-preparation and recurrence
interfaces, the ineffective sufficient coefficient, and the externally
cited Jones coding theorem remain required. No unconditional rational
undecidability assertion is made.

## Exact coordinate dictionary

For each surviving role, let `r_j` denote its stored coordinate
`int_ROLE_j` (with the historical prefix `int_i_reciprocal` for the
certified input `i_half`). Put

```math
c=r_{43},\quad \epsilon=r_{44},\quad \tau=r_{33},\quad
B=r_{34}=7\tau^2,
```

and define the physical pole coordinates by

```math
b=cB,\quad e=cr_{35},\quad u=cr_{36},\quad v=cr_{38},
\quad p=r_{37},\quad q=r_{39}.
```

The stored unit row is `c*epsilon=1`; the two square registers satisfy
`p^2=c*r_40` and `q^2=c*r_41`. Multiplying the three stored pole rows
by `c^2`, and using those retained identities, gives respectively

```math
e^2+bp^2-1,\qquad uv-e(1-b),\qquad bq^2-u^2+v^2.
```

Conversely, any physical CM solution lifts through this dictionary
using the already nonzero `c`, with `r_40=p^2/c` and `r_41=q^2/c`.
No inverse of a pole auxiliary is required. The checker audits every
occurrence of `r_34,...,r_41` and finds no hidden outside guard.

## Elementary pole soundness

These equations exclude every negative odd valuation of `b`, at every
prime. Suppose `nu=v_l(b)<0` is odd. In the first equation the two
summand valuations, when finite, have opposite parity, so the equation
forces `v_l(e)=0`; this also follows directly if `p=0`. The middle
equation then gives `v_l(u)+v_l(v)=nu`, and both factors are nonzero.
If their valuations differed, the last equation would equate an even
valuation with an odd one when `q!=0`. If `q=0`, it directly gives equal
valuations. Either way their sum is even, contradicting `nu`. The
argument includes the prime two and all allowed zero-auxiliary branches.

## Prepared existence without changing the table

The existing common-numerator proof
`../abc_common_numerator_v103/common_numerator.tex`, in its fixed-place
and real preparation paragraph, supplies all of the following
simultaneously for the actual physical inputs:

```math
0<b_i<1,\qquad \operatorname{den}(b_i)\text{ is a square},\qquad
b_i\in7\mathbb Q_2^{\times2},\qquad v_2(b_i)\ge4.
```

Indeed it makes `c_i` a two-adic square of arbitrarily large positive
even valuation and `tau_i` a unit; taking depth at least four is one of
the same finite open conditions. Its normalizer argument proves square
reduced denominators even when the shared numerator has additional
point denominators. Its real limit gives the interval `(0,1)`. Removing
the `c` integer block only omits one contact list and does not affect
these preparations for the remaining twelve blocks.

The prepared-existence proposition in
`../quadratic_reduction_v104/bb_native_combined.tex` applies directly
with `d=b`. Its external input is the rational-point assertion of
[Bhargava–Burungale, Theorem 2.3](https://arxiv.org/html/2611.16130v2):
for the positive squarefree parts `j=sqf(b)` and `k=sqf(1-b)`, the
mutual local square conditions yield points of nonzero ordinate on two
congruent-number twists with the required abscissa squareclass.

Here is the required hypothesis check. Write `b=A/D^2` in lowest
terms. The positive integers `A` and `D^2-A` are coprime, so `j,k` are
coprime. The dyadic preparations give `j=7 mod8` and `k=1 mod8`.
At any odd prime dividing `j`, the number `1-b` is a unit congruent to
one; at any prime dividing `k`, the number `b` is a unit congruent to
one. These are the mutual-square conditions. If `k=1`, write
`1-b=r^2` and take `e=1,p=q=0,u=v=r`; this branch is permitted.

For `k>1`, after scaling the second supplied point, the prepared
existence proposition gives nonzero `a_0,b_0,U,V,n` with

```math
U^2=b^3a_0^4-bn^2,\qquad
V^2=b^3b_0^4-bn^2(1-b)^2.
```

The direct substitutions

```math
e=\frac{n}{ba_0^2},\quad p=\frac{U}{b^2a_0^2},\quad
u=\frac{b_0}{a_0},\quad v=\frac{e(1-b)}u,\quad
q=\frac{V}{b^2a_0b_0}
```

satisfy the three native equations. Each identity is independently
checked symbolically. Private pole witnesses can therefore be supplied
for all twelve prepared inputs using this theorem. There is no further
simultaneous requirement on the pole witnesses and no density argument.

## Reproduction and scope

Run from the repository root:

```sh
python -B undecidability/abc_bb_native_v107/verify_abc_bb.py
```

The standalone checker imports no table compiler. It pins the complete
table hash, reconstructs all **84 literal rows** (seven per pole), audits
private auxiliary occurrences, verifies the three physical scaling
identities and three two-point recipe identities, and checks exact
prepared examples with `b=112/225` and the allowed zero-auxiliary
branch `b=112/841`. These fixtures concern the pole equations and do
not claim to instantiate a complete integer-certificate witness.
The certificate records the count and premise conclusion separately;
the complete 605/528 polynomial table remains byte-for-byte unchanged.
