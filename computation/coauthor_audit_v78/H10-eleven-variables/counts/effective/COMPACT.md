# A quadratic input and a normalized split contact product

Under the same full-family modular, elliptic, prepared-pole and compatible prime-selection inputs specified in PROOF.md, the finite specification in compact117/explicit27 defines $\mathbb Z$ over $\mathbb Q$. It uses 27 variables including the input. Its degree is at most 702,371,856,384, its support is below $2^{956}$, and its maximum absolute coefficient is at most $2^{96366166540288}<2^{2^{47}}$. These are bounds on the finitely specified polynomial.

## Scalar formula

For odd $L\ge117$ put $p_*=167$ and set
$$
 \beta=102X^2+2957,\quad A=\beta(\beta-1)(\beta-2401),\quad
 B=(32\beta+343)(\beta+24),\quad T=102^2(p_*^{(L+1)/2}+2)^2,
$$
$$
 q=\frac{TA}{B},\qquad
 \rho=102^2p_*^L\frac{q}{(1+q)^2}
      =\frac{102^2p_*^L T A B}{(B+TA)^2}.
$$
The three arguments, all ten contacts at each argument, and their scalar and comparison tests are those of PROOF.md with this $\rho,\beta$. The input test uses $\beta$ itself. For the four root roles keep the square-abscissa chart. Use the larger v72 full-abscissa chart for the five auxiliary roles and the v75 reciprocal-abscissa weights for all three comparison arguments. Use the termwise positive determinant of h193/fewvars/POSITIVE.md.

## Scalar radical and fixed prime

Use the set $\Gamma_u$ of PROOF.md. For the scalar radical, add the supports of differences among $0,1,2401,-343/32,-24$. This adds only 97. At a prime outside the resulting $\Gamma_\beta$, negative $v(\beta)$ equals $2v(X)$ and cannot be an odd denominator contact. At a finite positive odd contact, exactly one of the factors of $AB$ has odd positive valuation. Thus $v(q)$ is odd, since $T$ is a square. For any nonzero rational $q$ with odd valuation, $v(q/(1+q)^2)=|v(q)|$. This gives odd positive valuation of $\rho$ at each contributing prime other than $p_*$.

For $X$ integral at $p_*$, exhaustive checking of its 167 residues gives
$$
                    A B\bigl(B+(204)^2 A\bigr)\not\equiv0\pmod {167}.
$$
Consequently $v_{167}(\rho)=L$ and 167 is absent from the scalar radical. For $v_{167}(X)=-e<0$, the valuations of $\beta,A,B,q$ are $-2e,-6e,-4e,-2e$, respectively. Thus $v_{167}(\rho)=L+2e$ and the denominator contact in $\beta$ is again even. The prime 167 is outside $\Gamma_u$. As before, some $R_j$ is a unit there and gives $167^{2L+1}\mid c$. Together with the scalar radical this proves $167^{2L+1}M_\beta^3\mid c$.

The smaller product $J=\prod_{\Gamma_\beta}p$ satisfies the same certified modular bound $2C_*J^2E(J)\operatorname{bitlength}(J)<2^{342}$. The contact sets for the comparison arguments are precisely those in PROOF.md, so the same $K=2^{551}$ and the shift 199 work.

## Effective size and soundness

As integer polynomials of $\beta$, $A,B$ have degrees three and two, and coefficient 1-norms 4804 and 9375, respectively. The height of the displayed degree-six rational function is at most $6h(\beta)$ plus the logarithm of the greater of
$$
       102^2 p_*^L T\|A\|_1\|B\|_1,\qquad
                       (\|B\|_1+T\|A\|_1)^2 .
$$
Using $T\le4\cdot102^2p_*^{L+1}$, either expression is bounded by $p_*^{2L}$ times a positive integer below $2^{128}$. Hence $h(\rho)\le 6h(\beta)+2L\log p_*+128$. In particular the weaker scalar height bound used in PROOF.md applies. The unchanged three-scale abscissa sum depends only on the four root roles, so its effective quadratic label-height bound remains valid. Since $167^{235}-1\ge2^{1735}$, the two quantitative contradictions in PROOF.md apply for every odd $L\ge117$. They give $\beta=n\in\mathbb Z$. For $X=u/v$ reduced this implies $v^2\mid102$, and 102 is squarefree.

For completeness of the local interpretation with the enlarged charts, v72 gives half-integral labels $h,j_i$ for the five auxiliary roles by $2H=[2h]P$ and $2U_i=[2j_i]P$. At each consumed prime they are integral since the primes lie outside $S$, which contains 2. The local formal group has no nonzero 2-torsion and the doubled logarithm identities yield the same ratios $(a-1)/h$, $j_i/h$ and $(j_i-n_i)/(h-1)$. All root labels remain integers. For every first-ten reciprocal-abscissa test its valuation is even because $D$ is a unit there and $E$ has equation $y^2=x^3-Dx$. The v75 unsquared reciprocal numerators therefore retain the needed valuations, including at the small-cutoff primes. Squaring each raw factor argument in the termwise positive construction doubles its nonpositive valuation contribution and preserves the needed local implications. All these arguments apply to every one of the three local products separately.

## Complete witnesses and denominator

Every integer $X$ gives an odd positive $\beta\ge2957$. In particular $A,B>0$ and $B/A<1$ because $32\beta+343<33\beta$, $\beta+24<2\beta$, and $(\beta-1)(\beta-2401)> 66\beta$. Thus uniformly over real $X$,
$$
                0<\rho<\frac{102^2p_*^L}{T}\frac BA<\frac1{167}.
$$

Write $q=a/b$ reduced with $b>0$. Then $q/(1+q)^2=ab/(a+b)^2$ and $\gcd(ab,a+b)=1$. Outside 167 multiplication by $102^2p_*^L$ adds an even valuation. At 167 the valuation of $\rho$ is positive. Hence every negative valuation of $\rho$ is even and the reduced denominator is a square. This coprimality accounts for primes shared by the displayed polynomial numerator and denominator before the normalization.

For integral $X$ the possible $\beta\bmod8$ are 3 and 5. Both $\beta(\beta+24)$ and $(\beta-1)(\beta-2401)$ are squares in $\mathbb Q_2$: for the second product use $v_2(\beta-1)\le2$ and $v_2(2400)=5$. The remaining $32\beta+343$ is 7 modulo 8, cancelled by $167$. At 3 and 17, $\beta$ is respectively 2957 modulo each prime and $AB$ is a unit with $167AB$ a nonzero quadratic residue. Thus $\rho$ is a square at these three places. Also $v_2(A)>0$, $B$ is odd, and $T$ is divisible by $2^2 3^2 17^2$. At 3 and 17 both $A,B$ are units. Therefore $v_2(q)>0$, $v_3(q)>0$, $v_{17}(q)>0$, and the valuations of $\rho$ are at least 4, 2 and 2 there. The prepared pole converse requires depths at least 3, 1 and 2 respectively.

These give precisely the scalar size, local squareclasses, depth and square-denominator hypotheses used in the ordered three-scale completeness proof of v19. At the support of $\rho$ impose the original finite neighborhoods before applying simultaneous prime selection to the three lists of affine contacts. This preparation permits any required positive depth at two. Fresh primes avoid the entire fixed support. On the successful embedding the ten unsquared v75 reciprocal numerators have valuation at least two, so their weighted summands have positive valuation, also after the termwise squaring. At the other embedding their nonzero raw summands have odd valuation, so the inverse of the factor after squaring reduces to zero or one. At finite preparation places and the real place, the bounded raw comparison terms tend to zero with the inverse normalizer; the scalar terms can be chosen small as before. All nine prepared points may lie in the old square-abscissa subfamily. The v72 full-auxiliary whole-character transfer and termwise positivity preserve the determinant guards. The original pole realizations and three independent finite square-root blocks then supply a witness for every integer $X$.

## Reproduction

Run build_compact.py, check_L53.py and check_compact.py from this directory with Python 3. The last checker reconstructs the scalar and the three arguments, contact weights and scalar factors by exact circuit arithmetic. It compares the unchanged local tests, both logarithm gauges and all nine point charts with the pinned construction. It independently replays all 66 termwise factors, 534 denominator checks, 69 positivity-certified atoms, and 100 retained norm factors before checking the determinant degree, support and coefficient majorants. Its finite arithmetic checks include the forced prime, preparatory primes, scalar height constant and sufficient fixed exponent. The source SHA-256 is 913592914b8e6e9a0d9c7923ebceb2a815cdbcbafd8648fe66b77334cff6c54f.

The chart and reciprocal-test sources are papers/few_variables25/full_auxiliary25_20261117_v72.tex and papers/few_variables25/even_valuation25_20261117_v75.tex. The arithmetic and determinant sources named in PROOF.md apply with the changes proved here.
