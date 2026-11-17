# Independent review of even-valuation general25

**Result: PASS within the retained arithmetic premises.** The revised family
remains complete in 25 total variables. Its degree upper bound is
4863007848923136. The normalized actual-trace variant remains sound in 21
variables, with simultaneous rational realization unproved. No sufficiently
large numerical defining exponent is certified.

This review was conducted by the separate quartic reconstruction/review
agent. The v72 source, v19 arithmetic proof, v53 reweighting proof, new
constructor, new independent checker and new manuscript were compared.
Imported elliptic, comparison, height, normalized modular realization,
prime-selection and intrinsic-pole premises were checked for applicability
to the transfer; they were not reproved from external foundations.

## 1. Local parity and extraction

For the project curve `y^2=x^3-D*x`, with `v(D)=0`, a nonzero abscissa x has
even valuation. When `v(x)>0`, the two right-hand summands have distinct
valuations and `2*v(y)=v(x)`; when `v(x)<0`, they give
`2*v(y)=3*v(x)`. In either nonzero-valuation case y is automatically nonzero,
so the displayed valuations are finite. The zero-valuation case is immediate,
including a possible two-torsion point. Since `Norm(D)=49`, this lemma
applies outside seven. At every consumed odd prime K is unramified, and a
rational weight has the same normalized valuation at both slots.

The lemma applies to all five full auxiliary points and all five guarded
differences. It does not require an integral index or a global square class.
Thus the first ten C values have even valuation on the entire soundness
domain. With odd `alpha=v_p(q_j)`, the new second summand has valuation
`v(C_i)-2*v(delta_j)-alpha`, which is odd. The unchanged squared terms also
have odd second-summand valuation when nonzero. Hence all detector factors
have nonpositive valuation; a zero test contributes one and causes no issue.

If m is the largest slot valuation of W, then m is nonpositive and trace
integrality gives `v_p(V)>=-m`. The pole implication and odd parity force
`1<=v_p(b)<=alpha+2*m`. This simultaneously rules out negative alpha and
gives `m>-alpha/2`. At a slot attaining m, each factor has valuation at least
m. For a unit delta, the revised first ten factors yield
`v(C_i)>alpha/2`, which is stronger than the old `alpha/4` inequality.
The six remaining field inequalities and all scalar inequalities are
unchanged. In particular, the scalar-odd argument does not need a unit delta;
the mixed-contact argument uses it exactly where the old proof did.

Every later divisibility and height step uses only those old conclusions.
The four root indices, scalar coefficient, contact functions and scales
are unchanged. The full auxiliary formal-index transfer already proved in
v72 therefore continues to apply. The stronger first-ten estimate does not
introduce a new unproved arithmetic premise.

## 2. Complete prepared witnesses and all characters

At a selected fresh contact, `v_p(q_j)=1`, delta is a unit, and each of the
first ten successful-slot reciprocal abscissae has valuation at least two.
Its new second summand therefore has valuation at least one, so the factor
is still one modulo p. At the opposite slot the odd-valuation rule makes
each factor either one modulo p or of negative valuation. The unchanged
comparison/scalar preparation then makes the reciprocal products reduce to
one at the designated slot and either one or zero at the other. The trace
is congruent to two or one and remains a unit, since the selected prime is
odd. The old stronger depth of three in these first ten summands was not
needed for this conclusion.

The ordered fixed-place preparation is preserved. Once the roots, compact
point neighborhoods and scalar conditions are fixed, all ten raw reciprocal
tests are bounded there. As the slope grows in the specified completions,
R tends to one and inverse delta tends to zero, so replacing a bounded
squared numerator by its bounded unsquared value still makes every
comparison summand arbitrarily small. This retains all previously required
square classes, finite depths and real bounds. The proof that each pole
input has square reduced denominator is consequently unchanged.

For real whole-character positivity, the argument correctly restricts the
completeness witnesses to the old `2E(K)` subfamily. Every geometric real
sign character yields points in the identity component of the real elliptic
curve. Differences stay in that component. Both real embeddings of D are
positive; every finite nonzero point in this component has positive
abscissa. Therefore all ten new C values are positive at every such
character. With positive q and squared nonzero delta, their factors are
positive and at least one. The other factors retain their old positivity.
Product and trace norm guards therefore hold simultaneously. No positivity
is assumed on arbitrary full auxiliary soundness points.

The revised product introduces no rational denominator. The list of
nondivision guard labels is exactly the same as v72, and there remain 101
recorded native guards. The final compiler suppresses only the second pole
ordinate, `detector1.q`. In particular the first pole ordinate and every
preceding radicand stay guarded. This distinction is essential and has
been explicitly checked.

## 3. Source semantics and finite specification

The constructor applies exactly two checked edits to the pinned v72 native
method: enumerate its field-test loop and select the first power for indices
zero through nine. Its other operations, scalar normalizations and two pole
blocks are unchanged. The original independent checker was rerun and passed
its source reproduction, point-algebra identities, guard/subalgebra traversal,
degree/coefficient bounds and terminal-root traversal. Its degree and guard
corruption controls were rejected.

The additional `independent_math_check.py` imports no producer or previous
checker. Its exact structural checks establish:

- The first 2567 arithmetic nodes equal v72, with all variables, nine point
  blocks, precomparison guards and height events unchanged.
- All 16 field tests, six scalar tests, their orders and formal precision are
  unchanged. Only the declared first ten powers change.
- The nondivision guard-label multiset is unchanged; the nonterminal pole
  ordinate is retained and only the terminal guard is suppressed.
- Rank is `4^9*4=1048576`, there are 25 retained/encoder coordinates, and
  the degree formula is exactly
  `1048576*(4637555553+170132+1)=4863007848923136`.
- The support bound equals
  `binom(D+25,25)-binom(D-1048576+24,25)` and is strictly below `2^1192`.
  The determinant has constant term one in the encoder, giving content one.

The new checker also reconstructs the arithmetic of both detectors directly
at 128 generic modular assignments over two finite fields: beta, rho, the
root trace scale, all ten contacts of each detector, every comparison and
scalar weight, all normalized scalar numerators, the revised products, and
their reciprocal-trace pole inputs. All 256 detector reconstructions agree
with the stored DAG. These are exact finite arithmetic comparisons, not
an exhaustive polynomial identity proof or actual point witnesses.

Separately, the package's native chord-and-tangent checker passed 72 actual
finite point characters, including half-integral auxiliary indices and
single-character sign flips. It does not exhaust the rank-`4^9` point
characters. The whole-character statement rests on the algebraic and
arithmetic transfer proof, not on the number of tested characters.

The stored L=3 coefficient `l1` bound is `2^34532878499971072`. L=3 is an
algebraic fixture and is not certified as sufficient for integer definability.

## 4. The normalized 21-variable source

The same argument applies after replacing q by `w=q/(1+q)^2` in the
normalized source. An odd valuation of w has opposite parity to every
first-ten numerator after its squared delta, so the new extraction is again
stronger than that source's old inequality. Its distinct scalar numerators
are left unchanged. At selected contacts w still has valuation one; at fixed
preparation places it tends to the old nonzero limit. Thus soundness and
local preparation transfer, without any claim that the compiled unnormalized
degree bound is the normalized source's degree.

The fixed-point obstruction also persists. At every one of the first
detector's ten simple contacts, w has a simple zero and all ten reciprocal
tests are nonzero. The revised first-ten factors still give poles of W in
both slots; the scalar factors tend to one. Therefore
`V=O(w)` and `V^2+w*(2-V)=2*w+O(w^2)`, retaining ten simple branch points
and genus at least four. No rational parametrization or simultaneous
prepared rational square follows. The paper correctly keeps rho and the
root-dependent comparison scale fixed by their source definitions rather
than treating them as new free variables.

## Reproduction

```sh
python computation/few_variables/even_valuation25_v75/check.py
python computation/few_variables/even_valuation25_v75/independent_math_check.py
```

The accompanying review receipt records the reviewed hashes and explicitly
separates structural assertions, exact finite computations, retained
arithmetic premises and the unresolved global realization requirement.
