# Status update: affine version supersedes the rational normalizer

The latest proved result and guard audit are in `affine_pheidas_theorem.tex`.
The unnecessary rational normalizer below has been replaced by c=2±4b.
The discriminant-prime scope is p outside {2,3,7}, which includes 5; no claim
that all such primes can be chosen >7 is intended. The independent audit
identified c=114/13, D_2=5(2307/13)^2 as a counterexample to that stronger scope.
The one-coordinate y=0 curve is locally soluble also at the class c=1 mod3,
by lifting the simple root x=1 with z=3; no extra mod3 condition is needed.

# Fixed normalized Pheidas surface: research checkpoint

Date: 2026-11-16. This is independent research, not a claimed 21/9-variable construction.

## Candidate and proved elementary properties

For b in Q*, choose a = ±2b and put

    c(a) = ((a^3+1)(a^2+2))/(a^2+1)^2,
    f_i(X) = c(a)^2 X^4 + X + i,  i=1,2.

Consider c z^2 = f_1(x) f_2(y), with c z nonzero. The only free rational coordinates after finite-root encoding are x,y. The sign of a and the quadratic root z are finite choices. This eliminates the parameter t from the Pheidas block in Kozachinskiy–Pasten–Vidaux, arXiv:2611.17124v1, Section 4, but retains two free coordinates, as does the repository's existing pole block. It does not by itself improve any established variable bound.

### Pole soundness

If p is odd and e=v_p(b)<0 is odd, v_p(a)=e. The dominant terms in a^3+1, a^2+2, and (a^2+1)^2 have valuations 3e,2e,4e, so v_p(c)=e. Write e=-k with k positive odd. For v=v_p(x), if v <= (k-1)/2 then the unique lowest-valuation term of f_i(x) is c^2 x^4, with even valuation -2k+4v. If v >= (k+1)/2 then the constant term i is a p-adic unit and the other terms have positive valuation, so v_p(f_i(x))=0. Thus both quartic values have even valuation, and c z^2 has odd valuation, a contradiction. This applies to i=1,2 because p is odd. Hence existence excludes all negative odd valuations away from 2.

### Arithmetic of c for nonzero integer b

Choose a=2|b|, so a is a positive even integer. The denominator is a square, so every negative valuation of c is even. Also v_2(c)=1: a^3+1 and a^2+1 are odd and a^2+2 has valuation 1. The inequality

    2(a^3+1)(a^2+2) - (a^2+1)^2
      = a^3(2a^2-a+4)+3 > 0

shows c>1/2. Since a^2+1 is a 3-adic unit, c is 3-integral, and c modulo 3 is either 0 or 2.

### Uniform irreducibility and S4

For c>1/2 the minimum of c^2 X^4+X+i over R is i - (3/4)(4c^2)^(-1/3)>i-3/4>0. Thus neither quartic has a rational root.

At 2, v_2(c)=1. The Newton polygons of f_1 and f_2 both have a length-three segment from (1,0) to (4,2), of slope 2/3. This produces an irreducible cubic factor over Q_2. Consequently each global quartic is either irreducible or cubic times linear. The latter is excluded by positivity. Its Galois group is a transitive subgroup of S4 of order divisible by 3. The discriminant is c^4 D_i, with

    D_i = 256 i^3 c^2 - 27.

Both D_i are 2-adic units congruent to 5 modulo 8, hence nonsquares. Therefore both Galois groups are S4.

### Distinct odd discriminant primes

D_i is positive, v_2(D_i)=0, and D_i congruent to 5 modulo 8. If every valuation outside {2,3,7} were even, its positive rational square class would have to be 21. This is impossible at 3. If v_3(c)<=1 then v_3(D_i) is even (the possibilities are 2v_3(c), 0, or 2). If v_3(c)>=2 then v_3(D_i)=3 and D_i/27 is congruent to 2 modulo 3, while a number of square class 21 with valuation 3 has quotient by 27 congruent to 1 modulo 3. Thus some p_i outside {2,3,7} has v_{p_i}(D_i) odd. Such a prime cannot divide the numerator of c (D_i is then a unit), and cannot divide its denominator to an odd discriminant valuation (the valuation of D_i would be even). Therefore c is a unit at p_i and v_{p_i}(D_i)>0 is odd. Since D_2-8D_1=189, p_i does not divide D_j for j != i.

The valuations obtained are odd, not necessarily one. Harpaz–Skorobogatov Theorem A as stated cannot be invoked directly. Their general Theorem 2.3 requires odd geometric component-group order, and appears applicable after a separate audit using multiplicative reduction. The exact verification is below, still being checked.

## Local solubility

At real infinity c>0 and both f_i are positive, so there are real solutions with z nonzero.

If v_p(c)>0 (including p=2), solve f_2(y)=c p-adically, with x=0,z=1. Mod p this is y+2=0 and its y derivative is 1, so Hensel gives the solution.

At odd p with v_p(c)=0, reduce c modulo p. For p>=19, Weil's bound for a non-square quartic, or a direct genus-one argument when nonsingular, gives suitable values. A sharper argument uses y=0 and searches for a nonzero value of 2 c f_1(x) that is a square. If 2c is square, x=0 works. If 2c is nonsquare, a nonsquare value of f_1 suffices. For p>=11, a smooth f_1 cannot have only square or zero values: the resulting elliptic curve would have at least 2p-2 rational points, exceeding Hasse's upper bound p+1+2 sqrt(p). If f_1 is singular, it has one double root r=-4/3 and factors as c^2 (X-r)^2 (X^2+2rX+3r^2); the residual quadratic has nonzero discriminant and supplies nonsquare values away from r for p>=5. Direct finite calculations handle p=5,7. At p=3, c=2 gives x=y=0, while c=1 gives x=0,y=1. Thus local Kummer points with nonzero right side exist for all odd unit primes.

At odd p with v_p(c)=-2k<0, write c=p^(-2k) gamma with gamma a unit, choose x=p^k X and y=0. The squareclass condition modulo p becomes that 2 gamma (gamma^2 X^4+1) be a nonzero square. If 2 gamma is square, X=0 works. Otherwise gamma^2 X^4+1 takes a nonsquare value for p>=11 by the same Hasse argument (this quartic is smooth and has square leading coefficient); direct finite calculations handle p=3,5,7. The lifted right side divided by c has even valuation, so it is a square in Q_p.

These arguments seem to prove everywhere local solubility for every c arising from positive even a. A reproducible finite-field checker is being prepared. The optional restriction y=0 also appears everywhere locally soluble for our c, because c mod 3 is never 1 when it is a unit. However the one-coordinate genus-one curve need not satisfy the Hasse principle; finiteness of 2-primary Sha alone does not remove its possible 2-torsion obstruction. No one-coordinate converse is claimed.

## Audit of Harpaz–Skorobogatov general theorem (ongoing)

Use g_1=f_1 and g_2=c f_2, so the Kummer equation is Z^2=g_1(x)g_2(y), Z=cz. At p_i outside {2,3,7}, c is a unit, and the quartic discriminant has positive odd valuation. The binary-quartic invariant I is 12 c^2 i (scaled by c^2 for g_2), a unit at p_i. Hence the elliptic Jacobian has multiplicative reduction and geometric component-group order equal to the discriminant valuation, which is odd. The other Jacobian has good reduction at p_i. The 2-torsion fields have Galois group S3. Their quadratic subfields are the discriminant fields and are ramified at p_i, whereas the other 2-torsion field is unramified there, proving disjointness. The quartic has exactly one double root and two simple roots in the geometric residue field at p_i; a simple root lifts to the maximal unramified extension, so its corresponding H^1(Q,E[2]) class is unramified. The class is nonzero because the quartic has no rational root. These are the missing hypotheses of their Theorem 2.3. Need finish checking the Jacobian invariants and all twists in the cited theorem before marking the conditional converse proved.

## References checked in primary sources

* A. Kozachinskiy, H. Pasten, X. Vidaux, Why should Z be Diophantine in Q?, arXiv:2611.17124v1 (12 Nov 2026), Section 4 and Theorem 1.1. https://arxiv.org/html/2611.17124v1
* Y. Harpaz, A. N. Skorobogatov, Hasse principle for Kummer varieties, Algebra & Number Theory 10 (2016), 813–841; Theorem 2.3, conditions (a)–(g), and proof of Theorem A. Author PDF https://wwwf.imperial.ac.uk/~anskor/hsk.pdf ; published PDF https://msp.org/ant/2016/10-4/ant-v10-n4-p05-p.pdf

KPv's final theorem requires abc, Dickson's conjecture, and finiteness of the 2-primary Sha of all elliptic curves over Q. It provides no small-variable count. Its literal expansion has many independent point/contact blocks and does not establish 9 variables. The normalized block considered here only uses the Sha assumption for its prospective integer-input converse; it does not eliminate any hypotheses needed in KPv's wider integrality construction or in the repository's existing constructions.
