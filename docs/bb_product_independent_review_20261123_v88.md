# Independent arithmetic review of the normalized Bhargava–Burungale product transfer

Date: 23 November 2026. Scope: the arithmetic transfer proposed by the root agent, read against `four_contact_scalar_20261119_v78.tex`, the original merged-v19 source, `general_intrinsic_transfer_20261117_v57.tex`, and Bhargava–Burungale v2 Section 2. This note does not independently verify the root agent's coefficient-DAG degree calculations.

## 1. Exact terminal equation

Suppose `d != 0`, `k != 0`, and `e = d k²`. The replacement

\[
Y^2=(1-e)(v^4-d^2)(s^4-d^2)
\]

is exactly equivalent to the Bhargava–Burungale equation at `e` under

\[
(s_0,t_0,z_0)=(kv,ks,k^4Y).
\]

The complete residual on the latter equation is `k^8` times the complete residual on the former. The accompanying SymPy checker verifies this identity independently of any source compiler. Therefore a rational solution forces `e` to have square reduced denominator, including at 2. This supplies the old local extraction whenever the scalar formerly fed to the pole block was exactly `e`. No claim about square denominators of `d` alone is needed for soundness.

For completeness the exact hypotheses to verify are

\[
0<e<1,\qquad e\text{ has square reduced denominator},\qquad e\in7\mathbb Q_2^{\times2},\qquad v_2(e)\ge4.
\]

They are the v2 Lemma 2.2 hypotheses, since the 2-adic class determines the positive squarefree representative modulo 8.

## 2. Density and zero terminal roots

Fix a prepared `e` and write `j=sqf(e)`, `k_0=sqf(1-e)`. Theorem 2.3 gives curves `E_n` and `E_{n k_0}` with infinite-order points in the abscissa class `e`. Odd multiples retain that class. From a point `(x,y)` with `x=e a²`, the quantity

\[
u_D=\frac{y}{a(x-D)}
\]

satisfies `u_D²=e(x+D)/(x-D)`, so infinitely many distinct abscissas give infinitely many `u_D`. Independently choose a point on each curve. Every pair of the resulting `u_n,u_{nk_0}` is the projection of a rational solution of the BB product equation, since the two quartic factors have classes `en` and `en k_0` and `1-e` has class `k_0`. This remains valid for `k_0=1`, using independent points on the same curve. Thus the projection contains a Cartesian product of two infinite sets and is Zariski dense, also over an algebraic extension. Multiplying the coordinates by the fixed nonzero scalar `1/k` preserves density.

Finite guard avoidance is legitimate only for guards that remain nonzero polynomials after substitution. At another point-algebra character `e_chi=1`, the new terminal radicand is identically zero; it cannot be made into a unit by density. The v78 terminal encoder explicitly permits zero roots and nilpotent specializations, so this is harmless with that encoder. An older encoder requiring every terminal radicand to be a unit would need a separate modification. Do not add a guard `1-e != 0` at every character or infer positivity at arbitrary complex characters.

## 3. New scalar

Retain

\[
\beta=1632X^2+2477,\quad A=\beta(\beta-1),\quad
B=(\beta-2401)(32\beta+343),
\]

\[
T_L=[1224(67^{(L+1)/2}+1)]^2,\qquad q=T_LA/B,
\]

for odd `L>=3`, and set

\[
\rho^*=102^2 67^L\frac{7q}{(1+7q)^2}
=\frac{7\cdot102^2 67^L T_LAB}{(B+7T_LA)^2}.
\]

The ratio to the old scalar is

\[
\frac{\rho^*}{\rho}=7\left(\frac{1+q}{1+7q}\right)^2.
\]

### Real and denominator assertions

For every real `X`, `beta>=2477`, `A,B>0`, `B/A<33`, and `q>T_L/33>1`. Hence `rho*` is defined, positive, and

\[
0<\rho^*\le(7/16)\rho<1/167.
\]

For any rational nonzero `w`, `w/(1+w)²` has no negative odd valuation: if `v(w)!=0`, its valuation is `|v(w)|`, and if `v(w)=0`, a negative valuation is `-2v(1+w)`. Apply this to `w=7q`. Multiplication by `102²` changes valuations evenly. Multiplication by `67^L` is harmless because the exact 67-adic valuation is positive, as checked below. Thus `rho*` has square reduced denominator. In fact this argument works for all rational `X`.

The value `v_7(rho*)` need not be positive: negative even valuations are allowed and do not violate any BB preparation condition. A proof copying the older v57 assertion `v_7(rho*)>=1` to this new scalar would need correction. The retained global exceptional set already contains 7.

### Exact consumed-prime valuation

For integral 67-adic `X`, `T_L=1224² mod67`. Direct independent enumeration of all 67 residues verifies

\[
A B(B+7\cdot1224^2 A)\ne0\pmod{67}.
\]

For negative `v_67(X)`, cancel the common leading valuation in `A,B`; then `A/B=1/32 mod67`, and

\[
32+7\cdot1224^2=22\pmod{67}\ne0.
\]

Consequently `v_67(rho*)=L` for every rational `X`. Outside the fixed exceptional set, multiplication by 7 is a unit and the scalar ratio is a square; positive odd scalar-contact valuations retain their exact value. The finite-contact radical is unchanged outside the old exceptional set.

### Preparation at 2, 3, 17

For integer `X`, `beta=13 mod32`, and `v_2(A)=v_2(B)=2`, with `AB/16=3 mod8`. Since `L` is odd, the old `67^L AB` class is square at 2; multiplication by 7 gives the desired class 7. Also `v_2(T_L)>=8`, so

\[
\rho^*\in7\mathbb Q_2^{\times2},\qquad v_2(\rho^*)\ge10.
\]

At 3 the class remains a square because 7 is a 3-adic square; the valuation remains 6. At 17 the old square class is multiplied by the nonsquare 7, while its positive depth remains at least 4. Reading the original source shows that the old `Q_17`-square hypothesis is used to invoke the old level-17 pole converse. The scalar reference neighbourhood itself is chosen by deep formal subgroup conditions and continuity; it does not require a square root of `rho` at 17. BB only needs the stated 2-adic preparation, so no missing 17-adic square requirement is inherited after replacing the entire pole predicate.

The ratio preserves any already-proved global norm property from `Q(sqrt2)` because `7=N(3+sqrt2)` and rational squares are norms. No assertion that every older scalar had such a norm property is needed for the current BB transfer.

### Height bound

The scalar remains a rational map of degree four in `beta`. Let

\[
F_0=4\cdot1224^2\cdot67=401511168.
\]

After factoring out `67^(2L)`, exact coefficient-one-norm majorants are

\[
7\cdot102^2F_0\cdot2\cdot900064=52638002498271117312,
\]

\[
(900064+14F_0)^2=31607518344686765056.
\]

Both are less than `2^66`. Therefore the stronger bound

\[
h(\rho^*)\le4h(\beta)+2L\log67+66\log2
\]

holds. In particular the retained `+128` bound is valid with ample room, and the v78 effective height ledger at `L=143` remains valid without changing its numerical inequalities.

## 4. Source completeness with the unnormalized physical weight

For the v78 source use the actual old pole input

\[
b=\frac{4\rho^*R}{\operatorname{Tr}(W^{-1})^2}.
\]

This review does not insert the extra normalizer `(1+rho*R)^2` from the different v57 source. At selected prime contacts, the existing successful-slot argument makes the trace a unit and gives positive odd valuation of `b`. At primes in the finite support of `rho*`, choose `R,W` sufficiently close to one as the source already permits; this preserves the parity and nonnegative odd valuations of `rho*`. Every remaining valuation of `rho*R` is even, and division by the trace square preserves parity. Thus `b` has square denominator.

At two the trace is sufficiently close to 2 and `R` to 1, so `b` has the same squareclass and valuation as `rho*`, giving class 7 and depth at least 10. At the selected real character, the source can arrange `R<2` and both detector values in `[1,2)`, hence `Tr(W^-1)>1` and

\[
0<b<8\rho^*<1.
\]

These statements verify precisely the BB converse. The retained reference choices, nonzero root indices, local logarithm conditions, comparison scales, and prime-pattern ordering are unchanged. The current source is still conditional on its stated group, height, modular-realization and prime-pattern inputs; this replacement removes only the old pole-converse dependency.

## 5. Verdict

The normalized product replacement and the proposed scalar rescaling pass this arithmetic review. They retain the same free-coordinate counts. Their reduced polynomial degrees require the separately checked exact finite-algebra compiler output. A smaller one-parameter pole, or sharing coordinates between the two actual general detectors with different squareclasses, is not proved by this transfer.
