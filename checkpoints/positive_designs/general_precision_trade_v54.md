# A corrected precision trade for the general source

## Status

This is a checked source-design calculation, not a completed source-transfer
theorem and not a variable reduction. A full local, completeness, and
whole-character guard audit remains necessary. No numerical degree or
coefficient bound has been computed for this revision.

Write s=n_S, c=|s-1|, and
\[
 B_{\rm ind}=\max\{|n_A|,|s|,|t|,|z|\}.
\]
All point roles remain present. The purpose is to trade degree for a
weaker scalar-depth requirement, potentially making a future reuse of
point roles easier.

## Proposed changes

1. Give the last two scalar tests order two, retaining order one for the first four.
2. Replace the Lucas residual by \({\cal F}(L_S^2,L_T,L_Z)\).
3. Give the three Lucas comparison tests and this residual order six.
4. Raise the ten reciprocal point-test orders from one to three.

The last change is essential for formal-group precision; it is not an
optional strengthening.

## Scalar inequalities

If the revised extraction is established with these orders, it gives
\[
 v_p(c)>\frac54|v_p(\rho)|.
\]
Thus each scalar alternative contributes \(p^2\mid c\).
The unchanged five-contact height estimate then yields
\[
 h(\beta)\le Cc^{7/6},\qquad
 h(\rho)\le Cc^{7/6}+C\log c+C.
\]
At the consumed prime, \(v_\ell(c)>5L/4\), so c still grows uniformly
with the source parameter L.

## Residual and height comparison

Let \(\Delta={\cal F}(s^2,t,z)\), which has total degree six.
The desired strengthened mixed alternatives imply
\[
 M_j^6\mid\Delta c^3.
\]
The original comparison contact-height exponent \(7/6\) then gives
\[
 B_{\rm ind}^2\le
 C(|\Delta|c^3)^{7/36}+Cc^{7/6}+C\log c+C.
\]
Since \(|\Delta|\le C B_{\rm ind}^6\) and \(c\le B_{\rm ind}+1\),
the first exponent is
\[
 (6+3)\frac7{36}=\frac74<2,
\]
and the scalar error exponent \(7/6\) is also below two.
The large-c contradiction therefore has the necessary strict exponent
inequalities to force \(\Delta=0\).

Applying the retained integer Lucas lemma with parameter \(s^2\) would
then give
\[
 \log B_{\rm ind}>|s^2-1|-4\ge c(c-2)-4.
\]
The nonzero input-residual argument would instead imply
\[
 \log B_{\rm ind}\le Cc^{7/6}+C\log c+C,
\]
which contradicts that quadratic growth for sufficiently large c.

These statements describe what follows from the strengthened source
inequalities; they do not replace the remaining transfer audit.

## Precision and completeness obligations

Successful reciprocal-test order three gives \(v(f)\ge3\).
Because formal abscissa valuations are even, the formal parameter then
has order at least two. On the j=1728 source curve the logarithmic quotient
error has order at least eight, enough for comparison modulo p^6.
The old order-one reciprocal tests only provided error order four and
would not justify this calculation.

For completeness the selected-prime congruence refinement must give
reciprocal-test order at least four and comparison error at least eight.
The existing arbitrary-depth refinement appears relevant, but its
ordered use with all other requirements must be proved. The explicit
Lucas witness must use parameter s^2 and retain parity and avoidance;
choosing s odd and s congruent to1 modulo3 is a proposed compatible choice,
not a completed source proof.

No free rational coordinate has been introduced by these formal changes.
Their validity as a full Diophantine source remains open.

## Excluded weaker variant

The earlier order-one scalar idea would only give \(h(\beta)\ll c^{7/3}\).
That error can exceed \(B_{\rm ind}^2\) before the Lucas residual is
known to vanish. A favorable residual exponent alone does not fix this.
The corrected order-two calculation above avoids that particular gap.
