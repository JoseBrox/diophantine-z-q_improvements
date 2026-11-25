# Denominator-sensitive contact estimate: a 52-variable ordinary-abc quartic

**Theorem.** Under the same arithmetic premises as the
[53-coordinate reciprocal-gate construction](../reciprocal_gate53_20261124/README.md),
including ordinary rational abc, the sum of the 42 integral quadrics
in quadrics.json defines Z in Q for every sufficiently large fixed
positive integer B congruent to 1 modulo 8. The 52 variables include
the input. No new arithmetic premise or additional pole-realization
hypothesis is used. The sufficient cutoff remains ineffective.

This completes the earlier
[52-coordinate candidate](../../docs/results_20261125_uniform_anchor.md)
by retaining the denominator radical in the binary-form abc estimate.

## 1. Contact chart and guards

Keep all 45 pre-contact coordinates and the reciprocal pole/gate
of the 53-variable parent, including

\[
 M=B+8(X^8+T_{\rm sc}^2),\quad
 a=M+16,\quad u=1/c.
\]
With \(x=a-z,\ y=a+z\), define
\[
 P(R)=\prod_{r\in\{1,4,7,8\}}(R-r^2),\quad G(t)=P(t^2),
 \quad A=G(x),\quad H_y=G(y)/y^4,
 \qquad c=H_y/A+3/H_y.
\]
The seven contact coordinates, numbered 46 through 52, are
\[
 z,\ r_x=x^2,\ r_y=y^2,\ s_x=r_x^2,\ s_y=r_y^2,\ F=cA,\ H_y.
\]
Their seven equations are the four square rows and
\[
 uF=P(r_x),\qquad H_y s_y=P(r_y),\qquad
 F H_y=H_y^2+3uF,
\]
where \(P(r)=r^4-130r^3+5073r^2-55120r+50176\) is evaluated
quadratically as \(s^2-130rs+5073s-55120r+50176\).
All seven rows are quadratic; the parent unit row guards u.

On every solution y is nonzero because P(0)=50176. If F or H_y
vanishes, the last row and u nonzero force both to vanish, hence
G(x)=G(y)=0. This is impossible since all their roots lie in [-8,8]
while x+y=2(M+16)>32. Thus both are nonzero and the displayed
rational formula for c follows exactly, with no additional guard.
Conversely every allowed contact tuple with c nonzero gives these
seven coordinates.

## 2. Denominator-sensitive abc estimate

For any rational t=A_0/D in lowest terms (D>0), set
\[
 h_t=h(t),\qquad d_t=\log\operatorname{rad}D.
\]
Assume G(t) nonzero and let T(t) and J_2(t) denote the logarithmic
weights of primes outside a fixed finite S at which v_p(G(t))=1
and v_p(G(t))>=2, respectively. Enlarge S to include the parent's
exceptions, primes dividing the fixed contact roots and their
differences, and 3.

Let \(N=\prod_{r=\pm1,\pm4,\pm7,\pm8}(A_0-rD)\).
The fixed squarefree binary form \(D N\) has degree nine.
The standard binary-form consequence of rational abc, already used
in [v63](../../papers/conditional_few_variables/derivative_detector11_20261117_v63.tex),
gives, for every fixed epsilon>0,
\[
 \log\operatorname{rad}N
 \ge (7-\epsilon)h_t-d_t-O(1).
\]
Here gcd(N,D)=1, including t=0, and \(\log|N|\le8h_t+O(1)\).
Subtracting the radical from the logarithmic size bounds the weight
of multiple primes. Consequently
\[
 J_2(t)\le(1+\epsilon)h_t+d_t+O(1),\qquad
 T(t)\ge(6-2\epsilon)h_t-2d_t-O(1).
\]
The constants are uniform in t, B and the witness tuple.

Write \(R_u=\log r^+_{\mathrm{odd},S}(u)\). At a simple x-contact,
put k=v_p(H_y). The two summands of c have valuations k-1 and -k.
If k<=0, then k is even (negative values of H_y arise either
from a negative valuation of y or from a positive valuation
of y, and in either case are multiples of four). The first
summand is uniquely minimal with negative odd valuation.
If k>=1, the second is uniquely minimal with negative valuation;
it is odd for k odd. All discarded x-contacts therefore belong
to the multiple-prime support J_2(y).

At a simple y-contact, v_p(H_y)=1, and if l=v_p(G(x))<=1,
the valuations 1-l and -1 have unique negative odd minimum -1.
Thus only J_2(x) need be discarded. These arguments are valid
for arbitrary rational contact tuples, not just prepared integer
witnesses, and include negative valuations of the other slot.
It follows that
\[
 \begin{split}
 R_u&\ge (6-2\epsilon)h_x-(1+\epsilon)h_y-2d_x-d_y-O(1),\\
 R_u&\ge (6-2\epsilon)h_y-(1+\epsilon)h_x-2d_y-d_x-O(1).
 \end{split}
\]
Averaging, with \(S_h=h_x+h_y\), gives
\[
 R_u\ge (5/2-3\epsilon/2)S_h-\tfrac32(d_x+d_y)-O(1).
\]

## 3. The denominator of the height scalar

Let \(H=h(M)\) and \(d_M=\log\operatorname{rad}\operatorname{den}(M)\).
For arbitrary rational x,y with x+y=2(M+16),
\[
 d_x+d_y\le d_M+S_h-H+O(1),\qquad S_h\ge H-O(1).
\]
For the first claim first replace M by x+y. If the denominator
depths of x,y,x+y at a prime are i,j,k, then when i!=j one has
k=max(i,j); when i=j one has k<=i. In both cases
\[
 {\bf1}_{i>0}+{\bf1}_{j>0}
 \le {\bf1}_{k>0}+i+j-k.
\]
Sum with weights log p. The remaining denominator logarithm
\(\log(\operatorname{den}(x)\operatorname{den}(y)/
\operatorname{den}(x+y))\) is at most
\(h_x+h_y-h(x+y)+\log 2\) by the archimedean triangle inequality.
Translation by the fixed 16 and multiplication by 2 change height
and denominator radical by bounded amounts only. The second claim
is the ordinary height inequality for addition.

Since epsilon<2/3, the averaged contact inequality now yields
\[
 R_u\ge (5/2-3\epsilon/2)H-\tfrac32d_M-O(1).
\]

The special denominator structure of M improves this further.
Outside primes dividing 2 and den(X), if M has negative
valuation then T_sc has negative valuation, and
\(v_p(M)=2v_p(T_{\rm sc})\) is even. In particular all denominator
primes of depth exactly one, except possibly 2, divide den(X).
Primewise, a denominator depth k>=2 has 1<=k/2.
Consequently
\[
 d_M\le \tfrac12\log\operatorname{den}(M)
      +\tfrac12\log\operatorname{rad}\operatorname{den}(X)+O(1)
 \le \tfrac12H+\tfrac12h(X)+O(1).
\]
Thus
\[
 R_u\ge (7/4-3\epsilon/2)H-\tfrac34h(X)-O(1).
\]

Take epsilon=1/100 and kappa=1001/1000 in the parent's
signed mixed-power estimate, permissible under ordinary abc.
As in that proof \(h(X)\le (501/997)H+O(1)\); hence R_u grows
at least a strictly positive multiple of H. In particular
for sufficiently large B there is at least one consumed prime,
and the 53-coordinate reciprocal-gate proof applies, including
its exclusion of the t=0 pole degeneration.
If X is neither 0 nor its integral difference-point label m,
the same local comparison at every consumed prime gives
\[
 R_u\le2h(X)+\log(1+|m|).
\]
Combining,
\[
 \left(\frac{347}{200}-\frac{11}{4}\frac{501}{997}\right)H
 \le \log(1+|m|)+O(1),\qquad
 \frac{347}{200}-\frac{11}{4}\frac{501}{997}
 =\frac{70409}{199400}>0.
\]
The parent trace-index bound, together with
\(2h(T_{\rm sc})\le h(X^8+T_{\rm sc}^2)+8h(X)+\log 2\),
bounds m^2 by O(H+1). Therefore H is bounded independently of B
if X is neither 0 nor m. Since M>=B this is impossible for all
sufficiently large fixed B. Thus every rational zero has integral
input. No assumption on the relative sizes of x and y is used.

## 4. Ordered completeness at all primes

The following repeats the arithmetic preparation of the previous
candidate in full, to separate completeness from the new estimate.

Fix integer X=n. Keep the parent's true multiplication family,
including its separately supplied X=0 fiber, reference data and M,
then choose the sixteen primes associated with the distinct slope
positions +/- (a+r), r in {-8,-7,-4,-1,1,4,7,8}, by the parent's
retained Gaussian prime-pattern supplier. Enlarge the fixed-for-n
preparation set as in the asymmetric-contact parent to include
coefficient primes, 3, the support of a, contact-position
numerators and denominators and differences, and the values of
y at contact positions. The selected primes are outside that set.
At a selected x-contact A has valuation 1 and H_y is a unit;
at a selected y-contact H_y has valuation 1 and A is a unit.
The two terms of c have unique minimum -1 in either case, hence
v_p(u)=1. The same local point preparation yields v_p(D)>0
in the reciprocal-gate parent.

At a nonselected prime outside the enlarged set with integral
slope, A and G(y) are units by the full contact prime factorization.
If y is a unit, c is integral. If v_p(y)>0, H_y has negative
valuation -4v_p(y); the first summand of c uniquely dominates
with negative even valuation. At a nonintegral slope prime
outside the set, x and y have the slope's negative valuation.
The expansion at infinity is
\[
 c=4z^{-4}(1+O(z^{-1})).
\]
Indeed G is monic of degree eight, so H_y has leading term y^4,
H_y/A has leading term z^-4, and 3/H_y has leading term 3z^-4.
All the relative coefficients after the leading 4 are integral
outside the enlarged fixed set. Thus c has positive even
valuation at these nonintegral slope primes. There are no
unprepared positive odd valuations of u outside the selected
prime set.

At every fixed preparation prime impose sufficiently deep
slope denominators. The same asymptotic ensures c has positive
valuation, and at 2 it is in the squareclass of 4z^-4 with
arbitrarily large even positive depth. The real large-positive
slope gives c>0 and c approaching zero. The parent estimates
W-1=O(c), D=O(c^2) and reciprocal t=1+1/(u+D_s) approaching one
remain valid since the raw tests are unchanged. In particular
the BB pole input b=7c/t^2 is positive and less than one,
has class seven at 2 with depth at least four, and positive
seven-adic valuation. At selected primes b has valuation 1
by the parent computation. For every other prime outside
the fixed set with negative odd valuation of u, the unchanged
true-multiplication identity and Section 3 of the reciprocal
gate parent give t a unit and v_p(b)>0. Even valuations of
u give even valuations of b. These cases prove that the
actual b has square reduced denominator. Its BB-native
realization therefore supplies the pole witnesses. All
contact and point preparations occur before that pole choice.

## 5. Exact census

The seven contact rows replace eight rows in the 53-variable
parent. Keep the 40 unchanged residuals (including the four
contact square rows and contact.rightValue). Replace
contact.leftValue by contact.leftScaledValue, remove
contact.rightInverse, and replace contact.asymmetric by
contact.harmonic. Variables x1 through x52 are retained,
with x51 now F and x52 still H_y. The exact table has 52
variables and 42 quadratic rows, 789 parameter-separated terms,
785 coordinate monomials. The sum of squares has degree four
and content one (coefficient 1 of x1^4). The B=1 algebraic
fixture has 11,146 ASCII bytes and coefficient height
5,531,402,752. It is **not** certified as a defining instance.
The coefficient family and sufficient-cutoff qualification are
as stated in the theorem.

The independent check reconstructs the two replacement rows,
the 40 retained rows, the split polynomial, the symbolic and
specialized expanded coefficients, and the exact height margin.
Finite valuation profiles check the elementary local and
denominator-depth inequalities. These checks supplement, but
do not replace, the preceding uniform arithmetic argument.
