# Uniform anchor via a depressed cubic (162/177 variables)

This improves the [harmonic scalar](../harmonic_scalar_20261125/README.md)
without changing its variable count or any retained arithmetic premise.
The 177-variable member now has the modest explicit parameter C=331^26,
and its full integer coefficient expansion is supplied. The previous
enormous parameter is no longer necessary.

## 1. Scalar and the uniform anchor

Keep k=2^20, s=k X^2, u=s/(1+s), beta=51X^2+2504. Set
\[
 r=(2401+2400s)(343+375s)(1+s),
 \qquad
 w=s+34981/36000.
\]
The exact depressed cubic identity is
\[
 r=e+\alpha w^3+\gamma w,\qquad
 e=-1081567619/25920000,\quad
 \alpha=900000,\quad\gamma=-1053721/480.
\]
For N>=1 let C=331^N, K=56*331*C^2 and
\[
 R=K r/(r-e).
\]
Since s>=0, r>=823543 and -823543<e<0, we have K/2<R<K,
so R>100. For nonzero X, the same contact map u lies strictly in
(0,1). Its reduced five homogeneous contact factors are exactly
those in the harmonic proof. Except for the three possible contacts
of r, all are even at primes outside S. If p is outside
S' = S union {47,1019,2053}, and outside 331, an odd contact
gives positive odd v_p(r); e is a p-adic unit since
\[
 1081567619=11\cdot47\cdot1019\cdot2053,\quad
 25920000=2^9 3^4 5^4.
\]
Consequently r-e is a unit and the same positive odd depth is
v_p(R). At 331, direct enumeration of x mod 331 gives
r(kx^2) and r(kx^2)-e nonzero modulo 331 (the notation r(kx^2)
here means evaluate the displayed cubic in s). At nonintegral
331-adic X both r and r-e have the same leading term of degree
three with unit coefficient, so their valuations are equal.
Thus **v_331(R)=2N+1 for every rational X**, without exception.
The prime 331 is not in the odd contact radical.

The reference guard and scalar extraction of v82/BB-native therefore
apply at 331 before any quotient is formed, exactly as in the
harmonic proof. For X nonzero let A_a=|a| be the absolute value of
the resulting nonzero integral scalar label. Put
\[
 L_N=\lfloor9(2N+1)/4\rfloor+1,\qquad
 M=M_{S'}(u).
\]
The scalar lemma gives
\[
 331^{L_N}M^3\mid A_a.
\]
Indeed 331 and M are coprime by the anchor residue computation;
outside S' the old scalar local extraction applies at every
positive odd scalar contact. No stronger modular estimate for a new
radical is assumed: put P=47*1019*2053<2^27; then
M_S(u)<=P M. H4.1 and its numerical bound in v68 give
\[
 h(u)<2^{237}P^2 M^2(1+\log P+\log M)^2
      <2^{301} M^3
      \le 2^{301}331^{-L_N}A_a.
\]
For the second inequality use (1+log P)^2<2^9, and
(1+log M)^2<2M for M>=1. All constants are uniform.

The rational height map has degree three and
\[
 h(\beta)\le h(u)+30,\qquad
 h(R)\le3h(u)+\log K+50.
\]
Indeed clear the denominator 25920000 of e, bound the coefficient
one-norm of r by 2^23, and use h(s)<=h(u)+log 2.
The real bound and these estimates now replace the height-valuation
dichotomy in the previous construction. As N grows, A_a>=331^L_N
tends to infinity, the ratio h(u)/A_a tends uniformly to zero,
and h(R)=o(A_a^2). The entire two-contact soundness argument in
Section 3 of the harmonic proof follows with unchanged comparison
and Lucas constants.

For the three-contact specified member fix N=26. Then L_N=120 and
A_a>=331^120>2^960. In particular h(u)<2^(-659) A_a.
The estimates give h(beta)<A_a/2 and h(R)<A_a (use
log K<400, which follows from 331<512 and log 2<0.7).
The effective weighted sum from the 178-variable source now has
360h(R)+2500<B_0^2/2. All the subsequent explicit endpoint
comparisons in that source apply, because they require only
B_0>=2^960 and h(beta)<A_a/2. Thus both Delta=0 and beta=n follow;
as before the denominator of X has square dividing 102.
For X=0 integrality is automatic.

## 2. Integer completeness

For integral X, s belongs to 2^20 Z_2 and r=7^7 modulo 2^20.
The depth of e is -9 and the unit 2^9(r-e) is 3 modulo 8.
Therefore r/(r-e) has depth 9 and odd unit 7/3=5 modulo 8.
The multiplier K=56*331^(2N+1) has depth 3 and unit
7*331^(2N+1)=5 modulo 8. Hence R has depth 12 and unit 1
modulo 8, as required in the harmonic proof. Also
(R+9792)/64=1 modulo 8. This preserves its full ordered completeness
proof, including the scalar's odd-support preparation, square
denominator at every foreign prime, and subsequent comparison
prime choices. The new R is fixed before any points or primes are
chosen. No global prime selection beyond the source is assumed.

## 3. Two quadrics instead of three

Use the harmonic table's numbering: x37=X^2, x89=R. Instead of
storing the value A, store x77=T. Write the following affine
expressions (not additional coordinates):
\[
 W=36000 k x_{37}+34981,\quad V=x_{89}-K,\quad
 L=432000000 T-1053721 V.
\]
The two quadrics, with fixed coefficient K=18536 C^2, are
\[
 3WL+2(1081567619)K=0,\qquad
 1944000000 TL+1081567619 K W V=0.
\]
Since W=36000 w>0, the first equation gives L nonzero.
Substitution into the second gives T=W^2 V/1296000000=w^2 V.
The first then gives (\alpha w^3+\gamma w)V=K e.
Since r-e>0, it follows that V=K e/(r-e) and
R=K+V=K r/(r-e), exactly the desired scalar. Conversely this
R and T satisfy both quadrics. In particular no spurious branch
of the projected rational quartic is admitted, including when X=0.

This is a useful general rechart: for a rational depressed cubic
D(w)=alpha w^3+gamma w and nonzero constant e0,
the graph D(w)V=e0, with w nonzero, is encoded by
w(alpha T+gamma V)=e0, T(alpha T+gamma V)=e0 wV.
Only one auxiliary is needed. Multiplication by fixed denominators
and primitive row normalization preserve the zero set.

All other rows are literally those of the harmonic tables.
The stored quadrics have exact degree at most two. Their squared
sum has X^4 coefficient 1 and uses all coordinates.

| Total variables | Quadrics | Symbolic profiles | Parameter-separated terms | At N=26: monomials |
|---:|---:|---:|---:|---:|
| 162 | 136 | 2765 | 2782 | 2765 |
| 177 | 149 | 3008 | 3025 | 3008 |

The explicit 177-variable polynomial (N=26) has coefficient height
of exactly 1923 bits (579 decimal digits), and its plain-text
expansion has 72580 ASCII bytes, with no final newline.
This is a finite materialized coefficient table, as opposed to the
earlier harmonic specialization C=211^(2^1600). It is still larger
in coefficient height than the older 178-variable member, but the
variable count has priority. The general 162-variable N=26
specialization is only an algebraic fixture; the two-contact
sufficient cutoff remains ineffective. The proof retains all
the stated project arithmetic premises, and the finite verifier
does not prove those premises.
