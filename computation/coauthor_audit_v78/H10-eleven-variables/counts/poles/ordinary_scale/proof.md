# Nine contacts at the square scale under ordinary rational abc

The scale change here is independent of the fixed weak-abc constructions. The assumptions for this family are those of the repository's ordinary-abc eleven-variable v75 row, including its intrinsic pole input. Retain the nine shifts and the balancing and determinant construction of fewvars/BALANCED.md. In the notation of v63 replace a=M⁴ by a=M² everywhere, in particular t=M⁴−z², where M=(X²+B)⁴+T⁴. The table in ordinary-abc v63 cited the derivative estimate in terms of h(t). Its proof supplies the stronger intermediate inequality

    log r⁺(u) ≥ (k−6−3ε) max(h(a−z),h(a+z)) − (2+ε) h(M) − O(1)

for any fixed positive integer m in a=M^m. The constants depend on m and the shifts. This follows immediately before the final line of the proof of Theorem thm:derivative-height. No signed mixed-power estimate is used here. Since the two moving slots sum to 2M², their maximum height is at least h(M)−O(1). With k=9 and ε=1/100 this yields

    log r⁺(u) ≥ (1−4ε) h(M) − O(1) = (24/25) h(M) − O(1).

The original v63 binary-power bound h(M)≥(997/1001)E_h−O(1) uses only β,T, before the moving slots. The product (24/25)(997/1001)=23928/25025 exceeds 1/2. Thus the original local bound log r⁺(u)≤E_h/2+log(1+|n|) and the original trace-height estimate give a uniform contradiction whenever X≠n and B is sufficiently large. The proof references are pinned to JoseBrox/diophantine-z-q_improvements at d3a8c223716a0fc0dbf5af4eb7998d640c21048d, papers/conditional_few_variables/derivative_detector11_20261117_v63.tex.

For completeness a is a positive rational square; a≥(B⁴)²>10. The nine pairs of slope contacts are distinct. The fixed-place asymptotics u∼z²/a, w∼a/z², together with the original prime preparation, therefore give the same square classes, strict positive local depths and real bounds as v63. The derivative proof with m=2 excludes the same exceptional coincidences with a fixed set and temporary finite set in their original order. The curve roles, balancing, local tests, three charts and native intrinsic pole remain those in the balanced ordinary construction.

The defining polynomial has eleven variables including X, degree at most 18,565,505 and support strictly less than 2^227. The guard degree is 1176, the separator operator degree is 143866, and the rank is 128. The coefficient one-norm of the B=3 fixture is at most 2^71153664; its ability to define the integers at that specific shift is unknown. The degree and support bounds are uniform in B. The recipes in fewvars/POSITIVE.md and BALANCED.md describe the determinant represented in output/abc11/certificate.json.

Run 'python -B build.py' and 'python -B check.py' in this directory. The scripts use the sibling fewvars code and pinned upstream checkout or accept explicit --fewvars and --repo paths. The checker changes the two folded exponents M⁴ and M⁸ to M² and M⁴ in the upstream native graph before reconciling it with the delivered circuit. It verifies all six modified detector factors, 164 denominators, 13 removed atoms and 25 retained norms and the degree bound.
