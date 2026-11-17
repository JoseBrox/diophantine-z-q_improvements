# Scalar precision transfer checkpoint

## Latest v58 results and independent audits

### Signed mixed-power heights and optimal conditional criteria

The canonical publication manuscript is now
`signed_mixed_power_height_v58.tex`. It combines the proved signed
height theorem and its complete single-cover application. Under weak
rational abc with exponent kappa>1 and constant K, for even d and
epsilon=d−kappa(d/2+2)>0 it proves

`h(x) <= ((2*kappa−1)/epsilon) h(x^d ± y^2) + log(K)/epsilon`,

whenever the output is nonzero, with no integrality or sign condition.
The minimal common denominator and the square gcd give the improved
coefficient. Parent and both other agents passed the proof. The exact
checker/certificate `check_signed_mixed_power_height_v58.py` and
`signed_mixed_power_height_v58_certificate.json` pass3133 fixtures,
including cancellation, unrelated denominators, negative output,
446 nontrivial square gcds, and519 denominator cancellations.

The application uses
`q=(2*kappa−1)/(epsilon*(e/kappa−3)*(8/kappa−6))` and strict
contraction `q*(k+1/2)<1`. Positive beta and the exact point-chart
trace `T=2(h0^2+2h1^2)>0` permit every integer e>=4, including odd e;
a self-contained proof of this binary-power height lemma is included.
The argument degree is exactly2ed. Ordinary-abc minima in this
criterion are48 for k=0 and60 for k=2. The latter uses e5,d6.
For weak exponents25/24,16/15,121/100, the optimal k2 degrees are
72,80,168. At degree ties the rows choose the least d.

`check_single_cover_height_criteria_v58.py` and its certificate verify
all8 exact rows, all46 smaller pairs, and all same-degree alternatives.
The application-only checkpoint `single_cover_height_criteria_v58.tex`
is synchronized with the canonical merged manuscript. These are scalar
argument degrees, not full determinant degrees. The nine-coordinate
criterion still requires unproved actual rational realization; the
established defining counts remain25/13.

The independent full-height/application receipt is
`../independent_route_v56/signed_height_application_independent_audit_v58.md`.

`small_quadratic_trace_class_20261117_v58.tex` proves that
`delta(V)=V^2−V+2` is an admissible no-loss class for the actual trace
conic. The inherited comparison primes split in Q(sqrt2), so its
fresh values2 and4 are local squares. It is strictly positive at every
real character; fixed-place preparation near V=2 handles every finite
place, including two. The radicand product has degree4, seven monomials,
and coefficient height4 in `(V,w)` only. The manuscript compiles cleanly.

`fixed_index_trace_ramification_independent_audit.md` independently
passes both propositions in the other agent's v58 negative manuscript:
the fixed-index multiplication family with free slope, and every
nonconstant rational slope graph on the entire multiplication surface,
retain an odd contact divisor. The second proof uses six even contact
fibers versus the genus-one Riemann–Hurwitz bound. Scope excludes
proper correspondences and individual rational witnesses.
`check_small_trace_and_ramification_v58.py` and its certificate pass.

`two_label_lucas_clause_20261117_v58.tex` proves the exact numerical
two-label clause: for integer s,b with |s|>=3 and b nonzero, a rational
root of `z^2=(s^4−4)(s^2−2)^2 b^2+4` is integral and recovers an
integer t satisfying the full squared-Lucas relation and exponential
growth. It does not identify the elliptic ratios with the integer
labels, so no coordinate reduction follows yet.

`negative_results/finite_lucas_point_reconstruction_v58.tex` proves a
sharper scoped obstruction. Any unbounded-s family of integer
squared-Lucas triples gives a Zariski-dense set in `(Res E)^3`.
Adjoining the shared auxiliary and the three multiplication points
keeps density if each root triple retains infinitely many auxiliary
indices. Therefore a fixed finite algebraic reconstruction of a Pell
point cannot preserve that entire flexible preparation family. The
proof uses the source's conjugate-generator independence and the
Mordell–Lang theorem. It is not an obstruction to a changed index
coupling, a numerical finite Pell root, or a smaller defining
polynomial. Both other agents passed the mathematical argument with
this scope. The full independent audit receipt is
`../independent_route_v56/lucas_reconstruction_independent_audit_v58.md`;
it rechecks the full manuscript, Lucas-growth source, conjugate
independence, and the primary Mordell--Lang theorem. The exact algebra checker/certificate are
`check_lucas_reconstruction_v58.py` and
`lucas_reconstruction_v58_certificate.json`.

**No new defining-variable bound is proved. The established counts
remain25 and13.** The outstanding numerical-label problem and actual
trace-square realization problem remain distinct.

## Latest v57 positive results

`trace_conic_criterion_20261117_v57.tex` replaces the earlier native
norm–trace square target by the simpler actual-trace radicand
`C=V^2+w(2−V)`. It proves pole soundness, whole-character positivity,
all local preparation assertions, both rational conic parametrizations,
and the exact 21/9 census conditional on simultaneous actual rational
realization. **The realization is not proved; defining counts stay
25/13.** The fixed admissible class menu is
`{1,1+24V,1+3(V−1)^2}`; it loses no contact prime and requires no
height budget in the unconditional Lucas source. The cubic branch has
five monomials and coefficient height47 as a radicand in `(V,w)`;
these are not full determinant bounds. Its checker and certificate pass.

The parent's broader family
`q=2+wc^2`,
`delta=(q^2−2q−1)^2+4q(q^2−1)V`
is independently audited in
`adaptive_trace_class_independent_audit.md`. It is valid for any already
guarded rational source function `c`, with no added free coordinate or
lost-contact height term. The explicit choice `c=lambda` is compatible
with both general and conditional fixed-place preparations. The exact
independent checker/certificate pass486 local fixtures and the three
square identities. Parent owns the integration of this proposition;
the agent's trace manuscript does not include that parent-owned text.

`cubic_trace_rank_20261117_v57.tex` proves that
`P=(49,336)` on
`y^2=x^3−(2+24w)x^2+(1+1176w)x`
has infinite order for every rational `0<w<=1/4`. Its only rational
nonsingular torsion specializations are `296/49`, `−96/49` (order3)
and `100/49` (order4). Exact division-polynomial factor products have
eleven projective no-root certificates at5,11,13; a separate whole-
quotient check uses5,877,449. Every test explicitly checks infinity
through a nonzero leading coefficient. The standard-library verifier
passes. Another agent independently confirmed the result by direct
group-law denominators over Q(w). The real/finite approximation
corollary supplies infinitely many **free** rational traces1<V<2;
it does not match prescribed actual detector traces.

The rank manuscript and trace-conic manuscript compile cleanly.
`cubic_trace_rank_build.json` and the latest trace build record the
successful builds. The full independent audit of both the cubic rank
and adaptive classes is in
`../single_cover_realization_v56/adaptive_and_cubic_independent_audit.md`.

## Latest v57 audits and scoped negative result

The parent's input/root-dependent squareclass theorem passes the audit
in `variable_squareclasses_independent_audit.md`. Its extra class
`1+X^4` has the same `k=2` height-support budget, uniformly inB>=1.
The exact checker/certificate include the improved ordinary-abc
parameter choices and1276 rational reduced-denominator fixtures.

`prepared_q0_independent_audit.md` and its independent checker/certificate
prove the correctness of the other agent's prepared-input Sha
counterexample `d=112/225`. The exact Cassels pairing onE791 is nonzero;
the curve has rank1 and excludes abscissa class−7. This disproves
uniform completeness of the q0=0 one-coordinate replacement for all
prepared inputs, not its completeness on some future actual-detector
subfamily.

`free_auxiliary_poles_20261117_v57.tex` gives a complete-source family
with all roots, slope, contact data and U_i fixed but with both rational
components of L_S having valuation1−r at one fixed unused prime.
It proves existing source conditions alone cannot bound these auxiliary
heights by fixed root/contact heights. Its scope excludes a newly
imposed Pell-cover or native-square equation. The manuscript compiles;
no separate independent audit receipt has yet been obtained.

## Latest complete intrinsic-pole transfer

The preferred same-count transfer is
`burungale_scalar_transfer_20261117_v56.tex`:

\[
\rho_L=A_Lr/(1+C_Lr)^2
\quad\longmapsto\quad
\rho_L^*=7A_Lr/(1+7C_Lr)^2.
\]

It keeps the original normalized physical weights and uses the
intrinsic degree-nine pole equation directly at `d=b`. It covers
both retained general scalars and either v53 or corrected order-two
scalar tests. It is a complete 25-coordinate transfer under the
remaining source premises and Burungale Theorem B, with no new
small-variable theorem or numerical determinant-degree bound.

`check_scalar_seven_transfer.py` and
`scalar_seven_transfer_certificate.json` pass. The consumed-prime
certificate enumerates every one of 76249 residues for each scalar.
The independent auditor uses polynomial gcds instead of enumeration;
its receipt and certificate are in
`../single_cover_realization_v56/general_source_transfer_independent_audit.md`
and `../single_cover_realization_v56/scalar_transfer_independent_certificate.json`.
The manuscript compiles cleanly in three passes.

The earlier coherent physical-weight transfer
`burungale_general_transfer_20261117_v56.tex` is also proved, but
is an alternative to the simpler scalar-only transfer. The larger
constant tuning in `scalar_constant_seven_transfer.md` is unnecessary.
Only the scalar-only version is proposed as the current polished result.

`conditional_burungale_independent_audit.md` records a passing audit
of the other agent's simplified 13-coordinate intrinsic-pole transfer.

## Fixed finite squareclass menus

`finite_squareclass_menu_audit.md` proves the native local obstruction
and finite one-encoder disjunction for any fixed finite positive
S-unit squareclass menu. Its exact discriminant checker passes.
The formal 21/9 censuses are preserved, but the required actual
rational realization remains unproved.

## Proved revision

`precision_transfer_20261117_v56.tex` gives the full source transfer with
scalar orders `(1,1,1,1,2,2)`, unchanged reciprocal orders one, paired
comparison orders `(1,6,6,6,1,6)`, the truncated logarithm

\[
\ell_8=z(1-2Df^2/5),
\]

and the exact Lucas equation `F(s^2,t,b)=0`. Its relative formal error has
valuation at least eight at first formal depth. The unchanged CRT thus
suffices. The scalar height exponent is `7/6`; the nonzero Lucas-residual
exponent is `7/4`. Both are less than two. Completeness retains the order
of choices, all scalar normalizers, both pole blocks, and every point,
difference, trace, and whole-character guard.

This is a **25-variable source**, under exactly the retained arithmetic
premises. It does **not** prove 21 variables, and no numerical sufficient
exponent or degree bound has been calculated.

## Correction to the earlier depth proposal

The proposed increase of both primary and opposite reciprocal test
orders to three cannot be supplied by unrestricted deeper CRT
preparation. At the explicit split good prime `76289`, both conjugate
minimal formal returns have depth exactly one. Raising both depths to
two forces `76289 | h` and `76289 | h-1`. The exact finite-field and
modulo-square certificate is separate in `depth_obstruction_certificate.json`.
The new logarithmic truncation fixes this problem without altering those
reciprocal orders.

## Reproduction

Run from the workspace root:

```sh
python checkpoints/general_scalar_v56/check_precision_transfer.py
```

The standard-library checker returns `PASS` and writes
`precision_transfer_certificate.json`. It verifies the exact exponents,
formal coefficients, explicit Lucas integer witnesses, prime and point
orders, projective multiplication modulo the prime square, and the two
nonzero first formal returns. These checks support the stated algebra
and counterexample; they do not replace the arithmetic hypotheses of
the source or prove a smaller variable bound.

## Remaining target

To save the scalar point and its paired auxiliary, a new coupling must
both bound the input height and accommodate arbitrary elliptic reduction
orders at scalar contact primes. Merely replacing `S` by the input point
is incomplete. An alternative source or a new arithmetic construction is
still required.
