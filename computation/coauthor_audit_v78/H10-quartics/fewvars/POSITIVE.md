# Positive detector products and independent pole signs

These proposed bounds use the arithmetic hypotheses and parameter sufficient thresholds of JoseBrox/diophantine-z-q_improvements at commit `d3a8c22`. All variable counts include the input. For the 25-variable row use v75, for the 27- and both 13-variable rows use v40, and for the 11-variable rows use v75. The cut in the 25- and 27-variable rows comes mainly from avoiding a separate high-rank norm of each detector's trace numerator.

| Source | Variables | Upstream degree bound | New degree bound | Improvement | Support bound |
|---|---:|---:|---:|---:|---:|
| General | 25 | 4,863,007,848,923,136 | 495,506,685,952 | 9,814.21× | < 2^874 |
| Explicit L=20483 | 27 | 99,279,020,543,180,800 | 1,941,079,851,008 | 51,146.28× | < 2^994 |
| Weak abc, exponent 121/100 | 13 | 43,211,777 | 3,998,209 | 10.81× | < 2^243 |
| Weak abc, exponent 16/15 | 13 | 39,858,177 | 3,066,369 | 13.00× | < 2^238 |
| Ordinary abc | 11 | 230,932,097 | 44,938,625 | 5.14× | < 2^240 |
| Ordinary abc, seven contacts | 11 | 356,146,817 | 69,270,913 | 5.14× | < 2^246 |

For the certified 27-variable member the coefficient l1 norm is at most 2^16,427,189,809,446,912 and its height is strictly below 2^(2^54). The other height bounds in the receipts concern their numerical fixtures. Their degree and support bounds concern the defining families. Suppressing a finite field or real norm guard is justified below only after a rational source character has been obtained.

## Positive factors

Every detector of these six routes computes W in the fixed real quadratic field K=Q(√2). Write the original W as a product of factors 1+a_i, including the scalar factors when present. Replace it by

    W+ = product_i (1 + a_i²).

Keep *all* original raw a_i, including their q and delta powers, unchanged. The detector input becomes the same source scalar divided by Tr(1/W+)². All arguments, scales, contacts, balancing functions and pole families are unchanged. At a rational point-algebra character the two real values of each new factor are ≥1. W+ has positive real values in both embeddings. Writing W+=U+V√2, both U and Norm(W+) are consequently positive. This supplies their nonvanishing directly on every rational source character with the protected denominators. It also handles zero raw tests.

**Valuation extraction.** At the good places where the upstream extraction lemma consumes a pole test, the source proves that each nonzero a_i has nonzero valuation: its valuation is odd. In v75's unsquared reciprocal tests this uses the even valuation of a nonzero reciprocal abscissa; the balanced 11-variable tests have an actual final numerator squared. In the two 13-variable rows the detector consumes positive odd v(R), with a normalizer that is a unit. Hence, allowing infinity for a_i=0,

    v(1+a_i²) = 2 min(0,v(a_i)).

In particular every factor has nonpositive valuation. If the source coefficient has odd valuation α, the pole obstruction and the integral local trace give 0<v(b)≤α+2q, where q is the largest v(W+) among places above the source prime. Thus α>0 and at a place attaining q each min(0,v(a_i)) is >−α/4. This implies the original >−α/2 requirement, including all raw comparisons, normalized scalar tests and all requested contact orders. On the ordinary-abc row this calculation is used only at positive odd v(u), where v(w)=v(u); at negative odd v(u) the old balancing lemma already makes every a_i have positive valuation. All height bounds, radical-divisibility implications, and constants determining the sufficient parameter are downstream of the unchanged local conclusions. No new global height estimate is required.

**Preparation.** At each fresh selected prime the old successful conjugate place makes every a_i zero modulo the place. There W+≡1. At the other place v(a_i) is positive or negative (or a_i=0), and the reciprocal of a new factor is respectively 1 or 0 modulo the place. Therefore Tr(1/W+) is still 1 or 2 modulo a fresh prime. The parity and positive signs of valuations in the reduced pole input are preserved. At places where the detector coefficient has even valuation, a nonzero square trace in the denominator leaves that parity even. The source's fixed finite-place preparation makes the raw a_i as small as needed, and squaring preserves and improves this. For the 11-variable negative-odd branch one uses W+≡1 at both places as above. At 2,3,17 for native zero-poles, and at 2,7 for the intrinsic pole, the pole input has the same limiting square class and valuation as required. More explicitly, the nonzero trace ratio between the positive and old detector changes the pole input by a rational square, and at fixed places the trace can be kept arbitrarily close to the old nonzero limiting value. The real preparation on the actual character makes the raw a_i arbitrarily small by the same scalar-point and slope choices. Thus W+ is as close to 1 and its trace reciprocal as close to 2 as required; this gives 0<b<17 for the native poles, or 0<7b<1 for the intrinsic pole. In the 13-variable rows the real asymptotic for b keeps its original leading term because W+→1. In the 25- and 27-variable rows the small scalar contributions can be fixed before choosing the prime pattern. The whole-character denominator preparation for unrelated conditions is retained: input test denominators are as before. On every prepared point character both embeddings are real, so the new product/trace are positive. Source density of admissible pole pairs permits avoiding finitely many vanishing conic denominators and extractions just as before, for these newly prepared actual pole inputs and nonzero conjugate parameters. This gives a prepared point for each required integer. The nonzero-ordinate relaxation is one-way on arbitrary base tuples, sufficient in the other direction on prepared tuples.

The local results used here are the source v19 general25 Trace Lemma and pole preparation, v22 conditional13 Local Lemma and preparation, and v63/74/75 intrinsic detector extraction and preparation. The 27-variable detector uses the same combined-pole calculation as the general row, on each of its three arguments.

## Exactly which guards can be removed

The new circuit records the two components of each raw a_i as rational polynomial pairs, each final W+, and Norm(W+). Let R be the set of all distinct nonconstant multiplicative atoms in the native nonzero guards after omitting the isolated pole ordinates. Let D be the union of the atoms in all denominators for these recorded raw a_i, W+, Norm(W+). Let H be the union of the atoms in the numerators of U and Norm(W+) across all detector products. Use the upstream norm product G on exactly

    R \ (H \ D).

All integer factors discarded are nonzero. On G≠0 every atom in D is a unit: the checker verifies D is contained in the retained set, even though this inclusion need not hold for a generic compiler. The guard supplies the protected fractional coordinates on every character. After extracting a rational character, exact rational-function identities in the point algebra identify the supplied W+ with the product 1+a_i² and its norm with the product of the individual norms. With protected denominators these are ordinary equalities in K. Therefore every factor of each U and Norm(W+) numerator is nonzero. Every suppressed atom in H\D is now nonzero at the selected character. This simultaneously certifies every earlier nonzero guard and all chart denominators, except for the isolated pole ordinates which genuinely may vanish. In particular this does not assume trace positivity on a complex character. There is no circular use of a removed denominator in establishing positivity. The denominator set D was checked first.

All reduced pole roots lie over the point algebra. Their full and reduced equations satisfy Z_j=S_j q_j as in PROOF.md. The reduced equations define an integral free algebra even at a singular specialization. The separator and determinant construction, including distinct-value descent and the treatment of zero pole ordinates, are given in PROOF.md. The valuation proof there applies to independent sign choices over a common point character, and the bounded point-prefix argument handles different point characters. Powers of 2 have distinct valuations modulo 3 at every prime over 2 in the common Galois 2-extension. This remains true when there are three pole signs.

## Degree calculation

The degree is N(1+g+w), plus one for the conditional input factor, where N is the algebra rank, g the retained scalar guard's degree bound, and w the multiplication-operator degree bound of the denominator-cleared separator. Powers of fixed L or B influence coefficients only. For general25 the occurrences of L in circuit weights come only through the positive fixed constants 76249^L and 76249^((L+1)/2). With all admissible L≥3, both exponents already produce the same nontrivial constant-power nodes, and distinct exponent values cannot affect nonconstant degrees or the sign-label subspaces. The B-dependent rows use a degree-zero parameter node. The polynomial degree and support bound are uniform. For the explicitly selected L=20483 member, all coefficient-size propagation uses this actual integer.

| Route | N | g | w | Retained norm atoms | Positivity-certified atoms |
|---|---:|---:|---:|---:|---:|
| General25 | 1,048,576 | 20,877 | 451,674 | 80 | 46 |
| Explicit27 | 2,097,152 | 75,072 | 850,506 | 99 | 69 |
| Weak13 | 256 | 551 | 15,066 | 28 | 14 |
| Strong13 | 256 | 499 | 11,478 | 28 | 14 |
| Ordinary11 | 128 | 68,120 | 282,962 | 31 | 7 |
| Ordinary11 seven contacts | 128 | 103,672 | 437,506 | 29 | 7 |

## Reproduction

Run with Python 3.10+ and the upstream SymPy dependency. In this directory use these commands. Supply the same `--repo PATH` to both if the upstream checkout is not at ../source.

    python -B positive.py --termwise
    python -B check_positive.py

For a different general25 family member use, for example, `python -B positive.py --termwise --route general25 --parameter 7 --output /tmp/general7`. The default verification compares with the upstream stored numerical members.

The producer gives an integral polynomial by its named source graph, retained norms, explicit separating element and determinant. Each `positive_factors/<route>/` directory contains the native circuit, upstream elementary operator bounds, and the receipt specifying the new determinant. In these directories `parent.json` gives the upstream finite-algebra compiler's intermediate result on the **new** native circuit. Its old separator and old scalar guard are superseded by the formula and atom list in `certificate.json` plus PROOF.md.

The verifier reconstructs all 146 detector factors by exact integer circuit node arithmetic. It derives the unchanged raw tests and detector weights from the pinned source, regenerates each positive factor and both field coordinates of their product, and recomputes the final norm as a product of the norms of the individual factors. It also checks the resulting pole input exactly. It checks every listed raw denominator separately for whole-algebra nonvanishing, and all 1,377 chart/event denominator records for the combined protection/rational positivity argument. It checks the degree by the expanded separator formula. It also recalculates elementary operator weights, logarithmic norms, every guard subspace dimension and stability under coefficient conjugation, all pole square-extraction identities, and all root envelopes from the new native graph using the upstream independent verification algorithm with the applicable v28 or v75 chart table. The algebraic checks verify this construction relative to those upstream inputs; the external Diophantine hypotheses and defining assertions have not been independently proved by computer.
