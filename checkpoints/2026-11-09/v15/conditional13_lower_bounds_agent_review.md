# Independent mathematical review of the thirteen-coordinate family

Review outcome: PASS under the arithmetic assumptions stated in the paper.

Reviewed source:
repo/papers/conditional_few_variables/conditional13_20261109_v15.tex

## Decisive inequalities

The rational abc conjecture at exponent 12/11 gives

    h(u)+h(v) <= (4/5)h(u^6+v^6)+C1,
    C1 = (7/15)log(2)+(11/15)log(K_{1/11}).

The common numerator factor, shared denominator, complete cancellation
against the output denominator, zero coordinates, and all signs are
accounted for. The proof's intermediate coefficients
1/6, 1/15, 1/6 add to 2/5 for the projective pair height.

Granville's homogeneous degree-five radical consequence of abc, with
epsilon=1/20, gives log M >= (9/10)h-C. Thus the contact height
coefficient is 10/9. The Mobius map t -> 2+1/t correctly carries the five
new contacts to the five original contacts and changes height by at most
log(3). All exceptional determinants have primes in the fixed excluded set.

For a=(beta^6+T^6)^2, the scalar coefficient is 2/5. Combining the two
contact heights therefore gives

    h(beta)+h(T) <= (8/9)log(N)+C.

As N <= exp(h(beta))*(1+|n|), this gives

    (1/9)h(beta)+h(T) <= (8/9)log(1+|n|)+C.

The fixed trace-height inequality n^2 <= A*h(T)+J bounds n, then h(beta).
Every constant in this chain is independent of the coefficient shift B.
The inequality beta=2X^2+B >= B therefore excludes beta != n uniformly
for all sufficiently large fixed odd B. Integrality of beta implies
integrality of X because the reduced denominator of X has square dividing 2.

## Local implication

At a contact prime the product valuations are sums of minima with terms
of different parity. The pole obstruction forces at least one local
component of every test to have positive valuation. The four first tests
put the two pairs of elliptic points in the required formal groups.

The exact local logarithmic ratios are u/h and (u-n)/(h-1). At least one
denominator is a p-adic unit. This makes one ratio integral; the relative
formal-parameter error and the difference test make the other ratio
integral. Only after this step are the relative error estimates converted
to absolute congruences. Multiplying by h and h-1 and subtracting then
gives beta=n modulo p. This justifies the radical divisibility used above.

## Completeness and guards

With n=beta fixed, A=[n]P, H=[h]P and U=[nh]P realize both exact ratios
as n. The affine difference denominators exclude h=+1,-1. All other
point and ratio denominators restrict to nonzero rational functions of
H, and exclude only finitely many multiples. The fixed real and local
neighborhoods can be chosen to avoid them.

For sufficiently large positive slope, both real embeddings of every
comparison factor are positive. Thus the product, its norm, and the trace
of its inverse are nonzero. On the fixed compact real neighborhood the
weights tend uniformly to zero and the pole input tends to zero through
positive values. At the contact primes the trace of the inverse is a unit,
with residue one or two. The preparation squareclasses and depths at
2,3,17 follow from the stated prime-pattern congruences and arbitrarily
deep fixed denominator divisibility.

The CRT requires h_* divisible by 16; the final text has the sufficient
stronger choice h_* in 64Z. This resolves the only textual omission found.

The inherited simultaneous pole construction has a fresh prime in its
twist parameter. Its required positive squareclass points are therefore
outside two-torsion, and both ordinates are nonzero. Rescaling gives
p*q*s nonzero, hence e!=1. The chart tau=p/(e-1) has
tau^2+3B0=4B0/(1-e)!=0 and reconstructs both the first pole equation
and the required nonzero second root. Two independent parameter pairs
therefore preserve completeness without a shared-parameter assumption.

## Precisely retained limitations

- Ordinary rational abc is an additional assumption.
- The source elliptic-group, pole-realization, and simultaneous
  prime-pattern inputs remain explicitly retained premises.
- The sufficient fixed input shift is ineffective.
- The numerical B=3 certificate verifies algebra, degree, and coefficient
  bounds for that member; it does not certify that it defines the integers.
- This review independently checks the mathematics. The separate exact
  circuit auditors certify the finite algebra and coefficient implementation.

No further mathematical gap was found in the reviewed argument.
