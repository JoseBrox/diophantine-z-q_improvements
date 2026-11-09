# Independent audit of the forced prime 149

Status: PASS, 9 November 2026. The scalar normalizer may use
ell=149 and A_N=149^(2N+1) in place of80989. This assertion concerns
the current shifted label beta=51X^2+2504 and scalar shift9792.
It does not assert a globally optimal prime or coefficient choice.

## Exact prime and contact tests

Trial division through12 proves149 prime. For the five rational roots
theta=0,1,2401,-343/32,1/2 of the scalar contact product, the residues
of (theta-2504)/51 modulo149 are respectively
59,97,109,108,78. Raising each to74 gives148. Thus none is a square,
including zero. An independent enumeration of all odd primes at most149
not dividing51 finds that149 is the only one satisfying all five
Euler exclusions for this fixed affine label.

If X is149-integral, the scalar product r is therefore a149-unit.
If v149(X)<0, its valuation is10v149(X). For
R=A_N r/(1+149^2 r), this proves v149(R)=2N+1 or2N-1,
respectively. Both are positive odd integers for every N>=1.

## Local scalar argument

The forced-prime extraction uses the pole obstruction only outside
2,3,17, and uses good odd reduction of E:y^2=x^3-(11-6sqrt2)x.
The discriminant has support over2 and7;149 is admissible.
The exceptional finite H translates have norm support in
2,3,7,17,41, so all reciprocal-abscissa norms are149-units.
The formal logarithm is an isometry over the unramified149-adic
completion; h=m/2 is integral there. None of these statements needs
the contact cutoff76176. In fact149 is inert in Q(sqrt2), just as80989
is, although inertness is not necessary for the argument.

Every consumed generic scalar contact prime exceeds76176, hence is
different from149. At such a prime, A_N and1+149^2r are units, so
the original positive odd contact valuation and unit shift argument
are unchanged. Conversely149 is automatically absent from M5(beta).
Thus the strengthened joint divisibility
149^L_N M5(beta)^3 | |a-1|
is valid for the fourth-power scalar tree.

## Completeness and preparation

For integral X, the unchanged elementary input congruences give
v2(r) in{2,3}, v3(r)=1 and r=15 mod17. The new denominator is a
unit at2 and3, and is1+15*149^2=3 mod17. A_N is a unit at all
three places. Hence v2(R) in{2,3}, v3(R)=1 and v17(R)=0.
Since9792=2^6*3^2*17, the unit1+9792/R is a square at each of
2,3,17. The pole input R(R+9792)W^2 is locally square there.
No separate local squareclass condition on149 is required.

Write D=1+149^2r. The scalar product is
R(R+9792)=A_N r(A_N r+9792D)/D^2.
Both numerator factors are coprime to D, because gcd(r,D)=1 and
D=1 mod149. Its reduced denominator is a square. Arbitrarily deep
finite preparation of W works as before. Also
R>=A_N/(1+149^2) uniformly for integral input; hence the current
real bounded-neighborhood argument remains uniform in the input.

The final shared index must preserve a finite scalar modulus which
may contain149 and its fixed reduction-order divisors. This modulus
is fixed before selecting new comparison primes. The retained
prime-pattern/separation premise permits precisely this arbitrary
fixed finite modulus, and149 already lies in the omitted small-prime
set. No group-order conflict or new arithmetic premise arises.

## Literal source dependency

Inspection of every integer coefficient in family249_v17 shows that
the only residual coefficient divisible by80989 is80989^2 in source
row733. The parameter A_N is separately declared. The normalized
row is R+ell^2*r*R-A_N*r=0. Therefore changing this row and the
fixed-parameter declaration accounts for every essential occurrence.
The exact polynomial expansion and height threshold must of course
be regenerated for149; the arithmetic proof needs no other change.
