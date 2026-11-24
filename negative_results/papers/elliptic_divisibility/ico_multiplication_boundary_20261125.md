# Boundary complexity of rational ico lifts on multiplication graphs

## Result and scope

This note complements the
[optimal off-diagonal interpolation](../../../papers/elliptic_divisibility/ico_boundary_interpolation_20261125/README.md).
It extends the obstruction from fixed rational graphs \(t=T(w)\) to
rational-function lifts on the elliptic reference curve that may be
chosen separately for every integer multiplier, with no bound on the
degrees of the chosen functions. The argument combines the moduli
interpretation of the ico surface, weak boundedness of period maps,
and ordinary rational abc.

It does not rule out choosing different arithmetic lifts at individual
rational points, nor a one-reference-per-input construction with a
varying lift.

Let \(E:y^2=x^3-2x\), \(R_0=(2,2)\), \(P=[2]R_0\), and
\(q=\widehat h(P)>0\). Put
\[
 f(Q)=\frac{x(Q)^2+2}{2y(Q)},\qquad f(Q)^2=x([2]Q).
\]
The reference and numerator in the true multiplication family are
\(H=[2]Q,\ U=[2m]Q\), with \(Q=[h]R_0\) and \(m\ne0\) integral.
The degree of \(f\) is four: its four simple poles are the geometric
two-torsion points, including the identity.

Let \(\mathcal S\subset\mathbb P^4\) be the ico surface and
\(\Delta\) its five coordinate points, so \(M=\mathcal S\setminus\Delta\).
Use the guarded plane chart and its inverse \(w,t\) from the
[ico cap](../../../papers/elliptic_divisibility/ico_exponential_cap_20261125/README.md).
For a rational point \(Z\in M(\mathbb Q)\) denote by \(B(Z)\) its
boundary radical, the product of primes with coordinate-point reduction.

**Theorem.** Assume ordinary rational abc. Fix a constant \(C>0\).
For every sufficiently large \(|m|\), there is no rational map
\(\phi_m:E\dashrightarrow\mathcal S\), defined over \(\mathbb Q\),
whose generic image is in the guarded chart and satisfies
\[
                      w\circ\phi_m=\pm f\circ[m],
                      \tag{1}
\]
such that
\[
        \log B(\phi_m([h]R_0))\le Cqh^2+O_m(1)
                      \tag{2}
\]
holds for arbitrarily large \(|h|\) on defined guarded values.
The fixed additive constant in (2) is even allowed to depend on
the particular chosen map and multiplier. The map need not be
given by a formula uniform in \(m\), and its degree is not assumed
bounded.

In particular a rational-function selection of the plane coordinate
\(t\), even separately for every \(m\), cannot restore
arbitrarily-large-reference completeness of the direct ico cap with
a fixed-coefficient exponential height budget obtained from
controlled diagonal prime support. This holds with arbitrarily many
mixed integer coefficients of arbitrary magnitudes and arbitrary
polynomial degrees. Only the necessary inclusion of the boundary
radical in the diagonal prime support is used.

## 1. Bounded punctures imply bounded degree

The needed geometric input is weak boundedness of the complex
Hilbert modular surface \(M\). We explain its applicability to
this particular coarse model rather than assuming arbitrary rational
surfaces have this property.

Fan--von Känel, *Rational points and rational moduli spaces*,
[arXiv:2501.17155v2](https://arxiv.org/html/2501.17155v2),
equation (7.5), identify the complement of the five coordinate
points as a coarse Hilbert moduli scheme of finite level. Its
branch locus over \(\mathbb C\) is empty: the five-point
degeneracy locus includes both the compactification boundary and
the branch locus of the coarse moduli scheme. In the proof of
their Proposition 5.2, their finite-level and empty-branch
conditions give a finite étale surjective scheme cover obtained
by adding level data to the moduli stack. This same argument
applies to \(M_{\mathbb C}\) itself. Choose such a cover
\(M'\to M_{\mathbb C}\) of finite degree \(d_0\), with the
universal family of abelian surfaces (and the fixed Hilbert
moduli data). Its period map is quasi-finite: the forgetful
map from the restricted real multiplication and level data
has finite fibers on complex abelian surfaces, by the finite
level and Hilbert moduli properties. Equivalently one can use
a sufficiently high torsion-free congruence cover of the
Hilbert modular variety.

We use A. Javanpeykar and D. Litt, *Integral points on algebraic
subvarieties of period domains: from number fields to finitely
generated fields*, Manuscripta Mathematica 173 (2024), 23--44,
[DOI](https://doi.org/10.1007/s00229-023-01463-w), Definition 3.3
and Theorem 4.2 (or Theorem 6.1 for a torsion-free congruence
cover). Their weak boundedness theorem for quasi-finite period
maps gives a fixed projective compactification \(V\) of \(M'\)
and a fixed ample line bundle on it for which the following
statement holds: degrees of maps from punctured smooth
projective curves are uniformly bounded when the genus and
the number of punctures of the source are bounded. This is
a characteristic-zero geometric theorem, not an arithmetic
uniformity assumption for arbitrary higher-genus rational points.

Let \(\phi:E\to\mathcal S_{\mathbb C}\) be any morphism whose
generic image is in the guarded chart. Put
\[
 r_\phi=\#\phi^{-1}(\Delta)(\mathbb C).
\]
The set is finite, since the map is not constant into
\(\Delta\). Over \(E^\circ=E\setminus\phi^{-1}(\Delta)\),
pull back \(M'\to M\) and take a connected component. It is a
finite étale cover of degree \(d\), \(1\le d\le d_0\).
Its smooth projective completion \(C'\) maps finitely to \(E\)
with ramification only above the \(r_\phi\) punctures. The number
of deleted points on \(C'\) is at most \(dr_\phi\).
Riemann--Hurwitz gives
\[
     2g(C')-2\le dr_\phi .
\]
Here the base genus is one, and the ramification contribution
over any one puncture is at most \(d-1\), so the weaker bound
\(d\) per puncture suffices.

If \(r_\phi\le r_*\) for a fixed integer \(r_*\), both the genus
and puncture count are bounded independently of \(\phi\).
Weak boundedness of \(M'\) therefore bounds the degree of the
extended map \(C'\to V\) with respect to its fixed ample bundle.

The fixed rational inverse-chart function \(w\) pulls back to a
rational function on \(M'\), regular on the corresponding chart
open. Its degree after composition with a curve map is at most
a fixed multiple of the degree of that map to \(V\), when the
generic image lies in that open. For detail, embed \(V\) by a
fixed power of the ample bundle. The rational function \(w\)
can be written as ratios of homogeneous forms of bounded fixed
degree on finitely many opens covering its regular locus in the
chart (use quasi-compactness and local numerator-denominator
representations in projective affine charts). For each curve
choose a representation whose denominator is nonzero at its
generic point. The degree of the ratio on \(C'\), after
canceling common zeros, is no greater than the degree of the
pulled-back homogeneous form. Taking the maximum of the finite
list of degrees gives the asserted uniform multiple.

The degree of the function on \(C'\) equals
\(d\deg(w\circ\phi)\). Thus we have proved the implication
\[
     r_\phi\le r_*
       \quad\Longrightarrow\quad
     \deg(w\circ\phi)\le K(r_*)                         \tag{3}
\]
for a fixed finite constant \(K(r_*)\).
No numerical or linear dependence of \(K\) on \(r_*\) is
claimed. Such a dependence would require a quantitative
Arakelov bound in the chosen compactification, not merely
the cited weak boundedness theorem. In particular (1), for
which \(\deg(w\circ\phi_m)=4m^2\), forces \(r_{\phi_m}\) to
tend to infinity as \(|m|\to\infty\), uniformly over all
possible maps satisfying (1).

This argument works without a bound on the degree of the
function \(t\) or on the coefficient degrees of \(\phi_m\).

## 2. From geometric punctures to arithmetic boundary mass

Fix one such rational map \(\phi=\phi_m\) for the moment.
Since \(E\) is a smooth projective curve and \(\mathcal S\)
is projective, the rational map extends to a morphism on
\(E\), regardless of its initial rational-function base
points. Its inverse image \(D=\phi^{-1}(\Delta)_{\rm red}\)
is a finite reduced Galois-invariant set of \(r=r_\phi\)
geometric points.

We apply the marked-Belyi contact argument already proved
in the project's
[odd-pole obstruction](../pole_parameters/quotient_cap_pole_obstruction_20261124.md).
Choose a marked Belyi map \(\pi:E\to\mathbb P^1\) over
\(\mathbb Q\) such that \(D\) is contained in its geometric
inverse image of \(0,1,\infty\). This map is fixed **after**
fixing \(\phi\); there is no uniformity assumption on its degree.
If its degree is \(d_\pi\), the reduced contact set has exactly
\(d_\pi\) points, by Riemann--Hurwitz in genus one. Write
\(q_0=\widehat h(R_0)=q/4\).

For clarity, the arithmetic argument uses a fixed splitting
field of all these geometric contacts. At each contact \(D_i\)
the full normalized finite contact height of \(Q_h=[h]R_0\)
is at most \(q_0h^2+O(|h|+1)\), using the abscissa height
of \(Q_h-D_i\). Meanwhile
\[
 h_{\rm W}(\pi(Q_h))=d_\pi q_0h^2+O(|h|+1)
\]
by the degree of its pole divisor and canonical height
comparison on the elliptic curve. Ordinary rational abc,
applied to the rational value \(\pi(Q_h)\), says that the
total normalized truncated contact height is
at least \(d_\pi q_0h^2-o(h^2)\).
Indeed the corresponding statement with loss depending
on a fixed exponent \(1+\epsilon\) follows directly from
abc; take liminf and then let \(\epsilon\) decrease to zero.
The equality of rational and extension truncated counts
holds after excluding finitely many ramified and bad primes,
and those where distinct contacts coincide in reduction.
The sum of the individual full-height upper bounds
forces each contact's truncated height to be
\(q_0h^2+o(h^2)\), and its multiplicity surplus to be
\(o(h^2)\). Thus simple contacts already give this mass.

All finite exclusions here are fixed for the chosen \(\phi,\pi\);
they may depend on \(m\) and the particular map. At the remaining
primes the morphism \(\phi\) and the distinct marked points have
good spreading-out models. A simple contact with any point
of \(D\) implies coordinate-point reduction of \(\phi(Q_h)\).
At a fixed extension place there is at most one such contact
because all the marked reductions are distinct.
The sum of the normalized prime weights over any rational
prime is at most its rational logarithmic weight, and any
rational prime counted this way lies in \(B(\phi(Q_h))\).
Consequently adding the \(r\) distinct geometric contact
masses gives
\[
            \log B(\phi(Q_h))
                   \ge r q_0 h^2-o_\phi(h^2).
                   \tag{4}
\]
This deduction does not count one rational prime \(r\)
times: the weighted sum is over places of the one splitting
field, and there is at most one contact per place. In
particular it does not assume that all geometric contacts
are rational or torsion. Points where \(Q_h\) itself is
a marked point may be omitted, a finite number of indices.

## 3. Proof of the obstruction

If the budget (2) held for arbitrarily large \(|h|\) for
this fixed map, dividing (4) by \(qh^2\) and taking a limit
would give \(r\le4C\).
The uniform geometric implication (3) then gives
\[
                       4m^2\le K(\lfloor4C\rfloor).
\]
This bounds \(|m|\) by a constant independent of the chosen
rational map, proving the theorem.

A finite menu of rational maps for each fixed \(m\) gives
the same conclusion: if the union of their accepted
reference-index sets is unbounded, some one map has
unbounded accepted indices. The menu may vary with \(m\).
For a separate ico construction using integer forms
\(F\) that are allowed to vary even at each individual
reference, the interpolation theorem's necessary inclusion
\(B(\phi(Q_h))\mid\nu_F\) suffices. Thus any uniform budget
on \(\log\nu_F\) gives the same contradiction, without
any bound on the number, degrees, or mixed coefficients
of those forms.

## 4. Limitations

This result does not prove a uniform-in-\(\phi\) finite bound
on the exceptional indices \(h\) for which (2) can hold.
The rational abc constant for a marked Belyi map and the
finite exceptional-prime set depend on the chosen map.
The order of quantifiers is essential: fix a multiplier
and its finite menu of maps before letting \(|h|\to\infty\).
The theorem does not exclude an arithmetic choice of the
plane lift depending on each individual reference index,
even if that choice belongs to an infinite family of
rational maps. It also does not exclude a higher-genus
multisection with finitely many rational points chosen
separately at each input, or a single bounded reference
per integer. In particular the earlier
[bounded-reference theorem](../../../papers/elliptic_divisibility/bounded_reference_20261125/README.md)
remains relevant.

The proof is a geometric obstruction, conditional on
ordinary rational abc only in Section 2, with the cited
moduli and weak boundedness theorems as external inputs.
It is not a claim that general completeness of all ico
caps is impossible. No new defining-polynomial count
is claimed.
