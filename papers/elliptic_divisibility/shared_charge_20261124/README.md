# A single conic charge for an entire tuple of elliptic quotients

This continues the
[one-conic foreign charge](../one_conic_foreign_charge_20261124/README.md)
and the
[adaptive joint quotient transfer](../adaptive_joint_quotient_20261124/README.md).
The objective is to share the charge as well as the reference, scalar pole
and direct index-residual tests.

The result proves a new simultaneous charging relation using **one ordinary
coordinate and one finite root, independently of the tuple length**.
It does not prove an upper cap on that coordinate.

## 1. Assumptions and construction

Use the same rational curve \(E:y^2=x^3-2x\), point \(P\), and
\(q=\widehat h(P)>0\). Let \(U_i=[j_i]P\ne O\), for \(1\le i\le r\),
with nonzero integer indices and \(g_i^2=x(U_i)\).
Put
\[
          J=\max_{1\le i\le r}|j_i|,\qquad
          L=\sum_{i=1}^r g_i^{\,2i-1}.
\]
Adjoin the one conic
\[
             R^2=1+Ls^2,\qquad s\ne0,\qquad L\ne0.
             \tag{1}
\]
The \(g_i\) are the existing square-abscissa coordinates, so \(L\)
is a fixed polynomial in them. Retain the ordinary coordinate \(s\)
and encode \(R\) as one finite monic root. The guards are part of
the existing selected-character encoder.

The sign of a square root \(g_i\) is irrelevant to the physical point
\(U_i\), since its finite ordinate character changes simultaneously
when that sign is changed. In completeness choose all \(g_i>0\);
then \(L>0\). For arbitrary solutions no positivity is needed in
the local proof below. For every actual tuple with \(L\ne0\),
\[
       s=\frac{2t}{1-Lt^2},\qquad R=\frac{1+Lt^2}{1-Lt^2}
       \tag{2}
\]
gives rational lifts for all \(t\ne0\) outside its finitely many
poles. In particular take \(t=1\), or \(t=2\) when \(L=1\).
This supplies complete lifts with
\(h_{\rm W}(s)\le h_{\rm W}(L)+O(1)\). There is no new
simultaneous rational-point realization assumption.

## 2. All simple primes outside a negligible surplus

Assume ordinary rational abc and use the rational doubled-point
simple-denominator mass theorem already established in the project:
if \(B_n\) is the denominator of a reduced square root of
\(x([n]P)\), then
\[
    \log\prod_{v_p(B_n)=1}p=q n^2+o(n^2),\qquad
    \log B_n\le qn^2+O(1).
\]
It follows, by subtracting the simple mass from the total weight
of the denominator, that
\[
       \sum_{p:\ v_p(B_n)\ge2} v_p(B_n)\log p=o(n^2).
       \tag{3}
\]
In particular the logarithmic weight of the radical of the
higher-depth primes is \(o(n^2)\). All these estimates are for
one fixed elliptic sequence; their implied errors are independent
of the choice of the other points.

Choose any \(i_*\) with \(|j_{i_*}|=J\). Start with its simple
denominator prime set, remove the fixed bad primes and every prime
which has higher denominator depth in **any** \(U_i\). For fixed
tuple length \(r\), (3) bounds the total removed logarithmic mass
by \(o(J^2)\), uniformly as \(J\longrightarrow\infty\).
To see uniformity explicitly, for each \(\epsilon>0\) choose a
fixed index cutoff beyond which the error in (3) is bounded by
\(\epsilon n^2\). For the finitely many smaller indices take
the maximum of their higher-depth masses. Summing gives at most
\(r\epsilon J^2+O_\epsilon(1)\).
The remaining prime product \(F\) therefore has
\[
                       \log F=qJ^2-o(J^2).
                       \tag{4}
\]

At such a prime \(p\), every \(g_i\) has valuation either \(-1\)
or a nonnegative integer, and at least one valuation is \(-1\).
Let \(i_0\) be the largest index with \(v_p(g_{i_0})=-1\).
The corresponding term of \(L\) is the unique negative minimum,
of valuation \(-(2i_0-1)\). In particular no cancellation is
possible, irrespective of the splitting of \(p\) in any field
and irrespective of the chosen signs of the roots.
In (1), if \(2v_p(s)<2i_0-1\), the term \(Ls^2\) would have
negative odd valuation. The other term is 1, so the right-hand
side could not be a rational square. Equality is impossible by
parity. Consequently
\[
                        v_p(s)\ge i_0\ge1.
\]
Every retained prime divides the reduced numerator of \(s\).
By (4), we have the uniform lower bound
\[
                        h_{\rm W}(s)\ge qJ^2-o(J^2).
                        \tag{5}
\]
This is an all-prime argument, not a density assertion about
primes inert in a prescribed quadratic field. It does omit
higher-depth primes, but their contribution is negligible for
the maximum index by the fixed-sequence ordinary-abc theorem.

For a variant literally retaining the foreign-prime interpretation,
replace \(L\) by \(L/g_H^2\) where \(g_H^2=x(H)\), and in (4)
also remove primes of the numerator or denominator of \(g_H\).
The loss is at most \(2qh^2+O(1)\); the same proof gives
\(h_{\rm W}(s)\ge qJ^2-2qh^2-o(J^2)-O(1)\).
For bounding the largest label the simpler unnormalized \(L\)
in (1) is preferable.

## 3. One independent cap would now suffice for every label

In the adaptive joint quotient relation of the preceding note
\(h\mid j_i\) and \(m_i=j_i/h\) is integral.
Appending (1) brings its total ordinary coordinate count from
\(k+r+4\) to **\(k+r+5\)**, not \(k+2r+4\).
The simple mass estimate (5) bounds every \(|j_i|\) simultaneously.

Suppose a new complete auxiliary constraint could establish
\[
                \log(1+h_{\rm W}(s))\le A qh^2+O(1).
                \tag{6}
\]
For sufficiently large \(J\), (5) gives
\(h_{\rm W}(s)\ge(q/2)J^2\), hence
\[
           \log(1+\max_i|m_i|)\le (A/2)qh^2+O(1).
\]
The same bound for bounded \(J\) follows by enlarging the constant.
Choose the fixed logarithm precision \(N\) so large that
\[
   \frac9{10}(N+2)-\frac{D}{100}
                  > \frac{A}{2}\max(1,D),
\]
where \(D\ge1\) bounds all the total polynomial-residual degrees.
The adaptive joint discrepancy theorem then forces every input
equality \(X_i=m_i\) and every prescribed polynomial equality
\(\Psi_\nu(X,m)=0\) at all zeros beyond a fixed reference cutoff.
If the extra cap constraint has the required true integer
completeness and uses two more ordinary coordinates, this
would yield a complete **\(k+r+7\)-coordinate** direct-index
transfer. The nonzero label convention is inherited from the
point chart; shifts and finite disjunctions treat required zero
labels. This is a conditional reduction of the remaining goal,
not a proof of (6).

For \(k=r=1\) the count is nine, exactly the present target.
For polynomial coding relations with multiple hidden labels,
a single shared cap would suffice rather than independently
bounding each charge. This is the reverse-transfer advantage
for the undecidability part of the project as well.

## 4. True-witness height scale and limits

For fixed true labels \(j_i=hm_i\), the usual square-abscissa
height formula \(h_{\rm W}(g_i)=qm_i^2h^2+O(1)\) gives
\[
     h_{\rm W}(L)\le qh^2\sum_i(2i-1)m_i^2+O_r(1).
\]
The rational lifts (2) thus have heights bounded by the same
linear expression, and satisfy the lower bound (5).
The bound has the required multiplier-dependent coefficient:
it does not mistakenly constrain the charge linearly with a
constant independent of all integer multipliers.

All previous CRT false witnesses survive (1), by choosing the
root signs positive. In particular the charge is unbounded at
fixed reference and fixed input on those witnesses.
No independent upper height constraint or defining-variable
improvement is claimed. The construction shares the missing
global cap among arbitrarily many numerator points; it does not
make that missing arithmetic restriction disappear.
