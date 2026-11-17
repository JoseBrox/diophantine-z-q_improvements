# Independent audit: derivative-detector completeness and guards

Date: 17 November 2026.

## Scope and conclusion

**PASS** for the ordered completeness, denominator classification, whole-character guards and eleven-coordinate census described below. This audit does **not** certify the separate abc height theorem or its numerical absorption choices; that argument has a different independent reviewer.

I read the final scaled specification in `checkpoints/single_cover_realization_v56/derivative_detector_11_v59.tex`, with `e=4`, `d=6`, `a=M^3`, sixteen shifts `±1,…,±8`, and thirty-two prime positions. Its completeness and whole-character proof pass this audit. The conclusions below hold for the normalized family

\[
 F=\prod_{c\in\{-m,\ldots,-1,1,\ldots,m\}}
       ((a+c)^2-z^2),\qquad k=2m,
 \qquad u=-\frac{2kaF}{F_a},\qquad w=\frac{u}{(1+u)^2},
\]

with any fixed even number `k` of shifts, positive rational `a=M^(d/2)>m`, and even positive `d`. This variant needs no square assumption on `a` and includes the proposed `d=6` choice.

The six transformed tests and actual detector are

\[
 D_i=\frac{C_i^2}{1+uC_i^2},\quad
 W=\prod_i(1+D_i^2/u),\quad V=\operatorname{Tr}(W^{-1}),
 \quad b=4w/V^2,\quad \eta=7b.
\]

## 1. Exact local implication

At an odd unramified prime with odd `nu=v_p(u)`, the summands of `1+uC_i^2` have unequal valuations, so

\[
 v(D_i)=\max(2v(C_i),-\nu).
\]

For positive `nu`, the original maximal-slot valuation argument gives `v(D_i)>nu/4`, hence `v(C_i)>0`. Thus the transformed detector preserves the original formal-comparison extraction on the consumed positive odd support.

For negative `nu`, `v(D_i^2/u)>=-3nu>0`. Both slots of `W` are one modulo `p`, so `V` is two modulo `p`, and

\[
 v_p(b)=v_p(w)=-\nu>0.
\]

This deals with arbitrary new odd numerator primes of `F_a`, independently of poles in the original tests. Zero tests are harmless.

The valuation formula is **not** automatic at even `nu`: equality of the two denominator valuations can cause cancellation. The ordered finite-place argument correctly avoids this by first fixing the valuations of every nonzero test on a neighborhood, then choosing `z` sufficiently large. Identically zero tests stay zero.

## 2. Fixed places and the square leading term

Symmetry gives

\[
 F\sim z^{2k},\qquad F_a\sim-2ka z^{2k-2},\qquad u\sim z^2.
\]

The ratios tend to one at every fixed finite place. Include all numerator and denominator primes of `a`, all primes dividing `2k`, and the original finite preparation set. Choose the valuation of `z` sufficiently negative at each of them, after fixing the test neighborhoods. Then `u/z^2` is in the appropriate local square neighborhood; `v_p(u)=2v_p(z)` is negative and even. The transformed tests tend to zero, `W` tends to one, and `V` tends to two.

At two this gives `w` a rational local square, `v_2(w)>=4`, and `v_2(V)=1`, so `b` is a local square of valuation at least four. Hence `eta` lies in `7 Q_2^{*2}` with the required depth. At seven, `V` is a unit and `v_7(b)>=0`. This is sufficient for the intrinsic pole theorem. No fixed-set enlargement is inserted into the soundness theorem; these are temporary completeness preparations depending on the fixed input/root point.

## 3. Prime realization and all remaining valuations

The `2k` rational coefficients `±(a+c)` are distinct because `a>m`. After a common square denominator dilation, Sun's retained theorem gives the distinct primes

\[
 p_c^\pm=N\pm D^2(a+c)L^2,\qquad z=N/(D^2L^2).
\]

The free divisibility of `L` supplies the prescribed fixed finite-place depths, and its real approximation supplies `z>a+m`. The numerator `N` is a unit at every prescribed denominator prime: otherwise all distinct selected primes would share that fixed prime. The exact identity is

\[
 F=\frac{\prod_c p_c^-p_c^+}{D^{4k}L^{4k}}.
\]

At a selected prime there is exactly one vanishing linear factor and its opposite is a unit. Therefore `2(a+c)` is a unit and the derivative term associated with that factor is the unique unit term of `F_a`; hence `F_a` is a unit. Finite avoidance makes `2ka` a unit as well. Thus `v_p(u)=1`.

The existing shared-index CRT puts the actual multiplication tuple in the successful local neighborhoods. The first four tests have valuation at least two and the comparison tests at least four, so the transformed successful factors are one modulo `p`. The opposite reciprocal slot is zero or one modulo `p`, and `V` is a unit. Consequently `v_p(b)=1`.

Outside the temporary preparation and the selected primes:

- If `z` is integral, the prime product makes `F` a unit and `F_a` is integral. Thus `v_p(u)<=0`.
- If `z` has negative valuation, `a` and `2k` are units and the leading terms above are unique minima. Thus `v_p(u)=2v_p(z)` is even.
- If `v_p(u)` is negative odd, the automatic local argument in Section 1 makes `v_p(b)>0`.
- If `v_p(u)` is even, then `v_p(w)` and `v_p(b)` are even, including the case `v_p(u)=0` and cancellation in `1+u`.

These cases exhaust every prime. Therefore `b` has square reduced denominator. Multiplication by seven preserves this because `v_7(b)>=0` has been prepared.

## 4. Real bounds and whole-character guards

For `z>a+m`, every quadratic factor of `F` is negative, so `F>0` since `k` is even. Also

\[
 F_a/F=\sum_c\frac{2(a+c)}{(a+c)^2-z^2}<0.
\]

Thus `u>0`. For every real value of any test, including zero,

\[
 0\le D_i<1/u,\qquad
 1\le W\le(1+u^{-3})^6,\qquad
 0\le1-W^{-1}\le6u^{-3}.
\]

The last inequality, rather than `W-1<=6/u^3`, is the convenient correct uniform bound. Hence `0<=2-V<=12/u^3` at every real point-algebra character. Taking `u>28` makes `V>1` and `0<b<1/7` uniformly. In particular the actual intrinsic input satisfies `0<eta<1`.

The values `M,a,z,F,F_a,u,w` depend only on retained abscissas and the scalar coordinates, not on the finite ordinate signs. Every prepared point-algebra character is real. The new denominators `1+uC_i^2`, every product factor, the trace and the detector input are therefore nonzero at every character. Their scalar norm guards add no free coordinates. The original point and affine-difference guards remain covered by the source's existing signed-index argument.

The intrinsic pole equation has two rational parameters and one finite quadratic root. At every point-algebra character with nonzero input `eta=c`, its radicand polynomial is nonzero. The intrinsic theorem's Zariski-dense witness pairs can avoid the product of all cleared radicand norms. I checked the encoder proof in `papers/finite_algebra/unit_norm_20261114_v28.tex`, Section “The single determinant”: it explicitly permits nonreal conjugate pole roots. Nonzero radicand norms suffice; an additional positivity requirement on every pole radicand would be unnecessary.

## 5. Census and the remaining dependency

There are three free rank-four point algebras and one finite quadratic pole extension, for total algebra rank `4^3*2=128`. The unrestricted rational coordinates are

\[
 1\text{ input}+6\text{ point coordinates}+1\text{ parameter }z
 +2\text{ intrinsic pole parameters}+1\text{ separator}=11.
\]

The signed cover `t=M^d-z^2` uses the retained rational coordinate `z`; no extra rational square root or height-recovery coordinate has been omitted. Every new inverse is guarded inside the single norm guard and adds no free variable.

Accordingly, the completeness and guard portions of the prospective eleven-variable theorem are supported by this audit. A complete numerical choice must still satisfy the separately audited height inequality and retain precisely the source arithmetic hypotheses.

## Reproducible exact checks

`check_derivative_detector_completeness_v59.py` uses standard-library arithmetic to verify the normalized derivative identity, its leading terms, the odd-valuation formula over a finite exact fixture set, and the correct real uniform bound. Its output is `derivative_detector_completeness_v59_certificate.json`. These checks verify algebraic computations; the prime, height and intrinsic existence theorems are not presented as computational conclusions.
