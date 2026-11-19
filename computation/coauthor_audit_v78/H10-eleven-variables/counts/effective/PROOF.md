# An effective coefficient parameter for the three-scale construction

Every odd $L\ge53$ suffices in the 27-variable explicit27 v19 family. This assumes the pinned normalized elliptic group, full-family modular height theorem H4.1, prepared pole theorem, and simultaneous prime selection and compatible index progressions. Completeness for integer inputs is the v19 proof for every odd $L\ge3$.

## Scalar and comparison primes

Use the v19 labels, scalar $\rho$, scales $t_j=A_j\lambda$ and functions $R_j$. Thus $A_0=1$, $A_1=(1+\rho U^2)^2$ and $A_2=(1+\rho V^2)^2$. Write $\Theta=\{0,-1/2,-1,1/2399,-32/407\}$, $T_j=(4j+2+\Theta)\cup(4j+4+\Theta)$, $Y_j=T_j\cup\{-j-1\}$, $c=|a-1|>0$, $B=\max(1,|n|,|a|,|t|,|b|)$, and $\beta=u/v$ reduced with $v>0$.

Let $S=\{2,3,5,7,11,13,17,37,41,2399\}$. Add all numerator and denominator primes of elements of $Y_0$, and all primes dividing both $\operatorname{num}(x-y)$ and $\operatorname{num}(x-z)$ for $x\in Y_0,y\in Y_1,z\in Y_2$. This gives $\Gamma_u=S\cup\{19,23,457,4799\}$. All three sets' denominators have support in $S$.

Suppose $p\notin\Gamma_u$ and $v_p(\rho)$ is odd. If $v_p(\lambda)\ne0$, $R_0$ is a unit because every element of $Y_0$ is a unit. If $\lambda$ is a unit, each $t_j$ either has negative valuation, giving $R_j\equiv1$, or satisfies $t_j\equiv\lambda\pmod p$. Indeed each of $\rho U^2,\rho V^2$ is zero or has odd valuation. When all three arguments are integral, three nonunit $R_j$ would force $\lambda\bmod p$ to occur in all three $Y_j$, excluded by the construction of $\Gamma_u$.

A unit $R_j$ suffices for the scalar extraction of v19 (trace lemma and scalar lemma), which gives $v_p(\rho)>0$ and $v_p(c)\ge2v_p(\rho)+1\ge3$. The good-prime formal-logarithm bound $\log_E(z)/z\in1+p^{4v(z)}\mathcal O$ is proved in v68, section 3, on this same curve and parameter for every prime outside $S$. It also supplies precisely the local precision used in the mixed comparison lemma of v19.

To obtain $\Gamma_\beta$ add to $\Gamma_u$ the support of pairwise differences within $\{0,1,2401,-343/32,1/2\}$. The new primes are 359 and 4801. Let $M_\beta$ be the odd five-contact radical of $\beta$ outside $\Gamma_\beta$, with contacts $\infty,0,1,2401,-343/32$. Negative valuations of $\beta$ are divisible by four outside this set. At a contributing numerator prime exactly one of the five factors of $r=\beta(\beta-1)(\beta-2401)(32\beta+343)(2\beta-1)$ has positive valuation, and $1+C_Lr$ is a unit. For $\ell=76249$, enumeration modulo $\ell$ excludes all five finite roots of $r$ for integral $X$ at $\ell$. Nonintegral $X$ has $v_\ell(\beta)\in4\mathbb Z$. Independently $v_\ell(\rho)$ is odd and at least $L$ by the scalar normalization theorem. Therefore
$$
                    \ell^{2L+1}M_\beta^3\mid c .
$$

Let $\Gamma_j$ add to $\Gamma_u$ every prime in the support of a difference within $Y_j$. Let $M_j$ multiply the primes outside $\Gamma_j$ at which $v_p(R_j)$ is positive odd. For any such $p$, odd $v_p(\rho)$ gives $p^3\mid c$. For even $v_p(\rho)$, the mixed comparison lemma gives $p^3\mid\Delta$ and $p\mid u-nv$, where $\Delta=\mathcal F(a,t,b)$. Its proof uses a unit normalizer at a unique contact, the local trace extraction, the stated formal precision, and the fact that one of $h,h-1$ is a $p$-unit. Hence
$$
             M_j^3\mid\Delta c,\qquad M_j\mid(u-nv)c
$$
whenever the relevant right side is nonzero.

## Modular height constants

The precise H4.1 estimate in v68, section 3, is $h(q)<C_*R^2E(R)\log R$ for the five-contact radical outside $S$. Here $B_S=\prod_{p\in S}p$, $R=B_SM_S(q)$, $E(R)=\prod_{p\mid R}(1+1/p)$ and $C_*=(74712001/10^6)2^{68}3^{16}5^{16}7^4$. This full-family modular input supplies the small-cutoff radical.

Write $J=\prod_{p\in\Gamma_\beta}p$. Then $R\le JM_\beta$, $E(R)\le E(J)(1+\log M_\beta)$, by the harmonic sum bound for the divisor sum of reciprocals of squarefree $M_\beta$. Also $\log R\le\log J(1+\log M_\beta)$ and $(1+\log M)^2\le2M$ for $M\ge1$. The finite check gives $2C_*J^2E(J)\operatorname{bitlength}(J)<2^{342}$. Thus
$$
              h(\beta)<2^{342}M_\beta^3\le2^{342}c/\ell^{2L+1}.
$$

Apply H4.1 at $q_s=2+1/(t_j-s)$ for $s=4j+2,4j+4$. Its unimodular inverse costs at most $\log35$ in height. Outside $\Gamma_j$ the two radicals are disjoint with product $M_j$. A prime $p\in\Gamma_j\setminus S$ can occur in both only if two contacts in opposite translates coincide modulo $p$. Indeed all denominators are $p$-units and no negative-valuation $t_j$ lies at a finite contact. Set $e_p=1+\mathbf1_{\text{cross-block collision}}$ and
$$
 K_j=B_S^2\prod_{p\in\Gamma_j\setminus S}p^{e_p},\qquad
 E_j=E(B_S)^2\prod_{p\in\Gamma_j\setminus S}(1+1/p)^{e_p}.
$$
The two H4.1 products obey $R_1R_2\le K_jM_j$ and $E(R_1)E(R_2)\le E_j E(M_j)$. Taking the geometric mean and using the arithmetic mean on their logarithms yields
$$
 h(t_j)\le\log35+C_*K_jM_j\sqrt{E_jE(M_j)}
                (\tfrac12\log K_j+\tfrac12\log M_j).
$$
The exact checks give $K_j<2^{398}$ and $C_*K_jE_j<2^{550}$. Using $\sqrt{1+\log M}\le1+\frac12\log M$ gives, uniformly,
$$
             h(t_j)\le K M_j(199+\tfrac12\log M_j)^2,\qquad K=2^{551}.
$$

## Quantitative contradiction

The effective v19 height bounds are
$$
 B^2\le h(t_0)+\tfrac12h(t_1)+\tfrac12h(t_2)+2h(\rho)+84,\qquad
 h(\rho)\le15h(\beta)+2L\log\ell+128 .
$$
For $N=\Delta,k=3$ or $N=u-nv,k=1$, with $N\ne0$, this gives
$$
 B^2\le2K|Nc|^{1/k}(199+\tfrac1{2k}\log|Nc|)^2+
                         30h(\beta)+4L\log\ell+340.
$$
For odd $L\ge53$, $\ell^{2L+1}\ge120\cdot2^{342}$ and $c-1\ge2^{1735}$. Hence $h(\beta)<c/120$ and $4L\log\ell\le2\log c$. The last three summands are at most $c/4+2\log c+340<(c-1)^2/2\le B^2/2$.

For $\Delta\ne0$ the original degree-four Lucas estimate gives $|\Delta c|\le10B^5$. Rearrangement gives $B^{1/3}<9K(200+\frac56\log B)^2$. The quotient of the two variable factors is increasing for $B\ge1$. At $B=2^T$, $T=1735$, the inequality already fails, since $\log2<7/10$ and $2^{T-3\cdot551}12^6>9^3(2400+7T)^6$. Thus $\Delta=0$, and the elementary v19 Lucas descent yields $\log B>c-4$.

If $u-nv\ne0$, use $|u-nv|\le2e^{h(\beta)}B$. With $s=\log B,t=h(\beta)+\log c$, the $k=1$ bound after absorption gives $s\le\log(8K)+t+2\log(200+(s+t)/2)$. Using $\log(1+x)\le x$ and rearranging,
$$
 s\le(201/199)t+(200/199)\log(8K\,200^2)
      <2t+574\le(31/60)c+574<c-4 .
$$
This contradiction gives $\beta=n$. For reduced $X=u_0/v_0$, integrality of $216X^4+450459$ forces $v_0^4\mid216$, hence $v_0=1$.

## Polynomial and replay

The v28 unit-norm formulation and termwise positive detector variant use the same odd-valuation inequalities and required precision. The latter has an explicit finite specification at $L=53$ in the explicit53/explicit27 directory. It has degree at most 1,941,079,851,008, rank 2,097,152, support below $2^{994}$, and coefficient absolute values at most $2^{59077885427712}<2^{2^{46}}$. The stored L53 graph preserves the upstream family-parameter metadata about its previously certified threshold of 20483. The stronger sufficient bound is the arithmetic statement proved above. The corresponding fixed $L=20483$ termwise member has the same degree bound and coefficient absolute values below $2^{2^{54}}$.

Run check_L53.py for all finite arithmetic comparisons and check_polynomial.py for the independent finite-algebra, guard and majorant replay. Regenerate the candidate with

    python -B h193/fewvars/positive.py --termwise --route explicit27 --parameter 53 --output h193/counts/effective/explicit53

The pinned arithmetic sources are papers/few_variables27/explicit27_20261110_v19.tex, papers/quartic/quartic229_compact_20261117_v68.tex section 3, and papers/finite_algebra/unit_norm_20261114_v28.tex. The termwise determinant argument is in h193/fewvars/POSITIVE.md.
