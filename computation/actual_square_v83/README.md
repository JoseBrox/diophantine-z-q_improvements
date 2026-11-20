# Exact scalar squares and the remaining trace obstruction

This research checkpoint develops the **notes of Gabe Conant with Astra 6.2** and the v82 actual-realization criterion. It proves a new normalization and exact limitations of two proposed replacements. **The defining counts remain 25 and 11; the quartic counts remain 163, 179, and 56.** All counts include the input.

## A proved normalization

For the original derivative contact value `t`, set

\[
P=(t-7)(t-11),\qquad L=t^2-14t+77,\qquad
d=\frac{28tP}{L^2}.
\]

Then

\[
1+d=\left(\frac{t^2-77}{L}\right)^2.
\]

For each of the six even-valuation tests `C`, use

\[
r_C=\frac{P^2C^4}{t(1+t^2PC^4)},\qquad
W=\prod_C(1+r_C^2),\qquad
V=\operatorname{Tr}(W^{-1}),\qquad e=\frac{4d}{V^2}.
\]

The [complete valuation proof](saturated_contact_normalization.md) shows that the native pole condition on `e` still extracts all six tests at every positive odd contact of the original `t`. At every additional odd prime created by `P`, and at negative odd valuations of `t`, the new factors automatically satisfy `W = 1 mod p`; thus `V = 2 mod p`. The ordered preparation of the integer witnesses transfers. This gives an alternative source with the same two free pole parameters. It supplies no variable saving.

The actual pole input is **e**, so the remaining exact-square condition is

\[
1+e\in\mathbb Q^2
\quad\Longleftrightarrow\quad
V^2+4d\in\mathbb Q^2.
\]

The raw scalar identity does not establish it.

## Two exact obstructions

The [scalar-locus counterexample](new_scalar_counterexample.md) lies on the precise rational map above. It has

\[
t=49/4,\quad d=11760/16129,\quad V=238/127,
\quad e=240/289.
\]

Both scalar denominators are squares, the real and two-adic preparation holds, and `1+d=(167/127)^2`. Nevertheless

\[
Y^2=d\bigl(s^4-(V^2+d)^2\bigr)
\]

has no rational point. Its associated curve is `E_5235`, which has algebraic rank zero; none of its rational two-torsion abscissas has the required square class 15.

The [stronger counterfamily](deep_new_scalar_counterfamily.md) permits every prescribed two-adic depth `v₂(d)=v₂(e)=2k+2`, `k≥2`, arbitrarily large positive `t`, arbitrarily small positive `d,e`, and `V` arbitrarily close to 2 from below. Its obstruction is the complete Kummer image on `E_3615`: the only abscissa classes are `1,-1,3615,-3615`, so class 15 is absent. The proof combines odd elliptic multiples with an explicitly parametrized rational conic.

This family also has a precise limitation: its fixed class 15 forces the positive odd radical of `t` to have fixed finite support. The source height inequality therefore excludes these tuples from sufficiently large defining fibres. The family disproves a completeness theorem using scalar preparation alone; it does not disprove actual-source realization.

A separate example excludes the zero first parameter in the square-class-normalized native pole. Set

\[
d=112/729,\qquad V=10/9,
\qquad e=112/225=4d/V^2.
\]

Here `1+d=(29/27)^2`, and the same preparation conditions hold. At first parameter zero the remaining equation is, after dividing the ordinate by `d`,

\[
y^2=d\bigl(s^4-(1-e)^2\bigr).
\]

The map `(x,y_E)=(d s^2,d s y)` sends it to the congruent-number curve of level `d(1-e)`. Since

\[
d(1-e)=791(4/405)^2,
\]

this is a square rescaling of `E_791`. Algebraic descent gives rank one. The point `(-784,2940)`, together with the two-torsion, gives all eight classes in the full rational two-descent image. Its abscissa classes are exactly `1,-1,791,-791`, excluding the required class 7. The zero-abscissa case is impossible because `d>0` and `1-e>0`. Thus there is no rational solution, even allowing a zero ordinate. The [exact checker](raw_square_v0_certificate.py) verifies the complete Kummer image, rather than assuming a list of returned points generates it.

These are **prepared scalar counterexamples**. Neither value of `V` is asserted to occur at the actual elliptic detector. They do not disprove a 10-variable definition or the actual-input criterion.

## Reproduction and review scope

Run from the repository root:

```sh
python -m pip install sympy==1.14.0 passagemath-pari==10.8.14
python -B scripts/verify_v83.py --report /tmp/v83-verification.json
```

The rank bounds come from PARI algebraic descent. Calculations on a two-isogenous curve use the same implementation and are identified as such. Exact identity and finite arithmetic checks accompany the universal arguments; finite tests are not offered as a proof of rational realization.

The next constructive problem is a rational witness on the actual source, possibly only on one fixed quadratic progression as proved in the [v82 criterion](../../papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex). It requires an argument involving the actual elliptic trace, in addition to scalar preparation.
