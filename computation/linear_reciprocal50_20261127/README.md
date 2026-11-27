# A linear reciprocal term: ordinary-abc quartic in 50 variables

**Theorem.** Under exactly the retained arithmetic premises of the
[denominator-sensitive 52-variable construction](../denominator_radical52_20261125/README.md),
including ordinary rational abc, the sum of the 40 integral quadratic
residuals in [quadrics.json](quadrics.json) has rational input projection
Z for every sufficiently large fixed positive integer B congruent to
1 modulo 8. There are **50 rational coordinates including the input**.
The sufficient defining cutoff remains ineffective. The polynomial has
exact degree four and content one, with 1022 coordinate monomials
and 1026 parameter-separated terms.

This is a new conditional defining-variable bound, not merely a
compression of an isolated point chart. The proof deliberately does
not try to establish local integrality at all consumed primes.
At primes where X is a unit, an elliptic valuation identity permits
one of the two reciprocal-product terms to be linear, rather than
quadratic, in the physical detector. The strengthened p^2 comparison
then pays for discarding the other primes in the height estimate.
Integer completeness at foreign odd valuation primes must be checked
separately, and is proved below.

The original translated-secant/reference charts and hyperbolic
comparison packing are from the v65/v78 constructions (including
Gabe Conant's supplied notes with Astra 6.2). This note uses the
previous joint-reciprocal chart as a starting point, changes the
detector, and uses a different affine reference basis. It does
not introduce any further arithmetic hypothesis beyond the
52-variable parent, nor does it transfer to the no-abc routes here.

## 1. Complete joint quadratic chart

Work over K=Q(rho), rho^2=2, and put
\[
 a=1+\rho,\quad b=4-2\rho,\quad
 \delta=a-b^2=-23+17\rho,\quad D=a\delta=11-6\rho.
\]
The curve is E:y^2=x^3-Dx, with translating point R0=(a,ab).
Let f=1/x and let S_Q=y(Q)/x(Q) at a finite nonzero abscissa.

Use three reference field coordinates S,T,A and the affine expressions
\[
 B_r=A+S+T,\qquad E_r=-A-T-b,\qquad V_r=S+A+b.
\]
Require
\[
 AB_r=a,\qquad E_rV_r=\delta .
\]
All four expressions A,B_r,E_r,V_r are nonzero. Put l=A/a,
w=B_r/a, k=1/V_r=E_r/\delta. The two equations recover precisely
\[
 a l w=1,\qquad V_r(V_r-a(l+w)-2b)=\delta,
\]
since V_r-A-B_r-2b=E_r. Conversely these identities recover the
new reference chart using the affine formulas
S=V_r-b-al, T=aw-V_r+b, A=al. Thus the complete v40/v65
reference theorem applies on its original four-point complement.
In particular f(H)=l/V_r, f(H-R0)=w/V_r, S=S_H,
T=S_(H-R0). No division by a possibly zero reference coordinate
is needed in a quadratic row.

For X nonzero, use the original v65 translated-secant variables
s=X S_U, t=X S_V, F=X^2 f(U), G=X^2 f(V), h,d,
with p=h+s+t. Instead of F,G store Y=AF, Z=B_r G.
The four field quadrics and half-trace row are
\[
 \begin{aligned}
 A d&=pY,& B_r d&=hZ,\\
 \delta(B_rY+AZ)&=(s-t)h-t^2,&
 X_4&=d(s-t)-\delta YZ,\\
 h_0&=\operatorname{Re}(hp),& X_4&=X^4 .
 \end{aligned}
\]
X_4 is the existing power register, with X_2=X^2 and X_4=X_2^2.
The equivalence to the original chart follows by substituting
F=Y/A=B_rY/a and G=Z/B_r=AZ/a. Consequently it covers exactly
the original ordered distinct finite point pairs with nonzero
abscissas, including tangencies, zero ordinates, and all finite
two-torsion differences. The scaled difference trace remains
\[
 T_{\rm sc}=2h_0=X^2\operatorname{Tr}x(U-V).
\]
In particular this output is fixed before the contact primes on
the canonical multiplication family.

The four physical tests are
\[
 C=s-S,\qquad I=t-T,\qquad
 J=f(H)F=E_rY/D,\qquad K'=f(H-R_0)G=E_rZ/D.
\]
The two reciprocal products are not stored as separate field
coordinates. Retain the single field register L=cJ, where u=1/c.
Its definition
\[
 D uL=E_rY
\]
is quadratic. This is the crucial replacement for the two field
registers k_s=ck and L_s=cJ+conj(K') of the earlier joint packing.
Retain the hyperbolic comparison registers
\[
 P+cQ=2C^2,\qquad uP-Q=2\overline I^{\,2}.
\]
As cu=1, these are exactly
P=C^2+c bar(I)^2 and Q=u C^2-bar(I)^2.
Consequently PQ=u C^4-c bar(I)^4.

Define the **new physical detector**
\[
 W=1+cC^4-c^3\overline I^{\,4}+c^4J^2+c^2\overline{K'} .
\]
The last term is intentionally linear in the reciprocal product;
it is not a square and no such assertion is made.
With the existing register W_s=uW, its literal defining field row is
\[
 49(uW_s-u^2-PQ-L^2)-D\,\overline{E_rZ}=0 .
\]
Indeed Nm(D)=49, so D/49=1/bar(D), and division by 49
recovers uW_s=u^2+PQ+L^2+bar(K'). Multiplying by c^2
recovers exactly the displayed W. All monomials in the stored
equation have coordinate degree at most two.

The table multiplies the secant row by the nonzero field
constant 23+17rho, using delta(23+17rho)=49. It then clears
constant coefficient content separately in each rational component.
These operations do not change the common rational zero set.
The three reference coordinates S,T,A were selected to make the
comparison squares sparse; all reference maps used above are affine.

## 2. Unchanged scalar, norm and pole equations

Retain the 52-variable parent's contact scalar
\[
 M=B+8(X^8+T_{\rm sc}^2),\quad a_{\rm ct}=M+16,\quad
 x=a_{\rm ct}-z,\quad y=a_{\rm ct}+z,
\]
\[
 G_{\rm ct}(t)=\prod_{r\in\{1,4,7,8\}}(t^2-r^2),\quad
 H_y=G_{\rm ct}(y)/y^4,\quad
 c=H_y/G_{\rm ct}(x)+3/H_y,\qquad u=1/c.
\]
Its seven contact-register equations and all their automatic guards
are exactly those of the 52-coordinate parent. In particular M>=B>0,
both contact polynomials are nonzero, y!=0, and c,u are nonzero.

Use the same norm equation
\[
 D_g\operatorname{Tr}W=\operatorname{Nm}(W-1),\qquad D_s=uD_g.
\]
It has nonzero trace denominator: trace zero would force
Nm(W-1)=0, hence W=1 in the field K, a contradiction. The
normalizer and pole-input register are
\[
 (t_0-1)(u+D_s)=1,\qquad cK_s=t_0^2 .
\]
Here K_s is the old rational pole register, unrelated to the
deleted field register k_s. Keep the five old pole rows
\[
 p'^2=cP_s,\quad e_s^2+7P_s=u^2,\quad
 U_sV_s=e_s(K_s-7),\quad q^2=cQ_s,\quad
 U_s^2-V_s^2=7Q_s .
\]
On putting e=ce_s, U'=cU_s, V'=cV_s these give
\[
 e^2+7cp'^2=1,\quad U'V'=e(t_0^2-7c),\quad
 U'^2-V'^2=7cq^2.
\]
For t_0 nonzero these are precisely the native BB pole equations
at the physical input b_{\rm pole}=7c/t_0^2, via
p=t_0 p', U=U'/t_0, V=V'/t_0, with e,q unchanged.

For clarity recall the gate implication, which does not depend on
the detailed definition of W. At a good retained prime with
mu=v_p(u)>0 odd, the t_0=0 fiber of the three cleared pole
equations is impossible: the first makes e a unit, the second
gives v(U'V')=-mu odd, and the third has unequal valuation
parities on its two sides (including the possible zero q).
Thus t_0!=0. The native negative-odd obstruction forces
v_p(7c/t_0^2)>0, so v_p(t_0)<-mu/2. The reciprocal normalizer
then yields v_p(D_g)>-mu/2. If both slots of W have negative
valuation, the numerator of D_g has the sum of the two valuations
and its denominator has valuation at least their minimum. Hence
v_p(D_g)<=max(v(W),v(bar W)). If one slot is integral use it
instead. In either case there is a slot satisfying
\[
                         v(W)>-\mu/2.                 \tag{A}
\]
This also works at inert good primes with the repeated valuation.
The proof only uses the old pole and norm equations, so it is
valid for this modified W and arbitrary rational witnesses.

## 3. Valuation identity and noncancellation at unit inputs

Fix a good unramified odd prime outside the parent's exceptional
set, enlarged if necessary by p<=5. Normalize v(p)=1.
For a finite nonzero-abscissa point Q define d_Q=|v(f(Q))|/2.
Then d_Q is a nonnegative integer, and there is a sign
epsilon_Q in {+1,-1} with v(f(Q))=2 epsilon_Q d_Q.
If d_Q>0, v(S_Q)=-d_Q; if d_Q=0, v(S_Q)>=0, including
infinity for a zero ordinate. This follows from the curve equation:
a negative abscissa valuation gives the formal branch at O,
a positive one gives the branch at (0,0), and a unit abscissa
gives an integral ordinate. In particular the positive reciprocal
valuation branch is exactly the formal branch.

**Unit-input lemma.** Let X be a p-adic unit. For any two such
points Q,R put B'=X^2 f(Q)f(R), E'=X S_R-S_Q.
If v(B') is 2 modulo 4, the depths d_Q,d_R have different
parity, since v(B')=2(epsilon_Q d_Q+epsilon_R d_R).
They are therefore different. The error has the unique negative
minimum
\[
 v(E')=-\max(d_Q,d_R),\qquad
 4v(E')\le-|v(B')|-2.                                \tag{B}
\]
The latter follows from d_Q+d_R<=2max(d_Q,d_R)-1.
If v(E')>0 and v(B')>0 instead, both depths are equal and positive,
and both signs are positive. In that case both points are formal
with the same depth d and v(B')=4d.

At a consumed prime v(c)=-mu with mu positive odd, discard primes
where v_p(X)!=0 for the moment. In any slot the four nonconstant
terms of W have valuations
\[
 -\mu+4v(C),\quad -3\mu+4v(\bar I),\quad
 -4\mu+2v(J),\quad -2\mu+v(\overline{K'}).
\]
All finite reciprocal-product valuations are even.
The first two displayed valuations are odd, distinct modulo four;
the last two are even. The only possible finite equality between
different nonconstant terms is between the two even terms.
Such an equality forces v(bar(K'))=2 modulo 4.
Apply (B) at the conjugate slot to H-R0,V. Then
\[
 -3\mu+4v(\bar I)
 \le -3\mu-|v(\overline{K'})|-2
 < -2\mu+v(\overline{K'}).
\]
Hence the tied even terms cannot realize the minimum. All zero
terms may simply be omitted. Whenever the minimum is negative,
it is unique and cannot cancel, including with the constant 1.

Consequently (A) implies in its successful slot
\[
 v(C)>\mu/8,\quad v(\bar I)>5\mu/8,\quad
 v(J)>7\mu/4,\quad v(\overline{K'})>3\mu/2.             \tag{C}
\]
The unit-input lemma puts H,U in their formal groups at that
slot and H-R0,V in their formal groups at the conjugate slot,
with equal reference/numerator depths in each pair. Call these
depths d_+,d_-. They satisfy
\[
 d_+\ge 1+\lfloor7\mu/16\rfloor,\qquad
 d_-\ge 1+\lfloor3\mu/8\rfloor .
\]
The parameter z_E=-x/y gives z_E(U)/z_E(H)=S_H/S_U.
Thus its difference from X has valuation at least v(C)+d_+.
The alternate ratio analogously has precision v(bar I)+d_-.

At good p>5, the invariant differential on the short curve has
integral formal coefficients with first nonconstant term of degree
four. The formal logarithm therefore agrees with z_E to relative
order at least 4d at positive integral depth d: integration of
the degree n-1 coefficient loses at most v_p(n), and
(n-1)d-v_p(n)>=4d for n>=5. Both parameters have the same depth,
so replacing them by logarithms loses at most the corresponding
relative-error bound 4d (i.e. the ratio still has precision the
minimum of that bound and its original precision).

Let h_* be the integer free label of H relative to R0, and m
that of U-V. Doubling the formal relations kills global two-torsion
and identifies the two logarithmic ratios with the ratios of their
integer free labels. The reference labels are h_* and h_*-1;
they are nonzero on the corresponding nonzero formal branches.
Multiply each ratio estimate by its integral reference label
and subtract, obtaining
\[
 v_p(m-X)\ge
 e(\mu):=2+\lfloor\mu/8\rfloor+\lfloor7\mu/16\rfloor\ge2.  \tag{D}
\]
For the bound, the primary ratio error has precision at least
e(mu) by (C); the alternate one has precision at least
2+floor(5mu/8)+floor(3mu/8)=mu+1. Both 4d_+,4d_-
are >=e(mu): for mu>=3 this follows from e(mu)<=2+9mu/16
and 4d_->3mu/2, 4d_+>7mu/4, and mu=1 is immediate.
Also mu+1>=e(mu) for odd mu>=3 and for mu=1.

No conclusion about local integrality or noncancellation is
needed or asserted for arbitrary witnesses with v_p(X)!=0.
The next section accounts for all these primes, rather than
silently removing them from the contact height theorem.

## 4. Strict height contradiction after discarding nonunits

Retain exactly the denominator-sensitive contact inequality of
the 52-variable parent (its Sections 2-3, epsilon=1/100):
\[
 R_u=\log r^+_{\mathrm{odd},S}(u)
 \ge (347/200)H-(3/4)h(X)-O(1),\qquad H=h(M).
\]
Here the squarefree radical includes every prime outside the fixed
set S with positive odd valuation of u. The inherited signed
mixed-power abc estimate with kappa=1001/1000 gives
\[
 h(X)\le (501/997)H+O(1).
\]
The constants are uniform in B and all rational witnesses; in
particular the lower bound supplies consumed primes for large B.

Suppose X!=0 and X!=m, and write X=N/D_0 in lowest terms,
D_0>0. Consumed primes at which X is not a unit divide |N|D_0.
Their total logarithmic mass is at most log|N|+log D_0<=2h(X).
All remaining consumed primes, by (D), have their squares dividing
the nonzero integer m D_0-N. Their mass is therefore at most
(1/2)log|m D_0-N|. In full,
\[
 R_u\le \tfrac52 h(X)+\tfrac12\log(1+|m|).
\]
This bound includes denominator primes of X, which the previous
detectors had to exclude individually. Combining with the lower
bound gives
\[
 \left(\frac{347}{200}-\frac{13}{4}\frac{501}{997}\right)H
 \le \tfrac12\log(1+|m|)+O(1),\qquad
 \frac{20309}{199400}>0 .
\]
This strict margin is sufficient, although smaller than the margin
in the more expensive joint-reciprocal detector.

The original all-point trace-index bound is unchanged:
m^2<=C_0(h(T_sc)+2h(X))+J_0. With M=B+8(X^8+T_sc^2),
the parent argument gives 2h(T_sc)<=H+8h(X)+O(1);
the fixed translation and factor eight affect this only by an
absolute constant since the sum is nonnegative. Thus m^2=O(H+1).
The strict inequality above now bounds H independently of B
(because H cannot be bounded above by a fixed multiple of log(H+1)
on an unbounded sequence). But H>=log B. For all sufficiently
large fixed B this is impossible. Hence X=0 or X=m in Z.

## 5. Integer completeness, including every foreign odd prime

The point chart is exactly equivalent to the old one, and the
height scalar and fixed contact positions depend on the same
difference trace. For a nonzero integer n use the parent's
U=[n]H, V=[n](H-R0), so U-V=[n]R0. Fix its trace, M and contact
positions before selecting primes. Use the same real and finite
neighborhoods and compatible index refinement of the retained
Gaussian prime-pattern theorem, excluding primes dividing n.
All actual points may be chosen finite with nonzero abscissas.

At each freshly selected prime v(c)=-1, the successful slot
has v(C),v(bar I)>=3, v(J),v(bar(K'))>=4, exactly as in the
parent. These bounds make every nonconstant term of the new W
positive in that slot (the two reciprocal terms have depth at
least four and two respectively). We also need control of the
other slot, and of primes not in the selected list.

**Actual-multiplication lemma.** At a good unramified odd prime,
take Q finite nontorsion with nonzero abscissa and R=[n]Q, n!=0.
Put e=v_p(n)>=0 and use B'=n^2 f(Q)f(R), E'=n S_R-S_Q.
The following implications hold:
\[
 \begin{array}{ll}
 v(B')=-2j,\ j>0\text{ odd}&\Longrightarrow v(E')=-j,\\
 v(B')=2,\ e=0&\Longrightarrow v(E')=-1.
 \end{array}                                           \tag{E}
\]
Proof: if Q is formal of depth d, then R is formal of depth
d+e, so v(B')=4(d+e). If Q reduces to the zero-abscissa
two-torsion, translate it by that torsion, getting a formal
point of depth d. R is formal for even n and near that same
torsion for odd n; the product valuation is respectively
4e or -4d. Neither case gives either valuation in (E).
The remaining case is a unit abscissa of Q, so S_Q is integral.
For v(B')=-2j the reciprocal of R has valuation -2(e+j),
and therefore v(n S_R)=-j. For v(B')=2 with e=0 the
reciprocal of R has valuation 2, so v(n S_R)=-1.
In both cases the integral S_Q cannot cancel it. The formal
depth computation uses the standard good-prime formal logarithm
isometry. This proves (E) without a prime-distribution assumption.

At the selected primes n is a unit, so Section 3 proves that
any negative minimum is unique also at the other slot. If W
is integral there, the odd terms cannot have valuation zero.
The J term has valuation zero only if v(J)=2, and the K'
term only if v(bar(K'))=2. The corresponding instance of (E)
would force v(C)=-1 or v(bar I)=-1, making its odd term
negative, a contradiction. Thus every integral slot has
W congruent to 1. If the other slot is a pole, the norm
of W-1 and the trace cancel its pole order; if it is integral,
the trace is 2 modulo the prime. In either case v_p(D_g)>0.
The reciprocal normalizer therefore gives the actual pole input
b_pole valuation one, as required.

Now let a foreign good prime have v(c)=j>0 odd. The odd
nonconstant term valuations are j+4v(C) and 3j+4v(bar I)
and are distinct modulo four. The even terms have valuations
4j+2v(J) and 2j+v(bar(K')). If these even terms tie at
a nonpositive value, v(bar(K'))<=-2j and v(bar(K'))=2 mod 4.
Apply the first implication of (E) to get v(bar I)=v(bar(K'))/2.
Then 3j+4v(bar I)=3j+2v(bar(K'))<2j+v(bar(K')), so their
tie cannot be minimal. Every negative minimum is unique.
If W is integral, neither even term can have valuation zero:
a zero J term would give v(J)=-2j and v(C)=-j, making the
first odd term -3j; a zero K' term would give v(bar I)=-j
and its odd term -j. Both contradict integrality. Thus every
integral slot is 1 modulo the prime, also at these foreign
places where n may be divisible by p.

As in the 53-variable reciprocal-gate proof,
\[
 1+D_g=(\operatorname{Nm}W+1)/\operatorname{Tr}W.
\]
If both slots are integral the ratio is a unit (both residues
are 1 and p is odd). If exactly one is a pole, the numerator
and denominator have its valuation. If both are poles, the
ratio has valuation at most the larger pole valuation, which
is negative. Thus v_p(1+D_g)<=0 and the ratio is nonzero.
It follows that v_p(u(1+D_g))<0, so the reciprocal normalizer
t_0=1+1/[u(1+D_g)] is a unit, and the actual b_pole has
positive valuation. This proves the required foreign odd
denominator condition, not just the selected-prime condition.

At the fixed preparation places and positive real infinity in
the slope, the original contact scalar tends to zero and all
physical point tests stay bounded by the parent's ordered
preparation. The new W has W-1=O(c), D_g=O(c^2); hence
t_0 approaches 1, and b_pole is asymptotic to 7c. The
parent's contact factorization states that no other positive
odd v_p(u) occur outside the fixed places, and negative odd
v_p(u) have just been handled. At every even valuation of u
the valuation of b_pole is even outside seven. The fixed
preparation gives positive seven-adic valuation, dyadic
squareclass seven and depth at least four, and real
0<b_pole<1. Thus b_pole has a square reduced denominator
and satisfies precisely the prepared BB-native hypothesis.
Invoke the retained theorem for this actual input, after all
point and contact choices, to fill the five pole witnesses.

The zero-input witness is also unchanged: H=2R0, s=S,t=T,
F=G=Y=Z=d=0, h=t^2/(s-t). The denominator is nonzero
(Nm(S-T)=7199/328 by the original v65 computation). Every raw
test vanishes, L=P=Q=0 and W=1. The same fixed trace and
contact preparation give the actual prepared pole and its
witnesses, exactly as above. No factor X was multiplied into
the defining polynomial.

## 6. Complete coefficient census, exact replay and scope

The field components in basis 1,rho occupy the following
coordinates:
\[
\begin{array}{c|l}
1&X\\
2:3,\ 4:5,\ 6:7&S,T,A\\
8&h_0\\
9:10,\ 11:12,\ 13:14,\ 15:16,\ 17:18,\ 19:20&s,t,Y,Z,h,d\\
21:22,\ 23:24,\ 25:26&L,P,Q\\
27,28&X_2,X_4\\
29:30&W_s\\
31,32&t_0,K_s\\
33,34,35,36,37,38,39&e_s,U_s,p',V_s,q,P_s,Q_s\\
40,41,42&D_s,c,u\\
43,44&M,z\\
45,46,47,48,49,50&r_x,r_y,s_x,s_y,F_{\rm ct},H_y
\end{array}
\]
The last 17 rational rows are the 52-variable parent tail
with indices shifted after deleting x21,x22. Its two power
rows are also retained. The new 23-row prefix contains the
four reference rows, eight pair rows, one half-trace row,
two primary reciprocal rows, two power rows, four hyperbolic
comparison rows and two detector rows. This makes 40 integral
quadratic residuals. The coefficient of X^4 is exactly one,
which proves exact degree four and integer content one
for every specialization.

The complete parametric [expanded coefficient list](polynomial.json)
has 1026 parameter-separated terms and 1022 coordinate monomial
profiles. At B=1 there are exactly 1022 nonzero monomials, with
maximum coefficient 5531402752 and **16134 ASCII bytes** in
[expanded-B1.txt](expanded-B1.txt). This is an algebraic fixture,
not a certified defining specialization. It is below 100 kB
but the defining threshold is still ineffective. The count
50 supersedes 52 in the variable-count priority; the earlier
52-variable presentation has smaller support and is retained.

Finite evidence: a standalone Python/SymPy checker independently
reconstructed every semantic row and expanded the full sum of
squares, and its four output files were compared by exact Git
blob identity with the BigInt reconstruction from the pinned
52-variable parent. The independently executed elliptic fixtures
and valuation profile tests are recorded in verification.json.
The point checks include 32 references, 2244 ordered pair/scale
fixtures, 64 tangencies, 196 finite torsion differences (68 with
zero difference abscissa), and the canonical zero-input fiber.
The local profile checks include 2286144 unit-input profiles,
1843200 foreign positive-odd profiles, 137641 selected-prime
profiles and 10001 odd depths. These finite tests supplement the
universal proofs in Sections 3-5; they do not establish the
retained group, trace-height, abc, prime-pattern or BB suppliers.

Reproduce the exact coefficient compilation from the repository
checkout using

    node computation/linear_reciprocal50_20261127/check.js

The independent Python verifier uses SymPy 1.14.0. The affine-basis
search examined 66 admissible reference/slope/point scaling
combinations (the initial count-50 chart had 1128 monomials);
nonzero constant field row multipliers further reduced the
chosen support to 1022. No global complexity minimum is claimed.

Pinned parent: commit 6864691d536057574be873667936610da6a4ea99,
computation/denominator_radical52_20261125/quadrics.json, Git blob
8c9ba17ddfa6f4e2900c9d65c30ea24a1d71c026. Principal arithmetic
references in that snapshot: the 52-variable README Sections 1-4;
reciprocal_gate53_20261124/README.md Sections 1-4;
papers/quartic_existence/quartic_abc68_20261117_v65.tex (reference,
pair and formal extraction); paired_contact56_20261119_v81.tex
(integer witnesses and dyadic trace); and
papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex.
The BB pole-realization theorem is retained from the 52/53 route,
not independently reproved or reviewed here.

Next: investigate whether a second linear reciprocal term admits
a comparably strong noncancellation principle, and whether the
unit-input/discard-budget method can reduce the contact circuit
or transfer to the no-abc comparisons. Such transfers are not
established in this checkpoint.
