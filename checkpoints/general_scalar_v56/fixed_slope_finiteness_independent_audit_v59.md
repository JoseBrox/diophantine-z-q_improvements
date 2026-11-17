# Independent audit of fixed-slope elliptic trace finiteness

**Mathematical verdict: PASS.** The audited manuscript is
`../independent_route_v56/negative_results/fixed_slope_elliptic_trace_finiteness_v59.tex`.
The theorem concerns a fixed prepared slope and fixed actual root
roles. It proves finiteness, not emptiness, of the exact rational
trace incidence. It supplies no new defining-variable bound.

## The source surface is simple over the rational field

Let `A=Res_{K/Q} E`, with `K=Q(sqrt(2))`. The retained group
assertion `2E(K)=Z P` implies that `A(Q)` has rank one. The
conjugate-generator independence proved in Section 2 of the weighted
trace paper implies that `Z P` is Zariski dense in `A`.

If `A` were not simple over `Q`, Poincaré complete reducibility over
`Q` would give an isogeny with a product of two elliptic curves.
Rank additivity and total rank one make one factor have rank zero.
A homomorphism from `A` to that factor then sends the cyclic source
subgroup to a finite group, contradicting its density. Thus `A` is
simple over `Q`. A nonzero rational homomorphism `A -> B` to an
elliptic curve would have a positive-dimensional proper connected
kernel, so it is impossible.

Both inputs must be retained: density of one cyclic subgroup alone
does not imply simplicity, and rank one alone does not imply density.
The argument asserts simplicity over `Q`, not geometric simplicity.

## Incidence with a fixed elliptic curve

For a simple rational abelian surface `A`, an elliptic curve `B`, and
nonconstant rational functions `f` and `g` on them, consider the
incidence `f(H)=g(Q)` on the common function domain. Its reduced
closed incidence is a subvariety of `A x B`.

Mordell–Lang applies to the finitely generated group
`A(Q) x B(Q)`. An infinite relevant group coset contains a rational
point `q` in the common function domain. The identity component `G`
of the Zariski closure of its underlying rational subgroup is then a
positive-dimensional abelian subvariety defined over `Q`, and its
translate `q+G` lies in the closed incidence. This is the correct
descent argument even if an initial geometric Mordell–Lang coset was
not defined over `Q`.

The first projection of `G` is zero or all of `A` by simplicity.
In the first case `G=0 x B`. In the second case its connected kernel
is either the elliptic factor, giving the whole product, or zero. In
the latter case it is isogenous to `A`; a nonzero second projection
would give an element of `Hom_Q(A,B) tensor Q`, which vanishes.
Thus the only remaining subgroup is `A x 0`.

A translate of each of these three possibilities through a common
domain point forces at least one of `f,g` to be constant. This is
impossible. Hence the guarded rational incidence is finite.

The domain qualification handles all projective-boundary issues.
A vertical elliptic component may occur over an indeterminacy point
of `f`, but it contributes no common-domain points. If a component
meets that domain, its intersection is a nonempty open subset and
the claimed constant identity follows. No assertion about the
absence of all boundary cosets is needed.

## Nonconstancy of the actual conditional trace

The revised detector uses

\[
W_F=\prod_{i=1}^{6}(1+C_i^2/F),\qquad
V_F=\operatorname{Tr}(W_F^{-1}),\qquad F>0,
\]

and includes `C_1=1/x(H)`. The actual multiplication relation
`U=[n]H`, `A_0=[n]P`, with `n != 0`, is imposed throughout.
Every test in each real slot is real on the rational-function
domain. All factors are at least one, and

\[
0<V_F\le
\sum_\sigma\frac{F}{F+f_0(H_\sigma)^2}.
\]

Approach the real point `(0,0)` in both elliptic slots, avoiding the
finitely many proper denominator divisors. Both reciprocal abscissas
are unbounded, so the right side tends to zero. At a regular real
point, the trace is strictly positive. It cannot therefore be a
constant rational function.

This argument works for every positive rational `F`, not merely a
generic slope. The real path may lie outside the doubled-point
component used for source completeness. That is harmless because it
is used to disprove an identity of rational functions on the surface;
any real open subset of the smooth surface is Zariski dense. The
square-root point chart imposes additional arithmetic restrictions on
rational witnesses but does not change this identity argument.

For the source polynomial

\[
F(t)=t(t+1)(2t+1)(3t+1)(4t+1)(5t+2)/120,
\]

every prepared `t>1` is covered. The same positivity estimate applies
to the general detector only after all its additional root roles,
positive physical weights, and nonzero comparison scales are fixed.

## Curve hypotheses and scope

The three stated small trace tests have smooth genus-one models and
rational reference points for `0<w<=1/4`, as certified in the small
classes paper. Thus the incidence theorem applies to all rational
points on each fixed model, without a restriction to multiples of
its known point. A finite menu of fixed models still yields a finite
union of finite sets.

For the adaptive multiplier with `q=2+w*c^2`, a fixed rational `c`
also produces a smooth genus-one curve in this interval: the conic
factor has negative discriminant `w(w-8)`, whereas the multiplier is
a nonconstant linear polynomial with a real root. They cannot share
a root. The reference trace `V=2` gives a nonzero rational square.
Thus a choice such as `c=lambda` is fixed when the slope is fixed.
A multiplier depending on the varying point tuple is outside this
argument.

The untwisted trace conic is genus zero and is also outside the
incidence theorem. The conclusion does not exclude a finite nonempty
set of exact witnesses, a jointly varying slope and point tuple, or
a point-dependent curve. It excludes using an unbounded auxiliary
progression at one fixed slope to obtain exact elliptic trace matches.

## References independently reopened

- Z. Gao, T. Ge and L. Kühne, *The uniform Mordell–Lang conjecture*,
  Theorem 1.1 and equation (1.1), author manuscript:
  <https://ziyangjeremygao.github.io/articles/UML.pdf>.
  The explicit coset formulation on its second page covers the
  required finitely generated subgroup after applying it to each
  irreducible component.
- J. S. Milne, *Abelian Varieties*, in *Arithmetic Geometry*
  (Storrs, 1984), Springer, 1986, Proposition 12.1, p. 122:
  <https://www.jmilne.org/math/articles/1986b.pdf>.
  The proposition gives a complementary abelian subvariety and an
  isogeny over the base field. Its original-proof caveat for an
  imperfect field is irrelevant to `Q`; the author's corrected
  notes are <https://www.jmilne.org/math/xnotes/AVs.pdf>.
- Source formulas and the inherited rank and independence assertions
  were checked in the repository's `reweighted_elliptic_detectors`
  and `weighted_trace` manuscripts.

## Editorial note

The initially supplied bibliography gave a nonexistent main-repository
path for the separate Lucas-density checkpoint. The final manuscript
has removed that dependency and included the short cyclic-closure
argument after citing the published weighted-trace manuscript.
The final citation and proof edits were rechecked. They do not change
the theorem hypotheses. No correction remains outstanding.

No numerical experiment is used as evidence for the finiteness
theorem. It follows from the stated geometric and arithmetic proofs.
