# Exact module specification for the primary degree-eight candidate

The frozen construction is `final/`, built by default options of `build.py` (output directory specified with `--out final`). It has one free rational input X and 15,671 rational witnesses. There are no imported polynomial files, opaque coefficients, mathematical searches, or external Python dependencies.

All field-valued notation means ordered pairs of rational coordinates for F=Q(sqrt(2)). The operations are

    (a,b)+(c,d)=(a+c,b+d),
    (a,b)(c,d)=(ac+2bd,ad+bc),
    conjugate(a,b)=(a,-b),  norm(a,b)=a^2-2b^2.

A field equation contributes its two rational coordinate equations. Every emitted rational residual is multiplied by the lcm of its coefficient denominators and divided by the positive gcd of the resulting integer coefficients. The final polynomial is the sum of the squares of these integer residuals. Consequently it has degree eight and integer coefficients; this precise normalization is part of the polynomial specification.

## Fixed curve and constant chain

    d=3-sqrt(2), D=d^2=11-6sqrt(2),
    E: y^2=x^3-Dx,
    P=(57/8-7sqrt(2)/2, -165/8+417sqrt(2)/32).

The point P is the image of the preceding generator under x'=lambda^2 x, y'=lambda^3 y, lambda=3+2sqrt(2). The fixed point [4]P is computed by two ordinary doubling circuits, rather than recorded by large rational coordinates.

There are 25 shared rational variables c_0,...,c_24, with residuals c_0-3 and c_{i+1}-c_i^2. Thus C=c_24=3^(2^24) is represented without a large literal coefficient.

## Point chart and arithmetic operations

A nonzero point of G=2E(F) is represented by eight field variables u,v,w,z,f,h,x,y (16 rational witnesses) satisfying

    f=u^2,
    v^2+d f=1,
    w^2+v^2=2,
    h=vw,
    zh+u=0,
    xf=1,
    yz+x=0.

Thus f=1/x and z=-x/y. The inverse equation xf=1 enforces the required nonzero chart guard. This is the ten-variable core chart with f,x,y explicitly named to maintain sparse low-degree equations.

Multiplication and inversion of field expressions are encoded by naming their two rational coordinates and equating their products. Doubling uses

    lambda=(3x^2-D)/(2y),
    x_2=lambda^2-2x,
    y_2=lambda(x-x_2)-y.

For subtraction of points (x,y),(r,s), use field variables lambda,nu,x_o,y_o,F_o,Z_o and a rational inverse of norm(x-r). The field residuals are

    lambda*x-y-nu,
    lambda*r+s-nu,
    x_o-lambda^2+x+r,
    lambda*x_o+y_o-nu,
    F_o*x_o-1,
    Z_o*y_o+x_o.

The norm inverse enforces x != r. This introduces 13 rational witnesses and 13 scalar residuals. Naming the line intercept nu substantially reduces expanded support.

## Formal logarithm

At precision 64 use

    ell(z)=z sum_{j=0}^{15} c_j (Dz^4)^j,
    c_j=(-1)^j binom(2j,j)/(4j+1).

Let w=Dz^4. Evaluate the degree-15 polynomial using eight two-term blocks c_{2i}+c_{2i+1}w, with Horner multiplication by w^2. Every field multiplication is assigned its two coordinate witnesses. Two-term blocks produce a smaller expanded coefficient table than the four-term blocks that minimize the number of multiplication witnesses.

## Seven-variable parity predicate

For rational input b, put B=17b. Seven rational witnesses t,U,e,p,q,s,h satisfy

    U(1+bt^2)-b(1-bt^2)=0,
    p^2-B(1-e)(1+3e)=0,
    h-e(B-U^2)=0,
    Bq^2-(s^2-Bh)(s^2+3Bh)=0.

This is the shared module `q_primeparity`; its four residuals have degree at most four. It is used 42 times in the instantiated construction.

## Binary norm batch

For nonzero r and rational tests X_i with prescribed orders L_i, form a binary tree with leaves 1 and X_i/r^{L_i}; internal nodes are N_r(a,b)=a^2+r b^2. The constant leaf remains on the left branch at every level. The first pair is encoded as

    r v-r-X_1^2=0

because L_1=1. Remaining tests are paired in increasing order within each equal-order group. A pair X_i,X_j of order L is encoded as

    v r^{2L}-X_i^2-rX_j^2=0.

An unpaired leaf is encoded by v r^L-X_i=0. Thereafter consecutive nodes are paired; an unpaired node is carried to the next level unchanged. Shared powers of r are formed by repeated squaring. If W is the final node, the ordinary contact batch invokes the parity predicate at rW^2.

The local four-index module uses 41 tests with orders

    (1 repeated 23 times, 64 repeated 18 times).

Its batch contributes 51 direct witnesses and 51 direct residuals, plus the seven parity witnesses and four parity residuals: total 58 witnesses and 55 residuals.

The scalar-height batch uses six tests with orders (1,1,1,1,48,48). It additionally has Boolean variables epsilon_p for p=2,3,5,7,11,13,17 and eta. Put

    A=(1+epsilon_2)(1+2epsilon_3)(1+12epsilon_13)(1+16epsilon_17),
    B=(1+4epsilon_5)(1+6epsilon_7)(1+10epsilon_11)(1-2eta).

Name A and B by quartic equations and invoke the same parity predicate at AB rW^2. The correction is supported at the fixed bad primes and permits the positive local square conditions at 2,3,17. This batch contributes 34 witnesses and 31 residuals including the parity call.

## Local four-index comparison

Its inputs are proxies a_1,...,a_4; [4]P and [4]Q_i; conjugate(f(J)); inverse(conjugate(z(J))); a rational square-root approximation theta; epsilon=theta^2-2; and the contact r.

Introduce H,X_1,...,X_4 in G using the point chart; put Q_0=P, X_0=H, and Y_i=X_i-[4]Q_i. The eleven order-one field expressions are

    f(H), f(X_1),...,f(X_4), conjugate(f(J)),
    conjugate(f(Y_0)),...,conjugate(f(Y_4)).

The nine order-64 field expressions are

    ell(z(X_i))/ell(z(H))-a_i (i=1,...,4),
    conjugate(z(Y_i))/conjugate(z(J)) (i=0,...,4).

Each field expression A+B sqrt(2) is replaced by the two rational tests epsilon B and A+B theta; epsilon itself is the first order-one test. This gives 23 order-one tests and 18 order-64 tests. The full module has 373 witnesses and 360 residuals.

## Anchor

For each coordinate f_i of f(S), introduce a_i with C a_i=f_i and seven rational witnesses satisfying

    u_0^2-2u_1^2-3u_2^2+6u_3^2=1,
    (a_i-2u_0)^2-8v_1^2-12v_2^2+24v_3^2=4.

There are 16 witnesses and six residuals. Applying the anchor directly to the scaled f-coordinates is equivalent to the old coordinates because the transition matrix [[17,24],[12,17]] and its inverse are integral.

## Root construction

Put beta=X^2+2. Introduce nonzero G-points A,S,T,Z and rational proxies s,t,z, and impose

    t^2-s(s-2)tz+(s-2)^2 z^2=1.

Apply the anchor to S. Introduce J_0 in G and apply the scalar-height batch with

    r=beta(beta-1)(beta-2401)(32beta+343)(2beta-1)

and the six rational coordinates of f(J_0), f(S), z(S)/z(J_0).

Introduce one common J in G for all local comparisons. Choose a nonzero rational coordinate denominator e and name the nine scalars

    e, e*x(A)_0, e*x(A)_1, e*x(S)_0, e*x(S)_1,
       e*x(T)_0, e*x(T)_1, e*x(Z)_0, e*x(Z)_1.

For these scalars a_i set A_i=47027 a_i+3. Introduce common u,v and use the 41 contact values

    v/(32W), u, u-v, u-2401v, u+343v/32,
    u-A_i v, u-(A_i-1)v, u-(A_i-2401)v, u-(A_i+343/32)v,

for i=1,...,9, where W=25878772920. At each contact invoke the four-index module with proxies (beta,s,t,z), points (A,S,T,Z), and the same J,theta,epsilon.

## Exact count hierarchy

| Module | Direct private variables | Direct scalar residuals | Calls |
|---|---:|---:|---|
| Parity | 7 | 4 | none |
| Anchor | 16 | 6 | none |
| 41-test batch | 51 | 51 | one parity |
| 6-test height batch | 27 | 27 | one parity |
| Four-index comparison | 315 | 305 | one 41-test batch |
| Root | 303 | 285 | one anchor, one height batch, 41 comparisons |
| Shared constant chain | 25 | 25 | none |

Hence the witness count is 25+303+16+34+41*373=15671, and the residual count is 25+285+6+31+41*360=15107. The reusable module table contains only 703 stored residuals and 46 stored call instructions. Calls allocate distinct private witnesses.
