# Direct ambient-field contact detector: 54 and 69 coordinates

## Theorem

Let K be a number field. Assume ordinary abc over K and a positive-rank elliptic curve over Q with the same rank over K. Retain the elliptic chart/group, trace height, formal comparison, simultaneous prime-pattern, recurrence, and BB pole-realization inputs of the [v110 joint integer selector](../../../undecidability/abc_selective_pole_v110/README.md). Then Z^k in K^k has a single integer-coefficient defining polynomial in at most

    15k+39

total K-coordinates (including all k inputs), or **15k+33** if K has no quadratic subfield. Consequently Z inside K requires **54** coordinates (or 48 in the latter case), and O_K has a polynomial over O_K in **15d+39** coordinates for d=[K:Q] (or 15d+33 in the latter case). In particular for quadratic K the counts are **54** and **69**. All bounds are unrestricted-degree, with ineffective sufficient shifts.

The improvement over [selective rationality transfer](../selective_rationality_transfer_20261124/README.md) is that neither the input coordinates nor the slope is rationalized. Only the elliptic point charts are constrained to be rational. The contact, gate, pole and height arguments operate directly in K. This uses ordinary abc over K, rather than merely the weaker v81 fixed-divisor inequality and a separate rational abc premise. The formulation allows totally imaginary K. There is no claim of a new Z-over-Q or quartic count.

## 1. A uniform binary-power height lemma over number fields

Use the ordinary absolute logarithmic projective heights, with local weights normalized by [K:Q], so all product formulas and heights of rational constants have their usual normalization. Suppose abc over K in the form

    h(A:B:C) <= kappa N^(1)(A:B:C)+C_K(kappa),  A+B=C, ABC!=0,

for kappa>1, where N^(1) is the weighted sum of finite primes where the three valuations are not all equal. Let a,b,c in K, c=a^e+b^e!=0, and write

    H=h(a:b), E=h(1:a:b), alpha=e/kappa-3>0.

For a,b nonzero, at each place write L_v=log max(|a|_v,|b|_v). The local upper bound log|c|_v<=e L_v+log2_v, where log2_v is zero at finite places, gives

    E = H+sum_v weight_v max(0,-L_v)
      <= H+(h(c)+log2)/e.

Here sum_v weight_v L_v=H by definition, and sum of the negative parts of log|c|_v is h(c) by the product formula. This inequality uses no archimedean lower bound and remains valid when a^e and b^e nearly cancel at a complex place.

At finite primes with v(a)!=v(b), count each prime by at most |v(a)-v(b)|. The total normalized weight is at most 2H (height of a/b). At a prime with v(a)=v(b)=m, the radical is nonzero only if v(c)>em. For m<0 the prime weight is bounded by -m times its weight, and these contributions sum to at most E. For m>=0 it is bounded by the positive valuation of c, and these contributions sum to at most h(c). Consequently

    N^(1)(a^e:b^e:c) <= 2H+E+h(c).

Also h(a^e:b^e:c)>= e H. Combining with abc gives

    alpha H <= (1+1/e)h(c)+O(1),
    E <= ((1+1/kappa-2/e)/(e/kappa-3))h(c)+O(1).

The constants depend only on K,e,kappa, not a,b,c. If either a or b is zero, E=h(c)/e and the displayed bound holds too (for the parameters below its coefficient exceeds 1/e). For e=8 and kappa=101/100 the coefficient is **703/1988<1/2**. Thus every nonzero eighth-power sum bounds the heights of its two summands by half its own height plus a fixed constant. This proof covers arbitrary denominators, complex embeddings, cancellation and zero summands; only a zero output is excluded.

## 2. Modified source over K

Denote the fixed auxiliary quadratic field of v110 by L0=Q(sqrt(2)), not by K. Keep its exact point charts for A_i,H,U, with ordinary components of each h constrained to be rational and its finite ordinate components constrained to be rational as in the selective rationality theorem. Thus A_i=[m_i]P with nonzero integer m_i, and H,U belong to the same original rational-index group. Keep the original affine and point guards. All the arithmetic operations on auxiliary-field data are now performed in the rank-two K-algebra K[J]/(J^2-2), with the involution J->-J, field norm interpreted as product with the involute, and trace as sum. This algebra may split; invertibility is imposed by the same explicit norm guards. Its rational point-chart characters are exactly those of the original L0 charts.

Allow the input X_i and slope z to vary over K without any rationality guard. For each i choose a fixed shift c_i in {0,1} by a finite disjunction, put Y_i=X_i+c_i, and replace the sixth raw test by r-Y_i. Keep the other five tests. This is the direct input comparison of v22; there is no squaring of the integer target. The shift permits nonzero integer labels for all integer inputs, including zero. Define beta_i=Y_i^2+B and T_i=Tr_{L0/Q}x(A_i), which is a positive rational number on the guarded point chart. Build

    M_i=beta_i^8+T_i^8;
    parent(L,R)=L^8+R^8;
    M=M_0^8+B^8,

where M_0 is the root of the same paired tree as v110, with an unpaired node carried. Guard every eighth-power sum nonzero (including M), not its individual summands. Here B is a sufficiently large fixed positive odd integer. This extra final node is essential: it controls h(B) even in nonreal fields, where beta_i might cancel B. It needs no coordinate in unrestricted degree.

Put a=M^4 and use the v110 shifts S_i, G_i, G, x_-=a-z, x_+=a+z, F=G(x_-)G(x_+), F_a and u=-18kF/F_a, with all source guards. Add guards 2a+c+c'!=0 for the finitely many distinct sums of shifts from the contact lists. The shifts have no opposite pair (and each is nonzero), so the pair sums needed for derivative collision are nonzero integers. These guards are automatic on the rational integer completeness construction for large B, but are not presumed for arbitrary K-valued solutions. Keep the v110 selective gates w(L),D(C),V(C,L), the product W and the trace V0 in the rank-two algebra. Its pole equation is unchanged:

    e=28u/((1+u)^2 V0^2), d_0=7u,
    q^2=(1-e)(v^4-d_0^2)(s^4-d_0^2).

This uses the ordinary terminal variables v,s in K; q is finite. Keep every original denominator and nonzero guard, including e!=0. All displayed arithmetic expressions are literal rational functions in the ordinary coordinates and finite algebra generators.

## 3. Local extraction over K

Exclude the fixed finite set of primes over rational primes ramified in K or L0, the bad source primes, and the original contact exceptions, including 2,7. Write v_P for the integral valuation of a remaining prime P of K, with v_P(p)=1. The algebra K_P[J]/(J^2-2) is either a product of two copies of K_P or an unramified quadratic field. Work in its two embedding slots, using the integral valuations extending v_P (in the field case the valuations coincide).

At a positive odd nu=v_P(u), all parity comparisons of the v110 selective lemma apply verbatim in each slot; all valuations there are integers. The terminal product pole excludes negative odd valuations of e at P directly, by the universal local obstruction. The inequality v_P(V0)>=-max_slots v(W) holds for the trace in either the field or the split case. Hence the same successful-slot conclusion holds: for any i whose gate is active with nu=1 and v_P(G_i(x_side))=1, all six tests have positive valuation in that slot.

The original formal-comparison argument (v22, local implication) only needs the first five tests on the rational L0 point data. The slot is a completion extending the corresponding completion of L0, with no ramification. Therefore the first four formal depths and fifth congruence hold in that original completion. For indices H=[h]P,U=[j]P, the first four tests give the formal logarithmic ratios j/h and (j-m_i)/(h-1). The relative errors are of depth at least four, and one of h,h-1 is a unit; the fifth test transfers integrality to both ratios and makes them equal modulo p in the chosen slot. Subtracting their products by h and h-1 gives r congruent to m_i. The sixth test gives Y_i congruent to m_i in the extension slot. Since Y_i-m_i is in K, its valuation at P is positive. This last implication does not require Y_i or z to be rational. Inert auxiliary primes are covered by the same argument; if the formal conditions cannot occur there, there is no solution with an active gate there.

This is a local calculation for every solution of the guarded source, not merely one with rational parameters. In particular the contribution of a consumed prime of K is its normalized log norm, not the weight of a distinct rational prime.

## 4. Enough contacts over K and height soundness

Ordinary abc over K gives the standard fixed reduced-divisor truncated-height estimate on P^1 used in v81. For any fixed squarefree polynomial G_*(T) of degree D over K, outside its fixed bad primes and at arguments x not its roots, the positive zero counting weight is at most D h(x)+O(1), and its truncated weight is at least (D-2-epsilon)h(x)-O(1). Consequently the weight of exact simple primes is at least (D-4-2epsilon)h(x)-O(1) and the weight of primes with positive valuation >=2 is at most (2+epsilon)h(x)+O(1): the surplus of multiplicity over truncated multiplicity bounds the latter. This statement applies to the split contact polynomials and to the fixed squarefree product of 2T^4+c+c' over distinct nonzero pair sums. Squarefreeness of the latter holds because each factor has simple roots and distinct constants give disjoint roots. All constants depend on the fixed lists, field, and epsilon but not B. Enlarge the fixed exception set by the finitely many primes in Section 3; this changes only additive constants.

Run the entire simple-prime/derivative-collision proof of v110 over K, using these normalized weights and heights: choose x the larger-height of x_-,x_+, and y the other. Each i starts with (9-4-2epsilon)h(x)-O(1) simple-prime weight of G_i(x). At any such prime x is integral and exactly one factor of the full G(x) vanishes simply. If v_P(M)<0, y is nonintegral, and the first summand G'(x)G(y) of F_a has strictly smaller valuation than G(x)G'(y), giving v_P(u)=1. If v_P(M)>0, y reduces to -x, so the absence of opposite shifts gives a unit G(y) and the same conclusion. If M is a unit, discard primes of multiplicity >=2 in G(y), of weight at most (2+epsilon)h(y)+O(1). Where G(y) has a simple contact too, derivative cancellation modulo P^2 requires v_P(2M^4+c+c')>=2 for its two contact shifts. Discard this multiple-prime support, of weight at most (2+epsilon)h(M)+O(1), by the fixed squarefree pair-sum polynomial bound. The new guards exclude identically vanishing pair sums at M. Every remaining prime is active for i with v_P(u)=1.

With epsilon=1/100 their total normalized weight R_i satisfies exactly the earlier estimate

    R_i >= (3-3epsilon) max(h(x_-),h(x_+))
                    -(2+epsilon)h(M)-O(1)
        >= (393/100) h(M)-O(1),

since x_-+x_+=2M^4 and h(x_-+x_+)<=h(x_-)+h(x_+)+log2. These calculations work when M or z has arbitrary complex embeddings; only nonzero guarded factors and finite valuations enter.

From Section 1 and the nonzero tree guards, every h(beta_i),h(T_i),h(B) is at most h(M)/2+O(1), with constants independent of B and all witnesses (the number of levels is fixed, each contraction coefficient is less than one half, and the fixed tree depth gives a fixed total error). Therefore

    h(Y_i) = h(Y_i^2)/2
           <= (h(beta_i)+h(B)+log2)/2
           <= h(M)/2+O(1).

If Y_i differs from m_i, the positive valuation contribution of Y_i-m_i bounds R_i, since each active prime has positive valuation by Section 3. The product formula and the height inequality for a difference give

    R_i <= h(Y_i-m_i)
        <= h(Y_i)+log(1+|m_i|)+log2.

Consequently (393/100-1/2)h(M) <= log(1+|m_i|)+O(1). The original one-point rational trace height estimate m_i^2<=A h(T_i)+J gives a bound on |m_i| and then on h(M), uniformly in B. This contradicts h(B)<=h(M)/2+O(1) for sufficiently large fixed B. Thus every Y_i=m_i, so every X_i=m_i-c_i belongs to Z. Unlike an argument with Y_i=X_i^2+1, no square-root ambiguity remains in K, even when it contains quadratic subfields. No real-order restriction was placed on K-valued witnesses.

## 5. Integer completeness

For integer inputs choose each shift c_i in {0,1} so n_i=X_i+c_i!=0. Fix A_i=[n_i]P; beta_i=n_i^2+B>0, T_i>0, every tree node positive, and M>0. The new M is just a different fixed positive rational scale chosen BEFORE prime selection. The common-numerator theorem's two-index CRT and bounded-neighborhood proof uses arbitrary fixed nonzero integer labels (the exact residues are j=0 mod the first annihilators, j=n_i mod the opposite annihilator for label i). Neither their sign nor parity is required: the v22 direct-comparison source explicitly permits every nonzero integer index. The fixed chart avoidance for H,U excludes 0, the finitely many +/-n_i and +/-1 as appropriate; the independent real returns preserve the original finite neighborhoods.

For large B all 18k contact positions +/- (a+c) are distinct and all pair-sum guards hold because a=M^4>max |c|. Now apply the retained v110 supplier and choose the two common indices exactly as there, with these fixed positions and labels n_i. The same selective local lemma shows e has positive valuation one at the chosen primes; all inactive gates are harmless. At nonselected primes and fixed places the v110 asymptotic u~z^2/a and the same bounded-neighborhood argument apply. The new a is still a rational fourth power, so the dyadic squareclass/depth, the real interval and the 7-adic preparation are unchanged. Hence the actual rational e has square reduced denominator, 0<e<1, and class seven of sufficient 2-adic depth. The BB theorem gives the terminal pole witnesses. This proof uses no prime supplier over K; the entire completeness tuple is rational, and then considered in K.

Finally supply rationality witnesses for the rational point data by the torsion-supported selector. Every finite branch for shift choice is allowed in the final polynomial. All witnesses can be rational on integer input tuples.

## 6. Coordinate count and exact polynomial prescription

There are k input coordinates, 2(k+2) ordinary point-chart components, one contact parameter z, and two ordinary pole parameters v,s. Thus 3k+7 ordinary source coordinates. The rank-four arithmetic-prefix algebras for the points and their literal finite multiplication tables are those of v110. As in the selected-character transfer, choose a separating linear combination alpha of the finite point-prefix generators, impose its maximal Hankel rank by a finite choice of nonzero minor and rank-upper residuals, and constrain alpha and the 2(k+2) ordinary chart components to be rational. This gives r=2k+5 rationality targets, one already a finite algebra element. Their 2r+1 point abscissas and 4r ordinary pole parameters are provided by the torsion-supported joint rationality construction. Its ordinates and pole roots and the original source pole root are monic algebra generators. The full finite algebra is encoded with one common encoder variable using the selected-character determinant and norm conjunction over K. Additional guards include the nonzero tree sums, pair sums, rationality correction H for each target, and all literal source guards. Each rational-expression denominator is guarded at the selected character and roots of A/B are adjoined by Z^2=AB. The finite disjunction is the product over shifts, rank strata, separators and pole menus. Clearing rational denominators of the final coefficient recipe yields integer coefficients. This is a finite polynomial specification; expanding the finite operations bounds the degree in the fixed data, but no numerical bound independent of the ineffective H is asserted.

The count is (3k+7)+(6r+1)+1=**15k+39**. When K has no quadratic subfield, the rational-base prefix algebras have 2-extension splitting fields, as proved in the selective rationality theorem. Their K-valued characters are then rational once the ordinary point components are rational, so alpha and its test are unnecessary. With r=2k+4 the count is **15k+33**.

For O_K use k=d=[K:Q] and the standard integral-basis substitution of the first input by X-sum_{i=2}^d omega_i X_i; it preserves the total count and yields coefficients in O_K. The same rank and arithmetic assumptions are retained. Ordinary abc over K implies rational abc by restriction to rational triples and absorption of fixed ramification/discriminant contributions. No additional local/global point-realization premise arises from using K in the soundness proof.

## Attribution and limits

The function-field preprint of Pasten--Vidaux motivates this separation between universal valuation obstruction, ambient-field height and rational auxiliary point arithmetic; the underlying rationality descent is their earlier number-field preprint. The rational index comparison and selective pole construction are v22/v110 project work; the prepared rational pole theorem is Bhargava--Burungale. The signed ambient-field binary-power inequality, extra height anchor and direct K-valued input/slope transfer above are new deductions. The ordinary abc hypothesis over K is stronger than the fixed-divisor height premise alone used by the preceding transfer. No unconditional result for every number field, effective shift, rational variable saving, or quartic bound is asserted. 
