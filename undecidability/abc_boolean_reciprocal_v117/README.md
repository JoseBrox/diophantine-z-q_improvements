# Reciprocal chart and derivative-weighted Boolean aggregation (387 variables)

**Theorem.** Under exactly the hypotheses of [v115](../abc_unscaled_aggregate_v115/README.md), the twelve-input Jones transfer has a quartic in **387 rational variables**, given by the sum of the squares of the **336 quadratic residuals** in this directory. All fixed coefficients and source instance ranges have the same interpretation as before. The sufficiently large odd shift remains ineffective. This is a new projection proof, not a claim about a global minimum.

## 1. Point chart, including exceptional cases

Work over K=Q(rho), rho^2=2, Delta=11-6rho. Write E:y^2=x^3-Delta*x and R0=(1+rho,2rho). Reciprocal coordinates are f=1/x, h=-y/x^2, with equation h^2=f-Delta*f^3. The affine chart excludes the point (0,0) of the original E and includes its origin as (f,h)=(0,0).

For reciprocal points (f,h),(g,k), impose
```
s(f-g)=h+k,
s(h-k)=1-Delta*(f^2+fg+g^2).
```
Together with the first point's curve equation these imply the second point's equation: multiply the first equation by h-k and the second by f-g. If f=g, the first gives k=-h and the second excludes h=0 (at a root of f-Delta*f^3 its right hand side is 1 or -2). Thus the chart includes nonvertical tangents as well as all distinct pairs in its domain. The original E difference A=U-V has
```
x(A)=s^2+Delta*(f+g),
y(A)=Delta*h-s*(Delta*f+x(A)).
```
Indeed in the reciprocal cubic with its usual infinity as origin, the chord through (f,h),(g,-k) gives x-coordinate -s^2/Delta-f-g for their standard difference. The reciprocal map translates the group origin by the two-torsion point (0,0) of that cubic. Translation by it sends reciprocal abscissa q to -1/(Delta*q) and ordinate r to r/(Delta*q^2), giving exactly the two formulas above. At q=0 the standard difference is that torsion point and the original difference is (0,0), also given by the formulas. Thus A is finite in every case. The two rows fixing x(A),y(A) to the coordinates of R0 make the shared reference points precisely H,H-R0. Inverses of h_H,h_HP are guarded by field unit equations; hence no zero reference ordinate enters a ratio.

Use a shared numerator U. Set c*u=1, C0=h_U/h_H, L0=h_U/h_HP. For each of the twelve inputs use only the three private fields
```
L_i=h(V_i)/h_HP, Fhat_i=c*f(V_i), sig_i=c^2*h_HP*s_i.
```
With shared FU=c*f_U, K0=c^3*h_HP^2, H0=K0*L0, the two field residuals are
```
sig_i*(FU-Fhat_i)=H0+K0*L_i,
sig_i*(L0-L_i)=c^2-Delta*(FU^2+FU*Fhat_i+Fhat_i^2).
```
The inverse change of coordinates gives exactly the chord/secant chart above. For the aggregate trace store sigsum=sum sig_i^2, den=c*K0, den*sigquot=sigsum, and
```
T=Tr(sigquot+Delta*u*(12*FU+sum Fhat_i)).
```
This is precisely Tr(sum x(A_i)). All field equations are quadratic in their retained registers, including the guards. For arbitrary zero inputs the chart still works: no division by X_i was introduced. Completeness needs only the nonzero canonical input witnesses of the retained source.

## 2. Height and contact circuit

Use the exact v115 fourth-power tree, a=M^8+784, paired eight-shift polynomials, shared coefficient circuit and derivative equations, with identical scales and constants. Write F_i for the group polynomial, r_i F_i=-partial_a F_i/(16a), and au=a*u. Thus omega_i=au*r_i=u*(-F_i'/16F_i), with sum omega_i=12. No division by a private r_i is required. The field aggregate trace above has exactly the same height bound on the integer labels m_i of A_i as in v115.

On every prime retained in the v115 radical argument (fixed exceptions enlarged by primes <=12), both contact arguments are integral; at most two distinct groups meet a simple linear root, and no multiple-prime exceptional factor remains. At such a prime v(u)=1. A group is active when F_i has positive valuation. If active, its logarithmic derivative has valuation -1: for one simple root this is immediate, and for two in the same group the retained condition p^2 not dividing their sum makes its derivative have valuation exactly one. For inactive groups the logarithmic derivative is integral. Consequently omega_i is a unit on each active group and is zero modulo p on all others. At most two omega_i are nonzero modulo p, and their sum is 12, a unit. For every input i the retained primes R_i have i active and log R_i >= 4.87 h(M)-O(1). This holds for arbitrary rational zeros, including collisions, by the v115 proof.

## 3. Boolean local tests

For f_H, f_U and conjugate(f_HP), form chi_f=u/(u+f^2) and let chi be their product. At any retained good prime all these denominators have opposite-parity terms. Each chi_f is integral and congruent to 1 exactly when v(f)>0, and to 0 otherwise. Here v(f)>0 includes the reciprocal origin, and is exactly the formal point condition. At a split prime at most one of the two slots can pass all three tests: if both passed then H and H-R0 would reduce to the origin at the same good place, which would make R0 reduce to the origin. Exclude the finite bad primes of this fixed point. At an inert prime neither passes for the same reason. Thus the rational trace of chi is 0 or 1 modulo p, and when it is 1 exactly one slot is selected.

Put E_i=C0-X_i, I_i=conj(L_i)-X_i, and
```
J_i=I_i^2+conj(Fhat_i),
B_i=c*E_i^2+J_i^4,
D_i=B_i/(u^2+B_i).
```
All are field elements. The compiler uses the affine expansion c*X_i^2-2*(c*C0)*X_i+c*C0^2 for the primary term. At a good prime all finite reciprocal abscissa valuations are even; this follows from the formal group expansion at the origin for positive valuations and the analogous local expansion at the point (0,0) for poles (or directly from the cubic equation). Since v(c)=-1, Fhat_i has odd valuation whenever nonzero. Thus the terms of J_i have different parity and v(J_i)>0 is equivalent to positive valuation of I_i and of f(V_i) in the conjugate slot. In B_i the valuations of nonzero terms are odd and multiples of 4; their minimum is unique. In particular v(B_i) cannot be 2. All D_i are integral with Boolean residues, namely D_i=0 modulo p if and only if v(E_i)>=2, v(I_i)>=1 and v(conj(f(V_i)))>0. This includes vanishing terms by the infinite valuation convention. The quadratic definition (u^2+B_i)*D_i=B_i has no zero-denominator solution because u is nonzero.

Aggregate using
```
L=sum r_i*D_i,
Z=1-Tr(chi)+au*Tr(chi*L),
alpha=u+Z^2.
```
At any retained good prime, Z is integral. If no common slot passes, Z=1 modulo p. If exactly one passes, Z reduces to the weighted sum of the Boolean failures in the selected slot. A nonempty subset of the at most two active weights has nonzero sum: a singleton is a unit and the full set has sum 12. Hence Z=0 modulo p if and only if the common slot exists and every active group passes its three tests.

The unchanged BB-native pole and tau*(1+alpha)=alpha, b=7*c*tau^2 force v(alpha)>1/2 at every retained prime (v(u)=1 and the two terms in alpha have different parity), so Z has positive valuation. We have obtained the common formal slot and every active test.

At formal points the reciprocal ordinate h has the same first-order logarithm comparison as the formal parameter z=-x/y: h/z=1-Delta*f^2, a relative unit 1 modulo p^4 for a nonorigin formal point, and h=z=0 at the origin. Thus C0 and conj(L_i), in the selected slot, are the primary and opposite logarithm ratios up to relative 1 mod p^4. Their corresponding integer-index ratios are j/h_index and (j-m_i)/(h_index-1), by the retained formal comparison (multiply by 2 to remove torsion). At least one denominator index is a p-adic unit. Since both actual ratios differ from X_i by positive valuation, X_i is integral at p; the integral ratios reduce to X_i. Multiplying by the two denominator indices and subtracting gives m_i=X_i modulo p. This also holds if one numerator is the origin, with zero index and exact zero ratio. In particular the v115 bound log R_i<=2h(X_i)+log(1+|m_i|) holds unless X_i=0 or m_i. The unchanged strict height margin and aggregate trace bound give the same contradiction for all sufficiently large fixed B_abc. All twelve inputs are integral. This proves soundness of the full preserved Jones core.

## 4. Ordered completeness

For a canonical nonzero integer tuple set A_i=[X_i]R0 and fix the trace T and height tree before choosing primes. Apply precisely the v115/v103 prime-pattern and simultaneous CRT preparation. The common reference and numerator points and all opposite points may be chosen in the same open neighborhoods with nonzero reference ordinates. The successful slot at the selected prime of group i has the four requisite formal points, with both actual formal-parameter ratios congruent to X_i modulo p^4: the original v115 errors X_i*S_U-S_H and X_i*S_V-T_H have valuation at least 3, and division by the formal ordinate ratio adds at least 1. The reciprocal-ordinate ratios differ from these by relative 1 modulo p^4. Thus E_i,I_i have valuation at least 4 and the active D_i is zero modulo p. All other groups are inactive and their D_j are integral regardless of the point denominators. The successful common selector is 1 and the opposite is 0, so Z is zero modulo p and the physical pole input b has valuation 1.

At the fixed prepared places and real infinity use bounded raw reciprocal point coordinates and ratios with nonzero reference ordinates, ensured by the same open-neighborhood argument. As the absolute slope tends to infinity, u~z^2/a, c~a/z^2, all chi_f tend to 1, J_i and B_i remain bounded, and D_i tends to zero. The normalized weights au*r_i tend to 1. Thus Z tends to -1 and alpha~u. All new denominators are nonzero in these neighborhoods and the real and dyadic preparations of b~7c are unchanged. Outside prepared places the v115 contact factorization gives nonpositive valuation of u away from selected primes with integral slope and even valuation with nonintegral slope. At negative odd valuations the terms in alpha have opposite parity, implying tau is a unit and b has positive odd valuation; at even valuations b has even valuation away from seven. The prepared value at seven has positive valuation. This proves square reduced denominator and every other BB preparation. The same native pole theorem supplies the remaining quadratic block. The core witness extends by all the displayed definitions.

## 5. Census and exact checks

76 preserved outer variables, 131 point/input-square registers, 27 height registers, 29 contact registers, 14 shared selector registers, 96 private detector registers, and 14 aggregation/pole registers give 387 variables. There are 52 unchanged Jones rows and 284 new quadratic residuals. The compiler pins the frozen v114 core, compares every outer row by named monomials, verifies exact contact expansions and the height margin, checks full coordinate support and degree, and exhausts 152561 integer valuation triples and 940 weighted Boolean cases. These finite checks supplement, rather than replace, the projection proof above. Run `node build.js` in this directory to check the table; `--write` regenerates it. No unconditional undecidability or optimality claim is made.
