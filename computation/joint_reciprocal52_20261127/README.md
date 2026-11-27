# Joint quadratic reciprocal packing, 27 November 2026

**Theorem (relative to the arithmetic inputs of the 52-variable parent).** Under exactly the premises of the [denominator-sensitive 52-coordinate construction](../denominator_radical52_20261125/README.md), including ordinary rational abc, the 42 quadrics in quadrics.json have sum of squares with rational input projection Z for all sufficiently large fixed positive integers B congruent to 1 modulo 8. This is a different joint quadratic chart, not a new variable-count record. No effective B is asserted.

## Exact chart

Use K=Q(rho), rho^2=2, a=1+rho, b=4-2rho, delta=-23+17rho, Delta=a delta=11-6rho. The translating point is (a,ab). The three field coordinates l,w,v satisfy a l w=1 and v(v-a(l+w)-2b)=delta. Thus all three are nonzero, k=1/v=(v-a(l+w)-2b)/delta is affine, and 49k=(23+17rho)(v-a(l+w)-2b). The complete v40 reference chart gives f(H)=l/v, f(H-R0)=w/v, S=v-b-al, T=aw-v+b, where f=1/x and S,T are ordinate-to-abscissa ratios. 

For the v65 pair put s=X y(U)/x(U), t=X y(V)/x(V), F=X^2 f(U), G=X^2 f(V), p=h+s+t. Its equations are d=pF=hG, Delta(F+G)=(s-t)h-t^2, X^4=d(s-t)-Delta FG. Introduce Y=lF and Z=wG instead of F,G. Require
\[
 l d=pY,\quad w d=hZ,\quad
 a\Delta(wY+lZ)=(s-t)h-t^2,\quad
 X^4=d(s-t)-a\Delta YZ .
\]
These are exactly equivalent, since F=awY, G=alZ and a l w=1. Thus the pair chart has its old finite-distinct-point domain, including tangencies and finite torsion differences. The unchanged half trace h0 is the real component of hp, and T_sc=2h0=X^2 Tr x(U-V).

The raw errors are C=s-S, I=t-T. The reciprocal products J=kY and K'=kZ need no individual registers. Instead store k_s=ck and L_s=k_sY+conj(kZ), using 49k_s=c(49k) and 49L_s=49k_sY+conj((49k)Z). Thus L_s=cJ+conj(K'). Store P=C^2+c conj(I)^2 and Q=u C^2-conj(I)^2 by the quadrics P+cQ=2C^2, uP-Q=2conj(I)^2 (u=1/c). The signed detector is now
\[
 W=1+cC^4-c^3\overline I^4+c^2 L_s^2,\qquad
 uW_s=u^2+PQ+L_s^2,\quad W_s=uW.
\]
The latter equation is quadratic and exactly recovers the former. Keep all the parent's scalar powers, height, seven contact registers, unit, norm gate, reciprocal normalizer and BB pole. The norm gate is D Tr W=Nm(W-1), D_s=uD; its trace denominator cannot vanish.

Coordinate meanings (pairs indicate components in 1,rho): x1=X; x2:3=l, x4:5=w, x6:7=v, x8=h0, x9:10=s, x11:12=t, x13:14=Y, x15:16=Z, x17:18=h, x19:20=d, x21:22=k_s, x23:24=L_s, x25:26=P, x27:28=Q. All remaining coordinates have exactly the parent meaning. In particular x29=X^2, x30=X^4, x31:32=W_s, x42=D_s, x43=c, x44=u, x45=M. The point/comparison block with quadratic outputs J,K' has 23 rational coordinates (excluding input and its two powers); compiling the detector adds four helper components, leaving the total at 52.

## Soundness

At a consumed good prime put v(c)=-mu, with positive odd mu. In each unramified slot, J,K' have even valuations by the elliptic equation (zero has infinite valuation). The two summands of L_s have distinct parity when nonzero, hence its valuation is their minimum. The C and I terms in W have distinct odd classes modulo four; the L_s term has even valuation. A negative minimum therefore cannot cancel, even with the constant 1. The reciprocal gate proof in the 53-variable parent, including exclusion of its zero normalizer fiber, gives v_p(D)>-mu/2. If W is nonintegral at both slots, v_p(D) is at most the larger slot valuation of W, by comparing the norm and trace; otherwise choose an integral slot. In either event some slot has v(W)>-mu/2. Consequently
\[
 v(C)>\mu/8,\quad v(\overline I)>5\mu/8,\quad
 v(L_s)>3\mu/4,\quad v(J)>7\mu/4,\quad
 v(\overline {K'})>3\mu/4.
\]
All four old raw tests are positive; the retained inverse-parameter lemma gives local integrality of X and p|num(X(m-X)), where m is the integer difference label.

When X is a p-adic unit, the reference and comparison points are formal at the corresponding slots and have equal depths, d_+,d_- respectively. Their product valuations are 4d_+,4d_-. The inverse-parameter errors divided by the unit-scaled ordinate ratios have valuation at least floor(mu/8)+1+d_+ and floor(5mu/8)+1+d_-. The relative formal-logarithm errors have valuation at least 4d_+,4d_- at p>5 (the short Weierstrass formal logarithm has first correction in degree five). Thus
\[
 v_p(m-X)\ge 2+\lfloor\mu/8\rfloor+\lfloor7\mu/16\rfloor .
\]
Indeed d_+>=1+floor(7mu/16), d_->=1+floor(3mu/16). Each of the two logarithm bounds and the alternate comparison bound is at least the displayed integer: for mu>=11 this follows from floor(r)>=r-1 and the corresponding linear bounds, and for mu=1,3,5,7,9 by substitution. Multiply each ratio estimate by its integral reference label, subtract, and use that the labels differ by one. This strengthens the previous large-depth bound, and yields p^2 at mu=1. At primes dividing num(X) no stronger conclusion is claimed.

For X nonzero and X!=m, the odd positive support of u divides num(X) times the square root of the prime-power part of num(m-X) supported away from num(X). Its logarithm is at most (3/2)h(X)+(1/2)log(1+|m|). The parent contact estimate gives R_u >= (347/200)H-(3/4)h(X)-O(1), H=h(M), and its mixed-power estimate gives h(X)<=(501/997)H+O(1). Substitution leaves the strict margin 120509/199400. The unchanged trace-index estimate bounds m^2 by O(H+1); therefore H is bounded independently of B, contradicting M>=B for sufficiently large B. This is exactly the parent's height contradiction with strengthened precision.

## Completeness, including foreign denominator primes

Use the parent's true multiplication family X=n, U=[n]H, V=[n](H-R0) and its fixed contact data (including the unchanged difference trace). At selected contact primes mu=1, the parent's prepared formal comparisons have C,I of depth >=3d and J,K' of depth >=4d in the successful respective slots, with d>=1 (separate depths are sufficient), so all nonconstant terms of the new W have positive valuation there. At any other slot with v(c)=-1 the only possible zero-valued nonconstant term is c^2 L_s^2. If it has valuation zero, v(L_s)=1, so the odd summand cJ dominates and v(J)=2. In the true multiplication family at these primes n is a unit. The classification of abscissa valuations shows that v(J)=2 forces H to have unit abscissa and [n]H to be formal of depth one: a formal H gives a multiple-of-four valuation, a point reducing to (0,0) gives either a nonpositive multiple of four (odd n) or zero (even n), and otherwise H has unit abscissa. In the latter case v(C)=-1, so c C^4 has negative valuation. Thus if W is integral all its nonconstant terms are positive, and it is 1 modulo the prime. Otherwise it is a pole. Combining with the successful slot, v_p(D)>0, and the reciprocal gate gives the required pole-input valuation one.

At foreign good primes with v(c)=j>0 odd, the only possible zero-valued nonconstant term is again c^2 L_s^2. Then v(L_s)=-j, so v(J)=-2j. Apply the actual-multiplication identity in Section 3 of the 53-coordinate parent to H,U: v(C)=-j. Hence c C^4 has valuation -3j<0, contradiction to integrality of W, since negative minima are unique. Again every integral slot reduces to 1, and every other slot is a pole. The identity 1+D=(Nm W+1)/Tr W yields v_p(1+D)<=0 exactly as in that parent, so the reciprocal normalizer is a unit and its actual BB input has positive valuation. This checks the foreign odd denominator obstruction, rather than merely the selected contact primes.

At the fixed preparation places and real infinity the unchanged raw comparisons and products are bounded, c tends to zero, W=1+O(c), D=O(c^2). All the parent's contact preparation and pole-input parity arguments apply. In particular its positive seven-adic valuation, class seven at 2, dyadic depth >=4, positive real input <1 and square reduced denominator are preserved. Invoke the same BB realization only after fixing the actual input. The X=0 canonical fiber uses H=2R0, s=S, t=T, Y=Z=d=0, h=t^2/(s-t), whose denominator is nonzero by the v65 zero fiber; both errors and L_s vanish, W=1, and the rest of the parent's preparation is unchanged.

## Reproduction and status

The exact checker rebuilds every changed row from the field equations, retains the parent rows after the detector and its two original power rows, expands the complete sum of squares by integer convolution, and checks the depth inequality on 10,001 odd depths. The depth proof above is uniform; the finite test is supplementary. The B=1 fixture is not a defining specialization. The arithmetic hypotheses and prime-pattern supplier are inherited, not reproved by the checker. Source pin: 6864691d536057574be873667936610da6a4ea99. No new numerical defining threshold, or transfer to the 161/175 general routes, is asserted.

Next goal: eliminate k_s or compress the comparison pair without changing the negative-odd foreign-prime argument. The chart now separates that problem from the moving-difference equation.

Exact algebraic census: `{"variables":52,"rows":42,"parameterSeparatedTerms":1250,"coordinateMonomials":1246,"fixtureMonomials":1246,"fixtureHeight":"5531402752","degree":4,"inputFourth":"1","oddDepthChecks":10001}`.
