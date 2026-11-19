# Arithmetic transfer for the shared product

The two-argument source is Brox v74 with v73's arithmetic proof. The three-argument source is v68 with v62's arithmetic proof. All assertions below are relative to the corresponding source premises. Keep the contact functions, excepted primes, scalar extraction, point equations, and label and height arguments of the relevant source. Write $q_j=R_j^{-1}-1$ wherever this is defined, $c=\sum_jq_j$ and $s_j=c-q_j$. Compute the source's first five-factor product only once at weight $c$, calling it $W$. The source factor assignments need not agree across detectors, since its first assignment contains all sixteen tests at the required precision.

## The scalar gate

In the quadratic field $K=\mathbb Q(\sqrt2)$ introduce one rational $D$ by
$$
D\operatorname{Tr}(W)=\operatorname{Nm}(W-1).
$$
This relation forces $\operatorname{Tr}(W)\ne0$ over $\mathbb Q$, since a zero trace forces $W=1$ by the norm equation, a contradiction. Put $g_j=1+s_j^2+q_jD^2$. Use $\tau_j=g_j/2$ as the pole input's trace normalization, so the actual argument is $\gamma^2R_jg_j^2/4$ at every consumed prime, with $\gamma=408/409$.

At a consumed good prime for argument $j$, $v_p(q_j)=-\mu$ and $v_p(R_j)=\mu$, with $\mu>0$ odd. Both source exceptional sets contain $2,3,17$, so $v_p(\gamma)\le0$. In the explicit source $p=409$ can be consumed and its effect strengthens the inequality. If $g_j\ne0$, its pole input has odd valuation, and the pole obstruction gives $v_p(g_j)>-\mu/2$. The same inequality holds if $g_j=0$, using $v(0)=+\infty$.

A negative valuation of $1+s_j^2$ is even, whereas every finite valuation of $q_jD^2$ is odd. Thus a negative minimum cannot cancel, and
$$
v_p(D)>\mu/4,\qquad v_p(s_j)>-\mu/4,\qquad v_p(c)=-\mu.
$$
At each of the two unramified slots, possibly coincident, the five factors of $W$ have nonpositive valuation. If both valuations $w_1,w_2$ of $W$ were strictly negative, the numerator norm in the definition of $D$ would have valuation $w_1+w_2$, while the denominator trace would have valuation at least $\min(w_1,w_2)$. It would follow that $v_p(D)\le\max(w_1,w_2)<0$. Hence at one slot $v(W)=0$. Every factor at this slot is a unit, with every nonconstant term strictly positive by the unique-minimum computation below. This is stronger than the required source test $v(W)>-\mu/2$. This argument does not assume disjointness of the radicals on arbitrary rational points.

## The field gate

A second valid realization sets
$$
A_j=\frac{1+s_j^2}{1+q_j},\qquad G_j=\tfrac12(W^2+A_j)
$$
and uses the original cleared norm-over-trace equation with $G_j$ in place of the product. The cleared gate equation automatically excludes $q_j=-1$, since $1+s_j^2>0$ rationally. All prepared real weights are positive, so this exclusion preserves integer completeness. At a consumed prime the rational denominator is automatically nonzero.

If $G_j=0$ both slots have $v(G_j)>-\mu/2$. Otherwise the cleared norm-over-trace equation forces the rational component to be nonzero and $\tau_j=1/\operatorname{Tr}(G_j^{-1})\ne0$. If $v(G_j)\le-\mu/2$ in both slots, the trace of the inverse has valuation at least $\lceil\mu/2\rceil$. Then $\gamma^2R_j/\operatorname{Tr}(G_j^{-1})^2$ has negative odd valuation, contrary to the same obstruction. In a successful slot a negative valuation of $A_j$ is necessarily $\mu+2v_p(s_j)$, which is odd. A finite valuation of $W^2$ is even, excluding cancellation of a negative minimum. Since $p$ is odd, the gate bound gives
$$
v(W)>-\mu/4,\qquad v_p(s_j)>-3\mu/4,\qquad v_p(c)=-\mu.
$$
This again implies the upstream local hypothesis.

## The individual factor tests

For the v74 two-argument system, the ten nonzero reciprocal abscissas have even valuation; the other six tests are the four cleared comparison errors, the homogeneous Lucas error, and the input numerator. In an ordinary factor the three terms besides the constant have distinct classes $-\mu,-2\mu,-3\mu$ modulo four. The special factor has a fourth nonconstant term of valuation $4\bmod8$; the ordinary terms still have nonzero class modulo four. Therefore each factor has nonpositive valuation, inverse residue zero or one, and no cancellation at its minimum. At a slot with $v(W)>-\mu/2$, every term of every factor has valuation greater than $-\mu/2$. For an ordinary term $c^eT^m$ this yields $v(T)>(e-1/2)\mu/m$. Thus the reciprocals have depth at least two, all four cleared comparisons and homogeneous Lucas error have depth at least one, and the special input term gives $v(\mathcal N)>7\mu/16$. The physical comparison denominators regain two orders, the homogeneous Lucas denominator two, and the input denominator one. The two-argument source's formal integrality transfer and its global height proof apply.

The explicit five factors in v62 are
$$
\begin{aligned}
&1+c^5 C_2^2+c^2D_H^2+c^4 B_1^4,\\
&1+c^5 G^2+c^2 A_3^2+c^4 B_0^4,\\
&1+c^5 I^4+c^3 A_2^2+c^2 A_4^2+c^4 B_3^4,\\
&1+c^5 C_3^2+c^2 C_1^4+c^4 B_4^4,\\
&1+c^5 C_4^2+c^2 A_1^2+c^4 B_2^4.
\end{aligned}
$$
The generic factors have nonconstant terms of odd valuation, valuation $2\bmod4$, and valuation $4\bmod8$. The third factor splits the odd class into the disjoint classes $-\mu,\mu\bmod4$, since reciprocal abscissa valuations are even. These suffice for unique minima in both slots and show each factor has valuation at most zero. At the successful slot every term has valuation $>-\mu/2$. In particular $v(C_2,C_3,C_4,G)>9\mu/4$ and hence at least three. The first comparison and input satisfy $v(C_1)>3\mu/8$ and $v(I)>9\mu/8$, respectively. Each tested reciprocal has positive even valuation, at least two. These are exactly the comparisons consumed by v62. Vanishing test terms can be omitted from minima. Its full formal-logarithm transfer, height constants and their arithmetic use are unchanged by the comparison substitution.

## Preparing integer witnesses

For v74 the two additive contact shifts are separated on the prepared integer witnesses because $T>7$. Indeed, $Q_1=[\beta]P_0$ and $Q_2=[a]R_0$ are nonzero nontorsion doubles. At each real embedding of $y^2=x^3-d^2x$ their abscissas exceed $d$, whereas both remaining abscissas are at least $-d$. The contact set is contained in $[-1,3]$. For v62 the shifts are at least seven and nine, above the center-$3/11$ diameter $25/11$. Thus the twenty or thirty selected forms have distinct shifts once the source integer witnesses are fixed. At a selected prime for detector $j$, its weight has valuation $-1$. Each other weight is integral: reduce the other argument to its fixed contact shift and avoid prime divisors of the corresponding finitely many nonzero contact-function denominators. This cutoff is imposed before prime selection and may depend on the fixed integer input and its prepared elliptic roots.

Consequently $v_p(c)=-1$. The respective source preparedness estimates depend on that valuation only. In v74 these include synchronizing the two reference formal depths as proved in v73; in v62 its original absolute order-four estimates make each nonconstant term positive. At the prepared slot for $j$, the shared $W$ has residue one. In the other slot it either has residue one or has negative valuation.

For the scalar gate, if both slots have $W\equiv1$, then its trace is $2\bmod p$ and its shifted norm is divisible by $p$. If the other slot has negative valuation $-k$, the trace has valuation $-k$, while the shifted norm has valuation at least $1-k$ (or it is zero). Either way $v_p(D)>0$. At this selected contact, $s_j$ has the residue of a fixed rational number $z$, the sum of the evaluations of the other contact weights at their translated contact positions. In advance, also avoid prime divisors of the numerators and denominators of $1+z^2$, which is a nonzero rational number. It follows that $g_j\equiv1+z^2\ne0$, and the pole input has valuation one. For the field gate, $v_p(A_j)\ge1$. At a slot where $W\equiv1$ the inverse of $G_j$ has residue two; at an opposite slot where $W$ has a pole it has residue zero. The actual reciprocal trace has residue two or four, nonzero for these large selected primes. This also gives pole valuation one.

At the real and prepared finite places, all $q_j\to0$, so $c\to0$ and $W\to1$ as the original regular point functions remain bounded. Thus the scalar gate has $D\to0$, $g_j\to1$, and the field gate has $A_j\to1$, $G_j\to1$. In the prepared real embeddings the weights are positive, the shared product of even-powered factors is positive, and both gates used as pole normalizations are positive. Every actual argument tends to $(204/409)^2$ in the real open interval $(0,17)$ and has the prepared square classes with depths $4,2,2$ at $2,3,17$. In each source $R_j$ has even valuation outside its own selected primes by the retained product of primary forms over a square denominator. The rational normalization changes valuations by even integers. The actual pole arguments have square reduced denominators; their independent real and finite preparations therefore invoke the same source pole-realization theorem. The added cutoffs do not change a source parameter threshold.

## Signed tests and changes of field coordinates

The constant term of every field factor is one. In the 168-variable layout (and its three-contact counterpart), two pairs of ordinary terms use signs $+,-$ at exponents one and three. In the promoted layout the same sign choice applies to three such pairs. Replacing a coefficient $1$ by $-1$ preserves every nonarchimedean term valuation used above. All nonconstant terms retain positive valuation in the prepared successful slot. At the prepared real embeddings the original weights tend to zero and the point functions are bounded, so every signed factor still tends to one. Shrinking the same neighborhoods makes all factors positive and supplies the original real bound for the actual pole input.

For an ordinary pair of native field tests $A,B$, the replacement uses the two field coordinates $U=A+cB$ and $V=A-cB$. In the factor equation this gives
$$cUV=cA^2-c^3B^2.$$
The inverse map $A=(U+V)/2$ and $B=(U-V)/(2c)$ is defined on every rational zero of the unit-guarded system. Apply this inverse in every retained equation that used the original physical test coordinates, with the physical factors of $C$ and $c$ and the imaginary basis coefficients fixed by v74. For example, if $A=E_i^2$ is physically $C(x+2\sqrt2 y)/c$ and $B=\mathcal H^2$ is $(z+4\sqrt2 t)/c$, the substitutions apply to $A,B$ as displayed, including their unequal imaginary normalizers. The negative factor coefficient multiplies the square of the entire native field test, including the prescribed conjugation of opposite reciprocals.

For the promoted five-factor 166-variable layout, move the input test from $c^4\mathcal N^8$ to $c^3\mathcal N^4$ with a negative coefficient in its hyperbolic pair. The fourth-power helper for the input can be deleted, as its square helper already stores $\mathcal N^2$. Promote the obligatory second primary reciprocal square into $c^4 A_2^4$ in the special factor. Its finite valuation belongs to $4\bmod8$ because $v(A_2)$ is even. Thus the original modulo-eight separation of the five terms in that factor still holds. Its extracted desired condition is merely $v(A_2)>0$, which follows from $v(W)>-\mu/2$. All other reciprocal tests are the usual even squares; all cleared comparison, input and Lucas tests are fourth powers in ordinary slots with $e=1,2,3$. Each successful lower bound $v(\mathcal N)>(e-1/2)\mu/4$ is positive, sufficient for the original input and height proof. At selected primes $v(A_2)\ge2$ and $v(\mathcal N)\ge3$, so both replacement terms have strictly positive valuation. All preparation choices and the real continuity argument above still apply.

## Scalar gate used by the 166-variable coefficient table

The final table uses $g_j=1+D^2+s_j^2/q_j$ rather than the first scalar polynomial above. Its denominator $q_j$ is already guarded. The same pole valuation gives $v_p(g_j)>-\mu/2$, including its zero boundary. A negative valuation of $1+D^2$ is even, and a finite valuation of $s_j^2/q_j$ is odd. Therefore $v_p(D)>-\mu/4$ and $v_p(s_j)>-3\mu/4$. In particular $v_p(c)=-\mu$. At both slots the five factor valuations are nonpositive. If both $v_i(W)<0$, the norm/trace argument gives $v_p(D)\le\max_i v_i(W)$. If one is zero that slot already meets the bound. In either case some slot has $v_i(W)>-\mu/4$, stronger than the source cutoff. The signed pairs and the promoted special reciprocal were proved to meet precisely this cutoff above.

On the selected prepared data $D$ has positive valuation and $s_j$ is integral. Hence $g_j\equiv1$ without the finite exclusions of divisors of $1+z^2$ used for the first scalar gate. For the fixed finite places and the two real places, use the paired reflection form of the contact function. With midpoint $a$ and nonzero fixed rational $\kappa=\sum_{\theta}(\theta-a)^2>0$, its expansion at infinity is
$$
 q(t)=\kappa (t-a)^{-2}\bigl(1+O((t-a)^{-2})\bigr).
$$
For fixed additive shifts $b_i$, the ratios $q(\lambda+b_i)/q(\lambda+b_j)$ tend to 1 as $\lambda$ tends to infinity in the prepared real or $p$-adic topology. Thus $s_j^2/q_j=q_j(\sum_{i\ne j}q_i/q_j)^2\to0$ even at $p=2$. This preserves all the actual-input conclusions of the preceding completeness proof for either number of arguments.

## Four-factor coefficient table

The 165-variable refinement retains four factors. Their ordered lists of tests at powers $c,c^2,c^3,c^4$ are
$$
\begin{array}{c|llll}
0 &+\mathcal N^4 &B_1^2&-E_1^4&D_H^4\\
1 &+E_4^4&A_3^2&-\mathcal H^4&B_2^4\\
2 &+E_3^4&B_4^2&-E_2^4&A_2^4\\
3 &+A_1^2&B_3^2&-A_4^2&B_0^4 .
\end{array}
$$
The constant term of each is one. The valuations of the first three terms belong to the nonzero, pairwise distinct classes $-\mu,-2\mu,-3\mu\bmod4$. The fourth uses an even-valuation reciprocal fourth power and hence has valuation $4\bmod8$; the constant has valuation zero. Every factor is thus nonzero, has nonpositive valuation, and has residue one whenever its valuation is zero. In a successful slot $v(W)>-\mu/4$, hence each term has valuation greater than $-\mu/2$, which suffices to obtain the source local depths for all sixteen tests. The four promoted reciprocal fourth powers each give $v(T)>7\mu/8$, requiring positive even valuation. At the selected prime $\mu=1$, each reciprocal has depth at least two and each error has enough depth for every displayed term to be strictly positive. The source proof and the scalar-gate proof above apply without any new denominator on the test expressions.

For the last factor retain raw $A_1,A_4$ and one field helper $U=A_1+cA_4$. Then $cUA_1-c^2UA_4=cA_1^2-c^3A_4^2$. The other three signed odd pairs use the invertible hyperbolic change of coordinates above. Defining one rational $u_2=c^{-2}$ by $u_2=(c^{-1})^2$ gives the extra negative Laurent exponents needed in the final ordinary quadratic residuals.
