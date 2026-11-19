# Quartics under fixed weak rational abc

The 62-coordinate ordinary-abc quartic in the companion package supplies the scaled elliptic charts, common detector gate and two native pole blocks here. Changing its contact map and the exponent in its single gap gives the following additional hypotheses/count tradeoff. Each variable count includes the input.

| Weak abc exponent | Coordinates | Quadratic rows | Exact degree | Monomials | Exact coefficient height |
|---|---:|---:|---:|---:|---:|
| 121/100 | 64 | 52 | 4 | 856 | max(109940,B²+4091) |
| 16/15 | 63 | 51 | 4 | 853 | max(109940,B²+4091) |

The count and coefficient data hold for every fixed odd B≥81. The integer input projection is proved for sufficiently large such B under the other elliptic, prime-pattern, trace-height and twist inputs of Brox v65. The sufficient shift is ineffective. The prior 62-coordinate family uses ordinary rational abc.

## The contact calculation

Use the roots Θ={−2,−1,−5/7,−1/2,−1/5,1}. The map z=(5t+1)/(2t+4) carries them bijectively to the six v22 degree-four Belyi positions {0,−2,−1/2,1,−1,∞}. It has nonzero fixed determinant 18, with all exceptional primes contained in the inherited fixed set. For each t outside Θ, the product M(t) of primes outside the fixed set with positive odd valuation on a t−θ satisfies

    log M(t) ≥ γ h(t)−O(1),          γ=8/κ−6.

This follows directly from the explicit signed abc triple of v22, section 2, and the sextic numerator estimate. The signed triple controls the radical of the full homogeneous six-root form, while rad(J)²/|J| bounds even its multiplicity-one support below. Changing primitive coordinates through the indicated Möbius map modifies only the fixed coefficient primes and bounded height constants. Every contact now lies in the affine line, so a pole of t contributes no contact prime.

For both arguments t₀,t₁ replace the physical weight by

    w(t) = ∏(t−θ)/t⁴.

Its numerator multiplied by 70 has coefficients −10,−89,−230,−150,170,239,70 in ascending order. Retain auxiliaries e=1/t and f=e² and enforce exactly

    te=1,    f=e²,
    70w=70t²+239t+170−150e−230f−89ef−10f².

These are three quadrics per block, matching the size of the old eight-root contact subcircuit. No selected contact can have t=0 modulo a good prime, since zero is not in Θ. At a consumed prime the physical weight has positive odd valuation, and each actual solution has w≠0 because q_jw_j=1. Thus the contact-zero exception is excluded. The new te=1 equation excludes t=0 on the entire rational variety.

The 62-coordinate template stores t,e,f,w with physical factor c, and has c⁻¹ available; dividing the above three equations by c² gives the literal stored quadrics. The old power registers X²,X⁴ remain. Add X⁸=(X⁴)² in both cases, and X¹⁶=(X⁸)² for 121/100. Change only the final power used in the old gap equation, giving

    G = t₁−t₀ = B+Xᵈ+Tsc²,       d=32 or 16,       Tsc=2 times the stored half-trace.

Thus there are 62+2 or 62+1 coordinates. Every new register occurs in the expanded quartic.

## Soundness

Take X nonzero. The unchanged 62-coordinate local extraction gives an integer m, the index of U−V. At every prime counted in M(t₀) or M(t₁), X is integral and X(m−X) vanishes modulo the prime. In particular, if X=u/v in lowest terms and X differs from m, both products divide the nonzero integer |u(mv−u)|. Therefore

    h(G) ≤ (2/γ)(2h(X)+log(1+|m|))+O(1).

Set s=Xᵈ+Tsc². It is nonnegative, thus h(s)≤h(B+s) and h(G)≥log B. By the signed mixed-power theorem of Brox v58, applied to the plus sign,

    h(X) ≤ c h(s)+O(1),        c=(2κ−1)/(d−κ(d/2+2)).

The needed denominator is positive for both rows. If s=0 then X=0, already excluded. The resulting coefficient of h(G) on the right after substitution is 4c/γ. Its values are 17182/18907 for the weak row and 17/30 for the stronger row, both less than one. Hence h(G) is bounded above by a fixed multiple of log(1+|m|)+1. The height of X is bounded in the same way. From Tsc²=s−Xᵈ one obtains 2h(Tsc)≤h(s)+d h(X)+log 2, and the retained scaled-trace bound m²≤C(h(Tsc)+2h(X))+J₀ now bounds m. Thus h(G) is uniformly bounded independently of B. This contradicts h(G)≥log B at every sufficiently large fixed shift, proving X=m. The remaining possible input X=0 is integral.

## Completeness

For X=n≠0 use the retained family H=[h]R₀,U=[hn]R₀,V=[(h−1)n]R₀ as in v65 and the companion 62-coordinate proof. The scaled trace is fixed prior to choosing the comparison primes. The two fixed lists Θ and Θ−G are disjoint because G≥B≥81 exceeds their diameter. At the other argument evaluated at a chosen root of one translated list, q=1/w is a rational unit outside finitely many primes, and 1+q² is a positive rational number. Exclude these primes, denominators, reductions of the point-chart avoidance values, and all bad reductions of the contact polynomials before applying the retained finite-list prime-pattern theorem. If desired exclude the finitely many primes dividing the numerator of the other argument itself; that argument cannot vanish since the gap exceeds the diameter and the absolute values of the contacts.

For t_j=N/L+g_j, g₀=0, g₁=G, the twelve distinct positive prime values are p_{j,θ}=N+(g_j−θ)L after absorbing the rational coefficients into the common L. We have the exact identity

    w_j = ∏θ p_{j,θ} / [ L² (N+g_jL)⁴ ].

Thus each w_j has the selected squareclass, with unit leading coefficient in w_j∼t_j². At its selected primes v_p(w_j)=1 and v_p(q_other)≥0, while 1+q_other² remains a unit by the fixed exclusions. The unchanged common W gate gives v_p(b_j)=1 exactly as proved in the companion 62-coordinate chart. The other primes have even valuations of b_j because b_j=w_j τ_j². At the real and fixed finite-place preparations both weights tend to positive infinity in the real embedding and their reciprocals tend to zero at the prepared places. The same two-adic squareclass and depth, real positivity and native pole-input realization as for the 62-coordinate chart apply, since every selected prime is 1 modulo 8 and each displayed denominator is a square. Both arguments are nonzero for large real slope.

For X=0 use the explicit companion zero chart with both raw errors and reciprocal products zero. It has W=1,D=0 and τ_j=(1+q_other²)/2. The fixed gap is B+Tsc². The same disjointness, avoidance, prime selection and fixed-place preparations supply the two pole blocks and all new power coordinates. Both completeness directions are therefore retained.

Use `construct.py --parent /path/to/record62/quadrics.json` to rebuild the supplied specifications. The main 62-coordinate verifier validates the unchanged rows. `verify.py` checks the replacements, both Belyi and sextic identities, both height margins and the full independent integral expansion, exact support, height and content.
