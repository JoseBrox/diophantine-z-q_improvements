# Two pole square tests from the Fermat cubic

The two-pole rows in POSITIVE.md admit the smaller bounds below. This uses the same positive-factor source circuits, the same exhaustive norm guards, and their original arithmetic premises. Here rationality of the pole witnesses suffices without separating every pair of complex pole characters. The source polynomial still has the given number of rational variables and integer coefficients.

| Route | Variables | Upstream degree | Degree using projective encoder | Support |
|---|---:|---:|---:|---:|
| General | 25 | 4,863,007,848,923,136 | 238,739,783,680 | < 2^849 |
| Weak abc, 121/100 | 13 | 43,211,777 | 2,525,697 | < 2^235 |
| Weak abc, 16/15 | 13 | 39,858,177 | 2,206,209 | < 2^233 |

## Two-radical lemma

Suppose x²=d and z²=e with d,e rational, and |x|,|z|≤1/2 in the chosen complex embedding. Then

    x³ + z/(1+z) is rational if and only if x and z are rational.

Indeed z/(1+z)=(z-e)/(1-e), and 1-e≠0. Thus the only possibly irrational part of the expression is d x + z/(1-e). If just one of x,z is irrational, its coefficient is nonzero, including when the other root is zero. If both are irrational and the displayed expression is rational, they generate the same quadratic field and have ratio t=z/x∈Q. To see this, an affine rational relation forces equality of the two quadratic fields. Their nontrivial conjugation negates both roots, so their ratio is fixed and their rational linear combination must vanish. Multiplying out gives

    d²t² - t - d = 0.

Its discriminant 1+4d³ must be a rational square. On y²+y=d³ all affine rational points have d=0, contradicting the assumption that x is irrational.

For completeness, this last elliptic fact follows from Fermat's last theorem for exponent three. If r²=1+4d³ and d≠0, let X=4d,Y=4r. Then Y²=X³+16. Under

    P=(X³+64)/X²,    Q=Y(X³-128)/X³,

direct expansion gives Q²=P³−432. Here P≠0, since X=−4 would make Y² negative. Now (36+Q)/(6P) and (36−Q)/(6P) are rational with cubes summing to 1. Fermat's theorem forces one of them to vanish, so Q=±36 and P=12. Then X³−12X²+64=0. The rational-root theorem excludes the candidates ±1,±2,±4,±8,±16,±32,±64. This proves the asserted rational-point classification; it is also recorded for [LMFDB curve 27.a4](https://www.lmfdb.org/EllipticCurve/Q/27/a/4).

## Encoder

Let q1,q2 be the reduced pole roots in the original order. Let M1,M2 be their upstream positive scalar envelopes. Put H1=2M1, H2=2M2, x=q1/H1, z=q2/H2. On all complex characters both roots have absolute value ≤1/2. Use the terminal fraction

    phi_(m+1) = (x³ + z/(1+z))/8.

Its absolute value is ≤9/64<1/4. Its denominator is nonzero on every geometric character, even if a pole root is zero. Prepend each of the m point generators t_i with its envelope A_i by phi_i=t_i(1+phi_(i+1))/(4A_i), exactly as in PROOF.md. All these point stages have absolute value ≤1/3, and the value at the first point stage is nonzero.

If phi_1(chi) is rational at a geometric character chi, every Galois conjugate gives the same value. Characters differing at any point stage give distinct values, by the disjoint complex disks at their first differing point and the injectivity of every common earlier affine map. This proves that each conjugate agrees with chi on its point character. The point character is rational. Now the common point coefficients in the phi recursion are rational and nonzero, so it follows by inversion of its affine maps that phi_(m+1)(chi) is rational. Both d and e in the two-radical lemma are rational here because the checker showed each reduced pole radicand is in the point algebra. The lemma supplies rationality of both normalized roots and hence of q1,q2; thus the whole character is rational. A rational character plainly gives a rational nonzero phi_1.

Use the following numerator and denominator in the integral free arithmetic algebra. Set J=H2+q2 and

    N_(m+1)=q1³ J + H1³ q2,   D_(m+1)=8 H1³ J.
    N_i=t_i(D_(i+1)+N_(i+1)), D_i=4 A_i D_(i+1).

Then phi_i=N_i/D_i. Every D_i is a unit at every rational base specialization since all geometric character values are nonzero. Take the finite matrix pencil

    det(M_D1 - Y G M_N1),

where G is the positive-factor scalar guard, multiplying by the source input on the indicated conditional rows. When G=0 the determinant is Norm(D1)≠0. Otherwise a rational determinant root yields a geometric character where phi_1=1/(YG), which is rational and so the character is rational. The eigenvalue argument applies to simultaneous multiplication operators: after extending scalars the local Artin factors make the multiplication diagonal entries equal their residue-character values. Conversely a rational character and G≠0 give a rational Y. All remaining arithmetic and chart arguments follow POSITIVE.md. The displayed determinant need not have content one as written; dividing by its positive integer content produces a primitive polynomial of the same zero set and degree.

The weighted degree bound before the possible input factor is N max(deg D1, 1+g+deg N1), where N is the algebra rank. The logarithmic coefficient column bound is N(1+max(logNorm D1, logNorm G + logNorm N1)). All other counts use PROOF.md. Run `python -B projective.py` after the positive-factor construction and check. It computes the bounds from the positive arithmetic receipts and checks the 3-isogeny identity symbolically. [projective_bounds.json](projective_bounds.json) contains the numerical intermediate values.
