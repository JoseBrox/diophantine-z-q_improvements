# Packed quadrics with a reduced reference and Lucas amplifier (v143)

**612 / 632 rational variables; 547 / 565 quadratic residuals** (general / specified). Eight independently certified integers, one scalar pole and two/three comparison poles. The 197-coordinate packed source of [v142](../packed_quadrics_v142/README.md) is unchanged. The new reduction is seven variables and seven rows in each route. Every arithmetic and coding premise of v142 is retained; no extra abc hypothesis is used.

## 1. Two rational coordinates removed from the reference chart

Write K=Q(rho), rho^2=2, D_E=11-6rho, and use the v131 finite difference chart with field registers S,T,F,G,eta,d_*:

    d_*=(eta+S+T)F=eta G,
    D_E(F+G)=(S-T)eta-T^2,
    1=d_*(S-T)-D_E FG.

For pi=eta+S+T the finite difference has x=eta*pi and y=-(eta+T)x-D_E*d_*. The reference difference is fixed at P_0=2R_0, with

    xP=57/8-7rho/2, yP=-165/8+417rho/32.

The reference y equation solves d_* **linearly**:

    d_*=-D_E^(-1)(yP+(eta+T)xP), D_E^(-1)=(11+6rho)/49.

Substitute this affine field expression in every reference row and delete the now tautological ordinate row. The reference abscissa row remains. This is an exact equivalence, not a restriction to a generic affine branch. All degrees are at most two. It saves one field register and one field equation, i.e. two rational coordinates and two residuals. Every private pair and the physical scalar ratio are otherwise unchanged.

## 2. Degree-four Lucas growth residual

Replace the degree-six Pell growth polynomial of v139 by the Lucas residual used in the older scalar-point route v82:

    v=(a-1)b, b=2m+1,
    w=(a+1)v,
    Delta=t^2-tw+v^2-1.

Here a,t,m are the three growth labels, and in the quadratic circuit they are represented by their existing primary field ratios. The field circuit stores v,w,Delta instead of five field helper registers. This saves four rational variables and residuals.

For every consumed comparison prime, v_p(u)=mu>0 is odd, and the successful slot passes all Boolean tests as in v139. For the three growth pairs keep the two reciprocal tests and replace the alternate error-square failure B_5(E_j^2) by B_3(E_j^2). Passing gives v(E_j)>3mu/2, hence valuation at least 2. Division by the formal opposite slope gains at least one. The order-four relative formal logarithm comparison of v131/v133 therefore recovers the three integral index labels modulo p^3: the primary ratio times the reference index is congruent to the primary label and the alternate ratio times the reference index minus one is congruent to the opposite label, and subtraction gives the difference label. This uses only multiplication by integral indices, not their inverses. Test the new residual with B_5(Delta_ratio^2) instead of B_7 of the old residual square. Passing gives v(Delta_ratio)>5mu/2, hence valuation at least 3. The integral polynomial evaluation agrees with the index residual modulo p^3. Thus for each comparison radical M_j,

    M_j^3 | Delta_index, if Delta_index != 0.

The target input tests and their p^2 congruences are unchanged. The powers u^2,u^3,u^5 suffice, instead of u^2,u^4,u^5,u^7, saving one more scalar register and row.

## 3. Global soundness

Use B_idx for the maximum of one and the absolute values of the eleven difference labels, with b=2m+1 included. Let A=|a|. The scalar circuit still gives A>=149^(9N+7) and the v136 linear-target height majorant h(k_i)<=D_N*149^(-9N-7)*A for all eight targets. With a sufficiently large fixed N, the v136 absorption argument gives B_idx^2 bounded by the comparison heights times a fixed constant, with the same constants H,K,C_B chosen as there (enlarging them if needed). All constants are independent of the witness.

If the new integral residual is nonzero then |Delta_index|<=10 B_idx^4, whence h(t_j)<=H M_j^(7/6)<=H(10 B_idx^4)^(7/18). The growth exponent is 14/9, strictly below two. Combining with the aggregate estimate B_idx^2<=2K(1+5 max_j h(t_j)+10) of v136/v133 gives B_idx^(4/9)<=C_B after enlarging C_B to a fixed constant. Hence, for sufficiently large N, the forced scalar label lower bound excludes Delta_index != 0. For the specified route the necessary constants and threshold remain effective under the retained quantitative premises.

Suppose Delta_index=0. Put A0=|a+1|>=3 and v=(a-1)b. Since b is odd, |v|>=|a-1|>1. The norm t^2-(a+1)tv+v^2=1 implies t nonzero and appropriate signs. After replacing t,v by their absolute values, and if necessary swapping, it gives positive integers X>Y satisfying X^2-A0 XY+Y^2=1 (equal values are impossible). Descent replaces (X,Y) by (Y,A0 Y-X); indeed X(A0 Y-X)=Y^2-1, so for Y>1 the new second coordinate lies strictly between 0 and Y. For Y=1 it is zero and X=A0. This proves that the positive values are consecutive terms of the Lucas sequence U_0=0,U_1=1,U_(j+1)=A0 U_j-U_(j-1). In particular |v|=U_j for some j>=1.

Modulo |a-1| the recurrence parameter A0 is 2 if a>0 and -2 if a<0, hence U_j is congruent to j or (-1)^(j-1)j respectively. Since |a-1| divides v, one gets j>=|a-1|>=A-1. Monotonicity of the recurrence gives U_j>=(A0-1)^(j-1). Since |v|<= (A+1) B_idx, this yields

    log B_idx >= (A-2) log(A-2) - log(A+1).

For A>100 this exceeds A/4+log A. For example log(A-2)>4 and log(A+1)<A/2 suffice. But if any input comparison residual J_i is nonzero, the unchanged v136 comparison-height estimate gives log B_idx<=h(k_i)+log C_B. Choose N large enough to make h(k_i)<A/4 and C_B<A. This is a contradiction, so every target equals its integral index and all eight certified source inputs are integral. The v142 packing proof finishes soundness.

## 4. Completeness

After choosing the positive scalar label a in 6Z, as in the original v136 preparation, use the Lucas sequence with parameter a+1 and n=a-1. Set v=U_n, t=U_(n+1), b=v/(a-1), m=(b-1)/2. The Lucas norm is one by induction. Reduction modulo a-1 gives U_n=n=0 modulo a-1. Modulo 2 the odd recurrence parameter gives period three, and n=5 modulo 6, so U_n and b are odd. Growth makes b>1 and all the chosen labels positive. Thus the new integral residual vanishes with the required labels.

Choose the difference points and all aggregate and contact shifts after this scalar and label choice. The v139 simultaneous prime/CRT, fixed-place and real preparation proof is unchanged: the reference chart substitution preserves all physical data, and the chosen synchronized formal depth gives the old stronger alternate-error and polynomial-residual precision (at least 3d and 4d respectively, where d>=1). Hence the relaxed exponents 3 and 5 pass. The Boolean limits and BB pole preparations are unchanged. The fixed larger scalar multiplier retains all v142 positivity and dyadic conditions.

## 5. Artifacts and verification

The included independent verifier checks parameter-uniform support and matching, direct modular evaluation of the complete radix prefix, six actual builds and 68 exact toy carry fixtures (two positive). The separate Lucas verifier checks 20 positive completion cases, 35 enumerated small norm-one pairs, the inverse constant and byte-for-byte regeneration of four v142/v143 fixtures. The two builders use pinned v128 source data. The fixture coefficients x=100,z=u=y=1 are not claimed universal or known solvable; the theorem and compiler are uniform for every positive x,z,u,y with x>32z, so a fixed nonrecursive projection follows on choosing the universal coefficients of Jones's coding theorem. The compiler emits exact sparse quadratic residuals, whose sum of squares is the quartic after fixing the defining parameter C_parameter. The results give upper bounds, not global minima. No full CI, numerical rational witness, independent arithmetic-premise proof or six/seven-integer transfer is claimed.
