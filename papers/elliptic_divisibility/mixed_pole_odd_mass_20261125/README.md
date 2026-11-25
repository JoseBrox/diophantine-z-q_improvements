# Mixed comparison poles on the Lucas-free odd-mass routes

## Scope and result

Retain the arithmetic premises of the 22/24-variable general routes
in [the mixed-class theorem](../../pole_parameters/mixed_class_simultaneous_20261125/README.md)
and additionally the bounded odd denominator mass hypothesis (OM) of
[the Lucas-free construction](../sublinear_odd_mass_amplifier_20261124/README.md).
Then the latter's 19/21-coordinate alternatives improve to **18/20
total rational coordinates**, respectively. There is no proof of (OM)
under the original general premises here, so these do not replace the
22/24 records. The two-scale threshold is ineffective. The three-scale
threshold is effective relative to effective (OM) data and the retained
effective abscissa-sum and modular height estimates.

A new rational scale rechart resolves an ordering issue: the Lucas-free
growth point is chosen deep in the formal group at seven, whereas the
mixed-class prime preparation needs the two height scales to be units
congruent to one modulo 49. No condition of integral abscissas at seven
is imposed on the growth point.

## 1. Bounded-at-seven height rechart

Put
\[
 \psi(v)=v/(1+7v^2),\qquad v\in\mathbb Q .
\]
It is everywhere defined, is 7-integral for every rational v, and
\[
 2h(v)-\log 7\ \le h(\psi(v))\le 2h(v)+\log 8.
\]
Indeed, for v=a/b reduced, b>0, the numerator and denominator are
ab and b^2+7a^2. Their gcd divides 7: gcd(a,b^2+7a^2)=1 and
gcd(b,b^2+7a^2)=gcd(b,7). The positive denominator is between
max(|a|,b)^2 and 8 max(|a|,b)^2. This proves the inequalities
(including v=0 separately). If v_7(v)<0, the denominator has
valuation 1+2v_7(v)<0, so v_7(psi(v))=-1-v_7(v)>=0.
For v_7(v)>=0 the denominator is a unit.

For any positive rational scalar rho with v_7(rho)>=3 and any rational v,
\[
 \alpha(v)=1+\rho\psi(v)^2>0,\quad \alpha(v)\equiv1\bmod49.
\]
For nonzero rho the height inequality for squaring and translating gives
\[
 h(\alpha(v))\ge 2h(\psi(v))-h(\rho)-\log 2
                \ge 4h(v)-h(\rho)-2\log 7-\log 2.
\]
The same lower bound holds without positivity on the guarded
nonzero-scale locus. At any prime of odd v_p(rho), the term
rho psi(v)^2, when nonzero, has odd valuation. Hence alpha either
has negative valuation or is congruent to one modulo p. This is
exactly the source scalar-unit argument, not just a seven-adic
statement about canonical witnesses.

This rechart also applies to the existing 24/26 and 22/24 constructions,
eliminating their special seven-adic restrictions on the Lucas labels.
It changes the fixed-degree coefficient recipe, not the number of
coordinates. It is not needed to justify those previously recorded counts.

## 2. Retained growth and comparison equations

Let the new external input be X0 and put
\[
 X=\prod_{j=0}^{465}(X_0-j),\quad
 \beta=1632X^2+2477,\quad \tau=X^2+1,\quad
 \rho=(7/9)^2\rho_*(X;L)
\]
with the v88 scalar rho_* and the fixed exponent progression
\(L\equiv3\bmod171033184\) of the mixed-class theorem.
This input substitution reflects integrality, since at a denominator
prime of X0 every factor has exactly its negative valuation.

Use precisely the five point blocks A=[n]P, S=[a]P, T=[j]P,
H=[h]P, U=[u]P of the original Lucas-free source. They can all use
square-abscissa charts. Write Q=S-P, c=|a-1|>0,
B0=max(1,|n|,|a|,|j|). Retain the entire bounded-odd-depth amplifier:
for the fixed depth parameter d of (OM) use s=6d-1,
\[
 \ell=y_0(Q)^s+\epsilon y_1(Q)^{s+2}\ne0,\quad \epsilon=1,2,
\]
\[
 Z=\ell^2/x(T)^{24},\quad\chi=(1+Z)^{-1},\quad
 F=z(T)/z(Q),\quad J=F^2/(\ell^{-1}+F^2),\quad
 C=2-\operatorname{Tr}(\chi(1-J)),
 \qquad e_{\rm amp}=\frac{112}{841}(1+\ell C^2).
\]
The amplifier keeps its own two ordinary BB parameters and terminal
quadratic root. All its divisions and nonzero input are guarded.
This is the exact local amplifier of the cited odd-mass theorem, so
\[
 \log|j|\ge(3/2)s\,\mathcal M_d(c).
\]
Its completeness, choosing T after Q and before the slope, is unchanged.

For the comparison part use the six original field tests and six
scalar functions of that theorem. Use its scalar precision orders
(1,1,1,1,k,k), where k>=3 and 3/k<eta for the exponent eta of (OM).
Use its literal factors
\[
 Q_i=\rho R_i,\quad
 G_{i,l}=R_i^{\kappa_l}\frac{R_i S_l}{1+R_i S_l},\quad
 W_i=\prod_{l=1}^6(1+C_l^2/(\delta_i^2 Q_i))
                 \prod_{l=1}^6(1+G_{i,l}^2/Q_i^{2\kappa_l-1}),
 \quad e_i=4 Q_i/\operatorname{Tr}(W_i^{-1})^2.
\]
All denominators and physical pole inputs are guarded nonzero.

Write the aggregate \(x(A)+x(S)+x(T)=V_0+\sqrt2 V_1\).
For two scales take alpha_0=1, alpha_1=alpha(2V_0);
for three take alpha_0=1, alpha_1=alpha(V_0),
alpha_2=alpha(V_0+V_1). As in the mixed-class preparation take
\[
 t_i=\alpha_i\lambda,\quad
 \sigma_0=0,\quad \sigma_i=4i+67/7^{2i}\ (i=1,2),
 \quad \Theta_i=\Theta_0+\sigma_i,\quad\delta_i=t_i+i+1,\quad
 R_i=\prod_{\theta\in\Theta_i}(t_i-\theta)/\delta_i^{10}.
\]
The base ten-contact list is
\(\Theta_0=(2+\Theta)\cup(4+\Theta)\),
\(\Theta=\{0,-1/2,-1,1/2399,-32/407\}\).
Use the three-parameter mixed-class pole predicate on
\(d_1=e_0(m_{1,l}/3^{30})^2/7\) and
\(d_2=e_1(m_{2,l'}/3^{30})^2/7\), with the exact eleven-entry
menus of the mixed-class theorem. The third comparison pole,
if present, is independent BB. No additional point or slope.

## 3. Soundness

Use the fixed exceptional set of the mixed-class theorem together
with that of the amplifier and the denominator primes of the new
fixed expressions. Do not exclude the variable support of a scale
in soundness. The fixed prime 67 retains its separate scalar role:
rho has valuation L, the rescalings are units there, and the first
two contact/pole lists remain disjoint modulo 67. The proof of
Section 1 gives the same odd-scalar scale alternative at every
nonexceptional prime, including 67.

The mixed-class predicate excludes negative odd physical valuations
of e_0,e_1 outside the fixed menu/scaling exceptions. At the third
pole the BB implication is unchanged. These are the only pole
implications used in the odd-mass source. Therefore its scalar
precision and direct input comparison give
\[
 67^{(k-1)L+1}M_\beta^k\mid c,\qquad
 M_i\mid Nc\quad(N=\operatorname{num}(\tau-n)\ne0).
\]
The comparison radicals M_i omit the new fixed exceptions; M_beta
also omits 67. No comparison between the three original Lucas
labels is needed, since the independent amplifier supplies growth.
Translating the contact arguments back to the old lists gives,
in the two-scale route,
\[
 h(\beta)\le K_1 c^{7/(3k)},\qquad
 h(t_i)\le K_2 M_i^{7/6}.
\]
In the explicit three-scale route the respective estimates are
\[
 h(\beta)\le K'_1 c^{3/k},\qquad
 h(t_i)\le K'_2 M_i(A_0+\log M_i)^2 .
\]
The constants are fixed, effective in the latter case by the
old quantitative bounds and the finite products of omitted primes.

The new scale height inequality gives
\(4h(v)\le h(t_i)+h(t_0)+h(\rho)+2\log7+\log2\).
Thus the original trace-height bound for three positive summands,
or its effective two-component version, still bounds B0^2
by a constant times the sum of h(t_i), h(rho), and 1.
In the two-scale case absorption of h(rho)=O(h(beta)+log c+1)
gives
\[
 B_0^2\ll |Nc|^{7/6}+c^{7/(3k)}+\log c+1 .
\]
In the specified case the bound is
\[
 B_0^2\ll |Nc|(A_0+\log|Nc|)^2+c^{3/k}+\log c+1 .
\]
All implied constants are effective in the specified case.
If N is nonzero, then |Nc|<=2B0 c exp(h(beta)). Since B0>=c-1,
the lower-order terms can be absorbed for sufficiently large c,
as in the original OM theorem. Taking logarithms (and using
log(1+x)<=x, or eventual absorption of logarithmic terms in
the specified case) gives
\[
 \log B_0=O(c^{3/k}+\log c+1).
\]
The amplifier instead gives
\(\log B_0\ge(3/2)s C_0c^\eta\)
for all sufficiently large c. The strict exponent gap 3/k<eta
excludes every nonzero N once c is sufficiently large. Increase L
in its required progression until the forced lower bound on c
lies beyond this threshold. Thus tau=n is integral and X0 is
integral. The sufficient L is effective in the specified route
given effective OM data, not a universal numerical value.

## 4. Completeness

For integral X0 retain the scalar-reference preparation and choose
a-1 sufficiently divisible, with S-P deep relative to H, exactly as
in the odd-mass parent (using the increased fixed scalar precision).
Choose the growth point T and its amplifier witnesses independently
now, before fixing the comparison slope. The new factor (7/9)^2
in rho preserves the square-denominator and dyadic conditions;
at three it changes the prepared valuation from 6 to 2, and
at seven the integer input substitution gives valuation 3.
The proof of Section 1 makes every alpha a seven-adic unit congruent
to 1 modulo 49, even though T was prepared deep at seven.
Thus the 7-adically separated cross-list positions of the mixed-class
proof are available without imposing any incompatible reduction on T.

All roots and scales are now fixed. Apply the original Gaussian
prime-pattern supplier to the 20 or 30 distinct positions.
Its avoidance modulus can include the supports of all fixed data,
including the amplifier's already fixed data, except for the original
separate treatment of seven. The proof of the mixed-class theorem
gives pairwise +1 quadratic symbols across different lists and
between each list and the scalar support away from seven.
The fixed-place and real recurrence refinements choose H and
U=[hn]P preserving the scalar preparation. At each selected
prime the six direct comparison tests pass in one slot; the
p-divisibility of h and the original scalar component alternatives
make the scalar factors units of residue one for every fixed k.
The inverse-trace is a unit. At fixed places the old limits
R_i->1, W_i->1 apply uniformly in the chosen neighborhoods.
At all other primes R_i has even valuation by the exact
linear-prime factorization; the scalar parity and square trace
then prove the prepared square-denominator property of each e_i.
This includes foreign poles of the newly chosen H and U.

At markers 113 and 233, enlarge the fixed-place preparation
so that e_i/7 has the residues of rho(0;L=3)/7 as in the
mixed-class theorem. The original eleven-entry fixed menus then
give exclusive complement markers and avoid the ten opposite-list
primes. All hypotheses of its simultaneous rank-one realization
are satisfied. Supply the three shared parameters and their
finite roots, and the independent third comparison pole if needed.
The amplifier witnesses chosen earlier remain valid because its
input depends only on Q and T. This completes the ordered
all-integer witness proof. The new scale rechart enters only
the already fixed comparison arguments, not the amplifier.

## 5. Exact finite recipe and counts

Use the five rank-four point blocks, the rational functions and
guards above, the amplifier's finite BB root, the three mixed
finite roots, and, in the three-scale route, the independent
third comparison root. Rescale finite roots to monic form
after clearing denominators and use the joint finite-algebra
encoder of the mixed-class theorem, with one extra ordinary
coordinate. Finite disjunctions over the two choices of epsilon
and the 121 marker-menu pairs are products of the corresponding
polynomials. No parameter used in the rank theorem is a quantified
coordinate. The five point blocks contribute ten ordinary
coordinates. The other counts are
\[
\begin{array}{c|rrrrrr|r}
 &X_0&\text{points}&\lambda&\text{shared poles}&
 \text{amplifier}&\text{encoder}&\text{total}\\
 2\text{ scales}&1&10&1&3&2&1&18\\
 3\text{ scales}&1&10&1&3+2&2&1&20 .
\end{array}
\]
No degree or coefficient-height bound for these new finite
specifications has been optimized or evaluated. The extra OM
premise and its threshold qualifications must not be removed from
the count.
