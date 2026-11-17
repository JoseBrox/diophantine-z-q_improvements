# Independent audit of the single actual-trace criterion

## Verdict and audited scope

**PASS as a transfer criterion, with its additional realization premise
explicitly unresolved.** The manuscript proves a sound nine-coordinate
family under the retained arithmetic hypotheses and ordinary rational abc.
It does not prove a nine-variable definition under abc alone, nor the
existence of any defining shift satisfying its trace-square premise.

Authoritative manuscript:
`papers/pole_parameters/single_trace_derivative_criterion_20261117_v64.tex`.

Audited TeX SHA-256:
`aa39c6c8d9804765c94ebf7733dbbd793fe76d2aef1b87264aea401b2ff69521`.

The publication copy has SHA-256
`ea518d072a377ddc3432bb3bb9a17e17142821a3eb37e57ad34600d256e70bc2`.
Its only difference is a local ragged-right setting for the exact-verification
paragraph; the mathematical text and formulas are identical.

The authoritative source was checked against the published v63 derivative
construction, the rank-four point algebra and homogeneous difference
formulas in `unit_norm_20261114_v28.tex`, and the actual terminal-root
separation and rational-descent statements in
`terminal_quadratic_root_20261115_v40.tex`.

The accompanying symbolic checker was independently rerun successfully;
its regenerated output agrees exactly with
`computation/pole_parameters/single_trace_v64/certificate.json`.

## 1. Odd-valuation implication, including zero terminal roots

For every nonzero rational `u` with `1+u!=0`, the weight
`w=u/(1+u)^2` has valuation

\[
v_p(w)=\begin{cases}
v_p(u),&v_p(u)>0,\\
-v_p(u),&v_p(u)<0,\\
-2v_p(1+u),&v_p(u)=0.
\end{cases}
\]

Every odd valuation of `w` is therefore positive, including at primes
where the derivative denominator contributes.

For an odd prime `p`, suppose `b=4w/V^2` has negative odd valuation.
Then `v_p(w)` is positive odd and `2v_p(V)>v_p(w)`. Hence `V` is
in `p Z_p`, `2-V` is a unit, and the two terms of

\[
\mathcal C=V^2+w(2-V)
\]

have distinct valuations. The smaller valuation is `v_p(w)`, which is
odd. In particular `C` is nonzero and cannot be a square. A terminal
ordinate equal to zero does not evade this argument.

The retained trace guard `V!=0` justifies the auxiliary definition of
`b`; all primes dividing the coefficient `4` are in the existing set.
No condition on `2-V` is needed as a guard, and no inverse of `2-V`
is introduced.

## 2. Complete extraction from positive odd contacts

At a positive odd valuation `nu=v_p(u)`, with `p` outside the retained
exceptional set, the quadratic algebra is unramified and its normalized
local value groups are integral. Thus the balanced transformation has

\[
v(D_i)=\max(2v(C_i),-\nu).
\]

This includes zero tests using value infinity. Every factor of `W` has
valuation `min(0,2v(D_i)-nu)<=0`. Let `q<=0` be the greatest valuation
of `W` over the places above `p`. The trace satisfies `v_p(V)>=-q`.
The new square equation excludes negative odd valuations of `b`, while
`v_p(b)=nu-2v_p(V)` is odd, so

\[
1\le v_p(b)\le\nu+2q.
\]

At a place attaining `q`, each individual factor has valuation at least
`q> -nu/2`. Therefore every `D_i` has valuation greater than `nu/4`
and every original `C_i` has positive valuation. This is precisely the
six-test hypothesis of the retained formal-comparison argument. It gives
`p`-integrality of the input and `X=n mod p` for the selected root point
`A=[n]P`.

Thus the odd positive support divides the numerator of `X-n` whenever
`X!=n`, with no additional discarded prime or height cost. The derivative
height proof, including its strict margin

\[
\frac{44272779}{198801800}>0,
\]

is unchanged. It supplies the same eventual fixed-shift soundness.

## 3. Local completeness claims and their precise limits

At a selected contact prime, `v_p(w)=1` and `V` is a unit. Thus

\[
\mathcal C/V^2=1+w(2-V)/V^2\in1+p\mathbf Z_p
\]

is a nonzero square for the odd selected prime.

At a negative odd valuation `nu=v_p(u)`, the balanced formula yields
`v(D_i^2/u)>=-3nu` in every slot. Hence `W^{-1}=1+O(p^{-3nu})`
and `V=2+O(p^{-3nu})`. Since `v_p(w)=-nu`, the correction to
`C/V^2` has valuation at least `-4nu>0`; Hensel applies. This covers
new derivative-denominator primes of negative odd valuation.

At a fixed preparation place, `u~z^2/a`, `w~a/z^2`, and `V->2`.
The local neighborhoods fix the nonzero test valuations, with identically
zero tests treated separately. Increasing the prescribed precision for
the existing slope makes the correction belong to `p Z_p` at odd primes
and to `8 Z_2` at two. No extra trace parameter is used. The argument at
two is the direct convergence argument, not the odd-valuation formula
for unramified extensions.

At prepared real characters, the original point-chart values in both
slots are real. Since `u,w>0`, all balanced denominators are positive and
all slots of `W` are at least one. Thus `0<V<=2` and `C>0`.

The manuscript correctly does **not** claim that these checks prove
local squareness at every new even-valuation prime. Nor do they prove
rational squareness. Those gaps are included in the explicitly stated
actual-trace realization property; the proof does not smuggle in a
Hasse principle or replace the actual trace by a free rational value.

## 4. All-character guards and quadratic algebra

For `W=A+B sqrt(2)` and `N=A^2-2B^2`, exact substitution gives

\[
\mathcal C=\frac{4A^2+2wN(N-A)}{N^2}.
\]

There are no new denominator divisors beyond the retained weight and
detector denominators. The original point, difference and quotient
guards, balanced denominator norms, product norm and trace norm remain
in force. No individual elliptic comparison test is guarded.

The point algebra remains free of rank `4^3=64`. Its six quadratic
stages for separation remain nonvanishing; these are the retained
primitive-element tower, not a claim that every coordinate such as the
rank-four generator `V` itself is nonzero. This distinction is consistent
with the original point-algebra construction and permits point-coordinate
zeros that its source permits.

Clearing `C=N_C/D_C` and adjoining `q^2=N_C D_C` gives a free monic
quadratic extension of rank `128`. If `N_C D_C=S_0^2 c`, adjoining
`q_0^2=c` recovers the original ordinate by multiplication,
`Y=S_0 q_0/D_C`. Soundness never divides by `S_0`.

In completeness, every prepared point-algebra character has `C>0` and
`D_C!=0`, so `S_0` is automatically nonzero there. A supplied rational
ordinate therefore yields the reduced root. There is no need for a new
positive-dimensional avoidance family of pole witnesses.

The terminal-root theorem applies because only the last radicand can
vanish. Its distinct nonzero geometric character values allow the
guarded norm determinant to select a rational character, even when the
last quadratic fiber is nonreduced. Repeated eigenvalues from nilpotent
lengths do not invalidate descent. The local obstruction in section 1
continues to hold for a zero final ordinate.

The exact unrestricted count is

\[
1\text{ input}+6\text{ point coordinates}+1\text{ existing slope}
 +1\text{ separator}=9.
\]

The new finite root replaces the old finite root; both unrestricted
intrinsic-pole parameters disappear. No free rational conic or trace
coordinate has been added.

## 5. Sign involution and finite completion

The map `(X,A,H,U,z) -> (-X,-A,H,-U,z)` preserves the prescribed
root-index relation and sends the multiplication family `U=[n]H` to
`-U=[-n]H`. Since abscissas are unchanged, every scalar height/contact
quantity is unchanged. The first four tests are fixed and the last two
negate; the balanced tests, products, actual trace and square radicand
are therefore fixed.

In the homogeneous difference formulas, simultaneous negation of both
input points fixes the abscissa difference and the abscissa numerator,
and negates the ordinate numerator. Their denominators remain nonzero.
The reference difference `H-P` is unchanged. Original point inverses
and all quotient guards remain valid.

In a rank-four block, `(U,V,W)->(-U,-V,W)` preserves all six of the
published multiplication relations. It is an automorphism, so applying
it in the two changed point blocks permutes the entire set of geometric
characters. The original primitive point separator negates, its square
is fixed, and all earlier radicand-unit conditions persist. Norm guard
nonvanishing therefore persists at every character. The selected prime,
fixed-place and real preparation conditions are transported by this same
sign map. The final rational square has exactly the same value.

Consequently `TC_B(n)` is equivalent to `TC_B(-n)`.

If positive-input realization holds for every `n>=N`, the explicit
finite completion

\[
P_{B,N}=P_B\prod_{m=1}^{N-1}(X^2-m^2)
\]

adds all omitted small positive and negative integer inputs. It adds no
noninteger input, since a product over a field vanishes only when one
factor vanishes. The existing factor `X` already includes zero. No
coordinate or inverse is added.

This is a computable family for specified integer parameters `B,N`;
neither an effective choice of `N` nor the realization premise follows.
With the integral determinant normalization `P_B|_{E_0=0}=X`, the finite
completion also has integer content one: its specialization at `E_0=0`
is the monic input polynomial `X prod_{m=1}^{N-1}(X^2-m^2)`.

## Publication qualification

The theorem and cofinite positive-input corollary are valid with their
stated hypotheses. They identify a sufficient additional arithmetic
realization theorem. They do not establish that theorem, even for one
sufficiently large shift, and should not replace the current proved
defining count in a results table.
