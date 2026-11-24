# Signed abscissa comparison: 348 variables, 297 quadratic residuals

**Theorem.** Under exactly the retained arithmetic and external Jones coding hypotheses of [v118](../abc_primary_moments_v118/README.md), with ordinary rational abc and a sufficiently large fixed positive odd shift, the table gives a quartic rational undecidability transfer in **348 variables**, the sum of squares of **297 quadratic residuals**. The 52 Jones equations and their twelve certified inputs are unchanged. The sufficient shift remains ineffective.

## Exact chart

Work over K=Q(rho), rho^2=2, on E:y^2=x^3-Delta*x with Delta=11-6rho and R0=(1+rho,2rho). For a point of finite nonzero x write f=1/x, h=-y/x^2; the reciprocal chart includes O as f=h=0. Use the v117 reference equations for H,H-R0 (translation by (0,0) gives affine coordinates (-Delta*f,-Delta*h), so the chord formula, including tangents, applies). Write U=(x,y), with f_U*x=1, h_U*x^2=-y, h_U*h_Uinv=1 and h_H*C0=h_U. Define the shared fields

    d=2*y*h_HP, d*di=1, d2=d^2,
    K0*d2=2*y, L0=3*x*di, B0*d2=3*x^2-Delta.

The guards imply that all reference ordinates and y are nonzero. For each input X_i use three fields a_i,s_i,t_i:

    d*t_i=s_i^2,
    a_i*t_i+K0*s_i=B0+L0*a_i+a_i^2.

They recover the finite point A_i=(x+d*a_i,y+d*a_i*s_i). Indeed multiplication of the second equation by d^2 gives 2*y*s_i+d*a_i*s_i^2=3*x^2+3*x*d*a_i+d^2*a_i^2-Delta. Multiplying the difference by d*a_i gives exactly the difference of the cubic curve residuals at A_i and U. If a_i=0 the recovered point is U and the equation gives the tangent slope. Conversely whenever x(A_i)!=x(U), use the ordinary line slope s_i and t_i=s_i^2/d. Thus no soundness exclusion arises from zero input or zero abscissa difference. The stored T=Tr(12*x+d*sum a_i) is Tr(sum x(A_i)). By the v27 weighted trace theorem with weights all 1, m_i^2<=C1*h(T)+C2 for every integer label m_i in E(K)=Z*R0+E[2], including torsion translates. For completeness the A_i are fixed first and U may avoid finitely many forbidden fibers.

## Contacts and primary/alternate tests

Use the v118 height tree and derivative circuit verbatim, with C=(1001/997)^4 and center a=M^32+784. In particular M>=B_abc and h(X_i),h(T)<=C*h(M)+O(1), uniformly in B_abc. After the costed denominator exclusion, each retained prime set R_i satisfies log R_i >= (28.51-12*C)*h(M)-O(1). At such a prime all X_j are integral, v_p(u)=1, c=1/u, and omega_j=au*r_j are integral weights of sum 12; at most two are units and the others reduce to zero. Group i is active. Omit also the fixed bad curve and reference primes and p<=12.

At each unramified slot form

    R=c*f_H^2+c^2*f_U^2+c^3*conj(f_HP)^2,
    chi0=1/(1+R),
    t=conj(h_U+h_Uinv), chiU=c/(c+t^2).

Finite reciprocal abscissa valuations are even. The three terms of R have distinct nonzero classes modulo four, so chi0 is integral and Boolean, residue 1 exactly when H,U are formal at this slot and H-R0 formal at the conjugate slot. There cannot be two successful slots (otherwise R0 would reduce to O), or an inert success. Also chiU is integral Boolean with residue 1 iff t is integral: this is precisely when h_U is a unit at the opposite slot, since for nonzero valuation of h_U the sum with its inverse has valuation -|v(h_U)|. At that slot f_U is a unit by h_U^2=f_U-Delta*f_U^3, so x(U) and y(U) are units.

Use the primary mean and variance

    mu=sum(omega_j*X_j)/12,
    var=sum(omega_j*X_j^2)-12*mu^2,
    chiE=u/(u+(C0-mu)^2),
    chi=chi0*chiU*chiE.

The mean and variance are integral. Opposite-parity denominator terms make chiE integral Boolean, passing precisely if C0=mu modulo p. For each i use two private fields

    Q_i=(conj(a_i)+X_i)^2,
    D_i=Q_i/(u+Q_i).

They give integral Boolean failures D_i: residue zero iff conj(a_i)+X_i has positive valuation. Zero errors cause no problem, and no restriction on inactive raw denominators is needed. Form

    Z0=1-Tr(chi)+au*Tr(chi*sum r_i*D_i),
    Z=Z0^2+c*var^2, alpha=u+Z^2,
    tau*(1+alpha)=alpha, b=7*c*tau^2.

The BB-native pole implies square reduced denominator of b. At a retained prime alpha has unequal-parity terms and is nonzero. If v(alpha)<=0 then v(tau)<=0, giving negative odd v(b), impossible. Thus v(alpha)>=1 and v(Z)>0. The two terms of Z have distinct parity; hence v(Z0)>0 and v(var)>0. No successful slot would give Z0=1 modulo p. In the unique successful slot, the weighted Boolean failures must all vanish: a nonempty subset of the at most two active weights has unit sum (a single unit or the total 12). The variance forces all active X_j=mu modulo p, since for two active weights w,w' it equals (ww'/12)*(X_i-X_j)^2. Therefore C0=X_i in the primary residue field and a_i=-X_i in the opposite residue field for each active i.

## Signed recovery and soundness

In the opposite slot put ell=v(h_HP)>=1. The identity x(A_i)-x(U)=2*y(U)*h_HP*a_i makes the abscissas congruent. The cubic equation implies integral y(A_i) congruent to either y(U) or -y(U), both nonzero. Choose epsilon=+1 or -1 so epsilon*A_i reduces to U. Then V=U-epsilon*A_i is formal. For the usual parameter z=-x/y at O, translation by U on the smooth integral group gives

    x(U-V)-x(U)=-2*y(U)*z(V)+O(z(V)^2).

The expansion is integral, with linear coefficient from the invariant differential dx/(2y)=dz+O(z)dz. Since 2*y(U) is a unit, v(z(V))=v(x(A_i)-x(U))>=ell when V!=O. If the abscissa difference vanishes, the chosen sign and nonzero reduction of y(U) give V=O. In either case division by 2*y(U)*h_HP gives z(V)/h_HP=-a_i=X_i modulo p. On formal points h/z=1-Delta*f^2, and the retained logarithm has the same leading parameter. Let j,h0,m_i be integer labels of U,H,A_i. The exact formal logarithm ratios are j/h0 and (j-epsilon*m_i)/(h0-1) in the two slots, by multiplication by 2 to remove torsion. Both reference indices are nonzero by the nonzero reference ordinates and the group hypothesis. Both ratios are integral by the already established comparisons, including V=O. Reducing after multiplication by the respective integer denominators gives

    j=h0*X_i mod p,
    j-epsilon*m_i=(h0-1)*X_i mod p.

Thus X_i=epsilon*m_i modulo p, with sign permitted to depend on p and i. If X_i=A/Q is reduced and neither m_i nor -m_i, then the nonzero integer (m_i*Q-A)*(m_i*Q+A) is divisible by R_i. Hence log R_i<=2*h(X_i)+2*log(1+|m_i|). The strict margin 28.51>14*C gives

    (28.51-14*C)*h(M)<=2*log(1+|m_i|)+O(1).

Together with m_i^2<=C3*h(M)+C4 this bounds both |m_i| and h(M) uniformly in B_abc. For sufficiently large B_abc it contradicts M>=B_abc. All twelve inputs are therefore integers, and the preserved Jones core has its old soundness.

## Ordered completeness

For a canonical nonzero source tuple fix A_i=[X_i]R0, hence T,M,a before prime selection. Use the original v115/v118 prime pattern and v103 simultaneous CRT with fixed-place and real recurrence. Enlarge temporary finite avoidance by primes of the fixed nonzero x(A_i),y(A_i); this is permitted and adds no soundness hypothesis. At a selected prime of group i, U-A_i is formal at the opposite slot, so x(U),y(U) are units there. The old primary and opposite comparison estimates give C0=X_i and z(U-A_i)/h_HP=X_i modulo p, with v(z(U-A_i))>=v(h_HP). The translation formula gives a_i=-X_i modulo p. All three common selectors pass at the successful slot, the opposite slot fails, and the sole active group passes its alternate test. Thus Z0 and var vanish modulo p, v(alpha)=1 and v(b)=1.

At fixed prepared places and at real infinity choose bounded point neighborhoods avoiding all chart poles and zero reference ordinates, U=+/-A_i, and h_U+1/h_U=0. These are finitely many fibers, excluded by the same recurrence used in v115. All point chart values including d and its inverse then remain bounded. As the absolute slope tends to infinity, the original asymptotic gives u~z^2/a, c~a/z^2 and omega_i~1. Hence chi0->1, chiU->0, chiE->1, D_i->0; mean and variance remain bounded. Thus Z0->1, Z->1, alpha~u, tau~1 and b~7c. These limits ensure the denominators are nonzero and all old dyadic, seven-adic and real preparations hold: b in 7*Q_2^{*2} of sufficient positive depth, v_7(b)>0, and 0<b<1. At remaining nonselected primes the v115 factorization gives v(u)<=0 for integral slope and even v(u) otherwise. Negative odd v(u) gives v(alpha)<=v(u)<0 and tau a unit, hence positive v(b); even v(u) gives even v(b) outside seven. All these assertions allow arbitrary point denominators. Thus b has square reduced denominator and every other BB preparation. Apply the same native-pole realization and fill the quadratic registers. No point is chosen anew after the contact and CRT stages.

## Census and reproduction

76 preserved outer registers, 130 point/input-square registers, 29 height registers, 29 contact registers, 20 common detector registers, 48 private detector registers and 16 aggregation/pole registers give 348 variables. There are 52 preserved outer and 245 new quadratic residuals. Their sum of squares has degree exactly four. Run node build.js (or --write to regenerate). The pinned compiler checks the Jones equations by named monomials, the exact line identity, contact expansions, full support and degree, the rational height margin, 10523 valuation cases and 940 Boolean cases. The table was rebuilt and compared exactly on promotion. The finite checks verify algebraic prescriptions, not the inherited arithmetic premises. No unconditional undecidability or minimality claim is made.
