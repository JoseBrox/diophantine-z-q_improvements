# A shorter selective fraction gate: 507 variables, 454 quadrics

Under the same ordinary rational abc, arithmetic interfaces and external Jones source as v113, the new complete quartic preserves the coded-instance projection. The sufficient fixed height coefficient can increase. This improves 519/466 to **507/454**, with all twelve integer inputs and one native pole.

## Construction and proof

Write u_i=1/c_i, u=12/(sum c_i), c=1/u. Keep every equation of the [shared-native-pole construction](../abc_shared_native_pole_v113/README.md) except its five private gate definitions per input. Its retained norm-error register d_i satisfies d_i=u_i D_i, with D_i the physical error. Replace its gate by

    R_i=u_i d_i,
    T_i=u+R_i^2,
    V_i T_i=d_i^2,
    c(W_i-1)=V_i^2.

The last row is multiplied by 12 and uses the affine sum of the c_i. These are four quadratic equations in four private registers instead of five. The global W=product W_i, alpha=u+(W-1)^2, tau and native pole are unchanged.

At any good prime with v(u)=1, the terms in T_i have distinct valuation parity (also when d_i=0), so T_i is nonzero and, for finite d=v(d_i), s=v(u_i),

    v(V_i)=2d-min(1,2s+2d),
    v(W_i)=min(0,1+2v(V_i)).

In particular, W_i has no positive valuation at such primes. If s=1, v(V_i)>=0 holds exactly when d>=1. If s<=0, v(V_i)=max(2d-1,-2s)>=0 regardless of d. Zero d_i yields V_i=0,W_i=1 and satisfies the same conclusions with infinite valuation.

For a prime in R_i of the v113 proof, v(u)=v(u_i)=1. The retained pole implies v(alpha)>1/2 and hence v(W-1)>0, so W is a unit. Every W_j has nonpositive valuation, forcing v(W_i)=0. Thus d_i has positive valuation, D_i is integral at the prime, and the original field extraction applies. The same R_i lower bound and height absorption prove X_i integral. Negative odd valuations of u remain harmless under the global alpha normalizer. No new zero denominator stratum is accepted, since some R_i is nonempty for sufficiently large B and every T_j is nonzero at its primes.

For completeness, use the same ordered simultaneous integer witnesses and contact positions. At a selected contact of group i, d_i is positive in valuation and s=1; at every foreign group s<=0. The new W_j are units congruent to 1 in all groups, giving v(alpha)=1 and v(b)=1. At fixed prepared places and real infinity, u_i~u~z^2/a and d_i=O(1/u_i); hence R_i stays bounded, T_i~u, V_i=O(1/u^3), W_i->1, alpha~u. These limits supply all new divisor conditions and preserve the same BB-prepared pole. The other valuation parities and real/dyadic preparations follow exactly from v113. Thus the source-instance completeness is retained.

## Exact table and checks

The table removes 36 coordinates (A_i,S_i,H_i), adds 24 (R_i,T_i), replaces 60 rows by 48, and keeps the other 406 rows exactly by named monomials. The complete sparse table is quadrics.json. Its sum of squares has degree exactly four, over the same integer parameter ring. The deterministic builder checks all removed occurrences, retained equations, support, degree and counts; it also verifies the valuation formulas on 25,921 integer pairs. These are finite checks of the formulas, not a proof of the imported arithmetic premises. Run node build.js; use --write to rebuild. The builder was executed on the frozen predecessor before publication.

No new arithmetic premise, source universality assertion, or claim of optimality is made.