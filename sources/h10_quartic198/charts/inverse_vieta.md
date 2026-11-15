# Seven-field scalar chart: exact quadratic replacement

Fix a characteristic-zero field F, D in F nonzero, and a rational scalar R nonzero. The application has F=Q(sqrt(2)), D=11-6sqrt(2), and R>0. Write R2=R^2, an already retained rational coordinate. Use seven field coordinates U,V,W,M,r,P,r2 and the existing field outputs FU,FV. Impose

(1) UV=R2 P;
(2) PW=r;
(3) r(U+V+W+2M)+D R2=0;
(4) R2 P+W(U+V)=M^2;
(5) r2=r^2;
(6) FU r2=U^2;
(7) FV r2=V^2.

Every displayed equation is quadratic in stored rational coordinates after splitting the field components. Equation (3) gives r!=0 because D R2!=0. Equations (1),(2) then give U,V,W,P!=0. The variables r2,FU,FV are therefore uniquely specified, with

FU=(U/r)^2=1/x(U_point)^2,
FV=(V/r)^2=1/x(V_point)^2.

## Point recovery, including tangent cases

Define

U_point=(VW/R^2, (M+U)VW/R^3),
V_point=(UW/R^2, -(M+V)UW/R^3),
Q=(P, -(M+W)P/R).

These are finite curve points on E:y^2=x^3-Dx and Q=U_point-V_point. Indeed the abscissas VW/R^2,UW/R^2,P are nonzero roots, with multiplicity, of

x^3-(M/R)^2*x^2-(D+2Mr/R^2)*x-(r/R)^2.

Their sum follows from (1),(4), the sum of pairwise products follows from (1)--(3), and their product is (r/R)^2. The displayed ordinates place U_point,-V_point,-Q on the line y=(M/R)x+r/R. The cubic equation is precisely the result of substituting this line into E. Hence all points lie on E, and the chord/tangent law gives the group relation. Repeated roots give intersection multiplicities and require no division by differences.

Conversely, suppose Q=U_point-V_point and all three points are finite with nonzero abscissas. Their chord or tangent is not vertical, because Q is finite, and it does not have zero intercept, because otherwise one of its three intersections would be (0,0). Write the line as y=s*x+b, with b!=0. Let

U=R*b/x(U_point), V=R*b/x(V_point), W=R*b/x(Q),
M=R*s, r=R*b, P=x(Q), r2=r^2.

Vieta gives (1)--(7), including tangencies. This is the inverse construction and shows the chart covers the entire stated domain. No nonzero rational-component restriction and no new inverse witness are used.

## Ratios, with the source's R conventions

Let S=y(H)/x(H), TH=y(H-P_ref)/x(H-P_ref), both nonzero. Use the unscaled comparison label coordinates L,LP and retain the old scalar coordinate Z_stored, which is divided by R. Impose

L(M+U)=2 R S,
LP(M+V)=-2 R TH,
Z_stored(M+W)=-2 S.

These equations are quadratic. Their nonzero right sides show M+U,M+V,M+W are nonzero, so all three recovered points have nonzero ordinate and are not two-torsion. They imply

L=2 z(U_point)/z(H),
LP=2 z(V_point)/z(H-P_ref),
R*Z_stored=2 z(Q)/z(H),

where z=-x/y. Thus the scalar integer label is a=2*nu(Q), not nu(Q). Its nonzero status follows automatically from Q not being torsion and the inherited group description. The exact scalar valuation estimates at consumed odd primes are unchanged by the factor2. At the prepared prime2 and at real places the extra fixed factors must be included in the completeness estimates; they only change fixed constants, and the source's sufficient defining threshold is already ineffective.

## Height aggregate

P is the actual root abscissa x(Q), not a new reciprocal or weighted ordinate. Thus when the other three point blocks use recovered abscissas x1,x3,x4, take

T=7+(1/4)Tr(P+x1+x3+x4).

At either real embedding every finite point satisfies x>=-d, with d=3-sqrt(2) at one embedding and its conjugate at the other. Therefore the trace of four abscissas is at least -24, and T>=1. The aggregate equation is quadratic: P occurs linearly and each other xi is s_i^2+D(f_i+g_i).

Brox's weighted-trace theorem with all weights equal to1 applies directly to these four finite points, allowing arbitrary torsion translates and half-integral indices. Replacing the trace by its fixed translate7 affects the logarithmic height by at most a fixed constant. Consequently the maximum squared index is bounded by A*h(T)+J. No additional h(R) term, no new mixed-pole height theorem, and no additional conjecture are needed.

## Completeness

Choose the prepared scalar point from the old doubled subgroup Q=[a_old]P_ref, and define its new label a=2a_old. Taking a_old sufficiently divisible makes a divisible6 as needed by the affine fourth-label construction. The old scalar local preparation is retained with the harmless factor2 in its ratio. Its fixed real bounds and2-adic depth are adjusted by fixed constants before choosing the input-dependent primes.

The new root Q, the other three roots and T are fixed before comparison-prime selection. For the reference H=[h]P_ref choose U_point=[h]Q and V_point=[h-1]Q. Existing avoidance of h=0,1 ensures these three points are non-torsion, hence their abscissas and ordinates are nonzero. The chord intercept is then nonzero automatically, so the converse chart applies without an additional open-domain restriction. All ratio equations follow from their definitions.

## Count

The source scalar root block has seven field coordinates, plus one field ordinate carrier j_S:16 rational coordinates. The new chart uses seven field coordinates:14 rational coordinates. Existing FU,FV,L,LP,Z_stored slots are reused. The replacement therefore saves two rational coordinates. Combined with the independently compiled affine fourth-label reduction from204 to200, the expected count is198; the circuit producer and independent verifier must certify the final count and all changed rows before it is reported as an algebraic construction.
