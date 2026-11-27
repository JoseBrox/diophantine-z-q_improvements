# Homogeneous pole gate and mixed fourth factor, 27 November 2026

Status: rigorous local transfer and exact complete systems relative to the
retained arithmetic suppliers of the pinned parents. No new quartic
variable-count record. No change to main or the upstream PR.

## 1. A 48-coordinate degree-eight ordinary-abc definition

Parent: linear_reciprocal50_20261127, commit
4c0436948d502f0290e9f2ed1018366a61a9d905, quadrics blob
db36624fe070015ccda873f2602f08508a3ba351. Keep its height/contact
equations, reference and point charts, comparison packing P,Q,
unit c u=1 and five native pole equations. Delete the two components
of L=cJ. Rename the pole denominator K_s and replace t_0 by a rational
coordinate r. Store W_s=rW and D_s=rD_g. In physical notation choose

    W=1+c^2 C^4-c^4 bar(I)^4+c J+c^3 bar(K').

(The exponents differ from the earlier 49-coordinate checkpoint.)
The existing comparison registers satisfy PQ=u C^4-c bar(I)^4.
The detector and three new gate equations are

    u^2 W_s = r(u^2+c P Q+u J+c bar(K')),
    D_s Tr(W_s) = Nm(W_s-r),
    u(K_s-u-2r)=r^2,
    D_s^2+K_s-u-(2+c)r=0.

The last three equations are quadratic. The first is a degree-four
field residual, since J=E_rY/D and K'=E_rZ/D are already quadratic
expressions in retained coordinates. Multiplication by 49 clears
the fixed denominator. The five retained native rows still give
the cleared native pole at t_0=1+c r, because K_s=u(1+c r)^2.

For sufficiently large fixed B the inherited height/contact bounds
force a consumed good odd prime (independently of the new gate).
If r=0, then K_s=u and t_0=1, and the native pole would have
input 7c with negative odd valuation. This is impossible by the
native pole obstruction. If t_0=0, the cleared native first equation
forces e to be a unit; the middle gives U'V' negative odd valuation;
the last equation then has incompatible valuation parity.
Thus r and t_0 are nonzero on every relevant fiber, not extra guards.
The norm equation recovers the actual D_g, since Tr(W)=0 implies
Nm(W-1)=0 in K, hence W=1, a contradiction.

Write D_g=D_s/r. Subtract the two gate equations after using cu=1:
r^2(D_g^2+c)=cr, hence

    r=c/(D_g^2+c),  t_0=1+cr.

At a consumed prime v(c)=-mu, mu positive odd, the native pole
obstruction at 7c/t_0^2 gives v(t_0)<-mu/2. Consequently
v(r)<mu/2 and v(D_g^2+c)=-mu-v(r)>-3mu/2. The odd valuation
of c cannot tie the even valuation of D_g^2, so v(D_g)>-3mu/4.
The inherited norm/trace estimate gives a successful slot with
v(W)>-3mu/4 (if both slots are negative use
v(D_g)<=max(v(W),v(bar W)); otherwise take an integral slot).

At every such prime where X is a unit, the four nonconstant
valuations of W are

    -2mu+4v(C), -4mu+4v(bar I), -mu+v(J), -3mu+v(bar K').

The first two are in distinct even classes modulo four. The last
two are odd. If the latter tie, their reciprocal valuations differ
by 2mu and exactly one is 2 modulo four. The proved unit-input
lemma of the 50-variable parent gives 4v(error)<=-|v(product)|-2
for that pair. Its corresponding fourth-power error term has
contact exponent one larger than its linear reciprocal term,
and therefore has strictly lower valuation than the tie. Thus any
negative minimum is unique; ties with the constant at zero are
harmless here, since this is a single detector, not a product of
factors. In the successful slot we obtain

    v(C)>5mu/16, v(bar I)>13mu/16,
    v(J)>mu/4, v(bar K')>9mu/4.

All tests are positive. The parent unit-input lemma puts both
pairs in the formal group, with equal positive integer depths
within each pair. Each comparison has precision at least two
after division by the corresponding slope; the relative
formal logarithm errors have depth at least four. Multiplication
by the integer reference labels, whose difference is one, and
subtraction give v_p(m-X)>=2. No conclusion is needed at
nonunit input primes. As in the 50 proof, their total logarithmic
mass is at most 2h(X). All remaining consumed primes have their
squares dividing the numerator of m-X. For X!=0,m this gives

    R_u <= (5/2) h(X)+(1/2)log(1+|m|).
    R_u >= (347/200) h(M)-(3/4) h(X)-O(1).
    h(X) <= (501/997) h(M)+O(1).

The strict margin is 20309/199400. The original unchanged
trace estimate bounds m^2 by O(h(M)+1). Thus h(M) is bounded
uniformly on any nonintegral-input fiber, contradicting
M>=B for all sufficiently large B.

### Completeness, including foreign primes

Take the parent's genuine multiplication family, with the
same prepared reference and point neighborhoods and the same
contact prime selection. At selected primes v(c)=-1; the
successful-slot errors have depth >=3 and products depth >=4,
so W=1 modulo the prime. For nonzero integer input the
opposite-slot reciprocal products are units under the parent's
preparation, giving a negative minimum by the just-proved
noncancellation argument. The shifted norm/trace therefore
gives v(D_g)>0. For the canonical X=0 family all tests vanish
and W=1,D_g=0 directly. In either case r is a unit and t_0
has valuation -1, so the actual pole input has valuation one.

At every foreign positive odd valuation j=v(c)>0, parity gives
v(D_g^2+c)=min(2v(D_g),j)<=j. Thus v(r)>=0, t_0 is a unit,
and v(7c/t_0^2)=j outside 7. This works for any D_g, without
a separate foreign noncancellation theorem for W. At even
valuations of c the pole input has even valuation outside 7.
The parent's contact factorization covers all remaining primes.
At fixed places and positive real infinity the bounded tests
and c->0 give W-1=O(c), D_g=O(c^2), r->1, t_0->1 and
7c/t_0^2~7c. Retain the parent's dyadic squareclass seven
and large even depth, seven-adic positive valuation and real
range (0,1). Hence the actual pole has square denominator and
all the required BB-native realization hypotheses. Choose the
pole witnesses last, as in the parent. This proves completeness
with no additional arithmetic premise.

### Compilation and the remaining obstruction

Indices 21,22 of the parent are deleted; all later indices
shift down by two. P,Q=21:22,23:24; powers=25,26;
W_s=27:28, r=29, K_s=30, D_s=38, c=39,u=40.
Every other retained row is copied with that renumbering.
The two new detector components are quartic, the other 36
residuals quadratic. Their squared sum has exact degree eight,
content one, and 48 coordinates. The B=1 expansion has
1133 terms and 21592 ASCII bytes; this fixture is NOT asserted
defining. The sufficient defining cutoff is still ineffective.

Restricted obstruction: a termwise diagonal Laurent compilation
of these particular affine-reference/point rows, with a common
weight for the two components of each field coordinate, cannot
absorb the unequal reciprocal weights. Allow weights in the
free abelian group generated by c,r and any additional independent
units, and arbitrary unit multipliers of rows. In A B_r=a, where
B_r=A+S+T, the quadratic monomials AA,AS,AT force
w_A=w_S=w_T. In the secant row
delta(B_r Y+A Z)=(s-t)h-t^2, the monomials AY and AZ then
force w_Y=w_Z. But in the detector the AY and AZ monomials
from u J and c bar(K') have equal coordinate weights and
opposite c exponents -1,+1. The common r and any row multiplier
cancel in this comparison. They cannot both be quadratic
without a nontrivial unit coefficient. Hence these termwise
rescalings cannot make the two residuals quadratic, even
with r as a second scaling unit. This argument does not rule
out nonlinear chart changes, variable-dependent row combinations,
or alternative detectors. No 48-variable quartic is claimed.

## 2. General routes: two multiplication stages instead of three

Use the same physical notation as affine_fourth_factor_20261127,
and the same original projective-contact parents. Keep the
first three shared factors, the scalar block and all remaining
arithmetic. Replace the fourth factor instead by the product
of two factors

    F_D=1+c A4+c^2 A1^2,
    F_C=1+c B3+c^2 B0^2.

At a consumed prime v(c)=-mu odd the reciprocal valuations
are even, and the square valuations multiples of four.
In EACH factor the three term valuations belong to
0 (constant), odd, and 2 mod 4. Thus its minimum is unique,
nonpositive, and if it is integral its residue is one.
The shared gate provides the same common slot. All four
reciprocal tests have positive valuations: the linear ones
are >3mu/4, and the squared ones are >7mu/4. The original
required depth bounds (even positive raw reciprocal valuation
>=2) follow. Every other comparison and the v82 extraction,
weighted trace/height and effective N=21 endpoint remain
unchanged. There is no input-unit restriction or discarded
prime set in this transfer. On the parent's prepared integer
family, c has depth -1 and all these terms have positive
valuation in the selected slot. The opposite slot has residue
one or a pole. The shifted norm/trace and all native pole
preparation are therefore unchanged. Fixed-place and real
limits are again one.

The exact quadratic chart uses the original gauges. Write
A_s=x119:120, B_s=x143:144, G_s=bar(x133:134),
R_s=x19-2 rho x20, P=x99:100, u=1/c, v=u^2.
Then A1=A_s,A4=u B_s,B3=c G_s,B0^2=R_s. Set
Phi=v(1+B_s)+A_s^2 and L_C=v+G_s+R_s; these are
u^2 F_D and u^2 F_C respectively.

For the fixed 175 construction u=x160,v=x161 and W_s=x153:154.
The first-three product is u^2 P, W_s=uW, so use
    x95:96=Phi, Y=x174:175=P Phi, u W_s=Y L_C.
For the 161 family u=x158,v=x159, W_s=x152:153.
The first-three product is c^2 P, W_s=u^2 W, so use
    u Phi_s=Phi, u Y=P Phi_s, v W_s=Y L_C,
with Phi_s=x95:96 and Y=x160:161.
All three field equations in each case are quadratic. They
have exact unique lifts on the guarded unit locus. The six
components replace precisely the old partial-pair, factor-3
and final-product rows. The other equations, including point
and pole charts, are literally unchanged.

This removes one multiplication stage relative to the previous
three-affine-factor implementation, but uses its register to
store the quadratic factor evaluation. Thus the coordinate
count remains 161/175. It is a small complexity improvement
over the prior affine rechart, not a two-coordinate saving.

The full expansions and independent BigInt compilation check give:
161-family: 135 quadrics, 2813 monomials at N=21, 64683 bytes.
Fixed 175: 147 quadrics, 3162 monomials, 72390 bytes, 802-bit
height, exact degree four and content one, C=331^21.
The 161-family's 17 parameter-varying profiles are unchanged,
and all changed coefficients are constant-only profiles.
Its byte count is 599 below the original projective-contact
parent for every positive N. Using the parent's established
monotonicity, the strict 100000-byte budget now extends through
N=290 (99928 bytes); N=291 gives 100060 bytes.
N=290 is NOT a certified defining member. Its defining cutoff
remains ineffective.

A parity-only merger into two affine factors cannot separate the
three raw even-valued reciprocal terms: two must be in the same
factor. If their exponents are both odd they can tie one another;
if either exponent is even its valuation can tie the constant.
This is a restriction on the parity-only proof, not an obstruction
to every possible merger using additional point identities.

Actual local negative control: at p=73, use A1=A4=f([34]R0)
at the slot with rho=143465843091848321867 mod 73^11.
The reciprocal is 136074681704984943834 mod 73^11,
of valuation two. For c=t/73, t=41001420833059094,
1+c A1+c^2 A4 has valuation at least nine. The derivative
with respect to t of the reduced expression
1+(f/73^2)t(73+t) is a unit at its root mod 73, so Hensel
gives arbitrarily deep positive valuations. This violates
the nonpositive-factor condition needed for the common-slot
product proof. It is not a rational counterexample to a
complete defining system, nor a global lower bound.

## 3. Verification and scope

Run node check.js from the repository checkout. It pins all
three original inputs, reconstructs the changed rows and
expands all squares using integer arithmetic. The reconstruction
and expansion functions were executed in the BigInt tool
environment; hosted CI and a full checkout execution are not
claimed. The 48 table and its B=1 literal independently match
the executed Python/SymPy reconstruction byte for byte (Git
blobs 6d8a962b7163f84229b39c805e8bcb67afc50a57 and
1311ca9ac4e3f89007365982caf18b3dd6e76407).
Independent finite tests: 5283920 unit-input valuation profiles,
56304 successful profiles, 2274 rational gate fixtures, 700
foreign gate profiles, and the exact height margin. These are
supplementary checks, not replacements for the proofs above
or verification of the inherited arithmetic suppliers.

The quartic variable frontier remains 161/175/50. The 48-coordinate
degree-eight system is a degree/variable tradeoff, not a replacement
for the 50-coordinate quartic. The next actual variable savings
require a nonlinear unequal-weight point/chart absorption in
the abc route, and making the mixed factor evaluation affine
or reusing an existing register in the general routes.
