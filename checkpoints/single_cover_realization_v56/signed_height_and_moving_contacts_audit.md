# Signed height and moving-contact audit

Date: 17 November 2026. The signed-height theorem and local moving-contact
normalization pass independent audit. The moving-contact lower radical
bound remains unproved; no eleven-coordinate definition is claimed.

## Signed height theorem

Audited file:
`checkpoints/general_scalar_v56/signed_mixed_power_height_v58.tex`.

For either sign, `u=x^d ± y² != 0`, the theorem proves

\[
h(x)\le Q_{\kappa,d}h(u)+\epsilon^{-1}\log K_\kappa,
\quad
\epsilon=d-\kappa(d/2+2)>0,
\quad Q_{\kappa,d}=\frac{2\kappa-1}{\epsilon}.
\]

The minimal common square denominator is essential. I checked that the
square gcd `g=G²` is coprime to the common denominator `ell`, that
`g|C`, `G|B`, and that the auxiliary denominator quotient satisfies
`M_aux²|F`. The primitive radical bound uses only integer factors and
has the claimed `G^(-3)` saving. The exponent `2−3kappa` is negative;
`M_aux^(2kappa−2) <= F^(kappa−1)` is valid. The final two cases
`log|C| >= log F` and the reverse have coefficients summing exactly
to `2kappa−1`. There is no missing factor two or `log 2`. Reordering
the primitive integer identity covers both signs and negative `u`.

Thus, for `a=M^(d/2)` and `t=a²−z²`,

\[
h(a)\le L_{\kappa,d}h(t)+O(1),\qquad
L_{\kappa,d}=\frac{d(2\kappa-1)}{(2-\kappa)d-4\kappa}.
\]

## Local moving-contact normalization

Audited file:
`checkpoints/independent_route_v56/moving_contact_detector_normalization_v58.tex`.
Let `F=product_i((a+c_i)²−z²)`, `delta=t/a`, and
`w=F/(4 delta^8)`, retaining the actual fast detector factors with
denominator `F`.

The three cases for the valuation of `a` are correct. For negative
valuation of `a`, an odd valuation of `F` forces `v(t)=v(a)`, hence
`delta` is a unit. For `v(a)=0`, an odd valuation of `F` is positive
and `v(delta)>=0`. For `v(a)>0`, an odd valuation forces `z,t` to be
units and `v(delta)=−v(a)`. The pole condition therefore extracts all
six tests at the first two types of prime, and excludes negative odd
valuations of `F` in a source solution.

Only numerator primes of `M` may be omitted. Their radical costs at
most `h(M)`, independent of `d/2`. The twelve prime positions
`u ± D²(a+c_i)h²` have the exact common-translation form required by
the cited Sun theorem. The fixed-place, real and whole-character
completeness limits agree with the intrinsic source transfer.

The existing separating encoder forces a selected finite cover root
to be rational. Alternatively retain `z` as the free coordinate and
define `t=a²−z²`; this has the same eleven-coordinate census and
reduces the formal finite-algebra rank from 256 to 128. Neither layout
provides the missing height theorem.

## Exact remaining lower-bound target

Put `E_h=h_2(beta,T)`, `M=beta^e+T^e`, and
`alpha=e/kappa−3>0`. Suppose a new theorem proved, uniformly in the
coefficient shift and all source tuples,

\[
 \gamma h(t)\le\log r_{\rm odd,S}(F)+C h(M)+O(1).
\]

The local extraction and numerator omission give, when `X!=n`,

\[
 \log r_{\rm odd,S}(F)
 \le\tfrac12 E_h+\log(1+|n|)+h(M)+O(1).
\]

Combining with `alpha E_h <= h(M)+O(1)` and
`h(M)<=Q h(t)+O(1)` closes the source soundness argument provided

\[
 \boxed{\quad Q_{\kappa,d}\left(C+1+\frac1{2\alpha}\right)<\gamma\quad}
\]

or equivalently

\[
                    C<\gamma/Q_{\kappa,d}-1-1/(2\alpha).
\]

The constant term must be independent of the fixed shift `B`, so the
usual final enlargement of `B` remains valid.

## Why the direct collision estimate does not suffice

Set `x=a−z`, `y=a+z`, `G(X)=product_i(X+c_i)`. Then
`F=G(x)G(y)` and exactly

\[
 r(F)=\frac{r(G(x))r(G(y))}{\gcd(r(G(x)),r(G(y)))^2}.
\]

Outside the fixed coefficient/difference primes, a prime in the
gcd divides `2a+c_i+c_j`. Let `r` be the number of distinct pair
sums `c_i+c_j`. The direct numerator bound gives

\[
 \log\gcd(r(G(x)),r(G(y)))\le r h(a)+O(1).
\]

For six distinct rational contacts, `11<=r<=21`; arithmetic
progressions attain the lower value. Even granting the fixed-six-
contact estimate with coefficient `gamma=8/kappa−6`, applying it
separately and using `h(x)+h(y)>=h(t)` gives only the target with
`C=r d`. The best limiting regime `kappa -> 1` has
`gamma/Q ~ d`, while `C>=11d`. Therefore this direct resultant
estimate cannot satisfy the boxed condition. Increasing the power
alone does not repair it.

Finally `z=0` gives `t=a²` and `F=product_i(a+c_i)²`, so the odd
radical is one with unbounded height parameter. Any proposed lower
bound must explicitly exclude or otherwise handle this diagonal.
Adding the nonzero guard removes that immediate example; it does
not prove the missing bound off the diagonal.
