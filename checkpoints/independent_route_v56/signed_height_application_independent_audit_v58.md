# Independent audit: signed height theorem and optimal single-cover rows

Date: 17 November 2026.

Audited in full:

- `checkpoints/general_scalar_v56/signed_mixed_power_height_v58.tex`;
- `checkpoints/general_scalar_v56/single_cover_height_criteria_v58.tex`;
- the retained single-cover and variable-squareclass repository papers cited there.

The final merged `signed_mixed_power_height_v58.tex` was re-read after the positive-input power lemma and odd-inner-exponent rows were incorporated. It is the canonical complete manuscript; the separate application draft is superseded by that merge.

## Verdict

PASS. The signed one-square height inequality, its improved coefficient, the revised parameter rows, the finite minimal-degree claims, and the distinction between soundness criteria and unproved realization are correct. The application permits every positive integer inner exponent e; only the outer exponent d must remain even.

## Signed height proof

The common-denominator identity uses `ell=lcm(D^(d/2),E)`, with `M=ell/D^(d/2)` and `N=ell/E`. At a prime dividing `ell`, one of the two summands is indeed a unit; hence the common gcd `g=G²` is coprime to `ell`, divides the reduced numerator `C` of `u`, and has `G|B`. For a prime dividing `M`, the square term has strictly smaller valuation, so `M²|F`, where `F` is the reduced denominator of `u`.

The radical bound after division by `g` correctly accounts for the removed gcd as `|A|(|B|/G)(|C|/g)rad(ell)`. The maximum of the three absolute values gives a positive coprime abc triple after reordering for either sign. All subsequent bounds apply to that maximum, so no hidden positivity assumption on `u` is used.

The factor `M^(kappa-2)rad(M)^kappa` is bounded by `F^(kappa-1)` because `kappa>1`. The terms involving the reduced numerator and denominator of `u` have nonnegative coefficients summing to `2kappa-1`. This proves the stated improved coefficient

`Q_(kappa,d)=(2kappa-1)/(d-kappa(d/2+2))`.

The cases `x=0`, `y=0`, and the excluded case `u=0` are handled correctly.

## Source application

The combined coefficient is `q=Q/(alpha_e gamma)`. The support-height bound gives the exact contraction `q(k+1/2)<1`. The term `1/2` follows without a B-dependent error from `2h(X)<=h(X²+B)`. Every retained height constant is independent of the fixed shift B. After absorption, the trace-height bound bounds both the integer index and the height, yielding the large-B contradiction.

Using the total outer exponent directly is valid: `epsilon_(dm)=m epsilon_d+2kappa(m-1)`, so no smaller degree was hidden in a separate outer amplification.

I re-read the full binary-power proof in `direct_input13_20261110_v22.tex`. Its only use of even inner exponent is positivity of the powers in its coprime abc triple. In the actual source, `beta=X²+B>0` and `T=2(h0²+2h1²)>0` at every guarded character, so the proof holds unchanged for odd e. All real positivity, denominator, radicand and point guards remain valid. No coordinate is added.

## Exact independent arithmetic

The separate checker `check_single_cover_rows_independent_v58.py` clears denominators before checking any inequality. For `kappa=p/q`, contraction is

`(2k+1)p²(2p-q) / ((d(2q-p)-4p)(eq-3p)(8q-6p))`.

It checks the eight principal rows, two co-minimal alternatives, and every pair of strictly smaller argument degree with arbitrary integer e and even d, using exact integers. The ordinary-abc minima are 48 and 60. The latter uses `(e,d)=(5,6)` at `kappa=101/100`, with `q=520251/1815355` and contraction `520251/726142<1`. The only smaller possible argument degree has `(e,d)=(4,6)`; its limiting contraction for budget2 is5/4. These are minima only inside the specified criterion, not lower bounds for defining-polynomial degrees.

At exponent16/15 the varying-budget minimum80 admits `(e,d)=(5,8)`, with contraction170/243; at121/100 the minimum168 admits `(7,12)`, with contraction5197555/5785616. The final manuscript uses these smaller-outer-exponent representatives. The even-inner-exponent alternatives `(4,10)` and `(6,14)` remain co-minimal in degree. The exact independent checker verifies all of them.

## Guards and logical scope

All arguments have `H0>1,t>1` at prepared real characters. The finite varying class menu is positive, and its denominator/radicand norms use the existing encoder. The count9 is a conditional construction census. Neither the restricted binary-quadratic prime patterns nor the actual rational-square realization has been proved. The manuscript states that limitation explicitly and does not change the established complete counts25/13.

No mathematical corrections requested.
