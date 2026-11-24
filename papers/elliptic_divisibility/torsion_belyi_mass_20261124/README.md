# Torsion-supported Belyi maps and simple primitive denominator mass

## Result

This note strengthens the denominator input of the project's [v82 divisibility detector](../prepared_eds_divisibility_20261120_v82.tex) and the later one-pole constructions. The unconditional asymptotic for the **full** primitive part is already known: M. Streng, *Divisibility sequences for elliptic curves with complex multiplication*, Algebra & Number Theory **2** (2008), 183–208, Proposition 1.3, [publisher's PDF](https://msp.org/ant/2008/2-2/ant-v2-n2-p04-p.pdf#page=5), p. 185. Streng explicitly notes that its integer-indexed version does not require CM. His result gives an error \(O(n^\epsilon)\) for every \(\epsilon>0\). The deduction below concerns the **exponent-one** part via a torsion-supported Belyi map and a fixed weak abc exponent. We also give a self-contained weaker-error Möbius argument for the full primitive part to specify the normalizations.

Let \(K\) be a number field of degree \(k\), \(E/K\) an integral Weierstrass elliptic curve, and \(P\in E(K)\) nontorsion. Suppose there is a nonconstant map \(g:E\to\mathbb P^1\) defined over \(K\), of degree \(d\), such that its geometric inverse image of \(\{0,1,\infty\}\) consists of precisely \(d\) torsion points, including the identity. In particular a Belyi map with torsion-supported three fibers has this property by Riemann–Hurwitz.

Assume weak abc over \(K\) with exponent \(\kappa>1\):
\[
 h(t)\le\kappa N^{(1)}(t;0,1,\infty)+C_\kappa
 \qquad(t\in K\setminus\{0,1\}).
\]
All logarithmic ideal norms and truncated finite-prime counts are normalized by \([K:\mathbb Q]\); the discriminant and finite additive terms for fixed \(K\) are included in \(C_\kappa\).

Write \(q=\widehat h(P)>0\), in the convention \(h(x([n]P))=2qn^2+O(1)\). Let \(\mathfrak B_n\) denote the square root of the denominator ideal of \(x([n]P)\). Its local exponent is the formal depth, zero for a nonformal point. Exclude any fixed finite set of rational primes including the ramified primes of \(K\), 2, the bad reduction primes and the bad primes of the map. Let \(J_n\) be the normalized log norm of the product of prime ideals dividing \(\mathfrak B_n\) primitively and with exponent precisely one, outside these exclusions. Then
\[
 \tag{1}
 J_n\ \ge\ qn^2\left(\prod_{p\mid n}(1-p^{-2})-
                         2d(1-1/\kappa)\right)-o(n^2).
\]
Under ordinary abc over \(K\) there is the sharper asymptotic
\[
 \tag{2}
 J_n=qn^2\prod_{p\mid n}(1-p^{-2})+o(n^2).
\]
Thus a sufficient fixed weak abc exponent for a positive quadratic simple-primitive mass is
\[
 \tag{3} \kappa<\frac{2d}{2d-1/\zeta(2)}.
\]
In addition, if one only keeps rational primes at which all the local denominator exponents are zero or one and some exponent is one, their logarithmic product has the lower bound
\[
 \tag{4}
 qn^2(1-(k+1)d(1-1/\kappa))-o(n^2).
\]
There is no primitivity condition in (4). In particular this recovers the simple-denominator hypothesis of the [Lucas-free amplifier](../simple_denominator_amplifier_20261124/README.md) for \(k=2,d=4,\kappa<12/11\).

## 1. Truncated mass and multiplicity surplus

Use the notation \(\mathcal N(\mathfrak a)=\log N_{K/\mathbb Q}(\mathfrak a)/k\). For fixed nontorsion \(P\), the archimedean Siegel approximation estimate gives
\[
 \mathcal N(\mathfrak B_n)=qn^2+o(n^2).
\]
This is the same fixed-point denominator asymptotic used in v82. Each fixed finite place contributes \(O(1+\log n)\): in its formal entry subgroup use the local logarithm after entry into a sufficiently deep formal disk. At all good unramified odd primes the logarithm is already isometric on the first formal group. Discarding finitely many places therefore does not change the asymptotic.

The pole divisor \(g^*(\infty)\) has degree \(d\) and torsion support. Its class differs from \(d[O]\) by a torsion class, since its degree-zero class in \(\operatorname{Pic}^0(E)\) is the corresponding sum of torsion points. After a fixed multiplication of divisors these are linearly equivalent. By functoriality and the bounded error for linearly equivalent Weil heights,
\[
 h(g([n]P))=dqn^2+O(1).
\]
No symmetry assumption on the individual pole multiplicities is needed.

Over a fixed finite extension \(K'/K\) containing the torsion points of the three fibers, discard the finitely many bad reduction primes of the curve, the map, and its contact divisors. At each remaining prime of \(K'\), a contact of \(g([n]P)\) with \(0,1,\infty\) is equivalent to reduction of \([n]P\) to one of those \(d\) torsion points. The normalized weight of a prime of \(K\) is the sum of the weights of its extensions in \(K'\), outside the fixed ramification exceptions. Thus the contribution of the identity to the truncated count is \(\mathcal N(\operatorname{rad}\mathfrak B_n)\), up to a fixed additive constant. For each nonidentity torsion point \(T\) the corresponding truncated contribution is at most the normalized denominator height of \([n]P-T\), which is at most \(h(x([n]P-T))/2=qn^2+O(1)\); the equality of canonical heights follows from torsion invariance. There is no application of abc over \(K'\). All bounds use the absolute heights and normalized counting functions.

Applying weak abc to \(g([n]P)\in K\) (the finitely many inadmissible indices may be discarded) gives
\[
 \mathcal N(\operatorname{rad}\mathfrak B_n)
 \ge (d/\kappa-d+1)qn^2-O(1).
\]
Consequently the total multiplicity surplus
\[
 S_n=\mathcal N(\mathfrak B_n)-\mathcal N(\operatorname{rad}\mathfrak B_n)
 =\sum_{\mathfrak p\mid\mathfrak B_n}
       (v_{\mathfrak p}(\mathfrak B_n)-1)\mathcal N(\mathfrak p)
\]
satisfies \(S_n\le d(1-1/\kappa)qn^2+o(n^2)\). The full multiplicity weight of primes with exponent at least two is at most \(2S_n\). For ordinary abc, apply this bound with every fixed \(\kappa>1\), take a limsup as \(n\to\infty\), and then let \(\kappa\downarrow1\). This gives \(S_n=o(n^2)\); the order of these limits is important.

## 2. Primitive mass and the Möbius identity

At a good odd unramified place let \(r\) be the order of the reduction of \(P\). The local denominator exponent is zero unless \(r\mid n\), and in the latter case equals \(a_r+v_p(n/r)\) with \(a_r>0\), by the formal logarithm. For \(r\mid n\), the coefficient at that prime in the Möbius sum
\[
 \sum_{j\mid n}\mu(n/j)\mathcal N(\mathfrak B_j)
\]
is \(a_n\) when \(r=n\). If \(r<n\), the constant \(a_r\) cancels, and the remaining sum of \(\mu\)-weighted \(v_p(j/r)\) equals 1 when \(n/r\) is a positive power of \(p\), and 0 otherwise. Indeed \(v_p\) is the divisor sum of the indicator of positive powers of \(p\). The total weight of these nonprimitive leftovers is at most \(\log n\): they occur only above primes dividing \(n\) and each rational prime contributes at most its logarithm. At the finitely many excluded places the corresponding signed sum is \(O(\tau(n)(1+\log n))=o(n^2)\), using the fixed-place bound and \(\tau(n)\le2\sqrt n\).

The error in replacing each \(\mathcal N(\mathfrak B_j)\) by \(qj^2\) is \(o(n^2)\) after summing over divisors: for every \(\epsilon>0\), all sufficiently large \(j\) have error at most \(\epsilon j^2\), while \(\sum_{j\mid n}j^2\le\zeta(2)n^2\), and the fixed smaller \(j\) contribute a bounded constant. The Möbius sum of the leading terms is
\[
 qn^2\sum_{b\mid n}\mu(b)/b^2=qn^2\prod_{p\mid n}(1-p^{-2}).
\]
This proves the weaker-error version of Streng's known full primitive-part asymptotic and its compatibility with the finite exclusions.

Remove all primitive prime ideals of exponent at least two. Their full multiplicity weight is at most \(2S_n\), as above. This proves (1); the upper bound by the full primitive part, together with \(S_n=o(n^2)\), proves (2). Since \(\prod_{p\mid n}(1-p^{-2})\ge1/\zeta(2)\), the fixed-exponent sufficient condition is (3).

For (4), discard an entire rational prime if some local exponent is at least two. At an unramified rational prime \(p\), write the normalized weights of its places as \(f_i\log p/k\), with positive integers \(f_i\) summing to \(k\). The multiplicity of the high-exponent places is at most twice their surplus. If some place is high, the weight of all the exponent-one places is at most \((k-1)\log p/k\), at most \(k-1\) times the surplus because a high place has weight at least \(\log p/k\). Thus the discarded multiplicity is at most \((k+1)\) times the surplus. At the remaining rational primes the full normalized multiplicity is at most \(\log p\). Combining these observations proves (4).

## 3. Explicit curves and stronger v82 constants

For \(E:y^2=x^3-Dx\), the degree-four Belyi map is \(x^2/D\), with the four two-torsion points in its three fibers. This works over both the original quadratic carrier and the rational curve \(y^2=x^3-2x\); on the latter the nonrational torsion points are treated by the extension argument in Section 1, without assuming abc over that extension. Under ordinary rational abc, the exponent-one primitive primes on the v82 rational curve therefore have eventual mass greater than \(3qn^2/5\), improving the \(qn^2/5\) used there. Indeed \(1/\zeta(2)=6/\pi^2>147/242>3/5\). Under the fixed rational weak abc exponent \(\kappa=27/25\) they have eventual mass at least \(qn^2/100\), because
\[
 \frac{147}{242}-8(1-25/27)
       =\frac{97}{6534}>\frac1{100}.
\]
Thus the five-coordinate divisibility detector and the \(k+4\) joint detector have the same sufficiency conclusions under this fixed weak exponent, without changing their point charts or their pole preparations. For the joint detector with shifted references, increase the finite exclusion of the reference index so each shifted nonzero index lies beyond the new threshold.

There is also a degree-three carrier: \(E:y^2=x^3+a^2\) for \(a\in K^\times\), with map \((y+a)/(2a)\). Its three contact points are the identity and \((0,\pm a)\), the latter of order three by the tangent intersection. With \(K=\mathbb Q\), (3) is satisfied by \(\kappa=10/9\), giving eventual mass at least \(qn^2/200\) because
\[
 \frac{147}{242}-6(1-9/10)=\frac9{1210}>\frac1{200}.
\]
For example \(a=3\) admits \(P=(3,6)\); \(x(2P)=-15/16\) by the doubling formula, so \(2P\) has formal depth two at 2, in the injective logarithm disk, and \(P\) is nontorsion. These mass estimates do not require rank one. To use that curve as a cyclic-index Diophantine carrier one must additionally supply its rank-one group certificate; no such certificate is assumed in this example. The curve and map illustrate the improvement from degree three rather than four.

## 4. Consequences for the six-coordinate quotient

The ordinary-abc [height-anchored quotient](../height_anchored_quotient_20261124/README.md) can now use eventual primitive mass \(3qn^2/5\) instead of \(qn^2/5\). After excluding the support of its input contact polynomial the remaining mass is at least \(qn^2/2\), since \(3/5-10/299>1/2\). The identical proof thus forces \(h\mid j\) and, when \(X\ne m=j/h\),
\[
 \log(1+|m|)\ \ge\
   \left(\frac{N+2}{2}-\frac1{1196}\right)qh^2-O(1).
\]
Its counterexamples remain, so this is a stronger dichotomy, not a definition of the integers.

The same six-coordinate construction, with explicitly changed scalar contacts, works under the fixed rational weak abc exponent \(27/25\). Use the six integral contacts
\[
 \Theta=\{1,31,37,41,46,61\},\qquad
 t=X^2+100,\qquad u=\prod_{\theta\in\Theta}(t-\theta)>1 .
\]
The Belyi identity
\[
 z=2+60/(t-61),\qquad
 \phi=z(z+2)^3/(2z+1)^3,\qquad
 \phi-1=(z-1)^3(z+1)/(2z+1)^3
\]
is the six-contact transform used in the project's v78 weak-abc contact estimates. Its three fibers are the images of exactly the displayed six contacts. To recall the quantitative calculation: \(h(\phi)=4h(t)+O(1)\). The truncated count of its three fibers is at most the count of the six contacts outside a fixed set, plus \(O(1)\). For each positive contact multiplicity \(a\), \(2\le a+(a\bmod2)\); and the total contact multiplicity count is at most \(6h(t)+O(1)\), by multiplying the six homogeneous linear forms in the reduced numerator and denominator of \(t\). Hence the positive odd contact product \(M\) satisfies
\[
 \log M\ge(8/\kappa-6)h(t)-O(1)
           =(38/27)h(t)-O(1).
\]
Take the same rational curve and two point charts as in the height-anchored quotient, but replace \(u^{-401}\) in its joint scalar by \(u^{-40001}\). At a positive odd input contact the identical valuation proof forces reference depth at least \(10000\): if it were smaller, \(-80002+8\cdot9999<0\) gives the rejected residue. Its heights now satisfy
\[
 h(t)\le\frac{27}{380000}qh^2+O(1),\quad
 h(X)\le\frac{27}{760000}qh^2+O(1),\quad
 2h(u)\le\frac{324}{380000}qh^2+O(1).
\]
Using the weak-abc primitive mass \(qh^2/100\) of Section 3, remove the input support and fixed exceptional primes. The remaining primitive mass is at least \(qh^2/120\) eventually because \(1/100-324/380000>1/120\). The reference cutoff can be increased once and encoded by the same finite guard. All logarithm, quotient and pole calculations are otherwise unchanged. Thus \(h\mid j\) and either \(X=m\) or
\[
 \log(1+|m|)\ge
 \left(\frac{N+2}{120}-\frac{27}{760000}\right)qh^2-O(1).
\]
Integer completeness and the noninteger false-positive construction use the same ordered reference selection, with the input support and all fixed exceptions included before the reference is chosen. They do not require ordinary abc. This proves a fixed-weak-abc six-coordinate quotient relation, not a defining polynomial for the integers. There is still no quotient-size cap.

## Status and references

The full primitive-part asymptotic is credited to Streng. The new project deductions are the torsion-Belyi weak-abc bounds on surplus, simple-prime mass, simultaneous rational-prime depth, and their quantitative applications to the existing divisibility and new amplifier constructions. The degree-three example is a candidate carrier for that analysis, not a claimed group-rank reduction. No effective abc constant, numerical reference threshold, unconditional simple-primitive theorem, new ordinary-abc defining-variable record or quartic record is asserted.