# Transfer to the two weak-abc eleven-variable families

The reciprocal product and direct terminal clearing of
[final.md](final.md) also apply under either of the fixed weak-abc
exponents used by the current v88 constructions. This does not
use the ordinary-abc binary-form estimate of the new contact map.
Instead retain the old weak-abc contact map and its exact height
and prime-preparation proof.

Under the respective retained hypotheses, the degree bounds become
\[
\begin{array}{c|r|r}
 \kappa&\text{v88 degree bound}&\text{new degree bound}\\\hline
121/100&16460929&3810177\\
16/15&9808001&2282369
\end{array}
\]
The variable count is eleven in each case; sufficient fixed odd B
remains ineffective. No new arithmetic premise is introduced.

## Arithmetic transfer

Use the same three point blocks and six raw tests of the
[weak11 source v78](../weak11_audit_and_transfer_20261119_v78.tex),
section "Full auxiliary points and one detector". These are the
same rational quantities as original_tests in the ordinary v88
point source, whose polynomial DAG and pre-contact guards are
pinned in degree.json. Explicitly they are the four reciprocal
abscissas and the cross and target differences of the two
logarithmic ratios. The weak and ordinary sources use the
same square-abscissa root and full auxiliary charts.

Keep the weak-abc scalar of v78 and v88:
\[
 \begin{gathered}
 \beta=X^2+B,\quad a=\beta^e+T^e,\quad
 x=a-z,\quad y=a+z,\\
 P=G(x),\quad Q=G(y),\quad J_0=(x-1)(y-1),\quad F=P^2+Q^3,\\
 U=J_0^{8(k-1)}PQF^2,\qquad
 D=(P^3+Q^5)(P+Q^k)(P^k+Q),\quad u=U/D.
 \end{gathered}
\]
Here \(G(t)=\prod_{\theta\in\Theta}(t-\theta)\),
\(\Theta=\{0,-1/21,-1/17,-1/25,-1/16,-1/26,-1,-1/41\}\).
The row parameters \((e,k)\) are (6,6) and (4,5).
Clear only the fixed rational coefficient denominators in the pair
\((D,U)\) by a common nonzero integer multiplier, and use the
resulting integral polynomials \(P_c,Q_c\) with \(c=1/u=P_c/Q_c\).
Guard \(P_cQ_c\ne0\). This also guards all contact and scalar
factors retained in the original source.

Use the even-valuation product
\[
 W=\prod_{i=1}^6(1+cC_i^{m_i}),\quad
 (m_1,\ldots,m_6)=(1,1,1,1,2,2),
 \qquad t=1+c\Tr W/(\Nm W+1).
\]
Use exactly the integral terminal radicand of final.md.
At positive odd \(v_p(u)\), the same gate proof excludes its zero
boundaries and gives all six raw tests positive at one slot, hence
\(X\equiv n\bmod p\) and p-integrality of X.
The old weak-abc height inequalities yield
\[
 \log r^+_{\rm odd,S}(u)\ge\lambda h(1:\beta:T)-O(1),
 \qquad \lambda=8374/14641,\ 99/160,
\]
respectively. Both are strictly greater than 1/2; no change to
this estimate is made. Thus there is a consumed prime on every
sufficiently large-B guarded tuple, independently of the terminal
equation. The old soundness contradiction follows.

For canonical witnesses retain the entire ordered scalar and
point preparation of v78, in particular its proof that outside
the temporary finite preparation set positive odd valuations
of u occur only at selected simple primes. This uses the exact
contact factorization, the nonzero resultants of F with the
denominator factors, and the specialized values at J0=0.
At the selected primes the successful raw tests are positive
and the residue-one property of W at integral slots gives
\(v_p(t)=-1,\ v_p(e_{\rm pole})=1\).
At every negative odd \(v_p(u)\), the reciprocal gate gives
t a unit and \(v_p(e_{\rm pole})=-v_p(u)>0\), independently
of foreign raw-test poles. Even valuations retain their
parity. At each fixed place the old asymptotic \(u/z^8\to1\)
makes \(c z^8\to1\), and bounded raw tests give \(W\to1,\ t\to1\).
Consequently \(e_{\rm pole}=7c/t^2\sim7z^{-8}\).
This gives the same positive real interval, square reduced
denominator, class-seven dyadic condition and depth as required
by the BB theorem; include 7 in the temporary finite set.
Thus the new actual pole is prepared on the old integer witnesses.
The BB existence theorem lifts to the new monic equation by
the same explicit scaling as in final.md. No guard on other
geometric terminal characters is imposed. Input zero is again
included by the exterior X factor.

## Finite specification and exact degree bound

Use the point DAG, twelve norm guards, six raw test numerator
and denominator pairs, terminal equation and bounded-prefix
determinant of final.md. Only substitute the weak contact
polynomials \(P_c,Q_c\) above and the new terminal envelope.
The coefficient clearing of the contacts is part of the
finite recipe (for example multiply by the product of their
fixed coefficient denominators). All point weights and
guards remain exactly as in degree.json.

Let \(L_g=16e\). Since a has degree at most 2e,
G(x),G(y) have degree at most Lg, and J0 degree at most 4e.
The numerator of c has degree at most
\(p_c=(2k+5)L_g\), and its denominator degree at most
\(q_c=(2k+6)L_g\).
The original weighted raw-test pairs are the same as in
degree.json; in particular \(\sum_i m_i\deg d_i=82\)
and the numerator weights exceed the denominator weights
by at most one. Since \(q_c-p_c=L_g\ge64\), the two terms
in each factor of the W numerator are bounded by
\(q_c+m_i\deg d_i\). Thus the weights are
\[
 \begin{split}
 w(L),w(N)&\le6q_c+82,\\
 w(J)&\le12q_c+164,\\
 w(K_0)&\le13q_c+164,\\
 w(\mathcal R)&\le
     2(13q_c+164)+2(2q_c+4)=30q_c+336 .
 \end{split}
\]
In the first factor of \(\mathcal R\) the other term has
weight at most \(p_c+q_c+2w(J)\le2w(K_0)\) at these
bounds. The terminal envelope has degree \(15q_c+168\),
using \(M_q=L_0 r_0^{(30q_c+336)/4}\) as before.
The six point envelopes contribute 30.
The total guard degree is at most \(288+p_c+q_c\).
The separator bound is \(15q_c+198\), the rank is 128,
and the degree is at most
\[
           1+128(487+p_c+16q_c).
\]
For the first row \((p_c,q_c)=(1632,1728)\) gives 3810177;
for the second \((960,1024)\) gives 2282369.
These are exact integer ledger calculations and complete
finite determinant specifications. The sufficient B is
still ineffective; no expanded determinants or new
numerical coefficient-height bounds are claimed.
