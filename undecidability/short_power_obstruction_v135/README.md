# Short-power quotient deletion: local obstructions and the remaining gap (v135)

The short block of [v97](../pell_power_v97/pell_power_replacement.tex), retained in v128/v133/v134, uses \(L=5^{60}\), \(b\ge2\), integer \(s\), and
\[
 T=b^5-1,\quad A=(b^9+8b^5+b-8)/2+5Ts,\quad m=2bA-b^2-1,
\]
\[
 C=L+\delta(A-1),\quad D^2-(A^2-1)C^2=1,\quad
 q=D-(A-b)C-\alpha_*m,\quad \lambda T=q^4-1.
\]
Both quotients \(\delta,\alpha_*\) are certified integers. These are used *before* reconstructing the integral prefix and the growth estimates.

## Deleting either predicate is not a local replacement

Take \(b=2,s=1\), so \(T=31,A=536,m=2139=69T\).

* Drop the delta predicate only. Take the integral Pell index two, \(C=1072,D=574591\), and \(\alpha_*=0\). Then \(q=2143>32=b^5\). The delta quotient is nonintegral (reduce \(C-L\) modulo 5), and \(\lambda\) is nonintegral because \(q^4-1\equiv7\bmod31\). The size requirement \(C^2<c^2\) can hold in this local block by choosing \(c>C\). Even integrality of \(C,D,q\) alone does not repair the lost index congruence.
* Drop the alpha predicate only. Take the genuine Pell index \(L\), \(C=Y_L(A),D=X_L(A)\), and the integral quotient \(\delta=(C-L)/(A-1)\) supplied by the Pell recurrence. Choose \(q=33\) and define the now rational \(\alpha_*=(D-(A-b)C-q)/m\). Since the old Pell residue is \(1\bmod31\) and \(q\equiv2\bmod31\), this quotient is nonintegral. Again \(q>b^5\), \(\lambda\) is nonintegral, and a local size bound can hold by choosing \(c>C\). The huge Pell values need not be explicitly computed.
* A single fixed integer linear combination \(u\delta+v\alpha_*\) also does not locally force both integrality predicates. For \(v\ne0\), use the first Pell pair and set \(\alpha_*=(k-u\delta)/v\) for arbitrary integer \(k\), choosing its sign and magnitude so \(q>b^5\). The delta quotient remains nonintegral. For \(v=0\), use the second pair and arbitrary rational alpha. Thus simply packing the quotients linearly or applying CRT without an independent integral numerator reconstruction does not provide the needed first step.

The statements concern the short-power subsystem; \(c\) is not an unconstrained choice in the full Jones source. These are **not** full-source counterexamples, and they do not rule out a new one-certificate/zero-certificate construction with additional equations or use of the remaining source constraints. The local counterexamples meet the original two size inequalities but not necessarily the coupled binomial growth/margin.

## What remains to prove

A useful replacement must reconstruct the integral prefix without assuming the very Pell growth conclusion that requires that prefix. One route is to force the two congruences from an already certified source integer and a new norm/divisibility identity with controlled denominators. Another is to replace the fixed-power source construction with a different coding identity whose large exponent is no longer required. Neither is completed here. We do **not** restore the 137-row chain; the v134 preferred tables keep the two short-power quotient certificates and all 52 source rows.
