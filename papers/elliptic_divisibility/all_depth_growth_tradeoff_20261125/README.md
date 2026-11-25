# All-depth growth tradeoff and a recursively anchored deficit charge

## Status and scope

This is a partial replacement of the bounded-odd-mass (OM) amplifier
in [the 18/20-coordinate continuation](../mixed_pole_odd_mass_20261125/README.md).
It proves the requisite power-scale growth inequality from **full**
elliptic denominator mass, without any simple-prime or odd-depth
hypothesis, provided a specified one-sided deficit charge exists.
The height anchor for that charge is constructed using the already
retained full-domain modular five-contact height estimate. The
arithmetic realization of the charge itself is not established.
In particular 17/19 below are conditional target counts, not new
defining-variable records.

We use the original quadratic carrier \(K=\mathbb Q(\sqrt2)\),
\(E:y^2=x^3-(3-\sqrt2)^2x\), \(P=2R_0\), and its rank-one
square-abscissa chart. The original v78/v88 modular, group,
formal-logarithm and prime-pattern inputs and the mixed-class pole
theorem are retained. The elementary height arguments use the
usual canonical height and Siegel's theorem in height form.
For the full-denominator asymptotic see also Streng, *Divisibility
sequences for elliptic curves with complex multiplication*,
Algebra & Number Theory 2 (2008), Lemma 4.3,
https://msp.org/ant/2008/2-2/ant-v2-n2-p04-p.pdf.
No abc or (OM) is used in the tradeoff or anchor.

## 1. A full-depth index-growth inequality

Write \(q=\widehat h(P)>0\). For nonzero integer indices \(c,j\)
put \(Q=[c]P,\ T=[j]P\). In the defining source Q will be
\(S-P=[a-1]P\); signed indices are harmless. For each good
unramified rational prime p outside a fixed finite set S, and
each place \(\mathfrak p\mid p\), put
\[
 a_{\mathfrak p}=\max(0,-v_{\mathfrak p}(x(Q))/2),\qquad
 b_{\mathfrak p}=\max(0,-v_{\mathfrak p}(x(T))/2).
\]
Use the normalization \(v_{\mathfrak p}(p)=1\), and set
\[
 a_p=\max_{\mathfrak p\mid p}a_{\mathfrak p},\qquad
 \delta_p=\max_{\mathfrak p\mid p}\max(0,2a_{\mathfrak p}-b_{\mathfrak p}),
 \quad D(c,j)=\sum_{p\notin S}\delta_p\log p.
\]
This *deficit* includes even as well as odd depths and vanishes
if T is sufficiently deep at every formal place of Q.

**Theorem.** Uniformly in the two nonzero indices,
\[
 \boxed{\log|j|+D(c,j)\ \ge\ q c^2-o(c^2)}
 \qquad (|c|\longrightarrow\infty).
\]
The little-oh depends only on the fixed carrier, point and S, not j.

Proof. At a prime with \(a_p>0\), choose a place with maximal
depth a. If \(b=b_{\mathfrak p}>0\), the isometric formal logarithm
and \([c]T=[j]Q\) give
\[
 b-a=v_p(j)-v_p(c).
\]
Since \(v_p(c)\ge0\), \(a\le v_p(j)+\max(0,2a-b)\).
If \(b=0\) then \(\delta_p\ge2a\), so the same inequality holds
without any use of the logarithm for a nonformal point.
Thus \(\sum a_p\log p\le\log|j|+D(c,j)\).

The height of x(Q) is \(2qc^2+O(1)\). By the full-denominator
asymptotic over the fixed number field, its finite-place
denominator contribution, divided by two, is
\(qc^2-o(c^2)\), in absolute-height normalization. Removing
a fixed finite set costs \(O(1+\log|c|)\) by entry into a fixed
formal subgroup followed by the local multiplication formula
(including deep formal entry at ramified/bad primes).
At an unramified rational prime the absolute-height weighted
average of the depths over its slots is at most their maximum.
Hence \(\sum_{p\notin S}a_p\log p\ge qc^2-o(c^2)\).
This proves the theorem.

In particular no assertion about the parity, primitive status,
or boundedness of any denominator depth is needed.
For each fixed Q, there are T with D(c,j)=0 and arbitrarily
large |j|: choose the index j in a sufficiently divisible
progression to put T as deep as required at all finitely many
places occurring in D, and use real recurrence if a fixed
real arc is also prescribed. This is an ordinary local
multiplication construction, not a proposed polynomial
certificate of D=0.

## 2. Precisely what a replacement charge must do

An appropriate one-ordinary-coordinate auxiliary predicate
would use Q,T and a rational scalar s, with finite algebraic
root choices and guarded equations, and prove
\[
                    D(c,j)\le C_D(1+h_{\mathbb Q}(s)).
                    \tag{C}
\]
For completeness it should allow s=0 on sufficiently deep
T for each fixed admissible scalar Q, retaining the usual
finite-place and real open conditions. One may instead use
a different fixed rational canonical charge. The use of
s=0 does not count an infinite valuation as a charge:
h(0)=0 and (C) is an inequality of ordinary finite heights.
A stronger sufficient condition is
\(\delta_p\le C_D\max(0,-v_p(s))\) at all retained primes
with the zero convention giving zero on the right. But the
global (C) itself is enough, and need not be proved this way.

The important difference from the numerator-quotient cap
problem is the required **one-sided** deficit. Denominator
mass of T at foreign primes, and T's large height, must not
be charged. The charge should be small when T is very deep
at Q's finitely many formal primes, regardless of what
happens at all other primes.

This distinction is mathematically necessary. For example,
take coherent square abscissas \(g_Q^2=x(Q),g_T^2=x(T)\)
in K and put \(F=g_Q^2/g_T\). Its denominator records each
deficit at a maximal-depth place, hence \(D(c,j)\le2h_K(F)\)
(the factor two converts the maximum over two slots to an
absolute-height sum). But
\[
 h_K(F)\ge qj^2-2qc^2-O(1).
\]
Here \(h_K(g_Q)=qc^2+O(1)\) and similarly for T.
Thus bounding the full ratio height by \(O(c^\epsilon)\)
would give j=O(c), incompatible with the growth theorem when
the deficit is small. This applies also to a sum-of-squares
conic \(r^2+s^2=F^2\) if both coordinates are required to have
such small total height: the ordinary sum-of-squares height
inequality bounds h(F) by \(h(r)+h(s)+O(1)\).
A charge which captures all depths **and** the whole height
of this ratio is not a solution of the growth problem.
The corresponding conic is useful in the opposite,
upper-quotient-cap direction.

## 3. A recursive scalar anchor for an additional charge

The height-control part of (C) can be handled without adding
a point or a pole, by adapting the project's v136 recursion
([recursive scalar theorem](../../../undecidability/recursive_scalar_v136/README.md)).

Use the fixed input substitution and positive v88 scalar of
the mixed-class theorem:
\[
 X=\prod_{r=0}^{465}(X_0-r),\quad
 \beta=1632X^2+2477,\quad\tau=X^2+1,\quad
 \rho_0=(7/9)^2\rho_*(X;L),
 \qquad L\equiv3\bmod171033184.
\]
As in that theorem \(\rho_0\) has positive odd valuation L at
67 on every rational input. Its positive odd contacts away
from a fixed set contain the four finite odd contacts of
beta; the denominator contact of beta is even away from
fixed coefficient primes. Its height satisfies
\(h(\rho_0)\le4h(\beta)+2L\log67+133\).
Introduce no new ordinary coordinate beyond the proposed s
and set
\[
 f(Y)=Y(Y-1)(Y-2401)(32Y+343),\quad C_0=2504,\quad
 F_0=f(C_0)=51948354689656,
\]
\[
 W=\rho_0 s^2,\qquad Y=C_0+\frac{W}{(1+W)^2},\qquad
 \rho=\rho_0\, f(Y)/F_0.
\]
Every denominator is nonzero on rational tuples because
\(\rho_0>0,W\ge0\); the four contact factors are positive.
Also \(1\le f(Y)/F_0<2\) on \(C_0\le Y\le C_0+1/4\).
At the canonical s=0, rho is exactly rho0, not merely
in its squareclass. Thus the entire earlier mixed-class
marker and scalar preparation applies literally.

Enlarge the fixed exceptional set by primes dividing F0,
and omit 67 in the contact radicals while retaining its
separate forced role. In particular \(67\nmid F_0\).
If \(v_p(\rho_0)\) is odd then \(v_p(W)\) is odd and nonzero
for s nonzero. The identity
\(v_p(W/(1+W)^2)=|v_p(W)|\) for nonzero valuation gives
\(Y\equiv C_0\bmod p\). The same holds at s=0.
Therefore the update preserves every old odd valuation
exactly. If a prime occurs to odd positive order at a
finite contact of Y, the old valuation is necessarily even,
so the update makes it odd. The reduced denominator of
\(Y=C_0+W/(1+W)^2\) is a square, by coprimality of the
reduced numerator and denominator of W. Thus its infinity
contact has no odd valuation. In particular the update
protects the forced valuation at 67 on every rational tuple.

Use this rho in the existing two or three comparison scales,
with the bounded-at-seven rechart
\[
 \psi(v)=v/(1+7v^2),\qquad \alpha(v)=1+\rho\psi(v)^2
\]
of the 18/20 theorem. The old scalar-unit argument holds
for arbitrary odd valuations of rho, and the same shifted
contact lists have disjoint first two residues modulo 67.
Increase the fixed orders of the last two scalar tests to k,
with k>=3. The original scalar extraction implies, writing
\(C=|a-1|=|c|\),
\[
 67^{(k-1)L+1} M_\beta^k\mid C,\qquad
 67^{(k-1)L+1} M_Y^k\mid C .
\]
Indeed at each odd scalar prime one contact weight is a unit
and the trace/pole obstruction forces the odd scalar
valuation to be positive and the same strict ratio-depth
bound \(v_p(C)>(k-3/4)v_p(\rho)\) as in the odd-mass
construction. A negative odd valuation of rho, if introduced
by the update, simply excludes the solution. The proof
does not assume square denominators on arbitrary tuples.

Using the retained full-domain modular height input for
both beta and Y gives
\[
 h(\beta)+h(Y)\le K_1 C^{3/k}
\]
with fixed K1 (the smaller 7/(3k) exponent is also available
where the stronger old estimate is used). All constants
here are independent of L, inputs and point indices.
For reduced \(W=u/v\ge0\), the reduced denominator of
\(W/(1+W)^2\) is \((u+v)^2\), including W=0.
Hence \(h(W/(1+W)^2)=2\log(u+v)\ge2h(W)\).
Translation by C0 gives
\[
 2h(s)\le h(W)+h(\rho_0)
       \le \tfrac12 h(Y)+h(\rho_0)+O(1)
 \qquad(s\ne0),
\]
and h(s)=0 when s=0. The forced prime bounds
\(2L\log67\le2\log C/(k-1)\). Therefore
\[
 \boxed{h(\beta)+h(s)+h(\rho)
             \le K_2(C^{3/k}+\log C+1).}                 \tag{A}
\]
For the last term use \(h(f(Y))\le4h(Y)+O(1)\).
This is a proved fixed-degree height anchor for the charge,
not a desired additional conjecture.

## 4. Conditional transfer, count and order of choices

Assume the missing charge predicate (C) has the stated
canonical completeness and uses only s and finitely many
monic finite-root choices. Keep the five point roles
A,S,T,H,U of the Lucas-free 18/20 route, but delete its
entire independent (OM) amplifier and two BB parameters.
Use the recursive scalar of Section 3, the six input
comparison tests, the six scalar tests with precision k,
and the two mixed-class comparison poles, plus the third
ordinary BB pole in the specified route.

All old local comparison implications hold, in particular
\(M_i\mid NC\) for \(N=\operatorname{num}(\tau-n)\ne0\).
The mixed scalar alternative uses the same p-divisibility
of C; the original scalar input map beta is still the one
whose contact primes the update preserves. The root
aggregate is \(x(A)+x(S)+x(T)\).
The original trace-height or effective abscissa-sum bound
and the new scale height inequality therefore give, as in
the Lucas-free 18/20 proof,
\[
 \log B=O(C^{3/k}+\log C+1)\quad(N\ne0),
 \qquad B=\max(1,|n|,|a|,|j|).
\]
This uses (A) in the scalar-height absorption.
On the other hand Sections 1--3 and (C) give
\[
 \log B\ge\log|j|\ge qC^2-o(C^2)
                    -C_D(1+h(s))\ge qC^2/2
\]
for sufficiently large C. The strict power gap already
holds for k=3. Increase the fixed L in its progression to
exclude N nonzero. Thus \(\tau=n\in\mathbb Z\), implying
integrality of X and then X0.

For the integer-witness direction, set s=0 **before** the
scalar/reference preparation. The update is identically one,
so no new marker or dyadic compatibility is needed.
Choose Q by the old scalar preparation, and then T
sufficiently deep at its formal places, using the proposed
charge completeness. The scales now use the already proved
seven-integral rechart, so there is no conflict if T is deep
at seven. Fix all roots and scales before selecting comparison
primes. The old comparison preparation and mixed-class
realization apply, while any actual charge witnesses are
fixed before that selection. Thus the extra charge does not
silently change the order of choices.

The proposed total ordinary counts would be
\[
 1+10+1+3+1+1=17,\qquad 1+10+1+5+1+1=19.
\]
The summands are input, five point charts, slope, comparison
poles, charge and final finite encoder. A charge with an
additional ordinary parameter costs one more; an independent
two-parameter BB pole costs two more. The target need not
use the old bounded odd-mass hypothesis at all. The
two-scale threshold remains ineffective; the three-scale
one would also need effective data for the charge inequality
and the full-denominator asymptotic to give an ordinary
numerical fixed exponent. We do not transfer the old
numerical exponent without those data.

**Unresolved step:** a charge satisfying (C), with the stated
coordinate budget and sufficiently-small-height canonical
witnesses, has not been proved. The theorem in Section 1
alone does not force j to grow exponentially, and the
all-depth radius conic of Section 2 cannot serve as this
charge. The anchor and the conditional transfer are genuine
consequences of the retained modular premise; (C) is not.

## 5. Verification

The companion verifier checks the fixed recursion constants,
normalization and height identities on exact rational fixtures,
the local full-depth deficit inequality including nonformal
branches, and the strict exponent comparisons. These finite
checks do not prove the retained arithmetic inputs, the
full-denominator asymptotic, or the missing charge realization.
