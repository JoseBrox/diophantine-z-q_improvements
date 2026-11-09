# Quartic research checkpoint, 9 November 2026

## Proved local reduction; exact table construction in progress

At every unramified good odd place of E:y²=x³−Dx, the valuation of f=1/x is even, whenever f is defined; put f(O)=0. For v(x)≠0, the curve equation gives v(x) even (if v(x)<0, 2v(y)=3v(x); if v(x)>0, 2v(y)=v(x)). At v(x)=0 it is tautological.

Let q have odd valuation −nu. The old order-one factor term at position j≥1 was q^(2^j) f^(2^(j+1)). Replace it by q^(2^j) f^(2^j). Its valuation is 2^j(v(f)−nu), exactly 2^j times an odd integer. Thus the distinct-valuation argument, nonpositive valuation of every factor, and the cleared trace extraction continue to hold. The extraction inequality gives v(f)>(1−2^(−j−1))nu≥3/4; hence v(f)≥2. Completeness has v(f)≥2, so each new term is positive at its selected primary place, and the product is1 in the residue field. Real signs remain positive. Finite preparation only becomes easier, as positive powers of q still tend to zero.

The shared H test may be weakened from v(f(H))≥40 to v(f(H))≥20: the cross comparisons first transfer integrality, then every nonzero U_i has formal depth at least that of H, at least10. Consequently primary ratios have relative logarithm accuracy40, exactly sufficient for the unchanged order40 Lucas comparisons. This proof includes zero U_i and the enlarged half-integer H group index. The exclusions H∈E[2] or ±P+E[2] only need positive f(H) valuation and remain unchanged.

At position1 encode the H test by q^38 f(H)^2. Its valuation is2(v(f(H))−19nu), exactly2 times an odd integer. Cleared trace extraction gives v(f(H))>(19−1/4)nu; evenness implies v(f(H))≥20. The weight q^38 and the squared H value already exist in the current table.

Use four groups:
(C2,H,U1,V0), (C3,C1,U2,V2), (C4,I,U3,V3), (F,U4,V1,V4).
Within each group positions0,1,2,3 have distinct valuation classes. The first position is an ordinary order40 comparison test. The second position uses q38 times H², C1⁴ or I⁴, or q² U4². The third uses q4 times U_i⁴ or V1⁴. The fourth uses q8 times V_i⁸. All V powers already occur in the logarithm circuits. New shared powers consist of C1⁴,I⁴,U1⁴,U2⁴,U3⁴:10 rational coordinates. All seven current scalar weight gates are retained unchanged.

Exact anticipated counts: 297−16=281 total variables for2 detectors, 342−20=322 for3 detectors. These are circuit-count predictions pending complete table reconstruction and independent verification. Orders40 and10, scalar normalization, and every global height threshold are unchanged. Only the H depth is20; no contact-height amplification is needed.

## Narrow screening results

- `search_even_H20.py`, `assignment_even_H202.json`, `assignment_even_H203.json`: SciPy MILP optimization within seven levels of dyadic distinct-valuation factors with the listed available powers; solver objective42/58, gap0. This is not a global lower bound.
- `search_lower_H.py`, `assignment_lower_H{2,3}.json`: lowering only the H order without using even valuations does not improve these costs.
- `search_amplification.py`, `amplification_screening.json`: exploratory gate cost screening for repeated contacts. Counts are labelled estimates, not constructions; some denominator savings were not charged.

## Rejected candidate

The tempting factor1+q^(2m) C²+q f1²+q³ f2² has pairwise distinct *negative* term valuations, but C's even-weight term can have valuation0 and cancel the constant. Its factor can then have positive valuation and defeat the product/trace argument. No polynomial claim is based on that candidate.
