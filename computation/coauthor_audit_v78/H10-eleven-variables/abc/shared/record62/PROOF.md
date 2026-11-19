# An ordinary-abc quartic in 62 rational coordinates

Take a fixed odd integer B≥81. The file `quadrics.json` specifies 50 quadrics in 62 variables, including the distinguished input X; `polynomial.json` is their expanded integer sum of squares. Its 830 monomials, degree four, integer content one and exact height B²+4091 hold for every such B. For all sufficiently large B its rational input projection equals the integers under the arithmetic premises of Brox v65 at commit d3a8c223716a0fc0dbf5af4eb7998d640c21048d. The sufficient threshold is ineffective. The argument uses its ordinary rational abc, elliptic-group, simultaneous prime-selection, trace-height and simultaneous twist hypotheses.

## The four tests in a single field coordinate

Use the unchanged scaled pair and reference charts, scaled trace, gap, and eight-contact rational weight of v65. Write β=X and K=Q(√2). In the notation of that source set J=β² f(H) f(U), K'=β² f(H−R₀) f(V), C=s−S and I=t−T_H. A bar denotes quadratic conjugation. Write w_j for the source weights, q_j=1/w_j, c=q₀+q₁. Require c to be a unit. Use the field element

    W=1+c C⁴+c² J²−c³ bar(I)⁴−c⁴ bar(K')².

Define a single rational D by D Tr(W)=Nm(W−1). Its trace cannot vanish at a rational solution: a vanishing trace would imply Nm(W−1)=0 in K, giving W=1 and trace two. Set

    2τ_j=1+(c−q_j)²+q_j D²,       b_j=w_j τ_j².

Each b_j enters the original pole predicate e²+bp²=1, uv=e(1−b), u²−v²=bz². Its two retained squares and every zero-witness branch are included. The old first-conic equation of block 1 is stored after subtracting the first-conic equation of block 0; this elementary row operation preserves simultaneous vanishing.

## Soundness

At each prime consumed by argument j, outside the v65 exceptional set, v(q_j)=−μ with μ positive and odd. The source's native pole obstruction excludes a negative odd valuation of b_j. If τ_j≠0, v(b_j)=μ+2v(τ_j), so v(τ_j)>−μ/2. If τ_j=0, the same inequality holds with v(0)=+∞, regardless of whether the pole system admits that fiber. A negative valuation of 1+(c−q_j)² is even. The other finite summand q_jD² has odd valuation, so a negative minimum cannot cancel. It follows that v(D)>μ/4 and v(c−q_j)>−μ/4. In particular v(c)=−μ.

For X≠0, the finite pair and reference charts identify the four tests above. Both J and K' have even valuation at any unramified good slot because all finite valuations of reciprocal abscissas are even. In W the first three nonconstant terms have classes −μ, −2μ, −3μ modulo four. The fourth has class zero modulo four. Thus every *negative* minimum is unique. The fourth term may tie the constant at zero. This causes no difficulty because only a nonnegative valuation of W is required. If both slot values of W are strictly negative, say w₁,w₂, then v(Nm(W−1))=w₁+w₂ and v(Tr W)≥min(w₁,w₂). This gives v(D)≤max(w₁,w₂)<0, contradicting v(D)>μ/4. This reasoning includes an inert prime with coincident valuations. At one slot W has nonnegative valuation. If any term there had negative valuation, its minimum would be strictly negative and unique, contrary to v(W)≥0. Thus all four nonconstant terms have nonnegative valuation, and hence all four underlying raw tests have strictly positive valuation since the exponents of c are positive and v(c)=−μ. This is exactly the hypothesis needed by the inverse-parameter extraction lemma of v65. At each consumed prime X is integral and X(m−X) vanishes modulo p, where m is the integral label of U−V. The unchanged contact-height, mixed-power and trace-height proof in v65 bounds all nonintegral solutions uniformly in B; its strict absorption coefficient is 602/679.

The contact equations are R=t²−2t, (R+1)Z=R²−35R and (R+1)w=Z²+24Z. The midpoint t=1 gives R=−1 and the impossible equation 0=36. For t≠1 elimination gives w=∏(t−θ)/(t−1)⁶, where θ runs over {−5,−2,−1,0,2,3,4,7}. A root of the numerator gives w=0 and is excluded by w_j q_j=1. This also rules out every contact when a height estimate is invoked. X=0 is already an integer in the soundness implication.

## Integer witnesses

For nonzero integral X use the v65 ordered preparations, with the same difference A=[X]R₀, scaled trace and gap B+X⁸+Tr(a)². The gap is fixed before the prime selection and exceeds the contact diameter. At a selected simple contact of block j, q_j has valuation −1. For the other block, at that translated contact evaluate q=1/w at the fixed rational argument z=θ±gap. This is finite and rational by disjointness. Its value is understood using the rational expression (z−1)⁶/∏(z−θ'). Enlarge the permitted finite avoidance set before selection to include every numerator and denominator prime of 1+q(z)² and all poles or reductions where the stated evaluation would fail. The former is a nonzero positive rational number. Thus q_other is integral there and 1+q_other² is a unit. In particular v(c)=−1.

At the prepared successful slot both raw errors have valuation ≥3 and both reciprocal products have valuation ≥4 as in v65. The four new nonconstant summands are strictly positive, so W≡1 there. At the opposite slot H and U, and the corresponding conjugated predecessor and V, reduce to the signed reference and signed fixed root as in v65. The prime avoidance for their nonzero abscissas and for X makes both reciprocal products units there. Thus the terms involving J or K' have negative valuation and the negative minimum is unique. If its order is −k, Tr(W) has valuation −k and Nm(W−1) has valuation at least 1−k. Therefore D has valuation at least one (including D=0). The gate 2τ_j reduces to 1+q_other², a unit, and v(b_j)=1. This proves positivity of the odd valuations in the denominators test.

The selected integer-witness construction has w_j>0 and both w_j tend to positive infinity at the large real slope and grow in absolute value at the fixed local preparations. Thus c>0 as a rational number, and c tends to zero at the prepared places. The physical tests are bounded on the fixed neighborhoods. Hence W→1, Tr(W)→2, D→0 and τ_j→1/2. On a sufficiently large real preparation the actual b_j>1. At two the original square-class formula for w_j makes b_j a two-adic square with v₂(b_j)≤−4. Each squarefree numerator source prime is 1 modulo 4; every valuation away from the selected support is even. Multiplication by τ_j² preserves parity and v(b_j)=1 at the selected primes of block j. Hence the reduced denominator is a square. The separate original prepared-pole realization theorem applies to each b_j. The fixed avoidance depends only on the data chosen before selecting comparison primes.

For X=0 use the v65 zero fiber with H=2R₀, s=S, t=T_H, F=G=d=J=K'=0 and h=t²/(s−t), whose denominator is nonzero by the source identity Nm(S−T_H)=7199/328. It gives a fixed gap B+Tr(a)². In both slots and before every prime choice the actual tests are zero: W=1, D=0 and τ_j=(1+q_other²)/2. The same disjointness, finite exclusions and real and two-adic depth choices give prepared b_j=w_j(1+q_other²)²/4 satisfying the original pole lemma. This supplies the required rational zero of the new polynomial.

## Compilation and verification

Use coordinates S,T_H,v for the reference as in the separate rechart, with a=1+√2, k=4−2√2 and δ=−23+17√2. The equations v(v+T_H−S)+δ=0 and S T_H+k(T_H−S)+2kv+2δ=0 are equivalent to the v65 unit equations via u=(v−k−S)/a and w=(v−k+T_H)/a. For c nonzero, the field coordinates

    P,Q=C²±c bar(I)²,        U,V=J±c bar(K')

are invertible replacements of the two comparison-square coordinates and the two reciprocal products. Decoding them gives C²=(P+Q)/2, bar(I)²=(P−Q)/(2c), J=(U+V)/2 and bar(K')=(U−V)/(2c). The shared product is W=1+c P Q+c² U V. To remove the D² coordinate, each gate is stored as

    2 w_j τ_j = w_j(1+c²)−2c+q_j+D² .

This identity follows by multiplying the displayed gate by w_j and using q_j w_j=1. The pole equation is q_j b_j=τ_j². We store q₀ and take q₁=c−q₀ identically. The compilation substitutes each physical coordinate x_i=c^{a_i} y_i and divides each equation by its assigned power of c. Store c and c⁻¹ with the literal unit equation. All weights are integral and the input weight is zero. This is an invertible rational change on the intrinsic unit domain; the resulting rows all have ordinary degree at most two. The net count is 62 variables (61 existential witnesses).

Run `python verify.py` beside the JSON files. The standard-library checker reconstructs the physical field and pole system directly, reverses every Laurent transformation, verifies each identity up to a nonzero fixed rational row multiple, independently expands every square, and checks the exact support and coefficient-height range. The largest absolute coefficient independent of B is 1548. The five coefficients depending on B are B²+4091, 8B+1, 2B+1, 2B and −2B.


## A presentation of linear coefficient height

On the cofinal subfamily B=n⁴, scale the 62 coordinates by the respective integer powers of n recorded in `parameter-scaling.json` and divide each row by the recorded power of n. All changes are invertible and fix the input. The resulting expanded polynomial in `polynomial-n.json` has 830 monomials and exact height B+4091 for all odd n≥3. The largest absolute separated coefficients at powers zero through four of n are 4091, 16, 44, 4 and 1. The only mixed profile is B+4091. All remaining profiles consist of a single power of n. This proves the height formula and constant coordinate support in that range. The fixed coefficients have gcd one. The verifier checks this full second expansion as well.


Four additional invertible row replacements followed by positive integer weights produce `sparse-n.json`, a 757-monomial quartic in the same 62 variables. The B=n⁴ specialization has exact height B+758541 for odd n≥3 and content one. Its only mixed coefficient is the constant B+758541. Its largest separate coefficients at powers zero through four are 758541, 16, 44, 4 and 1. The operations and weights are specified in `sparsity.json` and checked by `verify.py`.
