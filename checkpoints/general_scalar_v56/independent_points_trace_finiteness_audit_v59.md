# Independent audit: arbitrary point tuples at a fixed slope

**Verdict: PASS for the full extension.** The geometric proof applies
to all independent point roles in the conditional and general sources,
using the first detector block. It does not require the point relations
`U=[n]H`, a rank-one assertion, or density of a chosen cyclic subgroup.
The curve itself has the endomorphism property needed for the proof.

The author's manuscript is
`../independent_route_v56/negative_results/fixed_slope_elliptic_trace_finiteness_v59.tex`.
The independent exact finite checks are
`check_independent_trace_finiteness_v59.py` and
`independent_trace_finiteness_v59_certificate.json`.
The final rewritten manuscript, including all independent point roles
and removal of the rank premise, was reread in full. No mathematical
correction remains outstanding.

## 1. Exact rational endomorphism ring

Put `K=Q(sqrt(2))`, `d=3-sqrt(2)`, and `d'=3+sqrt(2)`.
The two conjugate elliptic curves have equations

\[
E_d:y^2=x^3-d^2x,\qquad E_{d'}:y^2=x^3-(d')^2x,
\qquad dd'=7.
\]

Their geometric endomorphism rings are `Z[i]`. The automorphism
corresponding to `i` is `(x,y) -> (-x,iy)`, so all geometric
endomorphisms are defined over `K(i)`. Since `K` is real, complex
conjugation fixes exactly the integer multiplications. Therefore
`End_K(E_d)=End_K(E_d')=Z`.

The explicit isomorphism over `K(sqrt(7))` is

\[
\phi(x,y)=\left(\frac{7x}{d^2},
                    \frac{7\sqrt7\,y}{d^3}\right).
\]

The coefficient identities proving it maps one displayed curve to
the other were checked exactly in `Q(sqrt(2))`.

Seven is not a square in `K(i)`. Indeed, if `(a+bi)^2=7` with
`a,b in K`, then `ab=0`. The case `a=0` is impossible because
`K` is real; the other case would make seven a square in `K`.
Writing an element of `K` as `r+s*sqrt(2)` then forces either
`r^2=7` or `s^2=7/2`, neither possible over `Q`.

Consequently an automorphism fixing `K(i)` changes `sqrt(7)` to
its negative, sends `phi` to `-phi`, and fixes every CM
endomorphism. Every geometric homomorphism from `E_d` to `E_d'`
has the form `phi` followed or preceded by a CM endomorphism.
A homomorphism defined over `K` would equal its negative and hence
vanish. Thus both cross homomorphism groups over `K` are zero.

For `A=Res_{K/Q} E_d`, the canonical base change is
`A_K=E_d x E_d'`, and hence

\[
\operatorname{End}_K(A_K)=\mathbb Z\times\mathbb Z.
\]

Galois interchanges the factors. Its invariant endomorphisms are
exactly the diagonal integer multiplications, giving

\[
\boxed{\operatorname{End}_{\mathbb Q}(A)=\mathbb Z.}
\]

Poincaré complete reducibility now implies that `A` is simple over
`Q`: otherwise `End_Q(A) tensor Q` would contain a nontrivial
idempotent. This derivation is independent of any Mordell–Weil rank
claim about the source curve. It also gives
`Hom_Q(A,B)=Hom_Q(B,A)=0` for every elliptic curve `B/Q`.

## 2. Rational abelian directions and the parity test

Every positive-dimensional rational abelian subvariety of `A^r`
contains the image of a map

\[
R\longmapsto([a_1]R,\ldots,[a_r]R),\qquad a_i\in\mathbb Z,
\]

with a nonzero primitive integer vector. To see this, choose a
simple factor by complete reducibility, identify its isogeny type
with `A`, and compose an isogeny from `A` with the inclusion.
The coordinate maps are integers because `End_Q(A)=Z`. Dividing
their common gcd does not change the image abelian subvariety,
since integer multiplication on `A` is surjective as a morphism.

The conditional reciprocal tests include the point roles
`H`, `U`, and `U-A0`. In role order `(A0,H,U)`, their linear
forms span all three coordinates modulo two.

The general tests include `H`, all `U_i`, and all `U_i-Q_i`.
In the nine-role order `(Q1,Q2,Q3,Q4,H,U1,U2,U3,U4)`, these
linear forms span all nine coordinates modulo two: the `U` rows
give their coordinates, and subtracting the difference rows gives
each root coordinate.

Thus every primitive direction has at least one tested point whose
coefficient in that direction is odd. The independent checker
verifies the two matrices have ranks three and nine modulo two and
checks all `7+511=518` nonzero direction-parity vectors. Fixed point
offsets such as `P` do not enter the direction matrix.

## 3. Nonconstancy on every relevant translate

Fix the input, the slope, and all fixed defining parameters. Use
block zero, whose physical weight and comparison scale are then
positive constants independent of every point role. Every detector
factor on the real function domain is at least one. For any tested
point `T`, in each real slot there is a fixed constant `c>0` with

\[
W_\sigma\ge1+c f(T_\sigma)^2,
\qquad f=1/x.
\]

The same assertion holds for conjugated reciprocal tests, since they
merely interchange the slots. The other comparison and scalar
factors cannot weaken this lower bound.

Take a rational translate of an `A` direction through a guarded
point. Choose a tested point with odd coefficient `m`. On that
direction it has the form `T0+[m]R`. Odd multiplication is surjective
on the real points of each elliptic curve: it is surjective on the
identity circle and on the component group, whose order is at most
two. Hence one may choose real `R` so that this tested point tends
to `(0,0)` in both real slots. Its reciprocal abscissas become
unbounded, forcing

\[
0<V=\sum_\sigma W_\sigma^{-1}\longrightarrow0.
\]

At the starting guarded point `V>0`. The trace is therefore not
constant on that translate.

All guard restrictions are handled correctly. Because the translate
passes through a guarded point, none of its restricted denominators
vanishes identically. A finite union of the resulting proper
algebraic subsets has empty interior in each real open neighborhood
of the smooth parameter surface. It can therefore be avoided while
approaching the target real point. The path need not remain in the
doubled-point component: it tests a rational-function identity on
the entire abelian translate, for which any real open subset is
Zariski dense.

The fixed-coefficient condition is essential. The second detector
block can depend on root heights; it is unnecessary for this proof.
The first block alone is sufficient.

## 4. Mordell–Lang for the full independent tuple

Let `B` be the fixed elliptic trace model, with nonconstant trace
coordinate `g`. Close the guarded incidence `V(H1,...,Hr)=g(Q)`
inside `A^r x B`. Apply Mordell–Lang to the finitely generated
rational group of that product.

An infinite relevant coset has a rational point in the guard domain.
The identity component of the Zariski closure of its underlying
rational subgroup is a positive-dimensional abelian subvariety
defined over `Q`. If its projection to `A^r` is zero, it is the
elliptic factor and would force `g` to be constant. Otherwise
complete reducibility supplies an `A` direction. The projection
of that direction to `B` is zero because there are no rational
homomorphisms from `A` to `B`. The incidence would then make
`V` constant along its translate, contrary to Section 3.

As in the restricted-tuple proof, boundary-only cosets contribute no
guarded points. A coset meeting the guard domain meets it in a
nonempty open subset, so it gives exactly the forbidden constant
identity. The set of all guarded rational tuples is consequently
finite at each fixed input and prepared slope.

This applies with `r=3` to the conditional source and `r=9` to the
general source. It allows all rational points on the trace elliptic
curve, not only multiples of a known section. Imposing the second
trace equation or using a fixed finite menu of genus-one models
preserves finiteness.

## Scope and remaining routes

The theorem does not say that any of these finite sets is empty.
It does not bound them effectively or uniformly in the slope.
It does not cover the untwisted trace conic, nor a curve whose
coefficients depend on the varying point tuple. A fixed coefficient
such as `c=lambda` is covered once the slope has been fixed.
Joint variation of slope and independent auxiliary indices remains
outside the theorem.

No realization theorem or new defining-variable count follows from
this obstruction. The exact checker certifies the finite algebraic
and parity inputs only; the finiteness conclusion follows from the
full mathematical argument.

The primary Mordell–Lang and complete-reducibility references were
independently reopened and recorded in
`fixed_slope_finiteness_independent_audit_v59.md`.
