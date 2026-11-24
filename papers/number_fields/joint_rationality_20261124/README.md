# Joint rationality descent with common elliptic denominators

## Result and hypotheses

Retain precisely the hypotheses of the [ten-coordinate selector](../ten_coordinate_rationality_20261119_v81.tex) and [amplified descent theorem](../amplified_rationality_descent_20261119_v81.tex): a fixed number field K, a curve E/Q of positive rank stable in K, the six-point truncated-height bound (e.g. abc over K), and the published class-seven pole completeness theorem. The ineffective finite correction H is the one from the predecessor, not a new assumption.

For every fixed k>=1, the relation Q^k inside K^k is defined by a single integer-coefficient polynomial in **7k+3 total K-coordinates**, counting the k distinguished inputs. All witnesses can be rational when all inputs are rational. No claim about effective coefficients or a new single-input count is made.

In consequence, any N-coordinate integer definition over Q gives a definition of Z in K in **7N+3** coordinates; using an integral basis gives a definition of O_K in **7N[K:Q]+3** coordinates over K (basis constants allowed as in the predecessor). For N=11 these are **80** and **157** in the quadratic case, instead of 110 and 220. This retains the rational integer definition's separate arithmetic and abc assumptions. For a nonquadratic K the stable-rank hypothesis must still be established; the quadratic case uses the cited Zywina theorem.

## 1. Joint density of ratios with a common denominator point

Let m be a fixed positive integer with mE(K) contained in E(Q), and xi=-x/y on the same guarded chart as v81. For any finite list of rational targets q_i, any finite set of rational primes and prescribed open real and local neighborhoods of all q_i, and finite avoidance sets, there are rational points U_1,...,U_k,V in mE(Q) with nonzero affine xi, all admitting rational preimages under [m], for which the ratios xi(U_i)/xi(V) meet all the conditions.

Proof: by weak approximation first choose nonzero rational r_i in the specified neighborhoods, avoiding the finite sets, and shrink the neighborhoods to exclude the forbidden values. Express all r_i=a_i/b with a common nonzero integer b and nonzero integer a_i. Choose a non-torsion Q in mE(Q) sufficiently deep in every prescribed finite-place formal group. Integral formal multiplication gives xi([a_i]Q)=a_i z+z^2 F_i(z), xi([b]Q)=bz+z^2 F_b(z), z=xi(Q), and the valuation of the difference from a_i/b is at least v_p(z)-2v_p(b) whenever v_p(z)>v_p(b). The same bound holds simultaneously for the finite list. The positive-rank subgroup lying in these neighborhoods has a non-torsion point; multiples of it approach the identity in the compact real group while preserving all finite-place conditions. Thus the ratios converge simultaneously really to r_i. Deep formal neighborhoods give nonzero x and y, so all guards hold. Take U_i=[a_i]Q and V=[b]Q. Since Q belongs to mE(Q), rational preimages exist. This is the predecessor density proof with a common denominator b; it does not claim density with an already fixed denominator point.

## 2. Ordered construction

Write f(T)=(T^3-2)/(T^3-3), g_i=f(t_i). Use two separate common denominator points V_1,V_2 and numerators U_i,W_i, all in mE(K), and put lambda_i=xi(U_i)/xi(V_1), beta_i=xi(W_i)/xi(V_2). The two detector values for input i are exactly those of v81:

    b_i1=(lambda_i-g_i)^2 (1+g_i)^2/g_i^3
    b_i2=(beta_i-t_i)^2 ((1+lambda_i)^2/lambda_i)^3.

Use the 16 signed multipliers from v81 and the two independent prepared-pole predicates for each i. Require the same H(t_i)!=0. Any accepted tuple supplies each individual v81 witness, so soundness is componentwise.

For completeness fix rational t_1,...,t_k. First apply joint density to the g_i at the union of the supports of g_i(1+g_i) and 2,3,5,7, and at the real place. Avoid lambda_i=0,+/-1,+/-g_i. This prepares all b_i1. Only **after** these choices fix the actual lambda_i and form the finite union of the supports of t_i (when nonzero), lambda_i(1+lambda_i), and 2,3,5,7. Apply joint density a second time, with an independent common denominator point, approximating the t_i and avoiding beta_i=+/-t_i and 0. This prepares all b_i2. The estimates are exactly the local and real estimates of v81: at every prime outside the relevant union, valuations of the corresponding b are even; inside it they can be made arbitrarily large. Each b is nonzero with absolute value less than 1. The prescribed dyadic and 3,5,7 depths allow a multiplier mu in the original 16-element menu with d=b/mu prepared in class seven.

Each pole has independent ordinary parameters v,s and an algebraic root Y with Y^2=P_d(v,s), where P_d=d(d+v^2)^2 s^4-d(d-v^2)^2(1-d)^2. By the predecessor class-seven density lemma, rational witnesses may avoid the product of all nonzero other-character radicands. No identification of the two stages' common points or of distinct pole parameters is used.

## 3. Exact finite determinant

Use one ordinary abscissa for each of the 2k+2 rational preimages of U_i,V_1,W_i,V_2. With E:y^2=F(x), adjoin their ordinates by monic equations Y_P^2=F(X_P). This point algebra A0 has rank 2^(2k+2). Write xi([m](x,y))=y u_m(x)/v_m(x) exactly as in v81. For each ratio, use the two corresponding ordinate generators and the numerator/denominator prescription of v81 section 4. Shared denominator abscissas and ordinates are literally the same generators in every appropriate ratio. Substitute these ratios into the v81 scalar-denominator expressions A_i1/B_i1, A_i2/B_i2 for the b values, using the same formulas and each t_i.

For each of the 16^(2k) choices of multipliers put C_ij=mu_ij B_ij, and adjoin monic generators W_ij^2=R_ij where

    R_ij=A_ij C_ij^3 (A_ij+C_ij v_ij^2)^2 s_ij^4
         -A_ij C_ij (A_ij-C_ij v_ij^2)^2 (C_ij-A_ij)^2.

The rank of A is n=2^(4k+2), with the basis of squarefree monomials in the 4k+2 named generators, adjoining all point roots first and then all pole roots. The guards G_* are the product of H(t_i), the three map numerator/denominator guards of each input, F(X_P)u_m(X_P)v_m(X_P) for each point, and all A0 multiplication norms of A_ij and R_ij. These are polynomial guards with integer coefficients. A0 and A are etale whenever G_*!=0. At the constructed rational point all point-chart guards hold for every sign choice, since shared signs can only send each lambda_i or beta_i to its negative. Our avoidance choices ensure that A_ij is nonzero at every sign character. Each other-character radicand is a nonzero polynomial in its own independent pole parameters, as in v81; the dense rational choices avoid the finitely many such zeros. Hence G_*!=0 and the full algebra has a rational character.

Order the 4k+2 generators explicitly by first listing the two denominator points, then the k first-stage numerator points, then the k second-stage numerator points, then the pole roots in lexicographic order (i,j). For an integer h set alpha_h=sum_{j=0}^{4k+1} h^j Z_j. Let M_h be its multiplication matrix in the displayed basis and Delta_h the determinant of the column matrix of 1,alpha_h,...,alpha_h^(n-1). Among the integers 1,..., (4k+1)*binomial(n,2)+1 there is a separating h: each pair of distinct geometric characters excludes at most 4k+1 values, and separation gives Delta_h!=0 by the Vandermonde identity. With G_h=G_* Delta_h use

    D_h(E0)=det(G_h (E0 I_n - M_h)-I_n).

If G_h=0 its determinant is (-1)^n=1, hence a zero forces G_h!=0. Then alpha_h generates A and a K-root of D_h is exactly a K-character translated by 1/G_h. Conversely a character chi yields E0=chi(alpha_h)+1/G_h, rational if the base tuple and character are rational. The product over the finite multiplier and h menus is the required single polynomial. This is a finite literal determinant prescription, not an assertion that a rational character implies an arbitrary prescribed root.

If d_M bounds degrees of multiplication-matrix entries for all generators and g bounds degree of G_*, then deg Delta_h <= n(n-1)d_M/2, by degrees of its columns. A single determinant has degree at most n(1+g+n(n-1)d_M/2+d_M); multiplying by the number of menu factors gives a finite degree bound in the fixed data. No numerical bound independent of the ineffective correction is asserted.

## 4. Census and composition

The retained variables are k inputs, 2k+2 point abscissas, 4k independent pole parameters, and one encoder E0: total 7k+3. At k=1 this is the original ten-coordinate selector. For N integer-definition coordinates apply the joint selector to all N, and combine its polynomial with the original integer-definition polynomial using the norm from a quadratic extension of K (choose a rational prime unramified in K and use the corresponding Eisenstein polynomial). This combines equations without variables and enforces the original rational witnesses, not just K-valued ones. The count is 7N+3. 

For an integral basis 1,omega_2,...,omega_d, use d copies of the rational integer polynomial, jointly rationalize their dN input and witness coordinates, and substitute the first integer coefficient by T-sum_{i=2}^d n_i omega_i. This is an invertible affine substitution with the distinguished ambient input T and preserves the total count 7dN+3. Combine d+1 residuals by the norm of the power basis of an Eisenstein extension of degree d+1 over K. The resulting polynomial is over K, with integral coefficients in O_K if the input polynomials are integral and the integral basis is used. No extra rationality assumption on the ambient distinguished input T is made. The result is a number-field definition, not a quartic or a result about rational variable counts.

## Attribution and limitations

The rationality-descent architecture is due to Pasten and Vidaux; the amplification, two-stage prepared-pole argument, and original guarded encoder are v81 project work, and the pole theorem is due to Bhargava and Burungale. The common-denominator density lemma and joint tensor encoder above are the present deductions. Both stage ordering and all character guards are essential. There is no proof here that one can share a denominator *between* the first and second stages, nor one that fixes the new primes of the first-stage ratios in advance. No new single-input rationality bound or smaller Z-over-Q definition follows.
