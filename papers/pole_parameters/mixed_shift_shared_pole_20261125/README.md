# A mixed-shift three-parameter predicate for two pole inputs

**Status.** Exact soundness at all odd primes, a necessary and sufficient
criterion for the common-point conic, and an explicit nontrivial globally
realized pair with different input squareclasses and nonsquare complements.
Completeness on the actual detector fibers is open. No defining-polynomial
count is changed by this note.

This is an alternative to sharing the first-abscissa class in the
[finite-support simultaneous twists](../../arithmetic_dependencies/finite_support_twists_20261123_v88.tex)
and [normalized BB product poles](../../few_variables25/bb_product_degree_transfer_20261123_v88.tex).
It exploits different Kummer coordinates of one point. No strengthening
of the published BB rank-one realization theorem is assumed.

## 1. Predicate

Let \(e_1,e_2\in\mathbb Q\setminus\{0,1\}\). Take ordinary rational
coordinates \(r,a,b\), all nonzero. Use the abbreviations
\[
 t=1+2e_2r^2,\qquad D=e_1/t,\qquad D_i=D(1-e_i).
\]
Guard \(t\ne0\). Require the following three rational square roots:
\[
 \begin{split}
 s^2&=e_1e_2(1+e_2r^2),\\
 Y_1^2&=x_1(x_1-D_1)(x_1+D_1),\qquad x_1=e_1a^2,\\
 Y_2^2&=x_2(x_2-D_2)(x_2+D_2),\qquad
 x_2=D_2(1+2e_2b^2).
 \end{split}
\]
All three root variables are finite over the three ordinary coordinates.
For clarity one may guard \(sY_1Y_2\ne0\); soundness does not need
this guard. The rational functions and guards can be cleared in the
existing finite-algebra encoder. Three finite quadratic extensions have
total rank at most eight, rather than four for two product poles.

The first equation produces a common point
\[
 (x_0,y_0)=\left(e_1,\frac{2e_1rs}{t}\right)\in E_D(\mathbb Q),
 \qquad E_C:y^2=x(x-C)(x+C).
\]
Indeed \(x_0-D=2De_2r^2\) and \(x_0+D=2D(1+e_2r^2)\).
Thus the first input class appears in \(x_0\), and the second
input class appears in \((x_0-D)/(2D)\). The private curves use
exactly these respective classes at levels \(D_1,D_2\).
The factor 2 is essential to the conic formula.

## 2. Soundness

**Lemma.** If \(p\) is odd and \(v_p(C)\) is even, then at any rational
point of \(E_C\) every nonzero one of \(x,x-C,x+C\) has even valuation.

Proof: scale \(C\) by a square to make it a unit at \(p\), scaling the
abscissa and ordinate by its square and cube factors. If the new abscissa
is nonintegral, all three factors have its valuation, and three times
this valuation is even. If it is integral, at most one factor vanishes
modulo \(p\), since \(p\ne2\); the valuation of that nonzero factor is
even by the curve equation. At a 2-torsion point the other nonzero
factors are units. Scaling back changes the three valuations by an
even integer.

**Proposition.** The predicate excludes negative odd valuations of
either \(e_i\) at every odd prime.

If \(v_p(e_i)<0\) is odd, then \(v_p(1-e_i)=v_p(e_i)\).
Exactly one of \(v_p(D)\) and \(v_p(D_i)\) is even. For \(i=1\), the
two relevant abscissas are \(e_1\) and \(e_1a^2\); both have odd
valuation and are nonzero. For \(i=2\), the relevant shifted abscissas
are \(2De_2r^2\) and \(2D_2e_2b^2\); on the curve whose level has
even valuation, the shifted abscissa has odd valuation and is
nonzero. In both cases the lemma is contradicted. This proof works
for arbitrary rational witnesses, not only prepared ones, and does
not assume the other input is prepared.

There is no claim of exclusion at 2. The consumed-prime sets of the
intended general comparison routes already omit 2.

## 3. Exact common-point criterion

For positive prepared inputs write \(e_i=j_i k_i^2\), with \(j_i\)
positive squarefree integers, \(k_i\in\mathbb Q^\times\), and
\(j_i\equiv7\bmod8\). In the conic equation put
\(R=k_2r,\ S=s/(k_1k_2)\). Then
\[
 S^2-j_1(j_2R)^2=j_1j_2.
\]
If \(j_1>1\), this is equivalent to \(-j_2\) being a norm from
\(\mathbb Q(\sqrt{j_1})\), by dividing by the norm of \(\sqrt{j_1}\).
By the quadratic norm criterion (or Hasse--Minkowski), it is equivalent
to the following finite tests:
* for odd \(p\mid j_1,\ p\nmid j_2\), \((-j_2/p)=1\);
* for odd \(p\mid j_2,\ p\nmid j_1\), \((j_1/p)=1\);
* for \(p\mid\gcd(j_1,j_2)\), writing \(j_i=p u_i\),
  \((u_1u_2/p)=1\).

These follow from the odd-prime Hilbert-symbol formula; all other odd
places give symbol 1, the real place gives 1 by \(j_1>0\), and at 2
the second entry \(-j_2\equiv1\bmod8\) is a square. A soluble conic
has a rational parametrization, hence infinitely many rational
points with \(r,s\ne0\), avoiding any prescribed finite set of \(r\)'s.
This supplies the common point without a rank theorem.

The condition is not automatic for arbitrary prepared inputs:
\(e_1=112/101^2,\ e_2=368/101^2\) are positive, less than one, have
square reduced denominators, and their dyadic classes are 7 with
valuation 4. But \(j_1=7,j_2=23\) and
\((-23/7)=-1\). Thus this particular predicate cannot be promoted
to a universal two-input prepared-pole theorem.

## 4. Actual nontrivial realization and density

A rational triple with the required classes exists with
\[
 e_1=\frac{11200}{4695889},\qquad
 e_2=\frac{1984}{199809}.
\]
Here \(j_1=7,\ j_2=31\); the reduced denominators are \(2167^2\)
and \(447^2\), and the positive complement classes are
\(520521\) and \(7913\), both nonsquare. The dyadic valuations of
the inputs are 6 and 6, respectively (for the first, \(11200=2^6
\cdot175\); for the second, \(1984=2^6\cdot31\)).
Start with the following points on three congruent-number curves:
\[
\begin{array}{c|cc}
 \text{level}&x&y\\\hline
 41881&260743&131414472\\
 609&5887/9&164836/27\\
 8897&2553439/225&2533011488/3375
\end{array}
\]
The base level \(41881=7\cdot31\cdot193\) has the two desired
classes, and the squarefree parts of \(41881(1-e_i)\) are 609 and
8897. Square rescaling gives the explicit parameters
\[
 D=\frac{347200}{906306577},\quad
 r=\frac{4023}{248},\quad a=\frac{899}{2167},\quad b=\frac{149}{40},
 \quad s=\frac{8960}{968649}.
\]
The private ordinates are
\[
 Y_1=\frac{314280273664000}{103550802255048880369},\qquad
 Y_2=\frac{162112735232000}{24539350711564713123}.
\]
All equations are directly verified in rational arithmetic by
[verify.py](verify.py).

More generally suppose there is some positive rational level \(N\)
with non-torsion points \(P_0\in E_N,\ P_i\in E_{N(1-e_i)}\)
in the prescribed classes:
\[
 x(P_0)\in e_1\mathbb Q^{\times2},\quad
 x(P_0)-N\in 2Ne_2\mathbb Q^{\times2},\quad
 x(P_1)\in e_1\mathbb Q^{\times2},\quad
 x(P_2)-N(1-e_2)\in2N(1-e_2)e_2\mathbb Q^{\times2}.
\]
Then square rescaling makes \(x(P_0)=e_1\) and yields a predicate
solution. Conversely any guarded solution yields such points at
\(N=D\) when the inputs are prepared and the three ordinates
are nonzero. Here rational torsion on a positive congruent-number
curve consists of its full 2-torsion, so the guarded points
are non-torsion.

Independent odd multiples preserve each Kummer class. Non-torsion
makes their abscissas range over infinite sets. Varying \(P_0\) and
rescaling as above makes \(r^2\) vary over infinitely many values;
for each such value, independent odd multiples of \(P_1,P_2\)
make \(a^2,b^2\) each vary over infinite sets. Thus the admissible
triples are Zariski dense in the ordinary parameter space
\(\mathbb A^3\). In particular finite nonzero polynomial exclusions
in these parameters can be met. The density argument does not
assume rank one.

## 5. Precise remaining task and accounting

A common level realizing the two different Kummer coordinates on
the base curve *and* their prescribed coordinates on the two
complement twists would save one ordinary coordinate in the
25-variable general construction, and likewise in the 27-variable
explicit construction by retaining its third private BB pole.
The conditional target counts are 24 and 26. The ordinary/weak-abc
11-variable single-pole routes are not reduced by this two-pole
predicate.

The norm criterion solves only the first common-point problem.
The two other rational points must exist at the **same** selected
level, up to the prescribed complement twists. Independent
applications of the BB theorem do not imply this. In addition,
the actual detector input classes must meet the norm criterion;
the example above and the local soundness proof do not establish
that property for every integer input of the current constructions.
Whole-character guards must still be checked after the substitution,
and the full degree and coefficient ledgers have not been rebuilt.
No variable-count improvement is asserted without this completeness
step.

The actual example is stronger than two individually prepared
scalars: the input classes differ and both complement twists are
nontrivial. It rules out treating equality of the two first
abscissa classes as a necessary condition for all three-parameter
sharing schemes.
