# Harmonic three-contact scalar: 162 and 177 coordinates

**25 November 2026.** The defining-quartic families are reduced from 163 to
162 and from 178 to 177 rational coordinates (input included), without
changing the comparison target, elliptic charts or native BB poles.
The first family has an ineffective sufficient integer N; the second
uses the completely specified constant C=211^(2^1600). The latter is an
exact succinct coefficient specification, **not** a materialized decimal
coefficient table and not a coefficient-height improvement.

The arithmetic statements retain the full-domain scalar modular height
input H4.1 of [v68](../../papers/quartic/quartic229_compact_20261117_v68.tex),
the group, point-chart, formal-logarithm, comparison, Lucas, weighted-sum
and ordered prime-supplier premises of
[v82](../../papers/quartic/scalar_point163_179_20261120_v82.tex), and the
[BB-native substitution](../bb_native_quartic_20261124/README.md).
The specified route uses the effective weighted-sum estimate of
[178](../weighted_explicit178_20261124/README.md). In particular neither
route adds an ordinary rational abc hypothesis. This does not independently
establish the inherited arithmetic premises.

## 1. A scalar with three necessary contacts

Keep beta=51X^2+2504 and the original input residual beta-n. Set

\[
 k=2^{20},\quad s=kX^2,\quad u=s/(1+s),\quad
 A=(2401+2400s)(343+375s),\quad B=1+s,
\]
\[
 C=211^N,\qquad K_N=3\cdot2^{15}\cdot211 C^2,\qquad
 R=K_N AB/(A+B).
\]

For every rational X, A,B>=1, so R>=K_N/2>100. For soundness X=0
already belongs to Z; assume X is nonzero, so 0<u<1 and H4.1 is
applicable. The original five homogeneous contacts for u are at
infinity, 0, 1, 2401 and -343/32. In the reduced representation
s=r/q, where r,q>0, the corresponding integer factors, up to sign,
are q+r, r, q, 2401q+2400r, 343q+375r.
Outside the original exceptional set
S={2,3,5,7,11,13,17,37,41,2399}, the valuations of r and q
are even (k is a square). If v_p(s) is nonzero, no odd contact
occurs: the other three homogeneous factors are units. If v_p(s)=0,
the only possible odd contacts occur on B or one of the factors of A.
These three linear factors have disjoint root sets modulo p: the first
factor minus 2400B is 1, the second minus 375B is -32, and the
cross determinant is 77175=3^2*5^2*7^3. At any such contact exactly one
of A,B has positive odd valuation and the other is a unit, making A+B
a unit. Thus at p outside S and 211, every odd contact yields positive
odd v_p(R).

At 211, all three factors and A+B are nonzero for every residue
s=kx^2 (211 cases, verified by check.py). For v_211(X)<0, write
d=-v_211(X); the leading terms give v(A)=-4d,
v(B)=-2d and v(A+B)=-4d. Consequently for all rational X,
with d=max(0,-v_211(X)),

\[
 v_{211}(R)=2N+1-2d.
\]

In fact 211 never contributes to the odd contact radical of u:
the integral-input residues just checked have no contact, except the
even valuation at 0; the nonintegral-input case has only the even
contact at 1. It is also sufficient to use the weaker bound below
that allows 211 as an additional exceptional prime.

## 2. Recovering the growth index before using its height

Let M=M_(S union {211})(u) be the product of primes with positive
odd valuation on at least one of the five reduced contact factors.
The full-domain H4.1 estimate in v68 gives

\[
 h(u)<2^{237} M_S(u)^2(1+\log M_S(u))^2
       <2^{262}M^{5/2}.
\tag{1}
\]

For the second inequality use M_S<=211 M, 211^2<2^16,
1+log 211<7, and (1+log M)^2<4 sqrt(M), the latter following by
maximizing (1+t)^2 exp(-t/2) on t>=0. All constants are independent of N.
One can even omit the 211 factor by the previous observation.

For sufficiently large N there is necessarily at least one prime of
positive odd valuation on R outside S. Indeed:
* If d<N/2 then the anchor prime 211 has odd depth >N+1.
* If d>=N/2 then v_211(1-u)=2d, hence h(u)>=2d log211>=N log211
  (write u as a reduced fraction strictly between zero and one).
  By (1), for N log211>=2^262 we have M>1.

Apply the v82 scalar lemma at any such prime **before** recovering the
scalar point. Its physical equations are unchanged:
\[
 J=Z^2/R^5+f^2/R^4,\qquad
 \tau\operatorname{Tr}(Z^2/R^5)=\operatorname{Nm}(J),\qquad
 b_s=R(R+9792)\tau^2.
\]
Here f is nonzero by the reference chart. The BB-native pole at
7b_s/9 has the same negative-odd-valuation obstruction at every
prime outside S. The lemma gives, at a common slot over any prime of
positive odd depth mu=v_p(R), the inequalities
v(Z)>9mu/4 and v(f)>7mu/4.
The reference norm exclusions in v82 use the nonzero norms
41^2/64,17^2/64,63^2/64,7, all units outside S; their use is
therefore valid at this prime, not just at the original 149.
This first successful slot excludes the exceptional reference strata
before division, so the same inverse-Vieta chart recovers the scalar
point Q2 and the nonzero integral label a=2 nu(Q2).
The formal isometry and torsion-label removal from v82 now give
v_p(a)>9mu/4 at every positive odd scalar depth.
In particular M^3 divides |a|. This order of implications avoids
assuming the label on a degenerate reference stratum.

Write A_a=|a|. By (1),

\[
 h(u)<H A_a^{5/6},\quad H=2^{262}.
\tag{2}
\]

The dichotomy also shows A_a tends to infinity uniformly on rational
zeros with X nonzero as N tends to infinity: the low-d case gives
log A_a > (9/4)(N+1)log211; the high-d case gives
N log211 < H A_a^{5/6} (a weak inequality suffices).

## 3. Uniform heights and the two soundness conclusions

For the usual absolute logarithmic rational height, the fractional
linear identities s=u/(1-u), beta=2504+51s/k and the degree-three
rational map defining R give

\[
 h(\beta)\le h(u)+30,\qquad
 h(R)\le3h(u)+(2N+1)\log211+45.
\tag{3}
\]

For example, the two homogeneous linear forms for beta as a function
of u have row norms below exp(30). The sum of absolute coefficients
of AB as a polynomial in s is 4801*718*2<2^23; the corresponding
degree-three homogenized denominator A+B has a smaller row norm.
Use h(s)<=h(u)+log2 and K_N=3*2^15*211^(2N+1).
These estimates apply even if numerator and denominator cancel.

In the low-d case, (9/4)(N+1)>2N+1, so (2N+1)log211<log A_a.
In the high-d case (2N+1)log211<=2h(u)+log211.
In either case
\[
 h(R)\le5h(u)+\log A_a+51.
\tag{4}
\]

For the two-contact family retain the weighted trace estimate of v82,
with constants fixed independently of R and N, and its contact height
bounds. Write B_0=max(1,|n|,|a|,|b|,|t|).
By (2)--(4) the contribution A h(R)+J in that estimate is
o(B_0^2), uniformly as N grows. Absorb it into B_0^2/2.
If Delta is the integral Lucas residual and Delta is nonzero,
the unchanged comparison implication M_j^3 | a Delta, and
|a Delta|<=14 B_0^5, give
B_0^2/2 <= C_3 B_0^(35/18).
The constant is independent of N. This bounds B_0, contradicting
uniform divergence of A_a for sufficiently large N. Hence Delta=0.
The unchanged Lucas descent yields
log B_0 >= (A_a-6)log(A_a-3).
If the input residual J_X=|num(beta-n)| is nonzero, then
M_j | J_X and J_X<=4B_0 exp(h(beta)); the original v82 two-contact
bound gives log B_0 <= (7/5)h(beta)+C_5. This contradicts (2)--(3)
and Lucas descent for sufficiently large N. Thus beta=n in
(1/2)Z. The reduced denominator of X has square dividing the
squarefree integer 102, so X is integral.

For the three-contact specified route take exactly N=2^1600.
The low-d anchor forces A_a>2^1600. In the high-d case, assuming
A_a<=2^1600 would imply
2^1600 log211 <= h(u)<2^(262+8000/6)<2^1600, impossible.
Thus always A_a>2^1600. Equation (2) implies h(u)<A_a/16 because
6*(262+4)<1600. By (3)--(4), h(beta)<A_a/2 and h(R)<A_a.
The effective weighted estimate (3) of the 178-variable construction is

\[
 B_0^2<40\sum_{j=0}^2 h(t_j)+360h(R)+2500.
\]

Since B_0>=A_a>2^1600, the last two terms are less than B_0^2/2.
This gives its equation (4), with the same contact constants.
All its subsequent effective inequalities require only B_0>=2^960
and h(beta)<A_a/2. They give first Delta=0 and then
log B_0<240+A_a if J_X is nonzero, again contradicting Lucas descent.
Hence beta=n and X is integral. No unknown sufficient constant
occurs in the 177-coordinate specialization.

## 4. Ordered completeness, including X=0

Fix an integer X and the new R first. The real bound R>100 holds
uniformly. For integral X, s is in 2^20 Z_2. We have A=823543
and B=1 modulo 2^20. Thus v_2(A+B)=3 and
(A+B)/8=7 modulo 8, while A B=7 modulo 8. Therefore AB/(A+B)
has depth -3 and unit class 1 modulo 8. The multiplier K_N has
depth 15 and odd unit 3*211^(2N+1)=1 modulo 8. Hence R is a
2-adic square of depth 12. Also R+9792 is a 2-adic square,
since 9792=64*153, and (R+9792)/64=1 modulo 8.
In particular K_s=R(R+9792) is a 2-adic square.

For any positive reduced R=r/v, K_s=r(r+9792v)/v^2 and
gcd(r(r+9792v),v)=1. All its odd valuations are positive.
The v82 formal preparation works for this fixed R unchanged:
prepare both slots of each odd-support prime of K_s and the fixed
primes 2,3,7,17. Choose the reference depth first and then the exact
index-ratio depth t_p in the interval described in the source proof.
Its expansion gives v_p(tau)=2t_p-5v_p(R)-v_p(2).
The lower requirements on t_p make tau integral at every odd-support
prime, give v_2(b_s)>=4, and give positive depths at 3 and 7.
All other primes have even v_p(b_s) if their valuation is negative;
the reduced denominator of b_s is square. At the real places the
same compact neighborhoods give the v82 inequality
0<b_s<=24482500/R^4<1. Thus 7b_s/9 has square denominator,
lies in the squareclass 7 at 2 with depth at least four, and is in
(0,1). The BB-native pole realization applies. No squareclass
at 3 or 17 is required by the BB theorem (unlike the older pole).
The chosen finite-place and real conditions are open; shrink the
reference progression before selecting any comparison primes.

Choose the remaining three points and Lucas labels as in v82, with
the same beta, and the two or three comparison arguments using the
new positive weight R. Because R>100, the source real shift separation
is unchanged. At the next prime selection avoid the support of R,
the previous preparation moduli and the prescribed finite support
of the scalar point. The comparison preparation, all foreign-prime
conditions and pole realization are then exactly the source argument:
they depend on the fixed R and those finite avoidances, not on its
old rational-function expression. Fill the old physical coordinates
with these witnesses and use the new scalar rows below.
This supplies a zero for every integer, including X=0; no use of H4.1
at the excluded contact u=0 is made in completeness.

## 5. Literal quadratic compilation

All labels in the following paragraph are the **old** parent labels.
In both parent systems replace x37 by the unscaled square X^2.
Change its defining row to X^2-x37. Replace the scalar pair row by

\[
 x_{78}=823543+1807299379200x_{37}
                    +989560464998400000x_{37}^2.
\]

This is A(k x37). Delete the four-contact product row and x77.
Replace the old forced-prime row by

\[
 x_{90}(x_{78}+1+kx_{37})
       -20742144 C^2 x_{78}(1+kx_{37})=0.
\]

It recovers R=x90 without division by a possibly vanishing coordinate,
as x78=A>0 and B>0. In the two input-cleared rows, replacing the old
gauged x37 by X^2 times the corresponding nonzero c-unit lets us
divide out that unit. The resulting equations are

\[
 -x_{17}+x_{23}+(51x_{37}+2504)x_{117}=0,\qquad
 -x_{18}+x_{24}+(51x_{37}+2504)x_{118}=0.
\]

The unit is old x160 in the 163 table and old x161 in the 178 table.
The unchanged literal unit equation ensures it is nonzero. Every
other row is identical to its parent after shifting indices above 77
down one. The remaining inverse Laurent gauges and their guards are
the parent's, with the newly forced R>0 established first. Thus the
recompiled system has the identical physical interpretation apart
from the deliberately changed scalar normalizer. There is no
unjustified projection from a zero set of a higher-degree row.

| Parent | New total | Quadratic rows | Symbolic coordinate profiles | Parameter-separated terms |
|---|---:|---:|---:|---:|
| 163 | 162 | 136 | 2761 | 2762 |
| 178 | 177 | 149 | 3004 | 3005 |

The polynomial is the sum of the listed quadratic squares, after
substitution of the fixed coefficient C. Its rational zero set is
the common zero set of the rows. In each case the coefficient of
X^4 is literally one, so the degree is exactly four and content one.
C is a coefficient, never an existential variable. The symbolic
profiles count is not an assertion about possible cancellation upon
every specialization. The huge fully specified 177 coefficients
are retained in parameter-separated form.

The pinned parent tables are
0f85885f659374bef4b8af37a1835d00d70d7196 (163) and
5f5dc81b80d46f93cd2018c93849c87e1ee83bc1 (178).
The source JSONs were rebuilt exactly when committed. An independent
checker replays the changes, occurrence audit, coefficient expansion
and scalar congruences without evaluating the huge fixed C.
Run from the repository root:
```sh
python -B computation/harmonic_scalar_20261125/check.py
```
