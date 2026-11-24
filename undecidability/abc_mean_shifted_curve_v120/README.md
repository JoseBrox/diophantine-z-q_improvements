# Mean-shifted cubic chart with a shared detector square

**Theorem.** Under precisely the [v119](../abc_signed_abscissa_v119/README.md) premises (including ordinary rational abc), the Jones transfer is a quartic in **324 variables**, the sum of squares of **273 quadratic residuals**. The defining shift is still fixed sufficiently large and ineffective. All twelve source integers are certified.

## 1. Exact shared chart

Keep the v119 reference, numerator, contact weights, height tree, shared primary selector, mean mu and variance. Write d=2*y(U)*h_HP and di=1/d; both are guarded by the unchanged inverse row. Move the common abscissa center to x_*=x(U)-d*mu, and define four shared fields:

    x_*=x(U)-d*mu,
    L=x_*/d,
    d*S=x_*^2-Delta,
    du=d*u.

For each i retain only three point fields e_i,Q_i,Y_i and one Boolean field D_i. The two point equations are

    di*Q_i=e_i^2,
    Y_i^2=L*S+(3*S+2*Delta*di)*e_i+3*L*Q_i+e_i*Q_i.

They recover the finite point with x(A_i)=x_*+d*e_i, y(A_i)=d*Y_i. Indeed Q_i=d*e_i^2 and

    ((x_*+d*e_i)^3-Delta*(x_*+d*e_i))/d^2
      = L*S+(3*S+2*Delta*di)*e_i+3*L*Q_i+e_i*Q_i.

The identity holds over the entire guarded chart, even when y(A_i), x(A_i), or e_i vanish. Conversely every finite A_i gives the unique registers by these formulas. The trace row is now T=Tr(12*x_*+d*sum e_i), still the trace of the sum of the actual abscissas. Thus the same v27 index-height inequality and v118 contact height estimates apply. Although the common center depends on the derivative mean, there is no new circular choice in completeness: A_i, their trace, and therefore the height center are fixed before primes or U are chosen; the shifted coordinates are filled last.

## 2. Sharing the curve square with the alternate detector

Replace the v119 alternate Boolean definition by the quadratic row

    D_i*(conj(du)+conj(Q_i))=conj(Q_i).

Since d is nonzero, this says exactly D_i=conj(e_i)^2/(u+conj(e_i)^2) whenever the denominator is nonzero. At any retained prime v(u)=1, the two denominator terms have different valuation parity, so D_i is integral Boolean and its residue is zero iff conj(e_i) has positive valuation. This applies in both slots, including zero errors and arbitrary inactive denominators.

Use precisely the v119 final weighted Boolean and variance aggregate. It forces every active group to pass, and the shared primary mean test and variance give C0=mu=X_i modulo p. In the opposite slot

    (x(A_i)-x(U))/(2*y(U)*h_HP)=e_i-mu=-X_i mod p.

The v119 signed local translation argument now gives X_i=+/-m_i modulo p at every retained active prime. Nothing in that argument requires the private slope fields. Its same signed residual bound, trace inequality and strict margin 28.51>14*(1001/997)^4 prove all twelve inputs integral. The outer source is unchanged.

## 3. Ordered completeness

Follow v119. At each selected prime the sole active group has mu=X_i modulo p, and the old signed abscissa comparison makes e_i=0 modulo p in the opposite slot. Thus D_i vanishes at the successful slot. All other conditions and the positive odd valuation of the physical pole input follow verbatim. For the fixed-place and real preparations choose the same bounded H,U neighborhoods and nonzero guards as v119. The normalized weights tend to 1 as the slope tends to infinity, so mu stays bounded and tends to the mean of the fixed integer tuple. The shifted point coordinates remain bounded because d and its inverse remain bounded. Hence every D_i tends to zero with nonzero denominator for large slope, while the old shared selectors, variance, pole input and its preparations behave exactly as in v119. No new finite avoidance or recurrence hypothesis is necessary. Apply the same BB-native realization. All added fields are then filled by their exact definitions.

## 4. Census

The old four shared fields d^2,K0,L0,B0 are replaced by four shared fields x_*,L,S,du. Each private group formerly had three point fields and two detector fields; it now has three point fields and one detector field, sharing its scaled square. The saving is exactly 24 rational coordinates and 24 quadratic residuals. All 52 original Jones rows and their borrowed squares are preserved. Run node build.js (or --write). The pinned exact compiler checks coefficient expansions, the shifted cubic identity, the unchanged outer equations, support, degree, valuation fixtures and the height margin. No unconditional undecidability or global minimum is claimed.
