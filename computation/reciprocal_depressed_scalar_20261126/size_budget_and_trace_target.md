# Exact 100 kB budget and a quantitative target for the two-contact height theorem

**Status.** This is not an effective defining specialization. It supplies
an exact finite numerical target for the missing trace estimate in the
161-variable family. No variable count changes. The existing 175-variable
specified construction remains the certified sub-100 kB member under its
stated arithmetic inputs.

## 1. Exact expanded size

Use the unchanged `quartic161.json` table and the same ASCII serialization
as `verify.py`. Its coefficient parameter is \(C=331^N\).
Exactly 17 of the 2858 nonzero coefficient profiles depend on C.
Each dependent profile is of the form \(aC^k+b\), \(k=2\) or \(4\),
\(a\ne0\). For all 17, \(|a|331^k>|b|+1\).
Their absolute values therefore increase with N, remain greater than 1,
and their decimal lengths are nondecreasing. All other terms and all
monomial strings are fixed. Direct integer expansion gives

| N | Bytes |
|---:|---:|
| 1 | 63078 |
| 25 | 66222 |
| 282 | 99902 |
| 283 | 100033 |
| 1000 | 193982 |

Thus **precisely \(1\le N\le282\)** satisfy the strict 100000-byte budget
for this table and serialization. There is no claim that these
specializations define the integers.

The executed BigInt expansion checked these five sizes, the complete
17-profile list and the boundary by integer arithmetic. A separate
Python verifier is supplied in `verify_size_budget.py`.

## 2. Sufficient quantitative trace target

Use the original two-contact midpoint 1 and the five-element list
\[
 \Theta=\{0,-1/2,-1,1/2399,-32/407\},\qquad
 \Theta^*=\Theta\cup(2-\Theta).
\]
The following argument **requires** the small-exception-set version of
the local comparison divisibilities:
\[
 M_j^3\mid a\Delta\quad(\Delta\ne0),\qquad
 M_j^3\mid J_X\quad(J_X\ne0),
\]
where \(M_j\) is the product of the primes of positive odd contact valuation
outside
\[
 \Gamma=\{2,3,5,7,11,13,17,37,41,47,67,109,179,257,439,
            2099,2399,2029147\}.
\]
This is the same valuation calculation as the effective midpoint
\(3/22\) case in v68 and v82, with contact collisions and midpoint
differences now excluded by \(\Gamma\). The four-factor proof of v78
uses only good unramified slots, the relative order-four formal
logarithm, reciprocal-abscissa valuation parity, and the native
pole obstruction. The BB-native obstruction excludes every negative
odd valuation away from 7; the rational scaling has positive valuation
only at 2,3,17. These primes lie in \(\Gamma\). No lower bound on the
prime size beyond these exceptions is required by that calculation.
Equivalently one can read the quantitative target below as conditional
also on this precise small-exception-set divisibility version.

The support verification uses all denominators of \(\Theta^*\), all
nonzero differences of its members, and all midpoint differences.
Write \(J_*=\prod_{p\in\Gamma}p<2^{116}\).
Apply H4.1 of v68 to \(u_+=2+1/t,\ u_-=2+1/(2-t)\).
These are the same projective contact transformations as v68.
Outside \(\Gamma\) their two five-contact radicals are disjoint,
with product \(M\). The height loss of either inverse transformation
is less than \(\log 10\). As in v68, taking the geometric mean of
the two estimates, with \(c_0C_0<2^{149}\), gives
\[
 h(t)\le\log 10+c_0 C_0 J_*^2 E(J_*)M\sqrt{E(M)}
                   (\log J_*+\tfrac12\log M).
\]
All \(t\) outside the contact set are allowed, including the midpoint.
Here \(E(n)=\prod_{p\mid n}(1+1/p)\le1+\log n\).
Since \(\log J_*<128\), \(E(J_*)<128\),
and \((1+x)^{3/2}<64e^{x/6}\) for \(x\ge0\)
(maximize the quotient by differentiation), we get the deliberately
loose effective bound
\[
                           h(t)<2^{410}M^{7/6}.
\]
It follows from \(T=t_1-t_0\), the triangle inequality for heights
and the two separate divisibilities that for either nonzero residual
\(J_0=a\Delta\) or \(J_0=J_X\),
\[
                           h(T)<2^{412}|J_0|^{7/18}.
\]

The remaining trace target is a proof, on the full allowed point
domain, of
\[
 B_0^2\le A(h(R)+h(T))+J,\qquad
                 A\le 2^{140},\qquad J\le 2^{20000}.
\]
These particular bounds are sufficient, not necessary. Neither numerical
inequality for the trace constants is claimed proved.

Indeed choose \(N=282\). The old scalar proof yields
\[
 c_a=|a|\ge331^{1272}>2^{10176},\quad
 h(\beta)<c_a/2,\quad h(R)<c_a .
\]
The latter two follow from
\(h(u)<2^{301}331^{-1272}c_a\) and the original map-height estimates;
the logarithm of the fixed multiplier is below 4000.
Consequently \(Ah(R)+J<B_0^2/2\), since \(B_0\ge c_a\).
If \(\Delta\ne0\), use \(|a\Delta|\le14B_0^5\) to get
\[
 B_0^{1/18}<2^{1+140+412}14^{7/18}<2^{555}.
\]
But \(B_0>2^{10176}\) implies \(B_0^{1/18}>2^{565}\).
Thus \(\Delta=0\).
If \(J_X\ne0\), then \(|J_X|\le4B_0e^{h(\beta)}\), and hence
\[
 (29/18)\log B_0
 <(553+7/9)\log2+(7/18)h(\beta).
\]
This implies \(\log B_0<400+c_a\), contrary to the unchanged Lucas
lower bound \((c_a-6)\log(c_a-3)\).
The usual half-integral input-label argument then proves integrality.

All preceding ordered integer completeness arguments are retained.
Thus the stated numerical trace target would suffice for a defining
161-variable quartic of 99902 bytes. The von Buhren bound presently
used by the two-contact construction does not furnish this numerical
control. A finite expansion or a bounded search of elliptic multiples
cannot fill that gap. In particular the additive constant may not
simply be chosen smaller than the displayed bound.
