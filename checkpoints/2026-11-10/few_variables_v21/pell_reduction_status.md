# Arithmetic status

No construction below 25 variables, or below 13 under weak abc, is proved here.

## Monic rational-root reduction

For integer labels a,u, put t=(a-2)u+1. A rational root C of

    C^2 - a*t*C + t^2 - 1 = 0

is integral. With u nonzero, |a|>7 and the usual nontrivial branches,
the Pell/Lucas recurrence forces an index of size at least |a-2|-1.
Thus the abstract growth mechanism can use two integer labels
and one finite rational choice instead of three integer labels.

The current elliptic source only provides truncated formal-logarithm
ratios L_a,L_u approximating a,u at its contact primes. Requiring an
exact rational root over those ratios has no proved global rational
completeness. If a rational C is instead retained freely and the Pell
polynomial is only a local test, its denominator is not bounded by the
retained integer labels. Forcing local solvability at many primes gives
quadratic-residue conditions on the integer discriminant; it does not
give a nonzero bounded integer residual. A nonsquare discriminant can
be a square at arbitrarily many primes, so prime quantity alone does
not repair this.

## A tempting point reuse and its failed order of choices

One point with label t*b would serve both numerator roles for t and b:

    (t*b)/b = t,       (t*b)/t = b,
    (t*b-t)/(b-1)=t,  (t*b-b)/(t-1)=b.

This would reuse the root points bP,tP as denominators. The existing
prime-pattern realization cannot justify it. Those root points and
the scales built from them are fixed before contact primes are chosen,
whereas the denominator index has to satisfy newly prescribed primary
and complementary reduction orders. A fixed nonzero root point is
formal at only finitely many good primes. The common free index in the
published construction is what avoids this obstruction.

## Algebraic removal of the product point

The accompanying TeX proves a stronger restriction than the
translated-homomorphism observation: the full index-product graph is
Zariski dense, even for infinitely many labels with an arbitrary
infinite set of common indices for each. Consequently finite algebraic
choices do not supply a uniform reconstruction of [hn]P from hP,nP.
The elliptic proof is elementary; the general abelian statement uses
the established Mordell--Lang theorem. This is a strategy restriction,
not a lower bound for arbitrary definitions.

## Sources checked

Faltings, The general case of S. Lang's conjecture (1994),
DOI 10.1016/B978-0-12-197270-7.50012-7, publisher entry verified.
The exact finite-union-of-cosets form was checked in the introduction
of the primary research manuscript Ghioca-Hu-Scanlon-Zannier,
https://math.berkeley.edu/~scanlon/papers/Ga_abelian.pdf.
Milne, Abelian Varieties (2008), Chapter I, Theorem 7.2 was checked
for the multiplication-degree calculation in the independent elliptic proof.
