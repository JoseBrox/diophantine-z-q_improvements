# Direct-input conditional thirteen-variable construction: arithmetic audit

Status: PASS. This audit concerns the mathematical transcription in
`papers/conditional_few_variables/direct_input13_20261110_v22.tex`.
The quartic agent separately checks the exact source-expression substitutions.

## Height estimate

For every rational input X and integer B>=3, beta=2X^2+B satisfies
beta>=B and 2h(X)<=h(beta). Indeed, if X=u/v is reduced with v>0,
the cancellation factor in (2u^2+Bv^2)/v^2 is gcd(2,v^2)<=2.
The numerator before cancellation is >=2 max(u^2,v^2).
The estimate has no additive term depending on B.

The general even-power lemma is correct with alpha=d/kappa-3>0:

    h(1:u:v) <= alpha^(-1) h(u^d+v^d)
                +(alpha+1)/(d alpha) log 2
                +1/(kappa alpha) log K_kappa.

The common numerator factor and all denominator cancellation are retained.
In its primitive proof the three final coefficients are nonnegative and
sum to 1/alpha; d-1-alpha=d(1-1/kappa)+2>0.

Combining two contact heights with gamma=8/kappa-6 gives
q=2/(gamma alpha). With N=|num(X-n)|, one has
log N<=h(X)+log(1+|n|), hence absorption coefficient q/2.
The exact pairs are:

* kappa=121/100, d=6: gamma=74/121, alpha=237/121,
  q=14641/8769, q/2=14641/17538<1.
* kappa=16/15, d=4: gamma=3/2, alpha=3/4,
  q=16/9, q/2=8/9<1.

The general criterion is gamma*alpha>1. Its stated boundaries
(30-2 sqrt(21))/17 for d=6 and (24-4 sqrt(2))/17 for d=4
are the smaller roots of the corresponding quadratic inequalities.

The trace-index inequality n^2<=A h(T(n))+J then gives a uniform
bound on n and h(beta), independent of B. Since beta>=B, every
sufficiently large fixed odd B forces X=n. The proof does not give
an effective numerical B.

## Completeness for every nonzero integer label

Take X=n, A=[n]P, H=[h]P and U=[hn]P, with n any nonzero integer.
The point chart describes all nonzero multiples of P. No step here
requires n positive or odd.

The difference chart U-A fails through equal abscissas exactly when
U=+A or U=-A; for n!=0 and non-torsion P this is h=+1 or h=-1.
The H-P chart has the same exclusion. Taking h!=0,+1,-1 also
excludes all identity points appearing in the source. Multiplication
by any nonzero integer n is a nonconstant isogeny. Therefore the
remaining finite rational-function denominator loci can be avoided
on the inherited real and fixed-prime compact neighborhoods.

The retained prime-pattern and CRT steps impose h=0 modulo primary
annihilating orders and h=1 modulo the conjugate orders. They make
H,U primary-formal and H-P,U-A conjugate-formal regardless of sign
or parity of n. Both exact formal logarithmic ratios equal n.
Since n is p-integral at every selected prime, relative precision
four supplies the absolute precision needed for the order-one
comparison and direct target X tests.

For n=+1 or -1 some tests vanish identically. This is harmless:
there are no guards requiring individual tests nonzero, and their
norm factors are simply one. The other affine guards still hold.

The scale beta^d+T(n)^d is positive, distinct from1 and fixed before
prime selection. The degree-six contact prefactor contributes its
sixth power, a rational square, even if the scale itself is not a
square. Real and bad-prime preparation consequently remains valid.

## Input zero

The guarded source necessarily has A=[n]P with n!=0. The outer
polynomial operation F=X*Q preserves its rational zero set for X!=0
and makes every rational witness tuple a zero when X=0. No point
chart is being evaluated at A=O in this added branch. The operation
adds one to degree and introduces no variable or guard.

## Scope

This verifies the revised arithmetic argument and its completeness,
conditional on precisely the elliptic, prime-pattern and pole inputs
retained in the paper. It is not an independent proof of those inputs,
and it makes no new variable-count reduction beyond the stated thirteen.
