# Projective symmetries and reciprocal reflected contacts

Let

\[
 S=\{\infty,0,1,2401,-343/32\}\subset\mathbf P^1(\mathbf Q).
\]

The following two statements are exact algebraic facts. Neither is a lower
bound on the number of variables in an arbitrary Diophantine definition.

## 1. The projective automorphism group is trivial

**Proposition.** The stabilizer of \(S\) in \(\mathrm{PGL}_2(\mathbf Q)\)
contains only the identity. The same holds in
\(\mathrm{PGL}_2(\overline{\mathbf Q})\).

**Proof.** For an unordered four-point subset, let

\[
 J(\lambda)=\frac{(\lambda^2-\lambda+1)^3}
                   {\lambda^2(1-\lambda)^2},
\]

where \(\lambda\) is any cross ratio of its four points. The six cross
ratios obtained by reordering have the same \(J\), so this is a projective
invariant of the unordered subset. The complements of the five points have
the following invariants; the last column is the exact integer part, not
a floating-point approximation.

| Omitted point | One cross ratio | \(\lfloor J\rfloor\) |
|---|---:|---:|
| \(\infty\) | \(35/32\) | 127 |
| \(0\) | \(-5/1024\) | 42150 |
| \(1\) | \(-1/224\) | 50403 |
| \(2401\) | \(-343/32\) | 128 |
| \(-343/32\) | \(2401\) | 5762403 |

These five invariants are different. Every projective automorphism of
\(S\) must therefore fix every point. A projective automorphism fixing
three points is the identity. This argument is valid over the algebraic
closure as well. Independently, the checker enumerates the 60 ordered
images of \((\infty,0,1)\), constructs the unique rational projective map
for each, and verifies that only the identity preserves the whole set.
\(\square\)

## 2. No rational normalization gives reciprocal squared distances

**Proposition.** There are no rational projective transformation \(f\)
and \(k\in\mathbf Q^\times\) such that all five values \(f(s)\),
\(s\in S\), are finite and nonzero, their squares are distinct, and

\[
 \{f(s)^2:s\in S\}
   =\{k/f(s)^2:s\in S\}.
\]

In particular, a different rational projective normalization and a
different reflection center cannot make the present ten reflected
contacts admit the reciprocal squared-distance simplification used for
the eight-contact abc construction.

**Proof.** All squared values are positive, hence \(k>0\). The involution
\(r\mapsto k/r\) has exactly one positive fixed point. Its action on a
set of five distinct positive rational numbers must consequently have
one fixed point and two transposed pairs. If the fixed squared value is
\(f(s_0)^2\), replace \(f\) by \(f/f(s_0)\). Then the fixed value is one,
the reciprocal constant is one, and the products of the two values in
each transposed pair are independently either \(+1\) or \(-1\).

Move \(s_0\) to infinity with the rational coordinate

\[
 w(s)=s\quad(s_0=\infty),\qquad
 w(s)=\frac1{s-s_0}\quad(s_0\ne\infty),
\]

with \(w(\infty)=0\) in the second case. A nonconstant rational
projective transformation taking infinity to one has the form

\[
 f(w)=\frac{w+A}{w+C},\qquad A,C\in\mathbf Q,\quad A\ne C.
\]

Write \(V=A+C\) and \(D=A-C\). For two finite coordinates \(x,y\),
the necessary equation \(f(x)f(y)=1\) reduces to

\[
 V=-(x+y),
\]

and \(f(x)f(y)=-1\) reduces to

\[
 D^2=-V^2-2V(x+y)-4xy.                 \tag{1}
\]

Let the two pairs be \((x,y)\), \((z,w)\), and put
\(p=x+y\), \(q=z+w\), \(r=xy\), \(s=zw\). There are four cases:

- For signs \((+,+)\), necessarily \(p=q\).
- For \((+,-)\), necessarily \(V=-p\), and (1) for the second pair
  must be a nonzero rational square.
- For \((-,+)\), necessarily \(V=-q\), and (1) for the first pair
  must be a nonzero rational square.
- For \((-,-)\), subtraction gives
  \(V=-2(r-s)/(p-q)\) when \(p\ne q\), after which (1) must be a
  nonzero rational square. When \(p=q\), the equations require
  \(r=s\), which would make the two unordered pairs equal and is
  impossible for four distinct points.

There are five choices of \(s_0\), three pairings of the other four
points, and four sign patterns: 60 cases in total. The exact rational
certificate records all of them. All 15 \((+,+)\) cases have unequal
pair sums; all 45 remaining cases have a negative or nonsquare value
of \(D^2\). Rational squareness is decided by integer square roots of
the reduced numerator and denominator. Hence no case is possible.
\(\square\)

The hypotheses that all squared distances are finite, nonzero, and
distinct are deliberate. The proposition does not analyze a contact
at a pole, colliding contacts, a nonlinear substitution, a union of
more projective copies of \(S\), or a different arithmetic contact
family.

## 3. Larger symmetric unions and the coordinate balance

For any five nonzero rational numbers \(b_i\) with disjoint orbits under
\(x\mapsto-x\) and \(x\mapsto c/x\), where \(c\in\mathbf Q^\times\),
the union of their four-element orbits has twenty points and

\[
 \prod_{i=1}^5
   (x^2-b_i^2)(x^2-c^2/b_i^2)
 =x^{10} Q_5\left(x^2+\frac{c^2}{x^2}\right),
\]

where

\[
 Q_5(Y)=\prod_{i=1}^5
       \left(Y-b_i^2-\frac{c^2}{b_i^2}\right).
\]

If the \(b_i\) form a projective copy of \(S\), the twenty-point set
is the union of four projective copies. Away from a fixed exceptional
set, their odd contact radicals are disjoint. The existing base
height bound of exponent \(7/3\) would therefore give exponent
\(7/12\) on the union, and the sharper logarithmic bound would give
exponent \(1/2\) with a logarithmic factor. This is a height statement
only; a defining polynomial requires a complete soundness and
realization proof for its precise normalization.

The obvious quadratic computation of
\(Y=x^2+c^2/x^2\) uses two coordinates \(r,Y\), with
\(r=x^2\) and \(rY=r^2+c^2\). A quintic contact circuit then uses
two more outputs. This is four contact outputs, compared with three
in the current ten-contact circuit. The quartic audit reports that
lowering deep comparison precision from three to two removes one
additional fifth-power weight per detector in the four-factor
explicit source, but removes no coordinate in the five-factor
existence source. Thus the obvious four-output implementation only
ties the present explicit count and worsens the existence count.
No unconditional variable improvement follows from this identity
without a further circuit or arithmetic saving.

## Reproduction

Run

```sh
python3 checkpoints/few_variables_v22/check_base5_symmetries.py
```

The standard-library checker produces
`base5-symmetries-certificate.json`, verifies the complete projective
enumeration and the independent five-invariant argument, and rejects
all 60 signed reciprocal cases by exact rational arithmetic.
