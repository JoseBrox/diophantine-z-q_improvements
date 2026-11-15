# Structural arithmetic routes examined

These are research notes, not additional defining-polynomial claims. Baseline: Brox 204, pinned d337a5500e2531139445bd7e30f966f62c4db03a. The affirmative affine fourth-label argument is in `affine_fourth_block.tex`.

## 1. Eliminate the input point using a shifted Pell coordinate

There is a useful algebraic mechanism, but its global forcing step is missing. For integer labels a,t,b put w=(a-2)b+beta and

    Delta_beta = t^2-a*t*w+w^2-1.

This expression is monic quadratic in beta, with integer coefficients. If Delta_beta=0 and beta is rational, beta is an integer. Thus its exact vanishing would remove the separate input-index point. Conversely, for integer beta and positive a, choose a Lucas index j congruent to beta modulo a-2. Since U_j(a) is congruent to j modulo a-2, b=(U_j-beta)/(a-2) is integral, and t=U_{j+1} solves Delta_beta=0. One can make j arbitrarily large.

The obstacle is quantitative, not the monicity or completeness. Delta_beta has reduced numerator of size at most a fixed polynomial in B times exp(2h(beta)). The current height/divisibility argument then gives only log B=O(h(beta)) when Delta_beta is nonzero. The exponential Lucas lower bound is obtained only after Delta_beta=0, so it cannot be invoked to force that first equality. No resolution of this circularity was found.

## 2. Prescribe the scalar index as a polynomial in the input

Taking a=149^(kN) r(beta)^m might make integrality of a imply semilocal integrality of X, potentially deleting the input point. It does not preserve the scalar completeness proof as presently stated. At varying primes p in the odd numerator support of the scalar pole input, the point [a]P must be formal. This requires that the reduction order of P modulo p divide a, in addition to p-adic divisibility of a. Powers of r(beta) supply powers of p but generally do not supply the unrelated prime divisors of ord(P mod p). The original proof chooses a in finite-index progressions incorporating those group orders and real recurrence. Fixing a as a polynomial removes that freedom. Fixed-real-neighborhood membership is another unresolved obstruction.

## 3. Remove one Lucas point by using monicity

The current Lucas residual is already monic in t. If the actual integer labels a and b were available as rational coordinates, a rational solution t would automatically be integral and a separate elliptic point for t would be unnecessary. The available coordinates L2,L4, however, are only formal-ratio approximations to a,b. Their values are not globally integral. Setting the Lucas polynomial exactly to zero in L2,L4 and a free rational t therefore does not apply the rational-root theorem. Nor is the height of the free rational t controlled by the fixed-root aggregate. Replacing a,b by new rational variables with local comparison equations recreates the same height problem.

## 4. One comparison block with the sum of the two weights

For q=q0+q1, an odd negative valuation of exactly one qj, with the other integral, is inherited by q. A single local-factor/pole block would then perform both sets of tests. At common contact primes, valuations can cancel or an even negative valuation can dominate. Those primes divide rational functions of the aggregate T. Simply bounding their product in terms of the ordinary height of T is too weak: it is exponential in h(T), which is the quantity the contact estimate is intended to control. No uniform height supplier for this merged rational function has been proved. Multiplying the two contact normalizers is worse: the reflected contact configuration can make the product a square and erase all odd valuation information.

## 5. Doubled formal parameters do not remove the branch guards

The tempting parameter w(Q)=z([2]Q)/2 is invariant under global two-torsion and has reciprocal-coordinate expression

    w = h(1+D f^2)/(1-6D f^2+D^2 f^4).

It still vanishes when [2]Q approaches (0,0), not only when [2]Q is formal at O. Thus its pullback adds four-torsion residue branches. The same sign ambiguity reappears after passing to logarithms. The soundness contact primes are arbitrary good primes; the selected Gaussian congruences are only a completeness choice and cannot exclude those branches in soundness. Iterating doubling does not solve this.

Functions 1/x and 1/y have positive valuation only in the formal neighborhood, but vanish to orders 2 and 3 rather than 1. Their ratios give powers of indices and introduce root/sign ambiguity or a changed Lucas equation. No valid reduction of the point-positivity guards follows from them alone.

## 6. Fixed polynomial elimination cannot preserve exponential growth

If one removes b by a fixed polynomial/rational substitution in a,t and obtains a nonzero polynomial equation in the sole growth index t with coefficients polynomial in a, the elementary root bound makes |t| polynomially bounded in |a|, apart from parameter values where the leading coefficient degenerates. Thus this mechanism cannot reproduce a uniform lower bound log|t| of order |a|log|a|. An additional discrete variable or a substantially different growth mechanism is needed. This is a limitation of that particular elimination strategy, not a lower bound for all Diophantine definitions.
