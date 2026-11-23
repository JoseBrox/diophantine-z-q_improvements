# Independent follow-up review: two height tests and the weak-abc transfer

23 November 2026. This review concerns the completed manuscript
`research/height/bb_two_tests_three_squares.tex` and the two eleven-variable
weak-abc routes in
`papers/conditional_few_variables/weak11_audit_and_transfer_20261119_v78.tex`.
It records an independent mathematical review, rather than an independent
recalculation of the native finite-algebra degree receipts.

## 1. Two tests, power amplification, and direct quadratic relations

**Verdict: the stated implications and their hypotheses pass review.**
The aggregate-trace argument is a transfer of the existing project method,
not a new general height theorem. The relevant external input is von
Buhren, Theorem 1.1, p. 308, independently checked in the
[published primary paper](https://www.numdam.org/article/JTNB_2017__29_1_307_0.pdf).
The local and scalar inputs remain those of Bhargava–Burungale,
[arXiv:2611.16130v2](https://arxiv.org/html/2611.16130v2), Sections 3–5.

### Positive aggregate trace, including zero indices

For `F=Q(sqrt(13))` and `d=(1+sqrt(13))/2`, the coefficients
`d_+=d` and `d_-=-d^sigma` are positive at the chosen embedding and
have independent squareclasses over `F(i)`; their product is 3. This
gives independent images of the generator and its conjugate over the
endomorphism ring `Z[i]`. Along a positive-dimensional abelian translate,
two poles in the same block can coincide only with proportional
endomorphism coefficients, so their combined leading coefficient is a
nonzero positive rational sum times a fixed nonzero coefficient. Poles
from different blocks cannot coincide because of independence. Thus the
translate cannot lie in a trace fibre.

The graph closure, fixed finite-rank subgroup, and the symmetric Segre
embedding check the hypotheses of von Buhren's theorem. Zero indices are
removed first and restored by taking maxima over finitely many strata.
The value `x*(O)=0` is a finite disjunction, not an evaluation of `x` at
its pole. The resulting constants `A,J` are independent of the indices.

For every nonzero doubled point the two real abscissas exceed the
corresponding absolute twist parameters. Consequently any nonzero-index
stratum has rational trace `T>sqrt(13)>3`. Hence `h(T)>log(3)` and the
additive error is absorbed by

\[
A_*=A+J/\log 3.
\]

This works also when exactly one of the two squaring indices is zero.
The all-zero case is separate and satisfies the desired relation.
For a fixed quadratic relation, including the extra fixed point `P_0`
in the trace gives the same positive lower bound even when all variable
indices vanish.

### The two-shift contradiction

If `Delta=n_1^2-n_2` is nonzero, then `|Delta|<=S=n_1^2+n_2^2`.
The two BB predicates at `s` and `s+T^k` imply

\[
kh(T)=h(T^k)\le 2H|\Delta|+\log2.
\]

Together with `S<=A_*h(T)`, this is contradictory for
`k>A_*(2H+log 2)`. The fixed power may be a power of two; the exponent
is not made effective. The Green–Tao progression construction works for
any fixed finite collection of rational shifts. Its denominator check
is explicit: each selected prime exceeds both the denominator-clearing
integer and the progression step, and therefore divides neither.

For `F_0` of total degree at most two, the same argument uses
`S=1+sum(n_j^2)` and any proved positive coefficient `C` such that
`|F_0(n)|<=CS`. The coefficient one-norm, increased to one, is a valid
general choice. For multiplication the sharper coefficient `C=1/2`
follows from the exact identities

\[
S-2(n_1n_2-n_3)=(n_1-n_2)^2+(n_3+1)^2,
\]

\[
S+2(n_1n_2-n_3)=(n_1+n_2)^2+(n_3-1)^2.
\]

### Local extraction and witness counts

The extended local predicate has `s+1` Gaussian points in each tuple,
including the reference index `n_0=1`. The logarithm comparison gives
`gamma_0 B_j=gamma_j` and `delta_0 C_j=delta_j` modulo the prescribed
prime-power, without presupposing integrality of the ratios. Since
`gamma_0+delta_0=1` and `B_j=C_j` to that precision, it follows that
`B_j=n_j` to that precision, and in particular `B_j` is integral.
Evaluation of `F_0` is therefore legitimate. Zero numerator points have
zero indices and ratios; the nonzero reference denominators remain
guarded.

At a selected prime, the Frobenius choices
`U_j=[(1-pi)/2]P_j`, `V_j=[(1+pi)/2]P_j` work for all indices,
including zero. There are still six selected primes, independent of
the number of polynomial inputs. The factor count per tuple is exactly
`2(s+1)+s+1=3(s+1)`. Thus the two squaring tests use 36 auxiliary
Gaussian points, direct multiplication uses 48, and three squaring
calls use 108 rather than the original 270. These are point counts,
not final rational-variable counts.

### Three-square interval

The displayed doubled point has coefficient valuations `-2,-3` at
2. They persist on a fixed coset of finite index whose real image is
still dense. For every integer `q`, the chosen positive interval
product `(q-a)(b-q)` therefore has 2-adic valuation `-5`, which suffices
for a sum of three rational squares by the three-square theorem.
No extra coset condition is imposed on the definition of `T`; the coset
is used only to select complete witnesses. Soundness follows from the
sign of the sum of squares. Consequently `r+19` becomes `r+18` for the
same quadratic presentation of `T`. The unspecified `r` remains
unspecified, so this does not give a new numerical project record.

## 2. The two weak-abc eleven-variable routes

**Verdict: the normalized BB product transfers to both routes without
an additional arithmetic hypothesis.** The existing assumptions on
`W_kappa`, the elliptic group and index charts, trace height, and the
prime-pattern theorem remain in force. The old level-17 pole converse
is replaced by the BB converse rather than retained as an extra input.

The two parameter choices are `(kappa,e,k)=(121/100,6,6)` and
`(16/15,4,5)`. Keep all contact forms, the scalar `u`, the six physical
tests, the balance factors, `W`, and `V=Tr(W^{-1})` unchanged. In the
notation of the existing proof,

\[
b=\frac{4u}{(1+u)^2V^2}.
\]

Write the existing exact extraction as `b=d_old t^2`. Replace the old
pole block by

\[
e_{\rm BB}=7b=d_{\rm new}t^2,\qquad d_{\rm new}=7d_{\rm old},
\]

\[
Y^2=(1-e_{\rm BB})(v^4-d_{\rm new}^2)(s^4-d_{\rm new}^2).
\]

The variables called `e` in the contact-power choice and
`e_BB` in this paragraph are different quantities.

### Completeness

The existing proof establishes `u/z^8 -> 1`, `W -> 1`, `V -> 2`,
and `b z^8 -> 1` at every fixed place as `z` becomes large there.
Before the prime selection, include 7 in the temporary prepared set
and require `v_7(z)<0` with sufficient size. Then

\[
v_7(b)=-8v_7(z)>0
\]

is even, so `v_7(7b)` is positive odd and causes no denominator
obstruction. Outside 7, multiplication by 7 preserves valuation
parity; the existing proof already supplies the square denominator of
`b` at every prime. Thus `7b` also has square reduced denominator.

At 2, take the original square neighbourhood with positive even depth
at least four. It gives `b in Q_2^{times 2}`, hence
`7b in 7 Q_2^{times 2}` with the same depth. Real largeness of `z`
strengthens the old bound to `0<b<1/7`. Therefore

\[
0<e_{\rm BB}<1,\qquad
e_{\rm BB}\in7\mathbb Q_2^{\times2},\qquad
v_2(e_{\rm BB})\ge4,
\]

with square denominator, exactly as required by BB Lemma 2.2.

These local and real restrictions are compatible with the old order
of choices: the stated prime-pattern input allows arbitrary fixed
finite-place congruences, chosen before the contact primes. Point
neighbourhoods may be kept fixed while `z` becomes sufficiently large;
an identically zero physical test contributes a factor one. No
additional prime-pattern theorem is required.

### Soundness and finite-algebra scope

The old fixed exceptional set contains 7. At every consumed positive
odd prime outside it, `v_p(7b)=v_p(b)`. BB square-denominator soundness
therefore gives exactly the old inequality

\[
0<v_p(b)\le\nu+2q_*.
\]

All six local tests, the congruence `X=n mod p`, the radical estimate,
and the constants `lambda=8374/14641` and `99/160` are unchanged.
The sufficient fixed input shift remains ineffective, as before.

The split normalization `d=d_0/(P+Q^k)^2` remains legitimate because
`P+Q^k>0` is recovered at the rational character in the established
order. BB witness density supplies finite-parameter avoidance for
guards that remain nonzero after substitution. At other point-algebra
characters, `e_BB=1` gives zero terminal radicand; this is allowed by
the existing terminal-zero encoder. No new global `1-e_BB` guard is
justified or needed.

The old denominator `tau^2+51d` belongs to the removed conic chart.
It is absent from the BB product block, so the guard receipt must be
rebuilt from the new native source; its old deleted-atom classification
must not be carried over without checking. The two retained pole
coordinates and one terminal square generator keep the free-variable
and finite-rank counts unchanged. Any improved degree bound requires
the separate exact compiler verification.

## 3. Common-squareclass sharing is not a completed route count

The finite-support twist manuscript now explicitly defines retained
parameters and supplies a uniform coefficient construction using only
existing inputs and finite square roots. Its `h+1` count is the number
of free coordinates before finite-algebra elimination. Rationality of
the square choices must still be imposed, and the appropriate encoder,
new generators and guards must be checked on every character. A
denominator `1-d_a` can vanish at another character, independently of
the retained parameters; density cannot repair such a fixed zero.
The all-complements-square specialization similarly has zero retained
free coordinates only when its zero ordinates and extra guards are
allowed. Neither statement alone subtracts variables from a complete
route.
