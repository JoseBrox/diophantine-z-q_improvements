# Three-pole chain: four-coordinate sound predicate and exact realization obstructions

## Scope

This extends the mixed-class two-pole equations of [README.md](README.md)
to three physical inputs. The result is a four-ordinary-parameter
predicate with the required negative-odd-valuation exclusion, and
an exact criterion for realizing it by four congruent-number curves
at related levels. It saves a parameter algebraically relative to
three mixed plus two independent pole parameters. Completeness for
the actual three-scale detector inputs is **not** proved. In
particular it does not establish a 23-variable ordinarily specified
definition of the integers.

## 1. Four ordinary parameters

For nonzero rational \(d_1,d_2,d_3\), set
\[
 F_1=1-d_1,\qquad F_2=1+d_2,\qquad F_3=1-d_3,\qquad
 D=\frac{d_1d_2}{1+d_2r^2},\quad
 D_1=DF_1,\quad D_2=DF_2,\quad D_3=DF_2F_3.
\]
Retain \(r,a,b,c\ne0\) and guard the three complements and the
denominator of D. Adjoin the five finite roots
\[
\begin{aligned}
 s^2&=d_1(2+d_2r^2),&
 z^2&=(2+d_2b^2)/d_3,\\
 Y_i^2&=x_i(x_i-D_i)(x_i+D_i)\quad(i=1,2,3),
\end{aligned}
\]
where
\[
 x_1=D_1(d_1a^2-1),\qquad
 x_2=D_2(1+d_2b^2),\qquad
 x_3=D_3(d_3c^2-1).
\]
Guard \(s,z\ne0\). No nonzero ordinate guard is needed for soundness.
The common curve \(E_D:y^2=x(x-D)(x+D)\) has the point
\((x_0,y_0)=(d_1d_2,Dd_2rs)\), since
\(x_0-D=Dd_2r^2,\ x_0+D=D(2+d_2r^2)\).
The adjacent pair for each input has these nonzero shifted classes:
\[
\begin{array}{c|cc}
 &\text{first level, shifted class}&\text{second level, shifted class}\\
 d_1&D,\ [x_0+D]=[Dd_1]&D_1,\ [x_1+D_1]=[D_1d_1]\\
 d_2&D,\ [x_0-D]=[Dd_2]&D_2,\ [x_2-D_2]=[D_2d_2]\\
 d_3&D_2,\ [x_2+D_2]=[D_2d_3]&D_3,\ [x_3+D_3]=[D_3d_3]
\end{array}
\]
where brackets are nonzero rational squareclasses. For the middle
plus shift use \(x_2+D_2=D_2d_3z^2\).

At any odd prime p, a rational point on \(E_C\) with even \(v_p(C)\)
has even valuation on each nonzero factor \(x,x-C,x+C\). Scale
\(C\) locally to a unit; either all three factors have the same
negative valuation or at most one vanishes modulo p. The curve
equation proves the assertion, including nonzero factors at
2-torsion. If \(v_p(d_i)<0\) is odd, the ratio of the two adjacent
levels, \(F_i\), has odd valuation. One level has even valuation
but its indicated shifted class has odd valuation, a contradiction.
Thus the four-parameter predicate excludes every negative odd
valuation of every input outside 2, on arbitrary rational tuples
satisfying its guards. Clearing denominators and adjoining the five
finite roots fits the existing selected-character encoder.

## 2. Precise sufficient global theorem

For positive prepared \(d_i<1\) with square reduced denominator
and squareclass \(1\bmod8\), write \(j_i=[d_i]\) and
\(k_i=[F_i]\) as positive squarefree integers.
Suppose a positive level N has non-torsion rational points on
\[
 E_N,\quad E_{NF_1},\quad E_{NF_2},\quad E_{NF_2F_3}
\]
with the two prescribed shifted classes at each of the internal
vertices (d1,d2 at the first, d2,d3 at the second), and the prescribed
single shifted class at each endpoint, as in the preceding table.
Then the four-parameter predicate has rational solutions. Indeed the
first point has first class \([d_1d_2]\) by the curve equation and
positive abscissa, necessarily greater than N; a common rational
square scaling makes its abscissa \(d_1d_2\). Its two shifts give
r and s. Rescale the other three points by the same factor; the
middle shifts give b and z, and the two endpoint shifts give a
and c. Their ordinates give the three remaining finite roots.
All stated guards hold. Conversely the predicate provides such
points if the ordinates are nonzero; for soundness no non-torsion
condition is necessary. The squarefree levels may equally be
written \(N,Nk_1,Nk_2,Nk_2k_3\) using the corresponding square
rescalings. The earlier mixed-class simultaneous theorem supplies
only the first three curves with **one** specified shift on the
third curve, so does not prove this new sufficient theorem.

## 3. A new local obstruction at the middle complement

The natural attempt is to choose squarefree N disjoint from the
complement supports (as in the two-pole theorem), including the
input squareclass support in N. For any odd prime \(p\mid k_2\)
with \(p\nmid Nj_2j_3\) the middle level \(C=NF_2\) has odd
valuation. Both shifts of its point have odd valuation because
their classes are \(Cd_2,Cd_3\).
If one shifted factor had valuation less than \(v_p(C)\),
both shifts and x would have that same odd valuation, contrary
to the curve equation. Hence both shift valuations are at least
\(v_p(C)\); x has even valuation, again by the curve equation.
In particular \(v_p(x)>v_p(C)\) (the case x=0 is included).
It follows that \(x/C\equiv0\bmod p\), so the two unit classes
of the shifted quotients are respectively -1 and 1. Consequently
\[
 (j_2/p)=(-1/p),\qquad (j_3/p)=1. \tag{*}
\]
The first condition follows from prepared \(F_2=1+d_2\)
and is precisely the condition in the old theorem. The second
does not follow from preparation or mutual quadratic residues
between the distinct input-class supports. It concerns the
variable prime support of the *complement* of the second input.
Allowing N to meet that support changes the local condition;
the argument does not exclude such a different construction.

### Explicit fixture

Take \(J=33,A=97,B=313,C_0=1153\), all pairwise coprime positive
squarefree integers of residue 1 modulo 8. Each of A,B,C0 is
prime, and the three groups have mutual quadratic residue symbols
+1, also with both primes 3 and 11 of J. Put
\[
 j_1=3201,\quad j_2=10329,\quad j_3=38049,\qquad
 d_1=\frac{16j_1}{1009^2},\
 d_2=\frac{16j_2}{409^2},\
 d_3=\frac{16j_3}{1013^2}.
\]
All three inputs are positive less than 1, have square reduced
denominator, class 1 at two, and two-adic valuation four.
Moreover
\[
 F_2=\frac{332545}{167281}=\frac{5\cdot66509}{409^2},\qquad
 (j_2/66509)=1,\quad (j_3/66509)=-1,
\]
with 66509 prime of residue 1 modulo 4. The numerator of F2 is
coprime to JABC0. This violates (*). Thus the usual disjoint
squarefree-level realization of this chain fails even on mutually
compatible input squareclasses. The example is not claimed to be
an actual tuple of the elliptic detectors.

The obstruction survives arbitrary small positive real inputs.
For instance replace the denominator 409 of d2 by arbitrarily
large positive odd integers congruent to 409 modulo
\(2\cdot66509^2 JABC_0\). The reduced denominator is still square,
the two-adic valuation remains four, the support of the numerator
of F2 remains disjoint from JABC0, and its valuation at 66509
remains one. Independently increase the odd denominators of
d1,d3 in progressions prime to their numerator classes. This
preserves the offending residue symbol.

## 4. Why simply demanding more mutual squares is also insufficient

There is a separate obstruction to the *minimal normalized Selmer
dimension* strategy of the preceding rank-one theorem. Suppose
\(j_1=JA,j_2=JB,j_3=JC_0\), with all four supports disjoint and
the three exclusive products nontrivial. Let N be squarefree of
type 5, contain their supports and be disjoint from k2.
All symbols now refer to the normalized Monsky--Redei system
of README.md. The prescribed base point requires normalized
first/second labels
\[
 u=AB,\qquad v=N/(JB)
\]
as divisor classes. The middle point requires at level Nk2
\[
 u'=BC_0,\qquad v'=Nk_2/(JB).
\]
Here the labels are exponent vectors, and u' has zero entries,
v' has one entries, at every added prime of k2. Restrict u',v'
to the support of N. On row p of the normalized system, deleting
the new vertices changes the first equation by
\([k_2/p]u'_p\) and the second by \([k_2/p](v'_p+1)\),
where square brackets on symbols mean additive Legendre bits.
The diagonal convention is the row-sum-zero convention; the
diagonal matrices of the residue signs are unchanged at old
vertices. Thus if
\[
 (k_2/p)=1\quad\text{at every prime dividing }JBC_0,
\]
the restricted middle class lies in the base normalized Selmer
kernel. It is independent of the base class since their first
labels AB and BC0 are distinct and nontrivial. In particular
the base kernel has dimension at least two. This contradicts
the dimension-one condition required by the preceding
minimal-Selmer rank-realization proof.

Therefore merely adding full mutual-square conditions between
k2 and the third input is not a solution: with that strengthening
the old nullity-one strategy breaks down. This does not prove
nonexistence of rational points on all four curves; a larger
Selmer dimension and different arithmetic realization may work.
The remaining target for a chain proof includes (*) at the
complement primes and suitable **nonconstant** interaction
symbols on the exclusive third support. If k2 is a square
at every prime of JB, as preparation requires, then the
minimal-kernel strategy needs a nonsquare k2 at at least one
prime of C0. By reciprocity and (*) their number is even when
C0 consists of type-one primes. In particular at least two such
interactions are needed. The earlier fixed marker menus do not
supply this property.

No defining-variable record is changed by this note. It isolates
the exact additional arithmetic realization problem for the
23-variable ordinary numerical target, separately from the
fixed 22-variable BB specialization which needs no third scale.
