# Weighted contact sets from a projective orbit

## Scope

This note records an elementary height-amplification observation under the
same five-contact height premise as the original construction. It gives a
degree-twenty contact product with only twelve distinct roots. It does not
give a smaller defining polynomial: the current local-test packing fails
at the roots of multiplicity three. Those failures are detailed below.

The finite orbit and polynomial identities are checked exactly by
`check_weighted_contact_orbits.py`; its output is
`weighted_contact_orbits_certificate.json`. No numerical approximation or
conjectural computation is used in that certificate.

## Weighted amplification

Let the original projective contact set be

\[
 C=\{\infty,0,1,2401,-343/32\}\subset\mathbf P^1(\mathbf Q).
\]

Assume its retained height bound has exponent nineteen. Let
\(g(z)=(z-1)/(z+1)\), of projective order four. Form the four blocks
\(g^jC\), \(0\le j<4\). Pass to the affine coordinate
\(u=1/(z-2)\); none of the blocks contains \(z=2\).

The orbit \(\{\infty,0,1,-1\}\) occurs with multiplicity three,
because three original contacts lie in that orbit. The other two
orbits each contain four contacts and occur once. Thus the union has
twelve distinct affine contacts, four of multiplicity three and eight
of multiplicity one. The total multiplicity is twenty and every
multiplicity is odd.

Remove a fixed finite set \(\Sigma\) containing the original cutoff,
the matrix determinants, contact denominators and contact differences.
For the j-th block, let \(M_j(u)\) be the product of primes outside
\(\Sigma\) at which u has positive odd contact order with that block.
Define the weighted radical

\[
 M_{\mathrm w}(u)=\prod_{j=0}^3M_j(u)
 =\prod_{\substack{p\notin\Sigma\\
              v_p(u-\theta_p)>0\text{ odd}}}p^{m(\theta_p)}.
\]

Here \(\theta_p\) is unique among the twelve distinct contacts and
\(m(\theta_p)\in\{1,3\}\). Repeated contacts across blocks cause
exactly the displayed multiplicities; pairwise coprimality of the four
block radicals is unnecessary.

The four maps back to the original contact variable are

\[
 2+1/u,\quad(3u+1)/(-u-1),\quad-u/(2u+1),\quad(u+1)/(3u+1).
\]

The maximum absolute row sums of their inverse projective matrices are
3,4,3,4. If E is the product of the newly omitted primes, applying the
original bound to each map gives

\[
 h(u)-\log4\le H E^{19}M_j(u)^{19}.
\]

Multiply these four inequalities when their common left side is positive;
otherwise the conclusion is immediate. The result is the proved bound

\[
 h(u)\le\log4+HE^{19}M_{\mathrm w}(u)^{19/4}.
\]

The coefficient data and exceptional primes are recorded in the exact
certificate. This is a weighted version of the usual four-block argument,
with no disjointness hypothesis on the blocks themselves.

## Exact factorization

In homogeneous coordinates put

\[
 A(z,w)=zw(z^2-w^2),\qquad
 J(z,w)=z^4-6z^2w^2+w^4.
\]

Substitution \((z,w)\mapsto(z-w,z+w)\) multiplies both forms by -4.
Hence J/A is invariant under g. Put

\[
 s=J(2401,1)/A(2401,1),\qquad
 t=J(-343/32,1)/A(-343/32,1).
\]

The weighted binary contact form is, up to nonzero constant,

\[
 A^3(J-sA)(J-tA).
\]

After \((z,w)=(2u+1,u)\), the two quartics become

\[
 A=u+6u^2+11u^3+6u^4=u(u+1)(2u+1)(3u+1),
\]

\[
 J=1+8u+18u^2+8u^3-7u^4.
\]

The certificate compares the normalized degree-twenty expression directly
with the product of the twelve linear factors with multiplicities.

## Why the existing quartic argument does not apply

At a root of multiplicity m and odd simple-contact order v, the detector
valuation is \(\nu=mv\), still positive and odd. Therefore the elementary
noncancellation argument survives. Its consequences must nevertheless be
combined with formal-logarithm errors and with completeness.

Consider the minimal new case \(m=3,v=1\), so \(\nu=3\).
The existing high comparison terms give \(v(C_i),v(G)\ge34\).
The primary reciprocal test gives \(v(f(H))\ge16\), hence primary
depth at least eight and plain-parameter accuracy at least thirty-two.
The alternate reciprocal tests give only \(v(f(V_i))\ge4\), hence
depth at least two and quadratic Taylor accuracy at least twenty-four.
Consequently the justified high comparison order is only twenty-four,
not thirty-four. Relative to the radical weight three, this is order
eight. The Lucas residual estimate would therefore give

\[
 B^2\le C|\Delta|^{19/32}+C_0
       \le C'B^{19/8}+C_0,
\]

which supplies no upper bound on B because \(19/8>2\).
Counting only the extracted C and G valuations overlooks this limitation.

For the input comparison, the analogous minimum is eight, giving the
weighted order \(8/3\). That individual exponent would yield
\(19/(4\cdot8/3)=57/32<2\), but it does not repair the failed Lucas step.

There is a separate completeness obstruction. With \(\nu=3\), the
term \(q^4f(V_i)^4\) has positive valuation only if the alternate
formal depth is at least two. The retained common-index construction
already imposes primary depth at least two, which generically requires
\(h\equiv0\pmod p\); alternate depth at least two requires
\(h\equiv1\pmod p\). These are incompatible at the same rational
contact prime. A general permission to impose finite congruences does
not solve incompatible congruences.

Finally, the evident factorized circuit currently uses more quadratic
coordinates than the five-coordinate symmetric degree-ten circuit of
the 263-variable family. No cheaper circuit or revised compatible local
packing has been proved. The weighted height lemma and orbit identity
may be reusable, but they are not a variable-count improvement.
