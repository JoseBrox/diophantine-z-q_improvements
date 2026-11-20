# Two further routes toward fewer variables

These are research lemmas and open construction targets, developing the project based on **notes of Gabe Conant with Astra 6.2**. They establish **no new defining-variable count**. The current counts, including the input, remain 25 and 11 for unrestricted degree, and 163, 179 and 56 for quartics under their respective retained premises.

## 1. Complex multiplication cancels the unknown logarithm depth

Let

\[
E/\mathbb Q:\quad y^2=x^3-2x,\qquad
P=(9/4,-21/8),\qquad K=\mathbb Q(i).
\]

The existing [elliptic divisibility paper](../papers/elliptic_divisibility/prepared_eds_divisibility_20261120_v82.tex) records the rational group and the chart for nonzero multiples of this point:

\[
x=g^2,\qquad y=g\eta,\qquad \eta^2=g^4-2.
\]

Thus each such rational point has one free rational base coordinate, with the quadratic root encoded by the existing finite-algebra method. The automorphism

\[
[i](x,y)=(-x,iy)
\]

is explicit. For integers \(n,k,l\), define

\[
H=P+[i][k]P=[1+ki]P,\qquad
U=[n]P+[i][l]P=[n+li]P.
\]

When the three rational multiples are nonzero, three rational point charts suffice to construct these points and the root point \([n]P\). This is a coordinate observation, not a defining polynomial: a complete detector and its ordered witnesses have not been constructed.

### Local lemma

Let \(p>5\) be a good prime, let \(v\) be a place of \(K\) above \(p\), normalized by \(v(p)=1\), and suppose that the nonzero points \(H,U\) are formal at \(v\). Put \(\xi=-x/y\). For a reduced rational \(X=a/b\), \(b>0\), suppose

\[
v\left(\frac{\xi(U)}{\xi(H)}-X\right)>0.
\]

Then

\[
p\mid N,\qquad N=(bn-a)^2+(bl-ak)^2.
\]

The conclusion includes primes dividing \(b\).

**Proof.** Extend the formal logarithm to the local elliptic group by multiplying into a sufficiently small formal subgroup and then dividing the logarithm by that integer. The extension is additive and commutes with \([i]\). Its value at \(P\) is nonzero: otherwise a nonzero integer multiple of the non-torsion point \(P\) would lie in the kernel of the injective formal logarithm. Consequently

\[
\frac{\log_E U}{\log_E H}=\frac{n+li}{1+ki}.
\]

No estimate for \(v(\log_E P)\) is needed.

For this integral short Weierstrass equation and \(p>5\), the formal logarithm satisfies

\[
\log_E(Q)=\xi(Q)(1+\varepsilon_Q),\qquad
v(\varepsilon_Q)\ge 4v(\xi(Q))>0
\]

on the formal subgroup. One can see the order four from the integral formal group and \([i]\)-equivariance: all exponents are congruent to one modulo four. Division by the exponents in the logarithm does not decrease the bound below four times the input depth when \(p>5\).

Write \(r=\xi(U)/\xi(H)\), and \(L=\log_E U/\log_E H\). The hypothesis implies \(v(br)\ge0\): explicitly, \(br=a+b(r-X)\) is integral. The multiplicative logarithm error is in the maximal ideal, so \(v(b(L-r))>0\). Also \(v(b(r-X))>0\). Hence \(bL-a\) is in the maximal ideal. Multiplication by the integral Gaussian integer \(1+ki\) gives

\[
v\bigl((bn-a)+i(bl-ak)\bigr)>0.
\]

The displayed Gaussian integer is integral at every finite place. Its rational norm is \(N\), so \(p\mid N\). This also works at an inert prime, where the norm valuation is at least two. \(\square\)

### Height consequence

The norm is nonnegative, and

\[
N=0\quad\Longrightarrow\quad X=n\in\mathbb Z,
\qquad l=nk.
\]

If \(N\ne0\), then

\[
\log N\le 2h(X)+2\log\bigl(1+|n|+|k|+|l|\bigr).
\]

Indeed, after bounding \(|a|\) and \(b\) by \(\exp h(X)\), the square root of \(N\) is at most \(\exp h(X)(1+|n|+|k|+|l|)\). A product of distinct consumed primes therefore divides this one integer norm. A sufficiently strong contact-radical lower bound involving the heights of all three rational points would force \(N=0\).

### Exact global gap

For integer input \(X=n\), the natural witnesses have \(l=nk\), so \(U=[n]H\). Their local preparation requires choosing \(k\) after the contact primes to satisfy the reduction-order conditions. Putting the heights of \([k]P\) and \([l]P\) into the contact parameter fixes these points before those primes are selected. The existing prime-pattern theorem does not solve this circular dependence.

Thus the open task is an ordered construction supplying the contact radical, the CM auxiliary points, and the required height domination together. The local lemma removes the logarithm-depth loss in an earlier rank-two proposal. It does not prove the global construction, an eight- or ten-variable definition, or a smaller quartic.

## 2. A different one-parameter sound cover

For the actual rational scalar \(d\ne0\) and reciprocal trace \(V\ne0\), consider

\[
Y^2=V^2+4d(1+dz^2)^2.
\]

Here \(z\) is one free rational parameter and \(Y\) would be encoded as a terminal quadratic root. At an odd consumed prime, let \(\mu=v_p(d)>0\) be odd. Then, including \(z=0\),

\[
v_p(1+dz^2)=\min\{0,\mu+2v_p(z)\}\le0,
\]

where the zero case is interpreted directly. The two terms inside the parentheses cannot cancel because their valuations have opposite parity. If \(2v_p(V)>\mu\), the second term in the radicand has odd valuation at most \(\mu\), strictly smaller than that of \(V^2\). The radicand cannot then be a rational square. Every rational solution therefore gives

\[
2v_p(V)<\mu,
\]

which is the precise scalar inequality used by the current local extraction.

Its quartic has coefficients

\[
a=4d^3,\qquad b=8d^2,\qquad c=V^2+4d.
\]

The associated genus-one Jacobian, when nonsingular, is

\[
y^2=x^3-16d^2x^2-16d^3V^2x.
\]

It is different from the congruent-number Jacobian of the [v82 cover](../papers/pole_parameters/genus_one_sound_criterion_20261120_v82.tex). In particular, the small scalar example in the [v83 checkpoint](../computation/actual_square_v83/new_scalar_counterexample.md) has \(4d/V^2=240/289\). The new equation has the rational point \(z=0,\ Y=23V/17\), although the former genus-one cover has no rational point at that prepared pair.

This distinction does not prove completeness. Rational realization of the new cover is still required at the **actual** source tuples, with the finite-algebra guards accounted for. No global realization theorem or full finite polynomial specification is supplied here. The first task is to prove actual rational points; any subsequent variable count must also verify the existing encoder's guard and character conditions. A count of ten is a target, not a current result.

## Status

The proofs above have been checked by the parent researcher against the independently developed local arguments. They are mathematical proofs, not conclusions inferred from finite tests. The earlier source premises, current coefficient tables and result counts are unchanged. No claim about a smaller definition follows from a dimension count, finite local approximation, or a prepared scalar example.
