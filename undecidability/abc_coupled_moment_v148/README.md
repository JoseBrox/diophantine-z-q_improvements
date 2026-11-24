# v148: couple the weighted alternate failure, variance and unit moment

**290 rational variables, 239 quadratic residuals**, under ordinary rational abc and the other retained v145 premises. Twelve certified source integers and the one native pole are unchanged. This improves 291/240 by one variable and one row.

## 1. Exact quadratic substitution

Keep the common-selector field V=R²+c(C0-mu)² and the harmonic equation D Tr(V)=Nm(V) of v145, where c=1/u. Keep all shifted-point charts, private scalar fractions D_i, derivative coefficients r_i, height and contact data of v126/v128. Use a for the common positive contact center, r=sum r_i, L=sum r_i X_i. The retained equations give a r=12c, mu r=L. In particular a and r are nonzero. Let s=Tr(h_U), with its inverse already guarded; T=(s+s^(-1))² is the existing n_trace_h_unit2 register.

In the old construction J=12 sum(r_i D_i)/r and var=12(sum r_i X_i²-mu L)/r. We no longer store either separately. Introduce six rational registers F,G,L_u,W,W2,Z:

    F=sum_i r_i D_i,
    G=a F,
    a L_u=T,
    r W=12(sum_i r_i X_i²-mu L+F G+L_u T),
    W2=W²,
    Z=D²+c W2.

All terms are at most quadratic in stored coordinates, including the existing X_i². The exact identity is

    W=var+c J²+u T².

Use the physical alpha=u+Z², tau(1+alpha)=alpha, and the same BB-native pole with physical input 7c tau². The n_alpha and n_tau registers now store their unscaled values.

This eliminates seven registers (var, var², J, J², Z0, scaled Z and T²) and nine residuals, replacing them by the six registers and eight rows above. This is a new projection-equivalent detector, not a claim of equality of auxiliary zero sets.

## 2. Sequential local soundness (no circular private-integrality assumption)

Use precisely the retained primes of v126, with v(u)=1, v(c)=-1, excluding the fixed bad primes, input denominators and nonzero difference-label factors as there. The pole obstruction and the unequal parities of u and Z² force v(alpha)>0 and hence v(Z)>0. Unequal parities of D² and c W² give v(D)>0 and v(W)>0. By the harmonic argument of v145 this yields a unique successful slot for V, with H and U formal there, H-P formal in the opposite slot and the common primary ratio equal to mu modulo p. No claim about s or the opposite h_U unit has yet been used.

We now show that the private scalar fractions are integral Boolean at these primes BEFORE extracting the unit condition. This is the primary-slot part of v123 section 3, which does not require the opposite h_U unit: if l=v(z(U))>=1, H-P reduces to -P at the primary slot, so h_HP is a unit after the fixed exclusions. With d=2y(U)h_HP we have v(d)=-3l, v(x(U))=-2l. For each private difference A_i, either it is nonformal and has integral abscissa, or it is formal and the formal logarithm comparison after doubling gives v(z(A_i))<=l, because p does not divide its nonzero label. A zero-label finite torsion point is nonformal. Thus v(x(A_i))>=-2l for all i. The mean is integral since the derivative weights are integral and all X_i are integral at the retained primes. The shifted-chart definition e_i=(x(A_i)-x(U)+d mu)/d² therefore gives v(e_i)>=3l at the primary slot for every i, including inactive groups.

The trace of e_i² consequently has valuation 2v(e_i') if the opposite value e_i' has valuation <=0, and valuation >=2 (possibly infinity) otherwise. The v128 shifted-square register implements this exact trace. The equation D_i(u+Tr(e_i²))=Tr(e_i²) makes D_i integral with residue 1 in the former case and 0 in the latter. Its denominator cannot vanish at these primes. This proves the needed Boolean property without the opposite unit assumption. In particular J and var, which are defined by the retained normalized derivative weights, are integral at every retained prime of a rational witness.

If s is not a unit then v(u T²)=1-4|v(s)|<=-3, whereas v(var)>=0 and v(c J²)>=-1. The negative unique minimum contradicts v(W)>0. Thus s is a unit. Now v(u T²)>=1, so if J is a unit the c J² term has unique negative valuation -1, again impossible. Hence v(J)>0, and consequently v(var)>0. Since h_U has positive valuation in the primary slot, its trace being a unit makes h_U a unit in the opposite slot. This recovers every v123/v125/v126 local test. The weighted residue argument (at most two active groups and unit total weight), variance, and signed formal logarithm argument yield X_i congruent to plus or minus its integer label, as before. The v126 height/radical argument is unchanged, including its accounting of discarded label primes. All twelve source inputs are integral; the same sufficiently large ineffective threshold suffices after retaining the previous fixed exclusions.

## 3. Completeness and foreign primes

Use the original v125/v126 ordered completeness and interpolation. At selected primes D,J,var have positive valuation and s is a unit. Thus W,Z are positive in valuation and v(alpha)=1, so the physical pole has valuation one. For a nonselected prime with negative odd v(u), the two summands of alpha have different parities; alpha has negative valuation regardless of new poles of W. Hence tau is a unit. At an even valuation the square factor in the pole preserves parity outside 7. This restores the simple foreign-prime argument without the extra v145 unit-term parity case.

At the real and prescribed fixed-place limits, the old bounded point neighborhoods can be chosen with s nonzero, and hence T nonzero (s is rational and s+s^(-1) cannot vanish rationally). The old asymptotics give c tending to 0, u tending to infinity, bounded D,J,var, and T bounded away from zero. Therefore W is asymptotic to u T², Z to u T^4, alpha to u² T^8, and tau tends to 1. The physical pole is asymptotic to 7c, so the inherited real, dyadic and seven-adic preparations and BB realization still apply. These are local asymptotics at all prepared places, not merely real limits. All divisors are nonzero at the prepared witnesses. No new prime-pattern or point interpolation premise is used.

## 4. Audit

The deterministic builder compares all 231 retained named rows exactly (including all 52 Jones source rows), removes exactly the seven registers listed above, and checks full support and quadratic degree. The complete coefficient table is committed. The independent valuation check in verify.mjs supplements the proof of the sequential moment argument. This is conditional on the inherited premises; no full CI or unconditional H10(Q) claim is made.
