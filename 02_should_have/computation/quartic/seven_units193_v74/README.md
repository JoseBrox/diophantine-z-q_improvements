# A recovered quartic in 193 rational coordinates

This package reconstructs the interrupted 193-variable result from the published v73 194-variable system. The interrupted working files were unavailable, so byte-for-byte recovery is not claimed. The physical equations and their arithmetic proof are preserved exactly. A seven-coordinate contact-unit chart removes one coordinate; a further diagonal rescaling improves the coefficient bound.

Every count includes the input. The fixed parameter is `C = 149^N`, `N >= 1`. Under the explicitly retained arithmetic premises in the [full manuscript](../../../papers/quartic/quartic193_20261117_v74.tex), every sufficiently large fixed `N` gives a definition of the integers in the rationals. A sufficient numerical `N` is unknown. This is not an effective replacement for the separately specified 229-variable polynomial.

## Main polynomial families

Each family has **193 variables, 167 primitive quadratic squares, degree exactly four, and integer content one**. Every coordinate occurs. The coefficient of the input's fourth power is one.

| Directory | Coordinate monomials | Parameter-separated terms | Exact height | Coefficient crossover |
|---|---:|---:|---|---:|
| `compact` | 2,770 | 2,775 | `max(K, 149^(2N+2))` | `N = 6` |
| `compact_fewer_monomials` | 2,626 | 2,631 | `max(L, 149^(2N+2))` | `N = 13` |

```text
K = 126616122944180358034867798936
L = 484991541504995159662206970923766531374664106904986910720
```

The crossover values concern coefficient height, not a sufficient defining threshold. The primitive reference basis has the smaller height through `N = 12`; both heights equal `149^(2N+2)` for `N >= 13`.

Each directory contains the complete `quadratic-family.json`, the fully expanded `polynomial-family.json`, the parameter coordinate transformation, and an independent verification receipt. A term record represents `coefficient * C^parameterPower` times its coordinate monomial; repeated coordinate indices give powers. `C` is a fixed coefficient parameter, not a quantified variable.

The intermediate directories `primitive` and `fewer_monomials` have the same respective support counts and heights `max(K,128*C^4)` and `max(L,128*C^4)`. They expose the physical Laurent compilation before the final parameter rescaling and allow each transfer to be checked separately.

## Why one coordinate disappears

Let `u` be the first contact weight and `v` the ratio of the second weight to the first. The new unit chart stores seven rational values:

```text
source id  77   90   91     92          901      902      903
value      u    v   1/v    1/(u*v^2)   1/v^3    u/v      1/(u*v)
```

Five quadratic equations force their values:

```text
x77*x903 = x91
x90*x91 = 1
x77*x92 = x91^2
x90*x901 = x91^2
x902 = x77*x91
```

The second equation gives `x90,x91 != 0`; the first then gives `x77,x903 != 0`; the other coordinates are products or quotients of these nonzero values. This chart is exactly the two-dimensional torus. The former independent coordinate `x78 = 1/u` is recovered as `x90*x903` and is omitted.

The 186 remaining storage coordinates are multiplied by explicitly recorded powers of `u` and `v`. Every one of the 804 Laurent support terms is compiled to degree at most two using the seven units. The input is fixed. All 162 physical rational component equations are exactly the v73 equations, including the scalar, comparison, contact, trace and pole equations and the detector assignments. The five unit equations bring the total to 167 quadrics. No division by a possibly zero point ordinate is added.

`check_transfer.py` compares the complete physical rows directly against v73, verifies the unique unit-chart parametrization, and binds the coordinate counts and input-preserving renumbering. The full manuscript reproduces the inherited arithmetic proof and states its retained foundations.

## Why the coefficient bound improves

In the final 193-coordinate numbering, substitute `old X_i = new X_i/C` for

```text
44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 99, 100.
```

Leave all other coordinates, including the input, unchanged. Divide each transformed row by its smallest parameter power. The result has integer coefficients and parameter degree at most one in every quadratic row; its squared sum has parameter degree two. Since `C != 0`, these operations give an explicit rational bijection preserving the input.

The height proof holds for every real `C >= 149`. Write `J=K` or `J=L` for the constant of the chosen basis. The largest constant coefficient is `J`, the largest quadratic coefficient is `22201 = 149^2`, and all pure linear coefficients are bounded by `M = 384444691473074`, with `M^2 <= 22201*J`. The five coefficients involving multiple parameter powers are `289*C^2-578` and four coefficients `A+C^2`; each positive constant satisfies `22201*A <= 22200*J`. The first such `A` differs between the bases; the manuscript and independent review record both values. These integer inequalities bound every coefficient by `max(J,22201*C^2)`, and an occurring pure coefficient attains the bound. The sole coefficient with signs of both kinds is positive for `C >= 149`, so all support counts are exact for every `N >= 1`.

## Reproduce and independently verify

From the repository root:

```sh
python computation/quartic/seven_units193_v74/build.py
python computation/quartic/seven_units193_v74/verify_height.py
python computation/quartic/seven_units193_v74/build_scaled.py
python computation/quartic/seven_units193_v74/check_scaled.py
python computation/quartic/seven_units193_v74/check_support.py --output computation/quartic/seven_units193_v74/support-certificate.json
python computation/quartic/seven_units193_v74/check.py --folder computation/quartic/seven_units193_v74/primitive --primitive-reference --output computation/quartic/seven_units193_v74/primitive/independent-verification.json
python computation/quartic/seven_units193_v74/check.py --folder computation/quartic/seven_units193_v74/fewer_monomials --output computation/quartic/seven_units193_v74/fewer_monomials/independent-verification.json
python computation/quartic/seven_units193_v74/check_arithmetic.py
python computation/quartic/seven_units193_v74/check_transfer.py
```

The construction, support, parameter transfer and height checkers use the Python standard library. The independent physical-row checker and finite arithmetic checks use SymPy 1.14.0. No solver is needed to verify the stored certificate. `search.py` optionally reproduces an unbounded integral-weight search using Z3; the proof consists of the exact certificate and its independent verification, not the solver's verdict.

## Scope

The retained physical arithmetic uses the elliptic group description, scalar extraction, modular contact height, positive elliptic trace height, prepared actual-input pole realization, and simultaneous prime-pattern interfaces listed in the full manuscript. The exact finite certificates establish the algebra, all coefficient identities, degree, support, unit boundary and claimed coefficient heights. They do not complete an independent audit of those imported foundations, supply an effective defining parameter, or establish the separate 21- or 9-variable global rational-realization targets.
