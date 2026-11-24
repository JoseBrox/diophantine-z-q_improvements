# One fewer elliptic denominator in joint rationality descent

## Theorem

Retain the hypotheses of the v81 [amplified rationality descent](../amplified_rationality_descent_20261119_v81.tex): a number field K, a curve E/Q with 0<rank E(Q)=rank E(K), the six-point divisor height bound with coefficient theta>7/2 (ordinary abc over K suffices), and the prepared class-seven pole realization. The new argument reduces the [joint rationality selector](../joint_rationality_20261124/README.md) from 7k+3 to **7k+2 total K-coordinates** for Q^k in K^k. In particular Q in K needs nine coordinates. All witnesses can be rational on rational input tuples. Combining with the [monic-absorption theorem](../absorbed_joint_rationality_20261124/README.md) gives 7N+1 total coordinates to transfer an N-coordinate definition of Z^d from Q to K: 78 for Z and 21d+57 for O_K via the v110 joint selector (99 for quadratic K). These are unrestricted-degree bounds; the exceptional correction is ineffective. All original integer-definition premises remain.

## 1. A torsion-supported parameter

Use an integral short Weierstrass model y^2=x^3+A x+B of E, with nonzero discriminant, and write z=-x/y. The third division polynomial is

    psi3=3x^4+6Ax^2+12Bx-A^2.
    f(P)=-psi3(x(P))/(3y(P)^3).

Its expansion at O is z+O(z^2). Its divisor is supported on E[2] union E[3]: a simple zero at O, simple zeros at the eight nonzero 3-torsion points, and poles of order three at the three nonzero 2-torsion points. This follows from the third division polynomial's simple roots on the smooth curve, the simple zeros of y at the nonzero 2-torsion, and the orders -2,-3 of x,y at O. These assertions hold in every good reduction characteristic greater than 3.

For any rational point P in the nonzero finite f chart, at every good prime p>3 with v_p(f(P))!=0,

    [6]P lies in E_1(Q_p),   1<=v_p(z([6]P))<=|v_p(f(P))|.    (1)

Indeed the reduction of P is in E[2] or E[3]. In the smooth integral curve, the relevant torsion point T lifts uniquely in its residue disk (prime-to-p torsion is etale; Hensel), and f is a local parameter to order 1 or -3 times a unit, or to order 1 at O. The formal parameter of P-T has positive valuation |v_p(f(P))| or |v_p(f(P))|/3. Multiplication by 6 preserves it, since 6 is a unit. The statement includes P reducing to O. Bad primes and 2,3 will instead be handled by choosing the original point very deep there.

Fix m with m E(K) contained in E(Q). Write Gamma=m E(K), and use points with guarded affine preimages under [m]. For the first stage use U_i,V in Gamma, set a_i=f(U_i), b=f(V), lambda_i=a_i/b. The second stage uses just W_i in Gamma, with

    C_i=a_i^4+a_i^(-4)+b^4+b^(-4),   beta_i=C_i z(W_i).          (2)

The numbers lambda_i,beta_i are rational. All displayed divisions are guarded. C_i is positive for rational nonzero a_i,b. The source test is exactly v81 with these lambda_i,beta_i and g_i=(t_i^3-2)/(t_i^3-3):

    b_i1=(lambda_i-g_i)^2(1+g_i)^2/g_i^3,
    b_i2=(beta_i-t_i)^2 ((1+lambda_i)^2/lambda_i)^3.

Impose the prepared pole tests and H(t_i)!=0. Soundness is verbatim v81, because it used only the rationality of lambda_i,beta_i and the even-pole obstruction, not their particular ratios. The same ineffective correction H for the larger predicate allowing arbitrary rational lambda,beta works; the v81 proof of finite irrational exceptions uses only that rationality. If the H in an earlier fixed presentation was chosen only for a smaller accepted set, take the product of the minimal polynomials of the exceptions of this larger predicate instead. No new height hypothesis.

## 2. Ordered all-prime completeness

Fix t_i in Q and write g_i=A_i/D with a common nonzero integer D and nonzero integers A_i. Here g_i cannot be 0, -1 or 1 (rational-root test, and the two cubics differ by 1). In particular |A_i|!=|D|. Let J=6 D product_i A_i, replacing it by its absolute value if desired. Let S contain 2,3,5,7, all bad primes of the curve, all prime divisors of J, the supports of g_i(1+g_i), and the denominator primes of t_i. The set is fixed before choosing the first-stage point. Use a nontorsion Q in m E(Q) lying very deep in all formal groups at S and arbitrarily close to O really, in the identity component. Such points follow from the finite-index formal neighborhoods and recurrence in the compact real group, as in v81. Put U_i=[A_i]Q and V=[D]Q.

At every p in S the ratios f([A_i]Q)/f([D]Q) approximate A_i/D to arbitrary accuracy, since f has expansion z+O(z^2) and integral formal multiplication has linear term the index. At the real place they converge to g_i. These rational functions of Q are nonconstant: a constant ratio would give equal divisors for the pullbacks of f under [A_i] and [D], whereas the degrees of the corresponding nonconstant maps to P^1 are deg(f) A_i^2 and deg(f) D^2. Hence in addition we avoid lambda_i=0,+/-1,+/-g_i, by excluding a finite set of curve points. Choose the first-stage approximation sufficiently close to prepare b_i1 exactly as in v81: nonzero, |b_i1|<1, square denominator, v_2>=5 and v_3,v_5,v_7>=1. Outside S its valuation is even. The finite avoidance is compatible with arbitrarily deep neighborhoods and infinitely many recurrent multiples.

Now fix Q, hence all actual lambda_i and C_i. Put R=[J]Q. Define T to consist of 2,3,5,7 and all rational primes at which at least one v_p(lambda_i) is odd. This is a finite set, possibly containing new primes outside S. At a new prime p, v_p(a_i)-v_p(b) odd implies |v_p(a_i)|!=|v_p(b)|; in particular at least one is nonzero. By (1), R is in E_1(Q_p), since J is divisible by 6A_i and 6D. At p outside S the quotient J/(6A_i) or J/(6D) is a unit. For every i with odd v_p(lambda_i), if M_i=max(|v_p(a_i)|,|v_p(b)|), the largest absolute valuation is attained uniquely and is positive. The four summands of C_i therefore have a unique minimum, giving

    v_p(C_i)=-4 M_i,   v_p(z(R))<=M_i.                          (3)

Since t_i is p-integral outside S, v_p(t_i/C_i)>=4M_i>=v_p(z(R)), including t_i=0. This is the crucial bound for foreign contact primes. At p in S, choose Q originally so deep that, writing L=v_p(z(Q)), one has v_p(a_i)=L+v_p(A_i), v_p(b)=L+v_p(D), and v_p(z(R))=L+v_p(J). These equalities hold for sufficiently deep formal points, including at bad primes (formal logarithm or linear term with fixed multiplication index). Whenever v_p(lambda_i) is odd the unique-minimum estimate again gives v_p(C_i)=-4 max(v_p(a_i),v_p(b)). At p=2,3,5,7 with equal valuations of a_i,b, the two inverse fourth powers have the same valuation. After division by that power of p, their unit fourth powers sum to a unit for p=3,5,7: fourth powers are squares and -1 is nonsquare for 3,7, and fourth powers are 1 mod 5. For p=2 their sum has valuation exactly 1 since odd fourth powers are 1 mod 16. The two positive fourth powers are negligible for deep Q. Thus v_p(C_i)<=-4L+1 at these fixed primes (the index valuations are nonnegative). The same sufficient original depth L, depending only on the fixed t_i,A_i,D,J and curve, ensures

    v_p(t_i/C_i)>=v_p(z(R))

for all pairs needing approximation at T. At primes in T where i does not need approximation, choose target 0. At real O, a_i,b tend to zero and C_i tends to positive infinity. Thus initially also ensure that every t_i/C_i lies in the small real image of z on the identity component.

At good p>3 outside S, the formal logarithm of the integral model is an isometric bijection E_1(Q_p) -> p Z_p, with log in the parameter z having leading coefficient 1; this is the usual convergence and inverse theorem over Q_p (v_p(z)>1/(p-1)). At primes in S use deep neighborhoods where the same statement holds. In particular the closure of the cyclic group generated by R in that formal neighborhood consists precisely of the points with parameter valuation >=v_p(z(R)), because log(nR)=n log R and Z is dense in Z_p. For each i choose a local point with z=t_i/C_i at the relevant primes, choosing O for a zero target; z is a coordinate on the formal disk. Any prescribed finite precision can be achieved by integer multiples [n]R with n in one residue class modulo a product of powers of the distinct primes: the congruences on n are independent by CRT. At the real place the same progression of multiples is dense in E(R)^0, since R is nontorsion and in that component. Therefore one can simultaneously make beta_i=C_i z(W_i), W_i=[n_i]R, arbitrarily close to t_i at the required places and really, with W_i avoiding the finitely many excluded chart points and beta_i=t_i. All W_i have rational preimages under [m]. This proves simultaneous approximation AFTER fixing all first-stage primes, without a second denominator point.

For b_i2, at any prime with even v_p(lambda_i), its valuation is even (including when lambda_i is a unit and 1+lambda_i is not). At every odd-valuation prime the above approximation makes b_i2 integral, and at 2,3,5,7 makes its valuation as large as needed. Really it makes 0<|b_i2|<1. Thus each b_i2 has the prepared class-seven pole witnesses, with the same multiplier menu as v81. The argument requires no approximation at foreign primes with even lambda valuation. All the witnesses can be rational.

## 3. Finite polynomial specification and counts

Use one ordinary abscissa for each of the 2k+1 point preimages of V,U_i,W_i; adjoin their ordinates monically by Y^2=X^3+A X+B. Compute [m] by guarded division polynomials and use (2) and the displayed b_i1,b_i2 as literal rational-expression DAGs. For each of the 16^(2k) multiplier choices adjoin the same two monic pole roots per input as in the joint rationality theorem, using numerator-denominator pairs: a root of N/D is obtained as Y/D with Y^2=ND. Every denominator, nonzero point chart, f and z chart, C_i, H(t_i), and nonzero prepared pole input is a selected-character guard; do not guard terminal ordinates. The polynomial uses the selected-character determinant of [monic absorption, Section 1](../absorbed_joint_rationality_20261124/README.md), which works with repeated roots and with vanishing guards at unselected geometric characters. The norm form over an Eisenstein extension of K combines equalities, finite products combine alternatives, and clearing fixed rational denominators gives integer coefficients. This is a finite coefficient recipe, not a numerical degree or height bound.

There are k input coordinates, 2k+1 point abscissas, 4k pole parameters and one final encoder: 7k+2. To transfer an N-coordinate polynomial over Q, use the degree-stratum monic absorption of one existential coordinate from the preceding note, then test all N original coordinates (one is a finite algebra element, not an ordinary coordinate). The identical selected-character proof gives 7N+1. The ring-of-integers substitution uses an integral basis exactly as before.

## Attribution and limitations

Pasten--Vidaux, *Diophantine sets over global function fields*, arXiv:2611.31218v1 (23 November 2026), motivates the present return to ordered local approximation and torsion-supported congruence propagation; the arithmetic descent itself originates in their arXiv:2611.24748v1. The two-stage amplification, class-seven preparation and finite-algebra encoder are the cited project constructions and Bhargava--Burungale theorem. The torsion-supported parameter, unique-minimum coefficient, and shared cyclic subgroup argument here are new deductions, not assertions of either Pasten--Vidaux paper. The result is conditional on the original stable-rank and height inputs and gives no new unconditional arithmetic rank theorem. It does not reduce the separate Z-over-Q counts or claim an effective cutoff.