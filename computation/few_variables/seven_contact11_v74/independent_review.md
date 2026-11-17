# Independent review of the seven-contact source and actual halfpoint cover

**Result: PASS within the retained arithmetic premises.** This review does not
prove those imported infinite arithmetic statements, any admissible rational
point on the actual cover, or nine-variable completeness. It verifies the new
transfer, the exact source circuit, and the finite polynomial assertions. The
review was performed separately from the producer and its original checker.

## 1. Seven-contact height argument

The shifts are `(-7,-6,-4,1,3,5,8)`. They are distinct and nonzero, their sum is
zero, and none of their pairwise sums vanishes, including a shift with itself.
The retained derivative-height theorem in
`papers/conditional_few_variables/derivative_detector11_20261117_v63.tex`
permits every fixed scale exponent and does not require nine shifts. For seven
shifts, scale `a=M^8`, and epsilon `1/100`, its radical coefficient is
`(7-6-3/100)/2=97/200`, while its height loss is `201/100`.

The signed mixed-power theorem in
`papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex`
applies to the guarded signed argument `t=M^16-z^2`. With kappa `1001/1000`,
its denominator is `16-10*kappa=599/100>0`, and its contraction factor is
`501/2995`. The binary-height contraction is `alpha=997/1001`. Exact rational
arithmetic gives the strictly positive absorption margin

    97/200 - (501/2995)*(201/100 + 1001/1994)
      = 38695561/597203000.

Consequently the existing trace-height and comparison argument still bounds
the root index and the height independently of the fixed odd parameter B.
The sufficient threshold for B is not made effective. Half-integral auxiliary
indices do not alter the consumed odd-prime comparisons; the root index stays
integral. The exceptional set already contains the primes of 14, all shift
differences and nonzero sums. Since `M >= beta^4 >= 81` at real characters,
`a>10`, so the omitted `2a+c+d` guards are automatically nonzero.

## 2. Completeness and whole-character guards

The full auxiliary source retains the old subfamily `H in 2E(K), U=[n]H`.
The six original tests and every precontact chart/difference/ordinate guard
are unchanged. Thus the original point preparation remains available.
The exact leading terms are `F~-z^14` and `F_a~14*a*z^12`; hence
`u~z^2/a` and `w~a/z^2`. The quantity `a=M^8` is a rational square.
These are the properties used in the fixed-place square-class preparation.

The simultaneous-prime construction has fourteen distinct positions
`+/-D^2(a+c)`; distinctness follows from distinct shifts and `2a+c+d != 0`.
At a selected prime exactly one factor of F has valuation one, while the
derivative is a unit. The original compatible index congruences and balanced
valuation argument therefore apply without changing the six tests. At poles
of z, leading-term valuations differ by `2*v(z)`; after preparing the finitely
many primes of a, the more precise expression is `2*v(z)-v(a)`, which is even.
The treatment of negative odd valuations of u remains the original balanced
identity and intrinsic-pole implication.

For the completeness subfamily, all finite point characters are real. With
z sufficiently large, u is positive; therefore every balanced denominator
is positive, each detector factor is positive, and every reciprocal trace is
positive. The selected-character intrinsic-pole hypotheses are prepared
separately. Density of rational pole parameters avoids the finite product of
the other nonzero character norms. No inequality on eta at every character
is needed. The only suppressed native guard is the last intrinsic-pole
ordinate. Earlier point radicands and all denominator norms remain units.

There are 32 native source guards before this permitted terminal suppression.
The polynomial has 11 variables including the input and a total-degree upper
bound of 357309057. This is not a degree improvement over the v71 source.
Replacing the two pole parameters by the actual trace square gives a sound
nine-variable source, but the rational realization and its prepared
whole-character completeness remain unproved.

## 3. Independent source and compiler checks

`independent_math_check.py` imports no construction or preexisting checking
module. It reads the stored coefficient DAG and checks the following exact
facts:

- The 869-node precontact prefix, precontact guards, point blocks, and six
  original tests equal the published v71 source.
- The contact product, its derivative and primitive half derivative are
  reconstructed symbolically from the seven shifts. The half derivative has
  integral coefficients with content one.
- The scale, signed argument, `u=-14*F/F_a`, and `w=u/(1+u)^2` match their DAGs.
  The degrees in the squared slope are seven and six; the leading coefficients
  are `-1` and `14*a`.
- All new contact, balanced, product, trace and intrinsic-input guards are
  present, and the terminal-root policy suppresses only the terminal ordinate.
- The height margin is recomputed by rational arithmetic.

The package's separate independent degree traversal, native chord-and-tangent
evaluation and corruption checks were rerun successfully. The native tests
cover 384 finite-field sign characters, from three actual index tuples at two
primes, and include half-integral auxiliary indices. The degree and guard
corruptions are rejected. Inspection of the generic subalgebra, unit-norm and
terminal-root compilers found no contact-count-specific assumption hidden in
the unchanged machinery. Their relevant 9 or 18 coefficients belong to the
elliptic cubic charts, not a hardcoded number of contacts.

## 4. Actual genus-twelve cover and physical lift

The independent reconstruction in
`computation/pole_parameters/halfpoint_trace_v74/check_independent.py`
was rerun. It imports no producer routine and checks the quadratic-field
point identity, including `2*(1+sqrt(2),2*sqrt(2))=P`, and all stored integer
coefficient lists. At `X=1,A=P,H=U=P/2` the six actual tests are
`(c,c,bar(c),bar(c),0,0)`, with `c=sqrt(2)-1`. Direct conjugate multiplication
gives

    D=u^2*(u^2+6*u+1)^2,
    R=D+2*u^3+12*u^2+34*u+1,
    W=(R/D)^2, V=2*D^2/R^2,
    Pi=4*D^4*(1+u)^2 + 2*u*R^2*(R^2-D^2).

Clearing the displayed square denominator gives
`Y0^2=Pi(u)` with `Y0=(1+u)*R^2*Y`. Its degree is 26, its leading coefficient
is 4, and zero is a simple root. The modulo-53 Bezout identity with its
derivative certifies squarefreeness and hence genus 12 over Q.
For rational `u != 0,-1`, the selected-character balanced, product and trace
denominators cannot vanish: the quadratic has nonsquare discriminant 32, and
the only possible rational roots of the monic constant-one R are +/-1, at
which it takes values 113 and -7. This statement is not extended to all
characters or to the preparation conditions.

The physical scale is exactly `(10621537/256)^8`. The reconstructed primitive
integer pair `A(T),B(T)` for `-14*F/F_a` has degrees seven and six and remains
coprime modulo 53. Its homogeneous composition
`P0(T)=B(T)^26*Pi(A(T)/B(T))` has degree 182, nonzero constant term, and a
verified modulo-53 Bezout certificate of squarefreeness. Therefore the three
normalizations for `P0(T)`, `T*P0(T)` and `P0(z^2)` have genera 90, 91 and 181.
The two physical polynomials retain their degrees modulo 53, so these finite
certificates imply the corresponding characteristic-zero statements.

The lift still requires `u*B(T)-A(T)=0`, `B(T)!=0`, a rational square `T=z^2`,
and every physical and preparation guard. No step identifies a rational
point on a quotient with a rational physical lift. The branch point at zero
and the rational points at infinity are outside the guarded affine domain.
No admissible rational witness or rational-point enumeration is claimed.

## Reproduction

From the repository root:

```sh
python computation/few_variables/seven_contact11_v74/check.py
python computation/few_variables/seven_contact11_v74/independent_math_check.py
python computation/pole_parameters/halfpoint_trace_v74/check_independent.py
```

The accompanying `independent_review.json` records the exact reviewed file
hashes. The review is a transfer audit and independent finite reconstruction;
it leaves every expressly retained infinite arithmetic premise visible.
