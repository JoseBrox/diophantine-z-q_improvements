# Single-cover algebra and height audit

Date: 16 November 2026. This checkpoint records proved algebraic consequences
and a source-scope audit. It does not assert the open rational realization
needed for a nine-variable definition.

## Arbitrary even inner exponents

The retained source `direct_input13_20261110_v22.tex`, Lemma `powers`,
explicitly proves its binary-power estimate for every even exponent `e`
with `alpha_e=e/kappa-3>0`. Its scope is not restricted to its numerical
examples `e=4,6`. Thus the proposed `e=8,10,16` uses are allowed.

For `m>1`, replace

`t=(beta^e+T^e)^(d m)+z^2`

by

`t=(beta^(e m)+T^(e m))^d+z^2`.

Both have the same formal degree `e d m`. The new binary-power coefficient
satisfies

`alpha_(e m)=m alpha_e+3(m-1)>m alpha_e`,

so the sufficient soundness coefficient strictly decreases. This modifies
the arithmetic realization problem; it preserves the soundness method and
census, not a completeness theorem that has yet to be proved.

The formal support of `(beta^(e m)+T^(e m))^d` is a subset of that of
`(beta^e+T^e)^(d m)`. At matching terms the inequality
`binom(d,k)<=binom(d m,m k)` follows, for example, by mapping a choice of
`k` blocks among `d` disjoint blocks of `m` objects to the union of those
blocks. The same nonnegative coefficient comparison survives substitution
`beta=X^2+B` when `B>0`. No automatic comparison is asserted after
substituting an arbitrary signed rational expression for `T` and clearing
its denominators.

The exact verification script certifies these `m=1` rows:

| kappa | e | d | C | alpha times gamma | q | e d |
|---|---:|---:|---|---|---|---:|
| 25/24 | 8 | 6 | 288/19 | 4914/625 | 10000/5187 | 48 |
| 16/15 | 10 | 6 | 18 | 153/16 | 32/17 | 60 |
| 121/100 | 16 | 12 | 2763/232 | 91538/14641 | 40453083/21236816 | 192 |

Here `epsilon=d-kappa(d/2+2)>0`, `gamma=8/kappa-6>0`, and every `q<2`.
The input degree of the formal height term is twice the last column.
No finite optimization over all exponents is claimed by this child audit.

## Reciprocal-trace form of the single radical

Write `W=A+B sqrt(2)`, `N=A^2-2B^2`, `g=1+w`, and

`D=g^2 N-2g A+1`.

The native radical is

`R=(1-Tr(W^-1)/g+N(W^-1)/g^2)(1+(1-Tr(W^-1)/2)/w)`.

Set

`S=w(g N-A)/D=(w/2) Tr(W/(gW-1))`.

Exact simplification gives

`R=S [D/(w g N)]^2`.

On the prepared real locus, each real slot of `W` is at least one and
`w>0`. For a slot `x>=1`, the summand `w x/(g x-1)` is positive and at
most one, so `0<S<=1`. The upper endpoint occurs at `W=1` in both slots.
All displayed denominators are nonzero there. At an odd bad contact,
the leading behavior of `S` is `w/g`, retaining the local obstruction.

This is a useful equivalent actual square test, not a solution of it.
Both cleared square conditions have the same square class represented by
`w(gN-A)D`, so no genus or determinant-degree decrease follows merely
from the rewrite.

## New source-scope findings

Sun, arXiv:2610.20691v3 (11 November 2026), Theorem 4.1 and Proposition
5.1 concern the simultaneous primes `u+c_j w^2` with unrestricted `u`.
They include the required Gaussian congruences and cross-reduction-order
conditions but do not specialize `u` to a second binary quadratic form.
Consequently they do not supply the contacts
`a^2+(c-theta)b^2` forced by `t=c+z^2`. No 11- or 9-variable
completeness claim follows from that theorem as stated.

Burungale, arXiv:2611.16130v1 (12 November 2026), Theorem B supplies the
simultaneous congruent-number twists used in `prepared_burungale_pole.tex`.
The source's complete integer definition does not supply a numerical
variable bound: its Section 7.3 uses a DPRM encoding of a recursive
exponential relation. Its square-denominator block, after preparation
and conic parametrization, does give the explicit two-coordinate block
proved in the accompanying note. This improves the available arithmetic
inputs and gives a small concrete radicand, while retaining two free
coordinates per pole block.

## Remaining arithmetic gap

No proof currently constructs, for every integer input, actual elliptic
point indices and a rational `z` for which the prescribed trace/norm
single-cover radical is a rational square. Local squares at a finite
set of primes, a parametrization with free `W`, and a prime-pattern
result with unrestricted numerator do not supply that conclusion.
