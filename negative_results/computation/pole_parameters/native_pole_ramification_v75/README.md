# Native pole witnesses: norms and ramification

This package records two precise limits of attempts to remove the native pole
parameters. It does not disprove prepared realization or establish a lower
bound for other Diophantine definitions.

1. The built-in norm representation of the balanced detector is automatic,
   but does not provide a native pole witness. An **actual physical**
   seven-contact tuple with `X=1`, `B=3`, `A=P`, `H=U=P/2` and
   `z=(10621537/256)^8+8+100003` has `v_100003(b)=-7`.
   All 30 native pre-pole guards hold at all 64 point characters. The
   point/contact/balanced/product/trace guards therefore do not repair the
   invalid inference from a norm identity to a pole witness.
2. The native intrinsic and general17 pole equations exclude odd negative
   orders over geometric discrete valued fields as well. Every finite
   degree-d slope cover carrying native witnesses must ramify evenly above
   each of r distinct odd contact poles, giving `g >= 1+d*(r-4)/4`.
   For `r=10,14,18`, the minimum genera are `4,6,8`. The codimension-two
   reference-test argument also forces constant slopes in the abelian
   families specified in the paper, including the even-valuation revisions.

The counterexample uses the original squared balancing in
`seven_contact11_v74`. Its physical weight is computed by differentiating
before specializing the scale. It is an actual multiplication tuple and
actual slope, **not** a fixed-place or selected-prime prepared witness.
No sufficiently large defining value of B is certified by the fixture B=3.

## Reproduction

From the repository root:

```sh
python negative_results/computation/pole_parameters/native_pole_ramification_v75/check.py
python negative_results/computation/pole_parameters/native_pole_ramification_v75/check_independent.py
```

The exact checker verifies the universal norm identities, point doubling
and tripling, physical contact values, halfpoint detector identity, negative
odd valuation, 768 positive balanced denominator evaluations, and 1920
nonzero evaluations of the actual source's 30 pre-pole guard numerators.
The latter use reduction modulo 1000000007 at all 64 algebraic characters;
nonzero reductions prove the characteristic-zero values are nonzero.
Finite valuation boundary cases supplement, but do not prove, the general
valuative statements.

The independent checker imports no producer or project module. It reconstructs
the quadratic norm in a four-coordinate algebra, doubles and triples the point
independently, rebuilds the physical weight and actual balanced product, and
recursively evaluates all 1920 guard values at the different split prime
1000000009. The independent mathematical review checks the new local,
ramification and abelian-family proofs and binds the final source hashes.

The complete proof is in
`negative_results/papers/pole_parameters/native_pole_ramification_20261117_v75.tex`.
The paper distinguishes fixed-point finite covers, variable abelian families,
and the arithmetic possibilities left open. The general cover obstruction
applies to certificates with the stated valued-function-field property;
it is not a theorem about every criterion whose soundness holds only over Q.
Constant-slope abelian families, isolated rational witnesses, and nonabelian
families of dimension at least two remain outside the exclusion.

The manuscript compiled twice and all six rendered pages were inspected. Its
separate build receipt is
`data/audits/tex_native_pole_ramification_20261117_v75.json`.
`manifest.json` binds the package files, manuscript, build receipt and the
stored seven-contact source used by the two independent evaluators.
