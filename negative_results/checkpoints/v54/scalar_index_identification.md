# Reduction orders in the proposed identification of scalar and input roots

## Exact coordinate saving and missing transfer

Identifying S=A and U_S=U_A removes four rational coordinates from the
general source. This is a coordinate count only. A defining polynomial
still requires a complete soundness and completeness argument.

For
\[
R(q)=q(q-1)(q-2401)(32q+343),\qquad
\beta=1+M R(q)^k,
\]
deep divisibility of \(\beta-1\) by contact primes does not imply that
\([\beta-1]P\) is in the formal group. The reduction order must also divide
the index.

## Certified counterexample to that divisibility implication

Take \(p=802231\), \(\ell=100279\), and \(q=p\).
Both \(p,\ell\) are prime. At the split place of \(K=\mathbb Q(\sqrt2)\)
with \(\sqrt2=254335\pmod p\), the source point reduces to
\[
 \widetilde P=(413460,581683)
\]
and has exact prime order \(\ell\). At the conjugate place its exact order
is \(2\ell=200558\). Direct arithmetic gives
\[
 v_p(R(p))=1,\qquad R(p)=10141\pmod\ell.
\]
Consequently, for every \(k\ge1\) and every \(M\) with \(\ell\nmid M\),
\[
 [M R(p)^k]\widetilde P\ne O.
\]
This defeats the proposed prescribed root \(S=[\beta]P\) at this scalar
contact, independently of the exponent used to deepen p-adic divisibility.
It does not exclude all fixed multipliers M: including \(\ell\) repairs
this particular example, and a new argument would be needed for the
other varying scalar-support primes.

The accompanying exact BigInt checker independently verifies both
primality statements, the split square root, the point, both exact
orders, and the valuation-one contact.

## Other scoped failures

Fixing the scalar can permit preparation at its finitely many support
primes. It removes the original input-height estimate
\[
 h(\beta(X))\le Cc^{7/9},\qquad c=|n_A-1|.
\]
Before the input residual has been shown to vanish, replacing n_A by
beta(X) is circular.

The integral status of the Lucas parameter cannot simply be omitted.
For
\[
 {\cal F}(a,t,b)=t^2-a(a-2)tb+(a-2)^2b^2-1
\]
there is the exact solution
\[
 (a,t,b)=(87/5,111,125),\qquad {\cal F}(a,t,b)=0,
\]
although \(\log125<a-5\). The checker verifies the rational identity by
clearing its denominator. The growth comparison follows, for example,
from \(\log125<5<62/5=a-5\).

No complete 21-variable source follows from these proposals. The
constructive gap is a scalar/label mechanism that supplies both the
input-height estimate and reduction-order divisibility while reusing
the point role. This note is a recovery audit, not a general lower bound.
