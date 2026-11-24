# Scalar alternate failures via a lifted mean (v123)

**312 rational variables, 260 quadratic residuals**, under the same retained premises as v122, including ordinary rational abc and the Jones coding theorem. All twelve certified integers and the single BB-native pole remain. The physical-point and input projection is preserved, not the full auxiliary zero set.

## 1. Lift the mean without changing its local residue

Use the notation of [v120](../abc_mean_shifted_curve_v120/README.md), [v119](../abc_signed_abscissa_v119/README.md) and [v122](../abc_nested_selector_v122/README.md). In particular c=1/u, d=2*y(U)*h_HP, and mu is the exact derivative mean. Add rational a, a2, nu with

    a2=a^2, (c+a2)*(nu-mu)=a.

The denominator cannot vanish (otherwise a=0 and c=0). At every retained prime v(u)=1 and v(c)=-1. For nonzero a of valuation j, the correction has valuation j-min(-1,2*j)>=1; for a=0 it vanishes. Thus nu is integral and equals mu modulo p, for arbitrary rational witnesses. Conversely every t in p*Z_p is locally attained by a/(c+a^2) with integral a: the equation a=t/u+t*a^2 has derivative 1 modulo p and a unique root in the required residue class by Hensel. Rational a can approximate these local roots at any finite list of selected primes and simultaneously stay in fixed bounded neighborhoods of 1 at the prepared places and over the reals, by weak approximation over Q.

## 2. A different common scaling

Keep d, set D=d^2 and I=1/D, and define x_*=x(U)-d*nu, L=I*x_*, S=L^2-Delta*I^2, K=3*L^2-Delta*I^2. Replace each private shifted point chart by

    Q_i=e_i^2,
    Y_i^2=L*S+K*e_i+3*L*Q_i+e_i*Q_i.

These are exactly the original elliptic curve equation for x(A_i)=x_*+D*e_i, y(A_i)=d^3*Y_i after division by d^6. The inverse guard D*I=1 ensures d!=0. The identity is valid at zero abscissa or ordinate, and every finite point lifts. Set T=Tr(12*x_*+D*sum e_i); the old trace-height and contact circuit apply to the actual abscissas, not to the shifted chart coordinates.

The v122 nested selector chi is unchanged, including its primary test C0=mu. Define one *rational* failure coordinate per input:

    D_i*(u+Tr(Q_i))=Tr(Q_i).

This is quadratic because Tr(Q_i)=2*Q_i[0] is linear in the stored square. Its denominator cannot vanish since u!=0.

## 3. Exclude only index primes, not point denominators

At a retained prime with a successful primary slot, H and U are formal there, H-R0 is formal at the opposite slot, and h_U is a unit in the opposite slot. Discard the fixed bad primes of the v119 proof and primes dividing the nonzero integer labels m_j of the A_j. The latter cost at most sum log(1+|m_j|), not a multiple of the abscissa heights. At the primary slot put l=v(z(U))>=1. H-R0 reduces to -R0, so h_HP is a unit after the fixed exclusion; v(d)=-3*l and v(x(U))=-2*l. At a good odd prime a finite two-torsion point is not formal, and a nonformal point has integral abscissa. If A_i is formal, the exact logarithm ratio log(A_i)/log(U)=m_i/j holds after doubling away the torsion, where j!=0 is the integer label of U. Because p does not divide the nonzero m_i, v(z(A_i))<=v(z(U)). Consequently in every case v(x(A_i))>=-2*l. As nu is integral, the numerator x(A_i)-x(U)+d*nu has valuation at least -3*l. Dividing by d^2 gives v(e_i)>=3*l>0 at the primary slot, **for all i, including inactive groups**.

At the opposite slot v(d)=ell>=1, since y(U) is a unit there. Write e_i' for the opposite-slot value. If v(e_i')>0, Tr(Q_i) has valuation at least 2 (possibly infinity). If v(e_i')<=0 its valuation is exactly 2*v(e_i')<=0 because the primary square has positive valuation. Thus the scalar D_i is integral Boolean, with residue zero exactly when the opposite-slot e_i has positive valuation. There is no assertion of its integrality when no slot succeeds.

## 4. Separate common success from the failure sum

Use the unchanged derivative weights omega_i=au*r_i and variance. Instead of the old weighted field failure trace, put

    F=sum r_i*D_i, J=au*F,
    Z0=(1-Tr(chi))^2+c*J^2,
    Z=Z0^2+c*var^2, alpha=u+Z^2.

The physical tau and BB pole are unchanged. At a retained prime, its square-denominator obstruction forces v(alpha)>0, hence v(Z)>0. In each of Z and Z0 the two terms have different valuation parity, regardless of arbitrary poles. It follows that 1-Tr(chi), J, var all have strictly positive valuation. In particular the common selector succeeds in exactly one slot **before** the argument concerning scalar D_i is applied. At a prime not discarded in Section 3 all D_i are therefore integral Boolean. At most two omega_i are units, their total is 12, so J vanishing modulo p forces every active D_i to vanish. The old variance and primary tests give C0=mu=X_i modulo p. In the opposite slot, positive e_i gives

    (x(A_i)-x(U))/d = d*e_i-nu = -X_i mod p.

The v119 signed translation and formal logarithm argument therefore yields X_i=+/-m_i modulo p. No stronger local assumption on arbitrary witnesses is used.

The old radical lower bound for each input now loses at most sum log(1+|m_j|). If X_i is neither m_i nor -m_i, its signed numerator product bounds the remaining radical. With C=(1001/997)^4 this gives

    (28.51-14*C)*h(M)
        <= sum_j log(1+|m_j|)+2*log(1+|m_i|)+O(1).

The trace theorem bounds max_j m_j^2 by O(h(M)+1); the positive margin then bounds h(M) uniformly in the fixed shift. Increasing the old sufficiently large shift (still ineffective) gives the same contradiction. This proves integrality of every input and source soundness.

## 5. Ordered completeness

Fix the canonical nonzero integer inputs and points A_i before the height center and slope. Add the finitely many nonzero label divisors to the temporary avoidance set. Use the old prime supplier and simultaneous point preparation with one active group i at each selected prime. At such a prime, the old comparison a_i=(x(A_i)-x(U))/d in the opposite slot satisfies a_i=-X_i modulo p and mu=X_i modulo p. Thus -a_i-mu belongs to p*Z_p. Use Section 1 and weak approximation to choose the new common rational a so that nu=-a_i to accuracy >ell at that opposite slot, simultaneously for all selected primes, where ell=v(d) at that slot. This is an ordinary finite rational approximation problem; a is chosen after the slope and common points, and no height/contact coordinate depends on a. At the same time choose a close to 1 at every prepared place and at the real place. Then the active e_i=(a_i+nu)/d has positive valuation, D_i=0 mod p, and the new Z0,Z vanish mod p. The unchanged physical pole has valuation 1 at each selected prime.

At the prepared places, choose the same bounded point neighborhoods as before with d and 1/d bounded. With z large, c->0, u->infinity, mu stays bounded, and a near 1 gives bounded nu. Hence e_i,Q_i are bounded, D_i->0, J->0, and the old chi->0. It follows that Z0->1, Z->1, alpha~u, tau->1, b~7c; the previous BB preparations hold. At arbitrary other primes, negative odd v(u) gives positive v(b) and even v(u) gives even v(b) outside 7, just as in v119/v122. The changed rational denominators are nonzero because they are nonzero at the selected primes. Apply the old BB realization to the actual physical pole. This constructs witnesses without imposing any of the completeness-specific prime restrictions on soundness.

## 6. Counts and exact regeneration

The twelve field failures become twelve scalar failures. Remove the old two-component du and one component of the failure sum. Add D and K (four coordinates), three lifted-mean coordinates and one failure-square coordinate. The other old coordinates are reused (in particular di now means 1/d^2, failTrace is J). Thus 319-15+8=312. There are 260 rows, each of degree at most two, and every coordinate occurs. The sum of squares is of exact degree four.

Run `node undecidability/abc_scalar_failures_v123/build.mjs` to replay the exact table (or add --write). The compiler was executed against the pinned v122 blob; it checks degree, support and local valuation fixtures. The displayed field identities and local proofs are the mathematical verification; full repository CI and an independent proof of the inherited arithmetic assumptions are not claimed.
