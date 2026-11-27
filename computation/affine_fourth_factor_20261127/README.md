# Affine reciprocal-factor rechart and dual-linear detector checkpoint

27 November 2026. This note gives a complete replacement of the fourth
shared factor in the projective-contact 161/175-variable quartics, under
their existing arithmetic premises. It improves sparsity and size, not
variable count. The second part records the actual obstruction and a
positive arithmetic result for linearizing both reciprocal-product
terms of the ordinary-abc 50-variable route. The latter is not a new
quartic record.

## 1. Complete general-route transfer

Use the notation and premises of
[projective_contacts_20261126](../projective_contacts_20261126/README.md),
[the v78 shared-product proof](../../papers/quartic/shared_product_audit_20261119_v78.tex)
and [the v82 scalar-point proof](../../papers/quartic/scalar_point163_179_20261120_v82.tex).
In the fourth factor write \(A_1=f(U_1), A_4=f(U_4),
B_3=\overline{f(V_3)}, B_0=\overline{f(H-P_0)}\).
The old factor was
\[
  1+c A_1^2-c^3 A_4^2+c^2 B_3^2+c^4 B_0^4 .
\]
Replace it by the product of the three factors
\[
 F_A=1+cA_1,\qquad F_B=1+cA_4,\qquad
 F_C=1+cB_3+c^2 B_0^2 .
\]
The first three factors, scalar block, point and comparison equations,
norm/trace equation, pole inputs and every contact remain unchanged.

At each consumed good unramified prime the shared gate first gives
\(v(c)=-\mu\) with \(\mu>0\) odd, as before. Every reciprocal-abscissa
valuation is even. In \(F_A,F_B\) the constant and the nonconstant
term have opposite parity; in \(F_C\) the three finite valuation
classes are respectively 0, odd, and \(2\bmod4\).
In particular each factor is nonzero, has valuation at most zero,
and an integral factor reduces to one. This is true at both slots,
including the repeated inert slot, without a unit-input restriction.
The product lemma therefore still gives a common slot where every
factor has valuation greater than \(-\mu/4\). It follows that
\[
 v(A_1),v(A_4),v(B_3)>3\mu/4,\qquad
 v(B_0^2)>7\mu/4.
\]
The even valuations of the three raw reciprocals and the multiple-of-four
valuation of the squared reciprocal imply exactly the original
positive depth bounds (at least two for each raw reciprocal).
The comparison, Lucas and scalar precisions established in v82 are
unchanged. In particular the same divisibilities \(M_j^3\mid a\Delta\)
and \(M_j^3\mid J_X\) apply where relevant. No primes are discarded
from the effective height argument. The numerical anchor N=21 and
the 175-variable defining theorem transfer without a new arithmetic
assumption. The 161-variable family's sufficient N remains ineffective.

For integer completeness, the prepared successful slot has raw
reciprocal depths at least two, and squared reciprocal depth at
least four; at a selected prime \(v(c)=-1\).
All four nonconstant terms are then positive. The opposite-slot
factor argument gives residue one or a pole. Thus the shifted
norm/trace has positive valuation at the selected prime, exactly
as in the parent. At fixed finite and real places the old bounded
point neighborhoods and \(c\to0\) give each new factor tending
to one. The parity of every actual pole input away from selected
primes depends only on the unchanged contact weight and a rational
square. Hence the parent prepared-input BB realization, ordered
after the contacts and point choices, applies unchanged. Neither
a global sign of a factor nor a new depth-two reference condition
is used.

### Literal quadratic implementation

Let \(u=c^{-1}\), \(v=u^2\). In the final tables write \(x_{i:i+1}\)
for the corresponding field pair in basis \(1,\sqrt2\). Put
\[
 P=x_{99:100},\quad
 A_s=x_{119:120},\quad B_s=x_{143:144},\quad
 G_s=\overline{x_{133:134}},\quad R_s=x_{19}-2\sqrt2\,x_{20}.
\]
The physical outputs are \(A_1=A_s,\ A_4=uB_s,\ B_3=cG_s,\ B_0^2=R_s\).
These follow from the retained pair and reference gauges; the
old partial-pair equation directly verifies the first two uses
of the scaled reciprocals. Define the affine expressions
\[
 L_A=u+A_s,\quad L_B=1+B_s,\quad L_C=v+G_s+R_s .
\]
Then \(F_A F_B F_C=c^3 L_A L_B L_C\).

In the 175-member \(u=x_{160},v=x_{161}\);
the product of the first three physical factors is \(u^2P\)
and the common product storage is \(W_s=uW=x_{153:154}\).
Use the formerly private partial-pair registers \(Z=x_{174:175}\)
and the old factor-3 registers \(Y=x_{95:96}\) for the product stages
\[
 Z=P L_A,\quad Y=Z L_B,\quad W_s=Y L_C.
\]
Their three field equations are quadratic, and recover exactly
the changed physical common product, since \(u\cdot u^2\cdot c^3=1\).
In the 161-family \(u=x_{158},v=x_{159}\),
the first-three-factor product is \(c^2P\), and
\(W_s=u^2W=x_{152:153}\).
Use \(Z=x_{160:161}\) and \(Y=x_{95:96}\), with
\[
 uZ=P L_A,\quad uY=Z L_B,\quad uW_s=Y L_C .
\]
This gives \(W_s=c^3P L_A L_B L_C\), as required.
The units are nonzero by the retained literal guard; the new stages
have unique recoveries. For both variants all six previous
factor-3, partial-pair, and final product rows are replaced by the six
rational components of the three displayed field equations. No
other row uses a reinterpreted private coordinate.

This removes the partial hyperbolic construction, but its two
coordinates are needed for the extra product stage. It therefore
does NOT give 159/173 variables. It is useful for further work
on the product chain because its final three factors are affine.

## 2. Exact coefficient effects

The [check.js](check.js) reconstruction reads the pinned projective
parents, checks that the private coordinates occur only in the
six replaced rows, builds the new bilinear stages, retains every
other row, and expands the complete sum of squares by BigInt convolution.

| Route | Variables | Rows | Old profiles | New profiles | Old N=21 bytes | New N=21 bytes |
|---|---:|---:|---:|---:|---:|---:|
| General family | 161 | 135 | 2846 | 2821 | 65282 | 64787 |
| Fixed member | 175 | 147 | 3196 | 3167 | 73080 | 72396 |

Both have exact degree four, coefficient of \(X^4\) equal to one,
integer content one, and the same 802-bit height at N=21.
The fixed 175-variable member retains the parent's effective
arithmetic proof at C=331^21; the 161-variable N=21 example
is only a fixture.

The 161 table has 17 parameter-varying monomial profiles. They
are literally unchanged, and the changed coefficients occupy
158 constant-only profiles. Consequently the canonical byte count
differs from the projective parent by the constant -495 for every
positive integer N, including N=1. By the parent's established
profile monotonicity from N=2 onward, the strict 100000-byte budget
now holds exactly for \(1\le N\le289\).
At N=289 the size is 99902 bytes, and at N=290 it is 100032.
No effective weighted-height bound for this family is proved by
that size improvement. N=289 is not a certified defining instance.
No new numerical parameter is claimed.

## 3. Failure of the direct same-weight dual-linear proposal

In the ordinary-abc 50-variable route use its physical
\(C=XS_U-S_H,\ I=XS_V-S_{H-R_0},\ J=X^2f(H)f(U),\
K'=X^2f(H-R_0)f(V)\).
The most immediate candidate to eliminate the remaining field
register replaces the detector by
\[
 W_{\rm bad}=1+cC^4-c^3\bar I^4+c^2(J+\bar K').
\]
The following is an obstruction to the claimed local extraction,
not a rational counterexample to the whole defining polynomial
(the contact scalar is not enforced in these fixtures).

Take \(X=1,\ H=[h]R_0,\ U=-H+(0,0),\ V=H-R_0\).
The translation identity
\(f(H+(0,0))=-x(H)/D\) and the change of sign of its slope
give \(C=I=0\) exactly, \(J=-1/D\), and
\(K'=f([h-1]R_0)^2\).
The difference \(U-V\) has integer label \(m=1-2h\).
At p=31 take h=13143 and the slot with
\(\sqrt2=2767\bmod31^3\).
The exact elliptic division-polynomial recurrence gives
\[
 f(H)=23908,\quad \overline{f(V)}=8116,\quad
 J=28236,\quad\bar K'=1555\pmod{31^3}.
\]
Thus both products are units and their sum is zero modulo p^3.
The other-slot sum is 18 modulo p, hence a unit.
With \(c=1/p\), the first slot of W_bad is 1 modulo p and
the other has valuation -2. In particular the norm/trace gate
gives positive valuation of D_g. The reciprocal gate and
its local pole constraints can be satisfied at this prime:
\(u(1+D_g)\) has valuation one, so \(t_0=1+[u(1+D_g)]^{-1}\)
has valuation -1 and \(b_{\rm pole}=7c/t_0^2\) has valuation one.
For a local pole solution take e=1, p=0 and U=V=sqrt(1-b_pole),
q=0; the square root exists by Hensel at odd p.
Nevertheless \(m\equiv3\pmod{31}\ne1=X\).
Every elliptic point in the example is an actual K-point
defined by its integer index, not a free valuation model.
The point pair is finite and distinct by its nonzero free labels.
A second fixture at p=167 and h=1070541 appears in
[dual_linear_receipt.json](dual_linear_receipt.json).
The local counterexamples rule out using the same extraction
proof for this detector; they do not rule out every modified
48-variable chart or certify a full rational zero with nonintegral input.

## 4. Separated-weight dual-linear arithmetic (not yet a quartic)

Both reciprocal products can be linearized arithmetically if
their contact weights are separated and the stronger old
normalizer is used. Set
\[
 W_*=1+c^3C^4-c^5\bar I^4+c^2 J+c^4\bar K',
 \qquad D_g\operatorname{Tr}W_*=\operatorname{Nm}(W_*-1).
\]
Use the extra rational register \(\alpha=u+D_s^2\), where
\(D_s=uD_g\); the normalizer is
\((t_0-1)\alpha=1\).
Keep the cleared BB-native pole at \(7c/t_0^2\) exactly as
in the 50-variable route. The norm equation guards its
trace denominator.

At a consumed prime \(v(c)=-\mu\), \(\mu>0\) odd, the
cleared pole obstruction excludes \(t_0=0\) and forces
\(v(t_0)<-\mu/2\).
Thus \(v(\alpha)>\mu/2\).
The valuations of u and D_s^2 have opposite parity,
so \(v(D_s)>\mu/4\) and \(v(D_g)>-3\mu/4\).
The norm/trace inequality supplies a slot with
\(v(W_*)>-3\mu/4\). These implications use only the
old gate and pole arguments.

Now suppose X is a unit. The two error terms have distinct
odd valuation classes modulo four. The only possible equality
between nonconstant terms of different types is between the
two linear reciprocal terms. Such equality gives
\(v(\bar K')=v(J)+2\mu\); precisely one of the two
reciprocal valuations is 2 modulo 4.
The 50-variable unit-input lemma for a pair \((E,B')=(C,J)\)
or \((I,K')\) states that in this case
\(4v(E)\le-|v(B')|-2\).
The error exponent (3 or 5) exceeds its reciprocal exponent
(2 or 4), hence this odd error term is strictly below the
tied even terms. A negative minimum is therefore unique.
At the successful slot
\[
 v(C)>9\mu/16,\quad v(\bar I)>17\mu/16,\quad
 v(J)>5\mu/4,\quad v(\bar K')>13\mu/4.
\]
Positivity of error and product puts each reference and its
numerator on the formal branch at equal depths, by the proved
50-variable unit-input lemma. In particular their product
valuations are \(4d_+,4d_-\).
The two slope ratio estimates followed by the relative
order-four formal logarithm estimate give
\[
 v_p(m-X)\ \ge\
 2+\lfloor9\mu/16\rfloor+\lfloor5\mu/16\rfloor\ \ge 2 .
\]
For the relative logarithm bound, \(4d_+>5\mu/4\),
\(4d_->13\mu/4\); these exceed the displayed required
precision for \(\mu\ge7\), and \(\mu=1,3,5\) are immediate.
Multiplying the two ratio congruences by the corresponding
integral reference labels and subtracting proves the stated
difference-label congruence. This uses the same torsion
removal as the 50-variable proof. All input-nonunit primes
are still accounted for by the same height discard bound.
Consequently the 50-route's strictly positive margin
20309/199400 suffices unchanged for soundness.

Completeness requires a distinct check. At a selected prime
of depth \(\mu=1\), the successful slot of the true family
has errors of depth at least three and products of depth
at least four. Thus W_* is integral there, even though
the last linear term need not be strictly positive.
The opposite reciprocal products are units by the retained
preparation, so the other slot is a pole: their valuations
are -2 and -4, and the two odd terms cannot cancel a
negative minimum (the unit-input lemma applies).
The shifted norm/trace gives \(v_p(D_g)\ge0\);
therefore \(v_p(D_s)\ge1\), \(v_p(\alpha)=1\),
and the actual pole input has valuation one.

At foreign odd positive valuations \(j=v_p(c)>0\),
the stronger normalizer handles every D_g, without requiring
W_* to reduce to one: the odd valuation \(-j\) of u
cannot cancel the even valuation of D_s^2. Hence
\(v_p(\alpha)\le-j<0\) and \(t_0\) is a unit, giving a
positive odd valuation of the actual pole input.
The other-prime and fixed-place preparations remain exactly
as in the 50-variable proof, since \(W_*\to1\) as c tends
to zero with bounded point tests, and \(D_g=O(c^2)\)
there. The real preparation ensures a nonzero trace;
the selected prime gives nonzero alpha and t_0.
At even valuations of u the pole input has even valuation,
outside the fixed exception seven, which is separately
prepared. The resulting real range, dyadic squareclass
and square denominator meet the same BB hypothesis.
The zero-input canonical fiber has zero raw tests, W_*=1
and the same prepared input. Thus this is a complete arithmetic
detector within the inherited ordinary-abc construction.

For reproduction at the equation level, keep the 50-route's
hyperbolic comparison registers P,Q, so
\(PQ=uC^4-c\bar I^4\).
Delete the field register L=cJ and its two defining rows,
replace the detector equation by
\[
 uW_s=u^2+c^2PQ+J+c^2\bar K',\qquad W_s=uW_*,
\]
where the raw products J and K' are the quadratic expressions
in the affine-reference chart of the 50-route. Add alpha
and replace its reciprocal gate as above. This is a complete
system with 49 coordinates, but the new detector row has
degree four, not two. Squaring all rows gives at most degree
eight, not a quartic. It does not supersede the 50-variable
quartic or the 11-variable unrestricted-degree route.
The open problem is absorbing the unequal powers into the
point and comparison charts, and the stronger normalizer
into an existing rational register, while retaining quadratic
rows. The simultaneous linearization is proved at the
arithmetic level; a 48-variable quadratic compilation is not.

## 5. Finite verification and scope

Run node check.js and node check_dual_linear.js in this directory.
The first reconstructs the two general tables and all coefficient
profiles from pinned projective parents, and compares the fixed
decimal literal. The second checks the two exact division-polynomial
fixtures, 401408 unit-input valuation profiles, 764694 actual-
multiplication foreign-prime profiles, and 10001 depth inequalities.
These verifier functions were executed in the BigInt tool
environment. The division-polynomial search was also carried out
in Python. The Node file wrappers have not been run as a complete
repository checkout or in hosted CI. These finite tests do not
replace the uniform proofs above or independently establish the
inherited arithmetic suppliers.

No new variable-count record is claimed here. The existing
research counts are 161/175/50. The earlier 175 polynomial
submitted to PR #175 is not modified by this research checkpoint.
