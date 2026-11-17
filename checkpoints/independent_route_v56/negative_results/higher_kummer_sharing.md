# Higher Kummer products and a shared reference coordinate

## Scope

These statements audit the normalized Pheidas blocks. They do not rule out rational points for actual detector tuples, nor a different coupling of the source indices. They show why the general Harpaz–Skorobogatov Kummer theorem does not by itself lower the variable count, and why the most direct common-reference replacement loses pole soundness.

Write

    f_(c,i)(X)=c²X⁴+X+i.

The normalized block for input b uses c=2±4b and

    Z²=c f_(c,1)(x) f_(c,2)(y),  cZ≠0.

## 1. A common twist retains four free coordinates

For two inputs, take the four genus-one curves

    U_1²=f_(c1,1)(x1),  U_2²=c1 f_(c1,2)(y1),
    U_3²=f_(c2,1)(x2),  U_4²=c2 f_(c2,2)(y2).

A Kummer variety for their product is a four-dimensional quotient by simultaneous sign change. It can be described by three equations

    V_j²=g_1(t_1)g_j(t_j),  j=2,3,4.

The three V_j are finite quadratic roots; the four abscissas t_1,t_2,t_3,t_4 remain free rational coordinates. Even if all the hypotheses of H–S Theorem 2.3 are established, the conclusion gives a common quadratic twist, not an equality of abscissas. The retained pole-parameter budget is still four. In addition, the independent discriminant-prime and disjointness conditions must be checked across all four factors; the two separate pairwise checks do not automatically imply them.

## 2. Identifying a reference coordinate gives Kodaira dimension one

Let c1,c2 be nonzero rationals with c1²≠c2². The direct shared-y construction is

    Z_1²=c1 f_(c1,1)(x1) f_(c1,2)(y),
    Z_2²=c2 f_(c2,1)(x2) f_(c2,2)(y).

Its smooth projective model has Kodaira dimension 1, and therefore is not birational to a Kummer variety of an abelian threefold.

Here is an explicit calculation. On B=P¹_(x1)×P¹_(x2)×P¹_y, the two double-cover branch equations have multidegrees (4,0,4) and (0,4,4). Their y-branch divisors are disjoint: a common root would satisfy (c1²−c2²)y⁴=0 and hence y=0, where both quartics equal 2. The line bundles of the two double covers are L1=O(2,0,2) and L2=O(0,2,2). Adjunction gives

    ω_Y = π* O(0,0,2).

The only singularities are locally an A1 surface singularity times a smooth curve, arising where x_i and its own y-branch divisor meet. They have crepant resolutions. Since

    π_* O_Y = O ⊕ O(−2,0,−2) ⊕ O(0,−2,−2) ⊕ O(−2,−2,−4),

the plurigenus of a smooth crepant resolution is

    P_m = 2m+1  (m≥1).

Thus κ=1. The shared-x construction has the same calculation.

Equivalently, let C be the degree-four cover of P¹_y given by

    v_1²=f_(c1,2)(y),  v_2²=f_(c2,2)(y).

Its eight disjoint branch points give genus 5 by Riemann–Hurwitz:
2g−2=4(−2)+8·2=8. The shared-coordinate threefold is a V4 quotient of E1×E2×C, with generators changing the signs of (U_i,v_i) together. This makes the genus-five synchronization explicit.

The excluded case c1²=c2² has coincident branch divisors and a different geometry. It is not a general realization theorem for two actual pole inputs; in the positive-completeness branch it equates the two coefficients.

## 3. A common fixed reference loses pole soundness

Replacing the first factor by g0(x)=4x⁴+x+1 gives

    Z²=c g0(x) f_(c,2)(y), c=2+4b.

This admits

    b=7/67, c=162/67, x=2, y=0, Z=18,

despite v_67(b)=−1. The input is positive and 2-integral, and c>2.

Even restricting the relevant primes to the KPv tailored class does not repair this. Set

    p=4441, x=912, N=g0(x)=2767192327057, k=1663489,
    b=(k²−N)/(2N)=1663032/2767192327057,
    c=2k²/N=5534391306242/2767192327057,
    y=0, Z=2k=3326978.

Then p≡1 mod8, p≡3 mod7, (p+1)/2=2221 is prime, and v_p(b)=−1. All assertions are checked exactly in the companion certificate. This example concerns the tailored-prime class; p is below the current source's separate exceptional bound.

## 4. The reference from a valid first input also fails

The proposed three-factor Kummer system

    Z_1²=c1 f_(c1,1)(x) f_(c1,2)(y1),
    Z_2²=c2 f_(c1,1)(x) f_(c2,2)(y2)

has an explicit rational family accepting a bad second input while the first input has odd square denominator.

Choose t∈Q with t⁴≠2 and t≠2, and set

    u=(2−t)/(4(t⁴−2)), c1=2u², x=1/u, y1=tx,
    g=f_(c1,1)(x)=5+1/u.

Direct substitution gives f_(c1,2)(y1)=2g. Hence Z1=2ug solves the first equation. Write g=D s² with D a positive squarefree integer. When D is even and v_2(D)=1, choose a positive odd integer k coprime to D and set

    c2=4k²/D, y2=−2, Z2=8c2ks.

Then f_(c2,2)(−2)=16c2², so the second equation holds. At every odd prime p|D one has v_p(c2)=−1 and v_p(b2)=−1 for b2=(c2−2)/4.

One exact instance uses

    t=110/91,
    u=6782139/4630039,
    c1=91994818830642/21437261141521,
    b1=12280074136900/21437261141521,
    x=4630039/6782139,
    y1=509304290/617174649,
    Z1=77081468/4630039,
    g=38540734/6782139,
    D=3507206794=2·7·13·17·1133551,
    s=1/24843, k=41877,
    c2=3507366258/1753603397,
    b2=39866/1753603397,
    y2=−2,
    Z2=391674604763376/14521589730557.

Both inputs are positive and 2-integral, c1,c2>2, and b1 has odd square denominator. The second input has v_1133551(b2)=−1. The prime 1133551 is larger than 76176 and differs from each of 1875611,3828397,3982747, so it is outside the listed exceptional set of the 25-variable source. It also satisfies p≡7 mod8, so it splits in Q(sqrt(2)). The sign-character guards are nonzero. This is a counterexample to the shared-reference pole system, not a claimed actual detector tuple; additional actual-trace equations could exclude it and would require their own new soundness argument.

## 5. A rational common pole coefficient cannot work uniformly

There is no nonzero rational function H(U,V)∈Q(U,V) having the following property for every pair of nonzero rational inputs: at every sufficiently large odd prime p, if either v_p(U) or v_p(V) is negative odd, then v_p(H(U,V)) is negative odd.

Proof: avoid the finitely many primes dividing the nonzero coefficients of a numerator and denominator for H. Choose an open cone in the negative valuation quadrant on which both numerator and denominator have unique lowest-weight monomials. For integer valuation vectors (e1,e2) in this cone,

    v_p(H(p^e1,p^e2))=a e1+b e2

for fixed integers a,b. The cone contains arbitrarily large negative integer vectors in each parity class. The requested property on classes (odd,even), (even,odd), and (odd,odd) would force a odd, b odd, and a+b odd, respectively, a contradiction.

This obstruction concerns a single rational coefficient on the full independent input space. It does not apply automatically to the correlated actual detector tuples or to a ramified incidence cover.

## Remaining arithmetic target

A coordinate saving requires a rational realization theorem on the shared-coordinate threefold, or a different common-reference construction whose pole soundness survives the actual detector equations. H–S on a higher-dimensional Kummer product does not supply either claim. The established counts remain 25 and 13.

Primary source: Y. Harpaz and A. N. Skorobogatov, Hasse principle for Kummer varieties, Algebra & Number Theory 10 (2016), 813–841, Theorem 2.3. https://msp.org/ant/2016/10-4/ant-v10-n4-p05-p.pdf
