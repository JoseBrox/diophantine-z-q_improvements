# Positive balancing denominators for the eleven-variable rows

The two ordinary-abc rows admit one more change before the positive detector of POSITIVE.md. The degree bound is **36,482,433** with nine contacts and **56,391,041** with seven. Their support bounds are strictly below 2^237 and 2^243, respectively. Both use eleven total rational variables and the same inherited ordinary-abc, elliptic, height, prime-pattern and intrinsic-pole premises.

For each of the six tests let c be the unsquared reciprocal-abscissa test in the first four positions, and the square of the cross or target test in the last two. In the upstream v75 detector the raw second summand supplied to a field factor is

    a = [c/(1+u c)]² / u.

Use instead

    a = c²/[u(1+u² c²)].

The final detector still takes the field product of the positive factors 1+a² and uses its original pole input with the new W. If c=0 the summand is zero.

At an unramified consumed odd valuation nu=v(u), the valuation of every nonzero c is even. For the first four tests this is the upstream elliptic abscissa parity lemma. For the last two it follows from the explicit square. Thus v(uc) is odd and the two summands of 1+u²c² have unequal valuations. In particular

    v(c²/(1+u²c²)) = 2v(c)-min(0,2v(u c))
                     = 2 max(v(c), -nu).

This is the original squared-test valuation at every consumed place and gives exactly the extraction and negative-odd implications needed in POSITIVE.md. At the fresh successful place and at its conjugate, signs and strictness of these valuations suffice for the residues 1 and 0/1. At the exceptional finite places and the real places the original preparation makes |u| large (in the indicated absolute value) and keeps every nonidentically-zero c bounded away from zero in its specified compact neighborhood. Then the balanced quantity is asymptotic to 1/u². Identically zero tests remain zero. Thus the same limiting local square classes, depths and real upper bound on the intrinsic input apply. The rest of the positive-factor preparation and the inherited height argument apply as before.

For the first four tests use c=R/L, followed when appropriate by K-conjugation. Here (L,R)=(x,1) for the two direct abscissas and (X,dx²) for the two homogeneous difference abscissas. For the final two tests take (L,R)=(1,C²). The conserved point guards already give Norm(L)≠0, as the verifier checks separately. The implemented squared quantity is

    R²/(L²+u² R²).

Every real conjugate of L²+u²R² is strictly positive. Its norm numerator may therefore be protected by positivity after rational descent. The atom guards for the u numerator, Norm(L) numerator, and all denominators of L,R,L²+u²R² and its norm are retained. These establish positivity first, then the six positive balancing denominators permit computing the arguments of the positive detector, then the trace and norm protections of POSITIVE.md apply. These three steps exclude circular nonvanishing assumptions. All other recorded source denominators are covered by this chain. They can vanish on an irrelevant nonrational character because the separator works in the whole polynomial algebra before chart decoding.

The native generation and receipt checker are

    python -B positive.py --balanced
    python -B check_positive.py --balanced

Use the same `--repo PATH` on both if needed. The `balanced/<route>` directories contain native graphs, elementary operator bounds and final determinant receipts. The checker exactly reconstructs the original c as R/L or its conjugate, all six squared quantities, all positive detector factors, their product and its norm, and the resulting intrinsic pole input. It checks all 164 denominator records per route. With rank 128 the nine-contact scalar guard degree is 2056, and the separator degree is 282962. The seven-contact bounds are 3048 and 437506, respectively. This gives 128(1+2056+282962)+1 and 128(1+3048+437506)+1 for the degrees in the opening paragraph.
