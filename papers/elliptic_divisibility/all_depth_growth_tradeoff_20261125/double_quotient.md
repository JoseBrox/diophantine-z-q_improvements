# Full-depth charging and a nonlocal size bound for the double quotient

## Scope

This concerns the proposed two-point integer quotient from
[point_elimination_limits.md](../../pole_parameters/mixed_class_simultaneous_20261125/point_elimination_limits.md).
It also strengthens the all-depth conic estimate in
[one_conic_foreign_charge](../one_conic_foreign_charge_20261124/README.md)
by removing ordinary abc from the **height charging** step.
It is not a definition of the integers: an actual polynomial
height-cap relation or another nonlocal integer-recognition step
is still missing.

Work first over Q on the retained rank-one rational carrier
\(E:y^2=x^3-2x,\ P=(9/4,-21/8)\). Put \(q=\widehat h(P)>0\).
Write \(H=[h]P,U=[j]P\), \(h,j\ne0\), and
\(g_H^2=x(H),g_U^2=x(U)\) for the square-abscissa charts.
Denote the positive reduced denominator of \(g_{[n]P}\) by \(B_n\).
Assume the exact index divisibilities of the intended source
\[
 h\mid j,\qquad h-1\mid j-1,\qquad |h|\ge2.
\]
The result below is conditional on these divisibilities, not on
their simultaneous Diophantine certification. The integer
\[
                  m=\frac{j-h}{h(h-1)}
\]
then exists, since h and h-1 are coprime.
For the ordinary quotient m=j/h only the first divisibility
is necessary.

## 1. Full foreign denominator mass

Let S be a fixed finite set including 2 and the bad primes.
Put
\[
 \mathcal F(H,U)=
 \sum_{\substack{p\notin S\\ p\nmid B_h}}v_p(B_j)\log p.
\]
No prime multiplicity is truncated here.

For p outside S dividing B_h, the divisibility h|j and the
formal logarithm give exactly
\[
 v_p(B_j)=v_p(B_h)+v_p(j/h).
\]
Consequently
\[
 \mathcal F(H,U)\ge
     \log B_j-\log B_h-\log|j/h|-O(1+\log|j|).       \tag{1}
\]
The O term removes contributions at the finitely many fixed
primes, using the fixed-entry formal-depth formula. This is
uniform even for moving h and j.
By Siegel's theorem in height form (or the full-denominator
asymptotic of Streng, Algebra & Number Theory 2 (2008),
pp. 197–198 (the height estimate following (3.10))),
\[
 \log B_j=qj^2+o(j^2),\qquad \log B_h\le qh^2+O(1).
\]
The error in the first assertion depends only on j and the
fixed carrier; it is uniform in h. Combining with (1),
\[
 \mathcal F(H,U)\ge q(j^2-h^2)-o(j^2)-O(1+\log|j|).
                                                        \tag{2}
\]
This includes every even formal depth. Unlike the earlier
odd-prime estimate, (2) does not consume abc, a primitive
divisor theorem, or any squarefree-mass hypothesis.

## 2. One conic, and an actual quotient bound

Use the all-depth conic
\[
 R=g_U/g_H,\qquad s^2+r^2=R^2.
\]
Here s is one ordinary coordinate and r a finite quadratic
choice; zero roots are permitted, R is nonzero. At a prime
counted in \(\mathcal F\), \(v_p(R)\le-v_p(B_j)\) and
\(\min(v_p(r),v_p(s))\le v_p(R)\). Thus
\[
             h(s)+h(r)\ge\mathcal F(H,U),             \tag{3}
\]
with the zero-coordinate case interpreted in the evident
way, since then the other coordinate equals ±R.
Write \(A=h(s)+h(r)\).

Choose the fixed cutoff for j in the asymptotic so that
the little-oh and logarithmic errors in (2) can be absorbed
into \(qj^2/2+O(1)\). Equations (2)--(3) give
\[
                 j^2\le 2h^2+(2/q)A+O(1)
                                                        \tag{4}
\]
for all nonzero indices, by enlarging the fixed additive
constant for the finitely many small j.
Since \(|h-1|\ge |h|/2\) for \(|h|\ge2\), the double quotient
satisfies the uniform nonlocal bound
\[
 \boxed{\log(1+|m|)
    \le C+\tfrac12\log\bigl(1+A/h^4\bigr).}             \tag{5}
\]
Indeed \(|m|\le2(|j|+|h|)/h^2\); insert (4) and bound
\(1+\sqrt{A/h^4}\le\sqrt{2(1+A/h^4)}\).
All constants depend only on the fixed carrier and
exceptions, not on h,j,s,r. For the ordinary quotient one
similarly obtains the stronger normalized estimate
\[
              \log(1+|j/h|)
                   \le C'+\tfrac12\log(1+A/h^2).
\]

These are proved global upper bounds **in terms of the
charge heights**. They do not yet bound the charges
themselves. In particular adding this conic does not
restrict the point indices: it has the exact rational
solution \((s,r)=(3R/5,4R/5)\) on every guarded tuple.

## 3. A smaller, polynomial-height cap would suffice

For each fixed nonzero integer m the true double quotient
has \(j=h+m h(h-1)\); its height cost is fourth order in h,
rather than the second order cost of the ordinary quotient.
By (2)--(3), for such a family with \(|h|\to\infty\),
\[
          A\ge q m^2 h^4-o(h^4).
\]
Conversely the displayed Pythagorean solution and the
elementary height inequality for R give
\[
          A\le2q(j^2+h^2)+O(1)
             =2qm^2h^4+O_m(|h|^3+1).
\]
Thus a uniform linear bound on A in terms of the usual
base height \(1+h(X)+\widehat h(H)\) would destroy cofinal
completeness **even for a single fixed m nonzero**, not
just for unbounded m. This rules out directly importing
a linear finite-projection height bound.

A uniform polynomial cap
\[
          A\le C_0(1+\widehat h(H))^{2+\epsilon},
          \qquad \epsilon>0\text{ fixed},
                                                        \tag{6}
\]
would, numerically, be compatible with the canonical conic
witnesses for every fixed m by taking h sufficiently
large. It would give \(\log(1+|m|)=O(\log|h|+1)\)
by (5), much stronger than the exponential quotient cap
sought in the earlier approach. The exponent 2 itself
with a fixed coefficient independent of m cannot be
complete on these cofinal families.
There is no claim that (6) is Diophantine or that the
existing height theorem on modular contacts enforces it.
In particular forcing a small odd-contact support of a
charge into the reference support would, under ordinary
abc, give the incompatible linear bound, not (6).

If a nonlocal comparison source supplies a discrepancy
lower bound of the form \(\log(1+|m|)\ge b\widehat h(H)-O(1)\)
for X not equal to m, with b>0, (6) would finish soundness
after a fixed finite reference exclusion. An exponential
cap on A with coefficient smaller than 2b also suffices.
We have not established such a complete double-quotient
source or the required cap.

## 4. The all-depth inequality over the quadratic carrier

For the original quadratic carrier use absolute Weil
height and the maximum formal depth across the two slots.
For h|j, define foreign slots by those where H is not
formal. The weighted finite denominator mass on foreign
slots is at least \(q(j^2-h^2)-o(j^2)-O(1+\log|j|)\):
subtract the mass at the H-formal slots using the same
exact depth identity and the fact that the normalized
prime weights over any rational prime sum to one.
The conic over K \(s^2+r^2=(g_U/g_H)^2\) charges this
weighted mass into \(h_K(s)+h_K(r)\). The same estimates
(4)--(6) hold with these heights. The field s costs two
ordinary rational components, and r is a finite quadratic
choice over K (with the usual finite-algebra encoding).
This is a count of the extension only, not a claim that
two-point comparison over K is complete.

The point of the all-depth transfer is to remove any
need for (OM) or even ordinary abc in the charge lower
bound. The missing upper constraint, which must be
genuinely nonlocal, remains the decisive problem.
