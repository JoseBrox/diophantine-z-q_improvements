# Independent audit of the elliptic sum-height theorem

17 November 2026.

## Verdict

The theorem and its effective S-integral finiteness corollaries are valid as
stated. No mathematical gap or necessary correction was found. The argument
requires a common cyclic group modulo K-rational torsion. The extension to
every elliptic curve and every number field is justified. Replacing the sum
by a field trace, allowing unrestricted higher-rank tuples, or deducing
Diophantine definability of a ring of integers requires additional arguments.

## Integral formal group, bad reduction and residue characteristic two

Substitution z=-x/y and X=z^2 x gives X^3-X^2+A z^4 X+B z^6=0. Its X derivative
at (1,0) is 1, so coefficient recursion is integral over Z[A,B]. Uniqueness and
the absence of a z^2 term give X in 1+z^4 Z[A,B][[z^2]]. The invariant
differential identity 1-zX'/(2X) is integral because X is even. Thus the
logarithm has only odd exponents m>=5 beyond z, with integral numerators
divided by m.

At odd primes, v_p(m)<=(m-3)/2 and 2v(z)>=e give correction valuation at least
3v(z). At p=2 every m is odd, so the correction has valuation at least 5v(z),
for any ramification index. This proves the logarithm isometry and integrality
of x-ell^-2. Good reduction is unnecessary: the integral model is smooth at
its origin and the formal group has integral law. A negative x-valuation
forces the point into that formal group with v(x)=-2v(z).

The deep subgroup is open in the compact local group. A positive multiple of
P lies in it. L=ell([q]P)/q is independent of q and nonzero. Multiplication
by the torsion order proves ell([n]P+T)=nL whenever the point is deep. Thus
zero-index finite points are never deep. Shallow torsion points are correctly
allowed to have denominators bounded by the ramification allowance.

## Sum, translation and normalization

The subset numerator C_J is a positive integer for every nonempty set of deep
indices; all those indices are nonzero. Negative and repeated indices cause
no cancellation. The bound on local loss remains valid when the principal
and error terms tie, including exact cancellation of the entire sum.
The place weight f log(p)/[K:Q] makes the total weighted valuation of a positive
rational integer equal to its logarithm. This gives the stated a_r and b_r.
The different exponent is at least e-1, proving the discriminant bound. An
arbitrary c contributes exactly h_fin(c); no archimedean term in c is needed.

## David--Hirata-Kohno checked directly

The published primary paper is S. David and N. Hirata-Kohno, Linear forms in
elliptic logarithms, J. reine angew. Math. 628 (2009), 37-89,
DOI 10.1515/CRELLE.2009.018. Its complete published text was independently read
at https://www.academia.edu/109964712/Linear_forms_in_elliptic_logarithms .
Data 1.4, Theorem 1.6 and the projective exponential definition on printed
pages 40-43 were checked.

Choose auxiliary E=e and large fixed V_i for the fixed logarithms. These V_i
include the analytic sizes of the periods; identity images do not force V_i=1.
The coefficient-height parameter occurs only as a linear factor log B. The
iterated logarithm applies to fixed V, not to B. The theorem's constant is
effectively computable. The projective exponential includes the identity,
so period logarithms are permitted. A nonzero evaluated linear form puts the
fixed vector outside its kernel, hence outside every subgroup tangent contained
in that kernel. This is exactly s=t=1. No independence of the three fixed
logarithms is required.

The product of counts at two good reductions of distinct residue characteristics
annihilates rational torsion: each prime-primary torsion subgroup injects at
one of the two places. The centered parallelogram gives coefficients
O(t(|n|+3)), and contains no lattice point except zero. Therefore the linear
form is nonzero for every finite point, including n=0. The double pole of wp
proves the claimed effective O(log(2+|n|)) archimedean bound.
An optional editorial clarification is to choose the period basis with its
ratio in the standard fundamental domain, matching DHK's notation explicitly.

## Effective S-integral finiteness and rank-one curves

At a fixed finite place, the denominator height of a deep point is
2v_p(n)+2v_p(L), an effective O(log M) quantity. The fixed valuation v_p(L)
is computed from v_p(z([q]P))-v_p(q), so it does not require approximating an
infinite p-adic logarithm. Shallow points have bounded local height. Removing
any fixed finite set S and the infinite places therefore costs O(log M).
For S-integral c, the outside-S translation loss is zero. The quadratic
canonical height then gives an effective bound on all indices of S-integral
sums. No separate p-adic linear-forms theorem is needed.

Zywina's Theorem 1.1 was independently checked on the primary manuscript
https://davidzywina.github.io/papers/Rank1WithStability.pdf . It states infinitely
many rank-one elliptic curves over every number field up to isomorphism.
Their full rational point groups are cyclic modulo torsion; canonical-height
comparison converts log M to O(log(H+2)), proving the whole-point-domain
corollary. Effectiveness is correctly stated for a supplied curve and generator;
no uniformly effective choice of all generators is claimed.

The finite formal-series checker was rerun and passed. It certifies only the
finite identities it checks, while the manuscript proves the infinite formal
and transcendence assertions. No defining-variable reduction follows from
this height theorem alone.

Audited manuscript SHA-256: `6c63f90fde1b06ca1f22274380a604338534e960af5649df445dd9d3a67ff7de`.
