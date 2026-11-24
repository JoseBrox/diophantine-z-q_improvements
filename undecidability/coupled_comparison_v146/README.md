# v146: coupled private comparisons with an isolated growth selector

Conditional quartic bounds: **566 general / 584 specified**, with 501 / 517 quadratic residuals and eight independently certified source integers. The source is v145; all arithmetic premises, the two/three comparison poles, the recursive scalar pole, and the Lucas amplifier of v143 are retained. This construction does not remove either Pell quotient.

## 1. Fusing the private tests

Use the notation of v143 and v145. At a private weighted pair let k be its target, S',T' the scaled slopes and F',G' the reciprocal abscissas scaled by k². The chart gives
F'(S'²+D F')=k⁴, G'(T'²+D G')=k⁴.
Indeed, with pi=eta+S'+T', the secant row yields S'²=(S'-T')pi-D(F'+G') and T'²=(S'-T')eta-D(F'+G'). Multiply by F',G', respectively, and apply d=pi F'=eta G' and the unit row.

For the primary slot use F_nu=F', E_nu=S'-2S_H; for the alternate slot use F_nu=conj(G'), E_nu=conj(T')-2conj(T_H). Replace the three fields used for each old pair of tests by two:
L_nu=E_nu²+u F_nu, J_nu(u+L_nu)=L_nu.
These equations are quadratic. The denominator cannot vanish on a solution since u is nonzero. The J_nu need not be locally integral everywhere: treating them as globally Boolean without qualification would be incorrect.

Keep all the original Boolean tests for the reference and three growth pairs and for the Lucas residual. Let W_g=u+sum of these unchanged fractions, W_i=sum of the sixteen new J_nu. Introduce two fields W_i² and V=W_g²+C W_i², where C=1/u. Use the harmonic selector
D_g Tr(V)=Nm(V), u² E_scaled=D_g.
The contact gate remains that of v145, with E_scaled². Thus sixteen slots save 32 rational variables and rows; the two new fields cost four. Net saving: 28 in each system. All operations are quadratic.

## 2. Growth survives every consumed prime

At any consumed good prime outside the inherited fixed exceptional set (enlarged if necessary to include p<=60), write v_p(q)=-mu, mu positive odd. The native pole obstruction gives v_p(g)>-mu/2. In g=1+E_scaled²+(C-q)²/q the last two terms have even and odd valuations, respectively, so a negative minimum cannot cancel. Hence v_p(C-q)>-3mu/4 and v_p(E_scaled)>-mu/4, giving v_p(C)=-mu, v_p(u)=mu and v_p(D_g)>7mu/4.

In each unramified slot W_g is integral and is positive in valuation exactly when all the unchanged growth/reference tests pass: their residues are 0 or 1 and their number is less than p. At most one slot can pass, because H and H-P0 cannot both reduce to the identity in a single slot at the good primes in question. Inert primes cannot pass. The two terms of V have even and odd valuations, so v(V)>0 implies v(W_g)>0 and v(W_i)>mu/2, with the usual convention v(0)=infinity. The converse holds as well. In particular V cannot vanish globally, and the harmonic equation forces at least one positive slot (if both valuations are nonpositive, the valuation of the norm divided by the trace is at most their maximum). There is exactly one successful slot. This argument does not require any integrality of the new private tests.

The unchanged growth tests therefore imply the original divisibility M_j³ | Delta_index for every comparison radical M_j and every nonzero Lucas residual. The v143 height and Lucas argument applies without discarding any input-denominator primes: it forces Delta_index=0 and, for A=|a|>100, gives log B>A/4+log A, with B the index maximum in v143.

## 3. Private soundness and the denominator loss

Only now discard primes in the denominators of the eight rational targets k_i. Let P_bad be their union radical; log P_bad<=sum_i h(k_i), where h is the logarithmic rational height.

At a remaining consumed prime in the successful slot, each F_nu has even valuation, and the two summands of L_nu have opposite parity of valuation. Equality v(L_nu)=mu could occur only if v(F_nu)=0 and 2v(E_nu)>mu. But then the corresponding scaled slope has the negative valuation of the reference slope. Its curve identity F'(S'²+DF')=k⁴ (or the conjugate identity) contradicts integrality of k: the left side has negative valuation. Thus v(L_nu) differs from mu. Each J_nu is integral in this slot and has residue 0 precisely if v(L_nu)>mu, otherwise residue 1. Since v(W_i)>mu/2 and p>60, every one of the sixteen tests passes. We obtain v(E_nu)>mu/2 and v(F_nu)>0.

The scaled slope has negative valuation by the error estimate. Its curve identity gives v(F')+2v(S')=4v(k), so the physical reciprocal abscissa has v(F')-2v(k)=2v(k)-2v(S')>0. The alternate slot works identically. Thus the two physical formal conditions are recovered. The positive valuation of the cleared slope errors, divided by the formal reference slopes, gives the same precision modulo p² as in v133/v139/v143. Consequently k_i is congruent to its integer difference label m_i modulo p². For M'_j=M_j/gcd(M_j,P_bad), this proves (M'_j)² | |num(k_i-m_i)| for each nonzero difference.

We give explicitly the modification of the global height absorption, since ignoring the lost primes would invalidate the compression. The v143 scalar estimate gives h(k_i)<=delta_N A with delta_N tending to zero as the fixed coefficient N grows. Its already absorbed aggregate estimate gives B²<=K_2 max_j M_j^(7/6), where K_2 is fixed independently of N for sufficiently large N. If k_i differs from its label, put J=|num(k_i-m_i)|>0 and choose a maximal M_j. Since M_j<=P_bad sqrt(J) and J<=2B exp(h(k_i)),
2 log B <= log K_2+(7/6)sum_nu h(k_nu)+(7/12)(h(k_i)+log B+log 2).
Thus
log B <= (14/17)sum_nu h(k_nu)+(7/17)h(k_i)+C_0 <= 7 delta_N A+C_0.
Choose N so that delta_N<1/28, A>100 and log A>C_0, using the original forced scalar lower bound on A. This contradicts the Lucas lower bound. All eight targets therefore equal their integer labels. The choice is effective in the specified route under its inherited quantitative premises, and ineffective in the general route as before.

## 4. Completeness

Use the original simultaneous preparation and reference recurrence, after choosing the source integers, scalar parameters and fixed growth/difference labels. For the additional real and fixed-place limits, choose reference neighborhoods avoiding 1+k² f(U)=0 and 1+k² f(V)=0 in both embeddings for every private pair. Along the old nonzero-label numerator progressions these exclude finitely many points (the prescribed abscissa would be -k²). They can be avoided before shrinking neighborhoods and applying the same simultaneous CRT and recurrence; no new local existence assumption is needed.

At the selected primes mu=1, the original synchronized formal depth d>=1 gives reciprocal valuations >=2d and cleared error valuations >=3d. Thus v(L_nu)>=3, v(J_nu)>=2 in the successful slot, and v(W_g)>=1, v(W_i)>=2. Hence v(V)>=2. The other slot has v(W_g)=0, and parity gives v(V)<=0 there. The harmonic value D_g has the positive-slot valuation, so E_scaled=D_g/u² is integral. The unchanged contact gate has nonnegative valuation and its pole input has positive odd valuation. At nonselected primes the original even-support or fixed-place preparation applies.

At the real and prepared fixed places in the large-slope limit, q_j is asymptotic to lambda^(-2), C tends to zero and u tends to infinity. The unchanged Boolean fractions tend to zero, so W_g is asymptotic to u. The new J_nu tend to F_nu/(1+F_nu), bounded by the neighborhoods just chosen. Hence V is asymptotic to u², Tr(V) to 2u², D_g to u²/2 and E_scaled to 1/2. The gate tends to 5/4, exactly the old BB preparation. These are limits in the relevant local fields, also at 2. All denominator nonvanishing and sign/valuation preparations are therefore preserved.

## 5. Verification and remaining obstacle

The builder uses the v145 sparse source with pinned predecessor. Five distinct integer parameter fixtures in each of the two routes gave exactly 566/584 variables and 501/517 quadratic rows, with exact sparse support and degree checks. These tests verify the compilation, not the inherited arithmetic premises. See the independent verifier for the finite support and valuation checks.

The small-Pell equation k=r+1+(p-1)h and third-Pell equation H=c+F²(B-c)+cF j still require their integral quotient certificates. The v144 deletion obstructions remain relevant. Merely certifying h+j does not prove either quotient integral. Even if k,H are already known integral, the possible denominators of h,j divide |p-1| and |cF| respectively (when these are nonzero). Integrality of h+j implies that their reduced denominators coincide, hence divide the gcd of these two moduli. Coprimality would suffice, but neither this coprimality nor an independent simultaneous integrality argument has been established in the required fibers. A genuine joint replacement must give both exact signed index conclusions, including all exceptional fibers, and permit simultaneous canonical witnesses. No seven-integer source or unconditional undecidability theorem is claimed.
