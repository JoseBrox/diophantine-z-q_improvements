# Algebraic-fiber and rational-Lucas obstructions to the charge-height cap

We continue the
[one-conic foreign charge](../../../papers/elliptic_divisibility/one_conic_foreign_charge_20261124/README.md)
and its proposed upper bound
\[
                 \log(1+h_{\rm W}(s))\le A qh^2+O(1).
                 \tag{1}
\]
Here \(H=[h]P\), \(U=[j]P\), \(q=\widehat h(P)>0\) on
\(E:y^2=x^3-2x\), and \(h_{\rm W}\) is the rational logarithmic height.
The charge equation is
\[
             r^2=1+(g_U/g_H^2)s^2,\qquad s\ne0,\qquad
             g_V^2=x(V).
             \tag{2}
\]
We retain ordinary rational abc and the inherited cyclic-group input.
The statements below exclude several inexpensive ways to establish (1).
They do not exclude genuinely coupled new arithmetic geometry.

## 1. Uniformly finite algebraic projection is too strong

By the previous all-prime charge and full simple denominator theorem,
for any fixed finite excluded prime set the following inequality holds
on (2):
\[
     h_{\rm W}(s)\ge qj^2-qh^2-o(j^2)-O(1).
     \tag{3}
\]
Indeed the simple denominator primes of \(U\) which are not denominator
primes of \(H\) all divide the numerator of \(s\). Their logarithmic
weight is at least the right hand side, since removing the support
of the denominator of \(H\) loses at most \(qh^2+O(1)\).
The little-oh is uniform in the reference, since it is a statement
about the fixed sequence indexed by \(j\).

Suppose an auxiliary cap condition entails a fixed nonzero algebraic
equation
\[
              \sum_{i=0}^D a_i(X,H) s^i=0,                 \tag{4}
\]
with the \(a_i\) rational functions of bounded degree and fixed
rational coefficients on the input/reference base
\(\mathbb A^1\times E\), or its fixed square-abscissa chart.
The functions must be defined at the witnesses and not all vanish
there. Fixed finite algebraic covers of the base, followed by
norms, are allowed when they supply an equation with these properties.

The rational-root height estimate gives
\[
                  h_{\rm W}(s)\le C(qh^2+h_{\rm W}(X)+1)
                  \tag{5}
\]
with a constant independent of the witnesses.
For clarity, to prove the estimate specialize the coefficients of
(4), discard any leading zeros, clear their denominators and divide
out common content. If \(s\ne0\), also discard the initial zero
coefficients by dividing by a power of \(s\). By the rational-root
theorem the reduced numerator of \(s\) divides the resulting
nonzero constant term, and its denominator divides the nonzero
leading coefficient. Their logarithmic absolute values are bounded
by the sum of the specialized coefficient heights plus a fixed
constant. The standard height inequalities for fixed rational
functions, and \(h_{\rm W}(x(H))=2qh^2+O(1)\),
\(h_{\rm W}(y(H))\le3qh^2+O(1)\), prove (5). The same estimate
holds in the square-root chart.

This is incompatible with complete true integer witnesses of (2)
on (4) for unbounded integer inputs \(X=m\), \(j=mh\),
**even if only one reference per input is required**. In fact, for
all sufficiently large \(|j|\), (3) gives
\[
                   h_{\rm W}(s)\ge qj^2/2-qh^2-O(1).
\]
Substitution of \(j=mh\) and \(h_{\rm W}(m)=\log|m|\) into (5) yields
\[
    (m^2/2-1-C)qh^2\le C(1+\log|m|)+O(1).
\]
Since \(|h|\ge1\), this bounds \(|m|\) by a fixed constant.

The argument also applies to a fixed finite list of equations or
branches satisfying the same nondegeneracy condition, by taking
the maximum of their height constants.

### Consequence for eliminating the auxiliary variables

Suppose a fixed algebraic condition on the base \((X,H)\), the
charge \(s\), and any finite number of additional variables has
projection to \((X,H,s)\) contained in a proper algebraic subset
of that space, over \(\mathbb Q\). For an integral base (or after
restricting to one component of the fixed chart), this gives a
nonzero polynomial relation of the form (4) on a dense open of the
base. The possible coefficient degeneration and poles lie in a fixed
proper closed subset of \(\mathbb A^1\times E\).
For every fixed integer \(X=m\) outside a finite exceptional set,
this subset contains at most finitely many reference points on the
curve. Thus the proposed condition cannot have true integer
witnesses with arbitrarily large reference index for every integer
input. This is an elimination obstruction, not a count of auxiliary
variables.

In particular a generic finite algebraic projection to the charge
over the input/reference base is too restrictive. Replacing several
ordinary coordinates by finite root encodings cannot by itself
implement (1) in this manner. Nonconstant rational functions with
an algebraically finite fiber necessarily give a *linear* height
bound, whereas the actual charge requires a bound whose linear
coefficient grows at least as \(m^2-1\) at a true multiplier \(m\).

The assertion does not apply to a finite algebraic equation whose
coefficients also depend on \(U\): those coefficient heights may
already contain \(qj^2\). Nor does it apply when the charge projection
is algebraically infinite but only arithmetically finite.

## 2. Low-genus standalone cap fibers

Consider a proposed additional relation on \((X,H,s)\) and at most
two ordinary auxiliary variables which is independent of \(U\).
For each fixed admissible \((X,H)\), if the relation itself implies
(1), its rational charge projection must be finite, by Northcott's
elementary rational-height finiteness theorem. Finiteness of the
projection of rational points is much weaker than algebraic finiteness.

The following conditional classification is useful in choosing
a new cap fiber. On a fixed algebraic curve component of a fiber,
if \(s\) is a nonconstant rational function and the component has
infinitely many rational points, its charge projection is infinite.
Deleting finitely many guard zeros and poles does not change this.
Therefore:

* a rational genus-zero component carrying a smooth rational point
  cannot bound a nonconstant charge;
* a smooth genus-one component with a rational point and positive
  Mordell-Weil rank cannot bound a nonconstant charge;
* a rationally parametrized positive-dimensional component cannot
  bound a charge that varies along its rational parametrization.

For a rationally pointed Weierstrass family of genus one with
rank-zero rational fibers, every rational point is torsion.
If the Weierstrass coefficients, chosen origin and rational function
giving the charge are fixed-degree rational functions of \((X,H)\),
Mazur's rational torsion theorem bounds the orders uniformly
(the order is at most 12). A nonidentity point of order dividing
one of these integers satisfies one of finitely many fixed division
polynomials in the abscissa. Applying the rational-root height
argument and then the Weierstrass equation bounds the heights of
its affine coordinates linearly in \(h_{\rm W}(X)+qh^2+1\).
A fixed-degree rational charge map on these points gives (5),
with the usual nonzero denominator guards. The identity and
any other separately parametrized regular chart give the same
bound. So such a pointed rank-zero family cannot give a complete
standalone cap either, outside the coefficient-degeneration loci.

This last argument does not cover general genus-one torsors with
no specified bounded-height rational origin. Higher-genus curves
can have finitely many rational points without a useful height
bound in terms of their coefficients. Likewise a higher-dimensional
fiber can have an arithmetically finite charge projection. These
are precisely the possibilities not eliminated by the above
argument.

A relation which depends on \(U\) as well as \((X,H,s)\) also
does not satisfy the standalone hypothesis. The old conic itself
depends on \(U\), so finiteness of the charge projection of a
standalone constraint is **not necessary** if the bound is proved
only after intersecting that constraint with the conic and the
other source equations. We do not infer such a finiteness claim
for an arbitrary coupled cap.

Reference for the torsion bound: B. Mazur, *Modular curves and the
Eisenstein ideal*, Publ. Math. IHES 47 (1977), 33--186.
Only the usual torsion consequence over \(\mathbb Q\) is used.

## 3. Exact Lucas failure on rational targets and on local quotient tests

The [degree-four Lucas amplifier v143](../../../undecidability/packed_lucas_v143/README.md)
of the undecidability construction uses the **integer** identity
\[
  \Delta=t^2-(a+1)tv+v^2-1=0,\qquad
  v=(a-1)b,\qquad b=2m+1.
  \tag{6}
\]
With integer labels, large \(a\), and odd \(b\), the descent proves
exponential growth of the other labels in \(a\).
It would be tempting to apply (6) to rational height witnesses
or to quotient ratios in the six-coordinate source.

There is a simple exact obstruction. For any integer \(a>2\),
\[
 t=1,\qquad v=a+1,\qquad
 b=\frac{a+1}{a-1},\qquad m=\frac1{a-1}
 \tag{7}
\]
satisfies (6), with \(b,m,t\) all nonzero.
For even \(a\), \(b\) is a two-adic odd unit. Every height
of the displayed rational labels is \(O(\log a)\). If desired,
take \(a\) a multiple of \(6\cdot7\cdot29\cdot149^L\) for any
fixed \(L\). All the rational targets in (7) then have denominators
prime to \(2,7,29,149\); the large fixed-prime divisibility condition
on \(a\) holds exactly. The rational identity and two-adic oddness
are not enough for Lucas descent; integrality of the labels is
essential.

The
[adaptive joint quotient transfer](../../../papers/elliptic_divisibility/adaptive_joint_quotient_20261124/README.md)
proves a stronger obstruction for using (6) as a fixed
finite-precision index-residual test. In that construction include
\(\Psi=t^2-(a+1)t(a-1)(2m+1)+(a-1)^2(2m+1)^2-1\)
as a polynomial in three hidden quotient labels. Use the tuple (7)
as rational targets, and the separate external input \(X=1/5\),
with its own hidden quotient. Choose \(a\) as above. Prescribe
deep reference preparation also at 149, using the same CRT
congruence on the hidden label \(a\) at this fixed prime.
The simultaneous CRT theorem produces actual integer quotient
labels in unbounded progressions, with positive choices available,
the desired fixed-prime congruences, the old input congruences,
and a fully prepared single pole. In particular it produces
actual noninteger input \(1/5\). The optional numerator-charge
conic still has its rational parametrization.

Here (6) is tested through the finite-precision local residual,
not imposed as an exact equation on rationally visible integer
labels. The actual integer residual need not vanish. This is why
the exact integer Lucas growth proof in v143 cannot be imported
to infer a height cap in the new setting. It is not a flaw in v143:
that construction proves the integer residual vanishes by an
independent aggregate height argument before applying descent.
The full undecidability construction remains unchanged.

## 4. Status

These results isolate the remaining issue. A finite algebraic
bound in the input/reference alone has the wrong asymptotic
scale for foreign-prime charges. Rationally parametrized
standalone cap fibers leave the charge unbounded. The recent
Lucas and Pell mechanisms need an independent integer
comparison-height argument, and finite local polynomial tests
do not furnish it. The necessary new global bound (1) with
two or fewer ordinary variables has not been established.
No lower bound on all possible coupled definitions, or
nonexistence assertion for the nine-variable target, is made.
