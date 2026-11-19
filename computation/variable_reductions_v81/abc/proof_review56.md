# Independent review of the 56-variable quartic

**Conclusion:** the change from the published 58-variable construction to
56 variables is valid under the explicitly retained arithmetic premises
and ordinary rational abc. The exact native pole uses Burungale's
published Theorem B in its square class seven. This is a review of the
new transfer and its algebra, not an independent proof of the inherited
elliptic, formal-comparison, trace-index or simultaneous prime-pattern
inputs. The sufficient odd parameter remains ineffective.

The retained chart and Laurent packing come from **notes of Gabe Conant
with Astra 6.2**, audited in v78. The derivative transfer is v79; the
one-helper normalization and published square-class-seven realization
are v80. The nonlinear paired contacts and the uniform two-adic trace
argument are the new v81 steps.

## 1. Independent reconstruction and count

`check56.py` imports neither the producer nor an earlier checker. Its
retained physical reconstruction and native twist identities are copied
explicitly from the reviewed v80 code, so no new independence is claimed
for those inherited routines. It reconstructs the new contact equations
from four factors `P-2*r*r*S+r**4`, differentiates them symbolically,
and compares every row and coefficient using SymPy. The producer uses
separate sparse integer arithmetic.

The result is 44 retained coordinates, two height coordinates, nine
contact coordinates, and one normalization coordinate: **56 total**.
There are 32 retained and 14 new or rederived rows: **46 quadrics**.
The full sum of their squares has degree four, **809 coordinate
monomials**, **812 parameter-separated terms**, and content one.
All 56 coordinates occur. The coefficient of the fourth power of the
input is one, so content remains one after specializing the parameter.

The constant coefficient is `B^2+377888002299`. The greatest absolute
coefficient independent of B is `125368156160`. The only other mixed
profiles are `16*B+1` and `4*B+1`; the largest purely linear parameter
coefficient is `2*B`. Completing squares proves that the constant
coefficient dominates for every positive integer B. Thus the exact
height is `B^2+377888002299`, independently of the ineffective defining
threshold.

## 2. Contact identities and complete rational fibres

Set a=M^4+16, x=M^4-z, y=M^4+z, and use the eight shifts
8, 9, 12, 15, 17, 20, 23, 24. With T=a^2-z^2, S=a^2+z^2,
P=T^2, the product G(x)G(y) is the product of the four factors above,
for radii 1, 4, 7, 8. Pairing (1,8) and (4,7) produces A1 and A2.
Their equal sums of squared radii, 65, imply

```math
H_2-H_1=720(-4T+8S-130),\qquad
H_i=2T(A_i)_P+(A_i)_S.
```

The checker derives this identity and the chain rule
F_a=2a(H1*A2+A1*H2) directly. Store Fbar=F/a, which is permitted
because a>0 for every rational M. The quadratic quotient row then
recovers F_a+16cF=0 exactly. There is no division by z, T, S, P,
individual paired factors or their derivatives. Their zero fibres are
retained; these are equations with a unique lift of the physical
contact tuple, not a birational assertion on an unspecified open set.

The literal unit row gives c nonzero. Both G(x) and G(y) cannot vanish:
that would force x+y to be a negative sum of two positive shifts,
whereas x+y=2M^4>0. If one vanishes, its derivative is nonzero and
the other factor is nonzero, contradicting F_a+16cF=0. Thus F and
F_a are nonzero automatically. The sole new division by a is harmless.

## 3. Height estimate and soundness

The proof of v63's derivative-height theorem was checked before its last
replacement of the maximum slot height by half a product height. That
intermediate inequality only requires distinct fixed nonzero shifts
with no opposite pair. It does not require zero sum of the shifts or
nonzero x*y. All present shifts are positive, so all required pair sums
and translated contact sums are nonzero. A zero slot has only fixed,
nonzero shifted factors and creates no exceptional height loss.

For eight contacts and epsilon=1/100, the intermediate lower bound is
1.97 max(h(x),h(y))-2.01 h(M)-O(1). Since x+y=2M^4, its coefficient
of h(M) is **193/100**. All constants depend on the fixed shifts and
retained chart, not B.

The height padding is M=B+2s, s=X^8+Tsc^2>=0. In lowest terms s=N/D,
the numerator BD+2N and denominator D have common divisor at most two.
Therefore h(s)<=h(M)+log(2) uniformly in positive B. The retained signed
mixed-power estimate has coefficient **501/997** for h(X). The strict
margin is **92221/99700**. The trace-index bound completes the same
bounded-height contradiction as v80. This argument does not use an
effective value of B.

For each consumed positive odd valuation mu=v(u), the normalizer yields
v(D)>-3mu/4. If both valuations of W are negative, the norm/trace
selector gives v(D)<=max(v(W),v(bar(W))); otherwise an integral slot
already exists. Thus one slot has v(W)>-3mu/4. The four nonconstant
terms of W have different valuation classes modulo four, using the
retained even valuation of reciprocal abscissas. Any negative minimum
is unique, so the four raw tests have strictly positive valuation.
The original inverse-parameter extraction then applies. Zero raw tests
have infinite valuation and are included.

## 4. Normalizer, signs and zero values

The physical variables satisfy

```math
\alpha=u+u^2D^2,\qquad
\tau(1+\alpha)=\alpha,\qquad b=7\tau^2/u.
```

The stored equations decode with D=c*Ds, b=c*bs, and c=1/u. In
particular the actual pole input is b, with exactly the displayed
square factor. The gate excludes alpha=-1 identically. The radical
height bound guarantees a positive odd valuation of u for sufficiently
large B, excluding u equal to a negative rational square. Hence
alpha=0 is impossible as well. No extra inverse coordinate is needed.

If mu=v(u) is odd and d=v(D), the two summands of alpha have different
parity, so v(alpha)=min(mu,2mu+2d). At mu<0 this is negative; tau is a
unit and v(b)=-mu>0 away from seven, without any bound on the actual
point denominators. At mu>0 the native pole excludes v(b) negative
odd, forcing v(alpha)>mu/2 and d>-3mu/4. The D=0 fibre is retained
at both signs. The finite grid in the checker is regression evidence;
this parity proof supplies the universal statement.

The native pole's obstruction has no hidden nonzero witness hypotheses.
At v(b)<0 odd, the first conic forces e to be a unit; its mixed equation
then forces the two product factors to be nonzero and to have unequal
valuations. Their squared difference has even valuation, contradicting
the last equation even if its right-hand witness is zero. This works
also at two.

## 5. Uniform two-adic preparation

Independent exact duplication confirms the coordinates of [2]R0,
its formal parameter (232+86*sqrt(2))/357, and
4 Tr(x([2]R0))=57. In Q2(sqrt(2)), with v2(2)=1, this formal parameter
has valuation 3/2. The integral formal logarithm is isometric when
v2(xi)>1, because each higher term a_j*xi^j/j has strictly greater
valuation. For every nonzero even n this gives
v2(xi([n]R0))=v2(n)+1/2, hence n^2*x([n]R0) belongs to (1/2)O.
The trace of (1/2)Z2[sqrt(2)] lies in Z2.

For odd n, write [n]R0=R0+Q, where Q is in that formal neighborhood
or is the identity. In the secant addition formula the normalized
denominator x(Q)-x(R0) is a unit power series. Its expansion has
integral coefficients; the negative powers cancel, leaving integral
translation. This does not presume nonsingular reduction of R0.
The checker confirms the first coefficients directly, while the
unit-power-series argument proves the full statement. Thus the scaled
trace is two-adically integral for every integer witness.

The zero-input fibre has Tsc=-37888/7199 and nonzero reference-difference
norm 7199/328, both checked exactly. Consequently every integer
witness has M odd at two when B is odd, and a=M^4+16 congruent to one
modulo eight. This is precisely the local square needed at the actual
detector input, rather than a condition on an unrelated auxiliary value.

## 6. Completeness and every prime

For a fixed integer n, first fix Tsc, M and a using the parent
multiplication family. The sixteen contact positions are distinct.
The retained simultaneous prime-pattern and comparison-index theorem
is invoked with the required real and local neighborhoods. This
invocation is an explicit retained premise, not a finite search.

The finite preparation set includes all numerator and denominator
primes of the fixed contact positions, their nonzero pairwise
differences, and a. It may depend on n; it does not change the fixed
exceptional set in the height proof. The exact factorization of F
into sixteen selected primes divided by D0^32 L^32 ensures that all
positive odd valuations of u occur at those selected primes. At those
primes the original successful-slot preparation gives v(D)>0 and
v(b)=1. Outside that set, integral slope gives v(u)<=0. A nonintegral
slope outside the preparation set gives even v(u)=2v(z). At a prepared
place the exact leading terms give v(u)=2v(z)-v(a)<0. This last value
may be odd; the uniform negative-odd normalizer was specifically checked
to handle it without a later choice depending on point denominators.

For large slope, F has leading term z^16 and F_a has leading term
-16a z^14. Thus c is asymptotic to a/z^2, including at two after
sufficient local depth. Bounded raw point neighborhoods give D=O(c^2)
and tau tending to one. Real preparation gives 0<b<1. The uniform
two-adic lemma gives b in 7 Q2-square with v2(b)>=4. Seven is explicitly
prepared to have positive valuation. Every other negative valuation
of b is even, so b has square reduced denominator.

The published Burungale theorem is applied with beta the positive
squarefree part of b and eta that of 1-b. They are coprime, beta is
seven modulo eight, eta is one modulo eight, and the required cross-local
square conditions follow from b or 1-b being congruent to one at the
corresponding odd primes. Eta=1 is allowed. The points obtained have
nonzero ordinates: the possible positive two-torsion abscissas have
two-adic class five, distinct from class seven. All denominators in
the explicit map to the three native equations are therefore nonzero.
The checker verifies the map as rational-function identities.

The zero-input fibre has all raw tests zero, W=1 and D=0. Its equations
give tau=1/(1+c) and b=7c/(1+c)^2, so the same real and local
preparation applies. No input factor is attached to the polynomial.

## 7. Scope and remaining work

This establishes the 58-to-56 reduction under the named assumptions.
It neither lowers the general 165/180 quartics nor realizes the
unresolved 25/11-variable pole families. A direct deletion of another
contact register would require a new equivalence proof; the current
count is not a global lower bound. Computational certificates do not
prove abc, the retained arithmetic inputs, or effectiveness.
