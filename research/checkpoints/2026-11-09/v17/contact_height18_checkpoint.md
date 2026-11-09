# Exact exponent 18 for the inherited five-contact height estimate

Status: proof derived 2026-11-09; independent review requested. This is an implication of the same geometric and modular construction used in the pinned upstream five-contact theorem. No abc inequality is added. It is not, by itself, a variable-count improvement.

## Source

Elliot Glazer, `diophantine-z-q`, commit
`14e8f601fe0d9173d4a5f084aedc3e07066a7688`,
`manuscripts/quartic_v9.tex`, proof of `hyp:o8-height`, equations (LR2)--(LR5), followed by `thm:quartic-height19`.

Put B = product of primes p <= 76176, M = the source odd five-contact radical, R = B M, and C = 210^300. R is squarefree and divisible by 2. The source construction gives:

* a geometric inequality h(a) <= 2 max(0,h_F(A)) + 128;
* a CM estimate h_F(A) < 854R;
* in the non-CM case, [L:Q] <= 576, a scalar character of order m, and an extension L'/Q;
* the **unrelaxed** scalar-character bound m <= 2 product_{odd p|R}(p-1) = 2 phi(R), from (LR2);
* d' = [L':Q] <= 2m[L:Q] <= 1152m <= 2304 phi(R), from (LR3);
* a primitive weight-two newform of level N <= C R^2, rad(N)|R, whose nebentypus epsilon satisfies epsilon^2|_{G_L'} = 1.

Consequently t = ord(epsilon) <= 2d' <= 4608 phi(R).

For H = ker(epsilon), the modular curve X_H has Belyi degree at most

    d_H = Nt product_{p|N}(1+1/p)
        <= 4608 C R^2 phi(R) product_{p|R}(1+1/p)
        = 4608 C R^3 product_{p|R}(1-1/p^2)
        < 4608 C R^3.

The crucial cancellation removes the extra R^(1/6) previously introduced by bounding the Euler product independently of the character order.

Set T = 2^14 C R^3. Then g = dim J_H < T, d_H < T, T >= 16, and log d' < 8 + log R <= 8 + log T. The source argument now applies verbatim:

    h_F(J_H) <= 13000000 d_H^5 g < 2^24 T^6;
    V <= 16T^4(2+log T) + 2T^2(25+7log T) <= T^6;
    h_F(Z) > -3g/2;
    h_F(A) < (2^24+1)T^6 + 3T/2 < 2^25 T^6.

Here J_H is L'-isogenous to A x Z and V is exactly the isogeny-height correction already used in the source. The CM estimate is smaller as well. Therefore

    h(a) <= H18 M^18,
    H18 = 2^110 * 210^1800 * B^18 + 128.

The source coarse B < 2^109445 and 210 < 2^8 give

    H18 < 2^(111 + 14400 + 18*109445) = 2^1984521.

The additive 128 is absorbed because M >= 1. This is a bound for logarithmic height h, not for multiplicative height.

## Character-order refinement not needed for exponent 18

At each odd p one can choose an odd Dirichlet character modulo p of order 2^{v_2(p-1)}. Their product has order the maximum of these powers of two, together with at most 2 at the prime 2. Thus the source can use

    m <= max(2, max_{odd p|R} 2^{v_2(p-1)}).

This supplies a sharper support-sensitive bound. It does not give a better universal power of R, and the source soundness proof does not restrict all contact primes to a fixed congruence class. No count reduction is claimed from it.

## Original literature used by the inherited proof

* A. Javanpeykar, with appendix by P. Bruin, Polynomial bounds for Arakelov invariants of Belyi curves, Algebra & Number Theory 8 (2014), 89--140, Theorem 1.1.1 and Section 2.3, DOI 10.2140/ant.2014.8.89.
* E. Gaudron and G. Remond, Nouveaux theoremes d'isogenie, Memoires de la SMF 176 (2023), Theorem 1.9(1), pages 7--8, DOI 10.24033/msmf.484.
* R. von Kaenel, The effective Shafarevich conjecture for abelian varieties of GL2-type, Forum of Mathematics, Sigma 9 (2021), e39, equation (2.2) and equations (4.1)--(4.2), DOI 10.1017/fms.2021.29.

## Remaining research question

The exponent 18 comes from the generic Belyi-Jacobian estimate of degree six. A verified estimate for arbitrary modular quotients X_H with height substantially below d_H^6, or a sharper comparison with a fixed-dimensional factor, could improve the exponent further. Squarefree-level asymptotics for X_0(N) do not automatically apply here.
