# Projectively optimized modular contacts (26 November 2026)

This continuation retains the variable counts 161 and 175 and all the
arithmetic premises of the preceding reciprocal-depressed-scalar
construction. It changes only the reflected contact locations and their
quadratic evaluation. The new three-contact explicit member has
**C=331^21**, degree four, 147 quadratic residuals, 3196 monomials,
802-bit maximum coefficient height, and **73080 ASCII bytes**.
No ordinary or weak abc assumption is added. The 161-variable
two-contact family remains ineffective; its 21-specialization is an
algebraic fixture, not a certified defining member.

## 1. A projective change before reflection

Use the five-point H4.1 height input in the form of v68
(papers/quartic/quartic229_compact_20261117_v68.tex, equation
height-input). In the old auxiliary variable v its five contacts are
\[
 \Theta_0=\{0,-1/2,-1,1/2399,-32/407\},
 \qquad u=2+1/v.
\]
Instead of reflecting this affine set immediately, change projective
coordinates:
\[
 t=\frac{973v-77}{1632v+32},\qquad
 u=\frac{1127-1568t}{32t+77},\qquad
 t=\frac{1127-77u}{1568+32u}.
\]
The images of the five original contacts, in the displayed order,
are \(-77,23,21,-75,51\), divided by 32. Reflect these images in zero.
Their ten members are distinct and have diameter \(77/16<5\).
The transformation is a genuine projective linear change, with
determinant of absolute value 156800 = \(2^7 5^2 7^2\). In
particular it has good reduction at every prime outside the
exceptional set S of v68.

Let \(S=\{2,3,5,7,11,13,17,37,41,2399\}\).
Factoring the radii and their pairwise sums and differences gives
\[
 \Gamma=S\cup\{19,23\},\qquad J_*=\prod_{p\in\Gamma}p
     =811898089212210<2^{50}.
\]
The same set contains all denominators, all contact differences
and the differences from the reflection midpoint. In the previous
effective chart the corresponding extra primes were 79,89,647,3593.
The new projective change was found by searching bounded rational
fixed points of a projective involution conjugate to t -> -t.
No claim of a globally optimal contact configuration is made.

At \(p\notin\Gamma\), the two five-contact radicals obtained from
\(u(t)\) and \(u(-t)\) are disjoint and their product is exactly
the odd-positive-contact radical M of the ten-point set. This follows
from invertibility of the projective transformation modulo p:
the five primitive homogeneous linear forms for the H4.1 contacts
are identified, up to p-adic units, with the five corresponding
primitive forms for t. In particular the infinity contact is
included. The two five-point images contain no infinity point,
so the same assertion covers negative valuations of t.
All omitted primes have been included in Gamma. On the complement
of the ten contacts the two rational maps are defined and avoid
the four forbidden finite values of u. Also
\[
 h(t)\le h(u(\pm t))+\log1600.
\]
This is the elementary height inequality for the inverse
fractional-linear map, whose largest absolute row sum is 1600.

## 2. Effective contact height and the scalar exponent

Write \(E(M)=\prod_{p\mid M}(1+1/p)\), and let
\[
 c_0=74712001/10^6,\quad C_0=2^{68}3^{16}5^{16}7^4,\quad
 {\cal C}=c_0C_0J_*^2 E(J_*).
\]
The two H4.1 bounds give, by taking their geometric mean exactly
as in v68,
\[
 h(t)\le\log1600+{\cal C}M\sqrt{E(M)}
                    (\log J_*+\tfrac12\log M).
\]
Indeed \(R_+R_-\le J_*^2M\) and
\(E(R_+)E(R_-)\le E(J_*)^2E(M)\), where \(R_\pm\) are the
two H4.1 squarefree level bounds. Apply arithmetic-geometric mean
to the two logarithms. This also covers the midpoint t=0 and M=1.
Exact rational arithmetic gives
\[
 2^{68}<{\cal C}<2^{249}.
\]
For comparison the old \({\cal C}\) had binary logarithm about
299.214, whereas the new one has binary logarithm about 248.999.
The product over primes at most 1000 outside Gamma of \(1+1/p\)
is less than 21/10. The same elementary large-prime estimate as
in v68 thus yields \(E(M)<(21/10)M^{1/6006}\) (a weak inequality
at a vacuous endpoint suffices). We may retain the old coarse
bound \(h(t)\le 2^{304}M(22+\log M/2)^2\): use
\(\log J_*<35,\log1600<8\), \(E(M)\le1+\log M\), and
\((1+x/2)(35+x/2)\le(22+x/2)^2\) for \(x\ge0\).

All extraction calculations of v82 hold outside the new Gamma:
the point equations, the four factors with their distinct
valuation classes, the shared norm gate, the actual pole
arguments, the formal-logarithm estimates, and the fixed
comparison scaling are unchanged. The underlying local comparison
argument requires only good unramified primes and unit contact
separation/midpoint differences. The fixed factor 408/409 has
nonpositive valuation outside S, so 409 need not be added.
Consequently the same divisibilities \(M_j^3\mid a\Delta\)
when \(\Delta\ne0\) and \(M_j\mid J_X\) when \(J_X\ne0\) hold.
Here the notation is that of v82 and the 178-variable proof.
The scalar radical uses its separate unchanged exceptional set
from the depressed scalar proof.

For N=21 the scalar anchor has \(L_N=97\) and
\[
 |a|\ge331^{97}>2^{810},\qquad
 h(u_{\rm scalar})<2^{301}331^{-97}|a|<2^{-509}|a|.
\]
The height estimates of the depressed scalar proof give
\(h(\beta)<|a|/2,\ h(R)<|a|\); the logarithm of its multiplier
is less than 400. Thus the effective weighted abscissa-sum bound
of the 178-variable proof yields \(B_0^2/2<40\sum_j h(t_j)\).

If \(\Delta\ne0\), the same calculation as in that proof,
now with \({\cal C}<2^{249}\) and the additive \(\log1600<8\),
gives
\[
 B_0^2<242{\cal C}\sqrt{21/10}\,
 |a\Delta|^{1/3+1/36036}(\log J_*+\tfrac16\log |a\Delta|).
\]
The additive \(240\log1600\) is absorbed by the two extra units
in the coefficient 242, since \({\cal C}>2^{68}\) and \(J_*>2\).
Using \(|a\Delta|\le14B_0^5\) and the same elementary rational
upper bounds for the constants as in v82, with \(s=\log B_0\),
\[
 e^{(1/3-5/36036)s}<1000\,2^{249}(54+5s/6).
\]
At \(s=810\log2\) the left side divided by \(2^{249}\)
is greater than \(2^{21}(1-2835/36036)\), using
\(\log2<7/10\) and \(e^{-x}\ge1-x\).
This exceeds 526500, the strict upper bound on the right
side divided by \(2^{249}\) at that endpoint. The quotient of
the exponential by the linear factor is increasing for \(s\ge0\).
This excludes \(\Delta\ne0\). With the old coarse bound and
\(h(\beta)<|a|/2\), the input-residual contradiction of the
178-variable proof is then unchanged: \(J_X\ne0\) would give
\(\log B_0<240+|a|\), violating the Lucas lower bound.
Thus the input is integral, by the unchanged half-integral
label and squarefree-denominator argument.

## 3. Integer completeness and quadratic replacement

The old weighted aggregate shifts exceed 13 and 17 on the
canonical integer witnesses, and in the two-contact construction
the single shift exceeds 7. The ten-point diameter is less
than 5, so the required lists of rational positions remain
disjoint. Choose all point labels and shifts before the
simultaneous Gaussian prime supplier. Enlarge its fixed finite
avoidance set to include the nonzero midpoint differences and
all pairwise position differences, as in the parent. No new
prime-pattern assertion is invoked. Each selected prime
occurs simply in its designated contact product and the other
contacts and its midpoint are units. The parent synchronized
comparison depths and local gate calculation then give
positive valuation one of the actual comparison pole input.

At every fixed finite place and at real infinity, with the
already fixed shifts, the new weight has
\(q_j(t_j)\sim(\sum r_i^2/32^2)\lambda^{-2}\),
where \(r_i=77,23,21,75,51\).
The leading coefficient is the same nonzero positive rational
number in all lists. Thus \(q_j\to0\), their ratios tend to
one, and \(R_j=1/(1+q_j)\to1\), exactly the limits used in the
shared-gate and BB-native completeness proof. At a nonselected
prime, the numerator of \(R_j=G(t_j)/t_j^{10}\) is the
product of the selected linear contact primes divided by an
even power of the common slope denominator, and its midpoint
denominator also has even valuation. Equivalently, with a
common square slope denominator clearing the fixed shifts and
radii, the linear factors have exactly their chosen prime
numerators and the factor \(t_j^{10}\) has even valuations.
This is precisely the earlier reflected-contact factorization
with the new rational positions. Multiplication by the
unchanged rational square gate factor preserves even
valuation away from selected and finitely prepared primes.
The latter are handled by the same fixed-place limits.
The old dyadic, seven-adic and real preparation of the actual
BB inputs is therefore retained. The scalar block and its
preparation are unchanged.

The new monic polynomial in the squared argument is
\[
 P(r)=\prod_{k=1}^5(r-r_k^2)
 =r^5-15125r^4+77366218r^3-151547683050r^2
      +98933750608581r-20236648618580625 .
\]
Use \(r=(32t)^2,\ s=r^2,\ w=1/q_j\), and
\[
 d=rs+(1+w)(77366218r-15125s),\quad
 sd+(1+w)(98933750608581r-151547683050s
             -20236648618580625)=0 .
\]
These yield \((1+w)P(r)=wr^5\) exactly. No division by r is
introduced; r=0 forces w=-1 as in the parent chart, and at
r a root of P the relation is impossible since the root is
nonzero. The inherited unit equations guard w. The contact
weight interpretation at consumed primes and the midpoint
boundary are the same as in the previous reflected chart.
Every equation is quadratic with integral coefficients.

In the stored 175 table these four rows use, respectively,
(t,r,s,d,w)=(2,60,61,62,156), (68,69,70,71,157),
(162,167,168,169,158). In the 161 table the stored t
coordinates 2 and 68 are \(u t\), with \(u=x158\) and
\(u^2=x159\) the retained units. The new square row is
\(1024(ut)^2-u^2r=0\); the other three rows have the same
unscaled contact expressions, on (60,61,62,155) and
(69,70,71,156). The other residuals are literally unchanged.
The complete tables, not a partial arithmetic circuit, are
provided here.

## 4. Two-contact family: a larger numerical target, not a defining instance

For the new 161-variable symbolic table the exact byte budget
is now \(1\le N\le285\), with 99875 bytes at N=285 and
100005 bytes at N=286. It has 2846 monomial profiles,
17 parameter-dependent. At N=1 the size is 62664 bytes;
at N=21 it is 65282 bytes. The magnitude of every
nonconstant coefficient profile is nondecreasing for N>=2;
the constant coefficient is positive with positive leading term.
The separate small-N check covers N=1.

The sharper H4.1 estimate in section 2 also considerably relaxes
the sufficient numerical trace-height target. In the notation of
size_budget_and_trace_target.md for the preceding chart, it
suffices to prove on the full allowed domain
\[
 B_0^2\le A(h(R)+h(T))+J,\qquad
 0<A\le 2^{3000},\quad 0\le J\le2^{20000}.
\]
Indeed N=285 gives \(L_N=1285\) and
\(|a|\ge331^{1285}>2^{10280}\) and \(h(R)<|a|\).
Hence \(Ah(R)+J<B_0^2/2\). If \(\Delta\ne0\),
apply \(h(T)\le h(t_0)+h(t_1)\) and the sharp bound
above to \(M_j^3\mid a\Delta\); it gives, with the
same overestimates used for the three-contact calculation,
\[
 e^{(1/3-5/36036)s}<1000\,2^{3249}(54+5s/6).
\]
At \(s=10280\log2\) its left side divided by \(2^{3249}\)
is larger than \(2^{170}\) (since
\(10280(1/3-5/36036)-3249>170\)).
The right side divided by \(2^{3249}\) is less than \(2^{24}\).
Monotonicity excludes the residual. For the input residual use
the old coarse \(2^{304}\) bound and the factor \(A\);
taking logarithms as in the 178-variable argument gives
\(s<4000+|a|\), again contradicting the Lucas lower bound.
For instance the coarse inequality is bounded by
\(e^s<960\,2^{3304} e^{h(\beta)}
(23+(s+h(\beta))/2)^2\), and the displayed conclusion follows
from the same \(\log(1+x)\le x\) calculation.

This is a sufficient **conditional numerical target**.
Neither the numerical trace constants nor a defining
specialization of the two-contact family have been proved.
The 175-variable explicit polynomial is a defining member
under the previously stated arithmetic inputs.

## 5. Reproduction and scope

Run python verify.py from this directory. The independent checker
uses the pinned parent tables, recomputes P, all nine/six contact
rows, the five projective images, the exceptional-prime supports,
the exact H4.1 constants and endpoint inequalities, and the
expanded polynomial. The executed BigInt replay independently
parsed the entire stored 175-variable polynomial back to its
coefficient dictionary, and checked the new numerical constants.
The independent Python checker is provided for reproducibility;
it is not claimed to have been executed by the connector.
The proof of the imported H4.1, point group, prime-pattern and
BB realization assertions is not part of these finite tests.


## 6. Restricted obstruction to another contact-register deletion

For the isolated reflected contact graph, a direct exact quadratic
replacement using only two private helpers is impossible under the
following geometric hypotheses. Work over the algebraic closure of Q;
the two visible coordinates are the physical affine t and w, and
the three or more quadratic equations in t,w and the two helpers
have a component which projects dominantly onto the exact contact
graph (and not dominantly onto the entire (t,w)-plane).

Indeed \(w=G(t)/(t^{10}-G(t))\), where \(G(t)\) is the monic
degree-ten split contact polynomial with no root at zero.
The numerator and denominator are coprime and the denominator
has degree less than ten. Hence \(\mathbf Q(t)/\mathbf Q(w)\)
has degree ten (equivalently the equation
\((1+w)G(t)=w t^{10}\) is irreducible over \(\mathbf Q(w)\)).
After fixing generic w, a component in affine three-space
(t and the two helpers) defined by quadratic equations has
degree at most eight: intersect successively with quadrics
until its codimension is reached, or use the usual degree
bound for components of an intersection of quadrics.
The projection to the t-line cannot have ten distinct
points on the generic graph, since a linear projection
does not increase degree. More directly, apply the bound
to the union of the generic-fibre components arising from
the one dominant component of the original system: the
ten conjugate t-values all occur, and each contributes
at least one component of positive degree. The corresponding
component of the original system has degree at most
\(2^{4-\dim V}\le8\), and its intersection with a generic
w-hyperplane has degree at most eight. This contradiction
proves the restricted assertion.

This is **not** a lower bound for general quartic definitions or even
for charts required to be correct only on rational points. It excludes
the exact, geometrically dominant, isolated two-helper re-encoding of
the same graph. A smaller construction can still use a different
arithmetic weight, an algebraic covering visible only on rational
points, or sharing with the other detector/point equations. In
particular it explains why the contact-configuration search improves
the numerical constant rather than by itself saving a private helper.
