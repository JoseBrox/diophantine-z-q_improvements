# Selective input/Lucas contacts: 22 and 24 total rational coordinates

## Result and scope

Combining the simultaneous mixed-class pole theorem in [README.md](README.md)
with a selective common-numerator construction gives a 22-variable general
unrestricted-degree family and a 24-variable explicitly specified family.
No additional abc assumption is used. The arithmetic premises are the
original v78/v88 general premises, including the full all-sign finite
prime-pattern theorem (as explicitly stated in Section 2 of
[arithmetic_dependencies_20261108_v8.tex](../../arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex)).
The other inputs, including the analytic rank criterion in the mixed-class
theorem and the BB converse for the remaining private pole, are the same
as in README.md.

The general sufficient coefficient threshold remains ineffective; the
specified route can use the concrete integer \(L=171033187\). The source
is an exact finite coefficient prescription; no new degree/expanded
coefficient bound is claimed.

This transfer removes an entire auxiliary elliptic-point block.
It is not obtained by treating a free coordinate as a finite root.
The technique of sharing a numerator with disjoint prime tests is from
the project's prior undecidability construction
[v103](../../../undecidability/abc_common_numerator_v103/common_numerator.tex)
and [v147](../../../undecidability/selective_common_numerator_v147/README.md).
Here the required new separation is between the single input comparison
and the *simultaneous* Lucas-growth comparison, not between the three
individual integer labels occurring in the Lucas residual.

## 1. Fixed contact partition

Retain the substituted input \(X\), scalar \(\rho=(7/9)^2\rho_*\),
root labels and scales of README.md. Thus \(X=\prod_{j=0}^{465}(X_0-j)\)
and \(\tau=X^2+1\). The fixed exponent is odd and belongs to the
progression in that note. There are two or three source arguments
\(t_j=\alpha_j\lambda\), with the original \(\alpha_0=1\) and original
unsquared positive shifts \(1+\rho T_j^2\).

Use two ten-contact families per argument, labelled \(I,G\):
\[
 \begin{gathered}
 s_0=0,\quad s_1=15+67/7^2,\quad s_2=30+67/7^4,\\
 \Theta_{j,I}=\Theta_0+s_j,\qquad
 \Theta_{j,G}=\Theta_0+s_j+4,\qquad
 \Theta_0=(2+\Theta)\cup(4+\Theta),\\
 \Theta=\{0,-1/2,-1,1/2399,-32/407\}.
 \end{gathered}
\]
Set
\[
 G_{j,g}(t)=\prod_{\theta\in\Theta_{j,g}}(t-\theta),\quad
 \delta_j=t_j+j+1,\quad
 R_j=\frac{G_{j,I}(t_j)G_{j,G}(t_j)}{\delta_j^{20}},\quad Q_j=\rho R_j .
\]
Guard both polynomials, \(\delta_j\), and the source nonzero denominators.
Each family is just a fixed translation of the original ten-contact
family. The twenty roots in any one scale are distinct and positive.
The first two twenty-contact-and-pole sets are disjoint modulo 67 and
contain no zero there (exact residue check in verify_selective.py).
All new fixed contact/pole constants, their denominators and their
nonzero differences contribute only a fixed exceptional set.
As before keep the forced prime 67 separately, even if it is omitted
from the height radicals.

At a good prime, if \(t_j\) has negative valuation, \(R_j\) is a
unit by its equal numerator and denominator degrees. If it is
integral, at most one of the twenty contact factors and the pole can
vanish modulo the prime. In particular a positive odd valuation of
\(R_j\) means that precisely one family \(g\) has a positive odd
contact valuation, equal to \(v_p(R_j)\), and \(\delta_j\) is a unit.
Define \(M_{j,g}\) to be the product of the nonexceptional primes
with positive odd valuation of \(G_{j,g}(t_j)/\delta_j^{10}\).
These are the primes of that family's ten-contact radical, including
the same balanced-denominator convention as the original.

## 2. Eight point blocks and a valuation-controlled comparison product

Use the original four square-abscissa root charts \(A,S,T,Z\) with
nonzero integer labels \(n,a,t,b\), respectively. Retain the original
reference \(H=U_0\), auxiliary \(U_2,U_3\), but replace the two old
auxiliary points \(U_1,U_4\) by a single point \(U\) in the same full
auxiliary chart. In all functions substitute \(U_1=U_4=U\) literally.
The four root differences are still
\(V_i=U_i-Q_i\) with \(Q_1=A,Q_2=S,Q_3=T,Q_4=Z\);
also \(V_0=H-P\).
Use the original functions \(f(Q)=1/x(Q)\), \(z(Q)=-x(Q)/y(Q)\),
\(L_i=z(U_i)/z(H)\) and \(L_i'=\sigma(z(V_i)/z(V_0))\),
where \(\sigma\) is the nontrivial quadratic conjugation.

Take input-family raw tests
\[
 \mathcal C_I=(f(H),\sigma f(V_0),f(U),\sigma f(V_1),
                       L_1-L'_1,L_1-\tau),
\]
all of required order one. Take growth-family raw tests
\[
 \mathcal C_G=(f(H),\sigma f(V_0),
   (f(U_i),\sigma f(V_i),L_i-L'_i)_{i=2,3,4},
   \mathcal F(L_2,L_3,L_4)),
\]
where \(\mathcal F(u,v,w)=v^2-u(u-2)vw+(u-2)^2w^2-1\).
The reciprocal tests have order one; all the cross differences and
the Lucas residual in \(\mathcal C_G\) have order three. Retain every
original point, difference and local-parameter guard. Duplicate
reference tests in the two families need not be optimized away.

Write
\[
 \eta_{j,g}=\frac{G_{j,g'}(t_j)^8}
                   {G_{j,I}(t_j)^8+G_{j,G}(t_j)^8},\qquad
 B_{j,C}=\frac{(C/\delta_j)^2}{1+Q_j(C/\delta_j)^2},
 \qquad
 k(C)=\begin{cases}1&\text{order-one test},\\6&\text{order-three test}.\end{cases}
\]
Here \(g'\) denotes the other family. These are rational functions,
not new ordinary coordinates. Include all new denominators in the
selected-character nonzero guard. Replace the old comparison factors
of \(W_j\) by
\[
 \prod_{g\in\{I,G\}}\prod_{C\in\mathcal C_g}
          (1+Q_j^{\,1-2k(C)}\eta_{j,g}^2 B_{j,C}^2).
\]
Keep the exact original v78/v88 scalar factors, replacing \(R_j,Q_j\)
by the new functions. For example in the v19 notation these are
\((1+a_{j,l}^2)\), with the same raw rational normalizations and
orders from v78; do not modify their scalar-test arguments.
Let \(W_j\) be the product of the six retained scalar factors and
the displayed selective comparison factors. Use
\[
                         e_j=4Q_j/\operatorname{Tr}(W_j^{-1})^2.
\]
Guard the inversions and trace. The first two pole inputs will be
certified by the mixed-class predicate of README.md, the third
independently as before.

## 3. Local soundness, including arbitrary inactive test poles

At an unramified good prime let \(\alpha=v_p(Q_j)\) be odd.
For either slot and any nonzero raw test \(C\), the two summands in
the denominator of \(B_{j,C}\) have distinct valuations. Consequently
\[
       v(B_{j,C})=\max(2v(C/\delta_j),-\alpha).
\]
The nonconstant term of every new factor has odd valuation, if
nonzero, since all other powers are squares. Thus the factor
valuation is its nonpositive minimum with zero; when integral its
residue is 1. Zero raw tests give the factor 1. The retained scalar
factors have exactly the same nonpositive valuation property at an
odd \(\alpha\), by the v78/v88 proof. This suffices for the usual
trace-and-pole extraction: writing \(q_{\max}\) for the larger slot
valuation of \(W_j\), the negative-odd pole exclusion implies
\(\alpha>0,\ q_{\max}>-\alpha/2\). Every factor in the maximizing
slot has valuation greater than \(-\alpha/2\). The original scalar
extraction is therefore unchanged, with the new comparison factors
only contributing nonpositive valuations.

At a positive odd contact prime of \(M_{j,g}\) let
\(\nu=v_p(R_j)>0\) be odd. The selected family has \(\eta_{j,g}\)
a unit and the other has valuation \(8\nu\). If \(v_p(\rho)\) is
even, \(\alpha\) is odd and the preceding argument gives, in one
slot,
\[
       v(B_{j,C})>(k(C)-3/4)\alpha\qquad(C\in\mathcal C_g).
\]
Because \(\alpha>0,\delta_j\) is a unit, this implies \(v(C)>0\),
and in fact \(2v(C)=v(B_{j,C})\). If \(k(C)=6\) then the integral
valuation \(v(C)\) is at least three. Thus the active raw tests
have exactly the local implications in the original v19 formal
comparison proof, with no condition on an inactive numerator
or an inactive difference at this prime. The source index lemma
applies unchanged to the active indices: \(h\) or \(h-1\) is a
unit, the reciprocal tests give the two appropriate formal slots,
and multiplying the congruent truncated ratios by the two reference
indices and subtracting recovers the root label, with precision
one for \(I\) and three for \(G\). This uses the original full
auxiliary chart convention, including its half-integral indices,
and only odd primes.

If the scalar valuation \(v_p(\rho)\) is odd, use the original
scalar-unit argument across the first two scales. For nonintegral
or positive-valuation \(\lambda\), \(R_0\) is a unit, and otherwise
at an odd scalar valuation a nontrivial scale is nonintegral or
has residue 1. In the former case its \(R_j\) is a unit; in the
latter case disjointness of the first two contact/pole residues
gives one unit. The unchanged scalar factors give \(p^3\mid c\).
This also proves the forced-prime bound at 67, with
\(v_{67}(\rho)=L\) and the unchanged scalar-extraction order:
\(v_{67}(c)\ge2L+1\).
The first four scalar factors and the last two ratio factors
are exactly the ones in the original proof, which applies
because the new factors cannot have positive valuation at the
consumed odd prime.

Thus, for the nonzero residuals indicated,
\[
 67^{2L+1}M_\beta^3\mid c,\qquad
 M_{j,G}^3\mid\Delta c,\qquad M_{j,I}\mid Nc ,
\]
where \(N=\operatorname{num}(\tau-n)\), \(\Delta=\mathcal F(a,t,b)\).
It is not necessary for the \(I\) and \(G\) primes to coincide.
Each family separately gives the old modular contact-height bound,
by translating \(t_j\) back to its original ten-contact list.
In the Lucas-residual elimination use the \(G\) family on every
scale; in the input-residual elimination use the \(I\) family on
every scale. The original trace/abscissa height bound still uses
exactly the same four root points, so the proof of Section 5 of
README.md applies with the corresponding enlarged fixed constants.
In particular \(\Delta=0\) is forced *before* using the integer
Lucas growth lower bound, with no relaxation of its integer
hypotheses.

## 4. Simultaneous all-integer completeness

For a fixed integral \(X_0\), choose the scalar neighborhood and
the integer \(c=a-1\) as in README.md, fixing the four nonzero root
labels \(n=\tau,a,t,b\) with \(\Delta=0\). Their 7-integrality is
unchanged. Fix all scales and rational contact positions before
selecting primes. Within each scale the \(I,G\) positions are
distinct (their lists are separated by a real gap). Across scales
the 7-adic negative even leading valuations of \(s_j\) are different,
because all \(\alpha_j\equiv1\bmod49\), hence these positions are
also distinct. Include their differences and all fixed preparation
data in finite avoidance. The prime supplier now supplies twenty
primes per scale with the exact common square-denominator slope
and the prescribed fixed-place divisibility. No extra slope
coordinate is used.

Take \(H=[h]P\) in the original compatible reference progression
and real/finite neighborhoods; add divisibility of \(h\) by every
selected prime as in v19. Keep \(U_2=[ha]P,\ U_3=[ht]P\).
For the shared point \(U=[j_*]P\), choose a separate initial index
\(j_0\) divisible by 64 away from the finitely many forbidden
chart points and fix a modulus preserving its fixed finite-place
and compact real neighborhoods, as in the v103 common-numerator
proof. Take a common preparation modulus \(M_0\) for \(h,j_0\)
including 64 and the real component group order. For a selected
prime \(p_d\) let \(u_d,v_d\) be the divided primary and opposite
annihilators \(d_-(\pi_d)/4,d_+(\pi_d)/4\) from the source.
They annihilate \(P\), which is a double. Assign \(n_d=n\) on
\(I\)-contacts and \(n_d=b\) on \(G\)-contacts. Impose
\[
 j_*\equiv j_0\bmod M_0,\qquad
 j_*\equiv0\bmod u_d,\qquad
 j_*\equiv n_d\bmod v_d,\qquad
 j_*\equiv h n_d\bmod p_d^{L_d}.
\]
The all-sign assertion in the retained prime supplier gives
pairwise coprimality of the opposite orders and their coprimality
with all primary orders. The primary two-parts are 16 and
compatible with \(64\mid j_0\). Every selected prime is coprime to
all the orders by the v19 short-prime-cluster argument, and the
fixed preparation modulus has coprime odd parts as in that source.
Thus all these congruences are simultaneously compatible. Real
recurrence in the prescribed component provides \(U\) in its
already chosen real neighborhood. The exponents \(L_d\) may be
taken arbitrarily large after \(h\) is chosen. Indeed \(j_*-h n_d\)
is divisible by both corresponding reduction annihilators, as
\(h\equiv0\bmod u_d,1\bmod v_d\), and by \(p_d^{L_d}\); the formal
group at the two slots makes the point difference arbitrarily
small. This proves that at each selected \(I\)-prime the active
points have the original local behavior of \(U=[hn]P\), and at
each selected \(G\)-prime that of \(U=[hb]P\). The other growth
numerators are the true multiplication points. The finite real
and local chart guards can all be preserved: the initially chosen
reference and numerator neighborhoods are away from the finitely
many forbidden multiples, and the active required positive
valuations are open conditions at the chosen formal points.

At a selected prime, \(\alpha=\nu=1\), the active reciprocal tests
have valuation at least two and all active difference and residual
tests at least four in the successful slot by the original
formal-logarithm proof (or the just described arbitrary-precision
approximation to that proof). For an active test,
\(v(B_{j,C})=2v(C)\); all active new factors have residue 1.
For an inactive test, even with an arbitrary pole, \(v(B_{j,C})\ge-1\)
and \(v(\eta_{j,g'})=8\). The new nonconstant term then has valuation
at least \(1-12+2(8-1)=3\). Hence the inactive factor has residue 1
as well. At the opposite slot all factors again have inverse residue
0 or 1 by their odd valuation parity. The retained scalar factors
are units congruent to 1 by the original \(p_d\mid h\) preparation,
since the scalar functions involve only \(H,S-P\).
Therefore \(\operatorname{Tr}(W_j^{-1})\) is a unit at every
selected prime of scale \(j\).

At each fixed place and real infinity the old small scalar
neighborhoods are unchanged. The raw comparison tests are bounded
on the chosen independent numerator/reference neighborhoods.
As the slope tends to infinity, \(R_j\to1,\eta_{j,g}\to1/2\),
\(Q_j\to\rho,\delta_j^{-1}\to0\); the new \(B_{j,C}\) tend to zero
and their denominators tend to 1. Thus the same fixed-place
preparation makes \(W_j\) arbitrarily close to 1, and the same
real preparation gives \(0<e_j<1\). At all other primes
the physical weight has even valuation unless it lies in the
fixed scalar support: this follows from the exact twentieth-power
factorization of \(R_j\) with its twenty distinct selected prime
numerators. Division by the trace square does not change that
parity. Hence all \(e_j\) have square reduced denominators and
the dyadic class-seven preparation, including \(v_7(e_j)=3\).
This is the complete denominator check, not merely a local
solubility test.

In the mixed-class argument \(P_j\) is now the product of twenty
selected primes; its prime factors are all type 1, and distinct
scales have mutual quadratic symbols +1 by the same negative even
7-adic difference calculation in README.md. All the hypotheses
of the simultaneous-rank theorem on \(J,P_0,P_1\) remain valid.
Replace each marker menu by its 21 entries
\[
 m_{1,l}=32764985881+lM,\qquad m_{2,l}=4885738625+lM,\qquad
 0\le l\le20,
\]
where \(M,H\) and the fixed markers are those of README.md.
The same congruence checks apply and \(m_{i,l}<H\).
Twenty opposite-list primes forbid at most twenty choices.
The complementary supports have the two required exclusive markers
and the same mutual Legendre conditions. The same rank-one theorem
therefore gives the shared poles for every integer input and every
\(L\) in the specified progression. No more retained coordinates
are needed.

## 5. Explicit sufficiently large \(L\) for the three-scale route

For clarity we give an ordinary numerical defining coefficient exponent,
not just an algorithmic search. Use the old explicit constants
\(2^{342},2^{551},199\) of v78 and the height argument in Section 5
of README.md. Define a fixed exceptional set containing every prime
at most 76176, the three old additional primes
1875611, 3828397, 3982747, all prime divisors of numerators and
denominators of the fixed contact/pole values and their nonzero
differences (old and new, including the scalar contacts),
the fixed menu numerators, their nonzero pairwise squared
differences within each menu, and the fixed scalar multiplier and
menu denominator. All such additions are fixed independently of
\(L\) and of the witnesses. The source bad-prime and small-prime
exceptions are contained in this set. For the height radicals we
omit 67 as well, but use its scalar implication separately.

Let \(q=4000000\). The product of these distinct primes is at most
\(2^q\): the small primes divide \(76176!\), which is less than
\(2^{17\cdot76176}\). There are fewer than 128 relevant old/new
contact and pole rational constants, each with numerator and
denominator less than \(2^{40}\) in absolute value. Their differences
have numerator less than \(2^{81}\) and denominator less than
\(2^{80}\). Multiplying these bounds over all \(\binom{128}{2}\)
pairs and over the constants, then including the three extra
primes, the 42 menu numerators and at most \(2\binom{21}{2}\)
squared differences (each less than \(2^{80}\)), still gives
a bit bound less than \(q\). The denominator \(H=3^{30}\) only
has the already included prime 3. This deliberately coarse bound
avoids factoring any large integers; the exact census of these
fixed constants is checked in verify_selective.py.

In the effective height proof take \(Q=2^q\) as the upper bound
for the omitted radical multiplier,
\[
 K_\beta=2^{342+3q},\qquad A_0=q+201,\qquad K=2^{q+600}.
\]
The last two choices bound the old reflected-contact estimates
on the fixed translates for either family, since the fixed
translation heights are less than 80. They also suffice for the
original 24/26 construction without selective comparison.
As in README.md, for a nonzero residual \(Z\) of order \(j=1\) or 3,
\[
 B_0^2\le4K|Zc|^{1/j}(A_0+\log|Zc|)^2
             +8h(\beta)+4L\log67+350.
\]
Set \(m=4q+10000\), and let \(C_1=2(\operatorname{bitlength}(16K)+2(A_0+1))\).
Then
\[
 2^m>(24K)^3(A_0+3+5m)^6,\qquad C_1<2^{25}.
\]
These follow directly by comparing bit lengths. Once \(c\) is at
least \(2^m+1\), \(1000\), and \(4(C_1+4)\), and
\(67^{2L+1}\ge120K_\beta\), the two strict residual contradictions
of README.md apply. Choose
\[
 \boxed{L=171033187=171033184+3}.
\]
This is in the required progression, and \(67^{2L+1}>2^{6(2L+1)}\)
dominates all the listed thresholds. This is an explicit defining
member under the same retained effective three-scale arithmetic
premises, although its coefficients are enormous. The general
two-scale route uses any sufficiently large \(L\) in the same
progression, with its inherited ineffective trace-height constant.

## 6. Finite coefficient prescription and count

Use the eight point charts (four square-abscissa root charts and
four full auxiliary charts) in the original order, omitting the
duplicated \(U_4\) chart and substituting the shared \(U\) in all
its functions. The source coefficient recipe consists of these
point charts, the unchanged scalar factors and new rational
functions in Sections 1--2, the physical pole arguments, the
monic finite-root equations of README.md, and the third original
BB product pole when present. Every division is protected at the
selected character. For each of the 441 pairs of marker-menu
choices apply the same joint finite algebra encoder as in
README.md to the guarded source, then multiply these finitely
many polynomial factors. This is a precise specification by
finite integer operations, with no further quantified unknown.

The ranks are \(4^8 2^3=2^{19}\) and \(4^8 2^4=2^{20}\).
Counting ordinary base coordinates and the one shared encoder:
\[
\begin{array}{c|rrrrrr|r}
 &\text{input}&\text{point components}&\text{slope}&\text{shared pole}&
 \text{third pole}&\text{encoder}&\text{total}\\\hline
 \text{general}&1&16&1&3&0&1&22\\
 \text{specified}&1&16&1&3&2&1&24 .
\end{array}
\]
The proof uses the integer growth labels as genuine integer labels
of the retained four roots. It does not assert that two *different*
growth numerators can be identified: the Lucas residual still
needs all three simultaneously. Nor does it produce a point-block
deletion for the ordinary/weak-abc eleven-variable routes, where
there is only one input comparison and no separate Lucas group.
The higher degree of this specification and the large fixed input
substitution are accepted here in accordance with the priority of
lower ordinary coordinate count.
