# Independent review of even-valuation balancing

**Result: PASS within the retained arithmetic premises.** The source remains
complete in eleven total variables; the actual-trace source remains sound in
nine. The new degree bounds are upper bounds from a finite determinant
specification, not exact expanded degrees. Neither global rational
realization nor an effective defining parameter is established.

## Local lemma and soundness

For a normalized nonarchimedean valuation and
`y^2=x(x^2+A*x+B)` with `v(A)>=0,v(B)=0`, the proof of even `v(x)` is
complete: if `v(x)>0`, the constant B is uniquely minimal in the second
factor; if `v(x)<0`, the term x squared is uniquely minimal. The resulting
equalities `2*v(y)=v(x)` and `2*v(y)=3*v(x)` force even parity. If `v(x)=0`
there is nothing to prove. The hypotheses exclude zero x and y as the source
already requires. For the project curve, `Norm(11-6*sqrt(2))=49`, so the
coefficient is a unit outside seven. At the consumed odd primes, K is
unramified, and rational u has the same normalized valuation in each slot.
The argument applies equally to full auxiliary points and their guarded
differences; it makes no global square assumption.

With odd `nu=v_p(u)` and even `c=v(C)`, `nu+c` cannot vanish. Therefore
`v(C/(1+u*C))=c-min(0,nu+c)=max(c,-nu)`. For positive nu, positivity is
equivalent to that of c. For negative nu, `2*v(D)-nu>=-3*nu>0`.
This proves exactly the local properties the detector uses. The remaining
two comparison tests retain squared balancing, including their possible zero
values; those zero factors simply contribute one to W.

At positive odd nu, the intrinsic pole implication gives
`1<=v_p(b)<=nu+2*q`, where q is the largest slot valuation of W and q is
nonpositive. Each factor valuation is nonpositive, so each is at least q.
It follows that every transformed test has valuation greater than `nu/4` in
a successful slot. The new identity recovers positive valuations of all four
abscissa tests; the old identity does so for the comparisons. Thus the
unchanged formal comparison extracts the same congruence for X and the root
index. Contact polynomials and height parameters are exactly preserved.
The absorption margins are `44272779/198801800` for nine contacts and
`38695561/597203000` for seven, both positive.

## Completeness and characters

At a selected contact `v_p(u)=1`, the old first four tests have valuation at
least two. The new D has that same valuation, so `D^2/u` has positive
valuation and the detector factor is still one modulo p. The old comparison
factors and the successful-slot trace argument are unchanged. At negative
odd u valuations every factor is again one modulo p, including new
denominator primes of the derivative. At even valuations the valuation of b
is even by its formula. These observations preserve the proof that eta has
square reduced denominator.

For fixed-place preparation, u grows with the slope while each already
prepared nonzero test is fixed. Both versions of D are then asymptotic to
`1/u`, and zero comparisons remain zero. Consequently W tends to one and V
to two with the same square-class preparation. No new finite obstruction is
introduced by the balanced denominators.

The real completeness argument correctly uses the original `2E(K)`
subfamily, not arbitrary full auxiliary points. The abscissae of this
subfamily are positive at every real point character. The displayed Kummer
identity for difference abscissae holds for either ordinate sign; the
existing difference guards exclude its zero or undefined cases. Therefore
the first four tests stay positive at all those characters. With positive u,
all new balanced denominators and all detector factors are positive. This
is enough to retain the whole-character norm avoidance and the original
intrinsic-pole existence argument. Only the terminal ordinate's native
guard is suppressed by the final compiler; earlier radicands remain units.

## Exact circuit and denominator audit

The direct implementations `1/(x+u)` and
`Delta^2/(X0+u*Delta^2)` are exactly equivalent to `C/(1+u*C)` on the old
guarded open set. In particular, replacing a norm of `1+u*C` by the norm of
its displayed numerator is valid because the old denominator norm is already
a unit. Conjugation for the two difference tests is retained. The source
continues to store all six balanced norms explicitly.

The additional `independent_math_check.py` imports no producer module. It
checks these rational identities, the Kummer identity modulo the curve
equations, the coefficient norm, and both stored source prefixes. For nine
contacts the first 963 DAG nodes equal v71; for seven contacts the first 942
equal v74. All point events, contact events, six original tests and
prebalancing guards are identical. It verifies the new guard labels, the
terminal-only suppression policy, and the exact final degree formulas.

Both original independent specification/native checkers were rerun. Each
passes its degree traversal, 384 actual finite-field point characters, and
both corruption rejection controls. In each case the native evaluator uses
the original C values and the rational expression `C/(1+u*C)`, independently
of the producer's direct denominator formulas. The resulting bounds are:

| Contacts | Source nodes | Native guards before terminal suppression | Degree upper bound | Fixture B=3 log2 l1 bound |
|---|---:|---:|---:|---:|
| Nine | 1865 | 32 | 230932097 | 480197504 |
| Seven | 1815 | 32 | 356146817 | 720737280 |

Both have rank 128, eleven total variables and content one. The nine-contact
degree bound improves the preceding 232094337. The seven-contact variant
serves the smaller physical lift and is not a final-degree record.

## Actual halfpoint cover

Both producer-free reconstructions in
`computation/pole_parameters/even_halfpoint_trace_v75/check_independent.py`
were rerun successfully. They reconstruct the actual quadratic-field point,
its duplication, the conjugate detector factors, and both physical pairs by
differentiating before specializing the scale. The resulting identities are

    D0=u^2*(1-2*u-u^2)^2,
    R0=D0+2*u^3+4*u^2+6*u+1,
    W=(R0/D0)^2, V=2*D0^2/R0^2,
    Pi0=4*D0^4*(1+u)^2+2*u*R0^2*(R0^2-D0^2).

The degree-26 weight polynomial is squarefree, certified modulo 53, and has
genus 12. The selected-character denominators are nonzero for rational
`u!=0,-1`: the balanced quadratic has discriminant eight, and the monic
constant-one polynomial R0 has nonzero values 17 and 1 at its only possible
rational roots 1 and -1.

The degree-seven and degree-nine physical pairs remain coprime modulo 53.
Their homogeneous compositions have degrees 182 and 234, nonzero constant
terms, and independent Bezout certificates with their derivatives. The
genera are respectively `(90,91,181)` and `(116,117,233)` for the squared
slope, its T twist, and the slope. Degree preservation and the Bezout
identities justify these statements in characteristic zero. All physical
square and denominator tests remain necessary; these covers provide no
guarded rational witness or completeness theorem in nine variables.

## Reproduction and limits

```sh
python computation/few_variables/even_valuation11_v75/check.py
python computation/few_variables/even_valuation11_v75/check.py --specification computation/few_variables/even_valuation11_v75/seven_contact
python computation/few_variables/even_valuation11_v75/independent_math_check.py
python computation/pole_parameters/even_halfpoint_trace_v75/check_independent.py --contacts 7
python computation/pole_parameters/even_halfpoint_trace_v75/check_independent.py --contacts 9
```

The retained elliptic group, formal comparison, height, prime-pattern and
intrinsic-pole inputs were checked for applicability to this transfer, not
reproved from external foundations. Finite native character evaluations
verify the stored circuit cases; they are not substitutes for the
whole-character proof. There is no claim of rational-point enumeration,
an effective sufficiently large B, or 21/9-variable completeness.
