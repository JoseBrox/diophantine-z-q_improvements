# Saturated contact normalization: independent audit

This note develops the source notes of **Gabe Conant with Astra 6.2**. It audits the new rational functions proposed by the parent researcher. It does not establish a lower defining-variable count.

## Definitions and the exact scalar identity

Let `t` be the actual derivative contact quotient of the v78 eleven-variable source. Define

\[
 P=(t-7)(t-11),\qquad L=P+4t=t^2-14t+77,
\]
\[
 g=\frac{4t}{P},\qquad
 d=\frac{7g}{(1+g)^2}=\frac{28tP}{L^2},\qquad
 \sigma=\frac{t^2-77}{L}.
\]
Retain `tP != 0`. The denominator `L` is automatically nonzero over the rationals because

\[
 L=(t-7)^2+28>0.
\]
The exact identity

\[
 (t^2-77)^2-L^2=28t(t-7)(t-11)
\]
proves `1+d = sigma²` at every rational scalar tuple in this domain.

Let `C` run over the six tests used by v78: the four direct or conjugated reciprocal abscissas and the squares of the two comparison errors. Replace each balanced factor by

\[
 r_C=\frac{P^2C^4}{t(1+t^2PC^4)},\qquad
 W=\prod_C(1+r_C^2),\qquad
 V=\operatorname{Tr}_{K/\mathbb Q}(W^{-1}),\qquad
 e=\frac{4d}{V^2},\quad K=\mathbb Q(\sqrt2).
\]
Retain the nonzero guards for the displayed denominators and the old point and quotient denominators. A zero individual test is allowed and gives `r_C=0`, so its factor is exactly one.

The distinction between `d` and `e` is essential: `e` is the actual intrinsic-pole input. The identity `1+d=sigma²` does **not** prove `1+e` square. The latter is equivalent to `V²+4d` square.

## Even valuations of the six tests

Outside the fixed set containing `2` and `7`, the coefficient `D=11-6 sqrt(2)` is a unit and the curve `y²=x³-Dx` has good reduction. If a finite nonzero point has `v(x)>0`, its equation gives `2v(y)=v(x)`. If `v(x)<0`, it gives `2v(y)=3v(x)`. Thus every reciprocal abscissa has even valuation. Conjugation preserves this assertion. The two remaining tests are squares, so they also have even valuation, unless they are zero.

For every place over an unramified rational prime, normalize the valuation by `v(p)=1`; it takes integer values. For a nonzero test write `k=v(C) in 2Z`.

## Scalar valuation classification

Fix an odd prime `p` outside `{7,11}`. Write

\[
 n=v_p(t),\qquad \delta=v_p(P),\qquad \ell=v_p(L).
\]
The coefficient `28` is a unit. The complete classification is:

| Scalar case | `delta` | `ell` | `v_p(d)` |
|---|---:|---:|---:|
| `n>0` | `0` | `0` | `n` |
| `n<0` | `2n` | `2n` | `-n` |
| `n=0`, `delta>0` | `delta` | `0` | `delta` |
| `n=0`, `delta=0` | `0` | `ell>=0` | `-2ell` |

Indeed, if `n<0`, the leading powers of `t` uniquely dominate both quadratics. If `n>0`, their constant terms are units. When `n=0` and `delta>0`, the equation `L=P+4t` makes `L` a unit. The last row includes every new denominator prime of `L`.

In particular, all odd valuations of `d` outside this fixed set are positive. Apart from positive odd valuations inherited from `t`, they come only from negative odd valuations of `t` or from positive odd valuations of `P`.

## Positive odd contact valuations give the old extraction

Suppose `n>0` is odd. At any place of `K` above `p`, the two terms of the denominator `1+t²PC⁴` have valuations `0` and `2n+4k`. They cannot tie, because `n+2k` is odd. Therefore

\[
 v(r_C)=4k-n-\min(0,2n+4k)
       =\max(4k-n,-3n).
\]
This is an odd integer for every nonzero `C`. Consequently

\[
 v(1+r_C^2)=\min(0,2v(r_C))\le 0,
\]
with no unit-depth cancellation. A zero test still contributes valuation zero.

Let `q<=0` be the largest valuation of `W` among the places over `p`. The trace inequality gives `v_p(V)>=-q`. Suppose the actual pole input `e` has no negative odd valuation. Since

\[
 v_p(e)=n-2v_p(V)
\]
 is odd, it is at least one. Hence `q>=-v_p(V)>-n/2`.

At a place attaining `q`, each individual factor valuation is at least `q`, because all the other factor valuations are nonpositive. Thus each nonzero test satisfies

\[
 v(r_C)>-n/4.
\]
The branch `v(r_C)=-3n` is excluded. The other branch implies

\[
 4k-n>-n/4,\qquad k>3n/16>0.
\]
All six old tests are therefore positive at this place, with zero tests already successful. This is precisely what the retained formal-comparison argument needs to conclude that the positive odd contact radical of `t` divides the numerator of the input minus the root-point index.

The trace argument works for both split and inert unramified primes. In the inert case there is only one place and the same trace inequality holds. If the resulting formal-point requirements are incompatible there, this excludes the candidate tuple; it is not an additional completeness assertion. The old height argument is unchanged because it still uses the positive odd radical of the original `t`, with its original height margin.

## Uniform preparation at all new odd scalar primes

First suppose `n<0` is odd. Then `delta=2n`. The denominator term has valuation

\[
 2n+\delta+4k=4(n+k).
\]
Here `n+k` cannot be zero, because `n` is odd and `k` is even. Therefore

\[
 v(r_C)=3n+4k-\min(0,4n+4k)
 =\begin{cases}
 -n,&n+k<0,\\
 4(n+k)-n,&n+k>0.
 \end{cases}
\]
In either case `v(r_C)>=-n>0`. The even valuation hypothesis on `C` is essential in this case.

Next suppose `n=0` and `delta>0` is odd. The denominator term has odd valuation `delta+4k`, hence again no tie. One gets

\[
 v(r_C)=2\delta+4k-\min(0,\delta+4k)
 =\begin{cases}
 \delta,&\delta+4k<0,\\
 2\delta+4k,&\delta+4k>0.
 \end{cases}
\]
Thus `v(r_C)>=delta>0` in every slot. Zero tests satisfy the same conclusion with infinite valuation.

In both cases `W=1 mod p` in every residue slot. Hence `V=2 mod p`, including at inert primes, and `V` is a rational `p`-adic unit. The actual input `e` has the same positive odd valuation as `d`. Every remaining odd-prime valuation of `d`, including the denominator primes of `L`, is even, so division by the rational square `V²` cannot create a negative odd valuation there.

## Ordered completeness and fixed places

At each selected old contact prime the valuation of `t` is one. The retained auxiliary-index refinement makes every successful test positive, so the corresponding slot of `W` is one modulo the prime. At the other slot, each reciprocal factor reduces to zero or one, by the odd-valuation formula above. Thus `V` is one or two modulo that odd prime and the actual input has positive odd valuation one.

At a fixed real or finite place, as `t` tends to infinity,

\[
 d\sim\frac{28}{t},\qquad r_C\sim\frac1t
\]
for every test that remains nonzero in the previously fixed neighborhood. Zero tests remain zero. Thus `W -> 1`, `V -> 2`, and `e ~ 28/t`. These limits are uniform on the prepared neighborhoods. The retained order of choices is unchanged: root data and neighborhoods first, then the contact slope and its simultaneous prime pattern, then the auxiliary-index refinement.

At the real place choose `t>11` and sufficiently large. Then `P>0`, every new balancing denominator is positive in every prepared real character, `W>=1`, `V>0`, and `0<e<1` eventually. This also proves the whole-character nonvanishing of the newly introduced denominators and trace.

At two, the v78 trace lemma makes the original scale a two-adic square for the integer witnesses. The large-slope expansion `t~z²/a` therefore makes `t` a two-adic square of arbitrarily negative even valuation. It follows that `d~28/t` has square class seven and arbitrarily large positive even valuation. The ratio `4/V²` is a rational square, and `v_2(V)=1`, so the same class and depth assertions hold for `e`.

At seven, eleven, and every other fixed preparation place, sufficiently strong large-slope dominance makes the actual input integral, regardless of the parity of the scale valuation there. These fixed primes remain in the exceptional set used for soundness. They were already present in the source's much larger fixed exceptional set.

Accordingly the redesigned factors give a complete alternative normalization **with the original two-parameter intrinsic pole**. This establishes no coordinate saving. A rational point on a proposed one-parameter replacement at the actual trace remains a separate requirement.

## Scope of the raw-square improvement

The new identity is at an actual scalar `t`, not a freely assigned normalized weight. Nevertheless it is still a raw scalar identity. The separate prepared counterexample supplied by the other research agent, with

\[
 t=49/4,\quad d=11760/16129,\quad V=238/127,\quad e=240/289,
\]
 satisfies `1+d=(167/127)²` and the displayed real and two-adic preparation. Its genus-one cover is associated with the rank-zero curve `E_5235`, which has no required abscissa class `15`. I independently verified its exact arithmetic and the unconditional PARI rank intervals on the curve and its two-isogenous curve. This is **not asserted to be an actual elliptic detector trace or an actual contact tuple**.
