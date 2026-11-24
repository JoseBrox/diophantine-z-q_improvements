# Source frontier: a different exponential source and an integral-trace lemma

**Status: proved local lemmas and a source-research checkpoint. No complete
quartic table is changed, no integer predicate is deleted, and no numerical
undecidability bound is improved by this checkpoint.**

The latest complete predecessors remain the v102 general and specified
tables and the v101 ordinary-abc table. Their arithmetic-interface premises
and the external Jones coding theorem remain in force. In particular this
note makes no unconditional claim about Hilbert's tenth problem over Q.

## 1. A genuinely different classical source to investigate

Jones and Matiyasevich, *A new representation for the symmetric binomial
coefficient and its applications*, Ann. Sci. Math. Quebec **6** (1982),
81–97, prove in Theorem 1 that every computably enumerable set has a
singlefold representation by an inequality in two natural-number unknowns,
using addition, multiplication and iterated fixed-base exponentiation.
The base may be 2. Adding an additive slack gives an equation in three
unknowns. Their construction makes only one unknown occur in exponents;
the other two may be bounded by functions of that unknown. The paper also
limits exponentiation nesting to two levels.

Primary source, inspected 24 November 2026:

- [Author paper, publisher PDF](https://www.labmath.uqam.ca/~annales/volumes/06-1/PDF/081-097.pdf),
  especially pp. 81–85 and the observation after equation (23), p. 89.

This is a potential alternative to the present many-integer Jones source.
It is **not** yet a two- or three-input polynomial source. Each exponential
value must still be represented polynomially, including all necessary
integrality, index, sign and nonzero conditions. Neither the number of
such certificates nor a shared certificate for their values has been
derived here. Accordingly no quartic count follows.

An actionable next step is to reconstruct one fully explicit universal
instance of this unary-exponential representation and make a dependency
graph of its exponentials. The fact that only one variable occurs in
exponents may permit more sharing than arbitrary independent power
predicates. The existence of a small quantified formula alone does not
establish that sharing.

### A separate literature qualification

Bayer and David explicitly distinguish the proved classical pair
`(58,4)` over the natural numbers from Jones' advertised intermediate
pair `(32,12)`, for which they report no published proof. Their exact
warning is in section 1.3, immediately after Theorem 1 of
[arXiv:2505.16963v1](https://arxiv.org/html/2505.16963v1).
The mathematical companion is
[Bayer–David–Haßler–Matiyasevich–Schleicher, arXiv:2506.20909v1](https://arxiv.org/html/2506.20909v1).
The smaller entries in a historical table should therefore not become
unqualified project inputs without their constructions being recovered.
The present checkpoint does not reconstruct the full Jones 1982 paper.

## 2. An integral first trace would already force c to be integral

The current first Pell block has

```math
d=(a-2)c+T,\qquad d^2-(a^2-1)c^2=1,
\qquad T=bw+(4a-5)\gamma.
```

The v102 checkpoint shows that integral `a,T` alone do not force rational
`c,d` to be integral. A stronger useful fact is the following.

**Proposition.** Suppose `a,T,d` are integers, `|a| >= 2`, and `c` is
rational. If the two displayed equations hold, then `c` is an integer.
Conversely, if `a,T,c` are integers, the linear equation makes `d` an
integer. Thus, within this block and with its other integer inputs
retained, certifying `c` and certifying `d` are equivalent.

Here is an elementary proof, including the exceptional prime 3.
Write `c=u/v` in lowest terms, `v>0`. Since `(a-2)c=d-T` is integral,
`v | a-2`. Since `(a^2-1)c^2=d^2-1` is integral,
`v^2 | a^2-1`. Reducing the latter integer modulo `v` gives
`v | 3`. Hence either `v=1` or `v=3`.

We exclude `v=3` using the next lemma. This also avoids assuming any
extra congruence of the source's `a` or `q`.

**Lemma (small denominators in an integral-trace Pell equation).**
Let `A>=2` and `d` be integers. If `c` is rational with reduced
denominator at most 3, and

```math
d^2-(A^2-1)c^2=1,
```

then `c` is integral. The bound 3 is sharp: `A=7,d=2,c=1/4`
satisfies the norm equation.

**Proof.** It remains to consider denominators `v=2,3`. Put
`Delta=A^2-1`. The norm equation implies `v^2 | Delta`.
We may replace `d,c` by their absolute values. If `c` is nonintegral,
then `c>0`, and

```math
lambda=d+c\sqrt{Delta}>1,\qquad
epsilon=A+\sqrt{Delta}>1.
```

Choose an integer `k>=0` so that `1 <= lambda epsilon^(-k) < epsilon`,
and write this unit as `d'+c' sqrt(Delta)`. Multiplication by
`epsilon^(-1)=A-sqrt(Delta)` transforms a pair into

```math
(d,c)\longmapsto (Ad-Delta c,\ Ac-d).
```

It preserves the properties `d in Z` and `c in (1/v)Z`, because
`v | Delta`. It cannot turn a nonintegral `c` into an integral one:
the inverse multiplication has integer coefficients. The norm is still
1. The chosen real interval consequently gives `0<c'<1` and integral
`d'>=1`.

For `v=2` the only possibility is `c'=1/2`. Its equation is

```math
(2d'-A)(2d'+A)=3.
```

The positive factors must be `1,3`, forcing `A=1`, a contradiction.
For `v=3`, the possibilities are `c'=1/3` or `2/3`, giving respectively

```math
(3d'-A)(3d'+A)=8,\qquad
(3d'-2A)(3d'+2A)=5.
```

In the first equation the factors have the same parity, so they are
`2,4`; in the second they are `1,5`. Both force `A=1`. This proves
the lemma and the proposition. The sharpness example follows from
`4-48/16=1`.

The equivalence does not yet remove a predicate: the present complete
source has no independent proof that `d` is integral after the `c`
predicate is removed. It supplies a more flexible target for further
reconstruction arguments. In particular, one need only recover the
first trace's integrality; it is unnecessary to exclude every rational
denominator of `c` directly.

### Why a monic rechart is attractive, and what it loses

If the first linear row instead had the form

```math
d=ac+T\quad (a,T\in\mathbb Z),
```

then substituting in the norm gives

```math
c^2+2aTc+T^2-1=0.
```

Every rational root of this monic integer polynomial is integral, so
both `c` and `d` would be integral without either predicate. This is a
valid local lemma. It is not a valid replacement of the present block:
the coefficient `a-2` is what makes the expression

```math
X_j(a)-(a-2)Y_j(a)\equiv 2^j\pmod{4a-5}
```

recover the power of two. With coefficient `a`, the expression becomes
`X_j(a)-aY_j(a)=-Y_(j-1)(a)` instead. A new exponential/binomial
certificate would be needed to use the monic row. Simply changing the
coefficient would invalidate the old proof.

## 3. What the power-of-two requirement contributes

For nonnegative integer `n`, let `s_2(n)` denote the number of ones in
its binary expansion. The exact identity

```math
v_2\binom{2n}{n}=s_2(n)
```

follows directly from
`v_2(n!)=sum_(j>=1) floor(n/2^j)=n-s_2(n)`.
In particular, multiplying `n` by `2^h` merely shifts its binary
digits and preserves the valuation of this central binomial coefficient.

**Proposition.** For a positive integer `b`, the identity

```math
v_2\binom{2bn}{bn}=v_2\binom{2n}{n}\qquad\text{for every }n\ge1
```

holds if and only if `b` is a power of 2 (including `b=1`).

**Proof.** Powers of 2 preserve binary digit count. Conversely, set
`n=1`; the asserted identity gives `s_2(b)=1`, which characterizes
positive powers of 2.

Thus a general even base cannot silently take the place of a binary
shift base. For example `b=6,n=1` gives valuations 2 and 1. Jones'
coding prefix uses powers of the base, and the classical binomial
methods relate divisibility to digit information. The current corrected
source explicitly retains the power-of-two condition from Jones 1980,
Theorem 2.

This identifies an exact arithmetic obstruction to carrying over a
binary-shift argument unchanged. It does **not** prove that the
power-of-two condition is logically independent of all other equations
in that specific complete source. No full-prefix non-power-of-two
counterexample, and no theorem making the condition redundant, has
been established here. Removing it would require one of those issues
to be resolved by an additional source argument.

## 4. Reproducible checks and next steps

Run from the repository root:

```sh
python undecidability/source_frontier_v103/verify_source_frontier.py
```

The independent checker verifies the two polynomial substitutions,
the denominator descent identities, finite rational Pell examples
including the sharp denominator-4 counterexample, and the binomial
valuation identity by direct integer computation. The quantified proofs
are given above; the finite checks are not extrapolated into those proofs.

Next directions are (i) a compact simultaneous certificate for the
unary-exponential source, (ii) obtaining the first trace's integrality
from other retained source rows, and (iii) designing a different
binomial certificate whose linear norm row is monic. None is presently
claimed to meet the target near 263 quartic variables.
