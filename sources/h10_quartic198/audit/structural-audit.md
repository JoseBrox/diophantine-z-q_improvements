# Baseline and structural audit

Source pinned at Brox commit d337a5500e2531139445bd7e30f966f62c4db03a. The 204-coordinate construction, not the user's earlier 206 figure, is the current baseline.

## Algebraic baseline

Imported the repository's independent checker without invoking its file-writing main. Both complete tables reconstruct: 204 coordinates, 186 quadratic residuals, 3046 ordinary quartic monomials. The balanced table has 3048 parameter-separated terms; the unbalanced table 3047. The 22 rational rescalings pass. The 33 bounded Gaussian-prime examples pass. This verifies these finite algebraic assertions only, not the retained arithmetic premises.

## Weighted trace application

Theorem 1.1 of Jerome von Buhren, JTNB 29 (2017), printed p.308, is applicable in the form used by Brox: the parameter variety may have dimension two, its graph closure need only be integral, the projective-normality hypothesis is explicitly satisfied, and the theorem has an additive constant uniform in the parameter for the fixed finite-rank group. The exceptional-translate exclusion uses positivity only in sums of rational squares within a conjugate block. Independence of the two conjugate generators excludes cross-block pole cancellation. No gap was found in this application in this review.

Primary statement checked at https://www.numdam.org/article/JTNB_2017__29_1_307_0.pdf, Theorem 1.1, and hypothesis (1.1). This is an application audit, not a complete audit of that published proof.

## Affine fourth index

For a recovered finite difference Q4 with index nu(Q4)=m/2, the affine label b=4nu(Q4)+1=2m+1 is automatically a nonzero integer. It includes finite torsion differences (m=0 gives b=1). Store the shifted ratio L4=4z(U4)/z(H)+1 and its alternate; the equations

h(L4-1)+4fS=0,
(1-DF)(L4-1)+4hS=0

are still quadratic. The comparison difference is unchanged by the common constant shift. With A=a+1 the Lucas expression becomes

t^2-(a+1)(a-1)tb+(a-1)^2b^2-1.

The existing two field product outputs can store (a-1)b and (a+1)t. For positive a divisible by 6, take j=a-1. Then j=A-2 is odd and not divisible by 3. The Lucas sequence U_j(A) satisfies U_j congruent j modulo A-2, and modulo 2 the recurrence has period 3. Therefore b=U_j(A)/(a-1) is an odd integer. Its associated root can be Q4=[(b-1)/2]R0. The scalar construction's freedom to require a divisible by 6 must be verified in the supplying statement before this is asserted as a completed construction.

A new aggregate with weights 1 on Q1,Q3,Q4 and R^2 on Q2 satisfies 4T>6R^2-18>0, since each arbitrary finite point has trace abscissa at least -6 and the retained nonzero doubled Q2 has trace abscissa greater than 6. The weighted-height theorem handles this assignment without change of hypotheses.

## Why one detector is not immediately obtained

Setting its argument equal to the root trace would supply the needed soundness height bound, but removes the free slope used in completeness. That slope is currently chosen after the roots, with every contact numerator forced into the required prime pattern. Restricting the slope to an elliptic trace, or to T0+u^2T1, is not an application of the retained fixed finite rational coefficient-list theorem.

Allowing positive rational square weights can make a free slope easier to represent, but the weighted-height bound then also contains the heights of those weights. Those cannot simply be discarded: a variable rational weight can absorb the trace height. The current soundness proof needs a bound on all such witnesses, not merely existence of a small-height representative.

Replacing the root aggregate by U/V coordinates breaks the established order of choices: those points depend on the reference index selected only after the comparison primes. The same prime premise cannot be applied circularly to their eventual trace.

## Detector packing observation

At an odd contact valuation, each present three-test factor is either a unit of residue 1 or has strictly negative valuation. The five-factor product makes valuation zero equivalent to all five factors being units. A sum of inverse factors does not have this property: one successful factor already gives a nonzero residue. A sum of the factors requires a separate noncancellation proof when several have equal negative valuation. No such replacement is certified here.

## Prescribing the scalar index to delete the input root

A more substantial proposal was to replace the target comparison L1-beta by L2-F_N(X), for a polynomial such as F_N(X)=149^(kN)r(beta)^3. The Pell/height argument would tolerate the fixed-degree height O(h(beta)+N), and the entire first root block might then disappear. However upstream uniform-existence.md P14 gives a concrete completeness obstruction: [a]P must be formal at every prime in the positive odd numerator support of R(R+9792). This requires its reduction order at each such prime to divide a. Large powers of that prime in a do not imply divisibility by its generally prime-to-p elliptic reduction order. The prescribed polynomial supplies the former, not the latter. The original construction deliberately chooses a in an arbitrary sufficiently divisible progression. No repair of this prescribed-index obstruction was obtained.

## Independent scalar Vieta review

The chart in ../charts/scalar_vieta.md has independently checked polynomial ideal identities in check_scalar_vieta.py. Its group-law interpretation includes repeated roots: the line intersects the cubic with multiplicity, so tangent cases obey the same equation U-V=Q. The ratio equations with nonzero right sides exclude zero ordinates of all three points. The product uvw=k^2 excludes zero reciprocal abscissas, and the k0 inverse guard excludes the collapsed k=0 component.

For each fixed scalar Q with x(Q) nonzero, the reciprocal line intercept k(U) is nonconstant. In a formal parameter z at O, as U approaches O and V=U-Q approaches -Q, the line intercept is asymptotic to a nonzero constant x(Q)/z. Therefore k(U) tends to zero, while k is not identically zero. On the product of the curve and its conjugate, k0=(k(U)+sigma(k)(U'))/2 is nonconstant and in particular not identically zero. The cyclic orbit generated by (R0,sigma(R0)) is Zariski dense by the same endomorphism independence used in the weighted-height proof. Mordell--Lang implies that a proper closed subset meets this cyclic group in a finite set: any positive-rank subgroup of the cyclic group has finite index and remains Zariski dense. Thus only finitely many reference indices violate k0 nonzero. They may be avoided after the finite congruences and real recurrence are imposed.

The suggested mixed aggregate involving w^2=1/x(Q)^2 has a fourth-order pole at the two-torsion point (0,0), with positive leading coefficient after translating the formal parameter. The highest-order pole cannot cancel with any ordinary abscissa's double pole. Within a conjugate block its coefficient is a common nonzero complex scalar times a positive sum of rational fourth powers; across the conjugate blocks a common pole would contradict generator independence. The existing family height theorem therefore gives the same type of index-height bound. Its additive constant remains ineffective.

Replacing the scalar physical quotient by twice that quotient does not alter any odd-prime valuation. At 2 its fourth-power and square summands gain valuations 4 and 2, so preparation that makes each summand sufficiently deep still applies. The real bounds grow by fixed factors and can be absorbed in a fixed sufficient threshold. Exact global circuit compatibility and its count are not certified by these observations.

## Final 198-coordinate construction

The inverse Vieta chart supersedes the six-field chart with a component guard. It uses seven field coordinates U,V,W,M,r,P,r2 and reuses the square and ratio outputs. Equations force r nonzero from r(U+V+W+2M)+DR^2=0; all three recovered abscissas are then nonzero. Its two ratio equations and scalar ratio equation exclude zero ordinates once the retained scalar reference exclusion is applied. The converse is valid for every finite nontorsion triple with nonzero difference, including tangencies: its chord intercept cannot vanish because that would place (0,0) among its intersections. Thus no Mordell--Lang finite-avoidance argument or component guard is needed in the final construction.

The native coordinate P equals x(Q2). The aggregate is 7+Tr(x(Q1)+P+x(Q3)+x(Q4))/4, which is at least 1. The existing weighted-height theorem with all weights 1 applies directly. This also removes the h(R) error term from the transfer bound.

The arithmetic proof in ../arithmetic/inverse_vieta_198.tex was read independently. The scalar integer label is a=2nu(Q2), and the new physical scalar quotient is Z=2z(Q2)/z(H). Its full logarithmic ratio is a/h, up to the harmless sign from translating by (0,0) when needed. Every consumed scalar prime is odd, so the factor two preserves all valuation exponents. At 2 and at real places the preparation proof explicitly handles the fixed factor. Completeness chooses an old scalar label a0 divisible by 3, sets a=2a0, and keeps Q2=[a0]P0. The affine fourth label and Lucas parameter then use a in 6Z. All roots and the aggregate are fixed before comparison-prime selection. No new arithmetic conjecture is introduced.

It is essential that R is shown nonzero in the final rescaled system before the Laurent coordinate changes are inverted. Its literal rows give

R*x106=(51X^2+103)(51X^2+2503)(51X^2+2504)(1632X^2+80471)>0

and 1+22201R*x106-A*x106=0. Therefore R is nonzero and then R=A*r_beta/(1+22201*r_beta)>0. This closes the possible new R=0 stratum.

The independent third implementation check_inverse198_third.py authenticates all 184 rows, including direct reconstruction of the final scaled chart, all retained Laurent substitutions, the aggregate, and all expanded coefficients. It finds 198 variables, 2945 ordinary monomials, exact degree 4 and content 1. The unbalanced height is max((5898050446009651968*31581660^28)^2,149^(4N+2)), with coefficient crossover N=53.

The separate check_inverse198_balanced.py authenticates the balanced rows and complete expansion. It finds 2945 ordinary monomials and 2959 parameter-separated terms, with exact height max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N)). The coefficient crossover remains 57. Two mixed coefficient profiles have opposite signs, but their constant term is even and their C^2 coefficient is 289; since C=149^N is odd, neither can vanish. Other mixed profiles have same-sign coefficients. These are coefficient thresholds, not defining thresholds.

The final arithmetic claim remains conditional on precisely the inherited premises and retains an ineffective sufficient defining N0. This review does not claim a complete independent audit of those premises. The improvement from the user's 206 figure to 198 is eight coordinates; from the pinned current 204 baseline it is six. This does not constitute a large-margin improvement.
