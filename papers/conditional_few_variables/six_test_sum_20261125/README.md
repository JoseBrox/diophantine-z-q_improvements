# Eleven variables, degree at most 520065 under ordinary rational abc

**Theorem.** Retain the arithmetic premises of the ordinary-abc row in
[v88](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex),
including the normalized group, formal comparison, trace height and
compatible simultaneous prime selection. Under ordinary rational abc
and the same published BB pole theorem, there is an integral polynomial
family in eleven rational variables, including its input, defining
\(\mathbb Z\) for every sufficiently large fixed odd \(B\).
The degree is at most **520065**, compared with the previous 3261569.
The sufficient cutoff is still ineffective. No variable count changes.

This transfer uses the reciprocal-gate and asymmetric-contact ideas
of the recent quartic reductions, but operates directly on the
unrestricted-degree three-point source. It does not convert the
52-variable quartic by counting ordinary variables as finite roots.

## 1. Retained point source and new contact weight

Use the first three point blocks and six original rational elliptic
comparison tests \(C_i\) of the pinned v88 native source:
[ native.json ](../../../computation/bhargava_burungale_v88/bb_twelve/abc11/native.json).
The latter are the six entries of original_tests in the
balanced_actual_detector event; do not use the transformed_tests.
The root \(A=[n]P\) has its square-abscissa chart and \(n\ne0\);
\(H,U\) retain their full auxiliary charts. Retain every guard
preceding the old contact.H division, including the point norm guards.
The old local implication is that positivity of all six raw tests
at one good place above \(p\) forces \(X\in\mathbb Z_p\) and
\(X\equiv n\bmod p\). The old canonical witnesses give all six
tests positive at their successful place.

Write
\[
 \beta=X^2+B,\quad T=\operatorname{Tr}x(A),\quad
 M=\beta^4+T^4,\quad a=M+16,\quad x=a-z,\quad y=a+z.
\]
The shift \(B\) is a fixed positive odd integer. The one retained
contact slope is \(z\). Put
\[
 G_8(t)=\prod_{r\in\{1,4,7,8\}}(t^2-r^2),\quad
 A_0=G_8(x),\quad H_0=G_8(y)/y^4,\quad c=H_0/A_0+3/H_0 .
\]
In particular the new contact numerator and denominator are
\[
 P_c=G_8(y)^2+3G_8(x)y^8,\qquad
 Q_c=G_8(x)G_8(y)y^4,\qquad c=P_c/Q_c,\quad u=1/c .
\]
Guard \(P_cQ_c\ne0\); these are rational polynomials in the
retained variables before character extraction. They also guard
\(G_8(x),G_8(y),y\). This replaces the twelve-root derivative
contact map, and uses no additional coordinates.

## 2. Contact height

For \(G_8(t)\ne0\), let \(T_1(t)\) be the logarithm of the product
of primes outside a fixed bad set with \(v_p(G_8(t))=1\), and let
\(J_2(t)\) be the corresponding weight for valuations at least two.
The binary-form abc argument of
[v63](../derivative_detector11_20261117_v63.tex), applied to this
squarefree degree-eight polynomial, gives
\[
 T_1(t)\ge(4-2\epsilon)h(t)-O(1),\qquad
 J_2(t)\le(2+\epsilon)h(t)+O(1).
\]
Indeed if \(t=a_1/b_1\) is reduced the numerator form is coprime
to \(b_1\), its logarithmic radical is at least
\((6-\epsilon)h(t)-O(1)\), and its logarithmic size is at most
\(8h(t)+O(1)\). The bad set includes the retained source exceptions,
2, 3, 7, and primes of the fixed roots and differences.

At a simple x-contact write \(k=v_p(H_0)\).
The two valuations in c are \(k-1,-k\).
If \(k\le0\), it is even (negative values are multiples of four)
and the first term is uniquely minimal and negative odd.
If \(k\ge1\), the second is uniquely minimal and negative,
odd unless k is even. Discarded x-contacts are contained in
\(J_2(y)\). At a simple y-contact \(k=1\), and if
\(v_p(A_0)\le1\), the second term is uniquely minimal with
valuation -1. Thus discard only \(J_2(x)\) on that side.
Averaging the two estimates yields
\[
 R=\log r^+_{\rm odd,S}(u)
 \ge (1-3\epsilon/2)(h(x)+h(y))-O(1)
 \ge (1-3\epsilon/2)h(M)-O(1).
\]
All implied constants are independent of the fixed shift B and
of the rational tuple. In particular \(M\ge B^4\) ensures that
for every sufficiently large B there is a consumed prime,
without using any pole equation.

## 3. A sum detector and reciprocal gate

Use
\[
 W=1+\sum_{i=1}^6 c^i C_i^8\in K=\mathbb Q(\sqrt2),
 \qquad A_1=\operatorname{Nm}(W)+1,\quad T_1=\operatorname{Tr}(W),
 \qquad t=1+cT_1/A_1 .
\]
(The use of \(T_1\) here is separate from the logarithmic
simple-prime weight of Section 2.) When defined, the pole input
is \(e=7c/t^2\). No extra ordinary variable is used for W, A1,
T1, t or e.

At any odd \(v_p(c)\), the six nonconstant terms have pairwise
distinct nonzero valuation classes modulo eight, at each
unramified slot of K. Omit identically zero terms. Therefore
\(W\ne0\), its valuation is at most zero, and when it is
integral its residue is one. This is valid for both signs
of the odd valuation, including negative raw-test valuations.

At a consumed prime let \(\nu=v_p(u)>0\) be odd.
Write \(w_1,w_2\le0\) for the two slot valuations (repeated
in the inert case). If \(A_1=0\) then \(\operatorname{Nm}W=-1\),
forcing \(w_1=w_2=0\), so both residues are one and the norm
cannot be -1 at this odd prime. Hence \(A_1\ne0\).

Assume for now \(t\ne0\). The pole obstruction gives
\(v_p(e)=-\nu-2v_p(t)>0\), so \(v_p(t)<-\nu/2\).
If both \(w_i\le-\nu/2\), then \(v_p(A_1)=w_1+w_2\), and
\[
 v_p(t)\ge\min(0,-\nu+\min(w_1,w_2)-w_1-w_2)\ge-\nu/2,
\]
a contradiction. This includes \(T_1=0\).
At the successful slot \(v(W)>-\nu/2\); the distinct-minimum
argument gives
\[
 8v(C_i)-i\nu>-\nu/2,\qquad i=1,\ldots,6
\]
for every nonzero test. Thus all six tests have positive valuation
(with zero tests assigned infinite valuation). The original
local implication applies unchanged.

## 4. Integral terminal radicand, including the t=0 boundary

In the point algebra choose the common denominators \(d_i\) of
the two coordinates of \(C_i\), exactly as recorded in the v88
original_tests event. Put
\[
 D_0=\prod_i d_i,\quad R_i=D_0 C_i,\quad
 L=Q_c^6 D_0^8,\quad N=L+\sum_{i=1}^6
       P_c^i Q_c^{6-i}R_i^8.
\]
Here each \(R_i\) and \(N\) is a polynomial pair over the point
algebra, with multiplication in \(K\) implemented by
\((a,b)(c,d)=(ac+2bd,ad+bc)\).
On the retained guard \(W=N/L\). Define the scalar polynomials
\[
 J=\operatorname{Nm}(N)+L^2,\qquad
 K_0=Q_cJ+P_c\operatorname{Tr}(N)L,\qquad d=7P_cQ_c.
\]
Then \(t=K_0/(Q_cJ)\) and \(e=d(J/K_0)^2\).
With the two ordinary pole coordinates v,s adjoin only the
finite root q of the monic equation
\[
 q^2=(K_0^2-dJ^2)(v^4-d^2)(s^4-d^2).                 \tag{*}
\]
This is the BB normalized product radicand, with its square
denominator cleared by \(K_0^2\).

At a rational point character the existence of a consumed prime
proved in Section 2 ensures \(J\ne0\), by Section 3.
If \(K_0=0\), then the right side of (*) has odd finite valuation
at that consumed prime: \(v_p(d)\) is odd since \(v_p(c)\) is
odd and \(p\ne7\). The two quartic factors each have finite even
valuation by the unequal valuations of \(v^4,d^2\) and \(s^4,d^2\)
(including zero v or s). This contradicts rationality of q.
Consequently no extra norm guard for J or K0 is necessary.
Now \(q/K_0\) is a BB pole witness; the old negative-odd
obstruction applies to the nonzero e, proving the claim in Section 3.

If \(X\ne n\), the consumed primes divide the reduced numerator
of \(X-n\) by the retained formal comparison. Writing
\(E=h(1:\beta:T)\), the binary-power and trace-height bounds of
v78 with \(\kappa=1001/1000\) give
\[
 (997/1001)E\le h(M)+O(1),\quad
 n^2\ll E+1,\quad R\le E/2+\log(1+|n|).
\]
Taking \(\epsilon=1/100\) in Section 2 gives the strictly positive
absorption margin
\[
 (197/200)(997/1001)-1/2=96309/200200.
\]
It follows that E, then B, is bounded independently of the
rational tuple if \(X\ne n\). Therefore all rational witnesses
at sufficiently large fixed B have integral input.

## 5. Integer completeness, including foreign primes

Fix a nonzero integer \(X=n\), and retain the old root, reference
neighborhood, and multiplication-family preparation. The now fixed
positive \(a=M+16>8\) gives sixteen distinct rational contact
positions \(\pm(a+r)\), \(r=\pm1,\pm4,\pm7,\pm8\).
Use the inherited simultaneous prime supplier, with exactly
its original freedom of fixed divisibility, finite avoidance
and arbitrarily large slope. Enlarge the temporary preparation
set to include the numerator and denominator primes of a and
of the distinct contact positions and differences, and the
fixed bad primes, including 2 and 7. There are no new permanent
exceptions depending on n in soundness.
Choose \(z=N_z/(D_z^2L_z^2)\) and distinct selected primes
\(N_z\pm D_z^2(a+r)L_z^2\) as in the parent completeness proof.
At each selected prime exactly one root factor of the pair
\(G_8(x),G_8(y)\) has valuation one and all other factors
and \(y\) are units (exclude the finitely many nonzero
values of y at contact positions). Hence \(v_p(c)=-1\).
The old compatible index refinement supplies a slot with all
six raw tests positive. There \(W\equiv1\bmod p\).
At the other slot W is either a pole or has residue one.
Thus \(v_p(\operatorname{Tr}W)=v_p(\operatorname{Nm}W+1)\):
both are units if both slots are integral, and otherwise
both have the valuation of the unique pole.
It follows \(v_p(t)=-1\) and \(v_p(e)=1\).

At nonselected primes outside the temporary set, if z is integral
both contact polynomials are units by their exact factorization
into the selected primes over the fixed common slope denominator.
If y is a unit, c is integral; if y has positive valuation,
\(v_p(c)=-4v_p(y)\) is even. If z is nonintegral, the two terms
of c have common leading behavior \(z^{-4}\) and \(3z^{-4}\).
Since p is odd and a is integral at such primes,
\(v_p(c)=-4v_p(z)>0\) is even. Thus positive odd valuations
of u outside that set occur only at selected primes.

At any negative odd valuation of u outside the fixed bad set,
use the same distinct-minimum calculation for W. If both slots
are poles, \(v_p(A_1)=w_1+w_2\), and
\(v_p(T_1/A_1)\ge-\max w_i>0\).
If at least one slot is integral, the residue-one property gives
\(v_p(T_1/A_1)=0\) (both integral or exactly one pole).
In every case \(t=1+cT_1/A_1\) is a unit and
\(v_p(e)=v_p(c)>0\). No foreign prime is assumed absent.
At even valuations of c the square factor leaves valuations
of e even.

At the finitely many prepared places and real infinity, the
contact asymptotic is
\[
 c\sim4z^{-4},\qquad W\to1,\quad A_1\to2,\quad t\to1,\quad e\sim28z^{-4}.
\]
The convergence holds in the bounded raw-test neighborhoods
of the parent; all raw denominators are already protected.
Deep local slope denominators give the required dyadic class
seven with arbitrarily large positive even valuation, and
nonnegative valuation at every other prepared prime, including 7.
For sufficiently large real slope e is positive and less than
one, and J and K0 are nonzero. Thus e is prepared in precisely
the sense of the BB theorem used in v88: positive, less than one,
square reduced denominator, dyadic class seven and depth at
least four. That theorem supplies v,s and a root of (*), after
the explicit square rescaling. There is no new pole-realization
hypothesis.

All whole-character guards for the point source are a subset
of the old pre-contact guards. The new scalar guards \(P_c,Q_c\)
are independent of the finite point signs and nonzero at the
prepared slope. J and K0 need not be guarded at other geometric
characters, since (*) is monic and zero terminal roots are allowed.
The integer zero is added by the same exterior factor X as
in the old ordinary-abc route.

## 6. Exact finite polynomial specification and degree

Use the rank-four point table in v28, as pinned in the v88
parent.json, with the same polynomial \(A_i,B_i\) and base
coordinates. Use the tensor product of these three algebras,
and adjoin q by (*). Its rank is 128. In the native integer
coefficient DAG evaluate just the nodes required for the point
blocks, original_tests and original height beta and trace.
All node indices are pinned in [degree.json](degree.json);
there are no undefined external auxiliary variables.
The root's square-abscissa chart is unchanged. The six point
tower generators and their envelopes are precisely the first
six entries of the parent quadratic_tower; their total envelope
degree is 30. The old point norm and primitive-generator
nonvanishing proof applies on the retained guard.

Let \(G_0\) be the product of the scalar subalgebra norms from
parent.json on the twelve nonconstant pre-contact atoms
\[
 27,48,75,115,132,165,190,424,452,575,648,718 .
\]
This is exactly the multiplicative atom set of the old
pre-contact guards, after removing nonzero integer factors.
It protects all the raw test denominators. Set
\(\mathcal G=G_0P_cQ_c\).
Use the v78 bounded-prefix separator from
[PROOF.md](../../../computation/coauthor_audit_v78/H10-quartics/fewvars/PROOF.md)
with one terminal generator q. In more detail let \(b_i\)
be the six successive point tower generators, \(M_i\)
their old positive polynomial envelopes, and \(M_q\) the
positive envelope of q defined below. Put \(B_q=1+M_q\) and
\[
 \Omega=
 \sum_{i=1}^6 4B_q\Big(\prod_{k\le i} b_k\Big)
                           \Big(\prod_{k>i}4M_k\Big)
      +\Big(\prod_{k=1}^6b_k\Big)q .
\]
The bounded-prefix argument distinguishes all geometric
characters, including when q is zero. In particular on
\(\mathcal G\ne0\) it is nonzero at every character. Use
\[
                 F_B=X\det(I-Y\mathcal G\operatorname{Mult}(\Omega)).
\]
Y is the single encoder coordinate. Over each Artin local
factor, multiplication has its residue character's value on
the diagonal. Thus a rational determinant root gives a
rational character by separation and Galois descent.
At \(\mathcal G=0\) the determinant is one, so the only
possible additional input is zero. Conversely each prepared
rational character gives \(Y=1/(\mathcal G\chi(\Omega))\).
The algebra, multiplication matrices, and separator are
integer polynomial operations. At Y=0 the polynomial is X,
so its integer content is one.

For explicit envelope selection, let \(\mathcal R\) denote the
polynomial point-algebra element on the right of (*), and let
\(L_0\ge1\) be the sum of the absolute values of the integer
coefficients of all entries of its point multiplication
matrix, or 1 if this sum is smaller. Use
\[
 r_0=1+\sum_{i=0}^9 \xi_i^2,\qquad M_q=L_0 r_0^{1728},
\]
where \(\xi_i\) are the ten retained base coordinates.
These instructions determine \(L_0\) by finite integer
polynomial operations for each fixed B, without adding
a coordinate. To see the envelope bound, scale the
weighted point basis by \(r_0^{-w(b)/2}\).
The entry-wise weighted degree bound for multiplication by
\(\mathcal R\) is 6912, so the similar complex matrix has
row sums at most \(L_0 r_0^{3456}\).
Its eigenvalues are the character values of \(\mathcal R\).
Taking a square root bounds \(|q|\) by \(M_q\).

Here are the full degree bounds, obtained using the v28
weighted basis \(1,U_i,V_i,W_i\): weights 2,2,4 for the
root block, 2,2,3 for each full auxiliary block. They are
valid for every fixed B because the degree of B is zero.
The point multiplication table respects these weights;
adding the last root of weight 3456 preserves the filtration.
The old DAG arithmetic uses addition by maxima and
multiplication by sums. The six raw numerator and denominator
weight pairs, independently replayed, are
\[
 (1,2),(1,2),(4,4),(9,10),(28,27),(6,5).
\]
Thus \(w(D_0)\le50\), and the six \(w(R_i)\) are bounded by
49,49,50,49,51,51. The degree of \(M\) is at most eight,
so \(\deg P_c\le128,\deg Q_c\le160\). Therefore
\[
\begin{array}{c|r}
 L&1360\\
 N&1360\\
 J&2720\\
 K_0&2880\\
 d&288\\
 \mathcal R&6912\\
 q&3456
\end{array}
\]
The two terms of N are bounded by
\(960+400\) and
\(128i+160(6-i)+8w(R_i)\), respectively.
The two quartic factors of \(\mathcal R\) each have weight
at most 576; the first factor at most 5760.
Thus \(\deg M_q=3456\), the separator weight is at most
3486, and the retained guard degree at most
\(288+128+160=576\), using the exact old subalgebra
norm majorants for the twelve atoms.
For multiplication matrices an entry with row/column basis
weights \(w_r,w_c\) has degree at most the operator weight
plus \(w_c-w_r\); these differences sum to zero in a
determinant term. Including Y and the input factor gives
\[
             \deg F_B\le 1+128(1+576+3486)=520065.
\]

The arithmetic ledger and guard audit can be reproduced with
[verify.py](verify.py). The determinant is specified by the
above finite recipe and is not expanded. No new numerical
coefficient-height estimate or sufficient numerical B is claimed.
The previous v88 polynomial remains an alternative implementation.
