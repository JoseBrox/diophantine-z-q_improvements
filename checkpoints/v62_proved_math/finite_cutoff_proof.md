# Replacing the legacy cutoff by eighteen primes

## Statement and scope

The arithmetic soundness consumers of the proposed 229-coordinate quartic can use the finite exceptional set

\[
\Gamma=\{2,3,5,7,11,13,17,37,41,2399,
47,67,109,179,257,439,2099,2029147\}.
\]

With the widened local proofs below, the inherited full-family height theorem H4.1 gives a soundness threshold **N>=19**. Completeness is unchanged if the original construction is retained with its large selected primes and all of its original local preparation; its quantitative scalar step only requires N>=3. This note does not certify the 229-coordinate row table or its completeness maps. It proves the replacement local lemmas and their height/threshold consumers, conditional on the already identified global point domains, scalar interpretation, local pole obstruction, H4.1, and affine Lucas lemma.

The source is upstream `manuscripts/quartic_v19.tex` at commit `498efba6fe75e9d28d6804f1391d7f70e4150afa`. The old cutoff 76176 was used to justify higher-order truncated logarithms in earlier constructions. The present detector uses the untruncated parameter z and only relative precision four, so that older statement is not cited outside its domain: the required replacement is proved here.

## Formal comparison at every required prime

On E:y^2=x^3-Dx, D=(3-sqrt2)^2, write z=-x/y. At any unramified odd place with D integral, the formal logarithm is

\[
\ell(z)=\sum_{k\ge0}\frac{(-1)^k\binom{2k}{k}D^k}{4k+1}z^{4k+1}.
\tag{1}
\]

For depth r=v(z)>=1, the first omitted term is -2Dz^5/5. Its valuation is at least 5r whenever p!=5. For every k>=2 and odd p,

\[
v_p(4k+1)\le4k-4,
\]

since 3^(4k-4)>=4k+1. Thus the k-th term has valuation at least

\[
(4k+1)r-v_p(4k+1)\ge5r.
\]

The valuations tend to infinity. Therefore, at every odd p!=5,

\[
v(\ell(Q))=v(z(Q)),\qquad \ell(Q)/z(Q)\in1+p^{4r}\mathcal O.
\tag{2}
\]

All consumed primes lie outside S={2,3,5,7,11,13,17,37,41,2399}; the field is unramified and the curve has good reduction there. No lower bound on the numerical size of p is needed. In particular, (2) gives the unit-ratio and absolute-congruence argument of the current detector after its first integrality step. One must still establish integrality of one full ratio from the integral indices, transfer it with the positive cross-test, and only then use relative precision four as an absolute congruence. Denominators 2 in half-indices are units at these primes. Multiplication by two kills every two-torsion term, so the argument covers the current half-generator and torsion domains. No high-order truncation G_J is being invoked.

## Widened scalar extraction

Let beta=51X^2+2504 and

\[
r_4=\beta(\beta-1)(\beta-2401)(32\beta+343),\qquad
R_s=149^{2N+1}r_4/(1+149^2r_4).
\]

The differences of the four roots 0,1,2401,-343/32 have prime support contained in {2,3,5,7}. At p outside S, a negative valuation of beta is 2v_p(X), hence even, so the infinity contact contributes nothing to M_S(beta). At a finite odd contact p!=149, exactly one of the four factors has positive odd valuation; 32 and 149 are units and the denominator of R_s is a unit. Thus v_p(R_s)=v_p(r_4)>0 is odd.

At 149, the residues of (theta-2504)/51 for those four roots are 59,97,109,108; all have 74th power -1 modulo149. If X is 149-integral, no finite contact occurs. If not, the infinity contact has even valuation. Therefore 149 does not divide M_S(beta). The normalizer still has its independently forced valuation 2N+1 or 2N-1.

The current scalar expression is

\[
W_s=Z_0^4/R_s^{10}+Z_1^2/R_s^5+F^2/R_s^4,
\qquad b_s=R_s(R_s+9792)W_s^2.
\]

Here F is the nonzero norm of the reciprocal abscissa of H, and the physical scalar ratio Z is the retained z-ratio, possibly multiplied by 2 in the half-generator chart. For every p outside S, 9792=2^6*3^2*17 is a unit, and reciprocal-abscissa valuations are even at each place because the curve has good reduction and D is a unit. Thus v_p(F) is even. The three summands of R_s^4 W_s have valuations in the disjoint classes

\[
2+4\mathbb Z,\qquad1+2\mathbb Z,\qquad4\mathbb Z.
\]

No cancellation is possible. The pole obstruction excludes negative odd valuation of b_s and gives

\[
v_p(Z_0)>19\nu/8,\quad v_p(Z_1)>9\nu/4,
\quad v_p(F)>7\nu/4,\qquad \nu=v_p(R_s)>0\text{ odd}.
\]

At a place where f(H) has positive valuation, H is formal. The ratio bounds make the scalar comparison point formal or close to (0,0); translation by that two-torsion point changes z only by sign and makes it formal. The integral multiplication identity killing two-torsion and the isometry (2) then give v_p(a)>9nu/4. Multiplication of the physical ratio by 2 causes no change in this valuation at odd p. Every prime of M_S(beta) therefore divides a to order at least three. At149 the same proof supplies its old stronger exponent L_N. Since149 is absent from the radical, the strengthened statement is

\[
\boxed{149^{L_N}M_S(\beta)^3\mid c=|a|,\qquad
L_N=\lfloor9(2N-1)/4\rfloor+1.}
\tag{3}
\]

The original forced149 exclusion of reference torsion and indices -1,0,1 is unchanged and must precede all ratio interpretations. The retained global scalar chart gives a!=0; widening the set of ordinary scalar primes does not alter that argument.

## Widened detector extraction

For t outside the ten contacts Theta2, let M_Gamma(t) be the squarefree product of primes outside Gamma with a positive odd contact valuation. Every denominator, every contact difference, and every difference 1-theta has support in Gamma. Consequently at p contributing to this radical, exactly one contact has odd positive depth nu, t-1 is a unit, and v_p(q)=-nu.

The detector's five factor valuation classes are unchanged. Outside Gamma, the curve is good, reciprocal-abscissa valuations are even, and the nonconstant summands in each factor have pairwise distinct classes. Every factor is nonzero of valuation at most zero. For W equal to their product, let ell=max_{v|p}v(W)<=0. The trace equation gives v_p(Tr(W^-1))>=-ell and the exact physical pole input is

\[
b=(408/409)^2R/\operatorname{Tr}(W^{-1})^2.
\]

Outside Gamma, v_p(408/409)<=0. At p=409 the valuation is -1, which strengthens the conclusion. In all cases

\[
v_p(b)\le\nu+2\ell,
\]

and this valuation is odd. The pole obstruction makes it positive, so ell>-nu/2. The existing rounding then gives cross/Lucas tests of order at least3, input test order at least1, and reciprocal tests of order at least2. Apply (2) with the required integrality-first argument. The current affine normalizations use only division by2, so at these odd primes the current integer consumers remain

\[
M_j^3\mid\Delta,\qquad M_j\mid J_{\rm num}
\]

whenever the corresponding integer is nonzero, separately for j=0,1,2. No multiplication of these three divisibilities or coprimality assertion is made.

## Reflected height with the finite set

Write

\[
J_*=\prod_{p\in\Gamma}p
=54852429049017820832107412529142530<2^{116}.
\]

For u_+=2+1/t, u_-=2+1/(2-t), set R_+=B_SM_S(u_+) and similarly R_-. Outside Gamma the two radicals are disjoint; their product is exactly M=M_Gamma(t). Each exceptional prime can occur at most twice in R_+R_-. Hence

\[
R_+R_-\le J_*^2M,\quad
E(R_+)E(R_-)\le E(J_*)^2E(M).
\]

Multiplying H4.1 for the two transformed arguments and using the arithmetic-geometric mean of their logarithms gives

\[
h(t)\le\log7+C M\sqrt{E(M)}(\log J_*+\tfrac12\log M),
\quad C=c_0C_NJ_*^2E(J_*)<2^{381}.
\tag{4}
\]

The bound also holds when h(t)<=log7. The exact rational inequality C<2^381 is certified directly.

An elementary split controls E(M) sharply without inserting any primorial in the height coefficient. The finite product over primes at most1000 outside Gamma is less than2. For every prime p>1000, log(1+1/p)<1/p and logp>6, hence

\[
\boxed{E(M)<2M^{1/6006}.}
\tag{5}
\]

For the input comparison alone a convenient weaker bound follows directly from E(R)<=1+logR, R_+R_-<2^232M, c0CN<2^149, and 1+116log2<83<4*22:

\[
\boxed{h(t)\le2^{386}M(22+\tfrac12\log M)^2.}
\tag{6}
\]

## Scalar height without a primorial

The H4.2 constant C2=c0CN B_S^2 E(B_S)logB_S is less than2^237. This inequality is also certified directly from the exact finite product and logB_S<41*7/10. Since logB_S>1, E(M)<=1+logM and (1+logM)^2<2M give

\[
h(\beta)<2^{238}M_S(\beta)^3
\le2^{238}149^{-L_N}c.
\tag{7}
\]

## The threshold N=19

The previously proved torsion sum-height bound and the actual affine trace equations give

\[
B^2<40\sum_{j=0}^2h(t_j)+2425.
\]

Using (4), (5), and M_j^3|Delta separately, if Delta is nonzero then

\[
B^2<121C\sqrt2\,|\Delta|^{1/3+1/36036}
\bigl(\log J_*+\log|\Delta|/6\bigr).
\]

The additive constants are absorbed because C>2665 and logJ_*>1. With |Delta|<=14B^4 and s=logB,

\[
e^{\frac23(1-1/6006)s}
<500\cdot2^{381}(82+2s/3).
\tag{8}
\]

Here logJ_*<116*7/10, log14<3, and
121 sqrt2 *14^(1/3+1/36036)<500.

At N=19, L_N=84, so s>=84log149. The quotient in (8) is increasing in s>=0. Using 5<log149<501/100, log2<7/10, log500<7 and log363<6, its logarithmic comparison at the endpoint gives

\[
\frac23(1-1/6006)84\log149
>280\frac{6005}{6006}>279.7,
\]

whereas

\[
\log500+381\log2+\log(82+56\log149)
<7+381(7/10)+6=279.7.
\]

This contradiction proves Delta=0 for every N>=19.

Equation (7) gives tau=h(beta)<c/2, since149>2^7 and L_N>=84. For a nonzero reduced numerator of n-beta, its bound |J_num|<=4Bexp(tau), together with (6), gives

\[
\log B<\frac{23}{22}\log(256036\cdot2^{386})+
\frac{12}{11}\tau<300+c.
\]

But c>=149^84>600 and logc>420, so the affine Lucas lower bound yields

\[
\log B\ge(c-6)\log(c-3)
>\frac{99}{100}419c>400c>300+c.
\]

Thus n=beta. If n=m1/2 is half-integral, 2beta is integral, and the reduced denominator v of X satisfies v^2|102. Squarefreeness of102 proves X is integral. All inequalities strengthen as N increases.

The exact script `certify_finite_cutoff.py` verifies the finite products, all contact support, four normalized nonsquare residues modulo149, and every numerical inequality above using only integer and rational arithmetic.
