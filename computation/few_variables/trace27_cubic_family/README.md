# A computable 27-variable family

This module specifies polynomials `F_L` in **27 total variables**, including the input, with **degree at most `2^158`**. The fixed odd integer `L >= 3` changes integer coefficients; it is not a quantified variable.

Under the four arithmetic inputs identified in the accompanying paper, **every sufficiently large odd `L` defines the integers over the rationals**. The proof uses von Buhren's height theorem, whose additive constant is ineffective. **No numerical sufficient threshold is known.** Generating or verifying one numerical member does not establish that this member defines the integers.

## Mathematical construction

The source retains 26 rational coordinates: one input, 18 square-root-abscissa coordinates, one slope, four comparison-pole parameters, and two scalar-pole parameters. Nine monic quartic point roots and three quadratic pole roots are eliminated with one additional rational coordinate. Three finite conic-chart bits give eight source cases. The maximum finite-algebra rank is `2^21`.

Every point uses `x=h^2`, `j^2=h^4-D`, and `y=h*j` with two retained rational components of `h`. The source group statement and elementary 2-isogeny descent show that this describes precisely the nonzero integer multiples of the source point. The adaptive multiplier `jprime=((2*A+B)-(A+B)*sqrt(2))*j`, with `j^2=A+B*sqrt(2)`, permits a single monic quartic reconstruction chart for every nonzero `j`. If `j=u+v*sqrt(2)`, its rational component is `2*(u^3-2*v^3)`, which cannot vanish because 2 is not a rational cube. Its multiplier norm is `2*A^2-B^2`, which is nonzero unless `A=B=0`. Thus the chart adds no arithmetic assumption, retained coordinate, or finite source branch.

The two comparison scales are one and the square of the sum of the four elliptic abscissa traces. The scalar contact is

```text
ell = 76249
beta = 216*X^4 + 450459
r = beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)
C_L = 17*(ell^((L+1)/2) + 1)
R_L = 102^2*ell^L*r/(1 + C_L*r)^2
```

The complete polynomial is specified by finite coefficient operations, determinants, resultants, traces, and finite products. Formal algebra generators and matrix coordinates are not quantified variables.

## Reproduction

Python 3 and its standard library suffice. From this directory run:

```sh
python3 reproduce.py --anchor-exponent 137731
```

This rebuilds the packaged example, checks its source and integer polynomial specification independently, and verifies the uniform degree bound using two independent coefficient symbols. Temporary output is removed after the check. To retain generated data, add `--output /absolute/output/directory`.

The individual stages are:

```sh
python3 build_forced_prime_source.py --anchor-exponent 137731 --output generated/source.json.gz
python3 check_forced_prime_source.py generated/source.json.gz
python3 compile_source.py generated/source.json.gz --output generated
python3 verify_specification.py generated/source.json.gz generated/polynomial-specification.json
python3 verify_family_degree.py
```

The independent `check_direct_points.py` verifies all nine new point charts by polynomial identities over `Z[h0,h1,Y]`. The source checker also verifies both abscissa sums, their trace and squared scale, the scalar normalization identity, all 76,249 residue classes, the coordinate inventory, and unchanged arithmetic methods. The separate polynomial checker imports no producer and verifies every finite-algebra conversion, the three quadratic zero/nonzero cases, guard coverage, and the degree majorant. The uniform-degree checker treats both powers of `ell` as independent integer coefficient symbols of degree zero and recomputes the degree recurrence independently. It makes no coefficient-height assertion for an unknown sufficiently large exponent.

## Packaged example and theorem status

`example_L137731/` contains a fully specified algebraic example and its certificates. Its source DAG has 7,369 nodes; the compiled integer coefficient DAG has 3,032 nodes. The independent verification covers nine point quartics, three rational-square clearings, and 101 atomic guard factors.

The example has verified degree at most `2^158` and coefficient height at most `2^(2^168)`. These bounds describe that numerical example. **The example is not certified to define the integers**, because the sufficient exponent threshold is ineffective. The proved defining-polynomial result is the existence theorem for all sufficiently large odd exponents, with its uniform degree bound.

`inherited-method-reference.json` records unchanged methods inherited from the frozen 29-variable source; it is deliberately retained as a provenance certificate. `family-semantic-reference.json` records the unchanged surrounding comparison code and the new sum-trace block. `baseline-provenance.json` identifies the exact inherited files before these documented changes.

## Main files

| File | Role |
|---|---|
| `build_forced_prime_source.py` | Builds an exact coefficient-family source |
| `check_forced_prime_source.py` | Independently checks the changed source identities and inherited methods |
| `check_direct_points.py` | Independently verifies the direct point quartics and every coordinate recovery |
| `compile_source.py` | Compiles the guarded finite algebra to a single-polynomial specification |
| `verify_specification.py` | Independently verifies the coefficient conversion and all bounds for a numerical member |
| `verify_family_degree.py` | Proves the degree bound uniformly in both coefficient symbols |
| `degree-family-verification.json` | Uniform degree certificate |
| `reproduce.py` | Runs all stages and checks the packaged example byte for byte |
| `example_L137731/` | Numerical algebraic example, with explicit status metadata |

The module does not computationally verify the four deep arithmetic inputs or remove the ineffectivity in von Buhren's theorem.
