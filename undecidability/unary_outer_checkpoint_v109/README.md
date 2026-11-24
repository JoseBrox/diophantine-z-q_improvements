# Three outer powers and a quadratic central-binomial test

**Status: a proved outer-circuit lemma and a bounded source-dependency
checkpoint. This is not a complete polynomial source, not a rational
undecidability witness, and not a new variable bound.** The exponential
graphs and their lower circuits remain uncompiled.

## Primary source and scope

Jones and Matiyasevich, *A new representation for the symmetric binomial
coefficient and its applications*, Ann. Sci. Math. Quebec 6 (1982),
81–97, Theorem1 and pp.87–89, reduce the source to functions `M,A` of
one unbounded integer. They write `2A+1=(E1-E2)/(E3-E4)`, with
`E3>E4`, and use a large power-of-two base. Their final signed-exponent
clearing uses five outer powers. The source is unary exponential;
the underlying exponential functions still require polynomial
compilation. [Primary paper](https://www.labmath.uqam.ca/~annales/volumes/06-1/PDF/081-097.pdf).

The lemma below is an independent exact derivation with a stronger size
margin. It retains only three outer exponential values and uses six
rational auxiliaries in four quadratic equations.

## Exact outer lemma

Let `A,M` be nonnegative integers and `P` an integer satisfying

```math
P\ge4A+6+4M.
```

Set

```math
U=2^P,\qquad V=2^M,\qquad W=2^{P(2A+1)}.
```

Then

```math
V\mid\binom{2A}{A}
```

if and only if there exist an **integer** `y` and rational
`K,T,D,r1,r2,r3` satisfying these four quadratic equations:

```math
\begin{aligned}
K-Vy&=0,\\
T-KU+4K&=0,\\
D-W+KT&=0,\\
T^2-4D^2-r_1^2-r_2^2-r_3^2&=0.
\end{aligned}
```

Thus the outer inequality requires six rational auxiliaries beyond
`U,V,W,y`. The integrality of `y` is essential and remains an external
requirement. The displayed power equalities are also external
requirements; they are not consequences of these four quadrics.

### Proof of the rounding equivalence

Write

```math
Q=\sum_{j=0}^{A}\binom{2j}{j}U^{A-j},\qquad
t=\frac{U^A}{\sqrt{1-4/U}}.
```

The binomial series and `binom(2j,j)<=4^j` give

```math
0<t-Q<\frac{4^{A+1}}{U-4}<\frac18.
```

The last inequality follows from the stipulated margin. Also `V|U`,
so `Q=binom(2A,A) mod V`.

The four equations imply `K=Vy` and

```math
\left|t^2-K^2\right|\le |K|/2.
```

Here `K=0` is impossible because `W>0`. Putting `k=|K|` gives

```math
|t-k|\le\frac{k}{2(t+k)}<\frac12.
```

Since `t=Q+R` with `0<R<1/8`, the only integer `k` this close is
`Q`. Hence `V|Q`, proving soundness.

Conversely, assume `V|Q` and take `y=Q/V`, `K=Q`,
`T=Q(U-4)` and `D=W-Q^2(U-4)`. Since `Q>=1`,

```math
0<t^2-Q^2=2QR+R^2<Q/4+1/64<Q/2.
```

Thus `S=T^2-4D^2` is a positive integer. It remains to prove that
three squares suffice; an arbitrary positive rational need not be a
sum of three rational squares.

### Why three square auxiliaries suffice

Let `nu=v2(binomial(2A,A))`. Since the central coefficient is at
most `2^(2A)`, `nu<=2A<P`. The congruence `Q=binomial(2A,A) mod U`
therefore gives `v2(Q)=nu`. Moreover

```math
v_2(U-4)=2,\quad v_2(T)=\nu+2,
\quad v_2(D)=2\nu+2,
```

because `v2(W)=P(2A+1)>2nu+2`. Write
`T=2^(nu+2)T0`, `D=2^(2nu+2)D0`, with `T0,D0` odd. Then

```math
\frac{S}{2^{2\nu+4}}=T_0^2-2^{2\nu+2}D_0^2
\equiv
\begin{cases}
5\pmod8,&\nu=0,\\
1\pmod8,&\nu\ge1.
\end{cases}
```

Legendre's three-square theorem applies to the positive integer `S`.
Choose integer, hence rational, `r1,r2,r3` whose squares sum to it.
This completes the equivalence. The use of three squares rests on this
valuation argument, not on an unrestricted positivity assertion.

## Three outer powers from the source's signed exponents

Suppose the source functions satisfy

```math
\mathcal D=E_3-E_4\ge1,\qquad
E_1-E_2=(2A+1)\mathcal D,
```

with `E1,E2,M` nonnegative integers. Define

```math
C=2E_1+4M+4,\qquad P=C\mathcal D,\qquad H=C(E_1-E_2).
```

Then `H=P(2A+1)` and `P>=4A+6+4M`, so the lemma uses just
`V=2^M`, `U=2^P`, `W=2^H`. The added constant four supplies the
stronger margin. Subtractions are harmless in a later polynomial
circuit once their nonnegative integer values have been proved.
This observation does not encode any of the three power graphs.

## Why one exponential input does not follow from one exponent variable

The author's book construction uses geometric sums with first-level
values `2^p` and `2^((2p+2)(z+1)^k)` for `1<=k<=m+1`, where
`p` is a nonconstant polynomial for fixed source parameters; see
§6.3, pp.101–105, especially (15)–(17) and (44)–(49).
[Author's book page](https://logic.pdmi.ras.ru/~yumat/H10Pbook/);
[primary book text, scanned copy](https://djvu.online/file/ooxCpSGldzPAC).

The following algebraic observation gives a precise limitation on
arithmetic-only sharing. If integer polynomials `p1,...,pd` are linearly
independent over the rationals modulo constants, the sequences
`2^p1(n),...,2^pd(n)` are algebraically independent over `Q(n)`.
Indeed, expand a proposed polynomial relation into terms
`f_alpha(n) 2^(sum alpha_j p_j(n))`. Distinct exponent polynomials
differ nonconstantly. Order them by their eventual growth; the unique
largest dominates every other term exponentially, while the nonzero
polynomial coefficients have only polynomial growth. Division by that
largest term yields `1+o(1)`, contradicting a relation on all sufficiently
large integers.

For the displayed family the degrees are `deg(p),deg(p)+1,...,deg(p)+m+1`,
so this criterion applies. Consequently those particular intermediate
values cannot all be recovered by rational arithmetic from fewer than
`m+2` arbitrary generators over `Q(z)`. This is **not** a lower bound
on the integer predicates of every possible Diophantine construction:
a different source or a relation with additional existential freedom
is not covered by the observation. It explains why the three-unknown
unary theorem cannot simply be counted as three polynomial integer
inputs.

## Verification and next step

```sh
python -B undecidability/unary_outer_checkpoint_v109/verify_outer.py
```

The checker verifies the quadratic degree, symbolic source exponent
identities, exact rounding inequalities and divisibility for finite
fixtures, and the three-square residue criterion. Its one fully explicit
fixture is `A=M=0,P=6`: `U=W=64,V=1,y=K=1,T=60,D=4`, with
`(r1,r2,r3)=(0,40,44)`.

A future quantitative transfer must first compile all lower exponential
values and all three outer power graphs with proved integer-domain
hypotheses, then account for their complete rational auxiliary systems.
No such compilation or numerical improvement is claimed in this
checkpoint.
